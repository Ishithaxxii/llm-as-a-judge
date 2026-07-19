const BASE = "/api";

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  createSubmission: (data) => request("/submissions", { method: "POST", body: JSON.stringify(data) }),
  judge: (data) => request("/judge", { method: "POST", body: JSON.stringify(data) }),
};