# #23 PasswordPolicy Checker — Design Rationale & Paper Defense Guide

> **Reference Paper:** *Security Functions and Network Layout – 2nd Deliverables* (`CORETICO_IT23_2ndDeliverables.docx`)  
> **Project Title:** PasswordPolicy Checker: A Web-Based System for Evaluating Password Policy Compliance and Security Risks  
> **Course:** System Administration and Maintenance – IT23/L (Code: 3493 • 7:30–9:30 PM)  
> **Author:** Kristine Paula S. Coretico  

This document explains **why** every architectural, technical, security, user, and UI decision in the paper and codebase was chosen—so you can clearly defend *every part* of your system.

---

## 1. Why This Project? (Case Study & Problem Rationale)

### Why the 2021 Colonial Pipeline Ransomware Attack?
The paper grounds the system in the **May 7, 2021 Colonial Pipeline ransomware attack** (DarkSide cybercrime group, CISA & FBI Advisory AA21-131A):
* **Why it is the ideal case study:** The attackers did **not** exploit a zero-day software flaw. They entered using a **single leaked, reused password** on an **inactive VPN account** that had **no Multi-Factor Authentication (MFA)**, **no account lockout**, and **no automatic deactivation**. That single policy failure shut down 5,500 miles of fuel pipeline for 6 days and led to a 75-Bitcoin (~$4.4M) ransom.
* **How PasswordPolicy Checker directly addresses it:** Every core check in [`backend/compliance_engine.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/compliance_engine.py) maps 1-to-1 to those exact policy gaps:
  1. **Length & Complexity Checks** → Prevent easily cracked/guessed passwords.
  2. **Account Lockout Check (`<= 5` attempts)** → Stops automated brute-force and password-spraying logins.
  3. **Password History (`>= 5`) & Breached Dictionary Check** → Blocks password reuse and leaked passwords.
  4. **MFA & Lifecycle Checks** → Flags missing MFA and weak expiration/aging rules early.
  5. **Automated Scoring & Audit Logs** → Gives IT teams a clear `0–100` score, remediation steps, and a permanent audit trail before attackers can exploit weak settings.

### Why Privacy-by-Design (Evaluate Rules, Never User Passwords)?
* **Rationale:** Storing or collecting real user passwords to "audit" them creates a massive new target (a honeypot of plaintext credentials). By evaluating **policy configuration parameters** (or JSON/CSV exports from AD GPO / Linux PAM / IAM) instead of user passwords, the system delivers full compliance visibility with **zero exposure of end-user credentials**.

---

## 2. Why These Target Users & RBAC Roles?

### Why These 5 Target User Groups?
1. **System Administrators:** Configure OS/directory password policies (Active Directory, Linux PAM) and need a fast way to verify settings before deployment.
2. **IT Security Officers / Cybersecurity Analysts:** Audit organizational posture against NIST/OWASP/CIS, compare policy revisions, and produce remediation plans.
3. **IT Auditors & Compliance Officers:** Need verifiable, read-only evidence (reports, CSV/PDF exports, immutable audit logs) without risking accidental policy changes.
4. **Educational Institutions (IT Departments):** Universities and schools manage thousands of student/staff accounts and need standardized baselines on limited budgets.
5. **IT Students, Educators, and Trainers:** Provides a hands-on, visual way to learn how NIST SP 800-63B, OWASP ASVS, and CIS Benchmarks translate into concrete rules and scores.

### Why the 3-Role RBAC Model (`Administrator`, `Security Analyst`, `Auditor`)?
* **Separation of Duties & Principle of Least Privilege:**
  * **Administrator** (`require_admin`): Owns system governance—user accounts, RBAC roles, benchmark thresholds, live policy activation (`PUT /api/policies/active`), and full audit log visibility.
  * **Security Analyst** (`require_analyst_or_admin`): Owns day-to-day technical evaluation—creating/importing `.json`/`.csv` policies in **Policy editor**, running compliance checks, reviewing findings, comparing reports, and exporting CSV/PDF reports. **Crucially, an Analyst cannot manage users, activate live policies, edit benchmark thresholds, or view the Activity log.**
  * **Auditor (Read-Only)** (`require_auditor_or_admin`, normalizing legacy `"Viewer"`): Can inspect dashboards, historical reports, CSV exports, and the `Activity log`, **without** any write/modify permissions on policies, standards, or users. This ensures audit independence.

#### Why Have a Separate **Security Analyst** Instead of Letting the **Administrator** Do Everything?
1. **Least Privilege (Blast-Radius Reduction):** A real IT/security team shouldn't hand out full `Administrator` credentials (which can create users, reset passwords, and change live policies) just to run policy evaluations. If an Analyst's account is compromised, the attacker cannot hijack user accounts or weaken system-wide benchmarks.
2. **Checks & Balances (Preventing Benchmark Tampering):** Because Analysts **cannot** edit `Benchmarks` (`PUT /api/standards/{id}`), an Analyst cannot lower the passing bar (e.g., changing `recommended_min_length` from `12` to `6`) just to make a weak policy look compliant. Only Administrators control the reference thresholds, and every change is logged in `audit_logs`.
3. **Operational Scalability:** Multiple Security Analysts can import, test, and compare department policies at the same time without needing Admin access.

---

## 3. Why This Technology Stack? (Frontend, Backend, Security & DB)

### Frontend: Why React 19 + Vite 8 + Chart.js + Custom CSS?
* **React 19:** Component-based architecture cleanly separates each role/workflow (`Dashboard.jsx`, `PolicyEvaluator.jsx`, `EvaluationReportView.jsx`, `StandardsManager.jsx`, `UserManagement.jsx`, `AuditLogsView.jsx`) and manages role-aware routing in [`frontend/src/App.jsx`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/App.jsx).
* **Vite 8:** Near-instant hot module replacement (HMR) during development and fast, lightweight static bundle output (`frontend/dist`) for Vercel deployment.
* **Chart.js (`react-chartjs-2`):** Lightweight, responsive data visualization for compliance score trends and overview metrics without heavy BI dependencies.
* **Custom CSS (`index.css`) instead of a heavy UI kit:** Keeps bundle size small, eliminates unused framework styles, and gives exact control over print/PDF styling and semantic security badges.

### Backend: Why Python + FastAPI + Pydantic + SQLAlchemy?
* **Python:** Readable, widely taught in IT/cybersecurity courses, and has first-class cryptography and data-parsing standard libraries.
* **FastAPI:** High-performance ASGI framework with native dependency injection (`Depends(...)`), which makes RBAC guards (`require_admin`, `require_analyst_or_admin`, `require_auditor_or_admin`) clean and impossible to forget on protected routes, plus automatic interactive **OpenAPI/Swagger docs at `/api/docs`**.
* **Pydantic (`backend/schemas.py`):** Enforces strict type checking and numeric boundaries (e.g., `Field(ge=..., le=...)`) at the API edge before bad data ever reaches the compliance engine or database.
* **SQLAlchemy 2.x ORM (`backend/models.py`):** Abstracts SQL so the exact same Python models run seamlessly on **SQLite** locally and **Supabase PostgreSQL** in production.

### Security Libraries & Integrations: Why BCrypt, PyJWT + Sessions, and HIBP?
* **BCrypt (`bcrypt` directly in [`backend/auth.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/auth.py)):** Adaptive, per-password salted hashing designed to resist GPU brute-force attacks. Enforces BCrypt's 72-byte UTF-8 boundary explicitly so passwords are never silently truncated.
* **PyJWT + Server-Side `user_sessions` Table:** Pure stateless JWTs cannot be revoked before expiration. By embedding a `jti` in each `HS256` JWT and storing it in `user_sessions`, the system gets fast token auth **plus** immediate server-side revocation on `POST /api/auth/logout`.
* **Have I Been Pwned (HIBP) SHA-1 k-Anonymity ([`backend/policy_enforcement.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/policy_enforcement.py)):** Sending a plaintext password or full hash to a third party is unsafe. Sending only the **first 5 hex characters** of the SHA-1 hash lets the backend check millions of breached passwords locally with zero password exposure, and a `2.5s` timeout ensures graceful degradation if offline.

### Database & Cloud Infrastructure: Why SQLite + Supabase PostgreSQL + Vercel + GitHub Actions?
* **Dual-Mode Database ([`backend/database.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/database.py)):**
  * **SQLite (`passwordpolicy.db`)** locally gives zero-configuration offline setup for development and live classroom demos.
  * **Supabase PostgreSQL** in production provides a managed, SSL-encrypted cloud RDBMS.
  * **Fail-Closed Guard:** If `VERCEL` or `RENDER` is detected without `DATABASE_URL` (or `JWT_SECRET`), the app raises `RuntimeError` rather than silently falling back to ephemeral local SQLite or weak dev secrets.
