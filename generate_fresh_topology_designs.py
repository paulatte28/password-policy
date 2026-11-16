import os
import subprocess
from PIL import Image, ImageChops

DOWNLOADS = r"c:\Users\Admin\Downloads"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ==============================================================================
# DESIGN A: 3-TIER HIERARCHICAL WEB ARCHITECTURE (CLEAN VERTICAL LAYOUT)
# ==============================================================================
SVG_DESIGN_A = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 620" width="980" height="620" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <marker id="arrow-down" viewBox="0 0 10 10" refX="5" refY="7" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 1 0 L 5 8 L 9 0 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-both-v" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 5 0 L 8 4 L 2 4 z M 5 10 L 8 6 L 2 6 z" fill="#2563eb"/>
    </marker>
    <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Title Banner -->
  <rect x="20" y="15" width="940" height="50" rx="8" fill="#0f172a"/>
  <text x="40" y="46" font-size="16" font-weight="800" fill="#38bdf8" letter-spacing="0.5">3-TIER CLIENT-SERVER ARCHITECTURE TOPOLOGY</text>
  <text x="560" y="46" font-size="13" font-weight="600" fill="#94a3b8">#23 PasswordPolicy Checker</text>

  <!-- ================= TIER 1: PRESENTATION TIER (CLIENTS) ================= -->
  <g transform="translate(20, 80)">
    <rect x="0" y="0" width="940" height="135" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="6,4"/>
    <text x="25" y="24" font-size="13" font-weight="800" fill="#0f172a" letter-spacing="0.5">TIER 1: PRESENTATION LAYER (CLIENT WORKSTATIONS)</text>
    <text x="550" y="24" font-size="11.5" font-weight="600" fill="#64748b">Web Browsers (Chrome / Edge / Firefox)</text>

    <!-- Admin Card -->
    <g transform="translate(25, 36)" filter="url(#card-shadow)">
      <rect x="0" y="0" width="280" height="82" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="82" rx="3" fill="#10b981"/>
      <text x="18" y="24" font-size="14" font-weight="700" fill="#0f172a">Administrator Client</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• Manage user accounts &amp; RBAC roles</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• Customize benchmark standards (NIST/OWASP)</text>
      <text x="18" y="74" font-size="11" fill="#64748b">• Activate policy for runtime enforcement</text>
    </g>

    <!-- Analyst Card -->
    <g transform="translate(330, 36)" filter="url(#card-shadow)">
      <rect x="0" y="0" width="280" height="82" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="82" rx="3" fill="#0284c7"/>
      <text x="18" y="24" font-size="14" font-weight="700" fill="#0f172a">Security Analyst Client</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• Input &amp; import password policies (CSV/JSON)</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• Run compliance checks &amp; risk scoring</text>
      <text x="18" y="74" font-size="11" fill="#64748b">• Compare policies &amp; export audit reports</text>
    </g>

    <!-- Viewer Card -->
    <g transform="translate(635, 36)" filter="url(#card-shadow)">
      <rect x="0" y="0" width="280" height="82" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="82" rx="3" fill="#8b5cf6"/>
      <text x="18" y="24" font-size="14" font-weight="700" fill="#0f172a">Auditor / Viewer Client</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• Read-only access to dashboard overview</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• View compliance scores &amp; letter grades</text>
      <text x="18" y="74" font-size="11" fill="#64748b">• Review published evaluation reports</text>
    </g>
  </g>

  <!-- Connecting Bus between Tier 1 and Tier 2 -->
  <line x1="490" y1="215" x2="490" y2="252" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-down)"/>
  <rect x="360" y="222" width="260" height="22" rx="4" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
  <text x="490" y="237" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">HTTP / HTTPS (REST API &amp; JWT Bearer Auth)</text>

  <!-- ================= TIER 2: APPLICATION & LOGIC TIER ================= -->
  <g transform="translate(20, 255)">
    <rect x="0" y="0" width="940" height="175" rx="10" fill="#f0f7ff" stroke="#3b82f6" stroke-width="2" filter="url(#card-shadow)"/>
    
    <rect x="0" y="0" width="940" height="34" rx="10" fill="#1e40af"/>
    <rect x="0" y="24" width="940" height="10" fill="#1e40af"/>
    <text x="25" y="23" font-size="13" font-weight="800" fill="#ffffff" letter-spacing="0.5">TIER 2: APPLICATION &amp; LOGIC LAYER (FASTAPI BACKEND &amp; REACT FRONTEND)</text>
    <text x="730" y="23" font-size="11.5" font-weight="700" fill="#bfdbfe">Host: Localhost / Vercel Edge</text>

    <!-- Submodule 1: Frontend SPA -->
    <g transform="translate(25, 48)">
      <rect x="0" y="0" width="205" height="110" rx="6" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
      <text x="14" y="22" font-size="12.5" font-weight="700" fill="#0f172a">React + Vite Frontend</text>
      <text x="14" y="40" font-size="10.5" fill="#64748b">• Single Page Application (SPA)</text>
      <text x="14" y="56" font-size="10.5" fill="#64748b">• Chart.js Score Visualizations</text>
      <text x="14" y="72" font-size="10.5" fill="#64748b">• Form Validation &amp; CSV/JSON Import</text>
      <text x="14" y="92" font-size="10" font-weight="700" fill="#0284c7">Port 5173 (Dev) / Static Asset</text>
    </g>

    <!-- Submodule 2: Compliance Engine -->
    <g transform="translate(250, 48)">
      <rect x="0" y="0" width="215" height="110" rx="6" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
      <text x="14" y="22" font-size="12.5" font-weight="700" fill="#0f172a">Compliance Engine</text>
      <text x="14" y="40" font-size="10.5" fill="#64748b">• Evaluates Length, Complexity</text>
      <text x="14" y="56" font-size="10.5" fill="#64748b">• Lockout, Expiration &amp; History</text>
      <text x="14" y="72" font-size="10.5" fill="#64748b">• Scores against NIST / OWASP</text>
      <text x="14" y="92" font-size="10" font-weight="700" fill="#16a34a">Outputs: 0-100 Score &amp; Grades</text>
    </g>

    <!-- Submodule 3: Auth & Security Guard -->
    <g transform="translate(485, 48)">
      <rect x="0" y="0" width="215" height="110" rx="6" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
      <text x="14" y="22" font-size="12.5" font-weight="700" fill="#0f172a">Authentication &amp; RBAC</text>
      <text x="14" y="40" font-size="10.5" fill="#64748b">• BCrypt Password Hashing ($2b$)</text>
      <text x="14" y="56" font-size="10.5" fill="#64748b">• PyJWT Cryptographic Sessions</text>
      <text x="14" y="72" font-size="10.5" fill="#64748b">• Role Dependency Protection</text>
      <text x="14" y="92" font-size="10" font-weight="700" fill="#9333ea">Defensive Lockout Controller</text>
    </g>

    <!-- Submodule 4: Audit & Export Service -->
    <g transform="translate(720, 48)">
      <rect x="0" y="0" width="195" height="110" rx="6" fill="#ffffff" stroke="#bfdbfe" stroke-width="1.5"/>
      <text x="14" y="22" font-size="12.5" font-weight="700" fill="#0f172a">Audit &amp; Reporting</text>
      <text x="14" y="40" font-size="10.5" fill="#64748b">• Immutable Audit Trail Logging</text>
      <text x="14" y="56" font-size="10.5" fill="#64748b">• Policy Comparison Matrix</text>
      <text x="14" y="72" font-size="10.5" fill="#64748b">• PDF &amp; CSV Audit Exports</text>
      <text x="14" y="92" font-size="10" font-weight="700" fill="#d97706">Port 8000 (FastAPI ASGI)</text>
    </g>
  </g>

  <!-- Connecting Bus between Tier 2 and Tier 3 -->
  <line x1="490" y1="430" x2="490" y2="472" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-down)"/>
  <rect x="350" y="440" width="280" height="22" rx="4" fill="#eff6ff" stroke="#bfdbfe" stroke-width="1"/>
  <text x="490" y="455" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">SQLAlchemy ORM (Encrypted Pool / Port 5432)</text>

  <!-- ================= TIER 3: DATA PERSISTENCE TIER ================= -->
  <g transform="translate(20, 475)">
    <rect x="0" y="0" width="940" height="130" rx="10" fill="#f8fafc" stroke="#10b981" stroke-width="2" filter="url(#card-shadow)"/>
    
    <rect x="0" y="0" width="940" height="32" rx="10" fill="#047857"/>
    <rect x="0" y="22" width="940" height="10" fill="#047857"/>
    <text x="25" y="22" font-size="13" font-weight="800" fill="#ffffff" letter-spacing="0.5">TIER 3: DATA STORAGE LAYER (RELATIONAL PERSISTENCE)</text>
    <text x="680" y="22" font-size="11.5" font-weight="700" fill="#a7f3d0">Zero Raw Passwords Stored</text>

    <!-- DB Storage 1: Local SQLite -->
    <g transform="translate(25, 42)">
      <rect x="0" y="0" width="430" height="74" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="16" y="22" font-size="13" font-weight="700" fill="#0f172a">Local Development: SQLite Database</text>
      <text x="16" y="40" font-size="11" fill="#64748b">• File: passwordpolicy.db (Local disk storage)</text>
      <text x="16" y="56" font-size="11" fill="#64748b">• Used for offline development, local unit testing, and demos</text>
      <text x="16" y="68" font-size="9.5" font-weight="700" fill="#0284c7">Local Connection: sqlite:///./passwordpolicy.db</text>
    </g>

    <!-- DB Storage 2: Cloud Supabase PostgreSQL -->
    <g transform="translate(485, 42)">
      <rect x="0" y="0" width="430" height="74" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <text x="16" y="22" font-size="13" font-weight="700" fill="#0f172a">Cloud Production: Supabase PostgreSQL</text>
      <text x="16" y="40" font-size="11" fill="#64748b">• Managed AWS Cloud Relational Database (Connection Pooler)</text>
      <text x="16" y="56" font-size="11" fill="#64748b">• Tables: users, policy_settings, standard_definitions, evaluation_reports, audit_logs</text>
      <text x="16" y="68" font-size="9.5" font-weight="700" fill="#16a34a">SSL Mode: require • Port 6543 / 5432</text>
    </g>
  </g>
