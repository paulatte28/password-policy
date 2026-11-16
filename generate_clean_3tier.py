import os
import subprocess
from PIL import Image, ImageChops

DOWNLOADS = r"c:\Users\Admin\Downloads"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
WORKSPACE = r"c:\Users\Admin\Documents\4th Year\IT23\password-policy"

# ==========================================
# 1. HORIZONTAL 3-TIER ARCHITECTURE SVG
# ==========================================
SVG_HORIZONTAL = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" width="1000" height="500" style="background:#ffffff; font-family:'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;">
  <defs>
    <!-- Arrow Marker -->
    <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#2563eb"/>
    </marker>
    <marker id="arrow-green" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 8 5 L 0 9 z" fill="#059669"/>
    </marker>
    <!-- Filter Shadow -->
    <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="112%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#0f172a" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- Main Banner Header -->
  <rect x="25" y="15" width="950" height="42" rx="8" fill="#0f172a"/>
  <text x="500" y="41" text-anchor="middle" font-size="15" font-weight="700" fill="#38bdf8" letter-spacing="0.5">3-TIER WEB ARCHITECTURE TOPOLOGY</text>

  <!-- ==================== TIER 1: PRESENTATION TIER ==================== -->
  <g transform="translate(25, 75)" filter="url(#card-shadow)">
    <!-- Outer Container -->
    <rect x="0" y="0" width="280" height="400" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect x="0" y="0" width="280" height="34" rx="10" fill="#e2e8f0"/>
    <rect x="0" y="22" width="280" height="12" fill="#e2e8f0"/>
    <text x="140" y="22" text-anchor="middle" font-size="12" font-weight="800" fill="#1e293b" letter-spacing="0.3">TIER 1: PRESENTATION TIER</text>
    <text x="140" y="48" text-anchor="middle" font-size="10.5" font-weight="600" fill="#64748b">Client Web Browsers &amp; UI</text>

    <!-- Sub-card 1: User Roles -->
    <g transform="translate(15, 62)">
      <rect x="0" y="0" width="250" height="135" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#f1f5f9"/>
      <rect x="0" y="16" width="250" height="8" fill="#f1f5f9"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#334155">Authorized User Roles</text>

      <!-- Role Items -->
      <g transform="translate(12, 34)">
        <circle cx="10" cy="10" r="10" fill="#dcfce7"/>
        <text x="10" y="14" text-anchor="middle" font-size="11">👤</text>
        <text x="28" y="10" font-size="11" font-weight="700" fill="#0f172a">Administrator</text>
        <text x="28" y="22" font-size="9.5" fill="#64748b">Full access, user &amp; policy control</text>
      </g>
      <g transform="translate(12, 68)">
        <circle cx="10" cy="10" r="10" fill="#e0f2fe"/>
        <text x="10" y="14" text-anchor="middle" font-size="11">🛡️</text>
        <text x="28" y="10" font-size="11" font-weight="700" fill="#0f172a">Security Analyst</text>
        <text x="28" y="22" font-size="9.5" fill="#64748b">Evaluates &amp; compares policies</text>
      </g>
      <g transform="translate(12, 102)">
        <circle cx="10" cy="10" r="10" fill="#f3e8ff"/>
        <text x="10" y="14" text-anchor="middle" font-size="11">👁️</text>
        <text x="28" y="10" font-size="11" font-weight="700" fill="#0f172a">Viewer / Auditor</text>
        <text x="28" y="22" font-size="9.5" fill="#64748b">Read-only dashboard &amp; reports</text>
      </g>
    </g>

    <!-- Sub-card 2: React Frontend UI -->
    <g transform="translate(15, 212)">
      <rect x="0" y="0" width="250" height="172" rx="8" fill="#ffffff" stroke="#38bdf8" stroke-width="1.5"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#e0f2fe"/>
      <rect x="0" y="16" width="250" height="8" fill="#e0f2fe"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#0369a1">React + Vite Frontend UI</text>

      <text x="14" y="44" font-size="10.5" font-weight="700" fill="#0f172a">Single-Page Application (SPA)</text>
      <text x="14" y="60" font-size="10" fill="#475569">• Runs locally on http://localhost:5173</text>
      <text x="14" y="74" font-size="10" fill="#475569">• Production deployed on Vercel</text>

      <line x1="14" y1="84" x2="236" y2="84" stroke="#f1f5f9" stroke-width="1"/>

      <text x="14" y="102" font-size="10.5" font-weight="700" fill="#0f172a">Key UI Modules:</text>
      <text x="14" y="118" font-size="10" fill="#475569">• Policy Rule Form &amp; JSON/CSV Upload</text>
      <text x="14" y="132" font-size="10" fill="#475569">• Chart.js Compliance Radar &amp; Bar Visuals</text>
      <text x="14" y="146" font-size="10" fill="#475569">• Side-by-side Policy Comparison Table</text>
      <text x="14" y="160" font-size="10" fill="#475569">• Security Audit Log Viewer</text>
    </g>
  </g>

  <!-- ==================== CONNECTOR 1: HTTP / REST API ==================== -->
  <g transform="translate(305, 240)">
    <line x1="0" y1="20" x2="50" y2="20" stroke="#2563eb" stroke-width="2.5" marker-end="url(#arrow-blue)"/>
    <rect x="-10" y="-8" width="70" height="18" rx="4" fill="#eff6ff" stroke="#93c5fd" stroke-width="1"/>
    <text x="25" y="5" text-anchor="middle" font-size="9" font-weight="700" fill="#1d4ed8">HTTP / JSON</text>
    <text x="25" y="32" text-anchor="middle" font-size="8" fill="#64748b">REST API</text>
  </g>

  <!-- ==================== TIER 2: APPLICATION TIER ==================== -->
  <g transform="translate(360, 75)" filter="url(#card-shadow)">
    <!-- Outer Container -->
    <rect x="0" y="0" width="280" height="400" rx="10" fill="#f8fafc" stroke="#3b82f6" stroke-width="1.5"/>
    <rect x="0" y="0" width="280" height="34" rx="10" fill="#dbeafe"/>
    <rect x="0" y="22" width="280" height="12" fill="#dbeafe"/>
    <text x="140" y="22" text-anchor="middle" font-size="12" font-weight="800" fill="#1e40af" letter-spacing="0.3">TIER 2: APPLICATION TIER</text>
    <text x="140" y="48" text-anchor="middle" font-size="10.5" font-weight="600" fill="#64748b">Business Logic &amp; Policy Engine</text>

    <!-- Sub-card 1: FastAPI Backend -->
    <g transform="translate(15, 62)">
      <rect x="0" y="0" width="250" height="85" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#f1f5f9"/>
      <rect x="0" y="16" width="250" height="8" fill="#f1f5f9"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#334155">FastAPI Backend Server</text>

      <text x="14" y="42" font-size="10" fill="#475569">• Python 3.14 running on Uvicorn</text>
      <text x="14" y="56" font-size="10" fill="#475569">• Local port: http://localhost:8000</text>
      <text x="14" y="70" font-size="10" fill="#475569">• Asynchronous request handling</text>
    </g>

    <!-- Sub-card 2: Policy Compliance Engine -->
    <g transform="translate(15, 160)">
      <rect x="0" y="0" width="250" height="110" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#eff6ff"/>
      <rect x="0" y="16" width="250" height="8" fill="#eff6ff"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#1d4ed8">Compliance Evaluation Engine</text>

      <text x="14" y="42" font-size="10" fill="#475569">• NIST SP 800-63B standards rule check</text>
      <text x="14" y="56" font-size="10" fill="#475569">• OWASP ASVS v4.0 verification</text>
      <text x="14" y="70" font-size="10" fill="#475569">• CIS Benchmarks &amp; PCI-DSS rules</text>
      <text x="14" y="84" font-size="10" fill="#475569">• Automated risk score calculation (0–100)</text>
      <text x="14" y="98" font-size="10" fill="#475569">• Remediation advice generation</text>
    </g>

    <!-- Sub-card 3: Security & Auth Module -->
    <g transform="translate(15, 282)">
      <rect x="0" y="0" width="250" height="102" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#f1f5f9"/>
      <rect x="0" y="16" width="250" height="8" fill="#f1f5f9"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#334155">Security &amp; Auth Controller</text>

      <text x="14" y="42" font-size="10" fill="#475569">• JWT token generation &amp; validation</text>
      <text x="14" y="56" font-size="10" fill="#475569">• BCrypt password hashing (salted)</text>
      <text x="14" y="70" font-size="10" fill="#475569">• Brute-force account lockout defense</text>
      <text x="14" y="84" font-size="10" fill="#475569">• Role-based route guard enforcement</text>
    </g>
  </g>

  <!-- ==================== CONNECTOR 2: SQLALCHEMY ORM ==================== -->
  <g transform="translate(640, 240)">
    <line x1="0" y1="20" x2="50" y2="20" stroke="#059669" stroke-width="2.5" marker-end="url(#arrow-green)"/>
    <rect x="-10" y="-8" width="70" height="18" rx="4" fill="#f0fdf4" stroke="#a7f3d0" stroke-width="1"/>
    <text x="25" y="5" text-anchor="middle" font-size="9" font-weight="700" fill="#047857">SQLAlchemy</text>
    <text x="25" y="32" text-anchor="middle" font-size="8" fill="#64748b">DB Queries</text>
  </g>

  <!-- ==================== TIER 3: DATA TIER ==================== -->
  <g transform="translate(695, 75)" filter="url(#card-shadow)">
    <!-- Outer Container -->
    <rect x="0" y="0" width="280" height="400" rx="10" fill="#f8fafc" stroke="#10b981" stroke-width="1.5"/>
    <rect x="0" y="0" width="280" height="34" rx="10" fill="#d1fae5"/>
    <rect x="0" y="22" width="280" height="12" fill="#d1fae5"/>
    <text x="140" y="22" text-anchor="middle" font-size="12" font-weight="800" fill="#065f46" letter-spacing="0.3">TIER 3: DATA STORAGE TIER</text>
    <text x="140" y="48" text-anchor="middle" font-size="10.5" font-weight="600" fill="#64748b">Database &amp; Persistence</text>

    <!-- Sub-card 1: SQLite Local -->
    <g transform="translate(15, 62)">
      <rect x="0" y="0" width="250" height="85" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#f1f5f9"/>
      <rect x="0" y="16" width="250" height="8" fill="#f1f5f9"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#334155">Local SQLite Database</text>

      <text x="14" y="42" font-size="10" fill="#475569">• File: passwordpolicy.db</text>
      <text x="14" y="56" font-size="10" fill="#475569">• Offline development &amp; quick testing</text>
      <text x="14" y="70" font-size="10" fill="#475569">• Zero network latency</text>
    </g>

    <!-- Sub-card 2: Cloud Supabase PostgreSQL -->
    <g transform="translate(15, 160)">
      <rect x="0" y="0" width="250" height="85" rx="8" fill="#ffffff" stroke="#059669" stroke-width="1.5"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#ecfdf5"/>
      <rect x="0" y="16" width="250" height="8" fill="#ecfdf5"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#047857">Cloud Supabase (PostgreSQL)</text>

      <text x="14" y="42" font-size="10" fill="#475569">• Hosted PostgreSQL on AWS</text>
      <text x="14" y="56" font-size="10" fill="#475569">• Production database for deployment</text>
      <text x="14" y="70" font-size="10" fill="#475569">• SSL encrypted connection pooling</text>
    </g>

    <!-- Sub-card 3: Stored Entities -->
    <g transform="translate(15, 258)">
      <rect x="0" y="0" width="250" height="126" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1"/>
      <rect x="0" y="0" width="250" height="24" rx="8" fill="#f1f5f9"/>
      <rect x="0" y="16" width="250" height="8" fill="#f1f5f9"/>
      <text x="12" y="16" font-size="11" font-weight="700" fill="#334155">Stored Data Entities</text>

      <text x="14" y="44" font-size="10" fill="#475569">• User credentials (hashed) &amp; roles</text>
      <text x="14" y="60" font-size="10" fill="#475569">• Active &amp; customized password policies</text>
      <text x="14" y="76" font-size="10" fill="#475569">• Historical password retention hashes</text>
      <text x="14" y="92" font-size="10" fill="#475569">• Compliance evaluation run reports</text>
      <text x="14" y="108" font-size="10" fill="#475569">• Immutable security audit event logs</text>
    </g>
  </g>
