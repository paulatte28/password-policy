import React, { useEffect, useState } from 'react';
import { api } from '../api';
import { 
  ShieldCheck, AlertTriangle, Layers, Play, Eye, 
  ArrowUpRight, Award, Activity, CheckCircle, Clock 
} from 'lucide-react';
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement
} from 'chart.js';
import { Radar, Doughnut } from 'react-chartjs-2';

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement
);

export default function Dashboard({ onStartEvaluation, onViewReport }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  async function loadDashboardData() {
    try {
      setLoading(true);
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error("Failed to load dashboard stats", err);
    } finally {
      setLoading(false);
    }
  }

  // Radar Chart Data (Dimension Baseline)
  const radarData = {
    labels: ['Length (30%)', 'Complexity (15%)', 'Lockout (25%)', 'Expiration (10%)', 'Reuse (10%)', 'Hygiene (10%)'],
    datasets: [
      {
        label: 'Average Score',
        data: [85, 78, 88, 70, 80, 92],
        backgroundColor: 'rgba(6, 182, 212, 0.25)',
        borderColor: '#06b6d4',
        borderWidth: 2,
        pointBackgroundColor: '#e29bb3',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: '#06b6d4'
      },
      {
        label: 'Target Benchmark (NIST)',
        data: [100, 80, 100, 90, 100, 100],
        backgroundColor: 'rgba(226, 155, 179, 0.15)',
        borderColor: '#e29bb3',
        borderWidth: 2,
        borderDash: [4, 4]
      }
    ]
  };

  const radarOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: {
        angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
        grid: { color: 'rgba(255, 255, 255, 0.08)' },
        pointLabels: {
          color: '#cbd5e1',
          font: { size: 11, family: 'Inter' }
        },
        ticks: {
          backdropColor: 'transparent',
          color: '#94a3b8',
          stepSize: 20
        },
        suggestedMin: 0,
        suggestedMax: 100
      }
    },
    plugins: {
      legend: {
        labels: { color: '#e2e8f0', font: { family: 'Inter' } }
      }
    }
  };

  // Doughnut Chart Data (Risk Breakdown)
  const riskCounts = stats?.risk_breakdown || { Low: 1, Moderate: 1, High: 1, Critical: 0 };
  const doughnutData = {
    labels: ['Low Risk', 'Moderate Risk', 'High Risk', 'Critical Risk'],
    datasets: [
      {
        data: [riskCounts.Low, riskCounts.Moderate, riskCounts.High, riskCounts.Critical],
        backgroundColor: [
          '#10b981', // green
          '#06b6d4', // cyan
          '#f59e0b', // amber
          '#f43f5e'  // rose
        ],
        borderColor: 'rgba(20, 15, 26, 0.8)',
        borderWidth: 3
      }
    ]
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { color: '#cbd5e1', padding: 16, font: { family: 'Inter', size: 12 } }
      }
    },
    cutout: '72%'
  };

  return (
    <div style={{ maxWidth: "1280px", margin: "0 auto", padding: "32px 20px" }}>
      {/* Hero Welcome Header */}
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: "20px",
        marginBottom: "32px"
      }}>
        <div>
          <div style={{ display: "inline-flex", alignItems: "center", gap: "8px", background: "rgba(226, 155, 179, 0.1)", border: "1px solid var(--border-subtle)", padding: "4px 12px", borderRadius: "9999px", fontSize: "0.8rem", color: "var(--primary)", marginBottom: "8px" }}>
            <Award size={14} /> System Administration & Maintenance (IT23/L Code: 3493)
          </div>
          <h1 style={{ fontSize: "2.1rem", fontWeight: 800, marginBottom: "6px" }}>
            Password Policy Security & Compliance Hub
          </h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "0.95rem", maxWidth: "700px" }}>
            Automated compliance engine evaluating length, character complexity, account lockout, expiration cycles, and reuse history against NIST SP 800-63B and OWASP benchmarks.
          </p>
        </div>

        <button 
          onClick={onStartEvaluation}
          className="btn-cyan-custom"
          style={{ padding: "12px 24px", fontSize: "1rem" }}
        >
          <Play size={18} /> Run New Evaluation
        </button>
      </div>

      {/* 4 Stat Cards */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))",
        gap: "20px",
        marginBottom: "32px"
      }}>
        {/* Card 1 */}
        <div className="sec-card" style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ width: "52px", height: "52px", borderRadius: "14px", background: "rgba(6, 182, 212, 0.15)", border: "1px solid rgba(6, 182, 212, 0.3)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--accent-cyan)" }}>
            <Activity size={26} />
          </div>
          <div>
            <div style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>Total Evaluations</div>
            <div style={{ fontSize: "1.9rem", fontWeight: 800, color: "var(--text-primary)" }}>{stats?.total_evaluations || 0}</div>
            <div style={{ fontSize: "0.75rem", color: "var(--color-pass)" }}>Recorded in audit trail</div>
          </div>
        </div>

        {/* Card 2 */}
        <div className="sec-card" style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ width: "52px", height: "52px", borderRadius: "14px", background: "rgba(226, 155, 179, 0.15)", border: "1px solid rgba(226, 155, 179, 0.3)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--primary)" }}>
            <ShieldCheck size={26} />
          </div>
          <div>
            <div style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>Average Compliance</div>
            <div style={{ fontSize: "1.9rem", fontWeight: 800, color: "var(--primary)" }}>{stats?.average_compliance_score || 0}%</div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)" }}>Composite score rating</div>
          </div>
        </div>

        {/* Card 3 */}
        <div className="sec-card" style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ width: "52px", height: "52px", borderRadius: "14px", background: "rgba(245, 158, 11, 0.15)", border: "1px solid rgba(245, 158, 11, 0.3)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--color-warning)" }}>
            <AlertTriangle size={26} />
          </div>
          <div>
            <div style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>Critical / High Risks</div>
            <div style={{ fontSize: "1.9rem", fontWeight: 800, color: "var(--color-warning)" }}>
              {(riskCounts.Critical || 0) + (riskCounts.High || 0)}
            </div>
            <div style={{ fontSize: "0.75rem", color: "var(--color-fail)" }}>Vulnerabilities flagged</div>
          </div>
        </div>

        {/* Card 4 */}
        <div className="sec-card" style={{ display: "flex", alignItems: "center", gap: "16px" }}>
          <div style={{ width: "52px", height: "52px", borderRadius: "14px", background: "rgba(16, 185, 129, 0.15)", border: "1px solid rgba(16, 185, 129, 0.3)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--color-pass)" }}>
            <Layers size={26} />
          </div>
          <div>
            <div style={{ fontSize: "0.8rem", fontWeight: 600, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.05em" }}>Security Standards</div>
            <div style={{ fontSize: "1.9rem", fontWeight: 800, color: "var(--text-primary)" }}>{stats?.standards_count || 4}</div>
            <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)" }}>NIST, OWASP, CIS, Custom</div>
          </div>
        </div>
      </div>

      {/* Charts Grid */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))",
        gap: "24px",
        marginBottom: "32px"
      }}>
        {/* Radar Chart: Dimension Compliance */}
        <div className="sec-card" style={{ display: "flex", flexDirection: "column" }}>
          <div style={{ marginBottom: "16px" }}>
            <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "4px" }}>
              Policy Dimension Compliance Breakdown
            </h3>
            <p style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>
              Evaluation performance across the 5 core checks & security hygiene
            </p>
          </div>
          <div style={{ height: "300px", position: "relative" }}>
            <Radar data={radarData} options={radarOptions} />
          </div>
        </div>

        {/* Doughnut Chart: Risk Level Distribution */}
        <div className="sec-card" style={{ display: "flex", flexDirection: "column" }}>
          <div style={{ marginBottom: "16px" }}>
            <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "4px" }}>
              Organizational Risk Distribution
            </h3>
            <p style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>
              Proportion of evaluated policies categorized by security risk level
            </p>
          </div>
          <div style={{ height: "300px", position: "relative" }}>
            <Doughnut data={doughnutData} options={doughnutOptions} />
          </div>
        </div>
      </div>

      {/* Recent Evaluations Table */}
      <div className="sec-card" style={{ marginBottom: "32px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "20px" }}>
          <div>
            <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "4px" }}>
              Recent Policy Evaluations
            </h3>
            <p style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>
              Saved compliance check history and executive scores
            </p>
          </div>
          <button 
            onClick={onStartEvaluation}
            className="btn-secondary-custom"
            style={{ padding: "6px 14px", fontSize: "0.8rem" }}
          >
            New Check
          </button>
        </div>

        {stats?.recent_evaluations?.length > 0 ? (
          <div style={{ overflowX: "auto" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left", fontSize: "0.88rem" }}>
              <thead>
                <tr style={{ borderBottom: "1px solid var(--border-subtle)", color: "var(--text-muted)", textTransform: "uppercase", fontSize: "0.75rem", letterSpacing: "0.05em" }}>
                  <th style={{ padding: "12px 16px" }}>Policy Name</th>
                  <th style={{ padding: "12px 16px" }}>Benchmark Standard</th>
                  <th style={{ padding: "12px 16px" }}>Score & Grade</th>
                  <th style={{ padding: "12px 16px" }}>Risk Level</th>
                  <th style={{ padding: "12px 16px" }}>Date</th>
                  <th style={{ padding: "12px 16px", textAlign: "right" }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_evaluations.map((r) => {
                  let badgeClass = "badge-pass";
                  if (r.risk_level === "Critical" || r.risk_level === "High") badgeClass = "badge-fail";
                  else if (r.risk_level === "Moderate") badgeClass = "badge-warning";

                  return (
                    <tr key={r.id} style={{ borderBottom: "1px solid rgba(255, 255, 255, 0.04)", transition: "background 0.2s ease" }}>
                      <td style={{ padding: "14px 16px", fontWeight: 600, color: "var(--text-primary)" }}>{r.policy_name}</td>
                      <td style={{ padding: "14px 16px", color: "var(--text-secondary)" }}>{r.standard_name}</td>
                      <td style={{ padding: "14px 16px" }}>
                        <span style={{ fontWeight: 700, color: r.overall_compliance_score >= 80 ? "var(--color-pass)" : r.overall_compliance_score >= 60 ? "var(--color-warning)" : "var(--color-fail)" }}>
                          {r.overall_compliance_score}%
                        </span>
                        <span style={{ marginLeft: "6px", fontSize: "0.75rem", background: "rgba(255,255,255,0.08)", padding: "2px 6px", borderRadius: "4px" }}>
                          {r.grade_letter}
                        </span>
                      </td>
                      <td style={{ padding: "14px 16px" }}>
                        <span className={badgeClass}>{r.risk_level}</span>
                      </td>
                      <td style={{ padding: "14px 16px", color: "var(--text-muted)", fontSize: "0.8rem" }}>
                        {new Date(r.evaluated_at).toLocaleDateString()}
                      </td>
                      <td style={{ padding: "14px 16px", textAlign: "right" }}>
                        <button
                          onClick={() => onViewReport(r.id)}
                          className="btn-secondary-custom"
                          style={{ padding: "6px 12px", fontSize: "0.8rem" }}
                        >
                          <Eye size={14} /> View
                        </button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <div style={{ textAlign: "center", padding: "40px", color: "var(--text-muted)" }}>
            No evaluation reports yet. Click "Run New Evaluation" above!
          </div>
        )}
      </div>

      {/* Official Proposal System Flow Banner Card */}
      <div className="sec-card" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "20px", background: "linear-gradient(135deg, rgba(226, 155, 179, 0.08) 0%, rgba(6, 182, 212, 0.08) 100%)" }}>
        <div style={{ maxWidth: "600px" }}>
          <div style={{ fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--accent-cyan)", fontWeight: 700, marginBottom: "6px" }}>
            Proposal Architecture Flow
          </div>
          <h3 style={{ fontSize: "1.25rem", fontWeight: 700, marginBottom: "8px" }}>
            Login → Enter Policy → Check Rules → Score Findings → Show Report
          </h3>
          <p style={{ color: "var(--text-secondary)", fontSize: "0.88rem", marginBottom: "16px" }}>
            Built specifically as Project #23 for System Administration & Maintenance (IT23/L). Complete with Role-Based Access Control, audit trail retention, and instant export capabilities.
          </p>
          <div style={{ display: "flex", gap: "10px" }}>
            <button onClick={onStartEvaluation} className="btn-primary-custom" style={{ padding: "8px 16px", fontSize: "0.85rem" }}>
              <Play size={15} /> Evaluate Policy
            </button>
          </div>
        </div>

        <div style={{ textAlign: "center" }}>
          <img 
            src="/images/logo.png" 
            alt="Official Logo" 
            style={{ width: "90px", height: "90px", borderRadius: "18px", border: "2px solid var(--border-card)", boxShadow: "0 6px 24px var(--primary-glow)" }} 
          />
          <div style={{ fontSize: "0.72rem", color: "var(--text-muted)", marginTop: "6px" }}>KRISTINE PAULA S. CORETICO</div>
        </div>
      </div>
    </div>
  );
}
