import { useState } from "react";

const CONTENT_TYPES = [
  { value: "code", label: "Code", icon: "</>" },
  { value: "essay", label: "Essay", icon: "¶" },
  { value: "text", label: "Text", icon: "T" },
];

export default function Submission({ onSubmitted, disabled = false }) {
  const [content, setContent] = useState("");
  const [contentType, setContentType] = useState("code");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!content.trim() || disabled || submitting) return;

    setSubmitting(true);
    setError(null);

    try {
      await onSubmitted({ content, content_type: contentType });
      setContent(""); // clear after successful submit
    } catch (err) {
      setError(err.message || "Something went wrong");
    } finally {
      setSubmitting(false);
    }
  }

  const isBusy = submitting || disabled;

  return (
    <form onSubmit={handleSubmit} className="submission-form">
      {/* Content Type Pills */}
      <div className="type-selector">
        <span className="field-label">Content type</span>
        <div className="type-pills">
          {CONTENT_TYPES.map((type) => (
            <button
              key={type.value}
              type="button"
              className={`type-pill ${contentType === type.value ? "active" : ""}`}
              onClick={() => setContentType(type.value)}
              disabled={isBusy}
            >
              <span className="pill-icon">{type.icon}</span>
              {type.label}
            </button>
          ))}
        </div>
      </div>

      {/* Content Area */}
      <div className="content-area">
        <label className="field-label" htmlFor="content">
          Content to evaluate
        </label>
        <textarea
          id="content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder={
            contentType === "code"
              ? "Paste your code here..."
              : contentType === "essay"
              ? "Paste your essay here..."
              : "Paste any text here..."
          }
          rows={10}
          disabled={isBusy}
        />
        <div className="char-count">{content.length.toLocaleString()} characters</div>
      </div>

      {error && <p className="error-text">{error}</p>}

      <button
        className="submit-btn"
        type="submit"
        disabled={isBusy || !content.trim()}
      >
        {submitting ? (
          <>
            <span className="spinner" />
            Submitting…
          </>
        ) : disabled ? (
          "Judges are working…"
        ) : (
          "Submit for Judging"
        )}
      </button>
    </form>
  );
}

