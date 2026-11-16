import React, { useState } from 'react';
import { AlertCircle, KeyRound } from 'lucide-react';
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
    <main className="auth-main">
      <form onSubmit={handleSubmit} className="auth-card" style={{ width: 'min(100%, 440px)' }}>
        <div className="auth-header">
          <span className="auth-eyebrow">
            <KeyRound size={13} strokeWidth={2.2} /> Account security
          </span>
          <h1>Change password</h1>
          <p>
            {required
              ? 'Your administrator activated a policy. Set a password that follows it before continuing.'
              : 'Your new password will be checked against the active policy.'}
          </p>
        </div>

        {error && (
          <div className="auth-error" role="alert">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <div className="auth-field">
          <label htmlFor="current-password">Current password</label>
          <input
            id="current-password"
            className="sec-input"
            type="password"
            autoComplete="current-password"
            required
            value={currentPassword}
            onChange={(e) => setCurrentPassword(e.target.value)}
          />
        </div>

        <div className="auth-field">
          <label htmlFor="new-password">New password</label>
          <input
            id="new-password"
            className="sec-input"
            type="password"
            autoComplete="new-password"
            required
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </div>

        <div className="auth-field">
          <label htmlFor="confirm-password">Confirm new password</label>
          <input
            id="confirm-password"
            className="sec-input"
            type="password"
            autoComplete="new-password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </div>

        <button
          className="btn-primary-custom auth-submit"
          type="submit"
          disabled={loading}
        >
          {loading ? 'Saving...' : 'Change password'}
        </button>
      </form>
    </main>
  );
}
