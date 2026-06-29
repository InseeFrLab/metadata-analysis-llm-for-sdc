/* Étape 1 — Dépôt : sélection et envoi du classeur de métadonnées. */
const VDS = window.SDCMetadataDesignSystem_967a78;
const { useState: useDepotState, useRef: useDepotRef } = React;

function StepDepot({ file, onSelect, onRemove, onNext }) {
  const inputRef = useDepotRef(null);
  const [dragOver, setDragOver] = useDepotState(false);

  function handleFileChange(e) {
    const f = e.target.files[0];
    if (f) onSelect({ raw: f, name: f.name });
    e.target.value = "";
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) onSelect({ raw: f, name: f.name });
  }

  return (
    <div className="sdc-step">
      <div className="sdc-step__intro">
        <img className="sdc-step__pic" src="../../assets/pictograms/document-add.svg" alt="" aria-hidden="true" />
        <div>
          <h1 className="sdc-h1">Déposez votre classeur de métadonnées</h1>
          <p className="sdc-lead">
            Formats acceptés : <b>.ods</b>, <b>.xlsx</b>, <b>.csv</b>. Taille maximale : 16&nbsp;Mo.
            Le classeur sera analysé par le modèle pour extraire et normaliser ses métadonnées.
          </p>
        </div>
      </div>

      <div
        onClick={() => !file && inputRef.current && inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        role={file ? undefined : "button"}
        tabIndex={file ? undefined : 0}
        aria-label="Zone de dépôt de fichier"
        onKeyDown={(e) => { if (!file && (e.key === "Enter" || e.key === " ")) inputRef.current && inputRef.current.click(); }}
        style={{
          border: "2px dashed " + (dragOver ? "var(--border-action-high)" : "var(--border-contrast)"),
          borderRadius: "var(--radius-md)",
          padding: "3rem 2rem",
          textAlign: "center",
          cursor: file ? "default" : "pointer",
          background: dragOver ? "var(--background-action-low)" : "var(--background-default)",
          transition: "background 0.15s, border-color 0.15s",
        }}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".ods,.xlsx,.csv"
          style={{ display: "none" }}
          onChange={handleFileChange}
        />
        {file ? (
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "1rem" }}>
            <i className="ri-file-excel-2-line" style={{ fontSize: "2rem", color: "var(--text-action-high)" }} aria-hidden="true"></i>
            <div style={{ textAlign: "left" }}>
              <p style={{ margin: 0, fontWeight: "var(--fw-bold)", color: "var(--text-title)" }}>{file.name}</p>
              <p style={{ margin: 0, fontSize: "var(--text-sm)", color: "var(--text-mention)" }}>
                {(file.raw.size / 1024).toFixed(1)} Ko
              </p>
            </div>
            <VDS.Button
              variant="secondary"
              icon="ri-delete-bin-line"
              onClick={(e) => { e.stopPropagation(); onRemove(); }}
            >
              Supprimer
            </VDS.Button>
          </div>
        ) : (
          <div>
            <i className="ri-upload-cloud-line" style={{ fontSize: "3rem", color: "var(--text-mention)", display: "block", marginBottom: "1rem" }} aria-hidden="true"></i>
            <p style={{ margin: "0 0 .5rem", fontWeight: "var(--fw-medium)", color: "var(--text-title)" }}>
              Glissez un fichier ici ou cliquez pour parcourir
            </p>
            <p style={{ margin: 0, fontSize: "var(--text-sm)", color: "var(--text-mention)" }}>
              .ods · .xlsx · .csv — 16 Mo max
            </p>
          </div>
        )}
      </div>

      {file && (
        <VDS.Alert type="info" small title={"Fichier sélectionné : " + file.name}>
          Cliquez sur « Analyser le classeur » pour lancer l'extraction des métadonnées.
        </VDS.Alert>
      )}

      <div className="sdc-actions">
        <VDS.Button icon="ri-search-line" iconRight disabled={!file} onClick={onNext}>
          Analyser le classeur
        </VDS.Button>
      </div>
    </div>
  );
}

window.StepDepot = StepDepot;