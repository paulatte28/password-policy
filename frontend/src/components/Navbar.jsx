import React from 'react';
import { Shield, Play, BarChart2, GitCompare, History, Scale, FileText, Users, LogOut, UserCheck } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, user, onLogout, onQuickLogin }) {
  return (
    <header className="sticky top-0 z-50">
      {/* Zero Password Security Guarantee Banner */}
      <div className="security-banner">
        <Shield size={15} style={{ color: "var(--accent-cyan)" }} />
        <span>
          <strong>Zero-Knowledge Guarantee:</strong> This system evaluates administrative policy rules only. It never requests, transmits, or stores actual user passwords.
        </span>
      </div>

      {/* Main Navigation Bar */}
      <nav style={{
        background: "rgba(20, 15, 26, 0.95)",
        backdropFilter: "blur(16px)",
        borderBottom: "1px solid var(--border-subtle)",
        padding: "12px 24px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: "16px"
      }}>
        {/* Brand */}
        <div 
          onClick={() => setActiveTab('dashboard')}
          style={{ display: "flex", alignItems: "center", gap: "12px", cursor: "pointer" }}
        >
          <img 
            src="/images/logo.png" 
            alt="PasswordPolicy Checker Logo" 
            style={{ width: "42px", height: "42px", borderRadius: "10px", border: "1px solid var(--border-card)", objectFit: "cover", boxShadow: "0 4px 12px var(--primary-glow)" }} 
          />
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "4px" }}>
              <span style={{ fontSize: "1.2rem", fontWeight: 800, letterSpacing: "-0.03em", color: "var(--text-primary)" }}>PasswordPolicy</span>
              <span style={{ fontSize: "1.2rem", fontWeight: 800, letterSpacing: "-0.03em", color: "var(--primary)" }}>Checker</span>
            </div>
            <div style={{ fontSize: "0.68rem", fontWeight: 600, color: "var(--text-muted)", letterSpacing: "0.06em", textTransform: "uppercase" }}>
              IT23 Security Suite • #23
            </div>
          </div>
        </div>

        {/* Nav Links */}
        <div style={{ display: "flex", alignItems: "center", gap: "6px", flexWrap: "wrap" }}>
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`btn-secondary-custom ${activeTab === 'dashboard' ? 'active-tab' : ''}`}
            style={{ padding: "8px 14px", fontSize: "0.85rem", borderColor: activeTab === 'dashboard' ? 'var(--accent-cyan)' : 'transparent' }}
          >
            <BarChart2 size={16} /> Dashboard
          </button>

          <button
            onClick={() => setActiveTab('evaluate')}
            className={`btn-cyan-custom`}
            style={{ padding: "8px 16px", fontSize: "0.85rem" }}
          >
            <Play size={16} /> Evaluate Policy
          </button>

          <button
            onClick={() => setActiveTab('compare')}
            className={`btn-secondary-custom`}
            style={{ padding: "8px 14px", fontSize: "0.85rem", borderColor: activeTab === 'compare' ? 'var(--accent-cyan)' : 'transparent' }}
          >
            <GitCompare size={16} /> Compare
          </button>

          <button
            onClick={() => setActiveTab('history')}
            className={`btn-secondary-custom`}
            style={{ padding: "8px 14px", fontSize: "0.85rem", borderColor: activeTab === 'history' ? 'var(--accent-cyan)' : 'transparent' }}
          >
            <History size={16} /> History
          </button>

          <button
            onClick={() => setActiveTab('standards')}
            className={`btn-secondary-custom`}
            style={{ padding: "8px 14px", fontSize: "0.85rem", borderColor: activeTab === 'standards' ? 'var(--accent-cyan)' : 'transparent' }}
          >
            <Scale size={16} /> Standards
          </button>

          <button
            onClick={() => setActiveTab('audit')}
            className={`btn-secondary-custom`}
            style={{ padding: "8px 14px", fontSize: "0.85rem", borderColor: activeTab === 'audit' ? 'var(--accent-cyan)' : 'transparent' }}
          >
            <FileText size={16} /> Audit Logs
          </button>

          {user?.role === 'Administrator' && (
            <button
              onClick={() => setActiveTab('users')}
              className={`btn-secondary-custom`}
              style={{ padding: "8px 14px", fontSize: "0.85rem", borderColor: activeTab === 'users' ? 'var(--accent-cyan)' : 'transparent' }}
            >
              <Users size={16} /> Users
            </button>
          )}
        </div>

        {/* User Info & Switcher */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          {user ? (
            <div style={{ display: "flex", alignItems: "center", gap: "10px", background: "rgba(255,255,255,0.04)", padding: "6px 14px", borderRadius: "var(--radius-md)", border: "1px solid var(--border-subtle)" }}>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: "0.82rem", fontWeight: 700, color: "var(--text-primary)" }}>{user.full_name}</div>
                <div style={{ fontSize: "0.7rem", color: "var(--primary)", fontWeight: 600 }}>{user.role}</div>
              </div>
              <button 
                onClick={onLogout}
                title="Log out"
                style={{ background: "transparent", border: "none", color: "var(--text-muted)", cursor: "pointer", padding: "4px" }}
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div style={{ display: "flex", gap: "6px" }}>
              <button 
                onClick={() => onQuickLogin('admin@passwordpolicy.local', 'Admin@123456')}
                className="btn-secondary-custom" 
                style={{ padding: "6px 12px", fontSize: "0.8rem", color: "var(--primary)" }}
              >
                <UserCheck size={14} /> Admin
              </button>
              <button 
                onClick={() => onQuickLogin('analyst@passwordpolicy.local', 'Analyst@123456')}
                className="btn-secondary-custom" 
                style={{ padding: "6px 12px", fontSize: "0.8rem", color: "var(--accent-cyan)" }}
              >
                Analyst
              </button>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
}
