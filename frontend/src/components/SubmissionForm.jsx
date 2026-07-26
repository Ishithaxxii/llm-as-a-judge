import { useState } from "react";

export default function SubmissionForm({ onSubmitted }) {
  const [content, setContent] = useState("");
  const [contentType, setContentType] = useState("code");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!content.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      await onSubmitted({ content, content_type: contentType });
      setContent("");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <label className="field-label" htmlFor="content-type">Content type</label>
      <select id="content-type" value={contentType} onChange={(e) => setContentType(e.target.value)}>
        <option value="code">code</option>
        <option value="essay">essay</option>
        <option value="text">text</option>
      </select>

      <label className="field-label" htmlFor="content">Content to evaluate</label>
      <textarea id="content" rows={8} value={content} onChange={(e) => setContent(e.target.value)} placeholder="Paste code, essay, or text..." />

      {error && <p className="error-text">{error}</p>}
      <button className="submit-btn" type="submit" disabled={submitting}>
        {submitting ? "Submitting…" : "Submit for judging"}
      </button>
    </form>
  );
}