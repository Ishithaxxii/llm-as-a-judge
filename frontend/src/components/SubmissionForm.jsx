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