</svg>
'''

# ==============================================================================
# DESIGN B: CENTRALIZED STAR TOPOLOGY (HUB AND SPOKE)
# ==============================================================================
SVG_DESIGN_B = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 600" width="960" height="600" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <filter id="hub-shadow" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#1e3a8a" flood-opacity="0.15"/>
    </filter>
    <filter id="node-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="spoke-arr-in" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="spoke-arr-out" viewBox="0 0 10 10" refX="3" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 9 1 L 0 5 L 9 9 z" fill="#2563eb"/>
    </marker>
  </defs>

  <!-- Title Header -->
  <rect x="25" y="15" width="910" height="46" rx="8" fill="#0f172a"/>
  <text x="45" y="44" font-size="16" font-weight="800" fill="#38bdf8" letter-spacing="0.5">CENTRALIZED STAR NETWORK TOPOLOGY (CLIENT-SERVER HUB)</text>
  <text x="640" y="44" font-size="13" font-weight="600" fill="#94a3b8">#23 PasswordPolicy Checker</text>

  <!-- Spoke Connecting Lines from Center Hub (480, 310) -->
  <!-- Line to Admin (200, 150) -->
  <line x1="480" y1="310" x2="230" y2="150" stroke="#3b82f6" stroke-width="3" stroke-dasharray="6,4"/>
  <!-- Line to Analyst (180, 330) -->
  <line x1="480" y1="310" x2="230" y2="330" stroke="#3b82f6" stroke-width="3"/>
  <!-- Line to Viewer (220, 500) -->
  <line x1="480" y1="310" x2="250" y2="490" stroke="#3b82f6" stroke-width="3" stroke-dasharray="6,4"/>
  <!-- Line to Database (480, 500) -->
  <line x1="480" y1="310" x2="480" y2="475" stroke="#10b981" stroke-width="4"/>
  <!-- Line to Cloud / Vercel (740, 170) -->
  <line x1="480" y1="310" x2="720" y2="180" stroke="#8b5cf6" stroke-width="3" stroke-dasharray="6,4"/>
  <!-- Line to Standards (740, 430) -->
  <line x1="480" y1="310" x2="720" y2="420" stroke="#f59e0b" stroke-width="3" stroke-dasharray="6,4"/>

  <!-- ================= CENTRAL HUB: APPLICATION SERVER ================= -->
  <g transform="translate(355, 230)" filter="url(#hub-shadow)">
    <!-- Main Center Circle/Rounded Rect -->
    <rect x="0" y="0" width="250" height="155" rx="16" fill="#1e3a8a" stroke="#60a5fa" stroke-width="2.5"/>
    
    <text x="125" y="28" text-anchor="middle" font-size="14" font-weight="800" fill="#ffffff" letter-spacing="0.5">CENTRAL SERVER HUB</text>
    <text x="125" y="46" text-anchor="middle" font-size="12" font-weight="700" fill="#93c5fd">FastAPI Backend + React UI</text>

    <!-- Inner feature box -->
    <rect x="15" y="56" width="220" height="85" rx="8" fill="#0f172a" opacity="0.8"/>
    <text x="25" y="74" font-size="10.5" font-weight="600" fill="#e2e8f0">• Compliance Scoring Engine</text>
    <text x="25" y="90" font-size="10.5" font-weight="600" fill="#e2e8f0">• JWT Role-Based Access Control</text>
    <text x="25" y="106" font-size="10.5" font-weight="600" fill="#e2e8f0">• BCrypt Hashes &amp; Lockout Guard</text>
    <text x="25" y="122" font-size="10.5" font-weight="600" fill="#e2e8f0">• Immutable Audit Trail Logger</text>
    <text x="125" y="136" text-anchor="middle" font-size="9" font-weight="700" fill="#38bdf8">Uvicorn ASGI • Port 8000</text>
  </g>

  <!-- ================= SPOKE 1: ADMIN CLIENT (Top Left) ================= -->
  <g transform="translate(30, 95)" filter="url(#node-shadow)">
    <rect x="0" y="0" width="200" height="95" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2"/>
    <rect x="0" y="0" width="200" height="26" rx="10" fill="#dcfce7"/>
    <rect x="0" y="18" width="200" height="8" fill="#dcfce7"/>
    <text x="100" y="18" text-anchor="middle" font-size="12" font-weight="800" fill="#166534">ADMINISTRATOR CLIENT</text>
    
    <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">• Account &amp; Role Management</text>
    <text x="14" y="60" font-size="10.5" fill="#64748b">• Benchmark Limit Configuration</text>
    <text x="14" y="76" font-size="10.5" fill="#64748b">• Runtime Policy Activation</text>
    <text x="14" y="88" font-size="9.5" font-weight="600" fill="#059669">Web Browser • Full Access</text>
  </g>

  <!-- ================= SPOKE 2: ANALYST CLIENT (Mid Left) ================= -->
  <g transform="translate(30, 275)" filter="url(#node-shadow)">
    <rect x="0" y="0" width="200" height="95" rx="10" fill="#ffffff" stroke="#0284c7" stroke-width="2"/>
    <rect x="0" y="0" width="200" height="26" rx="10" fill="#e0f2fe"/>
    <rect x="0" y="18" width="200" height="8" fill="#e0f2fe"/>
    <text x="100" y="18" text-anchor="middle" font-size="12" font-weight="800" fill="#0369a1">SECURITY ANALYST CLIENT</text>

    <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">• Policy Testing &amp; Import</text>
    <text x="14" y="60" font-size="10.5" fill="#64748b">• NIST / OWASP Compliance Check</text>
    <text x="14" y="76" font-size="10.5" fill="#64748b">• Comparative Audit Reports</text>
    <text x="14" y="88" font-size="9.5" font-weight="600" fill="#0284c7">Web Browser • Evaluator</text>
  </g>

  <!-- ================= SPOKE 3: VIEWER CLIENT (Bottom Left) ================= -->
  <g transform="translate(45, 450)" filter="url(#node-shadow)">
    <rect x="0" y="0" width="200" height="95" rx="10" fill="#ffffff" stroke="#8b5cf6" stroke-width="2"/>
    <rect x="0" y="0" width="200" height="26" rx="10" fill="#f3e8ff"/>
    <rect x="0" y="18" width="200" height="8" fill="#f3e8ff"/>
    <text x="100" y="18" text-anchor="middle" font-size="12" font-weight="800" fill="#6b21a8">AUDITOR / VIEWER CLIENT</text>

    <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">• Read-Only Dashboard</text>
    <text x="14" y="60" font-size="10.5" fill="#64748b">• Compliance Grades &amp; Radar</text>
    <text x="14" y="76" font-size="10.5" fill="#64748b">• Historical Log Inspection</text>
    <text x="14" y="88" font-size="9.5" font-weight="600" fill="#7c3aed">Web Browser • Read-Only</text>
  </g>

  <!-- ================= SPOKE 4: DATABASE SERVER (Bottom Center) ================= -->
  <g transform="translate(360, 460)" filter="url(#node-shadow)">
    <rect x="0" y="0" width="240" height="105" rx="10" fill="#ffffff" stroke="#10b981" stroke-width="2"/>
    <rect x="0" y="0" width="240" height="26" rx="10" fill="#d1fae5"/>
    <rect x="0" y="18" width="240" height="8" fill="#d1fae5"/>
    <text x="120" y="18" text-anchor="middle" font-size="12" font-weight="800" fill="#065f46">RELATIONAL DATABASE TIER</text>

    <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">• SQLite (passwordpolicy.db) [Local]</text>
    <text x="14" y="60" font-size="10.5" font-weight="700" fill="#0f172a">• Supabase PostgreSQL [Cloud AWS]</text>
    <text x="14" y="76" font-size="9.5" fill="#64748b">Schemas: users, policy_settings,</text>
    <text x="14" y="88" font-size="9.5" fill="#64748b">standard_definitions, reports, audit_logs</text>
    <text x="14" y="100" font-size="9" font-weight="700" fill="#059669">SQLAlchemy ORM Connection Pool</text>
  </g>

  <!-- ================= SPOKE 5: CLOUD HOSTING (Top Right) ================= -->
  <g transform="translate(720, 110)" filter="url(#node-shadow)">
    <rect x="0" y="0" width="210" height="95" rx="10" fill="#ffffff" stroke="#8b5cf6" stroke-width="2"/>
    <rect x="0" y="0" width="210" height="26" rx="10" fill="#ede9fe"/>
    <rect x="0" y="18" width="210" height="8" fill="#ede9fe"/>
    <text x="105" y="18" text-anchor="middle" font-size="12" font-weight="800" fill="#5b21b6">CLOUD DEPLOYMENT</text>

    <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">• Vercel Cloud Platform</text>
    <text x="14" y="60" font-size="10.5" fill="#64748b">  password-policy1.vercel.app</text>
    <text x="14" y="76" font-size="10.5" fill="#64748b">• Serverless Edge Routing</text>
    <text x="14" y="88" font-size="9.5" font-weight="600" fill="#7c3aed">GitHub Actions Keepalive</text>
  </g>

  <!-- ================= SPOKE 6: STANDARDS REGISTRY (Mid/Bottom Right) ================= -->
  <g transform="translate(720, 360)" filter="url(#node-shadow)">
    <rect x="0" y="0" width="210" height="95" rx="10" fill="#ffffff" stroke="#f59e0b" stroke-width="2"/>
    <rect x="0" y="0" width="210" height="26" rx="10" fill="#fef3c7"/>
    <rect x="0" y="18" width="210" height="8" fill="#fef3c7"/>
    <text x="105" y="18" text-anchor="middle" font-size="12" font-weight="800" fill="#92400e">STANDARDS BENCHMARKS</text>

    <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">• NIST SP 800-63B Guidelines</text>
    <text x="14" y="60" font-size="10.5" fill="#64748b">• OWASP ASVS v4.0 Standard</text>
    <text x="14" y="76" font-size="10.5" fill="#64748b">• CIS Password Benchmarks</text>
    <text x="14" y="88" font-size="9.5" font-weight="600" fill="#d97706">Custom Institutional Rules</text>
  </g>
</svg>
'''

