# #23 PasswordPolicy Checker — Complete System Study Guide (Process, Flows & Architecture)

> **Project:** PasswordPolicy Checker: A Web-Based System for Evaluating Password Policy Compliance and Security Risks  
> **Course:** System Administration and Maintenance – IT23/L (Code: 3493 • 7:30–9:30 PM)  
> **Author:** Kristine Paula S. Coretico  

---

## 1. Big-Picture Overview

**PasswordPolicy Checker** is a full-stack **3-Tier Web Application** that evaluates an organization's password policy configuration against industry cybersecurity standards (**NIST SP 800-63B**, **OWASP ASVS v4.0**, **CIS Security Benchmark v8**, and a customizable **Organization Baseline**).

### Core Design Principles
* **Privacy-by-Design:** Evaluates *policy rules* (length, complexity, lockout, expiration, history, hygiene) without ever requesting or storing real end-user passwords.
* **Defense-in-Depth on Its Own Auth:** The system enforces its own active password policy (`active_policy` table) on staff accounts using salted **BCrypt** hashing, server-tracked **JWT** sessions, brute-force account lockout, password history retention, and **Have I Been Pwned (HIBP)** breached-password screening.
* **Environment-Aware Persistence:** Runs zero-config locally on **SQLite** (`passwordpolicy.db`) and fail-closed in production on **Supabase PostgreSQL**.

---

## 2. 3-Tier Architecture & Network Topology

```text
[ Tier 1: Presentation Layer (Client Web Layer) ]
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
        ▼  SQLAlchemy 2.x ORM (Atomic DB & Audit Transactions)
[ Tier 3: Data Storage & Third-Party Integration Layer ]
  Local: SQLite (passwordpolicy.db)
  Prod:  Supabase PostgreSQL (SSL, psycopg2-binary) + GitHub Actions Keepalive
```

---

## 3. End-to-End System Flows & Step-by-Step Processes

This section explains **exactly how the system works step by step** from startup to every user action.

### Flow 1: Application Startup & Database Seeding
1. **Database Connection (`backend/database.py`):**
   * Loads environment variables from `backend/.env`.
   * If `DATABASE_URL` is set, normalizes `postgres://` or `postgresql://` to `postgresql+psycopg2://` and connects with `pool_pre_ping=True`.
   * If `DATABASE_URL` is missing:
     * On `VERCEL` or `RENDER`: raises `RuntimeError` (**fail-closed** so production never silently uses ephemeral SQLite).
     * Locally: falls back to `sqlite:///./passwordpolicy.db`.
2. **Table Creation & Initial Seeding (`backend/main.py` + `backend/seed_data.py`):**
   * `Base.metadata.create_all(bind=engine)` creates all **9 tables** if they do not exist yet.
   * `seed_database(db)` inserts the 4 benchmark standards (`NIST_SP_800_63B`, `OWASP_ASVS`, `CIS_BENCHMARK`, `CUSTOM_ORG`), sample policy presets (`weak`, `moderate`, `strong`), the default `ActivePolicy`, and initial staff accounts.

---

### Flow 2: Authentication, Lockout Gate & JWT Session Lifecycle
1. **Login Request (`Login.jsx` → `POST /api/auth/login`):**
   * User enters email and password in the browser.
   * Frontend sends `POST /api/auth/login` with JSON `{ email, password }`.
   * Backend looks up the `User` row by email and checks `user.is_active`.
2. **Security Gate (`backend/auth.py` + `backend/policy_enforcement.py`):**
   * Checks `login_state.locked_until`. If still in the future, rejects immediately with an account-locked error and logs `LOGIN_FAILED` in `audit_logs`.
   * Verifies password against `user.hashed_password` using `bcrypt.checkpw()`.
   * **If invalid:** increments `login_state.failed_attempts`. If `active_policy.max_failed_attempts > 0` and the threshold is reached, sets `locked_until = now + lockout_duration_min`. Logs `LOGIN_FAILED` and returns HTTP `401`.
   * **If valid:** resets `failed_attempts = 0` and clears `locked_until`.
