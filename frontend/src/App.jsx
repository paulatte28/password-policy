import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import PolicyEvaluator from './components/PolicyEvaluator';
import EvaluationReportView from './components/EvaluationReportView';
import PolicyCompare from './components/PolicyCompare';
import EvaluationHistory from './components/EvaluationHistory';
import StandardsManager from './components/StandardsManager';
import AuditLogsView from './components/AuditLogsView';
import UserManagement from './components/UserManagement';
import { api } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [currentReport, setCurrentReport] = useState(null);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  // Initial user check or auto-login with default admin for ease of demo
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.getMe()
        .then(u => setUser(u))
        .catch(() => {
          localStorage.removeItem('token');
          // Auto login as default admin for seamless evaluation
          quickLogin('admin@passwordpolicy.local', 'Admin@123456');
        });
    } else {
      // Auto login as Admin on first load so user immediately has full capability
      quickLogin('admin@passwordpolicy.local', 'Admin@123456');
    }
  }, []);

  async function quickLogin(email, password) {
    try {
      setLoginError('');
      const res = await api.login(email, password);
      localStorage.setItem('token', res.access_token);
      setUser(res.user);
      setShowLoginModal(false);
    } catch (err) {
      setLoginError(err.message);
    }
  }

  function handleLogout() {
    localStorage.removeItem('token');
    setUser(null);
    setActiveTab('dashboard');
  }

  function handleEvaluationComplete(report) {
    setCurrentReport(report);
    setActiveTab('report');
  }

  async function handleViewReport(reportId) {
    try {
      const rep = await api.getReport(reportId);
      setCurrentReport(rep);
      setActiveTab('report');
    } catch (err) {
      alert(`Could not load report: ${err.message}`);
    }
  }

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        user={user}
        onLogout={handleLogout}
        onQuickLogin={quickLogin}
      />

      <main style={{ flex: 1 }}>
        {activeTab === 'dashboard' && (
          <Dashboard 
            onStartEvaluation={() => setActiveTab('evaluate')}
            onViewReport={handleViewReport}
          />
        )}

        {activeTab === 'evaluate' && (
          <PolicyEvaluator 
            onEvaluationComplete={handleEvaluationComplete}
          />
        )}

        {activeTab === 'report' && (
          <EvaluationReportView 
            report={currentReport}
            onBack={() => setActiveTab('history')}
            onCompare={() => setActiveTab('compare')}
          />
        )}

        {activeTab === 'compare' && (
          <PolicyCompare 
            onViewReport={handleViewReport}
          />
        )}

        {activeTab === 'history' && (
          <EvaluationHistory 
            onViewReport={handleViewReport}
          />
        )}

        {activeTab === 'standards' && (
          <StandardsManager 
            user={user}
          />
        )}

        {activeTab === 'audit' && (
          <AuditLogsView />
        )}

        {activeTab === 'users' && user?.role === 'Administrator' && (
          <UserManagement />
        )}
      </main>

      {/* Footer */}
      <footer className="no-print" style={{
        background: "rgba(15, 10, 20, 0.95)",
        borderTop: "1px solid var(--border-subtle)",
        padding: "20px 24px",
        textAlign: "center",
        fontSize: "0.82rem",
        color: "var(--text-muted)",
        marginTop: "auto"
      }}>
        <div style={{ maxWidth: "1200px", margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "10px" }}>
          <div>
            <strong style={{ color: "var(--primary)" }}>#23 PasswordPolicy Checker</strong> — System Administration & Maintenance (IT23/L Code: 3493)
          </div>
          <div>
            Author: <span style={{ color: "var(--text-primary)", fontWeight: 600 }}>Kristine Paula S. Coretico</span> • Systems Administration and Security Unit
          </div>
        </div>
      </footer>
    </div>
  );
}
