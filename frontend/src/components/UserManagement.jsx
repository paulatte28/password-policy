import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { Users, UserPlus, Check, X, Shield, Lock } from 'lucide-react';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newUser, setNewUser] = useState({
    email: "",
    full_name: "",
    role: "Security Analyst",
    department: "IT Security",
    password: ""
  });
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    try {
      const data = await api.getUsers();
      setUsers(data);
    } catch (err) {
      console.error("Failed to load users", err);
    }
  }

  async function handleCreateUser(e) {
    e.preventDefault();
    try {
      setErrorMsg("");
      await api.createUser(newUser);
      setShowAddModal(false);
      setNewUser({ email: "", full_name: "", role: "Security Analyst", department: "IT Security", password: "" });
      loadUsers();
    } catch (err) {
      setErrorMsg(err.message);
    }
  }

  async function toggleStatus(u) {
    try {
      await api.updateUser(u.id, { is_active: !u.is_active });
      loadUsers();
    } catch (err) {
      alert(`Update failed: ${err.message}`);
    }
  }

  return (
    <div style={{ maxWidth: "1150px", margin: "0 auto", padding: "32px 20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "16px", marginBottom: "28px" }}>
        <div>
          <h1 style={{ fontSize: "2rem", fontWeight: 800, marginBottom: "4px" }}>
            User Account & Role Management
          </h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "0.92rem" }}>
            Administrator console for managing access control (Administrator, Security Analyst, Viewer).
          </p>
        </div>

        <button 
          onClick={() => setShowAddModal(true)}
          className="btn-cyan-custom"
          style={{ padding: "10px 20px", fontSize: "0.85rem" }}
        >
          <UserPlus size={16} /> Add User
        </button>
      </div>

      <div className="sec-card" style={{ padding: "0", overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.88rem" }}>
          <thead>
            <tr style={{ background: "rgba(255,255,255,0.03)", borderBottom: "1px solid var(--border-subtle)", color: "var(--text-muted)", textTransform: "uppercase", fontSize: "0.75rem", letterSpacing: "0.05em" }}>
              <th style={{ padding: "14px 20px" }}>Full Name</th>
              <th style={{ padding: "14px 20px" }}>Email Address</th>
              <th style={{ padding: "14px 20px" }}>System Role</th>
              <th style={{ padding: "14px 20px" }}>Department / Unit</th>
              <th style={{ padding: "14px 20px" }}>Status</th>
              <th style={{ padding: "14px 20px", textAlign: "right" }}>Toggle Active</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id} style={{ borderBottom: "1px solid rgba(255, 255, 255, 0.04)" }}>
                <td style={{ padding: "14px 20px", fontWeight: 600, color: "var(--text-primary)" }}>
                  {u.full_name}
                </td>
                <td style={{ padding: "14px 20px", color: "var(--text-secondary)" }}>
                  {u.email}
                </td>
                <td style={{ padding: "14px 20px" }}>
                  <span style={{ 
                    fontSize: "0.75rem", 
                    fontWeight: 700, 
                    color: u.role === 'Administrator' ? 'var(--primary)' : u.role === 'Security Analyst' ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                    background: "rgba(255,255,255,0.05)",
                    padding: "3px 10px",
                    borderRadius: "4px"
                  }}>
                    {u.role}
                  </span>
                </td>
                <td style={{ padding: "14px 20px", color: "var(--text-muted)" }}>
                  {u.department || "N/A"}
                </td>
                <td style={{ padding: "14px 20px" }}>
                  {u.is_active ? (
                    <span className="badge-pass">Active</span>
                  ) : (
                    <span className="badge-fail">Inactive</span>
                  )}
                </td>
                <td style={{ padding: "14px 20px", textAlign: "right" }}>
                  <button
                    onClick={() => toggleStatus(u)}
                    className="btn-secondary-custom"
                    style={{ padding: "4px 10px", fontSize: "0.75rem" }}
                  >
                    {u.is_active ? "Deactivate" : "Activate"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Add User Modal */}
      {showAddModal && (
        <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100, padding: "20px" }}>
          <div className="sec-card" style={{ maxWidth: "480px", width: "100%", padding: "28px" }}>
            <h3 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: "6px" }}>Create New User</h3>
            <p style={{ color: "var(--text-muted)", fontSize: "0.82rem", marginBottom: "20px" }}>
              Add a staff user with specific role permissions.
            </p>

            {errorMsg && (
              <div style={{ background: "rgba(244,63,94,0.15)", border: "1px solid var(--color-fail)", padding: "10px", borderRadius: "var(--radius-sm)", color: "var(--color-fail)", fontSize: "0.85rem", marginBottom: "16px" }}>
                {errorMsg}
              </div>
            )}

            <form onSubmit={handleCreateUser} style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              <div>
                <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)", display: "block", marginBottom: "4px" }}>Full Name</label>
                <input
                  type="text"
                  required
                  value={newUser.full_name}
                  onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                  className="sec-input"
                  placeholder="e.g. Maria Santos"
                />
              </div>

              <div>
                <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)", display: "block", marginBottom: "4px" }}>Email Address</label>
                <input
                  type="email"
                  required
                  value={newUser.email}
                  onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                  className="sec-input"
                  placeholder="e.g. maria@passwordpolicy.local"
                />
              </div>

              <div>
                <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)", display: "block", marginBottom: "4px" }}>Role</label>
                <select
                  value={newUser.role}
                  onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                  className="sec-input"
                >
                  <option value="Security Analyst">Security Analyst</option>
                  <option value="Administrator">Administrator</option>
                  <option value="Viewer">Viewer</option>
                </select>
              </div>

              <div>
                <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)", display: "block", marginBottom: "4px" }}>Department</label>
                <input
                  type="text"
                  value={newUser.department}
                  onChange={(e) => setNewUser({ ...newUser, department: e.target.value })}
                  className="sec-input"
                  placeholder="e.g. IT Audit & Compliance"
                />
              </div>

              <div>
                <label style={{ fontSize: "0.8rem", color: "var(--text-secondary)", display: "block", marginBottom: "4px" }}>Password</label>
                <input
                  type="password"
                  required
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                  className="sec-input"
                  placeholder="Temporary password"
                />
              </div>

              <div style={{ display: "flex", justifyContent: "flex-end", gap: "10px", marginTop: "12px" }}>
                <button type="button" onClick={() => setShowAddModal(false)} className="btn-secondary-custom">
                  Cancel
                </button>
                <button type="submit" className="btn-cyan-custom">
                  Create Account
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
