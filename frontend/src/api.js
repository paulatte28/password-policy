const API_BASE = typeof window !== 'undefined' && window.location.port === '5173'
  ? 'http://localhost:8000/api'
  : '/api';

function getAuthHeaders() {
  const token = localStorage.getItem('token');
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  return headers;
}

export const api = {
  async login(email, password) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Login failed');
    }
    return res.json();
  },

  async getMe() {
    const res = await fetch(`${API_BASE}/auth/me`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Unauthorized');
    return res.json();
  },

  async logout() {
    await fetch(`${API_BASE}/auth/logout`, { method: 'POST', headers: getAuthHeaders() });
  },

  async changePassword(currentPassword, newPassword) {
    const res = await fetch(`${API_BASE}/auth/change-password`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({ current_password: currentPassword, new_password: newPassword }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Could not change password');
    }
    return res.json();
  },

  async getActivePolicy() {
    const res = await fetch(`${API_BASE}/policies/active`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Could not load active policy');
    return res.json();
  },

  async activatePolicy(policy) {
    const res = await fetch(`${API_BASE}/policies/active`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(policy),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Could not activate policy');
    }
    return res.json();
  },

  async getUsers() {
    const res = await fetch(`${API_BASE}/users`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load users');
    return res.json();
  },

  async seedDemoUsers() {
    const res = await fetch(`${API_BASE}/users/seed-demo`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Could not create demo accounts');
    }
    return res.json();
  },

  async createUser(userData) {
    const res = await fetch(`${API_BASE}/users`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(userData),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to create user');
    }
    return res.json();
  },

  async updateUser(userId, updateData) {
    const res = await fetch(`${API_BASE}/users/${userId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(updateData),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Failed to update user');
    }
    return res.json();
  },

  async getStandards() {
    const res = await fetch(`${API_BASE}/standards`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load standards');
    return res.json();
  },

  async updateStandard(standardId, data) {
    const res = await fetch(`${API_BASE}/standards/${standardId}`, {
      method: 'PUT',
      headers: getAuthHeaders(),
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to update standard');
    return res.json();
  },

  async getSamples() {
    const res = await fetch(`${API_BASE}/policies/samples`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load presets');
    return res.json();
  },

  async evaluatePolicy(policyData) {
    const res = await fetch(`${API_BASE}/policies/evaluate`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(policyData),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'Evaluation failed');
    }
    return res.json();
  },

  async importFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    const token = localStorage.getItem('token');
    const headers = {};
    if (token) headers.Authorization = `Bearer ${token}`;

    const res = await fetch(`${API_BASE}/policies/import`, {
      method: 'POST',
      headers,
      body: formData,
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || 'File import failed');
    }
    return res.json();
  },

  async getReports() {
    const res = await fetch(`${API_BASE}/reports`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load reports');
    return res.json();
  },

  async getReport(id) {
    const res = await fetch(`${API_BASE}/reports/${id}`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Report not found');
    return res.json();
  },

  async downloadReportCsv(id) {
    const res = await fetch(`${API_BASE}/reports/${id}/export-csv`, {
      headers: getAuthHeaders(),
    });
    if (!res.ok) throw new Error('Could not download CSV report');
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `compliance_report_${id}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  },

  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/dashboard/stats`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load stats');
    return res.json();
  },

  async getAuditLogs({ page = 1, pageSize = 20, search = '', action = '' } = {}) {
    const params = new URLSearchParams({ page, page_size: pageSize });
    if (search.trim()) params.set('search', search.trim());
    if (action) params.set('action', action);
    const res = await fetch(`${API_BASE}/audit?${params}`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load audit logs');
    return res.json();
  },

  async getIntegrationsStatus() {
    const res = await fetch(`${API_BASE}/integrations/status`, { headers: getAuthHeaders() });
    if (!res.ok) throw new Error('Failed to load integrations status');
    return res.json();
  },
};