* **Vercel (`vercel.json`):** Serves both the static React SPA and the FastAPI serverless function (`api/index.py`) from one unified origin, avoiding cross-origin deployment headaches.
* **GitHub Actions Keepalive (`.github/workflows/supabase-keepalive.yml`):** Free-tier Supabase projects pause after inactivity; a scheduled workflow pings `/api/keepalive` (protected by `X-Keepalive-Token` and `secrets.compare_digest`) 4 times daily to query `standard_definitions` and keep the database warm.

---

## 4. Why the UI & Visual Design Were Built This Way

* **Color System ([`frontend/src/index.css`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/index.css)):**
  * **Light Editorial Surfaces (`#f7f5f7` app background, `#ffffff` cards):** Designed for readability during long audit reviews and clean Print/PDF report generation (unlike dark-mode-only dashboards that waste ink or lose contrast when printed).
  * **Plum / Burgundy Primary (`#632d4d`):** Gives the workspace an authoritative, institutional identity distinct from generic blue templates.
  * **Semantic Status Tokens:** High-contrast, color-coded badges immediately communicate risk without reading paragraphs:
    * **Pass (`#196b50` on `#e7f6ef`)**
    * **Warning (`#8b5911` on `#fff4dc`)**
    * **Fail (`#ad3153` on `#fdebf0`)**
    * **Critical (`#a01f43` on `#f8dee7`)**
