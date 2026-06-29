# metadata-analysis-llm-for-sdc

Utilisation d'un LLM pour analyser des fichiers de métadonnées décrivant la publication de
tableaux statistiques, et les rendre exploitables par l'analyse automatique et la pose du secret
via **rtauargus**.

À partir d'un classeur de métadonnées (un producteur décrit les tableaux qu'il demande), le
pipeline produit un tableau plat normalisé (`.csv` pour relecture humaine, `.rds` pour rtauargus).

---

## Architecture

Un seul maillon est probabiliste (l'appel au LLM) ; tout le reste est déterministe et auditable :

```
classeur (.ods/.xlsx/.csv)
   → [transform_input.serialize]   déterministe   → Markdown
   → [LLM + prompts/prompt_questions.md]  PROBABILISTE  → JSON
        Phase 1 : questions au producteur (ou JSON direct si aucune question)
        Phase 2 : réponses → JSON final
   → [verify_json_output.validate]  déterministe  → JSON validé contre le schéma
   → [transform_output.write_csv/rds] déterministe → .csv (humain) + .rds (rtauargus)
```

Même JSON en entrée → tables identiques en sortie : le tableau remis à rtauargus est reproductible.

### Modules (`core/`)

| Module | Rôle |
|---|---|
| `transform_input.py` | Classeur → Markdown. **Sérialiseur canonique** (stdlib pour `.ods`/`.csv`, openpyxl pour `.xlsx`). |
| `llm_client.py` | Appel multi-tour à Qwen sur SSP Cloud (API compatible OpenAI), `temperature=0`. |
| `pipeline.py` | Orchestrateur en deux phases : `serialize → start → answer → to_csv`. |
| `verify_json_output.py` | Découpe le tableau JSON d'une réponse (`[ … ]`) **et** le valide contre `schema/sdc_output.schema.json` (échoue bruyamment). |
| `transform_output.py` | JSON validé → `.csv` (convention NA-vs-vide) + `.rds` (NA R). |

`cli.py` (racine) est le pilote terminal unique : fichiers locaux par défaut, ou Onyxia S3 avec `--s3`.

---

## Installation

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Les versions sont épinglées (`==`) pour la reproductibilité. Les étapes déterministes
(sérialisation / validation / CSV) ne nécessitent presque rien ; seul l'appel au modèle a besoin
du SDK OpenAI.

### Clé d'API (uniquement pour les appels au modèle)

Créez un `.env` (non versionné) à la racine :

```dotenv
CLE_API_OPENWEBUI=...           # ou OPENAI_API_KEY=...
# LLM_MODEL=qwen3-6-35b-moe     # facultatif
```

---

## Mise en place sur Onyxia

Pour utiliser ce dépôt sur **Onyxia / SSP Cloud** :

1. Lancer un service **VSCode-python**.
2. Dans les paramètres du service, onglet **« Git »** → renseigner l'URL du dépôt dans
   **« Repository URL »** :
   `https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc.git`
3. Onglet **« Environment variables »** → **« Ajouter »** une variable nommée **exactement
   `CLE_API_OPENWEBUI`** , et y coller la valeur de la clé API.
   > ⚠️ Un nom différent (`CLE_API_OPENWEB`, etc.) provoque l'erreur *« No API key found »*.
   > `OPENAI_API_KEY` est aussi accepté comme nom alternatif.
4. Une fois le service lancé, ouvrir un terminal dans VSCode et installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
5. Le service est prêt — lancez le pipeline (voir **Utilisation** ci-dessous).

**URL du modèle — rien à changer.** Par défaut, `core/llm_client.py` pointe déjà vers la passerelle
LLM de SSP Cloud (`https://llm.lab.sspcloud.fr/api/v1`), soit exactement l'endpoint d'Onyxia. Pour
surcharger sans toucher au code (par ex. si le nom du modèle `qwen3-6-35b-moe` change), définissez
les variables d'environnement `LLM_BASE_URL` et/ou `LLM_MODEL`. Il faut bien évidemment changer le nom du modèle
au modèle utilisé.

**S3 / MinIO.** Onyxia injecte automatiquement les identifiants S3 (`AWS_S3_ENDPOINT`,
`AWS_ACCESS_KEY_ID`, …) : rien à configurer pour le drapeau `--s3` de `cli.py`. Ce mode
requiert `s3fs`, qui n'est pas dans `requirements.txt` ; il est généralement pré-installé sur
l'image Onyxia (au besoin : `pip install s3fs`).

---

## Utilisation

> **Démo / présentation.** `notebook/demo_pipeline_for_minio.ipynb` déroule le pipeline de bout
> en bout sur un exemple, en conditions réelles sur Onyxia (appel au modèle + lecture/écriture
> MinIO) : la clé API et l'accès S3 sont donc requis (voir ci-dessous). Dépendances :
> `pip install -r requirements-notebook.txt`.

### Hors-ligne (aucune clé, aucune modèle)

```bash
# Sérialiser un classeur en Markdown et s'arrêter (ce que verrait le modèle) :
python cli.py meta.ods --serialize-only

# Rejouer une réponse LLM sauvegardée → CSV (chemin déterministe pur) :
python cli.py --reply reply.txt -o out/run1     # écrit out/run1.csv
```

### Run complet (nécessite la clé)

```bash
python cli.py meta.ods -o out/run1
# Phase 1 : si le modèle pose des questions, répondez (ligne vide pour terminer).
# Phase 2 : le JSON est produit, validé, puis écrit en CSV.
```

### Sur MinIO (Onyxia) — drapeau `--s3`

Le **même** `cli.py` lit et écrit sur S3 lorsqu'on ajoute `--s3` : `input` et `--output`
sont alors des **clés S3** (et non des chemins locaux). Les identifiants sont injectés par
Onyxia. Nécessite `s3fs` (voir ci-dessus).

```bash
# Prévisualisation Markdown d'un fichier S3 (vers stdout) :
python cli.py user/data/meta.ods --s3 --serialize-only

# Pipeline complet, S3 → S3 :
python cli.py user/data/meta.ods --s3 -o user/output/meta.csv
# Sans -o, la sortie est écrite à côté de l'entrée : user/data/meta.csv
```

**Sauvegarder le résultat en local.** Le mode `--s3` réécrit le CSV sur S3. Pour en garder une
copie locale, deux options :
- récupérer le fichier de sortie depuis S3 (interface Onyxia / `mc cp` / `s3fs`) ;
- ou exécuter le pipeline local `python cli.py meta.ods -o out/run1`, qui écrit directement
  `out/run1.csv` sur le disque.

--- 

## Reproductibilité

- **Déterministe de bout en bout sauf l'appel modèle** : même Markdown/JSON en entrée → mêmes
  fichiers en sortie.
- **Dépendances épinglées** (`requirements.txt`).
- **`temperature=0`** côté modèle pour minimiser (sans l'éliminer) la variabilité.
- La prévisualisation (`cli.py --serialize-only`, local ou `--s3`) utilise le même sérialiseur
  (`transform_input.serialize`) que le pipeline : ce que vous prévisualisez est exactement ce que
  le modèle reçoit.