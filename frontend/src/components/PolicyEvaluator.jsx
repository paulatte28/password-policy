import React, { useState, useEffect } from 'react';
import {
  Upload,
  Download,
  Key,
  CheckSquare,
  Lock,
  RefreshCw,
  SlidersVertical,
  Play,
} from 'lucide-react';
import { api } from '../api';

export default function PolicyEvaluator({ onEvaluationComplete, user }) {
  const [standards, setStandards] = useState([]);
  const [selectedStandard, setSelectedStandard] = useState('NIST_SP_800_63B');
  const [loading, setLoading] = useState(false);
  const [importing, setImporting] = useState(false);
  const [importStatus, setImportStatus] = useState('');
  const [activePolicyName, setActivePolicyName] = useState(null);
  const [policy, setPolicy] = useState({
    name: 'Enterprise Password Policy',
    description: 'Default baseline evaluation for organization systems',
    min_length: 12,
    max_length: 64,
    require_uppercase: true,
    require_lowercase: true,
    require_digit: true,
    require_special: true,
    min_categories: 3,
    max_failed_attempts: 5,
    lockout_duration_min: 15,
    lockout_reset_min: 15,
    max_password_age_days: 90,
    min_password_age_days: 1,
    password_history_count: 5,
    disallow_common: true,
    disallow_username: true,
    require_mfa: false,
  });

  useEffect(() => {
    loadStandards();
    api.getActivePolicy()
      .then((data) => {
        setActivePolicyName(data?.name || null);
        if (data) setPolicy(data);
      })
      .catch(() => {});
  }, []);

  async function handleActivate() {
    if (
      !window.confirm(
        `Activate "${policy.name}" for accounts in this app? All users will need to change their passwords at next sign in.`
      )
    ) {
      return;
    }
    try {
      await api.activatePolicy(policy);
      window.alert('Policy activated. Please change your own password now.');
      window.location.reload();
    } catch (err) {
      window.alert(`Activation failed: ${err.message}`);
    }
  }

  async function loadStandards() {
    try {
      const data = await api.getStandards();
      setStandards(data);
    } catch (err) {
      console.error('Failed to load standards', err);
    }
  }

  function applySample(type) {
    if (type === 'weak') {
      setPolicy({
        name: 'Weak Legacy Policy (High Risk Demo)',
        description: 'Legacy configuration with short length, disabled lockout, and no dictionary check.',
        min_length: 6,
        max_length: 16,
        require_uppercase: false,
        require_lowercase: true,
        require_digit: true,
        require_special: false,
        min_categories: 2,
        max_failed_attempts: 0,
        lockout_duration_min: 0,
        lockout_reset_min: 0,
        max_password_age_days: 30,
        min_password_age_days: 0,
        password_history_count: 0,
        disallow_common: false,
        disallow_username: false,
        require_mfa: false,
      });
    } else if (type === 'moderate') {
      setPolicy({
        name: 'Moderate Enterprise Baseline',
        description: 'Standard corporate configuration with 8 characters, lockout, and 90-day rotation.',
        min_length: 8,
        max_length: 64,
        require_uppercase: true,
        require_lowercase: true,
        require_digit: true,
        require_special: false,
        min_categories: 3,
        max_failed_attempts: 10,
        lockout_duration_min: 15,
        lockout_reset_min: 15,
        max_password_age_days: 90,
        min_password_age_days: 1,
        password_history_count: 3,
        disallow_common: true,
        disallow_username: true,
        require_mfa: false,
      });
    } else if (type === 'strong') {
      setPolicy({
        name: 'Strong Passphrase Policy (Demo)',
        description: 'Example proposal with 15+ length, lockout, no scheduled rotation, and an MFA requirement that cannot yet be activated.',
        min_length: 15,
        max_length: 128,
        require_uppercase: true,
        require_lowercase: true,
        require_digit: true,
        require_special: true,
        min_categories: 3,
        max_failed_attempts: 5,
        lockout_duration_min: 30,
        lockout_reset_min: 30,
        max_password_age_days: 0,
        min_password_age_days: 1,
        password_history_count: 10,
        disallow_common: true,
        disallow_username: true,
        require_mfa: true,
      });
    }
  }

  function updateField(field, value) {
    setPolicy((prev) => ({ ...prev, [field]: value }));
  }

  function handleExportJson() {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(policy, null, 2));
    const a = document.createElement('a');
    a.setAttribute('href', dataStr);
    a.setAttribute('download', `${policy.name.replace(/\s+/g, '_').toLowerCase()}.json`);
    a.click();
  }

  async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    try {
      setImporting(true);
      setImportStatus('');
      const imported = await api.importFile(file);
      setPolicy((prev) => ({
        ...prev,
        ...imported,
        name: imported.name || file.name.replace(/\.[^/.]+$/, ''),
      }));
      setImportStatus(`Successfully imported '${file.name}'`);
    } catch (err) {
      setImportStatus(`Import error: ${err.message}`);
    } finally {
      setImporting(false);
      e.target.value = null;
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      setLoading(true);
      const payload = {
        ...policy,
        standard_id: selectedStandard,
        save_report: true,
      };
      const result = await api.evaluatePolicy(payload);
      onEvaluationComplete(result);
    } catch (err) {
      alert(`Evaluation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="workspace-page policy-editor">
      <div style={{ marginBottom: '28px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '16px', marginBottom: '12px' }}>
          <div>
            <span className="page-eyebrow">Policy management</span>
            <h1>Policy editor</h1>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
              Set the rules, check them against a benchmark, then activate them for app accounts.
            </p>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>Start from:</span>
            <button type="button" onClick={() => applySample('weak')} className="btn-secondary-custom" style={{ padding: '6px 12px', fontSize: '0.8rem', color: 'var(--color-fail)' }}>
              Weak example
            </button>
            <button type="button" onClick={() => applySample('moderate')} className="btn-secondary-custom" style={{ padding: '6px 12px', fontSize: '0.8rem', color: 'var(--color-warning)' }}>
              Moderate example
            </button>
            <button type="button" onClick={() => applySample('strong')} className="btn-secondary-custom" style={{ padding: '6px 12px', fontSize: '0.8rem', color: 'var(--color-pass)' }}>
              Strong example
            </button>
          </div>
        </div>

        <div className="sec-card" style={{ padding: '14px 20px', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <label className="btn-secondary-custom" style={{ padding: '6px 14px', fontSize: '0.82rem', cursor: 'pointer', margin: 0 }}>
              <Upload size={14} /> Import External Policy (JSON / CSV)
              <input type="file" accept=".json,.csv" onChange={handleFileUpload} style={{ display: 'none' }} />
            </label>
            <button type="button" onClick={handleExportJson} className="btn-secondary-custom" style={{ padding: '6px 14px', fontSize: '0.82rem' }}>
              <Download size={14} /> Export JSON
            </button>
          </div>
          {importStatus && (
            <div style={{ fontSize: '0.82rem', color: importStatus.startsWith('Success') ? 'var(--color-pass)' : 'var(--color-fail)' }}>
              {importStatus}
            </div>
          )}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <label style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)' }}>Benchmark Standard:</label>
            <select
              value={selectedStandard}
              onChange={(e) => setSelectedStandard(e.target.value)}
              className="sec-input"
              style={{ padding: '6px 12px', fontSize: '0.85rem', width: 'auto' }}
            >
              {standards.map((s) => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="editor-status">
        <span className={`status-pill ${activePolicyName ? 'status-live' : 'status-empty'}`}>
          {activePolicyName ? 'Active policy' : 'No active policy'}
        </span>
        <strong>{activePolicyName || 'None yet'}</strong>
      </div>

      <nav className="editor-jump" aria-label="Policy sections">
        <a href="#policy-details">Details</a>
        <a href="#policy-length">Length</a>
        <a href="#policy-complexity">Complexity</a>
        <a href="#policy-lockout">Sign-in</a>
        <a href="#policy-lifecycle">Lifecycle</a>
        <a href="#policy-reuse">Reuse</a>
        <a href="#policy-hygiene">Other rules</a>
      </nav>

      <form onSubmit={handleSubmit}>
        <div id="policy-details" className="sec-card" style={{ marginBottom: '24px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '18px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Policy Name
              </label>
              <input
                type="text"
                value={policy.name}
                onChange={(e) => updateField('name', e.target.value)}
                required
                className="sec-input"
                placeholder="e.g. Enterprise Active Directory Password Policy"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Description / Scope
              </label>
              <input
                type="text"
                value={policy.description}
                onChange={(e) => updateField('description', e.target.value)}
                className="sec-input"
                placeholder="e.g. Mandatory baseline for IT and system administration users"
              />
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', marginBottom: '32px' }}>
          {/* 1. Password Length */}
          <div id="policy-length" className="sec-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(141, 53, 105, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--accent-cyan)' }}>
                <Key size={18} />
              </div>
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>1. Password Length Requirements</h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Short lengths (under 8 characters) result in critical failure. Recommended: 12-15+ characters.
                </div>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px', alignItems: 'center' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                  <label style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>Minimum Length</label>
                  <span style={{ fontSize: '0.95rem', fontWeight: 800, color: policy.min_length < 8 ? 'var(--color-fail)' : policy.min_length < 12 ? 'var(--color-warning)' : 'var(--color-pass)' }}>
                    {policy.min_length} characters
                  </span>
                </div>
                <input
                  type="range"
                  min="4"
                  max="32"
                  value={policy.min_length}
                  onChange={(e) => updateField('min_length', parseInt(e.target.value))}
                  style={{ width: '100%', accentColor: 'var(--accent-cyan)', cursor: 'pointer' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Maximum Allowed Length
                </label>
                <input
                  type="number"
                  min="16"
                  max="256"
                  value={policy.max_length}
                  onChange={(e) => updateField('max_length', parseInt(e.target.value))}
                  className="sec-input"
                />
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  NIST recommends allowing at least 64 characters for passphrases.
                </div>
              </div>
            </div>
          </div>

          {/* 2. Character Complexity */}
          <div id="policy-complexity" className="sec-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(99, 35, 70, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                <CheckSquare size={18} />
              </div>
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>2. Character Complexity Rules</h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Enforce character diversity (Uppercase, Lowercase, Numbers, Symbols).
                </div>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '16px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.require_uppercase} onChange={(e) => updateField('require_uppercase', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Require Uppercase (A-Z)</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.require_lowercase} onChange={(e) => updateField('require_lowercase', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Require Lowercase (a-z)</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.require_digit} onChange={(e) => updateField('require_digit', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Require Numbers (0-9)</span>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.require_special} onChange={(e) => updateField('require_special', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <span style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>Require Symbols (!@#$%)</span>
              </label>
            </div>
            <div style={{ maxWidth: '300px' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Minimum Character Categories Required
              </label>
              <select
                value={policy.min_categories}
                onChange={(e) => updateField('min_categories', parseInt(e.target.value))}
                className="sec-input"
              >
                <option value={1}>1 Category</option>
                <option value={2}>2 Categories</option>
                <option value={3}>3 Categories (Common Standard)</option>
                <option value={4}>All 4 Categories</option>
              </select>
            </div>
          </div>

          {/* 3. Account Lockout */}
          <div id="policy-lockout" className="sec-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(245, 158, 11, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-warning)' }}>
                <Lock size={18} />
              </div>
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>3. Account Lockout & Brute-Force Defense</h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Absence of lockout (0 attempts) leaves systems open to automated guessing.
                </div>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '18px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Max Failed Attempts Threshold
                </label>
                <input
                  type="number"
                  min="0"
                  max="50"
                  value={policy.max_failed_attempts}
                  onChange={(e) => updateField('max_failed_attempts', parseInt(e.target.value))}
                  className="sec-input"
                />
                <div style={{ fontSize: '0.72rem', color: policy.max_failed_attempts === 0 ? 'var(--color-fail)' : 'var(--text-muted)', marginTop: '4px' }}>
                  {policy.max_failed_attempts === 0 ? '⚠️ Lockout disabled! Will fail compliance check.' : 'Recommended: 5 or fewer attempts.'}
                </div>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Lockout Duration (Minutes)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1440"
                  value={policy.lockout_duration_min}
                  onChange={(e) => updateField('lockout_duration_min', parseInt(e.target.value))}
                  className="sec-input"
                />
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Minimum 15-30 minutes recommended.
                </div>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Counter Reset Window (Minutes)
                </label>
                <input
                  type="number"
                  min="0"
                  max="1440"
                  value={policy.lockout_reset_min}
                  onChange={(e) => updateField('lockout_reset_min', parseInt(e.target.value))}
                  className="sec-input"
                />
              </div>
            </div>
          </div>

          {/* 4. Password Expiration */}
          <div id="policy-lifecycle" className="sec-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(16, 185, 129, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--color-pass)' }}>
                <RefreshCw size={18} />
              </div>
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>4. Password Expiration & Lifecycle</h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  NIST discourages arbitrary forced rotation; OWASP/PCI recommends 90 days.
                </div>
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '18px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Maximum Password Age (Days)
                </label>
                <input
                  type="number"
                  min="0"
                  max="730"
                  value={policy.max_password_age_days}
                  onChange={(e) => updateField('max_password_age_days', parseInt(e.target.value))}
                  className="sec-input"
                />
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  0 = Passwords do not expire arbitrarily (NIST SP 800-63B guidance).
                </div>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                  Minimum Password Age (Days)
                </label>
                <input
                  type="number"
                  min="0"
                  max="30"
                  value={policy.min_password_age_days}
                  onChange={(e) => updateField('min_password_age_days', parseInt(e.target.value))}
                  className="sec-input"
                />
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '4px' }}>
                  Prevents users from immediately cycling passwords to bypass history limits.
                </div>
              </div>
            </div>
          </div>

          {/* 5. Password Reuse */}
          <div id="policy-reuse" className="sec-card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div style={{ width: '36px', height: '36px', borderRadius: '10px', background: 'rgba(99, 35, 70, 0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--primary)' }}>
                <SlidersVertical size={18} />
              </div>
              <div>
                <h3 style={{ fontSize: '1.05rem', fontWeight: 700 }}>5. Password Reuse (History Retention)</h3>
                <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  A history count of 0 is flagged as an immediate reuse vulnerability.
                </div>
              </div>
            </div>
            <div style={{ maxWidth: '340px' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)', marginBottom: '6px' }}>
                Number of Previous Passwords Remembered
              </label>
              <input
                type="number"
                min="0"
                max="50"
                value={policy.password_history_count}
                onChange={(e) => updateField('password_history_count', parseInt(e.target.value))}
                className="sec-input"
              />
              <div style={{ fontSize: '0.72rem', color: policy.password_history_count === 0 ? 'var(--color-fail)' : 'var(--text-muted)', marginTop: '4px' }}>
                {policy.password_history_count === 0 ? '⚠️ History = 0 allows immediate reuse of breached passwords!' : 'Recommended: 5 to 10 passwords remembered.'}
              </div>
            </div>
          </div>

          {/* 6. Security Hygiene */}
          <div id="policy-hygiene" className="sec-card">
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: '4px', color: 'var(--accent-cyan)' }}>
              6. Security Hygiene & Defense-in-Depth Controls
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginBottom: '16px' }}>
              Modern mitigation measures recommended by NIST SP 800-63B and OWASP.
            </p>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.disallow_common} onChange={(e) => updateField('disallow_common', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <div>
                  <div style={{ fontSize: '0.88rem', fontWeight: 600 }}>Block Common Passwords</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    Reject a small built-in list of common passwords; no live breach lookup
                  </div>
                </div>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.disallow_username} onChange={(e) => updateField('disallow_username', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <div>
                  <div style={{ fontSize: '0.88rem', fontWeight: 600 }}>Disallow Username in Password</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    Block usernames, emails, or company name tokens
                  </div>
                </div>
              </label>
              <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                <input type="checkbox" checked={policy.require_mfa} onChange={(e) => updateField('require_mfa', e.target.checked)} style={{ width: '18px', height: '18px', accentColor: 'var(--accent-cyan)' }} />
                <div>
                  <div style={{ fontSize: '0.88rem', fontWeight: 600 }}>Require Multi-Factor Authentication (MFA)</div>
                  <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                    Evaluation only; activation is blocked until MFA is implemented
                  </div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <div className="editor-actions">
          <p>Evaluation saves a report. Activation changes the rules used for app accounts.</p>
          <div className="editor-action-buttons">
            {user?.role === 'Administrator' && (
              <button type="button" className="btn-secondary-custom" onClick={handleActivate}>
                Activate these rules
              </button>
            )}
            <button type="submit" disabled={loading} className="btn-cyan-custom" style={{ padding: '11px 20px', justifyContent: 'center' }}>
              {loading ? (
                'Evaluating Policy...'
              ) : (
                <>
                  <Play size={17} /> Evaluate policy
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
