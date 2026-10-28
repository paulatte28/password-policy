import React from 'react';
import { Award, Shield, FileCheck, Layers, Play } from 'lucide-react';

export default function AboutProposal({ onStartEvaluation }) {
  return (
    <div style={{ maxWidth: "1150px", margin: "0 auto", padding: "32px 20px" }}>
      {/* Title */}
      <div style={{ marginBottom: "28px" }}>
        <h1 style={{ fontSize: "2.1rem", fontWeight: 800, marginBottom: "4px" }}>
          Project Proposal & Architecture Specifications
        </h1>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.92rem" }}>
          System Administration and Maintenance – IT23/L (Code: 3493 • 7:30–9:30PM)
        </p>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "24px", marginBottom: "32px" }}>
        {/* Metadata Card */}
        <div className="sec-card text-center" style={{ display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center" }}>
          <img 
            src="/images/logo.png" 
            alt="Official Proposal Logo" 
            style={{ width: "96px", height: "96px", borderRadius: "20px", border: "2px solid var(--border-card)", boxShadow: "0 8px 24px var(--primary-glow)", marginBottom: "16px" }} 
          />
          <h3 style={{ fontSize: "1.25rem", fontWeight: 800, color: "var(--primary)", marginBottom: "4px" }}>
            KRISTINE PAULA S. CORETICO
          </h3>
          <div style={{ fontSize: "0.82rem", color: "var(--text-muted)", marginBottom: "20px" }}>
            Author & Systems Administration Student
          </div>

          <table style={{ width: "100%", textAlign: "left", fontSize: "0.85rem", borderCollapse: "collapse" }}>
            <tbody>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)" }}>
                <td style={{ padding: "8px 0", color: "var(--text-muted)" }}>Project #</td>
                <td style={{ padding: "8px 0", fontWeight: 700, color: "var(--text-primary)" }}>#23 PasswordPolicy Checker</td>
              </tr>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)" }}>
                <td style={{ padding: "8px 0", color: "var(--text-muted)" }}>Subject</td>
                <td style={{ padding: "8px 0", color: "var(--text-primary)" }}>System Administration and Maintenance</td>
              </tr>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)" }}>
                <td style={{ padding: "8px 0", color: "var(--text-muted)" }}>Subject Code</td>
                <td style={{ padding: "8px 0", color: "var(--accent-cyan)", fontWeight: 700 }}>3493 (7:30–9:30PM)</td>
              </tr>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)" }}>
                <td style={{ padding: "8px 0", color: "var(--text-muted)" }}>Institution</td>
                <td style={{ padding: "8px 0", color: "var(--text-primary)" }}>Systems Administration and Security Unit</td>
              </tr>
              <tr>
                <td style={{ padding: "8px 0", color: "var(--text-muted)" }}>Date Submitted</td>
                <td style={{ padding: "8px 0", color: "var(--text-primary)" }}>October 26, 2026</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Technologies Stack Specified in Proposal */}
        <div className="sec-card">
          <h3 style={{ fontSize: "1.2rem", fontWeight: 700, marginBottom: "16px", color: "var(--accent-cyan)", display: "flex", alignItems: "center", gap: "8px" }}>
            <Layers size={20} /> Official Proposal Stack
          </h3>

          <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
            <div style={{ background: "rgba(15, 10, 20, 0.5)", padding: "12px 16px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-subtle)" }}>
              <div style={{ fontWeight: 700, fontSize: "0.85rem", color: "var(--primary)", marginBottom: "4px" }}>
                Backend & API Architecture
              </div>
              <ul style={{ paddingLeft: "18px", fontSize: "0.82rem", color: "var(--text-secondary)", lineHeight: 1.6 }}>
                <li><strong>Programming Language:</strong> Python (v3.14)</li>
                <li><strong>Framework:</strong> FastAPI</li>
                <li><strong>ORM:</strong> SQLAlchemy (with auto-migrating declarative models)</li>
                <li><strong>Authentication:</strong> JWT tokens with Passlib/Bcrypt password hashing</li>
              </ul>
            </div>

            <div style={{ background: "rgba(15, 10, 20, 0.5)", padding: "12px 16px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-subtle)" }}>
              <div style={{ fontWeight: 700, fontSize: "0.85rem", color: "var(--color-pass)", marginBottom: "4px" }}>
                Frontend & Visuals Architecture
              </div>
              <ul style={{ paddingLeft: "18px", fontSize: "0.82rem", color: "var(--text-secondary)", lineHeight: 1.6 }}>
                <li><strong>Library:</strong> React (v18+) with Vite build tool</li>
                <li><strong>Charts:</strong> Chart.js (Radar dimension scores & risk doughnuts)</li>
                <li><strong>Design System:</strong> Custom dark glassmorphism with plum/rose-gold accent</li>
                <li><strong>Exporting:</strong> Native PDF print engine and CSV generation</li>
              </ul>
            </div>

            <div style={{ background: "rgba(15, 10, 20, 0.5)", padding: "12px 16px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-subtle)" }}>
              <div style={{ fontWeight: 700, fontSize: "0.85rem", color: "var(--accent-cyan)", marginBottom: "4px" }}>
                Database Layer
              </div>
              <ul style={{ paddingLeft: "18px", fontSize: "0.82rem", color: "var(--text-secondary)", lineHeight: 1.6 }}>
                <li><strong>Primary:</strong> Supabase PostgreSQL (configured via DATABASE_URL)</li>
                <li><strong>Local Engine:</strong> Zero-configuration SQLite fallback for immediate testing</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Official System Flow Diagram */}
      <div className="sec-card" style={{ marginBottom: "32px", textAlign: "center" }}>
        <h3 style={{ fontSize: "1.3rem", fontWeight: 700, marginBottom: "8px" }}>
          Official Proposal System Flow
        </h3>
        <p style={{ color: "var(--text-secondary)", fontSize: "0.88rem", marginBottom: "20px" }}>
          The diagram below illustrates the exact architectural process submitted in the official proposal:
        </p>

        <div style={{ background: "#ffffff", padding: "24px", borderRadius: "var(--radius-md)", display: "inline-block", maxWidth: "100%", boxShadow: "0 8px 30px rgba(0,0,0,0.5)" }}>
          <img 
            src="/images/system-flow.png" 
            alt="Official Proposal System Flow Diagram" 
            style={{ maxWidth: "100%", maxHeight: "650px", objectFit: "contain" }} 
          />
        </div>
      </div>

      {/* Objectives and Description */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "24px" }}>
        <div className="sec-card">
          <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "14px", color: "var(--color-warning)" }}>
            Project Objectives
          </h3>
          <ul style={{ paddingLeft: "20px", fontSize: "0.88rem", color: "var(--text-secondary)", display: "flex", flexDirection: "column", gap: "10px", lineHeight: 1.5 }}>
            <li>To develop a web-based system that evaluates password policy settings and reports compliance for length, complexity, lockout, and expiration.</li>
            <li>To identify weak-password risks, password reuse policy gaps, and insecure configurations, and provide recommendations with a compliance score.</li>
            <li>To implement role-based access control, audit logging, and report exports while never requesting or storing the actual passwords of users.</li>
          </ul>
        </div>

        <div className="sec-card">
          <h3 style={{ fontSize: "1.15rem", fontWeight: 700, marginBottom: "14px", color: "var(--accent-cyan)" }}>
            Zero-Password Storage Guarantee (Proposal #64)
          </h3>
          <p style={{ fontSize: "0.88rem", color: "var(--text-secondary)", lineHeight: 1.6, marginBottom: "16px" }}>
            PasswordPolicy Checker evaluates administrative password policy settings only (minimum length, character complexity requirements, lockout thresholds, rotation frequency, and history retention). It never requests, transmits, or stores actual user passwords.
          </p>
          <div style={{ background: "rgba(6, 182, 212, 0.08)", border: "1px solid rgba(6, 182, 212, 0.25)", padding: "12px 16px", borderRadius: "var(--radius-sm)", fontSize: "0.82rem", color: "var(--accent-cyan)" }}>
            ✓ Complies with academic safety standards and zero-knowledge privacy requirements.
          </div>
        </div>
      </div>
    </div>
  );
}
