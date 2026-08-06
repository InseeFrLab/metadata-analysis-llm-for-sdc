# metadata-analysis-llm-for-sdc

Utilisation d'un LLM pour analyser des fichiers de métadonnées décrivant la publication de
tableaux statistiques, et les rendre exploitables par l'analyse automatique et la pose du secret
via **rtauargus**.

À partir d'un classeur de métadonnées (un producteur décrit les tableaux qu'il demande), le
pipeline produit un tableau plat normalisé.

---

 # Comment utiliser l'app : 
 Ouvrez votre navigateur et copiez l'adresse suivante : sdc-metadata.lab.sspcloud.fr, puis
 entrez le nom d'utilisateur et le mot de passe qui vous ont été fournis. 

 --- 


# Comment lancer l'application en local. 

## Sur SSP Cloud (Onyxia)

1. Ouvrir Onyxia sur le SSP Cloud et se connecter.
2. Lancer un service **VSCode-python** avec :
   - le nom de la clé API personnelle (tel qu'il apparaît dans « Secrets » sur Onyxia — pas la clé elle-même) dans la rubrique **« Secret »** de Vault. Plus d'informations ci-dessous pour créer votre clé API personnelle.
   - le dépôt `https://github.com/InseeFrLab/metadata-analysis-llm-for-sdc.git` dans la rubrique **« Repository »** de Git. Plus d'informations ci-dessous pour créer votre token sur GitHub.
   - cliquer sur **« Network access »** → **« Enable access to your service through specific ports »**. Par défaut Onyxia choisit Port 1 = 5000 (mettre la valeur 5000 si ce n'est pas déjà le cas).
   - Dans « Role », activez le bouton « Enabled » et choisissez le rôle « admin ».
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

**Important** : une fois l'application lancée, ne pas cliquer sur la fenêtre contextuelle de VSCode. Retourner sur « Mes services » dans Onyxia, cliquer sur « Ouvrir » pour le service en cours, puis cliquer sur « ce lien » après « Vous pouvez vous connecter à votre port personnalisé (5000) en utilisant ce lien ».

!! Ce pipeline n'est pas encore équipé pour traiter tous les cas, si vous avez configuré votre service correctement et que vous voyez une erreur apparaître, cliquez à nouveau sur le bouton de la phase où vous êtes !!

## Créer une clé API sur le SSP Cloud. 
1) Se connecter à Onyxia.
2) Appuyer sur AI Chat en haut à droite de la page.
3) Cliquer sur le Profil, en haut à droite, puis sur réglages --> compte --> Clés d'API
4) Copier la valeur de cette clé. 
5) Revenir sur Onyxia et cliquer sur Secrets --> Nouveau secret. Appeler celui-ci « llm ».
6) Rentrer dans le secret. Copier la valeur de la clé dans « Valeur », et « CLE_API_OPENWEBUI » dans « Nom de la variable ».

## Créer un token sur GitHub
Pour créer un token GitHub, allez dans les paramètres de votre compte, sélectionnez « Developer settings » puis « Personal access tokens » (tokens classic), et générez le token.

## Créer un compte DockerHub (https://hub.docker.com/) et génerer un token. 
Connectez-vous sur hub.docker.com, cliquez sur votre avatar en haut à droite puis sur « Account Settings ». Dans le menu de gauche, cliquez sur « Personal access tokens », puis sur « Generate new token ». Donnez-lui une description, choisissez une date d'expiration (ou « None ») et la permission « Read & Write », puis cliquez sur « Generate ». Copiez immédiatement le token affiché : il ne sera plus jamais visible ensuite. Il servira de valeur au secret `DOCKERHUB_TOKEN` du dépôt GitHub (utilisé par `.github/workflows/docker.yaml`), aux côtés de `DOCKERHUB_USERNAME` pour votre nom d'utilisateur.

## Command-line Interface

```{bash}
uv run python backend/main.py your_input_file.ods -o your_output_file.csv
```

