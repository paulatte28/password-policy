import React, { useState } from 'react';
import { AlertCircle, CheckCircle2, Eye, EyeOff, Lock } from 'lucide-react';
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
      <div className="auth-split">
        <section className="auth-brand-panel" aria-label="Workspace overview">
          <div className="auth-brand-top">
            <div className="auth-brand-lockup">
              <span className="brand-mark">
                <img src="/images/logo.png" alt="" />
              </span>
              <span className="auth-brand-copy">
                <strong>Password Policy</strong>
                <small>Administration workspace</small>
              </span>
            </div>
            <h2>Password Policy &amp; Risk Evaluation</h2>
            <p>
              Evaluate password configurations against industry benchmarks, track compliance
              history, and manage active workspace rules.
            </p>
          </div>

          <ul className="auth-highlights">
            <li>
              <CheckCircle2 size={16} />
              <span>Benchmark checks against NIST &amp; CIS rules</span>
            </li>
            <li>
              <CheckCircle2 size={16} />
              <span>Side-by-side policy report comparison</span>
            </li>
            <li>
              <CheckCircle2 size={16} />
              <span>Role-based access &amp; full activity log</span>
            </li>
          </ul>
        </section>

        <form onSubmit={handleSubmit} className="auth-form-panel">
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
      </div>
    </main>
  );
}
