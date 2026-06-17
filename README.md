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

## Utilisation

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
  user/analyse_LLM_metadata/data_tables/sujets.ods \
  user/analyse_LLM_metadata/output/sujets.csv
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