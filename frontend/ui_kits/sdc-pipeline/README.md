/* Étape 2 — Questions du modèle (boucle humaine). */
const QDS = window.SDCMetadataDesignSystem_967a78;
const { useState: useQState } = React;

function QuestionCard({ q, value, onAnswer }) {
  const [custom, setCustom] = useQState('');

  function handleCustomChange(e) {
    const v = e.target.value;
    setCustom(v);
    onAnswer(q.id, v || null);
  }

  function handleOption(opt) {
    setCustom('');
    onAnswer(q.id, opt);
  }

  const isCustomActive = value && !q.options.includes(value);

  return (
    <div className="sdc-question">
      <div className="sdc-question__head">
        <QDS.Badge type="new">Question {q.id}</QDS.Badge>
        <span className="sdc-question__cat">{q.category}</span>
      </div>
      <p className="sdc-question__text">{q.text}</p>
      <p className="sdc-question__ref"><i className="ri-file-text-line" aria-hidden="true"></i>{q.ref}</p>
      <div className="sdc-question__opts">
        {q.options.map((opt) => (
          <QDS.Tag key={opt} selected={value === opt} onClick={() => handleOption(opt)}>
            {value === opt ? <i className="ri-check-line" aria-hidden="true"></i> : null}
            {opt}
          </QDS.Tag>
        ))}
      </div>
      <div className="sdc-question__custom">
        <label className="sdc-question__custom-label" htmlFor={`custom-${q.id}`}>
          <i className="ri-edit-line" aria-hidden="true"></i>
          Autre réponse
        </label>
        <textarea
          id={`custom-${q.id}`}
          className={`sdc-question__custom-input${isCustomActive ? ' sdc-question__custom-input--active' : ''}`}
          placeholder="Saisissez votre réponse si aucune option ci-dessus ne convient…"
          value={custom}
          onChange={handleCustomChange}
          rows={2}
        />
      </div>
    </div>
  );
}

function StepQuestions({ questions, answers, onAnswer, onBack, onNext }) {
  const autoContinued = questions.length === 0;
  const answered = Object.keys(answers).length;
  const allDone = autoContinued || answered === questions.length;

  if (autoContinued) {
    return (
      <div className="sdc-step">
        <div className="sdc-step__intro">
          <img className="sdc-step__pic" src="../../assets/pictograms/document-search.svg" alt="" aria-hidden="true" />
          <div>
            <h1 className="sdc-h1">Aucune question nécessaire</h1>
            <p className="sdc-lead">
              Le modèle a analysé le classeur et produit directement le tableau normalisé,
              sans ambiguïté à lever. Vous pouvez passer à la vérification.
            </p>
          </div>
        </div>

        <QDS.Alert type="info" title="Tableau produit automatiquement">
          Le modèle n'a pas identifié de point d'ambiguïté dans vos métadonnées.
          Le tableau normalisé a été généré en phase&nbsp;1 — aucune réponse n'est requise.
        </QDS.Alert>

        <div className="sdc-actions sdc-actions--split">
          <QDS.Button variant="secondary" icon="ri-arrow-left-line" onClick={onBack}>Retour</QDS.Button>
          <QDS.Button icon="ri-arrow-right-line" iconRight onClick={onNext}>
            Vérifier le tableau
          </QDS.Button>
        </div>
      </div>
    );
  }

  return (
    <div className="sdc-step">
      <div className="sdc-step__intro">
        <img className="sdc-step__pic" src="../../assets/pictograms/document-search.svg" alt="" aria-hidden="true" />
        <div>
          <h1 className="sdc-h1">Le modèle a {questions.length} question{questions.length > 1 ? "s" : ""}</h1>
          <p className="sdc-lead">
            Ces points d'ambiguïté changeraient la valeur d'au moins un champ du tableau final.
            Répondez pour lever l'incertitude — chaque réponse est appliquée en phase&nbsp;2.
          </p>
        </div>
      </div>

      <QDS.Alert type="info" small title={`${answered} réponse(s) sur ${questions.length} — répondez à toutes pour continuer.`} />

      <div className="sdc-questions">
        {questions.map((q) => (
          <QuestionCard key={q.id} q={q} value={answers[q.id]} onAnswer={onAnswer} />
        ))}
      </div>

      <div className="sdc-actions sdc-actions--split">
        <QDS.Button variant="secondary" icon="ri-arrow-left-line" onClick={onBack}>Retour</QDS.Button>
        <QDS.Button icon="ri-arrow-right-line" iconRight disabled={!allDone} onClick={onNext}>
          Produire le tableau
        </QDS.Button>
      </div>
    </div>
  );
}

window.StepQuestions = StepQuestions;
