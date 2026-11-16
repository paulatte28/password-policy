import os
import subprocess

# ==============================================================================
# DESIGN 1: HIGH-FIDELITY ENTERPRISE NETWORK DIAGRAM (VISIO / PACKET TRACER STYLE)
# ==============================================================================
SVG_V2 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1020 360" width="1020" height="360" style="background:#ffffff; font-family:'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;">
  <defs>
    <!-- Gradients -->
    <linearGradient id="laptop-screen" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="50%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <linearGradient id="laptop-body" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#0f172a"/>
    </linearGradient>

    <linearGradient id="laptop-base" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#94a3b8"/>
      <stop offset="40%" stop-color="#64748b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <linearGradient id="server-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="25%" stop-color="#0f172a"/>
      <stop offset="70%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>

    <linearGradient id="server-face" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <linearGradient id="db-disk" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="35%" stop-color="#38bdf8"/>
      <stop offset="70%" stop-color="#0284c7"/>
      <stop offset="100%" stop-color="#0369a1"/>
    </linearGradient>

    <linearGradient id="db-top" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7dd3fc"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>

    <linearGradient id="cloud-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#ffffff"/>
      <stop offset="100%" stop-color="#f3e8ff"/>
    </linearGradient>

    <linearGradient id="wire-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#2563eb"/>
      <stop offset="100%" stop-color="#1d4ed8"/>
    </linearGradient>

    <!-- Arrowhead markers -->
    <marker id="arrow-blue-r" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1 L 9 5 L 0 9 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-blue-l" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 9 1 L 0 5 L 9 9 z" fill="#1d4ed8"/>
    </marker>

    <!-- Drop Shadows -->
    <filter id="shadow-soft" x="-8%" y="-8%" width="120%" height="125%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#0f172a" flood-opacity="0.10"/>
    </filter>
    <filter id="shadow-card" x="-4%" y="-4%" width="108%" height="110%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- ======================================================== -->
  <!-- 1. USER NETWORK (Client Segment)                         -->
  <!-- ======================================================== -->
  <g id="user-segment">
    <!-- Main dashed container -->
    <rect x="18" y="16" width="225" height="328" rx="16" ry="16"
          fill="#f0fdf4" stroke="#4ade80" stroke-width="2.5" stroke-dasharray="8,6" filter="url(#shadow-card)"/>
    
    <!-- Title Headers -->
    <text x="130" y="44" text-anchor="middle" font-size="16" font-weight="800" fill="#14532d" letter-spacing="0.5">USER NETWORK</text>
    <text x="130" y="63" text-anchor="middle" font-size="13" font-weight="600" fill="#15803d">(Client Segment)</text>

    <!-- 1A. ADMIN LAPTOP -->
    <g transform="translate(52, 78)" filter="url(#shadow-soft)">
      <!-- Screen Outer Bezel -->
      <rect x="12" y="0" width="56" height="38" rx="4" fill="url(#laptop-body)" stroke="#475569" stroke-width="1"/>
      <!-- Screen Display -->
      <rect x="15" y="3" width="50" height="32" rx="2" fill="url(#laptop-screen)"/>
      <!-- App Mockup UI on Screen -->
      <rect x="18" y="6" width="44" height="6" rx="1" fill="#ffffff" opacity="0.9"/>
      <rect x="18" y="14" width="16" height="18" rx="1" fill="#0284c7" opacity="0.8"/>
      <rect x="36" y="14" width="26" height="8" rx="1" fill="#bae6fd" opacity="0.9"/>
      <rect x="36" y="24" width="26" height="8" rx="1" fill="#ffffff" opacity="0.8"/>
      <!-- Screen Gloss Shine -->
      <path d="M 15 3 L 42 3 L 26 35 L 15 35 Z" fill="#ffffff" opacity="0.18"/>
      <!-- Laptop Hinge & Base -->
      <path d="M 0 38 L 80 38 L 76 45 L 4 45 Z" fill="url(#laptop-base)"/>
      <line x1="30" y1="40" x2="50" y2="40" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
      <!-- Label -->
      <text x="40" y="60" text-anchor="middle" font-size="13.5" font-weight="700" fill="#0f172a">Admin</text>
    </g>

    <!-- 1B. ANALYST LAPTOP -->
    <g transform="translate(52, 158)" filter="url(#shadow-soft)">
      <rect x="12" y="0" width="56" height="38" rx="4" fill="url(#laptop-body)" stroke="#475569" stroke-width="1"/>
      <rect x="15" y="3" width="50" height="32" rx="2" fill="url(#laptop-screen)"/>
      <rect x="18" y="6" width="44" height="6" rx="1" fill="#ffffff" opacity="0.9"/>
      <rect x="18" y="14" width="20" height="18" rx="1" fill="#0284c7" opacity="0.8"/>
      <circle cx="48" cy="23" r="7" fill="#38bdf8" stroke="#ffffff" stroke-width="1.5"/>
      <path d="M 15 3 L 42 3 L 26 35 L 15 35 Z" fill="#ffffff" opacity="0.18"/>
      <path d="M 0 38 L 80 38 L 76 45 L 4 45 Z" fill="url(#laptop-base)"/>
      <line x1="30" y1="40" x2="50" y2="40" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
      <text x="40" y="60" text-anchor="middle" font-size="13.5" font-weight="700" fill="#0f172a">Analyst</text>
    </g>

    <!-- 1C. VIEWER LAPTOP -->
    <g transform="translate(52, 238)" filter="url(#shadow-soft)">
      <rect x="12" y="0" width="56" height="38" rx="4" fill="url(#laptop-body)" stroke="#475569" stroke-width="1"/>
      <rect x="15" y="3" width="50" height="32" rx="2" fill="url(#laptop-screen)"/>
      <rect x="18" y="6" width="44" height="6" rx="1" fill="#ffffff" opacity="0.9"/>
      <line x1="18" y1="17" x2="60" y2="17" stroke="#ffffff" stroke-width="1.5"/>
      <line x1="18" y1="23" x2="54" y2="23" stroke="#bae6fd" stroke-width="1.5"/>
      <line x1="18" y1="29" x2="48" y2="29" stroke="#ffffff" stroke-width="1.5"/>
      <path d="M 15 3 L 42 3 L 26 35 L 15 35 Z" fill="#ffffff" opacity="0.18"/>
      <path d="M 0 38 L 80 38 L 76 45 L 4 45 Z" fill="url(#laptop-base)"/>
      <line x1="30" y1="40" x2="50" y2="40" stroke="#cbd5e1" stroke-width="1.5" stroke-linecap="round"/>
      <text x="40" y="60" text-anchor="middle" font-size="13.5" font-weight="700" fill="#0f172a">Viewer</text>
    </g>

    <!-- Blue Wiring Bus linking clients -->
    <line x1="135" y1="99" x2="182" y2="99" stroke="url(#wire-grad)" stroke-width="3"/>
    <line x1="135" y1="179" x2="200" y2="179" stroke="url(#wire-grad)" stroke-width="3"/>
    <line x1="135" y1="259" x2="182" y2="259" stroke="url(#wire-grad)" stroke-width="3"/>
    <!-- Vertical connector -->
    <line x1="182" y1="99" x2="182" y2="259" stroke="url(#wire-grad)" stroke-width="3"/>
    <!-- Junction Dot -->
    <circle cx="182" cy="179" r="5" fill="#1d4ed8" stroke="#ffffff" stroke-width="1.5"/>
    <!-- Bus line pointing out -->
    <line x1="182" y1="179" x2="252" y2="179" stroke="url(#wire-grad)" stroke-width="3"/>
  </g>

  <!-- ======================================================== -->
  <!-- 2. FIREWALL (Realistic 3D Masonry Brick Wall)             -->
  <!-- ======================================================== -->
  <!-- Wire from User Network to Firewall -->
  <line x1="250" y1="179" x2="280" y2="179" stroke="url(#wire-grad)" stroke-width="3" marker-end="url(#arrow-blue-r)"/>

  <g id="firewall" transform="translate(285, 142)" filter="url(#shadow-soft)">
    <!-- 3D Wall Base & Mortar Background -->
    <rect x="0" y="0" width="70" height="48" rx="2" fill="#7f1d1d" stroke="#450a0a" stroke-width="1.5"/>
    
    <!-- Brick Pattern with Mortar lines -->
    <g fill="#dc2626" stroke="#fecaca" stroke-width="1" shape-rendering="crispEdges">
      <!-- Course 1 -->
      <rect x="2" y="2" width="20" height="9" fill="#ef4444"/>
      <rect x="24" y="2" width="22" height="9" fill="#dc2626"/>
      <rect x="48" y="2" width="20" height="9" fill="#b91c1c"/>
      <!-- Course 2 -->
      <rect x="2" y="13" width="10" height="9" fill="#dc2626"/>
      <rect x="14" y="13" width="22" height="9" fill="#ef4444"/>
      <rect x="38" y="13" width="20" height="9" fill="#dc2626"/>
      <rect x="60" y="13" width="8" height="9" fill="#b91c1c"/>
      <!-- Course 3 -->
      <rect x="2" y="24" width="20" height="9" fill="#b91c1c"/>
      <rect x="24" y="24" width="22" height="9" fill="#ef4444"/>
      <rect x="48" y="24" width="20" height="9" fill="#dc2626"/>
      <!-- Course 4 -->
      <rect x="2" y="35" width="10" height="9" fill="#ef4444"/>
      <rect x="14" y="35" width="22" height="9" fill="#dc2626"/>
      <rect x="38" y="35" width="20" height="9" fill="#b91c1c"/>
      <rect x="60" y="35" width="8" height="9" fill="#ef4444"/>
    </g>

    <!-- Top 3D Isometric Cap -->
    <polygon points="0,0 12,-6 82,-6 70,0" fill="#f87171" stroke="#991b1b" stroke-width="1"/>
    <!-- Right 3D Shadow Side -->
    <polygon points="70,0 82,-6 82,42 70,48" fill="#991b1b" stroke="#7f1d1d" stroke-width="1"/>

    <!-- Firewall Label -->
    <text x="35" y="64" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">Firewall</text>
  </g>

  <!-- Wire between Firewall and Server Network -->
  <line x1="368" y1="179" x2="400" y2="179" stroke="url(#wire-grad)" stroke-width="3" marker-start="url(#arrow-blue-l)" marker-end="url(#arrow-blue-r)"/>

  <!-- ======================================================== -->
  <!-- 3. SERVER NETWORK (Application Segment)                  -->
  <!-- ======================================================== -->
  <g id="server-segment">
    <!-- Main dashed container -->
    <rect x="408" y="16" width="375" height="328" rx="16" ry="16"
          fill="#f0f9ff" stroke="#38bdf8" stroke-width="2.5" stroke-dasharray="8,6" filter="url(#shadow-card)"/>
    
    <!-- Title Headers -->
    <text x="595" y="44" text-anchor="middle" font-size="16" font-weight="800" fill="#0c4a6e" letter-spacing="0.5">SERVER NETWORK</text>
    <text x="595" y="63" text-anchor="middle" font-size="13" font-weight="600" fill="#0369a1">(Application Segment)</text>

    <!-- 3A. WEB / APPLICATION SERVER (3D Enterprise Tower) -->
    <g transform="translate(442, 102)" filter="url(#shadow-soft)">
      <!-- Server Case Outer -->
      <rect x="0" y="0" width="68" height="106" rx="5" fill="url(#server-grad)" stroke="#475569" stroke-width="1.5"/>
      <!-- Top Bevel -->
      <rect x="4" y="4" width="60" height="6" rx="2" fill="#38bdf8" opacity="0.8"/>
      
      <!-- Hot-swap Drive Bays -->
      <g fill="#0f172a" stroke="#334155" stroke-width="1">
        <rect x="6" y="14" width="56" height="10" rx="2"/>
        <line x1="10" y1="19" x2="44" y2="19" stroke="#475569" stroke-width="1.5"/>
        <circle cx="56" cy="19" r="2" fill="#22c55e"/>

        <rect x="6" y="27" width="56" height="10" rx="2"/>
        <line x1="10" y1="32" x2="44" y2="32" stroke="#475569" stroke-width="1.5"/>
        <circle cx="56" cy="32" r="2" fill="#22c55e"/>

        <rect x="6" y="40" width="56" height="10" rx="2"/>
        <line x1="10" y1="45" x2="44" y2="45" stroke="#475569" stroke-width="1.5"/>
        <circle cx="56" cy="45" r="2" fill="#38bdf8"/>
      </g>

      <!-- Ventilation Grille -->
      <g stroke="#0f172a" stroke-width="1.5">
        <line x1="8" y1="56" x2="60" y2="56"/>
        <line x1="8" y1="61" x2="60" y2="61"/>
        <line x1="8" y1="66" x2="60" y2="66"/>
        <line x1="8" y1="71" x2="60" y2="61"/>
      </g>

      <!-- LED Activity Cluster -->
      <circle cx="14" cy="85" r="3.5" fill="#22c55e"/> <!-- Power Green -->
      <circle cx="26" cy="85" r="3.5" fill="#38bdf8"/> <!-- Net Blue -->
      <circle cx="38" cy="85" r="3.5" fill="#f59e0b"/> <!-- Disk Amber -->
      
      <!-- Power Switch -->
      <circle cx="54" cy="85" r="4.5" fill="#334155" stroke="#94a3b8" stroke-width="1"/>

      <!-- Lower Intake -->
      <rect x="6" y="94" width="56" height="6" rx="1.5" fill="#0f172a"/>

      <!-- Labels -->
      <text x="34" y="124" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Web / Application</text>
      <text x="34" y="140" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Server</text>
      <text x="34" y="157" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0284c7">(FastAPI / React)</text>
    </g>

    <!-- Bidirectional Wire between Server and Database -->
    <line x1="552" y1="155" x2="618" y2="155" stroke="url(#wire-grad)" stroke-width="3" marker-start="url(#arrow-blue-l)" marker-end="url(#arrow-blue-r)"/>

    <!-- 3B. DATABASE SERVER (3D Layered Cylinder Stack) -->
    <g transform="translate(640, 106)" filter="url(#shadow-soft)">
      <!-- Tier 3 (Bottom Disc) -->
      <g>
        <path d="M 0 54 A 34 13 0 0 0 68 54 L 68 74 A 34 13 0 0 1 0 74 Z" fill="url(#db-disk)"/>
        <ellipse cx="34" cy="54" rx="34" ry="13" fill="#0284c7" stroke="#0369a1" stroke-width="0.5"/>
        <ellipse cx="34" cy="53" rx="33" ry="12" fill="url(#db-top)"/>
      </g>

      <!-- Tier 2 (Middle Disc) -->
      <g>
        <path d="M 0 27 A 34 13 0 0 0 68 27 L 68 47 A 34 13 0 0 1 0 47 Z" fill="url(#db-disk)"/>
        <ellipse cx="34" cy="27" rx="34" ry="13" fill="#0284c7" stroke="#0369a1" stroke-width="0.5"/>
        <ellipse cx="34" cy="26" rx="33" ry="12" fill="url(#db-top)"/>
      </g>

      <!-- Tier 1 (Top Disc) -->
      <g>
        <path d="M 0 0 A 34 13 0 0 0 68 0 L 68 20 A 34 13 0 0 1 0 20 Z" fill="url(#db-disk)"/>
        <ellipse cx="34" cy="0" rx="34" ry="13" fill="#38bdf8" stroke="#0284c7" stroke-width="0.5"/>
        <ellipse cx="34" cy="-1" rx="33" ry="12" fill="#bae6fd"/>
      </g>

      <!-- Gloss highlight arc -->
      <path d="M 6 0 A 28 9 0 0 0 34 9 A 28 9 0 0 0 62 0" fill="none" stroke="#ffffff" stroke-width="1.5" opacity="0.6"/>

      <!-- Labels -->
      <text x="34" y="100" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Database</text>
      <text x="34" y="116" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Server</text>
      <text x="34" y="133" text-anchor="middle" font-size="11.5" font-weight="600" fill="#0284c7">(Supabase PostgreSQL)</text>
    </g>
  </g>

  <!-- Wire between Database Server and External Network -->
  <line x1="783" y1="179" x2="823" y2="179" stroke="url(#wire-grad)" stroke-width="3" marker-start="url(#arrow-blue-l)" marker-end="url(#arrow-blue-r)"/>

  <!-- ======================================================== -->
  <!-- 4. EXTERNAL NETWORK (Reference & Updates)                -->
  <!-- ======================================================== -->
  <g id="external-segment">
    <!-- Main dashed container -->
    <rect x="826" y="16" width="176" height="328" rx="16" ry="16"
          fill="#faf5ff" stroke="#c084fc" stroke-width="2.5" stroke-dasharray="8,6" filter="url(#shadow-card)"/>
    
    <!-- Title Headers -->
    <text x="914" y="44" text-anchor="middle" font-size="15" font-weight="800" fill="#581c87" letter-spacing="0.5">EXTERNAL NETWORK</text>
    <text x="914" y="63" text-anchor="middle" font-size="12" font-weight="600" fill="#7e22ce">(Reference &amp; Updates)</text>

    <!-- Cloud with Globe inside -->
    <g transform="translate(862, 110)" filter="url(#shadow-soft)">
      <!-- Cloud Realistic Path -->
      <path d="M 24 64 
               C 8 64 0 54 0 42 
               C 0 32 8 24 18 22 
               C 16 10 28 0 46 0 
               C 62 0 74 8 78 20 
               C 86 16 98 22 100 34 
               C 108 38 108 52 100 60 
               C 96 64 88 64 84 64 
               Z" 
            fill="url(#cloud-grad)" stroke="#9333ea" stroke-width="2.5"/>

      <!-- Detailed Globe Inside Cloud -->
      <g transform="translate(36, 18)" stroke="#7e22ce" stroke-width="1.4" fill="none">
        <!-- Globe Circle -->
        <circle cx="18" cy="18" r="16" fill="#f5f3ff"/>
        <!-- Latitudes -->
        <line x1="2" y1="18" x2="34" y2="18"/>
        <line x1="5" y1="10" x2="31" y2="10"/>
        <line x1="5" y1="26" x2="31" y2="26"/>
        <!-- Longitudes -->
        <ellipse cx="18" cy="18" rx="7" ry="16"/>
        <line x1="18" y1="2" x2="18" y2="34"/>
      </g>

      <!-- Labels -->
      <text x="52" y="90" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">Internet</text>
      <text x="52" y="108" text-anchor="middle" font-size="10.5" font-weight="600" fill="#6b21a8">(Standards NIST/OWASP,</text>
      <text x="52" y="122" text-anchor="middle" font-size="10.5" font-weight="600" fill="#6b21a8">Reports, Cloud API)</text>
    </g>
  </g>
