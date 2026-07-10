# UI kit — SDC pipeline

Interface DSFR (React via Babel standalone, sans build) pour le pipeline d'analyse des
métadonnées SDC. Elle guide un agent à travers les quatre étapes du pipeline et dialogue
avec le backend Flask (`app.py`, servi depuis `frontend/`).

## Étapes

1. **Dépôt** (`StepDepot.jsx`) — dépôt du classeur (`.ods` / `.xlsx` / `.csv`) → `POST /api/upload`.
2. **Questions** (`StepQuestions.jsx`) — réponses aux questions de la Phase 1 → `POST /api/answer`.
   Si le modèle n'a aucune question, l'étape est franchie automatiquement.
3. **Vérification** (`StepVerification.jsx`) — Markdown sérialisé + tableau normalisé validé.
4. **Export** (`StepExport.jsx`) — téléchargement du `.csv` → `POST /api/export`.

## Fichiers

- `index.html` — page hôte ; charge le design system (`../../_ds_bundle.js`), les données de
  démonstration (`data.js`) puis les composants dans l'ordre, et monte `<App />`.
- `Shell.jsx` — en-tête / pied de page / `Layout`.
- `App.jsx` — orchestrateur : état, appels `fetch`, navigation entre étapes.
- `Step*.jsx` — les quatre étapes ; chacune s'expose sur `window`.
- `data.js` — jeu de données factice (`window.SDC_DATA`) pour prévisualiser le kit hors backend.

Les composants du design system (`Button`, `Card`, `Stepper`, `Table`, `Alert`, `Badge`, `Tag`,
`FileUpload`) proviennent de `window.SDCMetadataDesignSystem_967a78` (fourni par `_ds_bundle.js`).

## Lancer

```bash
uv run python app.py   # puis http://127.0.0.1:5000/
```
