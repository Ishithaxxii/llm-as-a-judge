import Landing from "./Landing";
import CosmicBackground from "./CosmicBackground";

export default function App() {
  return (
    <main className="relative min-h-screen overflow-hidden bg-background text-text">
      <CosmicBackground />
      <Landing />
    </main>
  );
}






// import { useState } from "react";
// import { api } from "./api/client.js";
// import Submission from "./Submission.jsx";
// import Results from "./Results.jsx";

// export default function App() {
//   const [result, setResult] = useState(null);
//   const [judging, setJudging] = useState(false);
//   const [error, setError] = useState(null);

//   async function handleSubmitted({ content, content_type }) {
//     setResult(null);
//     setJudging(true);
//     setError(null);

//     try {
//       const submission = await api.createSubmission({ content, content_type });
//       const judged = await api.judge({ submission_id: submission.id });
//       setResult(judged);
//     } catch (err) {
//       setError(err.message || "Failed to judge submission");
//     } finally {
//       setJudging(false);
//     }
//   }

//   return (
//     <main className="app">
//       <div className="brand">
//         <h1>JudgeAI</h1>
//         <span className="tag">Tribunal</span>
//       </div>

//       <p className="subtitle">
//         Multi-model deliberation with quantified agreement.
//         Submit code, essays, or text — the judges will decide.
//       </p>

//       <div className="panel">
//         <Submission onSubmitted={handleSubmitted} disabled={judging} />
//       </div>

//       {judging && (
//         <div className="judging-status">
//           <div className="judging-pulse" />
//           <p>The judges are deliberating…</p>
//         </div>
//       )}

//       {error && <p className="error-text">{error}</p>}

//       <div className="results">
//         <Results result={result} />
//       </div>
//     </main>
//   );
// }