* **Typography (`Outfit` headings + `Inter` body):** Crisp geometric headings paired with highly legible UI/tabular text for scores, IP addresses, and timestamps.
* **Layout & Workflow Ergonomics (`Navbar.jsx` & `EvaluationReportView.jsx`):**
  * **Two-section Sidebar (`WORKSPACE` vs `ADMINISTRATION`):** Separates daily analyst tasks (Overview, Policy editor, Reports, Compare reports) from governance tasks (Benchmarks, Users, Activity log).
  * **Actionable Report View:** Displays the headline score (`0–100%`), letter grade (`A+`–`F`), risk badge, 6-dimension progress bars, filterable findings (`All` / `Fails` / `Warnings` / `Pass`), one-click **Export CSV**, and **Print / Save PDF** for formal compliance submissions.

---

## 5. Why the Code & Architecture Are Structured This Way

* **3-Tier Separation of Concerns:**
  * Tier 1 (`frontend/`) handles presentation and client state only—never trust-critical security decisions.
  * Tier 2 (`backend/`) centralizes all validation (`schemas.py`), authentication/RBAC (`auth.py`), live enforcement (`policy_enforcement.py`), and scoring (`compliance_engine.py`).
  * Tier 3 (`models.py` + `database.py`) isolates persistence across **9 normalized tables**.
* **Why Weighted 6-Dimension Scoring (`30 / 25 / 15 / 10 / 10 / 10`)?**
  * **Length (30%) + Lockout (25%) = 55%** of the total score because short passwords (offline GPU cracking) and missing lockouts (online brute-force, as in Colonial Pipeline) are the two fastest paths to account compromise.
  * **Complexity (15%)** balances keyspace diversity with NIST SP 800-63B's warning against rigid composition rules that cause predictable user patterns.
  * **Expiration (10%), Reuse (10%), and Hygiene (10%)** capture lifecycle and defense-in-depth controls (e.g., NIST recommends `0` arbitrary periodic rotation, while penalizing missing password history or missing MFA/breach screening).
* **Why Immutable `audit_logs` (`record_audit` in `backend/main.py`)?**
  * Every security-sensitive event (login success/failure, logout, password change, user creation/update, benchmark update, policy evaluation, live policy activation) is written with actor name, role, client IP, score snapshot, and UTC timestamp—and no API endpoint exists to edit or delete audit rows, preserving forensic integrity.

