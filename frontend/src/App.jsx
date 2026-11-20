import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Login from './components/Login';
import PasswordChange from './components/PasswordChange';
import Dashboard from './components/Dashboard';
import PolicyEvaluator from './components/PolicyEvaluator';
import EvaluationReportView from './components/EvaluationReportView';
import PolicyCompare from './components/PolicyCompare';
import EvaluationHistory from './components/EvaluationHistory';
import StandardsManager from './components/StandardsManager';
import UserManagement from './components/UserManagement';
import AuditLogsView from './components/AuditLogsView';
import { api } from './api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [checkingSession, setCheckingSession] = useState(true);
  const [selectedReport, setSelectedReport] = useState(null);
  const [showChangePassword, setShowChangePassword] = useState(false);

  useEffect(() => {
    if (localStorage.getItem('token')) {
      api.getMe()
        .then(setUser)
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setCheckingSession(false));
    } else {
      setCheckingSession(false);
    }
  }, []);

  function handleLogin(data) {
    localStorage.setItem('token', data.access_token);
    setUser(data.user);
    setShowChangePassword(false);
  }

  function handleLogout() {
    api.logout().catch(() => {});
    localStorage.removeItem('token');
    setUser(null);
    setActiveTab('dashboard');
    setShowChangePassword(false);
  }

  async function handleViewReport(id) {
    try {
      const report = await api.getReport(id);
      setSelectedReport(report);
      setActiveTab('report');
    } catch (err) {
      alert(`Could not load report: ${err.message}`);
    }
  }

  function renderContent() {
    if (checkingSession) {
      return <main style={{ padding: 32 }}>Checking session...</main>;
    }
    if (!user) {
      return <Login onLogin={handleLogin} />;
    }
    if (user.must_change_password || showChangePassword) {
      return (
        <PasswordChange
          required={user.must_change_password}
          onChanged={handleLogout}
        />
      );
    }

    return (
      <main className="app-main">
        {activeTab === 'dashboard' && (
          <Dashboard
            user={user}
            onStartEvaluation={() => setActiveTab('evaluate')}
            onViewReport={handleViewReport}
            onNavigate={setActiveTab}
          />
        )}
        {activeTab === 'evaluate' && (
          <PolicyEvaluator
            user={user}
            onEvaluationComplete={(report) => {
              setSelectedReport(report);
              setActiveTab('report');
            }}
          />
        )}
        {activeTab === 'report' && (
          <EvaluationReportView
            report={selectedReport}
            onBack={() => setActiveTab('history')}
            onCompare={() => setActiveTab('compare')}
          />
        )}
        {activeTab === 'compare' && <PolicyCompare onViewReport={handleViewReport} />}
        {activeTab === 'history' && <EvaluationHistory onViewReport={handleViewReport} />}
        {activeTab === 'standards' && <StandardsManager user={user} />}
        {activeTab === 'audit' && (user.role === 'Administrator' || user.role === 'Auditor' || user.role === 'Viewer') && <AuditLogsView />}
        {activeTab === 'users' && user.role === 'Administrator' && <UserManagement />}
      </main>
    );
  }

  return (
    <div className={user ? 'app-shell' : 'public-shell'}>
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onLogout={handleLogout}
        onChangePassword={() => setShowChangePassword(true)}
      />
      <div className={user ? 'app-content' : 'public-content'}>
        {renderContent()}
      </div>
    </div>
  );
}
