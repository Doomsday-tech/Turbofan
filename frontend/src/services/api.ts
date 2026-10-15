const API_BASE = 'http://127.0.0.1:5000/api';

export const api = {
  async getHealth() {
    const res = await fetch(`${API_BASE}/health`);
    return res.json();
  },
  async getSummary() {
    const res = await fetch(`${API_BASE}/summary`);
    return res.json();
  },
  async getEngines() {
    const res = await fetch(`${API_BASE}/engines`);
    return res.json();
  },
  async getEngineHistory(id: number) {
    const res = await fetch(`${API_BASE}/engines/${id}/history`);
    return res.json();
  },
  async predict(history: any[]) {
    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ history })
    });
    return res.json();
  }
};
