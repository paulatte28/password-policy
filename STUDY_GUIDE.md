# #23 PasswordPolicy Checker — Complete System Study Guide (Internal to External)

> **Project:** PasswordPolicy Checker: A Web-Based System for Evaluating Password Policy Compliance and Security Risks  
> **Course:** System Administration and Maintenance – IT23/L (Code: 3493 • 7:30–9:30 PM)  
> **Author:** Kristine Paula S. Coretico  

---

## 1. Big-Picture Overview

**PasswordPolicy Checker** is a full-stack **3-Tier Web Application** designed to evaluate an organization's password policy configuration against industry cybersecurity standards (**NIST SP 800-63B**, **OWASP ASVS v4.0**, **CIS Security Benchmark v8**, and a customizable **Organization Baseline**).

### Core Design Principles
* **Privacy-by-Design:** Evaluates *policy rules* (length, complexity, lockout, expiration, history, hygiene) without ever collecting or storing end-user plaintext passwords.
* **Defense-in-Depth on Its Own Auth:** The app enforces its own active password policy (`active_policy` table) on staff accounts, using BCrypt hashing, server-tracked JWT sessions, account lockout, password history, and **Have I Been Pwned (HIBP)** breached-password screening.
* **Environment-Aware Persistence:** Runs zero-config locally on **SQLite** (`passwordpolicy.db`) and fail-closed in production on **Supabase PostgreSQL**.

---

## 2. 3-Tier Architecture (Internal to External)

```text
[ Tier 1: Presentation Layer (Client) ]
  React 19 + Vite 8 + Chart.js + Lucide Icons
  Hosted on Vercel Edge/Static CDN (or localhost:5173 in dev)
        │
        ▼  HTTPS / JSON (REST API + Bearer JWT)
[ Tier 2: Application & Security Layer (Server) ]
  FastAPI + Pydantic + Uvicorn / Vercel Serverless (api/index.py)
  Auth (BCrypt + PyJWT + RBAC) • Compliance Engine • JSON/CSV Parser
        │
        ├──► External API: Have I Been Pwned (api.pwnedpasswords.com/range/{prefix})
        │
        ▼  SQLAlchemy 2.x ORM
[ Tier 3: Data & Infrastructure Layer ]
  Local: SQLite (passwordpolicy.db)
  Prod:  Supabase PostgreSQL (SSL, psycopg2-binary) + GitHub Actions Keepalive
```

---

## 3. Complete Repository & File Map

### Root Directory
| File / Folder | Purpose |
| :--- | :--- |
| `api/index.py` | Vercel serverless entrypoint; adds repo root to `sys.path` and exports FastAPI `app`. |
| `vercel.json` | Builds `frontend/dist`, rewrites `/api/(.*)` to `/api/index.py`, and falls back to `/index.html` for SPA routing. |
| `requirements.txt` | Python dependencies (`fastapi`, `uvicorn[standard]`, `sqlalchemy`, `pydantic`, `python-dotenv`, `python-multipart`, `pyjwt`, `bcrypt`, `psycopg2-binary`, `email-validator`). |
| `start_all.bat` | One-click Windows launcher that starts both backend and frontend terminals. |
| `start_backend.bat` | Runs `.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000`. |
| `start_frontend.bat` | Runs `npm run dev` inside `frontend/` (Vite on port `5173`). |
| `.github/workflows/supabase-keepalive.yml` | Scheduled GitHub Action that pings `/api/keepalive` 4x/day to prevent Supabase Free-tier pausing. |