</svg>
'''

# Write and render Horizontal
h_svg_path = os.path.join(DOWNLOADS, "topology_3tier_horizontal.svg")
with open(h_svg_path, "w", encoding="utf-8") as f:
    f.write(SVG_HORIZONTAL)

w_h_svg = os.path.join(WORKSPACE, "topology_3tier_horizontal.svg")
with open(w_h_svg, "w", encoding="utf-8") as f:
    f.write(SVG_HORIZONTAL)

h_png_path = os.path.join(DOWNLOADS, "topology_3tier_horizontal.png")
w_h_png = os.path.join(WORKSPACE, "topology_3tier_horizontal.png")

subprocess.run([
    CHROME, "--headless=new", "--disable-gpu", "--window-size=1200,650",
    f"--screenshot={w_h_png}", w_h_svg
], check=True)

im = Image.open(w_h_png)
bg = Image.new(im.mode, im.size, (255, 255, 255))
diff = ImageChops.difference(im, bg)
bbox = diff.getbbox()
if bbox:
    pad = 10
    crop_box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.size[0], bbox[2]+pad), min(im.size[1], bbox[3]+pad))
    cropped = im.crop(crop_box)
    cropped.save(w_h_png)
    cropped.save(h_png_path)
    print(f"Rendered Horizontal: {w_h_png} ({cropped.size})")

print("Horizontal generation complete!")
