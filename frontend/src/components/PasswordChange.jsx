import React, { useState } from 'react';
import { api } from '../api';

export default function PasswordChange({ required, onChanged }) {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setError('New passwords do not match');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await api.changePassword(currentPassword, newPassword);
      onChanged();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ flex: 1, display: 'grid', placeItems: 'center', padding: 24 }}>
      <form onSubmit={handleSubmit} className="sec-card" style={{ width: 'min(100%, 440px)', padding: 32 }}>
        <h1 style={{ fontSize: '1.5rem', marginBottom: 8 }}>Change password</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 20 }}>
          {required
            ? 'Your administrator activated a policy. Set a password that follows it before continuing.'
            : 'Your new password will be checked against the active policy.'}
        </p>
        {error && (
          <p role="alert" style={{ color: 'var(--color-fail)' }}>
            {error}
          </p>
        )}
        <label>
          Current password
          <input
            className="sec-input"
            type="password"
            autoComplete="current-password"
            required
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
            style={{ margin: '6px 0 14px' }}
          />
        </label>
        <label>
          New password
          <input
            className="sec-input"
            type="password"
            autoComplete="new-password"
            required
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            style={{ margin: '6px 0 14px' }}
          />
        </label>
        <label>
          Confirm new password
          <input
            className="sec-input"
            type="password"
            autoComplete="new-password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            style={{ margin: '6px 0 20px' }}
          />
        </label>
        <button
          className="btn-cyan-custom"
          type="submit"
          disabled={loading}
          style={{ width: '100%', justifyContent: 'center' }}
        >
          {loading ? 'Saving...' : 'Change password'}
        </button>
      </form>
    </main>
  );
}