### Backend (`backend/`)
| File | Responsibility |
| :--- | :--- |
| `backend/main.py` | FastAPI app initialization (`/api/docs`), CORS, all REST endpoints, JSON/CSV policy import/export, `record_audit` helper. |
| `backend/database.py` | Loads `backend/.env`, normalizes `DATABASE_URL` to `postgresql+psycopg2://`, falls back to SQLite locally, enforces fail-closed checks on Vercel/Render. |
| `backend/models.py` | SQLAlchemy ORM definitions for all **9 database tables**. |
| `backend/schemas.py` | Pydantic `BaseModel` schemas for request validation, numeric bounds (`Field(ge=..., le=...)`), and response serialization. |
| `backend/auth.py` | BCrypt password hashing/verification, PyJWT token creation/validation, `UserSession` lookup, forced password-change/expiry checks, and RBAC dependencies (`require_admin`, `require_analyst_or_admin`, `require_auditor_or_admin`). |
| `backend/compliance_engine.py` | Weighted 6-dimension scoring engine (`evaluate_policy`), letter grading, risk classification, and actionable findings generator. |
| `backend/policy_enforcement.py` | Live password validation against `active_policy`, `COMMON_PASSWORDS` check, HIBP SHA-1 k-anonymity check, `password_history` check, and `login_state` tracking. |
| `backend/seed_data.py` | Seeds initial standards (`NIST_SP_800_63B`, `OWASP_ASVS`, `CIS_BENCHMARK`, `CUSTOM_ORG`), sample presets, and admin/demo accounts. |

### Frontend (`frontend/src/`)
| File | Responsibility |
| :--- | :--- |
| `frontend/src/api.js` | Centralized `fetch` client; auto-switches `API_BASE` between `http://localhost:8000/api` (when on port `5173`) and `/api` (production). Attaches `Bearer` JWT from `localStorage`. |
| `frontend/src/App.jsx` | Root state manager: authentication bootstrap (`getMe`), forced password-change modal, active tab routing, RBAC view guards. |
| `frontend/src/components/Navbar.jsx` | Role-aware sidebar navigation (hides `Policy editor` for Auditors; hides `Users` for non-Admins; shows `Activity log` to Admins and Auditors). |
| `frontend/src/components/Login.jsx` | Sign-in form displaying error messages (invalid credentials, locked account, inactive account). |
| `frontend/src/components/Dashboard.jsx` | Overview metrics, score trends, and Chart.js visualizations. |
| `frontend/src/components/PolicyEvaluator.jsx` | Interactive policy form, sample preset loader, and JSON/CSV file import UI. |
| `frontend/src/components/EvaluationReportView.jsx` | Detailed score card, 6-dimension breakdown, findings filter (`All`/`Fails`/`Warnings`/`Pass`), CSV export, Print/PDF. |
| `frontend/src/components/EvaluationHistory.jsx` | List of saved `EvaluationReport` records. |
| `frontend/src/components/PolicyCompare.jsx` | Side-by-side comparison of two saved evaluation reports. |
| `frontend/src/components/StandardsManager.jsx` | Displays NIST, OWASP, CIS, and Custom Org baselines; allows Administrators to edit thresholds. |
| `frontend/src/components/UserManagement.jsx` | Admin-only user creation, role assignment, activation/deactivation, password resets, and demo user seeding. |
| `frontend/src/components/AuditLogsView.jsx` | Searchable, filterable, paginated view of `audit_logs` (accessible to Administrators and Auditors). |
| `frontend/src/components/PasswordChange.jsx` | Modal for changing the logged-in user's password (triggered manually or forced when expired/`must_change_password`). |

---

## 4. Internal Security: Authentication, Sessions & RBAC

### A. Password Hashing (`backend/auth.py`)
* Uses **`bcrypt`** directly (`bcrypt.hashpw` with `bcrypt.gensalt()` and `bcrypt.checkpw`).
* Enforces BCrypt's **72 UTF-8 byte limit** (`len(password.encode("utf-8")) > 72` raises `ValueError` / HTTP `400`).

### B. JWT + Server-Side Session Tracking
1. On `POST /api/auth/login`, the backend verifies the password and checks `login_state`.
2. It generates a unique session ID (`jti`) stored in the **`user_sessions`** table with an expiration timestamp (`ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24` = **24 hours**).
3. It signs a **JWT (`HS256`)** containing `sub` (email), `role`, and `jti`.
4. On every authenticated request, `get_current_user` decodes the JWT **and** verifies that `jti` still exists in `user_sessions` and has not expired.
5. On `POST /api/auth/logout`, the row in `user_sessions` is deleted—meaning **logged-out tokens are immediately invalidated server-side** (true revocation, not just client-side token deletion).

