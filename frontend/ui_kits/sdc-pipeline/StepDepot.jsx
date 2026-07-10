/* Étape 1 — Dépôt : chargement du classeur de métadonnées à analyser. */
const DDS = window.SDCMetadataDesignSystem_967a78;

function StepDepot({ file, onSelect, onRemove, onNext }) {
  return (
    <div className="sdc-step">
      <div className="sdc-step__intro">
        <img className="sdc-step__pic" src="../../assets/pictograms/document-add.svg" alt="" aria-hidden="true" />
        <div>
          <h1 className="sdc-h1">Déposez votre classeur de métadonnées</h1>
          <p className="sdc-lead">
            Glissez un fichier <b>.ods</b>, <b>.xlsx</b> ou <b>.csv</b> décrivant les tableaux statistiques
            demandés. Le modèle le lit, vous pose des questions si nécessaire, puis produit un tableau
            normalisé prêt pour la pose du secret.
          </p>
        </div>
      </div>

      <DDS.FileUpload
        file={file ? { name: file.name, size: file.raw.size } : null}
        onSelect={(f) => onSelect({ raw: f, name: f.name })}
        onRemove={onRemove}
        pictogramSrc="../../assets/pictograms/data-visualization.svg"
      />

      <DDS.Alert type="warning" title="Ne transmettez jamais d'informations sensibles ou confidentielles.">
        Ce formulaire est exclusivement réservé aux métadonnées décrivant des tableaux statistiques.
        Vérifiez votre fichier avant de l'envoyer&nbsp;: il ne doit contenir aucune donnée individuelle,
        ni micro-donnée, ni information à caractère personnel.
      </DDS.Alert>

      <div className="sdc-actions">
        <DDS.Button icon="ri-play-line" disabled={!file} onClick={onNext}>
          Lancer l'analyse
        </DDS.Button>
      </div>
    </div>
  );
}

window.StepDepot = StepDepot;