---

## 6. Why Each Core Feature Exists (Policy Editor, Benchmarks, Compare Reports & "Why Not Just Google It?")

### Why Not Just Look It Up on Google?
A common question is: *"Why build a whole system when an admin can just Google 'is 8 characters good enough' or read NIST/OWASP online?"*
1. **Google gives static articles, not automated, repeatable audits:** Reading a 100-page NIST PDF or blog post does not automatically inspect your Active Directory GPO, Linux PAM, or IAM `.json`/`.csv` export, calculate a weighted `0–100` score, and pinpoint every exact gap.
2. **Standards conflict and change by context:** Google results often give outdated advice (like forcing 30-day password expiration, which NIST SP 800-63B now discourages). Having **NIST SP 800-63B**, **OWASP ASVS v4.0**, **CIS Benchmark v8**, and a **Custom Org Baseline** side by side in one engine prevents human misinterpretation.
3. **Google cannot produce audit evidence or accountability:** IT auditors and management do not accept "I Googled it and it looked fine." They require timestamped **Evaluation Reports**, **CSV/PDF exports**, **side-by-side comparisons**, and an **immutable Activity log** showing *who* checked *which* policy, *when*, and *what changed*.
4. **Google doesn't enforce or test your live rules:** PasswordPolicy Checker also lets Administrators activate a policy (`active_policy`) and test live enforcement—including lockout, password history, and **HIBP SHA-1 k-anonymity** breached-password screening.

### Why the **Policy Editor** ([PolicyEvaluator.jsx](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/components/PolicyEvaluator.jsx))?
* **Purpose:** It is the structured workspace where an **Administrator** or **Security Analyst** enters, loads (`weak`/`moderate`/`strong` presets), or imports (`.json`/`.csv`) an organization's *password policy rules*—never real user passwords.
* **Why you (the admin/analyst) enter the rules:** Every organization's servers and identity providers have different configurations. You supply the rules so the system can either **Evaluate** them against a benchmark (Audit Mode) or **Activate** them for live enforcement in `active_policy` (Admin-only).

### Why **Benchmarks** ([StandardsManager.jsx](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/components/StandardsManager.jsx))?
* **What "Benchmark" means:** A **Benchmark** is the official "answer key" or reference baseline (**NIST SP 800-63B**, **OWASP ASVS v4.0**, **CIS Security Benchmark v8**, or **Custom Organization Baseline**) stored in `standard_definitions`.
* **How it works:** When you evaluate a policy, `evaluate_policy()` reads the chosen benchmark's thresholds from the database and grades your policy against them. Administrators can click **Edit Limits** (`PUT /api/standards/{id}`) to tailor thresholds to institutional needs, with every change recorded in `audit_logs`.

### Why **Compare Reports** ([PolicyCompare.jsx](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/frontend/src/components/PolicyCompare.jsx))?
* **Connection to Colonial Pipeline & Continuous Compliance:** In the Colonial Pipeline incident, weak VPN password rules went unchecked. Fixing a policy requires **before-and-after proof**:
  1. *Before:* Evaluate a weak legacy policy (no lockout, no MFA, no history) → Grade `F`, Critical Risk.
  2. *After:* Harden the policy (lockout `<= 5`, history `>= 5`, MFA, length `>= 12`) and re-evaluate.
  3. *Compare Reports:* Displays both reports side by side (Score, Grade, Risk Level, Benchmark, and every rule setting) so auditors and management can verify remediation—or compare the *same* policy against two different benchmarks (e.g., NIST vs. CIS).

---

## 7. Possible Panel & Defense Questions (Q&A Cheat Sheet)

### Topic & Case Study Questions
1. **Q: Why did you choose the 2021 Colonial Pipeline attack instead of a newer breach?**  
   **A:** Because Colonial Pipeline is a textbook, verified example (CISA & FBI AA21-131A) where attackers didn't use a zero-day exploit—they used a **single leaked, reused password on an inactive VPN account with no MFA and no lockout**. Every check in our system (length, lockout, history, breached-dictionary screening, MFA) directly prevents that exact attack path.
