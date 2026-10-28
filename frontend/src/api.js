const API_BASE = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL.replace(/\/+$/, '')}/api` 
  : (typeof window !== 'undefined' && window.location.port === '5173' ? 'http://localhost:8000/api' : '/api');

function getAuthHeaders() {
  const token = localStorage.getItem("token");
  const headers = { "Content-Type": "application/json" };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

export const api = {
  // Auth
  async login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Login failed");
    }
    return res.json();
  },

  async getMe() {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Unauthorized");
    return res.json();
  },

  // Users (Admin)
  async getUsers() {
    const res = await fetch(`${API_BASE}/users`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error("Failed to load users");
    return res.json();
  },

  async createUser(data) {
    const res = await fetch(`${API_BASE}/users`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Failed to create user");
    }
    return res.json();
  },

  async updateUser(id, data) {
    const res = await fetch(`${API_BASE}/users/${id}`, {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Failed to update user");
    return res.json();
  },

  // Standards
  async getStandards() {
    const res = await fetch(`${API_BASE}/standards`);
    if (!res.ok) throw new Error("Failed to load standards");
    return res.json();
  },

  async updateStandard(id, data) {
    const res = await fetch(`${API_BASE}/standards/${id}`, {
      method: "PUT",
      headers: getAuthHeaders(),
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Failed to update standard");
    return res.json();
  },

  // Policy Evaluation & Samples
  async getSamples() {
    const res = await fetch(`${API_BASE}/policies/samples`);
    if (!res.ok) throw new Error("Failed to load presets");
    return res.json();
  },

  async evaluatePolicy(policyData) {
    const res = await fetch(`${API_BASE}/policies/evaluate`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(policyData)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "Evaluation failed");
    }
    return res.json();
  },

  async importFile(file) {
    const formData = new FormData();
    formData.append("file", file);
    const token = localStorage.getItem("token");
    const headers = {};
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}/policies/import`, {
      method: "POST",
      headers,
      body: formData
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "File import failed");
    }
    return res.json();
  },

  // Reports
  async getReports() {
    const res = await fetch(`${API_BASE}/reports`);
    if (!res.ok) throw new Error("Failed to load reports");
    return res.json();
  },

  async getReport(id) {
    const res = await fetch(`${API_BASE}/reports/${id}`);
    if (!res.ok) throw new Error("Report not found");
    return res.json();
  },

  getExportCsvUrl(id) {
    return `${API_BASE}/reports/${id}/export-csv`;
  },

  // Dashboard Stats & Audit
  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/dashboard/stats`);
    if (!res.ok) throw new Error("Failed to load stats");
    return res.json();
  },

  async getAuditLogs() {
    const res = await fetch(`${API_BASE}/audit`);
    if (!res.ok) throw new Error("Failed to load audit logs");
    return res.json();
  }
};
