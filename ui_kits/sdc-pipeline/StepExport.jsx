/* App — orchestrates the four-phase pipeline as an interactive click-through. */
const ADS = window.SDCMetadataDesignSystem_967a78;
const { useState: useAppState } = React;
const STEPS = ["Dépôt", "Questions", "Vérification", "Export"];

function Processing({ label }) {
  return (
    <div className="sdc-processing">
      <span className="sdc-spinner" aria-hidden="true"></span>
      <p className="sdc-processing__label">{label}</p>
      <p className="sdc-processing__sub">temperature = 0 · appel au modèle Qwen sur SSP Cloud</p>
    </div>
  );
}

function App() {
  const [step, setStep] = useAppState(0);
  const [file, setFile] = useAppState(null);
  const [answers, setAnswers] = useAppState({});
  const [processing, setProcessing] = useAppState(null);
  const [sessionId, setSessionId] = useAppState(null);
  const [questions, setQuestions] = useAppState([]);
  const [markdown, setMarkdown] = useAppState("");
  const [records, setRecords] = useAppState([]);
  const [error, setError] = useAppState(null);

  const reset = () => {
    setFile(null);
    setAnswers({});
    setStep(0);
    setSessionId(null);
    setQuestions([]);
    setMarkdown("");
    setRecords([]);
    setError(null);
  };

  async function handleUpload() {
    setError(null);
    setProcessing("Lecture du classeur et analyse des ambiguïtés…");
    const fd = new FormData();
    fd.append("file", file.raw);
    try {
      const res = await fetch("/api/upload", { method: "POST", body: fd });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Erreur lors de l'envoi du fichier.");
        setProcessing(null);
        return;
      }
      setSessionId(data.session_id);
      setMarkdown(data.extracted_markdown || "");
      setQuestions(data.questions || []);
      if (data.records && data.records.length > 0) {
        setRecords(data.records);
      }
      setStep(1);
    } catch (_e) {
      setError("Impossible de joindre le serveur. Vérifiez que Flask est en cours d'exécution.");
    }
    setProcessing(null);
  }

  async function handleAnswer() {
    setError(null);
    setProcessing("Application des réponses et production du JSON…");
    try {
      const res = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, answers }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Erreur lors de la production du tableau.");
        setProcessing(null);
        return;
      }
      setRecords(data.normalized_table || []);
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