### C. Account Lockout & Password Expiration Enforcement
* **`login_state` table** tracks `failed_attempts`, `last_failed_at`, `locked_until`, `password_changed_at`, and `must_change_password`.
* If `active_policy` configures `max_failed_attempts > 0`, exceeding the threshold sets `locked_until` to `now + lockout_duration_min`.
* If `must_change_password` is `True` OR `now > password_changed_at + max_password_age_days`, `get_current_user` blocks all endpoints except `/api/auth/me`, `/api/auth/logout`, and `/api/auth/change-password` with HTTP **`403`** (`"Change your password before continuing"`).

### D. Role-Based Access Control (RBAC) Matrix
Legacy `"Viewer"` roles are normalized to `"Auditor"` (`normalize_role` in `backend/main.py`).

| Capability / Endpoint | Administrator | Security Analyst | Auditor (Read-Only) |
| :--- | :---: | :---: | :---: |
| View Overview Dashboard (`/api/dashboard/stats`) | ✅ | ✅ | ✅ |
| View & Compare Reports (`/api/reports`, `/api/reports/{id}`) | ✅ | ✅ | ✅ |
| Export Report CSV (`/api/reports/{id}/export-csv`) | ✅ | ✅ | ✅ |
| View Benchmarks & Active Policy (`/api/standards`, `GET /api/policies/active`) | ✅ | ✅ | ✅ |
| View Activity / Audit Logs (`GET /api/audit`) | ✅ | ❌ | ✅ (Read-Only) |
| Evaluate Policies & Import JSON/CSV (`/api/policies/evaluate`, `/api/policies/import`) | ✅ | ✅ | ❌ |
| Activate Live Policy (`PUT /api/policies/active`) | ✅ | ❌ | ❌ |
| Edit Benchmark Thresholds (`PUT /api/standards/{id}`) | ✅ | ❌ | ❌ |
| Manage Users & Demo Accounts (`/api/users*`) | ✅ | ❌ | ❌ |

---

## 5. External Integration: HIBP SHA-1 k-Anonymity

In `backend/policy_enforcement.py`, `validate_password()` screens new passwords whenever `policy.disallow_common` is enabled:
1. **Local Dictionary Check:** Checks against `COMMON_PASSWORDS` (e.g., `"password123"`, `"admin@123456"`, etc.).
2. **HIBP API Check (`check_pwned_password`):**
   * Computes the **SHA-1** hash of the candidate password locally and converts it to uppercase hex.
   * Splits it into **`prefix` (first 5 hex characters)** and **`suffix` (remaining 35 characters)**.
   * Sends a `GET` request to `https://api.pwnedpasswords.com/range/{prefix}` with header `Add-Padding: true` and a `2.5s` timeout.
   * **Why this is private (k-Anonymity):** The full password and full hash **never leave your server**. HIBP returns all hash suffixes matching that 5-character prefix, and your backend checks locally if `suffix` is in the response. If found, the password is rejected. If HIBP is unreachable, it returns `None` and degrades gracefully without crashing.

---

## 6. Compliance Evaluation Engine (`backend/compliance_engine.py`)

The engine evaluates a `PolicyInput` against a selected `StandardDefinition` across **6 weighted dimensions**:

