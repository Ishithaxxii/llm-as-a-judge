export default function JudgeResults({ result }) {
  if (!result) return null;

  const maxScore = 10;
  const chartWidth = 500;
  const chartHeight = 160;
  const barGap = 24;
  const barWidth = result.results.length
    ? (chartWidth - barGap * (result.results.length + 1)) / result.results.length
    : 0;

  return (
    <div>
      <div className="summary-row">
        <div className="stat">
          <span className="stat-value">{result.aggregate_score}</span>
          <span className="stat-label">Aggregate score</span>
        </div>
        <div className={`stat ${result.flagged_disagreement ? "warn" : ""}`}>
          <span className="stat-value">{Math.round(result.agreement * 100)}%</span>
          <span className="stat-label">{result.flagged_disagreement ? "Low agreement" : "Agreement"}</span>
        </div>
      </div>

      <div className="chart-wrap">
        <svg width="100%" viewBox={`0 0 ${chartWidth} ${chartHeight + 30}`}>
          {result.results.map((r, i) => {
            const barHeight = (r.score / maxScore) * chartHeight;
            const x = barGap + i * (barWidth + barGap);
            const y = chartHeight - barHeight;
            return (
              <g key={r.model_name}>
                <rect x={x} y={y} width={barWidth} height={barHeight} rx="4" fill="#3730A5" />
                <text x={x + barWidth / 2} y={chartHeight + 16} textAnchor="middle" fontSize="10" fill="#5B6270">
                  {r.model_name.split(":")[0]}
                </text>
                <text x={x + barWidth / 2} y={y - 6} textAnchor="middle" fontSize="11" fontWeight="700" fill="#12151C">
                  {r.score.toFixed(1)}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {result.results.map((r) => (
        <div key={r.model_name} className={`judge-card ${r.confidence != null && r.confidence < 0.7 ? "low-confidence" : ""}`}>
          <div className="judge-card-header">
            <span className="model">{r.model_name}</span>
            <span className="score">{r.score.toFixed(1)}</span>
          </div>
          <p className="reasoning">{r.reasoning}</p>
          {r.confidence != null && <p className="confidence">confidence {Math.round(r.confidence * 100)}%</p>}
        </div>
      ))}
    </div>
  );
}