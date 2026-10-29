# #23 PasswordPolicy Checker

> **A Web-Based System for Evaluating Password Policy Compliance and Security Risks**  
> **Course:** System Administration and Maintenance – IT23/L (Code: 3493 • 7:30–9:30PM)  
> **Author:** Kristine Paula S. Coretico  
> **Unit:** Systems Administration and Security Unit  
> **Release Date:** October 26, 2026

---

## 🚀 Architectural Stack

* **Backend:** Python (FastAPI + SQLAlchemy)
* **Frontend:** React + Vite + HTML5/CSS3 + Chart.js
* **Database:** Supabase PostgreSQL (with automatic zero-config SQLite fallback)
* **Authentication:** JWT tokens with BCrypt password hashing & Role-Based Access Control (RBAC)

---

## ⚡ How to Run

### Option 1: One-Click Startup (Windows)
Double-click:
```powershell
start_all.bat
```
This automatically launches both the FastAPI backend and Vite React frontend in separate terminal windows.

---

### Option 2: Run Manually

#### Terminal 1 — FastAPI Backend:
```powershell
py -m uvicorn backend.main:app --reload --port 8000
```
Backend API will be available at: **http://localhost:8000** (Swagger documentation: **http://localhost:8000/docs**)

#### Terminal 2 — React + Vite Frontend:
```powershell
cd frontend
npm run dev
```
Open your browser to: **http://localhost:5173**

---

## 🔐 Default Seed Credentials

The system initializes with three pre-seeded user accounts:

| Role | Email | Password | Permissions |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@passwordpolicy.local` | `Admin@123456` | Manage users, configure standard limits, full audit view |
| **Security Analyst** | `analyst@passwordpolicy.local` | `Analyst@123456` | Evaluate policies, import CSV/JSON, compare, export reports |
| **Viewer** | `viewer@passwordpolicy.local` | `Viewer@123456` | View dashboard and saved reports (read-only) |

---

## 🛡️ The 5 Core Policy Checks

1. **Password Length:** Minimum length benchmark evaluation (short lengths < 8 flag critical failures).
2. **Password Complexity:** Diversity check across uppercase, lowercase, numbers, and symbols.
3. **Account Lockout:** Failed-attempt threshold and lockout duration defense against brute force.
4. **Password Expiration:** Evaluation of maximum and minimum password age against standard recommendations.
5. **Password Reuse (History):** Historical password retention depth (0 history flags immediate reuse risk).
6. **Defense-in-Depth:** Leaked/breached dictionary screening, username exclusion, and MFA enforcement.

---

## 🗄️ Supabase PostgreSQL Configuration

To link your live **Supabase** database:
1. Open [`backend/.env`](file:///c:/Users/Admin/Documents/4th%20Year/IT23/password-policy/backend/.env)
2. Paste your Supabase connection string:
   ```env
   DATABASE_URL=postgresql://postgres.[YOUR-PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
   ```
3. Restart the backend. SQLAlchemy will automatically create all tables in your Supabase PostgreSQL instance!