| Dimension | Weight | What It Evaluates |
| :--- | :---: | :--- |
| **1. Length** | **30%** | `min_length` vs standard's `recommended_min_length` (critical fail if `< 8`), plus `max_length` (NIST recommends supporting `>= 64` chars for passphrases). |
| **2. Lockout** | **25%** | `max_failed_attempts` (`0` = no lockout = critical fail) and `lockout_duration_min` vs standard's thresholds. |
| **3. Complexity** | **15%** | Uppercase, lowercase, digit, special character flags and `min_categories`. Also notes NIST SP 800-63B guidance when rigid composition rules are paired with short passwords. |
| **4. Expiration** | **10%** | `max_password_age_days` (`0` = no arbitrary rotation, aligned with NIST; periodic rotation checked against OWASP/CIS) and `min_password_age_days`. |
| **5. Reuse (History)** | **10%** | `password_history_count` vs `recommended_password_history_count` (`0` flags immediate reuse risk). |
| **6. Hygiene** | **10%** | `disallow_common` (breached dictionary screening), `disallow_username`, and `require_mfa`. |

### Scoring, Grades & Risk Levels
* **Overall Score:**  
  `score = (length * 0.30) + (lockout * 0.25) + (complexity * 0.15) + (expiration * 0.10) + (reuse * 0.10) + (hygiene * 0.10)` (rounded to 1 decimal place, clamped `0.0–100.0`).
* **Letter Grades:** `A+` (≥ 93), `A` (≥ 85), `B` (≥ 75), `C` (≥ 65), `D` (≥ 50), `F` (< 50).
* **Risk Levels:**
  * **Critical:** Any `CRITICAL` `FAIL` finding OR `overall_score < 50.0`
  * **High:** More than 1 `HIGH` `FAIL`/`WARNING` OR `overall_score < 70.0`
  * **Moderate:** `overall_score < 85.0`
  * **Low:** `overall_score >= 85.0` and no critical/multiple high issues.

---

## 7. Database Schema (All 9 Tables in `backend/models.py`)

| Table Name | Purpose |
| :--- | :--- |
| `users` | Staff accounts (`id`, `email`, `full_name`, `role`, `department`, `hashed_password`, `is_active`, `created_at`). |
| `policy_settings` | Saved policy profiles and sample presets (`weak`, `moderate`, `strong`). |
| `standard_definitions` | Benchmark baselines (`NIST_SP_800_63B`, `OWASP_ASVS`, `CIS_BENCHMARK`, `CUSTOM_ORG`). |
| `evaluation_reports` | Saved compliance results (`overall_compliance_score`, `grade_letter`, `risk_level`, `findings_json`, `scores_breakdown_json`, `policy_snapshot_json`). |
| `audit_logs` | Immutable activity trail (`action`, `details`, `user_name`, `user_role`, `ip_address`, `score_snapshot`, `timestamp`). |
| `active_policy` | Single-row (`id=1`) JSON configuration of the currently enforced live password policy. |
| `login_state` | Per-user brute-force lockout counters, `locked_until`, `password_changed_at`, and `must_change_password`. |
| `password_history` | Historical BCrypt hashes per `user_id` to prevent password reuse. |
| `user_sessions` | Active JWT session IDs (`id` = `jti`, `user_id`, `expires_at`) for server-side logout/revocation. |

---

## 8. Complete REST API Reference (`backend/main.py`)

Interactive Swagger/OpenAPI docs are served at **`/api/docs`** (`/docs` redirects to `/api/docs`; schema at `/api/openapi.json`).

### Authentication & Account
* `POST /api/auth/login` — Authenticate with email/password, enforce lockout, issue JWT + `UserSession`, log `USER_LOGIN` or `LOGIN_FAILED`.
* `GET /api/auth/me` — Return current user profile + password expiry status.
* `POST /api/auth/logout` — Delete `UserSession` row and log `USER_LOGOUT`.
* `POST /api/auth/change-password` — Verify current password, validate new password against `active_policy` + HIBP + `password_history`, update hash & `login_state`.

### Users (Admin Only)
* `GET /api/users` — List all users.
* `POST /api/users` — Create user (validates password against `active_policy`).
* `PUT /api/users/{user_id}` — Update role, department, active status, or reset password.
* `POST /api/users/seed-demo` — Create/reset demo Analyst and Auditor accounts.

