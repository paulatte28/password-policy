import React, { useState, useEffect } from 'react';
import { UserPlus } from 'lucide-react';
import { api } from '../api';

export default function UserManagement() {
  const [users, setUsers] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [resetUser, setResetUser] = useState(null);
  const [resetPassword, setResetPassword] = useState('');
  const [demoResult, setDemoResult] = useState(null);
  const [demoError, setDemoError] = useState('');
  const [seedingDemo, setSeedingDemo] = useState(false);
  const [newUser, setNewUser] = useState({
    email: '',
    full_name: '',
    role: 'Security Analyst',
    department: 'IT Security',
    password: '',
  });
  const [error, setError] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  async function loadUsers() {
    try {
      const data = await api.getUsers();
      setUsers(data);
    } catch (err) {
      console.error('Failed to load users', err);
    }
  }

  async function handleCreateUser(e) {
    e.preventDefault();
    try {
      setError('');
      await api.createUser(newUser);
      setShowCreateModal(false);
      setNewUser({
        email: '',
        full_name: '',
        role: 'Security Analyst',
        department: 'IT Security',
        password: '',
      });
      loadUsers();
    } catch (err) {
      setError(err.message);
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

  async function handleResetPassword(e) {
    e.preventDefault();
    try {
      setError('');
      await api.updateUser(resetUser.id, { password: resetPassword });
      setResetUser(null);
      setResetPassword('');
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleSeedDemo() {
    setSeedingDemo(true);
    setDemoError('');
    try {
      const res = await api.seedDemoUsers();
      setDemoResult(res);
      await loadUsers();
    } catch (err) {
      setDemoError(err.message);
    } finally {
      setSeedingDemo(false);
    }
  }

  return (
    <div className="workspace-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '28px' }}>
        <div>
          <span className="page-eyebrow">Administration</span>
          <h1>Users</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
            Add accounts, assign roles, and manage access.
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <button
            onClick={handleSeedDemo}
            disabled={seedingDemo}
            className="btn-secondary-custom"
            style={{ padding: '10px 16px', fontSize: '0.85rem' }}
          >
            {seedingDemo ? 'Creating...' : 'Create demo accounts'}
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="btn-cyan-custom"
            style={{ padding: '10px 20px', fontSize: '0.85rem' }}
          >
            <UserPlus size={16} /> Add User
          </button>
        </div>
      </div>

      {demoError && (
        <p role="alert" style={{ color: 'var(--color-fail)', marginBottom: 16 }}>
          {demoError}
        </p>
      )}

      <div className="sec-card data-table-wrap" style={{ padding: 0 }}>
        <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
          <thead>
            <tr style={{ background: 'var(--bg-table-head)', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.05em' }}>
              <th style={{ padding: '14px 20px' }}>Full Name</th>
              <th style={{ padding: '14px 20px' }}>Email Address</th>
              <th style={{ padding: '14px 20px' }}>System Role</th>
              <th style={{ padding: '14px 20px' }}>Department / Unit</th>
              <th style={{ padding: '14px 20px' }}>Status</th>
              <th style={{ padding: '14px 20px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                <td style={{ padding: '14px 20px', fontWeight: 600, color: 'var(--text-primary)' }}>{u.full_name}</td>
                <td style={{ padding: '14px 20px', color: 'var(--text-secondary)' }}>{u.email}</td>
                <td style={{ padding: '14px 20px' }}>
                  <span
                    style={{
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      color: u.role === 'Administrator' ? 'var(--primary)' : u.role === 'Security Analyst' ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                      background: 'var(--bg-inset)',
                      padding: '3px 10px',
                      borderRadius: '4px',
                    }}
                  >
                    {u.role}
                  </span>
                </td>
                <td style={{ padding: '14px 20px', color: 'var(--text-muted)' }}>{u.department || 'N/A'}</td>
                <td style={{ padding: '14px 20px' }}>
                  {u.is_active ? <span className="badge-pass">Active</span> : <span className="badge-fail">Inactive</span>}
                </td>
                <td style={{ padding: '14px 20px', textAlign: 'right' }}>
                  <button
                    onClick={() => toggleStatus(u)}
                    className="btn-secondary-custom"
                    style={{ padding: '4px 10px', fontSize: '0.75rem' }}
                  >
                    {u.is_active ? 'Deactivate' : 'Activate'}
                  </button>
                  <button
                    onClick={() => {
                      setError('');
                      setResetUser(u);
                    }}
                    className="btn-secondary-custom"
                    style={{ padding: '4px 10px', fontSize: '0.75rem', marginLeft: 6 }}
                  >
                    Reset password
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {demoResult && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', display: 'grid', placeItems: 'center', zIndex: 100, padding: 20 }}>
          <div className="sec-card" style={{ maxWidth: 620, width: '100%', padding: 28, maxHeight: '90vh', overflowY: 'auto' }}>
            <h3 style={{ marginBottom: 8 }}>Demo accounts</h3>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.87rem', marginBottom: 18 }}>
              These temporary passwords are shown once. Keep them private. Each demo user must change their password after signing in.
            </p>
            {demoResult.created.length ? (
              demoResult.created.map((acc) => (
                <div key={acc.email} style={{ borderTop: '1px solid var(--border-subtle)', padding: '12px 0' }}>
                  <strong>{acc.role}</strong>
                  <div style={{ fontSize: '0.85rem', marginTop: 4 }}>{acc.email}</div>
                  <code style={{ display: 'block', overflowWrap: 'anywhere', marginTop: 6, padding: 9, background: 'var(--bg-inset)', borderRadius: 6 }}>
                    {acc.temporary_password}
                  </code>
                </div>
              ))
            ) : (
              <p>No new accounts were created.</p>
            )}
            {demoResult.skipped.length > 0 && (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginTop: 14 }}>
                Already set up or changed: {demoResult.skipped.join(', ')}. Use “Reset password” if you need a new temporary password for one of them.
              </p>
            )}
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 20 }}>
              <button className="btn-cyan-custom" onClick={() => setDemoResult(null)}>
                Done
              </button>
            </div>
          </div>
        </div>
      )}

      {resetUser && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', display: 'grid', placeItems: 'center', zIndex: 100, padding: 20 }}>
          <form onSubmit={handleResetPassword} className="sec-card" style={{ maxWidth: 440, width: '100%', padding: 28 }}>
            <h3 style={{ marginBottom: 10 }}>Reset password for {resetUser.full_name}</h3>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 16 }}>
              Their current sessions will end. Give them the new password privately.
            </p>
            {error && (
              <p role="alert" style={{ color: 'var(--color-fail)' }}>
                {error}
              </p>
            )}
            <input
              type="password"
              className="sec-input"
              autoComplete="new-password"
              required
              value={resetPassword}
              onChange={(e) => setResetPassword(e.target.value)}
              placeholder="New password"
            />
            <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end', marginTop: 18 }}>
              <button
                type="button"
                className="btn-secondary-custom"
                onClick={() => {
                  setResetUser(null);
                  setResetPassword('');
                }}
              >
                Cancel
              </button>
              <button type="submit" className="btn-cyan-custom">
                Reset password
              </button>
            </div>
          </form>
        </div>
      )}

      {showCreateModal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100, padding: '20px' }}>
          <div className="sec-card" style={{ maxWidth: '480px', width: '100%', padding: '28px' }}>
            <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '6px' }}>Create New User</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.82rem', marginBottom: '20px' }}>
              Add a staff user with specific role permissions.
            </p>
            {error && (
              <div style={{ background: 'rgba(244,63,94,0.15)', border: '1px solid var(--color-fail)', padding: '10px', borderRadius: 'var(--radius-sm)', color: 'var(--color-fail)', fontSize: '0.85rem', marginBottom: '16px' }}>
                {error}
              </div>
            )}
            <form onSubmit={handleCreateUser} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>Full Name</label>
                <input type="text" required value={newUser.full_name} onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })} className="sec-input" placeholder="e.g. Maria Santos" />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>Email Address</label>
                <input type="email" required value={newUser.email} onChange={(e) => setNewUser({ ...newUser, email: e.target.value })} className="sec-input" placeholder="e.g. maria@passwordpolicy.local" />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>Role</label>
                <select value={newUser.role} onChange={(e) => setNewUser({ ...newUser, role: e.target.value })} className="sec-input">
                  <option value="Security Analyst">Security Analyst</option>
                  <option value="Administrator">Administrator</option>
                  <option value="Viewer">Viewer</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>Department</label>
                <input type="text" value={newUser.department} onChange={(e) => setNewUser({ ...newUser, department: e.target.value })} className="sec-input" placeholder="e.g. IT Audit & Compliance" />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '4px' }}>Password</label>
                <input type="password" required value={newUser.password} onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} className="sec-input" placeholder="Temporary password" />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '12px' }}>
                <button type="button" onClick={() => setShowCreateModal(false)} className="btn-secondary-custom">
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
