# metadata-analysis-llm-for-sdc

Utilisation d'un LLM pour analyser des fichiers de métadonnées décrivant la publication de
tableaux statistiques, et les rendre exploitables par l'analyse automatique et la pose du secret
via **rtauargus**.

À partir d'un classeur de métadonnées (un producteur décrit les tableaux qu'il demande), le
pipeline produit un tableau plat normalisé.

---

 TODO: Comment utiliser l'app: 
 aller sur le browser et copier l'adresse suivante: sdc-metadata.lab.sspcloud.fr
 Entrez le username et le mot de passe qui vous a été fourni. 

 --- 


# Comment lancer l'application en local. 

## Sur SSP Cloud (Onyxia)

1. Ouvrir Onyxia sur le SSPCloud et se connecter.
2. Lancer un service **VSCode-python** avec :
   - le nom de la clé API personnelle (comme appelée dans « Secrets » sur Onyxia — pas la clé elle-même) dans la rubrique **« Secret »** de Vault. Plus d'informations ci-dessous pour créer votre clé API personnelle.
   - le repo `https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc.git` dans la rubrique **« Repository »** de Git. Plus d'informations ci-dessous pour créer votre Token sur Git.
   - cliquer sur **« Network access »** → **« Enable access to your service through specific ports »**. Par défaut Onyxia choisit Port 1 = 5000 (mettre la valeur 5000 si ce n'est pas déjà le cas).
   - Dans 'Role', activez le bouton 'Enabled' et choisissez, le role 'admin'.
3. Lancer le service.
4. Une fois VSCode ouvert, ouvrir un nouveau terminal, puis :

```{bash}
cd metadata-analysis-llm-for-sdc
uv sync
```

# Lancer l'app en local

```{bash}
uv run python backend/app.py
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

## Créer un compte DockerHub (https://hub.docker.com/) et génerer un token. 
TODO: explain how to create the token in dockerhub 

## Command-line Interface

```{bash}
uv run python backend/main.py your_input_file.ods -o your_output_file.csv
```

! Cette commande lance le pipeline et créer your_output_file.csv dans le repo. A utiliser seulement par ceux qui prennent le code en main, pas ceux qui veulent simplment utiliser l'app. Si vous voulez utiliser l'app veuillez vous référer à la section ' Comment utiliser l'app '

# Reprendre le code en main 

**NB: **Avant de commencer à explorer la partir suivante, veuillez vous référer à la sous-partie 'Sur le SSP Cloud (Onyxia)' de la partie 'Comment lancer l'application en local.' Suivez ces instructions pour lancer votre service**

## Structure du repo git: 

TODO: Here I need a diagram that shows clearly the structure, which files are where (without showing the complete path of course, just visually)

## Role de chaque fichier. 

TODO: Have a table that explains in 1 line  what that file does for each script in the following way (the repo is pretty clean in that regard but better have good and thorough doc too): 
for backend, have a line for each python script: app.py main.py and each file in src
for frontend, have a line for: each file inside ui_kits/sdc-pipeline, tokens and assets as folders, _ds_bundle.js, styles.css
have a line for Dockerfile 
have a line for .github/workflows/docker.yaml 
have a line for each of the yaml files inside deploy 

The other files (uv, ignores, python version) are config files that are not to be explained in this part. 

## packages et dépendances. 

TODO: Create another table that lists the dependencies and packages managed by uv, one line to explain why each. 

