import React, { useState } from 'react';
import { api } from '../api';
import { 
  ShieldCheck, AlertTriangle, AlertOctagon, CheckCircle2, 
  Printer, Download, ArrowLeft, GitCompare, Share2, Award, Calendar, User
} from 'lucide-react';

export default function EvaluationReportView({ report, onBack, onCompare }) {
  const [filter, setFilter] = useState('ALL'); // ALL, FAIL, WARNING, PASS

  if (!report) return null;

  const findings = report.findings || [];
  const filteredFindings = findings.filter(f => {
    if (filter === 'ALL') return true;
    return f.status === filter;
  });

  const scores = report.scores_breakdown || {
    length_score: 80,
    complexity_score: 80,
    lockout_score: 80,
    expiration_score: 80,
    reuse_score: 80,
    hygiene_score: 80
  };

  // Color mappings
  let scoreColor = "var(--color-pass)";
  if (report.overall_compliance_score < 60) scoreColor = "var(--color-fail)";
  else if (report.overall_compliance_score < 80) scoreColor = "var(--color-warning)";

  let riskBadgeClass = "badge-pass";
  if (report.risk_level === "Critical" || report.risk_level === "High") riskBadgeClass = "badge-fail";
  else if (report.risk_level === "Moderate") riskBadgeClass = "badge-warning";

  return (
    <div style={{ maxWidth: "1150px", margin: "0 auto", padding: "32px 20px" }}>
      {/* Top Action Bar */}
      <div className="no-print" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "12px", marginBottom: "24px" }}>
        <button 
          onClick={onBack}
          className="btn-secondary-custom"
          style={{ padding: "8px 16px", fontSize: "0.85rem" }}
        >
          <ArrowLeft size={16} /> Back to Policies
        </button>

        <div style={{ display: "flex", gap: "10px" }}>
          {report.id && (
            <a 
              href={api.getExportCsvUrl(report.id)} 
              download
              className="btn-secondary-custom" 
              style={{ padding: "8px 16px", fontSize: "0.85rem", textDecoration: "none" }}
            >
              <Download size={16} /> Export CSV
            </a>
          )}
          <button 
            onClick={() => window.print()}
            className="btn-cyan-custom"
            style={{ padding: "8px 18px", fontSize: "0.85rem" }}
          >
            <Printer size={16} /> Print / Save PDF
          </button>
        </div>
      </div>

      {/* Main Executive Summary Card */}
      <div className="sec-card" style={{ marginBottom: "28px", position: "relative", overflow: "hidden" }}>
        {/* Subtle background glow */}
        <div style={{
          position: "absolute",
          top: "-60px",
          right: "-60px",
          width: "250px",
          height: "250px",
          borderRadius: "50%",
          background: scoreColor,
          opacity: 0.12,
          filter: "blur(60px)",
          pointerEvents: "none"
        }} />

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "24px", marginBottom: "24px" }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "6px" }}>
              <span className={riskBadgeClass}>{report.risk_level} Risk</span>
              <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>Benchmark: {report.standard_name}</span>
            </div>
            <h1 style={{ fontSize: "2.1rem", fontWeight: 800, marginBottom: "8px" }}>
              {report.policy_name}
            </h1>
            <div style={{ display: "flex", alignItems: "center", gap: "16px", color: "var(--text-muted)", fontSize: "0.82rem" }}>
              <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                <Calendar size={14} /> {new Date(report.evaluated_at || Date.now()).toLocaleString()}
              </span>
              <span style={{ display: "flex", alignItems: "center", gap: "4px" }}>
                <User size={14} /> Evaluated by: {report.evaluated_by_user || report.evaluated_by || "Security Analyst"}
              </span>
            </div>
          </div>

          {/* Big Score Box */}
          <div style={{
            background: "rgba(20, 15, 26, 0.8)",
            border: `2px solid ${scoreColor}`,
            borderRadius: "var(--radius-lg)",
            padding: "20px 32px",
            textAlign: "center",
            boxShadow: `0 8px 30px ${scoreColor}33`,
            minWidth: "180px"
          }}>
            <div style={{ fontSize: "0.75rem", textTransform: "uppercase", letterSpacing: "0.08em", color: "var(--text-muted)", fontWeight: 700 }}>
              Compliance Rating
            </div>
            <div style={{ fontSize: "3.2rem", fontWeight: 900, color: scoreColor, lineHeight: 1.1 }}>
              {report.overall_compliance_score}%
            </div>
            <div style={{ display: "inline-block", marginTop: "6px", background: "rgba(255, 255, 255, 0.1)", padding: "2px 10px", borderRadius: "9999px", fontSize: "0.85rem", fontWeight: 800 }}>
              Grade {report.grade_letter}
            </div>
          </div>
        </div>

        {/* Executive Summary Narrative */}
        <div style={{
          background: "rgba(255, 255, 255, 0.03)",
          borderLeft: `4px solid ${scoreColor}`,
          padding: "16px 20px",
          borderRadius: "0 var(--radius-sm) var(--radius-sm) 0",
          fontSize: "0.92rem",
          color: "var(--text-secondary)",
          lineHeight: 1.6,
          marginBottom: "24px"
        }}>
          <strong>Executive Assessment:</strong> {report.executive_summary}
        </div>

        {/* 6 Dimension Progress Bars */}
        <div>
          <h4 style={{ fontSize: "0.9rem", textTransform: "uppercase", letterSpacing: "0.06em", color: "var(--text-muted)", marginBottom: "14px" }}>
            Dimension Breakdown Scores
          </h4>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "14px" }}>
            {[
              { label: "1. Length", score: scores.length_score, weight: "30%" },
              { label: "2. Complexity", score: scores.complexity_score, weight: "15%" },
              { label: "3. Lockout", score: scores.lockout_score, weight: "25%" },
              { label: "4. Expiration", score: scores.expiration_score, weight: "10%" },
              { label: "5. Reuse / History", score: scores.reuse_score, weight: "10%" },
              { label: "6. Hygiene", score: scores.hygiene_score, weight: "10%" },
            ].map((dim, idx) => {
              let barColor = "var(--color-pass)";
              if (dim.score < 60) barColor = "var(--color-fail)";
              else if (dim.score < 80) barColor = "var(--color-warning)";

              return (
                <div key={idx} style={{ background: "rgba(15, 10, 20, 0.5)", padding: "10px 14px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-subtle)" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.78rem", fontWeight: 600, marginBottom: "6px" }}>
                    <span>{dim.label}</span>
                    <span style={{ color: barColor }}>{dim.score}%</span>
                  </div>
                  <div style={{ width: "100%", height: "6px", background: "rgba(255, 255, 255, 0.08)", borderRadius: "3px", overflow: "hidden" }}>
                    <div style={{ width: `${dim.score}%`, height: "100%", background: barColor, borderRadius: "3px" }} />
                  </div>
                  <div style={{ fontSize: "0.68rem", color: "var(--text-muted)", marginTop: "4px" }}>Weight: {dim.weight}</div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Findings Section Header & Filter Tabs */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "14px", marginBottom: "20px" }}>
        <div>
          <h2 style={{ fontSize: "1.4rem", fontWeight: 800 }}>Audit Findings & Recommendations</h2>
          <p style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>
            Detailed breakdown of rule compliance, detected security risks, and suggested fixes.
          </p>
        </div>

        {/* Filter Pills */}
        <div style={{ display: "flex", gap: "6px" }}>
          <button 
            onClick={() => setFilter('ALL')}
            className={`btn-secondary-custom ${filter === 'ALL' ? 'active-tab' : ''}`}
            style={{ padding: "6px 14px", fontSize: "0.8rem", borderColor: filter === 'ALL' ? 'var(--accent-cyan)' : 'transparent' }}
          >
            All ({findings.length})
          </button>
          <button 
            onClick={() => setFilter('FAIL')}
            className={`btn-secondary-custom`}
            style={{ padding: "6px 14px", fontSize: "0.8rem", color: "var(--color-fail)", borderColor: filter === 'FAIL' ? 'var(--color-fail)' : 'transparent' }}
          >
            Fails ({report.failed_count || findings.filter(f => f.status === 'FAIL').length})
          </button>
          <button 
            onClick={() => setFilter('WARNING')}
            className={`btn-secondary-custom`}
            style={{ padding: "6px 14px", fontSize: "0.8rem", color: "var(--color-warning)", borderColor: filter === 'WARNING' ? 'var(--color-warning)' : 'transparent' }}
          >
            Warnings ({report.warning_count || findings.filter(f => f.status === 'WARNING').length})
          </button>
          <button 
            onClick={() => setFilter('PASS')}
            className={`btn-secondary-custom`}
            style={{ padding: "6px 14px", fontSize: "0.8rem", color: "var(--color-pass)", borderColor: filter === 'PASS' ? 'var(--color-pass)' : 'transparent' }}
          >
            Pass ({report.passed_count || findings.filter(f => f.status === 'PASS').length})
          </button>
        </div>
      </div>

      {/* Findings Cards List */}
      <div style={{ display: "flex", flexDirection: "column", gap: "16px", marginBottom: "40px" }}>
        {filteredFindings.map((f, i) => {
          let statusBadge = <span className="badge-pass"><CheckCircle2 size={12} /> PASS</span>;
          let borderAccent = "rgba(16, 185, 129, 0.3)";
          if (f.status === 'FAIL') {
            statusBadge = <span className="badge-fail"><AlertOctagon size={12} /> FAIL ({f.severity})</span>;
            borderAccent = "rgba(244, 63, 94, 0.4)";
          } else if (f.status === 'WARNING') {
            statusBadge = <span className="badge-warning"><AlertTriangle size={12} /> WARNING ({f.severity})</span>;
            borderAccent = "rgba(245, 158, 11, 0.4)";
          }

          return (
            <div 
              key={i} 
              className="sec-card" 
              style={{ borderLeft: `5px solid ${borderAccent}`, padding: "20px 24px" }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px", marginBottom: "10px" }}>
                <div>
                  <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" }}>
                    <span style={{ fontSize: "0.72rem", background: "rgba(255,255,255,0.06)", padding: "2px 8px", borderRadius: "4px", color: "var(--text-muted)", fontWeight: 600 }}>
                      {f.rule_category}
                    </span>
                    {statusBadge}
                  </div>
                  <h3 style={{ fontSize: "1.1rem", fontWeight: 700, color: "var(--text-primary)" }}>
                    {f.title}
                  </h3>
                </div>
              </div>

              {/* Setting vs Requirement Comparison Grid */}
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "14px", background: "rgba(15, 10, 20, 0.4)", padding: "12px 16px", borderRadius: "var(--radius-sm)", marginBottom: "12px", border: "1px solid var(--border-subtle)" }}>
                <div>
                  <div style={{ fontSize: "0.72rem", textTransform: "uppercase", color: "var(--text-muted)", fontWeight: 700 }}>
                    Current Configuration
                  </div>
                  <div style={{ fontSize: "0.88rem", fontWeight: 600, color: "var(--text-secondary)", marginTop: "2px" }}>
                    {f.current_value}
                  </div>
                </div>

                <div>
                  <div style={{ fontSize: "0.72rem", textTransform: "uppercase", color: "var(--text-muted)", fontWeight: 700 }}>
                    Standard Benchmark Requirement
                  </div>
                  <div style={{ fontSize: "0.88rem", fontWeight: 600, color: "var(--accent-cyan)", marginTop: "2px" }}>
                    {f.standard_requirement}
                  </div>
                </div>
              </div>

              {/* Risk Description */}
              <div style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginBottom: "8px" }}>
                <strong style={{ color: "var(--text-muted)" }}>Security Risk:</strong> {f.risk_description}
              </div>

              {/* Actionable Remediation */}
              <div style={{ fontSize: "0.85rem", color: "var(--accent-cyan)", background: "rgba(6, 182, 212, 0.08)", padding: "8px 12px", borderRadius: "var(--radius-sm)", border: "1px solid rgba(6, 182, 212, 0.2)" }}>
                <strong style={{ color: "var(--text-primary)" }}>Remediation:</strong> {f.recommendation}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
