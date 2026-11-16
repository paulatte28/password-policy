import React, { useState, useEffect } from 'react';
import { RefreshCw, Search, ChevronLeft, ChevronRight } from 'lucide-react';
import { api } from '../api';

function formatAction(action) {
  return action
    .toLowerCase()
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function AuditLogsView() {
  const [searchInput, setSearchInput] = useState('');
  const [search, setSearch] = useState('');
  const [actionFilter, setActionFilter] = useState('');
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [refreshTick, setRefreshTick] = useState(0);
  const [data, setData] = useState({ items: [], total: 0, actions: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => setSearch(searchInput), 300);
    return () => clearTimeout(timer);
  }, [searchInput]);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError('');
    api.getAuditLogs({ page, pageSize, search, action: actionFilter })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [page, pageSize, search, actionFilter, refreshTick]);

  const totalPages = Math.max(1, Math.ceil(data.total / pageSize));
  const startEntry = data.total ? (page - 1) * pageSize + 1 : 0;
  const endEntry = Math.min(page * pageSize, data.total);

  function clearFilters() {
    setSearchInput('');
    setSearch('');
    setActionFilter('');
    setPage(1);
  }

  return (
    <div className="workspace-page">
      <div className="activity-heading">
        <div>
          <span className="page-eyebrow">Administration</span>
          <h1>Activity log</h1>
          <p>Review sign-ins, policy changes, and account actions.</p>
        </div>
        <button
          className="btn-secondary-custom"
          onClick={() => setRefreshTick((t) => t + 1)}
          disabled={loading}
        >
          <RefreshCw size={16} /> Refresh
        </button>
      </div>

      <div className="activity-toolbar">
        <label className="activity-search">
          <Search size={17} aria-hidden="true" />
          <span className="sr-only">Search activity</span>
          <input
            value={searchInput}
            onChange={(e) => {
              setSearchInput(e.target.value);
              setPage(1);
            }}
            placeholder="Search people, actions, details, or IP"
          />
        </label>

        <label className="activity-select">
          <span>Action</span>
          <select
            value={actionFilter}
            onChange={(e) => {
              setActionFilter(e.target.value);
              setPage(1);
            }}
          >
            <option value="">All actions</option>
            {data.actions.map((act) => (
              <option key={act} value={act}>
                {formatAction(act)}
              </option>
            ))}
          </select>
        </label>

        <label className="activity-select activity-page-size">
          <span>Rows</span>
          <select
            value={pageSize}
            onChange={(e) => {
              setPageSize(Number(e.target.value));
              setPage(1);
            }}
          >
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
          </select>
        </label>

        {(searchInput || actionFilter) && (
          <button className="text-action" onClick={clearFilters}>
            Clear filters
          </button>
        )}
      </div>

      {error && (
        <div className="overview-error" role="alert">
          {error}
        </div>
      )}

      <div className="activity-summary">
        {loading ? 'Loading activity…' : `${data.total} ${data.total === 1 ? 'entry' : 'entries'}`}
      </div>

      <div className="sec-card data-table-wrap" style={{ padding: 0 }}>
        <table className="data-table activity-table">
          <thead>
            <tr>
              <th>When</th>
              <th>Action</th>
              <th>Person</th>
              <th>Details</th>
              <th>IP address</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((item) => (
              <tr key={item.id}>
                <td className="activity-date">{new Date(item.timestamp).toLocaleString()}</td>
                <td>
                  <span className="activity-action">{formatAction(item.action)}</span>
                </td>
                <td>
                  <strong>{item.user_name}</strong>
                  <small>{item.user_role}</small>
                </td>
                <td>{item.details || '—'}</td>
                <td className="activity-ip">{item.ip_address}</td>
              </tr>
            ))}
          </tbody>
        </table>

        {!loading && !error && data.items.length === 0 && (
          <div className="activity-empty">
            {searchInput || actionFilter
              ? 'No activity matches these filters.'
              : 'No activity has been recorded yet.'}
          </div>
        )}
      </div>

      <div className="activity-pagination">
        <span>
          {data.total ? `Showing ${startEntry}–${endEntry} of ${data.total}` : 'No entries to show'}
        </span>
        <div>
          <button
            className="btn-secondary-custom"
            onClick={() => setPage((p) => p - 1)}
            disabled={page === 1 || loading}
            aria-label="Previous page"
          >
            <ChevronLeft size={16} /> Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button
            className="btn-secondary-custom"
            onClick={() => setPage((p) => p + 1)}
            disabled={page >= totalPages || loading}
            aria-label="Next page"
          >
            Next <ChevronRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
