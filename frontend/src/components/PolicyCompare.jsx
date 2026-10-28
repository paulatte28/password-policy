import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { GitCompare, ArrowRight, ShieldCheck, AlertTriangle } from 'lucide-react';

export default function PolicyCompare({ onViewReport }) {
  const [reports, setReports] = useState([]);
  const [leftId, setLeftId] = useState("");
  const [rightId, setRightId] = useState("");
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
        fetchPair(data[0].id, data[1].id);
      } else if (data.length === 1) {
        setLeftId(data[0].id);
        const single = await api.getReport(data[0].id);
        setLeftReport(single);
      }
    } catch (err) {
      console.error("Failed to load reports for compare", err);
    }
  }

  async function fetchPair(lId, rId) {
    if (lId) {
      const l = await api.getReport(lId);
      setLeftReport(l);
    }
    if (rId) {
      const r = await api.getReport(rId);
      setRightReport(r);
    }
  }

  function handleLeftChange(id) {
    setLeftId(id);
    if (id) api.getReport(id).then(setLeftReport);
    else setLeftReport(null);
  }

  function handleRightChange(id) {
    setRightId(id);
    if (id) api.getReport(id).then(setRightReport);
    else setRightReport(null);
  }

  const leftSnap = leftReport?.policy_snapshot || {};
  const rightSnap = rightReport?.policy_snapshot || {};

  const compareRows = [
    { label: "Overall Compliance Score", left: leftReport ? `${leftReport.overall_compliance_score}% (Grade ${leftReport.grade_letter})` : "-", right: rightReport ? `${rightReport.overall_compliance_score}% (Grade ${rightReport.grade_letter})` : "-" },
    { label: "Calculated Risk Level", left: leftReport?.risk_level || "-", right: rightReport?.risk_level || "-" },
    { label: "Benchmark Standard", left: leftReport?.standard_name || "-", right: rightReport?.standard_name || "-" },
    { label: "1. Minimum Password Length", left: leftSnap.min_length ? `${leftSnap.min_length} chars` : "-", right: rightSnap.min_length ? `${rightSnap.min_length} chars` : "-" },
    { label: "2. Complexity Categories", left: leftSnap.min_categories ? `${leftSnap.min_categories} of 4` : "-", right: rightSnap.min_categories ? `${rightSnap.min_categories} of 4` : "-" },
    { label: "3. Max Failed Attempts (Lockout)", left: leftSnap.max_failed_attempts !== undefined ? (leftSnap.max_failed_attempts === 0 ? "Disabled (Fail)" : `${leftSnap.max_failed_attempts} fails`) : "-", right: rightSnap.max_failed_attempts !== undefined ? (rightSnap.max_failed_attempts === 0 ? "Disabled (Fail)" : `${rightSnap.max_failed_attempts} fails`) : "-" },
    { label: "Lockout Duration", left: leftSnap.lockout_duration_min !== undefined ? `${leftSnap.lockout_duration_min} mins` : "-", right: rightSnap.lockout_duration_min !== undefined ? `${rightSnap.lockout_duration_min} mins` : "-" },
    { label: "4. Expiration Interval (Max Age)", left: leftSnap.max_password_age_days !== undefined ? (leftSnap.max_password_age_days === 0 ? "Never (NIST)" : `${leftSnap.max_password_age_days} days`) : "-", right: rightSnap.max_password_age_days !== undefined ? (rightSnap.max_password_age_days === 0 ? "Never (NIST)" : `${rightSnap.max_password_age_days} days`) : "-" },
    { label: "5. Password History Depth", left: leftSnap.password_history_count !== undefined ? `${leftSnap.password_history_count} remembered` : "-", right: rightSnap.password_history_count !== undefined ? `${rightSnap.password_history_count} remembered` : "-" },
    { label: "Dictionary / Leaked Screening", left: leftSnap.disallow_common ? "Enforced" : "Disabled", right: rightSnap.disallow_common ? "Enforced" : "Disabled" },
    { label: "MFA Authentication Enforced", left: leftSnap.require_mfa ? "Yes" : "No", right: rightSnap.require_mfa ? "Yes" : "No" },
  ];

  return (
    <div style={{ maxWidth: "1150px", margin: "0 auto", padding: "32px 20px" }}>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "2rem", fontWeight: 800, marginBottom: "4px" }}>
          Policy Comparison Matrix
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.92rem" }}>
          Side-by-side gap analysis comparing two password policy evaluations.
        </p>
      </div>

      {/* Selectors Bar */}
      <div className="sec-card" style={{ padding: "18px 24px", marginBottom: "28px", display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: "20px", alignItems: "center" }}>
        <div>
          <label style={{ display: "block", fontSize: "0.8rem", color: "var(--text-muted)", fontWeight: 700, textTransform: "uppercase", marginBottom: "6px" }}>
            Policy A (Baseline)
          </label>
          <select 
            value={leftId} 
            onChange={(e) => handleLeftChange(e.target.value)}
            className="sec-input"
          >
            <option value="">-- Choose Evaluation --</option>
            {reports.map(r => (
              <option key={r.id} value={r.id}>
                {r.policy_name} ({r.overall_compliance_score}%)
              </option>
            ))}
          </select>
        </div>

        <div style={{ color: "var(--accent-cyan)", display: "flex", alignItems: "center", justifyContent: "center" }}>
          <GitCompare size={24} />
        </div>

        <div>
          <label style={{ display: "block", fontSize: "0.8rem", color: "var(--text-muted)", fontWeight: 700, textTransform: "uppercase", marginBottom: "6px" }}>
            Policy B (Target / Comparison)
          </label>
          <select 
            value={rightId} 
            onChange={(e) => handleRightChange(e.target.value)}
            className="sec-input"
          >
            <option value="">-- Choose Evaluation --</option>
            {reports.map(r => (
              <option key={r.id} value={r.id}>
                {r.policy_name} ({r.overall_compliance_score}%)
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="sec-card" style={{ padding: "0", overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.9rem" }}>
          <thead>
            <tr style={{ background: "rgba(255,255,255,0.03)", borderBottom: "1px solid var(--border-subtle)" }}>
              <th style={{ padding: "16px 20px", color: "var(--text-muted)", width: "35%" }}>Rule / Metric</th>
              <th style={{ padding: "16px 20px", color: "var(--primary)", width: "32.5%", fontWeight: 700 }}>
                {leftReport?.policy_name || "Policy A"}
              </th>
              <th style={{ padding: "16px 20px", color: "var(--accent-cyan)", width: "32.5%", fontWeight: 700 }}>
                {rightReport?.policy_name || "Policy B"}
              </th>
            </tr>
          </thead>
          <tbody>
            {compareRows.map((row, idx) => {
              const isDifferent = row.left !== row.right;
              return (
                <tr 
                  key={idx} 
                  style={{ 
                    borderBottom: "1px solid rgba(255, 255, 255, 0.04)",
                    background: isDifferent ? "rgba(6, 182, 212, 0.04)" : "transparent"
                  }}
                >
                  <td style={{ padding: "14px 20px", fontWeight: 600, color: "var(--text-secondary)" }}>
                    {row.label}
                  </td>
                  <td style={{ padding: "14px 20px", color: "var(--text-primary)", fontWeight: isDifferent ? 700 : 400 }}>
                    {row.left}
                  </td>
                  <td style={{ padding: "14px 20px", color: "var(--text-primary)", fontWeight: isDifferent ? 700 : 400 }}>
                    {row.right}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