### Policies, Standards & Reports
* `GET /api/standards` & `GET /api/standards/{standard_id}` — Read benchmark standards.
* `PUT /api/standards/{standard_id}` — Update benchmark thresholds (Admin only).
* `GET /api/policies/active` & `PUT /api/policies/active` — Read or activate live policy (PUT is Admin only).
* `GET /api/policies/samples` — Return preset sample policies.
* `POST /api/policies/evaluate` — Run `evaluate_policy`, optionally save `EvaluationReport`, log `POLICY_EVALUATION` (Admin/Analyst).
* `POST /api/policies/import` — Parse uploaded `.json` or `.csv` policy file into a normalized policy object (Admin/Analyst).
* `GET /api/reports` & `GET /api/reports/{report_id}` — List or inspect saved reports.
* `GET /api/reports/{report_id}/export-csv` — Download findings as CSV.
* `GET /api/dashboard/stats` — Aggregate totals, average score, score history, and recent reports.

### Audit, Health & Operations
* `GET /api/audit` — Paginated, searchable, action-filterable audit logs (Admin & Auditor).
* `GET /api/health` — Basic health check (no DB query).
* `GET /api/integrations/status` — Reports status of policy import, OpenAPI, and keepalive configuration.
* `GET /api/keepalive` — Protected by `X-Keepalive-Token` header; queries `standard_definitions` to keep Supabase PostgreSQL active.

---

## 9. Deployment, Cloud & CI/CD (External)

### Local Development
* Uses `.venv` (Python 3.14) + Uvicorn on `http://localhost:8000` and Vite on `http://localhost:5173`.
* If `DATABASE_URL` is not set in `backend/.env`, `backend/database.py` automatically uses `sqlite:///./passwordpolicy.db`.

### Production (Vercel + Supabase)
* **Vercel (`vercel.json`):** Builds `frontend/` (`npm run build` → `frontend/dist`) and routes all `/api/*` traffic to the Python serverless function `api/index.py`.
* **Fail-Closed Safety:** When `VERCEL` or `RENDER` env vars are detected:
  * `backend/database.py` raises `RuntimeError` if `DATABASE_URL` is missing (never silently falls back to ephemeral SQLite).
  * `backend/auth.py` raises `RuntimeError` if `JWT_SECRET` is missing (never uses the local dev secret).
* **Supabase PostgreSQL:** Connected via `DATABASE_URL` normalized to `postgresql+psycopg2://` with `pool_pre_ping=True` over SSL.
* **GitHub Actions Keepalive (`.github/workflows/supabase-keepalive.yml`):**
  * Runs on cron `17 1,7,13,19 * * *` (4 times/day UTC: `01:17`, `07:17`, `13:17`, `19:17` UTC) plus manual `workflow_dispatch`.
  * Sends `X-Keepalive-Token` (stored in GitHub Secrets as `KEEPALIVE_TOKEN`) to `https://password-policy1.vercel.app/api/keepalive`, which uses `secrets.compare_digest` and executes a lightweight `SELECT` on `standard_definitions`.

---

## 10. Quick Defense Q&A Cheat Sheet

* **Q: How does Pydantic fit into the system?**  
  A: Defined in `backend/schemas.py`, Pydantic validates all incoming JSON payloads (types, required fields, numeric `Field` bounds like `min_length` `1–128`) and powers the `/api/docs` OpenAPI schema.
* **Q: Why use SHA-1 k-anonymity for Have I Been Pwned?**  
  A: Because sending a user's plaintext password—or even its full hash—to an external API is a security risk. Sending only the first 5 characters of the SHA-1 hash lets our server check for breaches locally without exposing the password.
* **Q: Why have an `Auditor` role if they can't edit policies?**  
  A: Principle of Least Privilege and Separation of Duties. Auditors and management need read-only access to dashboards, compliance reports, CSV exports, and the Activity log without the ability to alter security policies or user accounts.
* **Q: What happens when a user logs out—can their old JWT still be used?**  
  A: No. Each JWT embeds a `jti` linked to the `user_sessions` table. Logging out deletes that row, so `get_current_user` immediately rejects the token with `401 Session expired or signed out`.
