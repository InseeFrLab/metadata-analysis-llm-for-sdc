# metadata-analysis-llm-for-sdc

Utilisation d'un LLM pour analyser des fichiers de métadonnées décrivant la publication de
tableaux statistiques, et les rendre exploitables par l'analyse automatique et la pose du secret
via **rtauargus**.

À partir d'un classeur de métadonnées (un producteur décrit les tableaux qu'il demande), le
pipeline produit un tableau plat normalisé.

---

# Comment lancer l'application

## Sur SSP Cloud (Onyxia)

1. Ouvrir Onyxia sur le SSPCloud et se connecter.
2. Lancer un service **VSCode-python** avec :
   - le nom de la clé API personnelle (comme appelée dans « Secrets » sur Onyxia — pas la clé elle-même) dans la rubrique **« Secret »** de Vault. Plus d'informations ci-dessous pour créer votre clé API personnelle
   - le repo `https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc.git` dans la rubrique **« Repository »** de Git. Plus d'informations ci-dessous pour créer votre Token sur Git.
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

!! Ce pipeline n'est pas encore équipé pour traiter de tous les cas, si vous avez configuré votre service correctement et que vous voyez une erreur apparaître, cliquez à nouveau sur le bouton de la phase où vous êtes !!

## Créer une clé API sur le SSPCloud. 
1) Se connecter à Onyxia.
2) Appuyer sur AI Chat en haut à droite de la page.
3) Cliquer sur le Profile haut à droite, puis sur réglages --> compte --> Clés d'API
4) Copier la valeur de cette clé. 
5) Revenir sur Onyxia et cliquer sur Secrets --> Nouveau secret. Appler celui-ci "llm".
6) Rentrer dans le secret. Copier la valeur de la clé dans "Valeur"; et "CLE_API_OPENWEBUI" pour " Nom de la variable.

## Créer un token sur git
Pour créer un token GitHub, allez dans les paramètres de votre compte, sélectionnez "Developer settings" puis "Personal access tokens", (tokens classic) et générez le token.

## Command-line Interface

```{bash}
uv run python main.py your_input_file.ods -o your_output_file.csv
```

! This command runs the pipeline and saves the result inside metadata-analysis-llm-for-sdc