! Cette commande lance le pipeline et crée your_output_file.csv dans le dépôt. À utiliser seulement par ceux qui prennent le code en main, pas ceux qui veulent simplement utiliser l'app. Si vous voulez utiliser l'app, veuillez vous référer à la section « Comment utiliser l'app ».

# Reprendre le code en main 

**NB :** Avant de commencer à explorer la partie suivante, veuillez vous référer à la sous-partie « Sur le SSP Cloud (Onyxia) » de la partie « Comment lancer l'application en local. » Suivez ces instructions pour lancer votre service.

## Structure du repo git: 

Arborescence complète du dépôt :

```
metadata-analysis-llm-for-sdc/
├── .github/
│   └── workflows/
│       └── docker.yaml
├── backend/
│   ├── src/
│   │   ├── prompts/
│   │   ├── schema/
│   │   ├── __init__.py
│   │   ├── clean.py
│   │   ├── data.py
│   │   ├── extract_JSON_array.py
│   │   ├── LLM_API_call.py
│   │   ├── transform_input.py
│   │   ├── transform_output.py
│   │   └── validate_json_output.py
│   ├── app.py
│   └── main.py
├── deploy/
│   ├── deployment.yaml
│   ├── ingress.yaml
│   └── service.yaml
├── frontend/
│   ├── assets/
│   │   ├── fonts/
│   │   ├── pictograms/
│   │   └── logo-insee.png
│   ├── tokens/
│   ├── ui_kits/
│   │   └── sdc-pipeline/
│   │       ├── App.jsx
│   │       ├── data.js
│   │       ├── index.html
│   │       ├── README.md
│   │       ├── Shell.jsx
│   │       ├── StepDepot.jsx
│   │       ├── StepExport.jsx
│   │       ├── StepQuestions.jsx
│   │       └── StepVerification.jsx
│   ├── _ds_bundle.js
│   └── styles.css
├── .dockerignore
├── .gitignore
├── .python-version
├── Dockerfile
├── pyproject.toml
├── README.md
└── uv.lock
```

## Role de chaque fichier. 

**Backend**

| Fichier | Rôle |
|---|---|
| `backend/app.py` | Serveur Flask : expose l'API (`/api/upload`, `/api/answer`, `/api/export`, `/api/jobs/<id>`) et sert l'interface statique du dossier `frontend/`. |
| `backend/main.py` | Interface en ligne de commande : exécute le pipeline complet sur un fichier local et écrit un CSV. |
| `backend/src/LLM_API_call.py` | Configure et appelle le LLM (client OpenAI), et construit les messages de relance/correction envoyés au modèle. |
| `backend/src/clean.py` | Nettoie les cellules et les lignes des feuilles extraites (espaces, sauts de ligne, lignes/cellules vides en fin de feuille). |
| `backend/src/data.py` | Lit les classeurs de métadonnées (en local ou sur S3/MinIO) et détecte leur type de fichier (.ods/.xlsx/.csv). |
| `backend/src/extract_JSON_array.py` | Extrait le tableau JSON brut de la réponse texte du modèle. |
| `backend/src/transform_input.py` | Convertit les feuilles nettoyées en Markdown, au format attendu par le prompt. |
| `backend/src/transform_output.py` | Dérive les colonnes « spanning » (variables de croisement) à partir des enregistrements validés. |
| `backend/src/validate_json_output.py` | Valide les enregistrements JSON produits par le modèle par rapport au schéma de sortie. |
| `backend/src/__init__.py` | Fichier vide qui fait de `src` un package Python. |
| `backend/src/prompts/prompt_questions.md` | Prompt système qui pilote les deux phases du pipeline (questions puis JSON). |
| `backend/src/schema/sdc_output.schema.json` | Schéma JSON définissant le contrat de sortie attendu du modèle. |

**Frontend**

