import React from 'react';
import {
  LayoutDashboard,
  ClipboardList,
  History,
  GitCompare,
  BookOpen,
  Users,
  ScrollText,
  KeyRound,
  LogOut,
} from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, user, onLogout, onChangePassword }) {
  const brand = (
    <div className="app-brand">
      <span className="brand-mark">
        <img src="/images/logo.png" alt="" />
      </span>
      <span className="app-brand-copy">
        <strong>Password Policy</strong>
        <small>Administration workspace</small>
      </span>
    </div>
  );

  if (!user) {
    return null;
  }

  const isReadOnly = user.role === 'Auditor' || user.role === 'Viewer';
  const workspaceItems = [
    ['dashboard', 'Overview', LayoutDashboard],
    ...(isReadOnly ? [] : [['evaluate', 'Policy editor', ClipboardList]]),
    ['history', 'Reports', History],
    ['compare', 'Compare reports', GitCompare],
  ];

  const adminItems = [
    ['standards', 'Benchmarks', BookOpen],
    ...(user.role === 'Administrator' ? [['users', 'Users', Users]] : []),
    ...((user.role === 'Administrator' || isReadOnly) ? [['audit', 'Activity log', ScrollText]] : []),
  ];

  function renderNavItems(items) {
    return items.map(([id, label, Icon]) => {
      const isActive = activeTab === id || (activeTab === 'report' && id === 'history');
      return (
        <button
          key={id}
          type="button"
          className={`sidebar-link${isActive ? ' is-active' : ''}`}
          onClick={() => setActiveTab(id)}
          aria-current={isActive ? 'page' : undefined}
          disabled={user.must_change_password}
        >
          <Icon size={18} strokeWidth={1.8} />
          <span>{label}</span>
        </button>
      );
    });
  }

  return (
    <aside className="app-sidebar no-print">
      {brand}
      <nav className="sidebar-nav" aria-label="Main navigation">
        <div className="sidebar-group">
          <span className="sidebar-label">Workspace</span>
          {renderNavItems(workspaceItems)}
        </div>
        <div className="sidebar-group">
          <span className="sidebar-label">Administration</span>
          {renderNavItems(adminItems)}
        </div>
      </nav>
      <div className="sidebar-account">
        <div className="account-avatar" aria-hidden="true">
          {user.full_name?.[0]?.toUpperCase() || 'U'}
        </div>
        <div className="account-details">
          <strong>{user.full_name}</strong>
          <small>{user.role}</small>
        </div>
        <div className="account-actions">
          <button
            type="button"
            onClick={onChangePassword}
            title="Change password"
            aria-label="Change password"
          >
            <KeyRound size={18} />
          </button>
          <button
            type="button"
            onClick={onLogout}
            title="Sign out"
            aria-label="Sign out"
          >
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </aside>
  );
}
