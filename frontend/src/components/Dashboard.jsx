import React, { useState, useEffect } from 'react';
import {
  ClipboardList,
  ShieldCheck,
  ArrowRight,
  FileText,
  Users,
} from 'lucide-react';
import { api } from '../api';

export default function Dashboard({ user, onStartEvaluation, onViewReport, onNavigate }) {
  const [stats, setStats] = useState(null);
  const [activePolicy, setActivePolicy] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([api.getDashboardStats(), api.getActivePolicy()])
      .then(([statsData, policyData]) => {
        setStats(statsData);
        setActivePolicy(policyData);
      })
      .catch(() => setError('Could not load the overview. Refresh the page to try again.'));
  }, []);

  const recent = stats?.recent_evaluations || [];
  const highRiskCount = (stats?.risk_breakdown?.High || 0) + (stats?.risk_breakdown?.Critical || 0);

  return (
    <div className="overview-page">
      <div className="page-heading">
        <div>
          <span className="page-eyebrow">Workspace overview</span>
          <h1>Good to see you, {user?.full_name?.split(' ')[0] || 'there'}.</h1>
          <p>Review the active policy and recent evaluations from one place.</p>
        </div>
        {user?.role !== 'Viewer' && (
          <button className="btn-primary-custom" onClick={onStartEvaluation}>
            <ClipboardList size={17} /> Open policy editor
          </button>
        )}
      </div>

      {error && (
        <div className="overview-error" role="alert">
          {error}
        </div>
      )}

      <div className="overview-grid">
        <section className="overview-main">
          <div className="overview-panel active-policy-panel">
            <div className="panel-heading">
              <div>
                <span className="section-label">Current configuration</span>
                <h2>Active policy</h2>
              </div>
              <span className={`status-pill ${activePolicy ? 'status-live' : 'status-empty'}`}>
                {activePolicy ? 'Active' : 'Not set'}
              </span>
            </div>

            {activePolicy ? (
              <>
                <h3 className="active-policy-name">{activePolicy.name}</h3>
                <p className="panel-description">
                  These rules apply when people set or change passwords for accounts in this app.
                </p>
                <div className="policy-facts">
                  <div>
                    <span>Minimum length</span>
                    <strong>{activePolicy.min_length} characters</strong>
                  </div>
                  <div>
                    <span>Failed sign-ins</span>
                    <strong>{activePolicy.max_failed_attempts || 'No lockout limit'}</strong>
                  </div>
                  <div>
                    <span>Previous passwords</span>
                    <strong>{activePolicy.password_history_count}</strong>
                  </div>
                </div>
              </>
            ) : (
              <div className="empty-policy">
                <ShieldCheck size={26} strokeWidth={1.5} />
                <div>
                  <strong>No policy is active yet</strong>
                  <p>Use the policy editor to review rules, then activate them for app accounts.</p>
                </div>
              </div>
            )}

            {user?.role !== 'Viewer' && (
              <button className="text-action" onClick={onStartEvaluation}>
                {activePolicy ? 'Review policy' : 'Set up a policy'} <ArrowRight size={16} />
              </button>
            )}
          </div>

          <div className="overview-panel recent-panel">
            <div className="panel-heading">
              <div>
                <span className="section-label">Saved work</span>
                <h2>Recent evaluations</h2>
              </div>
              <button className="text-action" onClick={() => onNavigate('history')}>
                All reports <ArrowRight size={16} />
              </button>
            </div>

            {recent.length ? (
              <div className="recent-list">
                {recent.map((item) => (
                  <button
                    key={item.id}
                    className="recent-item"
                    onClick={() => onViewReport(item.id)}
                  >
                    <span className="recent-icon">
                      <FileText size={18} />
                    </span>
                    <span className="recent-copy">
                      <strong>{item.policy_name}</strong>
                      <small>
                        {item.standard_name} · {new Date(item.evaluated_at).toLocaleDateString()}
                      </small>
                    </span>
                    <span className="recent-score">{item.overall_compliance_score}%</span>
                    <ArrowRight size={16} className="recent-arrow" />
                  </button>
                ))}
              </div>
            ) : (
              <div className="recent-empty">
                <FileText size={24} strokeWidth={1.5} />
                <strong>No evaluations yet</strong>
                <p>Run a policy check to create your first report.</p>
              </div>
            )}
          </div>
        </section>

        <aside className="overview-aside">
          <div className="overview-panel summary-panel">
            <span className="section-label">At a glance</span>
            <h2>Reports</h2>
            <div className="summary-row">
              <span>Evaluations</span>
              <strong>{stats?.total_evaluations ?? '—'}</strong>
            </div>
            <div className="summary-row">
              <span>Average score</span>
              <strong>
                {stats?.total_evaluations ? `${stats.average_compliance_score}%` : '—'}
              </strong>
            </div>
            <div className="summary-row">
              <span>High or critical risk</span>
              <strong>{stats ? highRiskCount : '—'}</strong>
            </div>
          </div>

          <div className="overview-panel next-panel">
            <span className="section-label">Quick access</span>
            <button onClick={() => onNavigate('history')}>
              <FileText size={18} /> View reports <ArrowRight size={15} />
            </button>
            <button onClick={() => onNavigate('standards')}>
              <ShieldCheck size={18} /> Browse benchmarks <ArrowRight size={15} />
            </button>
            {user?.role === 'Administrator' && (
              <button onClick={() => onNavigate('users')}>
                <Users size={18} /> Manage users <ArrowRight size={15} />
              </button>
            )}
          </div>
        </aside>
      </div>
    </div>
  );
}
