import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function JudgeResults({ result }) {
  if (!result) return null;

  const chartData = result.results.map((r) => ({ model: r.model_name, score: r.score }));

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
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={chartData}>
            <XAxis dataKey="model" tick={{ fontSize: 11 }} />
            <YAxis domain={[0, 10]} />
            <Tooltip />
            <Bar dataKey="score" fill="#3730A5" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
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