2. **Q: Why make a web system when someone can just Google if a password policy is good enough?**  
   **A:** Googling gives generic advice and doesn't parse `.json`/`.csv` policy exports, compute a weighted `0–100` compliance score across 6 dimensions, compare before-and-after policies, export formal CSV/PDF audit reports, or maintain an immutable audit log for IT auditors.
3. **Q: Does your system store or check real users' passwords?**  
   **A:** **No.** For policy evaluation, it only inspects *policy settings* (e.g., `min_length = 12`, `max_failed_attempts = 5`). The only passwords hashed in the database are the system's own staff accounts (`users` and `password_history` using salted BCrypt).

### Architecture, Code & Security Questions
4. **Q: Why use a 3-Tier Architecture?**  
   **A:** It separates presentation (`React + Vite` on Vercel), security/business logic (`FastAPI + Pydantic + Compliance Engine`), and persistence (`SQLAlchemy` → `SQLite` / `Supabase PostgreSQL`), ensuring the client never makes trust-critical security decisions.
5. **Q: Why are Length (30%) and Lockout (25%) weighted the highest in `compliance_engine.py`?**  
   **A:** Together they represent **55%** of the score because short passwords fall to offline GPU cracking and missing lockouts allow online brute-force/password spraying (like Colonial Pipeline).
6. **Q: Why does NIST SP 800-63B in your system recommend `0` for `max_password_age_days`?**  
   **A:** Modern NIST guidance discourages arbitrary periodic rotation (e.g., every 30–60 days) because it causes users to pick predictable patterns (like `Spring2026!`). Instead, NIST emphasizes longer passwords, MFA, and breached-password screening.
7. **Q: How does your Have I Been Pwned (HIBP) check protect user privacy?**  
   **A:** Via **SHA-1 k-Anonymity** (`check_pwned_password()` in [`backend/policy_enforcement.py`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/policy_enforcement.py)). The server hashes the password locally, sends only the **first 5 hex characters** of the SHA-1 hash to HIBP, and checks the matching suffix list locally. The full password or full hash never leaves the server.
8. **Q: Why store JWT session IDs (`jti`) in `user_sessions` instead of using pure stateless JWTs?**  
   **A:** Pure stateless JWTs remain valid until expiration even after logout. Storing `jti` in `user_sessions` allows **immediate server-side revocation** when a user logs out (`POST /api/auth/logout`).
9. **Q: What happens if `DATABASE_URL` or `JWT_SECRET` is missing in production (Vercel)?**  
   **A:** The app **fails closed** (`RuntimeError` in `backend/database.py` and `backend/auth.py`) rather than silently falling back to local SQLite or a hardcoded dev secret.

### Users, RBAC & UI Questions
10. **Q: Why have three roles (`Administrator`, `Security Analyst`, `Auditor`)?**  
    **A:** To enforce **Least Privilege** and **Separation of Duties**. Analysts evaluate policies without being able to alter benchmarks or user accounts; Auditors can inspect reports, exports, and the Activity log read-only without modifying anything; only Administrators manage users, benchmarks, and live policy activation.
11. **Q: What does the Security Analyst do, and why can't the Administrator just do all of it?**  
    **A:** The Security Analyst handles day-to-day policy testing, JSON/CSV imports, scoring, and report comparisons. Separating this from the Administrator enforces **Least Privilege** (analysts don't need user-management or live-policy power) and **Checks & Balances** (an analyst cannot lower benchmark thresholds in `Benchmarks` to fake a passing score).
12. **Q: Why use a light editorial UI (`#f7f5f7` / `#ffffff` with `#632d4d` plum) instead of a dark hacker theme?**  
    **A:** Light surfaces maximize readability during long compliance reviews and ensure **Print / Save PDF** reports print cleanly without dark-background ink waste or contrast loss.
13. **Q: What is the purpose of the GitHub Actions keepalive workflow?**  
    **A:** Supabase Free-tier projects pause after periods of inactivity. The scheduled workflow pings `/api/keepalive` (secured with `X-Keepalive-Token`) 4 times a day to run a lightweight `SELECT` on `standard_definitions` and keep the cloud database responsive.
