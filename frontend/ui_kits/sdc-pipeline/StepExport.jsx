/* Étape 4 — Export du tableau normalisé (.csv pour relecture humaine et rtauargus). */
const EDS = window.SDCMetadataDesignSystem_967a78;

function Stat({ value, label }) {
  return (
    <div className="sdc-stat">
      <span className="sdc-stat__value">{value}</span>
      <span className="sdc-stat__label">{label}</span>
    </div>
  );
}

function StepExport({ records, fileName, sessionId, onRestart }) {
  const stem = fileName.replace(/\.[^.]+$/, "");

  async function download(fmt) {
    try {
      const res = await fetch("/api/export", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, format: fmt }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        alert(data.error || `Échec de l'export ${fmt.toUpperCase()}.`);
        return;
      }
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${stem}_normalise.${fmt}`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (_e) {
      alert("Impossible de joindre le serveur pour l'export.");
    }
  }

  return (
    <div className="sdc-step">
      <div className="sdc-step__intro">
        <img className="sdc-step__pic" src="../../assets/pictograms/document-download.svg" alt="" aria-hidden="true" />
        <div>
          <h1 className="sdc-h1">Tableau prêt à l'export</h1>
          <p className="sdc-lead">
            Le tableau normalisé est prêt au téléchargement en csv.
            Téléchargez-le pour relecture ou pour la pose du secret.
          </p>
        </div>
      </div>

      <EDS.Alert type="success" title="Pipeline terminé">
        {records.length} tableau{records.length > 1 ? "x" : ""} normalisé{records.length > 1 ? "s" : ""} et validé{records.length > 1 ? "s" : ""} à partir de <b>{fileName}</b>.
      </EDS.Alert>

      <div className="sdc-stats">
        <Stat value={records.length} label={`tableau${records.length > 1 ? "x" : ""}`} />
      </div>

      <div className="sdc-export">
        <EDS.Card
          title={`${stem}_normalise.csv`}
          pictogramSrc="../../assets/pictograms/document-download.svg"
          footer={
            <EDS.Button size="sm" icon="ri-download-line" onClick={() => download("csv")}>
              Télécharger le .csv
            </EDS.Button>
          }
        >
          Tableau plat pour relecture et pour la pose du secret via <b>rtauargus</b>.
        </EDS.Card>
      </div>

      <div className="sdc-actions">
        <EDS.Button variant="tertiary" icon="ri-restart-line" onClick={onRestart}>
          Analyser un autre classeur
        </EDS.Button>
      </div>
    </div>
  );
}

window.StepExport = StepExport;