3. **JWT + Server-Side Session Issuance:**
   * Generates a unique session ID (`jti`) and stores it in `user_sessions` (`ACCESS_TOKEN_EXPIRE_MINUTES = 1440` = 24 hours).
   * Signs an `HS256` JWT containing `sub` (email), `role`, and `jti`.
   * Logs `USER_LOGIN` to `audit_logs` with the client IP address.
   * Frontend (`App.jsx`) saves the JWT in `localStorage` and sets `user` state.
4. **Per-Request Validation (`get_current_user`):**
   * Every protected API request attaches `Authorization: Bearer <token>`.
   * Backend decodes the JWT, verifies `jti` still exists and is unexpired in `user_sessions`, and checks `user.is_active`.
   * Checks password expiration / `must_change_password`: if expired (`now > password_changed_at + max_password_age_days`) or flagged, all endpoints except `/api/auth/me`, `/api/auth/logout`, and `/api/auth/change-password` return HTTP `403` (`"Change your password before continuing"`), forcing the `PasswordChange.jsx` screen.
5. **Logout (`POST /api/auth/logout`):**
   * Deletes the `UserSession` row matching `jti`, logs `USER_LOGOUT`, and clears `localStorage` on the frontend. Any reuse of the old JWT is immediately rejected with `401`.

---

### Flow 3: Role-Based Access Control (RBAC) & Dashboard Routing
1. After login, `App.jsx` and `Navbar.jsx` render a role-aware sidebar (legacy `"Viewer"` is normalized to `"Auditor"`):
   * **Administrator:** Full access — Overview, Policy editor, Reports, Compare reports, Benchmarks (view + edit), Users (create/edit/reset/seed demo), Activity log.
   * **Security Analyst:** Evaluation & analysis — Overview, Policy editor (manual + JSON/CSV import), Reports, Compare reports, Benchmarks (view-only). Cannot manage users, edit benchmarks, activate live policy, or view Activity log.
   * **Auditor (Read-Only):** Oversight & compliance — Overview, Reports, Compare reports, Benchmarks (view-only), Activity log (read-only). Cannot evaluate, import, edit benchmarks, activate policies, or manage users.
2. **Backend Enforcement:** FastAPI route dependencies (`require_admin`, `require_analyst_or_admin`, `require_auditor_or_admin`) enforce RBAC server-side with HTTP `403 Forbidden`.

---

### Flow 4: Policy Editor, Evaluation & Risk Scoring Process
This is the core workflow of **PasswordPolicy Checker**, centered on the **Policy editor** (`PolicyEvaluator.jsx`):

#### What is the Policy Editor & Why Do You Use It?
* **What it is:** The **Policy editor** is the workspace where you input or import an organization's *password policy rules* (length, complexity, lockout, expiration, history, MFA, and dictionary checks)—**never** real user passwords.
* **Why you (the Administrator or Security Analyst) fill it in / import it:** Every organization's servers (Active Directory GPO, Linux PAM, school portals, or IAM systems) have different configured rules. The system cannot guess what rules your organization uses—you enter them into the Policy editor, load a sample (`weak` / `moderate` / `strong`), or upload a `.json`/`.csv` export so the system can **evaluate** them.
* **Two modes in the Policy editor:**
  1. **Evaluate Policy (Audit Mode):** Grades the entered rules against a chosen Benchmark (NIST, OWASP, CIS, or Custom Org) and saves a Compliance Report without changing any live login rules.
  2. **Activate Policy (Live Enforcement Mode — Admin only):** Saves those rules into the `active_policy` table (`PUT /api/policies/active`) so the app itself *enforces* them on its own staff accounts.

