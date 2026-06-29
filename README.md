# metadata-analysis-llm-for-sdc

Utilisation d'un LLM pour analyser des fichiers de métadonnées décrivant la publication de
tableaux statistiques, et les rendre exploitables par l'analyse automatique et la pose du secret
via **rtauargus**.

À partir d'un classeur de métadonnées (un producteur décrit les tableaux qu'il demande), le
pipeline produit un tableau plat normalisé (`.csv` pour relecture humaine, `.rds` pour rtauargus).

---

# Getting started

```{bash}
git clone https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc
cd metadata-analysis-llm-for-sdc
uv sync
```

# Lancer le code

## CLI

```{bash}
uv run python main.py
```

## UI

```{bash}
uv run python app.py
```

## Notebook

Pour activer l'exécution interactive du code, pointe VSCode vers l'environnement virtuel du projet :

1. Ouvre la palette de commandes avec Ctrl+Shift+P (Windows/Linux) ou Cmd+Shift+P (Mac)
2. Recherche et lance >Python: Select Interpreter
3. Choisis Enter interpreter path… et entre : /home/onyxia/work/funathon-project3/.venv/bin/python