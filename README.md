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
   → [read_input.serialize]        déterministe   → Markdown
   → [LLM + prompts/prompt_questions.md]  PROBABILISTE  → JSON
        Phase 1 : questions au producteur (ou JSON direct si aucune question)
        Phase 2 : réponses → JSON final
   → [extract_json.validate]       déterministe   → JSON validé contre le schéma
   → [json_to_table.write_csv/rds] déterministe   → .csv (humain) + .rds (rtauargus)
```

Même JSON en entrée → tables identiques en sortie : le tableau remis à rtauargus est reproductible.

### Modules (`core/`)

| Module | Rôle |
|---|---|
| `read_input.py` | Classeur → Markdown. **Sérialiseur canonique** (stdlib pour `.ods`/`.csv`, openpyxl pour `.xlsx`). |
| `llm_client.py` | Appel multi-tour à Qwen sur SSP Cloud (API compatible OpenAI), `temperature=0`. |
| `pipeline.py` | Orchestrateur en deux phases : `serialize → start → answer → to_csv`. |
| `jsonio.py` | Découpe/parse le tableau JSON d'une réponse (`[ … ]`). Source unique, sans dépendance. |
| `extract_json.py` | Validation du JSON contre `schema/sdc_output.schema.json` (échoue bruyamment). |
| `json_to_table.py` | JSON validé → `.csv` (convention NA-vs-vide) + `.rds` (NA R). |
| `table_to_md.py` | Wrapper de prévisualisation : délègue à `read_input.serialize` (même Markdown que le pipeline). |
| `run_on_minio.py` / `run_full_pipeline_on_minio.py` | Variantes lisant/écrivant sur MinIO (Onyxia). |

`cli.py` (racine) est le pilote terminal.

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
`AWS_ACCESS_KEY_ID`, …) : rien à configurer pour les scripts `core/run_*_on_minio.py`. Ces scripts
requièrent `s3fs`, qui n'est pas dans `requirements.txt` ; il est généralement pré-installé sur
l'image Onyxia (au besoin : `pip install s3fs`).

---

## Utilisation

> **Démo / présentation.** `notebooks/demo_pipeline.ipynb` déroule le pipeline de bout en bout
> sur un exemple, en **mode caché** (aucune clé ni MinIO requis). Voir
> `notebooks/cached/README.md`. Dépendances : `pip install -r requirements-notebook.txt`.

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

### Sur MinIO (Onyxia)

```bash
# Prévisualisation Markdown d'un fichier S3 :
python core/run_on_minio.py user/data/meta.ods user/data/meta.md

# Pipeline complet, S3 → S3 :
python core/run_full_pipeline_on_minio.py \
  user/[your_file_path_here]/example.ods \  # stockage des métadonnéees sur onyxia
  user/[your_file_output_path_here]/example.csv ## Stockage des fichiers output sur onyxia
```

**Sauvegarder le résultat en local.** `run_full_pipeline_on_minio.py` réécrit le CSV sur S3. Pour
en garder une copie locale, deux options :
- récupérer le fichier de sortie depuis S3 (interface Onyxia / `mc cp` / `s3fs`) ;
- ou exécuter le pipeline local `python cli.py meta.ods -o out/run1`, qui écrit directement
  `out/run1.csv` sur le disque.

--- 

## Reproductibilité

- **Déterministe de bout en bout sauf l'appel modèle** : même Markdown/JSON en entrée → mêmes
  fichiers en sortie.
- **Dépendances épinglées** (`requirements.txt`).
- **`temperature=0`** côté modèle pour minimiser (sans l'éliminer) la variabilité.
- La prévisualisation MinIO (`table_to_md.convert`) utilise désormais **le même** sérialiseur que
  le pipeline : ce que vous prévisualisez est exactement ce que le modèle reçoit.