# ==============================================================================
# DESIGN C: DUAL-ENVIRONMENT TOPOLOGY (LOCAL DEV VS. CLOUD PRODUCTION)
# ==============================================================================
SVG_DESIGN_C = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 980 500" width="980" height="500" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <filter id="env-shadow" x="-5%" y="-5%" width="110%" height="115%">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
    <marker id="flow-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#2563eb"/>
    </marker>
  </defs>

  <!-- Title Banner -->
  <rect x="20" y="15" width="940" height="46" rx="8" fill="#0f172a"/>
  <text x="40" y="44" font-size="16" font-weight="800" fill="#38bdf8" letter-spacing="0.5">DUAL-ENVIRONMENT SYSTEM ARCHITECTURE</text>
  <text x="560" y="44" font-size="13" font-weight="600" fill="#94a3b8">#23 PasswordPolicy Checker (Localhost vs. Cloud)</text>

  <!-- ================= LEFT: LOCAL DEVELOPMENT ENVIRONMENT ================= -->
  <g transform="translate(20, 75)" filter="url(#env-shadow)">
    <rect x="0" y="0" width="455" height="400" rx="12" fill="#f8fafc" stroke="#3b82f6" stroke-width="2"/>
    <rect x="0" y="0" width="455" height="38" rx="12" fill="#1e40af"/>
    <rect x="0" y="26" width="455" height="12" fill="#1e40af"/>
    <text x="25" y="25" font-size="14" font-weight="800" fill="#ffffff" letter-spacing="0.5">ENVIRONMENT A: LOCAL DEVELOPMENT (OFFLINE / DEV)</text>

    <!-- Step 1: Local Browser -->
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="405" height="75" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="75" rx="3" fill="#3b82f6"/>
      <text x="18" y="24" font-size="13.5" font-weight="700" fill="#0f172a">1. Local Client Workstation (Browser)</text>
      <text x="18" y="44" font-size="11" fill="#64748b">Operator signs in as Administrator, Security Analyst, or Viewer</text>
      <text x="18" y="62" font-size="10.5" font-weight="600" fill="#2563eb">URL: http://localhost:5173 (React + Vite Dev Server)</text>
    </g>

    <!-- Arrow down -->
    <line x1="227" y1="130" x2="227" y2="160" stroke="#2563eb" stroke-width="2.5" marker-end="url(#flow-arrow)"/>
    <text x="235" y="148" font-size="9.5" font-weight="700" fill="#1e40af">Local HTTP REST API Requests</text>

    <!-- Step 2: Local FastAPI Backend -->
    <g transform="translate(25, 165)">
      <rect x="0" y="0" width="405" height="95" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="95" rx="3" fill="#0284c7"/>
      <text x="18" y="24" font-size="13.5" font-weight="700" fill="#0f172a">2. Local Backend Service (Python FastAPI)</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• Compliance Engine benchmarks policies against NIST / OWASP</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• Authenticates users using JWT tokens &amp; BCrypt hashes</text>
      <text x="18" y="74" font-size="11" fill="#64748b">• Tracks failed login attempts &amp; enforces account lockout</text>
      <text x="18" y="88" font-size="10.5" font-weight="600" fill="#0284c7">Host: Uvicorn ASGI Server • http://localhost:8000</text>
    </g>

    <!-- Arrow down -->
    <line x1="227" y1="260" x2="227" y2="290" stroke="#2563eb" stroke-width="2.5" marker-end="url(#flow-arrow)"/>
    <text x="235" y="278" font-size="9.5" font-weight="700" fill="#1e40af">SQLAlchemy Direct Disk Access</text>

    <!-- Step 3: Local SQLite DB -->
    <g transform="translate(25, 295)">
      <rect x="0" y="0" width="405" height="80" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="80" rx="3" fill="#10b981"/>
      <text x="18" y="24" font-size="13.5" font-weight="700" fill="#0f172a">3. Embedded Database (SQLite)</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• File: passwordpolicy.db (Local disk storage)</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• Stores staff accounts, evaluation records, and audit logs</text>
      <text x="18" y="72" font-size="10" font-weight="600" fill="#059669">Fast, zero-configuration offline development storage</text>
    </g>
  </g>

  <!-- ================= RIGHT: CLOUD PRODUCTION ENVIRONMENT ================= -->
  <g transform="translate(505, 75)" filter="url(#env-shadow)">
    <rect x="0" y="0" width="455" height="400" rx="12" fill="#f8fafc" stroke="#8b5cf6" stroke-width="2"/>
    <rect x="0" y="0" width="455" height="38" rx="12" fill="#6d28d9"/>
    <rect x="0" y="26" width="455" height="12" fill="#6d28d9"/>
    <text x="25" y="25" font-size="14" font-weight="800" fill="#ffffff" letter-spacing="0.5">ENVIRONMENT B: CLOUD DEPLOYMENT (PRODUCTION)</text>

    <!-- Step 1: Remote Web Users -->
    <g transform="translate(25, 55)">
      <rect x="0" y="0" width="405" height="75" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="75" rx="3" fill="#8b5cf6"/>
      <text x="18" y="24" font-size="13.5" font-weight="700" fill="#0f172a">1. Remote Client Endpoints (Internet Browsers)</text>
      <text x="18" y="44" font-size="11" fill="#64748b">Administrators, Security Analysts, and Viewers access the live URL</text>
      <text x="18" y="62" font-size="10.5" font-weight="600" fill="#7c3aed">Secure HTTPS: https://password-policy1.vercel.app</text>
    </g>

    <!-- Arrow down -->
    <line x1="227" y1="130" x2="227" y2="160" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#flow-arrow)"/>
    <text x="235" y="148" font-size="9.5" font-weight="700" fill="#6d28d9">TLS 1.3 Encrypted HTTPS Port 443</text>

    <!-- Step 2: Vercel Cloud Server -->
    <g transform="translate(25, 165)">
      <rect x="0" y="0" width="405" height="95" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="95" rx="3" fill="#7c3aed"/>
      <text x="18" y="24" font-size="13.5" font-weight="700" fill="#0f172a">2. Cloud Web Server (Vercel Edge Network)</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• Hosts optimized React frontend bundles with global CDN caching</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• Serverless Python runtime executes FastAPI API endpoints</text>
      <text x="18" y="74" font-size="11" fill="#64748b">• Evaluates policies against stored NIST/OWASP standards</text>
      <text x="18" y="88" font-size="10.5" font-weight="600" fill="#7c3aed">Production Hosting: Vercel Serverless Edge Platform</text>
    </g>

    <!-- Arrow down -->
    <line x1="227" y1="260" x2="227" y2="290" stroke="#7c3aed" stroke-width="2.5" marker-end="url(#flow-arrow)"/>
    <text x="235" y="278" font-size="9.5" font-weight="700" fill="#6d28d9">Encrypted Database Pooler (Port 6543 / SSL)</text>

    <!-- Step 3: Supabase PostgreSQL -->
    <g transform="translate(25, 295)">
      <rect x="0" y="0" width="405" height="80" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="80" rx="3" fill="#047857"/>
      <text x="18" y="24" font-size="13.5" font-weight="700" fill="#0f172a">3. Cloud Managed Database (Supabase PostgreSQL)</text>
      <text x="18" y="42" font-size="11" fill="#64748b">• Hosted in dedicated AWS Cloud VPC with automated connection pooling</text>
      <text x="18" y="58" font-size="11" fill="#64748b">• Maintains persistent user credentials, policy profiles, and audit trail</text>
      <text x="18" y="72" font-size="10" font-weight="600" fill="#047857">Scheduled GitHub Actions keepalive ping maintains active state</text>
    </g>
  </g>
