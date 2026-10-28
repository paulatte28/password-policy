import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { FileText, Shield, User, Clock, Terminal } from 'lucide-react';

export default function AuditLogsView() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAuditLogs();
  }, []);

  async function loadAuditLogs() {
    try {
      setLoading(true);
      const data = await api.getAuditLogs();
      setLogs(data);
    } catch (err) {
      console.error("Failed to load audit logs", err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: "1150px", margin: "0 auto", padding: "32px 20px" }}>
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "2rem", fontWeight: 800, marginBottom: "4px" }}>
          Security Audit Trail
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.92rem" }}>
          Immutable log of all password policy evaluations, standard edits, user actions, and system logins.
        </p>
      </div>

      <div className="sec-card" style={{ padding: "0", overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.88rem" }}>
          <thead>
            <tr style={{ background: "rgba(255,255,255,0.03)", borderBottom: "1px solid var(--border-subtle)", color: "var(--text-muted)", textTransform: "uppercase", fontSize: "0.75rem", letterSpacing: "0.05em" }}>
              <th style={{ padding: "14px 20px" }}>Timestamp</th>
              <th style={{ padding: "14px 20px" }}>Action</th>
              <th style={{ padding: "14px 20px" }}>Actor / User</th>
              <th style={{ padding: "14px 20px" }}>Role</th>
              <th style={{ padding: "14px 20px" }}>Audit Details</th>
              <th style={{ padding: "14px 20px" }}>IP Address</th>
            </tr>
          </thead>
          <tbody>
            {logs.map(log => {
              let actionBadge = "var(--accent-cyan)";
              if (log.action.includes("LOGIN")) actionBadge = "var(--primary)";
              else if (log.action.includes("EVAL")) actionBadge = "var(--color-pass)";
              else if (log.action.includes("USER") || log.action.includes("STANDARD")) actionBadge = "var(--color-warning)";

              return (
                <tr key={log.id} style={{ borderBottom: "1px solid rgba(255, 255, 255, 0.04)" }}>
                  <td style={{ padding: "14px 20px", color: "var(--text-muted)", fontSize: "0.82rem", whiteSpace: "nowrap" }}>
                    {new Date(log.timestamp).toLocaleString()}
                  </td>
                  <td style={{ padding: "14px 20px" }}>
                    <span style={{ fontSize: "0.75rem", fontWeight: 700, color: actionBadge, background: "rgba(255,255,255,0.05)", padding: "2px 8px", borderRadius: "4px" }}>
                      {log.action}
                    </span>
                  </td>
                  <td style={{ padding: "14px 20px", fontWeight: 600, color: "var(--text-primary)" }}>
                    {log.user_name}
                  </td>
                  <td style={{ padding: "14px 20px", color: "var(--text-secondary)", fontSize: "0.82rem" }}>
                    {log.user_role}
                  </td>
                  <td style={{ padding: "14px 20px", color: "var(--text-secondary)", lineHeight: 1.4 }}>
                    {log.details}
                  </td>
                  <td style={{ padding: "14px 20px", color: "var(--text-muted)", fontSize: "0.8rem", fontFamily: "monospace" }}>
                    {log.ip_address}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        {logs.length === 0 && !loading && (
          <div style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
            No audit records found.
          </div>
        )}
      </div>
    </div>
  );
}
