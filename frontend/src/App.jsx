// App.jsx — GSSoC Issue Finder Dashboard
import { useState } from "react";

const API = "http://localhost:8000";

export default function App() {
  const [issues, setIssues] = useState([]);
  const [loading, setLoading] = useState(false);
  const [skills, setSkills] = useState("python,react");
  const [difficulty, setDifficulty] = useState("");
  const [label, setLabel] = useState("");
  const [msg, setMsg] = useState("");

  // Step 1: Refresh — GSSoC repos + GitHub issues fetch karo
  async function handleRefresh() {
    setLoading(true);
    setMsg("Fetching repos and issues...");
    const res = await fetch(`${API}/refresh`);
    const data = await res.json();
    setMsg(`✅ ${data.repos_found} repos, ${data.issues_found} issues fetched!`);
    setLoading(false);
  }

  // Step 2: Filter issues by skill/difficulty/label
  async function handleSearch() {
    setLoading(true);
    const params = new URLSearchParams();
    if (skills) params.append("skills", skills);
    if (difficulty) params.append("difficulty", difficulty);
    if (label) params.append("label", label);

    const res = await fetch(`${API}/issues?${params}`);
    const data = await res.json();
    setIssues(data.issues || []);
    setMsg(`Found ${data.total} matching issues`);
    setLoading(false);
  }

  return (
    <div style={s.app}>
      <h1 style={s.title}>♟ GSSoC Issue Finder</h1>
      <p style={s.sub}>Find unclaimed issues matching your skillset</p>

      {/* Controls */}
      <div style={s.controls}>
        <input style={s.input} placeholder="Skills (e.g. python,react,fastapi)"
          value={skills} onChange={e => setSkills(e.target.value)} />
        <select style={s.select} value={difficulty} onChange={e => setDifficulty(e.target.value)}>
          <option value="">All Difficulties</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
        <input style={s.input} placeholder="Label (e.g. bug, feature)"
          value={label} onChange={e => setLabel(e.target.value)} />
      </div>

      <div style={s.btnRow}>
        <button style={s.btnSecondary} onClick={handleRefresh} disabled={loading}>
          🔄 Refresh Data
        </button>
        <button style={s.btnPrimary} onClick={handleSearch} disabled={loading}>
          🔍 Find Issues
        </button>
      </div>

      {msg && <p style={s.msg}>{msg}</p>}

      {/* Issues List */}
      <div style={s.grid}>
        {issues.map((issue, i) => (
          <div key={i} style={s.card}>
            {/* Repo + Issue Number */}
            <div style={s.cardTop}>
              <span style={s.repo}>{issue.repo}</span>
              <span style={s.issueNum}>#{issue.number}</span>
            </div>

            {/* Title */}
            <a href={issue.url} target="_blank" rel="noreferrer" style={s.issueTitle}>
              {issue.title}
            </a>

            {/* Labels */}
            <div style={s.labels}>
              {issue.labels.map((l, j) => (
                <span key={j} style={s.label}>{l}</span>
              ))}
            </div>

            {/* Body preview */}
            {issue.body_preview && (
              <p style={s.preview}>{issue.body_preview}...</p>
            )}

            <a href={issue.url} target="_blank" rel="noreferrer" style={s.link}>
              View on GitHub →
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

const s = {
  app: { minHeight: "100vh", background: "#0a0b10", color: "#f0f0f5", fontFamily: "sans-serif", padding: "2rem" },
  title: { color: "#f4c430", fontSize: "2rem", margin: 0 },
  sub: { color: "#8b92a5", marginBottom: "1.5rem" },
  controls: { display: "flex", gap: "0.75rem", flexWrap: "wrap", marginBottom: "1rem" },
  input: { flex: 1, minWidth: "200px", padding: "0.6rem 1rem", background: "#141722", border: "1px solid #2c3245", borderRadius: "8px", color: "#f0f0f5" },
  select: { padding: "0.6rem 1rem", background: "#141722", border: "1px solid #2c3245", borderRadius: "8px", color: "#f0f0f5" },
  btnRow: { display: "flex", gap: "0.75rem", marginBottom: "1rem" },
  btnPrimary: { padding: "0.6rem 1.5rem", background: "#f4c430", color: "#000", border: "none", borderRadius: "8px", fontWeight: 700, cursor: "pointer" },
  btnSecondary: { padding: "0.6rem 1.5rem", background: "#1e2230", color: "#f0f0f5", border: "1px solid #2c3245", borderRadius: "8px", cursor: "pointer" },
  msg: { color: "#8b92a5", marginBottom: "1rem" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "1rem" },
  card: { background: "#141722", border: "1px solid #2c3245", borderRadius: "12px", padding: "1.2rem" },
  cardTop: { display: "flex", justifyContent: "space-between", marginBottom: "0.5rem" },
  repo: { color: "#8b92a5", fontSize: "0.8rem" },
  issueNum: { color: "#f4c430", fontWeight: 700, fontSize: "0.85rem" },
  issueTitle: { color: "#f0f0f5", fontWeight: 600, fontSize: "0.95rem", display: "block", marginBottom: "0.5rem", textDecoration: "none" },
  labels: { display: "flex", flexWrap: "wrap", gap: "0.4rem", marginBottom: "0.5rem" },
  label: { background: "#1e2230", border: "1px solid #2c3245", borderRadius: "4px", padding: "0.15rem 0.5rem", fontSize: "0.72rem", color: "#8b92a5" },
  preview: { color: "#6b7280", fontSize: "0.8rem", margin: "0.5rem 0" },
  link: { color: "#f4c430", fontSize: "0.85rem" },
};
