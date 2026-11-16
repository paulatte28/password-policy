import React, { useState } from 'react';
import { api } from '../api';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
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
    <main style={{ flex: 1, display: 'grid', placeItems: 'center', padding: 24 }}>
      <form onSubmit={handleSubmit} className="sec-card" style={{ width: 'min(100%, 420px)', padding: 32 }}>
        <h1 style={{ fontSize: '1.6rem', marginBottom: 8 }}>Sign in</h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>
          Use the account created by your administrator.
        </p>
        {error && (
          <p role="alert" style={{ color: 'var(--color-fail)', marginBottom: 16 }}>
            {error}
          </p>
        )}
        <label htmlFor="login-email">Email</label>
        <input
          id="login-email"
          className="sec-input"
          type="email"
          autoComplete="username"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ margin: '8px 0 18px' }}
        />
        <label htmlFor="login-password">Password</label>
        <input
          id="login-password"
          className="sec-input"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ margin: '8px 0 24px' }}
        />
        <button
          className="btn-cyan-custom"
          type="submit"
          disabled={loading}
          style={{ width: '100%', justifyContent: 'center' }}
        >
          {loading ? 'Signing in...' : 'Sign in'}
        </button>
      </form>
    </main>
  );
}
