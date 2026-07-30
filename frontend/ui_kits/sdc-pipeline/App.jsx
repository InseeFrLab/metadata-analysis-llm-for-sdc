/* App — orchestrates the four-phase pipeline as an interactive click-through. */
const ADS = window.SDCMetadataDesignSystem_967a78;
const { useState: useAppState } = React;
const STEPS = ["Dépôt", "Questions", "Vérification", "Export"];

function Processing({ label }) {
  return (
    <div className="sdc-processing">
      <span className="sdc-spinner" aria-hidden="true"></span>
      <p className="sdc-processing__label">{label}</p>
      <p className="sdc-processing__sub">Cette étape peut prendre du temps, merci de votre patience...</p>
    </div>
  );
}

/* Canonical identity of one submission, mirroring the backend's fingerprint:
   blank answers dropped, surrounding whitespace ignored, question order fixed.
   Only ever an optimisation — the server re-derives its own key and is the
   authority. Being *stricter* than the server is therefore safe (worst case a
   pointless round-trip that the server answers from its cache); being looser
   would not be, which is why nothing beyond trimming is normalised here. */
function submissionKey(answers, extraInfo) {
  const norm = {};
  Object.keys(answers).sort().forEach((k) => {
    const v = (answers[k] || "").trim();
    if (v) norm[k] = v;
  });
  return JSON.stringify({ a: norm, e: (extraInfo || "").trim() });
}

function App() {
  const [step, setStep] = useAppState(0);
  const [file, setFile] = useAppState(null);
  const [answers, setAnswers] = useAppState({});
  const [extraInfo, setExtraInfo] = useAppState("");
  const [processing, setProcessing] = useAppState(null);
  const [sessionId, setSessionId] = useAppState(null);
  const [questions, setQuestions] = useAppState([]);
  const [markdown, setMarkdown] = useAppState("");
  const [records, setRecords] = useAppState([]);
  const [error, setError] = useAppState(null);
  // Key of the submission the table on screen was produced from, so returning
  // from Vérification without touching anything skips the call entirely.
  const [submittedKey, setSubmittedKey] = useAppState(null);

  const reset = () => {
    setFile(null);
    setAnswers({});
    setExtraInfo("");
    setStep(0);
    setSessionId(null);
    setQuestions([]);
    setMarkdown("");
    setRecords([]);
    setError(null);
    setSubmittedKey(null);
  };

  async function handleUpload() {
    setError(null);
    setAnswers({});
    setExtraInfo("");
    setQuestions([]);
    setRecords([]);
    setSubmittedKey(null);
    setProcessing("Lecture du classeur et analyse des ambiguïtés…");
    const fd = new FormData();
    fd.append("file", file.raw);
    try {
      const res = await fetch("/api/upload", { method: "POST", body: fd });
      const data = await res.json();
      if (data.error) {
        setError(data.error);
        setProcessing(null);
        return;
      }
      setSessionId(data.session_id);
      setMarkdown(data.extracted_markdown || "");
      setQuestions(data.questions || []);
      if (data.records && data.records.length > 0) {
        // Auto-continued: the table came back with no questions asked, so it
        // already corresponds to the empty submission (the server seeded the
        // same key). Continuing without adding anything is then a no-op.
        setRecords(data.records);
        setSubmittedKey(submissionKey({}, ""));
      }
      setStep(1);
    } catch (_e) {
      setError("Impossible de joindre le serveur. Vérifiez que Flask est en cours d'exécution.");
    }
    setProcessing(null);
  }

  async function handleAnswer() {
    setError(null);

    // Nothing edited since the table on screen was produced — go straight back
    // to it rather than regenerating an identical one.
    const key = submissionKey(answers, extraInfo);
    if (key === submittedKey && records.length > 0) {
      setStep(2);
      return;
    }

    setProcessing("Prise en compte des réponses et production du CSV...");
    try {
      const res = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, answers, extra_info: extraInfo }),
      });
      const data = await res.json();
      if (data.error) {
        if (data.code === "session_expired") {
          reset();
          setError("Votre session a expiré côté serveur — veuillez déposer le fichier à nouveau.");
          setProcessing(null);
          return;
        }
        setError(data.error);
        setProcessing(null);
        return;
      }
      setRecords(data.normalized_table || []);
      // Recorded on success only, so a run that failed is genuinely retried.
      setSubmittedKey(key);
      setStep(2);
    } catch (_e) {
      setError("Impossible de joindre le serveur.");
    }
    setProcessing(null);
  }

  return (
    <Layout>
      <div className="sdc-container">
        <div className="sdc-stepper-wrap">
          <ADS.Stepper steps={STEPS} current={step} />
        </div>

        {error && (
          <div style={{ marginBottom: "1.5rem" }}>
            <ADS.Alert type="error" title="Une erreur est survenue" onClose={() => setError(null)}>
              {error}
            </ADS.Alert>
          </div>
        )}

        {processing ? (
          <Processing label={processing} />
        ) : step === 0 ? (
          <StepDepot
            file={file}
            onSelect={setFile}
            onRemove={() => setFile(null)}
            onNext={handleUpload}
          />
        ) : step === 1 ? (
          <StepQuestions
            questions={questions}
            answers={answers}
            onAnswer={(id, val) => setAnswers((a) => ({ ...a, [id]: val }))}
            extraInfo={extraInfo}
            onExtraInfoChange={setExtraInfo}
            onBack={() => setStep(0)}
            onNext={handleAnswer}
          />
        ) : step === 2 ? (
          <StepVerification
            markdown={markdown}
            records={records}
            onBack={() => setStep(1)}
            onNext={() => setStep(3)}
          />
        ) : (
          <StepExport
            records={records}
            fileName={file ? file.name : "metadonnees.ods"}
            sessionId={sessionId}
            onRestart={reset}
          />
        )}
      </div>
    </Layout>
  );
}

window.App = App;
