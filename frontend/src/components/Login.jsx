import React, { useState } from 'react';
import { AlertCircle, Eye, EyeOff, Lock } from 'lucide-react';
import { api } from '../api';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data = await api.login(email, password);
      onLogin(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="auth-main">
      <form onSubmit={handleSubmit} className="auth-card">
        <div className="auth-header">
          <span className="auth-eyebrow">
            <Lock size={13} strokeWidth={2.2} /> Workspace access
          </span>
          <h1>Sign in</h1>
          <p>Use the account created by your administrator.</p>
        </div>

        {error && (
          <div className="auth-error" role="alert">
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        <div className="auth-field">
          <label htmlFor="login-email">Email</label>
          <input
            id="login-email"
            className="sec-input"
            type="email"
            autoComplete="username"
            placeholder="name@organization.com"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>

        <div className="auth-field">
          <label htmlFor="login-password">Password</label>
          <div className="password-input-wrap">
            <input
              id="login-password"
              className="sec-input"
              type={showPassword ? 'text' : 'password'}
              autoComplete="current-password"
              placeholder="Enter your password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              type="button"
              className="password-toggle"
              onClick={() => setShowPassword((prev) => !prev)}
              aria-label={showPassword ? 'Hide password' : 'Show password'}
              title={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
            </button>
          </div>
        </div>

        <button
          className="btn-primary-custom auth-submit"
          type="submit"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>

        <p className="auth-footnote">
          Authorized personnel only. Activity is logged.
        </p>
      </form>
    </main>
  );
}
