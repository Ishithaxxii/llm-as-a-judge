import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

export default function Results({ result }) {
  if (!result) return null;

  const {
    aggregate_score,
    agreement,
    flagged_disagreement,
    jaccard = 0,
    cosine = 0,
    z_score,
    score_std = 0,
    results = [],
  } = result;

  // Prepare data for radar chart (using criterion_scores if available)
  const criterionNames = new Set();
  results.forEach((r) => {
    Object.keys(r.criterion_scores || {}).forEach((k) => criterionNames.add(k));
  });

  const radarData = Array.from(criterionNames).map((name) => {
    const entry = { criterion: name };
    results.forEach((r) => {
      const shortName = r.model_name.split(":")[0];
      entry[shortName] = r.criterion_scores?.[name] ?? 0;
    });
    return entry;
  });

  const colors = ["#6366f1", "#22d3ee", "#a78bfa", "#34d399"];

  return (
    <div className="results-container">
      {/* Header Summary */}
      <div className="verdict-header">
        <div className="verdict-score">
          <span className="score-number">{aggregate_score.toFixed(1)}</span>
          <span className="score-label">Aggregate Score</span>
        </div>

        <div className={`agreement-badge ${flagged_disagreement ? "low" : "high"}`}>
          <span className="agreement-value">{Math.round(agreement * 100)}%</span>
          <span className="agreement-label">
            {flagged_disagreement ? "Low Agreement" : "High Agreement"}
          </span>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="metrics-grid">
        <div className="metric-card">
          <div className="metric-value">{(jaccard * 100).toFixed(1)}%</div>
          <div className="metric-label">Jaccard Similarity</div>
          <div className="metric-desc">Token overlap between judges</div>
        </div>

        <div className="metric-card">
          <div className="metric-value">{(cosine * 100).toFixed(1)}%</div>
          <div className="metric-label">Cosine Similarity</div>
          <div className="metric-desc">Semantic similarity of reasoning</div>
        </div>

        <div className="metric-card">
          <div className="metric-value">
            {z_score !== null && z_score !== undefined ? z_score.toFixed(2) : "—"}
          </div>
          <div className="metric-label">Z-Score</div>
          <div className="metric-desc">vs historical average</div>
        </div>

        <div className="metric-card">
          <div className="metric-value">{score_std.toFixed(2)}</div>
          <div className="metric-label">Score Std Dev</div>
          <div className="metric-desc">Spread between judges</div>
        </div>
      </div>

      {/* Radar Chart */}
      {radarData.length > 0 && (
        <div className="chart-section">
          <h3 className="section-title">Criteria Breakdown</h3>
          <div className="radar-wrapper">
            <ResponsiveContainer width="100%" height={320}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="#334155" />
                <PolarAngleAxis dataKey="criterion" tick={{ fill: "#94a3b8", fontSize: 12 }} />
                <PolarRadiusAxis angle={30} domain={[0, 10]} tick={{ fill: "#64748b" }} />
                {results.map((r, i) => {
                  const shortName = r.model_name.split(":")[0];
                  return (
                    <Radar
                      key={shortName}
                      name={shortName}
                      dataKey={shortName}
                      stroke={colors[i % colors.length]}
                      fill={colors[i % colors.length]}
                      fillOpacity={0.25}
                    />
                  );
                })}
                <Tooltip
                  contentStyle={{
                    background: "#0f172a",
                    border: "1px solid #334155",
                    borderRadius: "8px",
                  }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {/* Individual Judge Cards */}
      <div className="judges-section">
        <h3 className="section-title">Judge Deliberations</h3>
        <div className="judges-grid">
          {results.map((r, idx) => (
            <div
              key={r.model_name}
              className={`judge-card ${r.confidence != null && r.confidence < 0.7 ? "low-confidence" : ""}`}
            >
              <div className="judge-header">
                <div className="judge-name">
                  <span className="judge-dot" style={{ background: colors[idx % colors.length] }} />
                  {r.model_name}
                </div>
                <div className="judge-score">{r.score.toFixed(1)}</div>
              </div>

              <p className="judge-reasoning">{r.reasoning}</p>

              <div className="judge-footer">
                {r.confidence != null && (
                  <span className="confidence">
                    Confidence: {Math.round(r.confidence * 100)}%
                  </span>
                )}
                {r.latency_ms != null && (
                  <span className="latency">{r.latency_ms} ms</span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
