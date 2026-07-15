# metadata-analysis-llm-for-sdc

Utilisation d'un LLM pour analyser des fichiers de métadonnées décrivant la publication de
tableaux statistiques, et les rendre exploitables par l'analyse automatique et la pose du secret
via **rtauargus**.

À partir d'un classeur de métadonnées (un producteur décrit les tableaux qu'il demande), le
pipeline produit un tableau plat normalisé (`.csv` pour relecture humaine, `.rds` pour rtauargus).

---

# Getting started

## Sur SSP Cloud (Onyxia)

1. Ouvrir Onyxia sur le SSPCloud et se connecter.
2. Lancer un service **VSCode-python** avec :
   - le nom de la clé API personnelle (comme appelée dans « Secrets » sur Onyxia — pas la clé elle-même) dans la rubrique **« Secret »** de Vault.
   - le repo `https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc.git` dans la rubrique **« Repository »** de Git.
   - cliquer sur **« Network access »** → **« Enable access to your service through specific ports »**. Par défaut Onyxia choisit Port 1 = 5000 (mettre la valeur 5000 si ce n'est pas déjà le cas).
3. Lancer le service.
4. Une fois VSCode ouvert, ouvrir un nouveau terminal, puis :

```{bash}
cd metadata-analysis-llm-for-sdc
uv sync

# Lancer l'app

```{bash}
uv run python app.py
```

**Important**: Quand l'application est lancée : ne pas cliquer sur le popup de VSCode. Retourner sur « Mes services » dans Onyxia, cliquer sur « Ouvrir » pour le service en cours, puis cliquer sur « ce lien » après « Vous pouvez vous connecter à votre port personnalisé (5000) en utilisant ce lien ».

## Command-line Interface

```{bash}
uv run python main.py
```

## Notebook

Pour activer l'exécution interactive du code, pointe VSCode vers l'environnement virtuel du projet :

1. Ouvre la palette de commandes avec Ctrl+Shift+P (Windows/Linux) ou Cmd+Shift+P (Mac)
2. Recherche et lance >Python: Select Interpreter
3. Choisis Enter interpreter path… et entre : /home/onyxia/work/funathon-project3/.venv/bin/python