#### Step-by-Step Execution
1. **Input (`PolicyEvaluator.jsx`):**
   * **Manual Form:** Enter `name`, `min_length`, `max_length`, complexity toggles (`require_uppercase`, `require_lowercase`, `require_digit`, `require_special`, `min_categories`), lockout rules (`max_failed_attempts`, `lockout_duration_min`, `lockout_reset_min`), expiration rules (`max_password_age_days`, `min_password_age_days`), reuse (`password_history_count`), and hygiene (`disallow_common`, `disallow_username`, `require_mfa`).
   * **Sample Preset:** Click `weak`, `moderate`, or `strong` to auto-fill realistic demo rules.
   * **JSON/CSV Import:** Upload a `.json` or `.csv` file to `POST /api/policies/import`. The backend parses and normalizes fields into a `PolicyInput` object and pre-fills the form.
2. **Benchmark Selection:** Choose which **Benchmark** (`NIST_SP_800_63B`, `OWASP_ASVS`, `CIS_BENCHMARK`, or `CUSTOM_ORG`) to grade the policy against.
3. **Pydantic Validation (`backend/schemas.py`):**
   * Submitting calls `POST /api/policies/evaluate`.
   * Pydantic validates types and numeric bounds (`Field(ge=..., le=...)`) before scoring begins.
4. **Compliance Engine Execution (`backend/compliance_engine.py` → `evaluate_policy()`):**
   * Compares each policy setting against the selected `StandardDefinition` thresholds from the database.
   * Computes sub-scores (`0–100`) for all **6 weighted dimensions**:
     * **Length (30%)** + **Lockout (25%)** + **Complexity (15%)** + **Expiration (10%)** + **Reuse/History (10%)** + **Hygiene (10%)**.
   * Generates structured `Finding` items (`PASS`, `WARNING`, or `FAIL` with `LOW`/`MEDIUM`/`HIGH`/`CRITICAL` severity, `current_value`, `standard_requirement`, `risk_description`, and `recommendation`).
   * Computes `overall_score` (rounded to 1 decimal, clamped `0.0–100.0`), `grade_letter` (`A+` to `F`), `risk_level` (`Low`, `Moderate`, `High`, `Critical`), and `executive_summary`.
5. **Atomic Persistence & Audit:**
   * Saves an `EvaluationReport` row (with JSON snapshots of findings, breakdown, and policy) and an `AuditLog` entry (`POLICY_EVALUATION` with `score_snapshot` and IP) in the same database transaction.
   * Frontend opens `EvaluationReportView.jsx` showing the score card, 6-dimension progress bars, and filterable findings (`All` / `Fails` / `Warnings` / `Pass`).

---

### Flow 5: Live Policy Activation & HIBP Password Enforcement
1. **Activating a Policy (`PUT /api/policies/active`, Admin-only):**
   * Administrator saves the policy JSON to `active_policy` (`id=1`) and logs the action in `audit_logs`.
