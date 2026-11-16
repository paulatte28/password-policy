import React, { useState, useEffect } from 'react';
import { GitCompare } from 'lucide-react';
import { api } from '../api';

export default function PolicyCompare({ onViewReport }) {
  const [reports, setReports] = useState([]);
  const [leftId, setLeftId] = useState('');
  const [rightId, setRightId] = useState('');
  const [leftReport, setLeftReport] = useState(null);
  const [rightReport, setRightReport] = useState(null);

  useEffect(() => {
    loadReports();
  }, []);

  async function loadReports() {
    try {
      const data = await api.getReports();
      setReports(data);
      if (data.length >= 2) {
        setLeftId(data[0].id);
        setRightId(data[1].id);
        loadPair(data[0].id, data[1].id);
      } else if (data.length === 1) {
        setLeftId(data[0].id);
        const r = await api.getReport(data[0].id);
        setLeftReport(r);
      }
    } catch (err) {
      console.error('Failed to load reports for compare', err);
    }
  }

  async function loadPair(idA, idB) {
    if (idA) {
      const a = await api.getReport(idA);
      setLeftReport(a);
    }
    if (idB) {
      const b = await api.getReport(idB);
      setRightReport(b);
    }
  }

  function handleSelectLeft(id) {
    setLeftId(id);
    if (id) api.getReport(id).then(setLeftReport);
    else setLeftReport(null);
  }

  function handleSelectRight(id) {
    setRightId(id);
    if (id) api.getReport(id).then(setRightReport);
    else setRightReport(null);
  }

  const snapL = leftReport?.policy_snapshot || {};
  const snapR = rightReport?.policy_snapshot || {};

  const rows = [
    {
      label: 'Overall Compliance Score',
      left: leftReport ? `${leftReport.overall_compliance_score}% (Grade ${leftReport.grade_letter})` : '-',
      right: rightReport ? `${rightReport.overall_compliance_score}% (Grade ${rightReport.grade_letter})` : '-',
    },
    {
      label: 'Calculated Risk Level',
      left: leftReport?.risk_level || '-',
      right: rightReport?.risk_level || '-',
    },
    {
      label: 'Benchmark Standard',
      left: leftReport?.standard_name || '-',
      right: rightReport?.standard_name || '-',
    },
    {
      label: '1. Minimum Password Length',
      left: snapL.min_length ? `${snapL.min_length} chars` : '-',
      right: snapR.min_length ? `${snapR.min_length} chars` : '-',
    },
    {
      label: '2. Complexity Categories',
      left: snapL.min_categories ? `${snapL.min_categories} of 4` : '-',
      right: snapR.min_categories ? `${snapR.min_categories} of 4` : '-',
    },
    {
      label: '3. Max Failed Attempts (Lockout)',
      left: snapL.max_failed_attempts === undefined ? '-' : snapL.max_failed_attempts === 0 ? 'Disabled (Fail)' : `${snapL.max_failed_attempts} fails`,
      right: snapR.max_failed_attempts === undefined ? '-' : snapR.max_failed_attempts === 0 ? 'Disabled (Fail)' : `${snapR.max_failed_attempts} fails`,
    },
    {
      label: 'Lockout Duration',
      left: snapL.lockout_duration_min === undefined ? '-' : `${snapL.lockout_duration_min} mins`,
      right: snapR.lockout_duration_min === undefined ? '-' : `${snapR.lockout_duration_min} mins`,
    },
    {
      label: '4. Expiration Interval (Max Age)',
      left: snapL.max_password_age_days === undefined ? '-' : snapL.max_password_age_days === 0 ? 'Never (NIST)' : `${snapL.max_password_age_days} days`,
      right: snapR.max_password_age_days === undefined ? '-' : snapR.max_password_age_days === 0 ? 'Never (NIST)' : `${snapR.max_password_age_days} days`,
    },
    {
      label: '5. Password History Depth',
      left: snapL.password_history_count === undefined ? '-' : `${snapL.password_history_count} remembered`,
      right: snapR.password_history_count === undefined ? '-' : `${snapR.password_history_count} remembered`,
    },
    {
      label: 'Common-password option',
      left: snapL.disallow_common ? 'Selected' : 'Off',
      right: snapR.disallow_common ? 'Selected' : 'Off',
    },
    {
      label: 'MFA option in proposal',
      left: snapL.require_mfa ? 'Selected' : 'Off',
      right: snapR.require_mfa ? 'Selected' : 'Off',
    },
  ];

  return (
    <div className="workspace-page">
      <div style={{ marginBottom: '28px' }}>
        <span className="page-eyebrow">Saved work</span>
        <h1>Compare reports</h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
          Select two reports to see how their rules and results differ.
        </p>
      </div>

      <div className="sec-card" style={{ padding: '18px 24px', marginBottom: '28px', display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: '20px', alignItems: 'center' }}>
        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
            Policy A (Baseline)
          </label>
          <select value={leftId} onChange={(e) => handleSelectLeft(e.target.value)} className="sec-input">
            <option value="">-- Choose Evaluation --</option>
            {reports.map((r) => (
              <option key={r.id} value={r.id}>
                {r.policy_name} ({r.overall_compliance_score}%)
              </option>
            ))}
          </select>
        </div>

        <div style={{ color: 'var(--accent-cyan)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <GitCompare size={24} />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
            Policy B (Target / Comparison)
          </label>
          <select value={rightId} onChange={(e) => handleSelectRight(e.target.value)} className="sec-input">
            <option value="">-- Choose Evaluation --</option>
            {reports.map((r) => (
              <option key={r.id} value={r.id}>
                {r.policy_name} ({r.overall_compliance_score}%)
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="sec-card" style={{ padding: 0, overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
          <thead>
            <tr style={{ background: 'var(--bg-table-head)', borderBottom: '1px solid var(--border-subtle)' }}>
              <th style={{ padding: '16px 20px', color: 'var(--text-muted)', width: '35%' }}>Rule / Metric</th>
              <th style={{ padding: '16px 20px', color: 'var(--primary)', width: '32.5%', fontWeight: 700 }}>
                {leftReport?.policy_name || 'Policy A'}
              </th>
              <th style={{ padding: '16px 20px', color: 'var(--accent-cyan)', width: '32.5%', fontWeight: 700 }}>
                {rightReport?.policy_name || 'Policy B'}
              </th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => {
              const differs = r.left !== r.right;
              return (
                <tr key={i} style={{ borderBottom: '1px solid var(--border-subtle)', background: differs ? 'rgba(141, 53, 105, 0.04)' : 'transparent' }}>
                  <td style={{ padding: '14px 20px', fontWeight: 600, color: 'var(--text-secondary)' }}>{r.label}</td>
                  <td style={{ padding: '14px 20px', color: 'var(--text-primary)', fontWeight: differs ? 700 : 400 }}>{r.left}</td>
                  <td style={{ padding: '14px 20px', color: 'var(--text-primary)', fontWeight: differs ? 700 : 400 }}>{r.right}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
