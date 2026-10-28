import React, { useState, useEffect } from 'react';
import { api } from '../api';
import { Scale, Edit3, Save, Check, Shield } from 'lucide-react';

export default function StandardsManager({ user }) {
  const [standards, setStandards] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [editForm, setEditForm] = useState({});
  const [saveMsg, setSaveMsg] = useState("");

  useEffect(() => {
    loadStandards();
  }, []);

  async function loadStandards() {
    try {
      const data = await api.getStandards();
      setStandards(data);
    } catch (err) {
      console.error("Failed to load standards", err);
    }
  }

  function startEdit(s) {
    setEditingId(s.id);
    setEditForm({
      recommended_min_length: s.recommended_min_length,
      requires_complexity: s.requires_complexity,
      max_failed_attempts_threshold: s.max_failed_attempts_threshold,
      min_lockout_duration_minutes: s.min_lockout_duration_minutes,
      recommended_max_password_age_days: s.recommended_max_password_age_days,
      recommended_password_history_count: s.recommended_password_history_count,
      requires_breached_dictionary_check: s.requires_breached_dictionary_check,
      mfa_recommendation: s.mfa_recommendation
    });
  }

  async function saveEdit(id) {
    try {
      await api.updateStandard(id, editForm);
      setEditingId(null);
      setSaveMsg("Standard parameters updated successfully!");
      loadStandards();
      setTimeout(() => setSaveMsg(""), 3000);
    } catch (err) {
      alert(`Update failed: ${err.message}`);
    }
  }

  return (
    <div style={{ maxWidth: "1150px", margin: "0 auto", padding: "32px 20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "16px", marginBottom: "28px" }}>
        <div>
          <h1 style={{ fontSize: "2rem", fontWeight: 800, marginBottom: "4px" }}>
            Security Framework Standards
          </h1>
          <p style={{ color: "var(--text-secondary)", fontSize: "0.92rem" }}>
            Regulatory benchmarks and customizable organizational thresholds (Proposal Feature #56 & #74).
          </p>
        </div>

        {saveMsg && (
          <div style={{ color: "var(--color-pass)", fontSize: "0.85rem", fontWeight: 600, display: "flex", alignItems: "center", gap: "6px" }}>
            <Check size={16} /> {saveMsg}
          </div>
        )}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))", gap: "24px" }}>
        {standards.map(s => {
          const isEditing = editingId === s.id;
          const canEdit = user?.role === 'Administrator' && (s.is_custom_editable || true);

          return (
            <div key={s.id} className="sec-card" style={{ display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
              <div>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
                  <span style={{ fontSize: "0.75rem", background: "rgba(6, 182, 212, 0.12)", color: "var(--accent-cyan)", padding: "2px 8px", borderRadius: "4px", fontWeight: 700 }}>
                    {s.publisher}
                  </span>
                  {s.is_custom_editable && (
                    <span style={{ fontSize: "0.72rem", background: "rgba(226, 155, 179, 0.15)", color: "var(--primary)", padding: "2px 8px", borderRadius: "4px", fontWeight: 600 }}>
                      Customizable
                    </span>
                  )}
                </div>

                <h3 style={{ fontSize: "1.25rem", fontWeight: 700, marginBottom: "4px" }}>
                  {s.name}
                </h3>
                <div style={{ fontSize: "0.82rem", color: "var(--text-muted)", marginBottom: "14px" }}>
                  {s.subtitle}
                </div>
                <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", lineHeight: 1.5, marginBottom: "20px" }}>
                  {s.description}
                </p>

                {/* Parameters List or Form */}
                {isEditing ? (
                  <div style={{ display: "flex", flexDirection: "column", gap: "10px", background: "rgba(15, 10, 20, 0.5)", padding: "14px", borderRadius: "var(--radius-sm)", marginBottom: "16px" }}>
                    <div>
                      <label style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Min Length (Chars)</label>
                      <input 
                        type="number" 
                        value={editForm.recommended_min_length} 
                        onChange={(e) => setEditForm({ ...editForm, recommended_min_length: parseInt(e.target.value) })}
                        className="sec-input"
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Max Lockout Attempts</label>
                      <input 
                        type="number" 
                        value={editForm.max_failed_attempts_threshold} 
                        onChange={(e) => setEditForm({ ...editForm, max_failed_attempts_threshold: parseInt(e.target.value) })}
                        className="sec-input"
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Lockout Duration (Mins)</label>
                      <input 
                        type="number" 
                        value={editForm.min_lockout_duration_minutes} 
                        onChange={(e) => setEditForm({ ...editForm, min_lockout_duration_minutes: parseInt(e.target.value) })}
                        className="sec-input"
                      />
                    </div>
                    <div>
                      <label style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>Max Age Days (0 = never)</label>
                      <input 
                        type="number" 
                        value={editForm.recommended_max_password_age_days} 
                        onChange={(e) => setEditForm({ ...editForm, recommended_max_password_age_days: parseInt(e.target.value) })}
                        className="sec-input"
                      />
                    </div>
                  </div>
                ) : (
                  <div style={{ background: "rgba(15, 10, 20, 0.4)", padding: "12px 16px", borderRadius: "var(--radius-sm)", border: "1px solid var(--border-subtle)", fontSize: "0.82rem", display: "flex", flexDirection: "column", gap: "6px", marginBottom: "16px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span style={{ color: "var(--text-muted)" }}>Recommended Min Length:</span>
                      <strong style={{ color: "var(--text-primary)" }}>{s.recommended_min_length} chars</strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span style={{ color: "var(--text-muted)" }}>Lockout Max Failures:</span>
                      <strong style={{ color: "var(--text-primary)" }}>{s.max_failed_attempts_threshold} attempts</strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span style={{ color: "var(--text-muted)" }}>Lockout Duration:</span>
                      <strong style={{ color: "var(--text-primary)" }}>{s.min_lockout_duration_minutes} mins</strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span style={{ color: "var(--text-muted)" }}>Max Password Age:</span>
                      <strong style={{ color: "var(--text-primary)" }}>{s.recommended_max_password_age_days === 0 ? "No arbitrary rotation" : `${s.recommended_max_password_age_days} days`}</strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span style={{ color: "var(--text-muted)" }}>History Retention:</span>
                      <strong style={{ color: "var(--text-primary)" }}>{s.recommended_password_history_count} remembered</strong>
                    </div>
                    <div style={{ display: "flex", justifyContent: "space-between" }}>
                      <span style={{ color: "var(--text-muted)" }}>MFA Recommendation:</span>
                      <strong style={{ color: "var(--accent-cyan)" }}>{s.mfa_recommendation}</strong>
                    </div>
                  </div>
                )}
              </div>

              {canEdit && (
                <div style={{ display: "flex", justifyContent: "flex-end", gap: "8px" }}>
                  {isEditing ? (
                    <>
                      <button onClick={() => setEditingId(null)} className="btn-secondary-custom" style={{ padding: "6px 12px", fontSize: "0.8rem" }}>
                        Cancel
                      </button>
                      <button onClick={() => saveEdit(s.id)} className="btn-cyan-custom" style={{ padding: "6px 14px", fontSize: "0.8rem" }}>
                        <Save size={13} /> Save Rules
                      </button>
                    </>
                  ) : (
                    <button onClick={() => startEdit(s)} className="btn-secondary-custom" style={{ padding: "6px 14px", fontSize: "0.8rem" }}>
                      <Edit3 size={13} /> Edit Limits
                    </button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