2. **Enforcing on Password Change / User Creation (`backend/policy_enforcement.py` → `validate_password()`):**
   * Checks BCrypt 72-byte UTF-8 limit.
   * Validates `min_length`, `max_length`, character classes, and `min_categories` against `active_policy`.
   * Checks `disallow_username` (ensures email/local-part isn't inside the password).
   * If `disallow_common` is enabled:
     1. Checks local `COMMON_PASSWORDS` set.
     2. Calls `check_pwned_password()` → computes local **SHA-1** hash, sends **only the first 5 hex characters** (`prefix`) to `https://api.pwnedpasswords.com/range/{prefix}` with `Add-Padding: true` (`2.5s` timeout), and checks locally if the remaining 35-char `suffix` is in the response. If matched, rejects the password; if HIBP is unreachable, degrades gracefully (`None`).
   * Checks `min_password_age_days` (prevents rapid cycling) and `password_history` (verifies against the last `password_history_count` BCrypt hashes).
   * On success, hashes with `bcrypt`, appends to `password_history`, and updates `login_state.password_changed_at`.

---

### Flow 6: Compare Reports, Export & Benchmarks
* **Compare Reports (`PolicyCompare.jsx`):**
  * **What it does:** Lets you pick any two saved `EvaluationReport` records (`GET /api/reports/{id}`) and view them **side by side**—comparing Overall Score, Grade, Risk Level, Benchmark Standard, and every rule setting (min length, complexity categories, lockout attempts, expiration, history, MFA).
  * **Why it exists & how it connects to your topic (Colonial Pipeline & Continuous Compliance):** Evaluating a weak policy once isn't enough—administrators and auditors need **before-and-after proof** that remediation worked:
    1. *Before:* Evaluate a weak legacy policy (like Colonial Pipeline's pre-attack VPN settings: no lockout, no MFA, no history) → failing score (e.g., Grade `F`, Critical Risk).
    2. *After:* Harden the policy (lockout `<= 5`, history `>= 5`, MFA enabled, length `>= 12`) and re-evaluate.
    3. *Compare Reports:* Shows the exact security improvement side by side for management and IT auditors, or lets you compare the *same* policy against two different benchmarks (e.g., NIST SP 800-63B vs. CIS Benchmark v8).
* **Export CSV (`GET /api/reports/{id}/export-csv`):** Streams findings as a downloadable `.csv` file.
* **Print / Save PDF (`EvaluationReportView.jsx`):** Triggers browser print layout styled for clean PDF export.
* **Benchmarks (`StandardsManager.jsx`):**
  * **What "Benchmark" means:** A **Benchmark** is the official "answer key" or **reference standard** (**NIST SP 800-63B**, **OWASP ASVS v4.0**, **CIS Security Benchmark v8**, or **Custom Organization Baseline**) defining minimum safe thresholds (recommended min length, max failed attempts, lockout duration, password history count, MFA requirement).
  * **How it works:** All 4 benchmarks live in the `standard_definitions` table. When you evaluate a policy, `evaluate_policy()` reads the chosen benchmark's thresholds from the database and grades your policy against them. Administrators can click **Edit Limits** (`PUT /api/standards/{id}`) to customize thresholds, and every edit is logged in `audit_logs` (`UPDATE_STANDARD`).

---

### Flow 7: Production Keepalive & Cloud Operations
* **Vercel (`vercel.json`):** Builds `frontend/dist` and rewrites `/api/(.*)` to `api/index.py` (which exports the FastAPI `app`).
* **GitHub Actions Keepalive (`.github/workflows/supabase-keepalive.yml`):** Runs 4x/day (`17 1,7,13,19 * * *` UTC) and sends `X-Keepalive-Token` to `/api/keepalive`. The backend verifies the token via `secrets.compare_digest` and queries `standard_definitions` to keep the Supabase Free-tier database active.

---

## 4. Complete Repository & File Map

### Root & Deployment
| File / Folder | Purpose |
| :--- | :--- |
| [`api/index.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/api/index.py) | Vercel serverless entrypoint; adds repo root to `sys.path` and exports FastAPI `app`. |
| [`vercel.json`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/vercel.json) | Builds `frontend/dist`, rewrites `/api/(.*)` to `/api/index.py`, and falls back to `/index.html` for SPA routing. |
| [`requirements.txt`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/requirements.txt) | Python dependencies (`fastapi`, `uvicorn[standard]`, `sqlalchemy`, `pydantic`, `python-dotenv`, `python-multipart`, `pyjwt`, `bcrypt`, `psycopg2-binary`, `email-validator`). |
| [`start_all.bat`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/start_all.bat) | One-click Windows launcher starting backend (`start_backend.bat`) and frontend (`start_frontend.bat`). |
| `.github/workflows/supabase-keepalive.yml` | Scheduled GitHub Action pinging `/api/keepalive` 4x/day. |

### Backend (`backend/`)
| File | Responsibility |
| :--- | :--- |
| [`backend/main.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/main.py) | FastAPI app (`/api/docs`), CORS, all REST endpoints, JSON/CSV parser & exporter, `record_audit` helper. |
| [`backend/database.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/database.py) | Loads `backend/.env`, normalizes `DATABASE_URL` to `postgresql+psycopg2://`, falls back to SQLite locally, fail-closed on Vercel/Render. |
| [`backend/models.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/models.py) | SQLAlchemy ORM definitions for all **9 database tables**. |
| [`backend/schemas.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/schemas.py) | Pydantic `BaseModel` schemas for request validation, numeric bounds (`Field(ge=..., le=...)`), and responses. |
| [`backend/auth.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/auth.py) | BCrypt hashing, PyJWT token creation/validation, `UserSession` lookup, expiry checks, and RBAC dependencies. |
| [`backend/compliance_engine.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/compliance_engine.py) | Weighted 6-dimension scoring engine (`evaluate_policy`), grading, risk classification, and findings generator. |
| [`backend/policy_enforcement.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/policy_enforcement.py) | Live password validation against `active_policy`, `COMMON_PASSWORDS`, HIBP SHA-1 k-anonymity, `password_history`, and `login_state`. |
| [`backend/seed_data.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/seed_data.py) | Seeds initial standards, sample presets, active policy, and admin/demo accounts. |

### Frontend (`frontend/src/`)
| File | Responsibility |
| :--- | :--- |
| [`frontend/src/api.js`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/api.js) | Centralized `fetch` client; auto-switches `API_BASE` between `http://localhost:8000/api` (port `5173`) and `/api` (prod); attaches `Bearer` JWT. |
| [`frontend/src/App.jsx`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/App.jsx) | Root state manager: session bootstrap (`getMe`), forced password-change modal, tab routing, RBAC view guards. |
| `frontend/src/components/Navbar.jsx` | Role-aware sidebar navigation (`Workspace` & `Administration` sections). |
| `frontend/src/components/Login.jsx` | Sign-in form displaying authentication, lockout, and inactive account feedback. |
| `frontend/src/components/Dashboard.jsx` | Overview metrics, score trends, and Chart.js visualizations. |
| `frontend/src/components/PolicyEvaluator.jsx` | Interactive policy form, sample preset loader, and JSON/CSV file import UI. |
| `frontend/src/components/EvaluationReportView.jsx` | Score card, 6-dimension breakdown, filterable findings (`All`/`Fails`/`Warnings`/`Pass`), CSV export, Print/PDF. |
| `frontend/src/components/EvaluationHistory.jsx` | List of saved `EvaluationReport` records. |
| `frontend/src/components/PolicyCompare.jsx` | Side-by-side comparison of two saved evaluation reports. |
| `frontend/src/components/StandardsManager.jsx` | Displays NIST, OWASP, CIS, and Custom Org baselines; Admin threshold editor. |
| `frontend/src/components/UserManagement.jsx` | Admin-only user creation, role assignment, status toggle, password reset, and demo seeding. |
| `frontend/src/components/AuditLogsView.jsx` | Searchable, action-filterable, paginated view of `audit_logs` (Admin & Auditor). |
| `frontend/src/components/PasswordChange.jsx` | Modal for changing password (manual or forced on expiration/`must_change_password`). |

---

## 5. Compliance Engine Scoring Formula (`backend/compliance_engine.py`)

| Dimension | Weight | What It Evaluates |
| :--- | :---: | :--- |
| **1. Length** | **30%** | `min_length` vs `recommended_min_length` (critical fail if `< 8`), plus `max_length` (NIST recommends `>= 64`). |
| **2. Lockout** | **25%** | `max_failed_attempts` (`0` = no lockout = critical fail) and `lockout_duration_min`. |
| **3. Complexity** | **15%** | Uppercase, lowercase, digit, special character flags, and `min_categories`. |
| **4. Expiration** | **10%** | `max_password_age_days` (`0` = no arbitrary rotation, aligned with NIST) and `min_password_age_days`. |
| **5. Reuse (History)** | **10%** | `password_history_count` vs `recommended_password_history_count` (`0` flags immediate reuse risk). |
| **6. Hygiene** | **10%** | `disallow_common` (breached dictionary screening), `disallow_username`, and `require_mfa`. |

* **Overall Score:**  
  `score = (length * 0.30) + (lockout * 0.25) + (complexity * 0.15) + (expiration * 0.10) + (reuse * 0.10) + (hygiene * 0.10)` (rounded to 1 decimal, clamped `0.0–100.0`).
* **Letter Grades:** `A+` (≥ 93), `A` (≥ 85), `B` (≥ 75), `C` (≥ 65), `D` (≥ 50), `F` (< 50).
* **Risk Levels:**
  * **Critical:** Any `CRITICAL` `FAIL` finding OR `overall_score < 50.0`
  * **High:** More than 1 `HIGH` `FAIL`/`WARNING` OR `overall_score < 70.0`
  * **Moderate:** `overall_score < 85.0`
  * **Low:** `overall_score >= 85.0` and no critical/multiple high issues.

---

## 6. Database Schema (All 9 Tables in `backend/models.py`)

| Table Name | Purpose |
| :--- | :--- |
| `users` | Staff accounts (`id`, `email`, `full_name`, `role`, `department`, `hashed_password`, `is_active`, `created_at`). |
| `policy_settings` | Saved policy profiles and sample presets (`weak`, `moderate`, `strong`). |
| `standard_definitions` | Benchmark baselines (`NIST_SP_800_63B`, `OWASP_ASVS`, `CIS_BENCHMARK`, `CUSTOM_ORG`). |
| `evaluation_reports` | Saved compliance results (`overall_compliance_score`, `grade_letter`, `risk_level`, `findings_json`, `scores_breakdown_json`, `policy_snapshot_json`). |
| `audit_logs` | Immutable activity trail (`action`, `details`, `user_name`, `user_role`, `ip_address`, `score_snapshot`, `timestamp`). |
| `active_policy` | Single-row (`id=1`) JSON configuration of the currently enforced live password policy. |
| `login_state` | Per-user brute-force lockout counters, `locked_until`, `password_changed_at`, `must_change_password`. |
| `password_history` | Historical BCrypt hashes per `user_id` to prevent password reuse. |
| `user_sessions` | Active JWT session IDs (`id` = `jti`, `user_id`, `expires_at`) for server-side revocation. |

---

## 7. Complete REST API Reference (`backend/main.py`)

Interactive OpenAPI/Swagger docs are served at **`/api/docs`** (`/docs` redirects to `/api/docs`; schema at `/api/openapi.json`).

* **Auth:** `POST /api/auth/login`, `GET /api/auth/me`, `POST /api/auth/logout`, `POST /api/auth/change-password`
* **Users (Admin):** `GET /api/users`, `POST /api/users`, `PUT /api/users/{user_id}`, `POST /api/users/seed-demo`
* **Standards:** `GET /api/standards`, `GET /api/standards/{standard_id}`, `PUT /api/standards/{standard_id}` (Admin)
* **Policies & Evaluation:** `GET /api/policies/active`, `PUT /api/policies/active` (Admin), `GET /api/policies/samples`, `POST /api/policies/evaluate` (Admin/Analyst), `POST /api/policies/import` (Admin/Analyst)
* **Reports & Dashboard:** `GET /api/reports`, `GET /api/reports/{report_id}`, `GET /api/reports/{report_id}/export-csv`, `GET /api/dashboard/stats`
* **Audit & Ops:** `GET /api/audit` (Admin/Auditor), `GET /api/health`, `GET /api/integrations/status`, `GET /api/keepalive`

---

## 8. Quick Defense Q&A Cheat Sheet

* **Q: How does Pydantic fit into the system?**  
  A: Defined in `backend/schemas.py`, Pydantic validates all incoming JSON payloads (types, required fields, numeric `Field` bounds) and powers `/api/docs`.
* **Q: Why use SHA-1 k-anonymity for Have I Been Pwned?**  
  A: Sending a plaintext password or full hash to an external API is unsafe. Sending only the first 5 hex characters of the SHA-1 hash lets the backend check for breaches locally without exposing the password.
* **Q: Why have an `Auditor` role if they can't edit policies?**  
  A: Principle of Least Privilege and Separation of Duties. Auditors and management need read-only access to dashboards, reports, CSV exports, and the Activity log without altering security policies or user accounts.
* **Q: What happens when a user logs out—can their old JWT still be used?**  
  A: No. Each JWT embeds a `jti` linked to `user_sessions`. Logging out deletes that row, so `get_current_user` immediately rejects the token with `401`.