</svg>
'''

# Write SVGs
path_a = os.path.join(DOWNLOADS, "topology_option_a_3tier.svg")
path_b = os.path.join(DOWNLOADS, "topology_option_b_star.svg")
path_c = os.path.join(DOWNLOADS, "topology_option_c_dual_env.svg")

with open(path_a, "w", encoding="utf-8") as f:
    f.write(SVG_DESIGN_A)
with open(path_b, "w", encoding="utf-8") as f:
    f.write(SVG_DESIGN_B)
with open(path_c, "w", encoding="utf-8") as f:
    f.write(SVG_DESIGN_C)

print("Saved 3 SVG options to Downloads!")

# Render PNGs using headless Chrome
for svg_p, png_name in [
    (path_a, "topology_option_a_3tier.png"),
    (path_b, "topology_option_b_star.png"),
    (path_c, "topology_option_c_dual_env.png")
]:
    png_p = os.path.join(DOWNLOADS, png_name)
    subprocess.run([
        CHROME, "--headless=new", "--disable-gpu", "--window-size=1200,800",
        f"--screenshot={png_p}", svg_p
    ], check=True)
    
    # Auto-crop
    im = Image.open(png_p)
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    bbox = diff.getbbox()
    if bbox:
        pad = 8
        crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.size[0], bbox[2]+pad), min(im.size[1], bbox[3]+pad))
        cropped = im.crop(crop_box)
        cropped.save(png_p)
        print(f"Rendered and cropped: {png_name}")

print("All 3 fresh designs generated and rendered!")
