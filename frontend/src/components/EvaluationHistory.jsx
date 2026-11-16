import React, { useState, useEffect } from 'react';
import { Search, Eye, Download } from 'lucide-react';
import { api } from '../api';

export default function EvaluationHistory({ onViewReport }) {
  const [reports, setReports] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReports();
  }, []);

  async function loadReports() {
    try {
      setLoading(true);
      const data = await api.getReports();
      setReports(data);
    } catch (err) {
      console.error('Failed to load reports', err);
    } finally {
      setLoading(false);
    }
  }

  const filtered = reports.filter(
    (r) =>
      r.policy_name.toLowerCase().includes(search.toLowerCase()) ||
      r.standard_name.toLowerCase().includes(search.toLowerCase()) ||
      r.evaluated_by_user.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="workspace-page">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px', marginBottom: '28px' }}>
        <div>
          <span className="page-eyebrow">Saved work</span>
          <h1>Reports</h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.92rem' }}>
            Review and export your saved policy evaluations.
          </p>
        </div>

        <div style={{ position: 'relative', minWidth: '260px' }}>
          <Search size={16} style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
          <input
            type="text"
            placeholder="Search policies or standards..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="sec-input"
            style={{ paddingLeft: '36px' }}
          />
        </div>
      </div>

      <div className="sec-card data-table-wrap" style={{ padding: 0 }}>
        <table className="data-table" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
          <thead>
            <tr style={{ background: 'var(--bg-table-head)', borderBottom: '1px solid var(--border-subtle)', color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: '0.75rem', letterSpacing: '0.05em' }}>
              <th style={{ padding: '14px 20px' }}>Policy Name</th>
              <th style={{ padding: '14px 20px' }}>Benchmark Standard</th>
              <th style={{ padding: '14px 20px' }}>Rating &amp; Grade</th>
              <th style={{ padding: '14px 20px' }}>Risk Level</th>
              <th style={{ padding: '14px 20px' }}>Evaluator</th>
              <th style={{ padding: '14px 20px' }}>Date</th>
              <th style={{ padding: '14px 20px', textAlign: 'right' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((r) => {
              let badgeClass = 'badge-pass';
              if (r.risk_level === 'Critical' || r.risk_level === 'High') badgeClass = 'badge-fail';
              else if (r.risk_level === 'Moderate') badgeClass = 'badge-warning';

              return (
                <tr key={r.id} style={{ borderBottom: '1px solid var(--border-subtle)' }}>
                  <td style={{ padding: '14px 20px', fontWeight: 600, color: 'var(--text-primary)' }}>{r.policy_name}</td>
                  <td style={{ padding: '14px 20px', color: 'var(--text-secondary)' }}>{r.standard_name}</td>
                  <td style={{ padding: '14px 20px' }}>
                    <span style={{ fontWeight: 700, color: r.overall_compliance_score >= 80 ? 'var(--color-pass)' : r.overall_compliance_score >= 60 ? 'var(--color-warning)' : 'var(--color-fail)' }}>
                      {r.overall_compliance_score}%
                    </span>
                    <span style={{ marginLeft: '6px', fontSize: '0.75rem', background: 'var(--bg-inset)', padding: '2px 6px', borderRadius: '4px' }}>
                      {r.grade_letter}
                    </span>
                  </td>
                  <td style={{ padding: '14px 20px' }}>
                    <span className={badgeClass}>{r.risk_level}</span>
                  </td>
                  <td style={{ padding: '14px 20px', color: 'var(--text-muted)', fontSize: '0.82rem' }}>{r.evaluated_by_user}</td>
                  <td style={{ padding: '14px 20px', color: 'var(--text-muted)', fontSize: '0.82rem' }}>
                    {new Date(r.evaluated_at).toLocaleString()}
                  </td>
                  <td style={{ padding: '14px 20px', textAlign: 'right' }}>
                    <div style={{ display: 'inline-flex', gap: '8px' }}>
                      <button onClick={() => onViewReport(r.id)} className="btn-cyan-custom" style={{ padding: '6px 12px', fontSize: '0.78rem' }}>
                        <Eye size={13} /> View
                      </button>
                      <button onClick={() => api.downloadReportCsv(r.id).catch((err) => alert(err.message))} className="btn-secondary-custom" style={{ padding: '6px 12px', fontSize: '0.78rem' }}>
                        <Download size={13} /> CSV
                      </button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
        {filtered.length === 0 && !loading && (
          <div style={{ textAlign: 'center', padding: '40px', color: 'var(--text-muted)' }}>
            No evaluation reports matched your search criteria.
          </div>
        )}
      </div>
    </div>
  );
}
