import { useState } from "react";
import { api } from "./api/client.js";
import SubmissionForm from "./components/SubmissionForm.jsx";
import JudgeResults from "./components/JudgeResults.jsx";

export default function App() {
  const [result, setResult] = useState(null);
  const [judging, setJudging] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmitted({ content, content_type }) {
    const submission = await api.createSubmission({ content, content_type });
    setResult(null);
    setJudging(true);
    setError(null);
    try {
      const judged = await api.judge({ submission_id: submission.id });
      setResult(judged);
    } catch (err) {
      setError(err.message);
    } finally {
      setJudging(false);
    }
  }

  return (
    <main className="app">
      <div className="brand">
        <h1>JudgeAI</h1>
        <span className="tag">multi-model</span>
      </div>
      <p className="subtitle">Bias-aware evaluation across multiple LLM judges, with agreement tracking</p>

      <div className="panel">
        <SubmissionForm onSubmitted={handleSubmitted} />
      </div>

      {judging && <p className="status-text">Running judges…</p>}
      {error && <p className="error-text">{error}</p>}

      <div className="results">
        <JudgeResults result={result} />
      </div>
    </main>
  );
}