</svg>
'''

# ==============================================================================
# DESIGN 2: MODERN CYBERSECURITY CLOUD ARCHITECTURE (LUCIDCHART / ENTERPRISE STYLE)
# ==============================================================================
SVG_V3 = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1020 380" width="1020" height="380" style="background:#ffffff; font-family:'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;">
  <defs>
    <!-- Card Gradients -->
    <linearGradient id="header-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e293b"/>
    </linearGradient>

    <linearGradient id="admin-badge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#10b981"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>

    <linearGradient id="analyst-badge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0ea5e9"/>
      <stop offset="100%" stop-color="#0284c7"/>
    </linearGradient>

    <linearGradient id="viewer-badge" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#6d28d9"/>
    </linearGradient>

    <!-- Connectors -->
    <marker id="m-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 2 L 8 5 L 0 8 z" fill="#2563eb"/>
    </marker>

    <filter id="box-shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="3" stdDeviation="5" flood-color="#0f172a" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Top Title Bar -->
  <rect x="15" y="10" width="990" height="42" rx="8" fill="url(#header-grad)"/>
  <text x="35" y="36" font-size="15" font-weight="700" fill="#38bdf8" letter-spacing="0.5">SYSTEM ARCHITECTURE &amp; TOPOLOGY</text>
  <text x="365" y="36" font-size="13" font-weight="500" fill="#cbd5e1">#23 PasswordPolicy Checker  •  IT23/L Systems Administration &amp; Maintenance</text>
  <rect x="880" y="20" width="110" height="22" rx="4" fill="#0284c7"/>
  <text x="935" y="35" text-anchor="middle" font-size="11" font-weight="700" fill="#ffffff">RBAC ENFORCED</text>

  <!-- ================= 1. CLIENT ACCESS TIER ================= -->
  <g transform="translate(15, 65)">
    <rect x="0" y="0" width="230" height="300" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#box-shadow)"/>
    <rect x="0" y="0" width="230" height="34" rx="12" fill="#f1f5f9"/>
    <rect x="0" y="24" width="230" height="10" fill="#f1f5f9"/>
    <text x="115" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">USER NETWORK (CLIENTS)</text>

    <!-- Admin Card -->
    <g transform="translate(12, 44)">
      <rect x="0" y="0" width="206" height="68" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="68" rx="3" fill="#10b981"/>
      <text x="16" y="22" font-size="13" font-weight="700" fill="#0f172a">Administrator Node</text>
      <text x="16" y="38" font-size="11" fill="#64748b">VLAN 10 • Full Management</text>
      <rect x="16" y="44" width="105" height="16" rx="3" fill="#dcfce7"/>
      <text x="68" y="56" text-anchor="middle" font-size="9.5" font-weight="700" fill="#166534">RBAC: Administrator</text>
    </g>

    <!-- Analyst Card -->
    <g transform="translate(12, 122)">
      <rect x="0" y="0" width="206" height="68" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="68" rx="3" fill="#0ea5e9"/>
      <text x="16" y="22" font-size="13" font-weight="700" fill="#0f172a">Security Analyst Node</text>
      <text x="16" y="38" font-size="11" fill="#64748b">VLAN 15 • Policy Audits</text>
      <rect x="16" y="44" width="115" height="16" rx="3" fill="#e0f2fe"/>
      <text x="73" y="56" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0369a1">RBAC: Security Analyst</text>
    </g>

    <!-- Viewer Card -->
    <g transform="translate(12, 200)">
      <rect x="0" y="0" width="206" height="68" rx="8" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5"/>
      <rect x="0" y="0" width="6" height="68" rx="3" fill="#8b5cf6"/>
      <text x="16" y="22" font-size="13" font-weight="700" fill="#0f172a">Auditor / Viewer Node</text>
      <text x="16" y="38" font-size="11" fill="#64748b">VLAN 30 • Read-Only Logs</text>
      <rect x="16" y="44" width="85" height="16" rx="3" fill="#f3e8ff"/>
      <text x="58" y="56" text-anchor="middle" font-size="9.5" font-weight="700" fill="#6b21a8">RBAC: Viewer</text>
    </g>

    <text x="115" y="288" text-anchor="middle" font-size="10.5" font-weight="600" fill="#64748b">🔒 TLS 1.3 / HTTPS (Port 443)</text>
  </g>

  <!-- Connector Line 1 -->
  <line x1="245" y1="215" x2="280" y2="215" stroke="#2563eb" stroke-width="2.5" marker-end="url(#m-arrow)"/>

  <!-- ================= 2. FIREWALL / WAF ================= -->
  <g transform="translate(285, 140)" filter="url(#box-shadow)">
    <rect x="0" y="0" width="105" height="150" rx="10" fill="#ffffff" stroke="#ef4444" stroke-width="2"/>
    <rect x="0" y="0" width="105" height="28" rx="10" fill="#fee2e2"/>
    <rect x="0" y="20" width="105" height="8" fill="#fee2e2"/>
    <text x="52" y="18" text-anchor="middle" font-size="11.5" font-weight="800" fill="#991b1b">FIREWALL</text>

    <!-- Shield Icon -->
    <path d="M 52 38 L 74 46 C 74 65 52 76 52 76 C 52 76 30 65 30 46 Z" fill="#ef4444"/>
    <path d="M 52 44 L 66 50 C 66 62 52 70 52 70 Z" fill="#f87171"/>

    <text x="52" y="94" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0f172a">Port 443 Only</text>
    <text x="52" y="108" text-anchor="middle" font-size="9" fill="#64748b">Rate Limiting</text>
    <text x="52" y="120" text-anchor="middle" font-size="9" fill="#64748b">Brute-Force Guard</text>
    <text x="52" y="132" text-anchor="middle" font-size="9" fill="#64748b">WAF Protection</text>
  </g>

  <!-- Connector Line 2 -->
  <line x1="390" y1="215" x2="425" y2="215" stroke="#2563eb" stroke-width="2.5" marker-end="url(#m-arrow)"/>

  <!-- ================= 3. APPLICATION & LOGIC TIER ================= -->
  <g transform="translate(430, 65)">
    <rect x="0" y="0" width="345" height="300" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#box-shadow)"/>
    <rect x="0" y="0" width="345" height="34" rx="12" fill="#eff6ff"/>
    <rect x="0" y="24" width="345" height="10" fill="#eff6ff"/>
    <text x="172" y="22" text-anchor="middle" font-size="13" font-weight="700" fill="#1e3a8a">SERVER NETWORK (APPLICATION TIER)</text>

    <!-- App Server Box -->
    <g transform="translate(15, 48)">
      <rect x="0" y="0" width="145" height="195" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
      <rect x="0" y="0" width="145" height="26" rx="8" fill="#dbeafe"/>
      <rect x="0" y="18" width="145" height="8" fill="#dbeafe"/>
      <text x="72" y="17" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">App / API Server</text>
      
      <!-- Tech Pill -->
      <rect x="18" y="32" width="109" height="18" rx="4" fill="#0f172a"/>
      <text x="72" y="45" text-anchor="middle" font-size="10" font-weight="700" fill="#38bdf8">FastAPI + React</text>
      
      <text x="12" y="68" font-size="9.5" font-weight="700" fill="#0f172a">• Compliance Engine</text>
      <text x="12" y="82" font-size="8.5" fill="#64748b">  NIST / OWASP Scoring</text>

      <text x="12" y="100" font-size="9.5" font-weight="700" fill="#0f172a">• Auth &amp; RBAC Guard</text>
      <text x="12" y="114" font-size="8.5" fill="#64748b">  JWT HMAC-SHA256</text>

      <text x="12" y="132" font-size="9.5" font-weight="700" fill="#0f172a">• Policy Enforcement</text>
      <text x="12" y="146" font-size="8.5" fill="#64748b">  BCrypt Hashing &amp; Lock</text>

      <text x="12" y="164" font-size="9.5" font-weight="700" fill="#0f172a">• Audit Logger</text>
      <text x="12" y="178" font-size="8.5" fill="#64748b">  Immutable Tracking</text>
    </g>

    <!-- Connector within Server Segment -->
    <line x1="160" y1="145" x2="185" y2="145" stroke="#2563eb" stroke-width="2.5" marker-end="url(#m-arrow)"/>

    <!-- Database Server Box -->
    <g transform="translate(185, 48)">
      <rect x="0" y="0" width="145" height="195" rx="8" fill="#ffffff" stroke="#93c5fd" stroke-width="1.5"/>
      <rect x="0" y="0" width="145" height="26" rx="8" fill="#dbeafe"/>
      <rect x="0" y="18" width="145" height="8" fill="#dbeafe"/>
      <text x="72" y="17" text-anchor="middle" font-size="11" font-weight="700" fill="#1e40af">Database Server</text>

      <!-- Tech Pill -->
      <rect x="14" y="32" width="117" height="18" rx="4" fill="#047857"/>
      <text x="72" y="45" text-anchor="middle" font-size="10" font-weight="700" fill="#ffffff">Supabase PostgreSQL</text>

      <text x="12" y="68" font-size="9.5" font-weight="700" fill="#0f172a">• users (BCrypt)</text>
      <text x="12" y="82" font-size="8.5" fill="#64748b">  Staff Accounts &amp; Roles</text>

      <text x="12" y="100" font-size="9.5" font-weight="700" fill="#0f172a">• policy_settings</text>
      <text x="12" y="114" font-size="8.5" fill="#64748b">  Length, Lockout, Age</text>

      <text x="12" y="132" font-size="9.5" font-weight="700" fill="#0f172a">• standard_definitions</text>
      <text x="12" y="146" font-size="8.5" fill="#64748b">  NIST / OWASP Limits</text>

      <text x="12" y="164" font-size="9.5" font-weight="700" fill="#0f172a">• audit_logs &amp; history</text>
      <text x="12" y="178" font-size="8.5" fill="#64748b">  Tamper-Evident Records</text>
    </g>

    <text x="172" y="288" text-anchor="middle" font-size="10.5" font-weight="600" fill="#1e40af">⚡ Private Subnet • SQLAlchemy Connection Pooling</text>
  </g>

  <!-- Connector Line 3 -->
  <line x1="775" y1="215" x2="810" y2="215" stroke="#2563eb" stroke-width="2.5" marker-end="url(#m-arrow)"/>

  <!-- ================= 4. EXTERNAL NETWORK ================= -->
  <g transform="translate(815, 65)">
    <rect x="0" y="0" width="190" height="300" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5" filter="url(#box-shadow)"/>
    <rect x="0" y="0" width="190" height="34" rx="12" fill="#faf5ff"/>
    <rect x="0" y="24" width="190" height="10" fill="#faf5ff"/>
    <text x="95" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="#6b21a8">EXTERNAL NETWORK</text>

    <!-- Cloud Card 1: NIST Standards -->
    <g transform="translate(12, 44)">
      <rect x="0" y="0" width="166" height="68" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.5"/>
      <text x="12" y="20" font-size="11.5" font-weight="700" fill="#0f172a">Security Benchmarks</text>
      <text x="12" y="36" font-size="9.5" fill="#6b21a8">• NIST SP 800-63B</text>
      <text x="12" y="50" font-size="9.5" fill="#6b21a8">• OWASP ASVS v4.0</text>
      <text x="12" y="62" font-size="9.5" fill="#6b21a8">• CIS Password Benchmarks</text>
    </g>

    <!-- Cloud Card 2: Cloud Platform -->
    <g transform="translate(12, 122)">
      <rect x="0" y="0" width="166" height="68" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.5"/>
      <text x="12" y="20" font-size="11.5" font-weight="700" fill="#0f172a">Cloud Infrastructure</text>
      <text x="12" y="36" font-size="9.5" fill="#0284c7">• Vercel Edge Serverless</text>
      <text x="12" y="50" font-size="9.5" fill="#047857">• Supabase AWS VPC</text>
      <text x="12" y="62" font-size="9.5" fill="#64748b">• Automated Keepalive</text>
    </g>

    <!-- Cloud Card 3: Reports -->
    <g transform="translate(12, 200)">
      <rect x="0" y="0" width="166" height="68" rx="8" fill="#ffffff" stroke="#e9d5ff" stroke-width="1.5"/>
      <text x="12" y="20" font-size="11.5" font-weight="700" fill="#0f172a">Auditing &amp; Exports</text>
      <text x="12" y="36" font-size="9.5" fill="#e11d48">• Executive PDF Reports</text>
      <text x="12" y="50" font-size="9.5" fill="#15803d">• Audit Trail CSV Dumps</text>
      <text x="12" y="62" font-size="9.5" fill="#64748b">• Zero Password Intercept</text>
    </g>

    <text x="95" y="288" text-anchor="middle" font-size="10.5" font-weight="600" fill="#7e22ce">🌐 External Reference</text>
  </g>
</svg>
'''

# Write both SVG files
v2_svg_path = os.path.abspath("network_topology_v2_visio.svg")
with open(v2_svg_path, "w", encoding="utf-8") as f:
    f.write(SVG_V2)

v3_svg_path = os.path.abspath("network_topology_v3_modern.svg")
with open(v3_svg_path, "w", encoding="utf-8") as f:
    f.write(SVG_V3)

print("Saved SVG files:")
print(" -", v2_svg_path)
print(" -", v3_svg_path)

# Render both to high-resolution PNGs using headless Chrome
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

v2_png_path = os.path.abspath("network_topology_v2_visio.png")
subprocess.run([
    chrome_path, "--headless=new", "--disable-gpu", "--window-size=1200,450",
    f"--screenshot={v2_png_path}", v2_svg_path
], check=True)

v3_png_path = os.path.abspath("network_topology_v3_modern.png")
subprocess.run([
    chrome_path, "--headless=new", "--disable-gpu", "--window-size=1200,470",
    f"--screenshot={v3_png_path}", v3_svg_path
], check=True)

print("Rendered PNG previews successfully!")