| Fichier / dossier | Rôle |
|---|---|
| `frontend/ui_kits/sdc-pipeline/index.html` | Page hôte : charge le design system et les données de démonstration, puis monte l'application React. |
| `frontend/ui_kits/sdc-pipeline/App.jsx` | Orchestrateur de l'application : état, appels à l'API, navigation entre les quatre étapes. |
| `frontend/ui_kits/sdc-pipeline/Shell.jsx` | En-tête, pied de page et mise en page générale (`Layout`). |
| `frontend/ui_kits/sdc-pipeline/StepDepot.jsx` | Étape 1 — dépôt du classeur de métadonnées. |
| `frontend/ui_kits/sdc-pipeline/StepQuestions.jsx` | Étape 2 — questions du modèle et saisie des réponses du producteur. |
| `frontend/ui_kits/sdc-pipeline/StepVerification.jsx` | Étape 3 — aperçu du Markdown sérialisé et du tableau normalisé. |
| `frontend/ui_kits/sdc-pipeline/StepExport.jsx` | Étape 4 — téléchargement du tableau normalisé au format CSV. |
| `frontend/ui_kits/sdc-pipeline/data.js` | Jeu de données factice, utilisé pour prévisualiser l'interface sans backend. |
| `frontend/ui_kits/sdc-pipeline/README.md` | Documentation de ce kit d'interface (étapes, fichiers, lancement). |
| `frontend/tokens/` (dossier) | Variables de design (couleurs, typographie, espacements, polices) du DSFR. |
| `frontend/assets/` (dossier) | Ressources statiques : logo Insee, pictogrammes et polices. |
| `frontend/_ds_bundle.js` | Bibliothèque de composants d'interface (bouton, tableau, alerte...) partagée par toutes les étapes. |
| `frontend/styles.css` | Point d'entrée CSS : importe les fichiers de `tokens/`. |

**Déploiement et intégration continue**

| Fichier | Rôle |
|---|---|
| `Dockerfile` | Construit l'image Docker de l'application (étape de build des dépendances, puis image d'exécution). |
| `.github/workflows/docker.yaml` | Workflow GitHub Actions qui construit et publie l'image Docker sur DockerHub à chaque push sur `main`. |
| `deploy/deployment.yaml` | Déploiement Kubernetes : démarre le conteneur de l'application. |
| `deploy/ingress.yaml` | Ingress Kubernetes : expose l'application sur `sdc-metadata.lab.sspcloud.fr`, avec authentification basique. |
| `deploy/service.yaml` | Service Kubernetes : expose le déploiement en interne sur le port 5000. |

Les autres fichiers (`uv.lock`, `.gitignore`, `.dockerignore`, `.python-version`...) sont des fichiers de configuration qui ne sont pas détaillés dans cette partie. 

## packages et dépendances. 

| Paquet | Pourquoi |
|---|---|
| `flask` | Framework web utilisé pour exposer l'API et servir l'interface. |
| `gunicorn` | Serveur WSGI de production utilisé pour lancer l'application dans le conteneur (voir `Dockerfile`). |
| `jsonschema` | Valide le tableau JSON produit par le modèle par rapport au schéma de sortie attendu. |
| `odfpy` | Permet la lecture des classeurs au format `.ods`. |
| `openai` | Client utilisé pour appeler le LLM (compatible avec l'API OpenAI). |
| `openpyxl` | Permet la lecture des classeurs au format `.xlsx`. |
| `pandas` | Manipulation des données tabulaires : lecture des feuilles, nettoyage, transformation. |
| `pyreadr` | Lecture/écriture de fichiers R (`.rds`), en prévision de l'export au format RDS (pas encore disponible dans l'app). |
| `python-dotenv` | Charge les variables d'environnement depuis un fichier `.env` en local. |
| `s3fs` | Accès aux fichiers stockés sur le stockage S3 (MinIO) du SSP Cloud. |
| `tabulate` | Formatage de tableaux pour un affichage lisible en ligne de commande. |
| `werkzeug` | Utilitaires HTTP sous-jacents à Flask (gestion des fichiers, exceptions...). |

