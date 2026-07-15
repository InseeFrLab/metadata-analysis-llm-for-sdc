/* Étape 3 — Vérification : aperçu Markdown sérialisé + tableau validé contre le schéma. */
const VDS = window.SDCMetadataDesignSystem_967a78;

const VCOLUMNS = [
  { key: "table_name",        label: "table_name",        mono: true, width: "8rem" },
  { key: "field",             label: "field",             mono: true },
  { key: "hrc_field",         label: "hrc_field",         mono: true, width: "7rem" },
  { key: "indicator",         label: "indicator",         mono: true },
  { key: "hrc_indicator",     label: "hrc_indicator",     mono: true, width: "9rem" },
  { key: "spanning",          label: "spanning_variables", mono: true },
];

function StepVerification({ markdown, records, onBack, onNext }) {
  return (
    <div className="sdc-step">
      <div className="sdc-step__intro">
        <img className="sdc-step__pic" src="../../assets/pictograms/data-visualization.svg" alt="" aria-hidden="true" />
        <div>
          <h1 className="sdc-h1">Vérifiez les tableaux extraits</h1>
          <p className="sdc-lead">
            Aperçu du tableau normalisé
          </p>
        </div>
      </div>

      <div className="sdc-verif">
        <section className="sdc-verif__panel">
          <h2 className="sdc-panel-title"><i className="ri-table-line" aria-hidden="true"></i>Tableau normalisé</h2>
          <VDS.Alert type="success" small title={`Format valide`} />
          <div style={{ marginTop: "1rem" }}>
            <VDS.Table columns={VCOLUMNS} rows={records.slice(0,10)} striped
              caption="« NA » = attribut sans hiérarchie." />
          </div>
        </section>
      </div>

      <div className="sdc-actions sdc-actions--split">
        <VDS.Button variant="secondary" icon="ri-arrow-left-line" onClick={onBack}>Retour aux questions</VDS.Button>
        <VDS.Button icon="ri-check-line" onClick={onNext}>Valider et exporter</VDS.Button>
      </div>
    </div>
  );
}

window.StepVerification = StepVerification;
