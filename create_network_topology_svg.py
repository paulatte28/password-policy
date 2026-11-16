import os
import subprocess

SVG_CONTENT = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 340" width="1000" height="340" style="background:#ffffff; font-family:'Segoe UI', Arial, sans-serif;">
  <defs>
    <!-- Arrowhead markers -->
    <marker id="arrow-both" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-right" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1d4ed8"/>
    </marker>
    <marker id="arrow-left" viewBox="0 0 10 10" refX="2" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 8 1.5 L 0 5 L 8 8.5 z" fill="#1d4ed8"/>
    </marker>

    <!-- Filters for subtle shadows -->
    <filter id="card-shadow" x="-5%" y="-5%" width="110%" height="115%" filterUnits="userSpaceOnUse">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.06"/>
    </filter>
  </defs>

  <!-- ======================================================== -->
  <!-- 1. USER NETWORK (Client Segment)                         -->
  <!-- ======================================================== -->
  <g id="user-network">
    <!-- Outer dashed container -->
    <rect x="15" y="12" width="225" height="315" rx="14" ry="14"
          fill="#f2fbf2" stroke="#84cc84" stroke-width="2.5" stroke-dasharray="7,5"/>
    
    <!-- Header Titles -->
    <text x="127" y="38" text-anchor="middle" font-size="16" font-weight="800" fill="#0f172a" letter-spacing="0.5">USER NETWORK</text>
    <text x="127" y="56" text-anchor="middle" font-size="13" font-weight="600" fill="#166534">(Client Segment)</text>

    <!-- 1A. Admin Laptop -->
    <g transform="translate(48, 72)">
      <!-- Laptop Screen -->
      <rect x="14" y="0" width="52" height="34" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <rect x="17" y="3" width="46" height="28" rx="1" fill="#38bdf8"/>
      <!-- Window mock lines -->
      <line x1="21" y1="8" x2="35" y2="8" stroke="#0369a1" stroke-width="2" stroke-linecap="round"/>
      <rect x="21" y="13" width="38" height="14" rx="1" fill="#ffffff" opacity="0.9"/>
      <!-- Laptop Base / Keyboard -->
      <path d="M 4 34 L 76 34 L 80 40 L 0 40 Z" fill="#475569"/>
      <line x1="28" y1="36" x2="52" y2="36" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
      <!-- Label -->
      <text x="40" y="54" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Admin</text>
    </g>

    <!-- 1B. Analyst Laptop -->
    <g transform="translate(48, 148)">
      <!-- Laptop Screen -->
      <rect x="14" y="0" width="52" height="34" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <rect x="17" y="3" width="46" height="28" rx="1" fill="#38bdf8"/>
      <line x1="21" y1="8" x2="35" y2="8" stroke="#0369a1" stroke-width="2" stroke-linecap="round"/>
      <rect x="21" y="13" width="38" height="14" rx="1" fill="#ffffff" opacity="0.9"/>
      <!-- Laptop Base -->
      <path d="M 4 34 L 76 34 L 80 40 L 0 40 Z" fill="#475569"/>
      <line x1="28" y1="36" x2="52" y2="36" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
      <!-- Label -->
      <text x="40" y="54" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Analyst</text>
    </g>

    <!-- 1C. Viewer Laptop -->
    <g transform="translate(48, 224)">
      <!-- Laptop Screen -->
      <rect x="14" y="0" width="52" height="34" rx="3" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
      <rect x="17" y="3" width="46" height="28" rx="1" fill="#38bdf8"/>
      <line x1="21" y1="8" x2="35" y2="8" stroke="#0369a1" stroke-width="2" stroke-linecap="round"/>
      <rect x="21" y="13" width="38" height="14" rx="1" fill="#ffffff" opacity="0.9"/>
      <!-- Laptop Base -->
      <path d="M 4 34 L 76 34 L 80 40 L 0 40 Z" fill="#475569"/>
      <line x1="28" y1="36" x2="52" y2="36" stroke="#94a3b8" stroke-width="1.5" stroke-linecap="round"/>
      <!-- Label -->
      <text x="40" y="54" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Viewer</text>
    </g>

    <!-- Bus wiring connecting Admin, Analyst, Viewer -->
    <!-- From Admin -->
    <line x1="128" y1="92" x2="168" y2="92" stroke="#1d4ed8" stroke-width="2.5"/>
    <!-- From Analyst -->
    <line x1="128" y1="168" x2="185" y2="168" stroke="#1d4ed8" stroke-width="2.5"/>
    <!-- From Viewer -->
    <line x1="128" y1="244" x2="168" y2="244" stroke="#1d4ed8" stroke-width="2.5"/>
    <!-- Vertical bus backbone -->
    <line x1="168" y1="92" x2="168" y2="244" stroke="#1d4ed8" stroke-width="2.5"/>
    <!-- Junction Dot -->
    <circle cx="168" cy="168" r="4.5" fill="#1d4ed8"/>
    <!-- Line leading out toward firewall -->
    <line x1="168" y1="168" x2="252" y2="168" stroke="#1d4ed8" stroke-width="2.5"/>
  </g>

  <!-- ======================================================== -->
  <!-- 2. FIREWALL (Perimeter Security)                         -->
  <!-- ======================================================== -->
  <!-- Arrow from User Network Bus to Firewall -->
  <line x1="250" y1="168" x2="278" y2="168" stroke="#1d4ed8" stroke-width="2.5" marker-end="url(#arrow-right)"/>

  <g id="firewall" transform="translate(282, 134)">
    <!-- Brick Wall Graphic -->
    <g stroke="#ffffff" stroke-width="1.5" shape-rendering="crispEdges">
      <!-- Row 1 -->
      <rect x="0" y="0" width="23" height="11" fill="#e11d48"/>
      <rect x="23" y="0" width="22" height="11" fill="#be123c"/>
      <rect x="45" y="0" width="23" height="11" fill="#e11d48"/>
      <!-- Row 2 -->
      <rect x="0" y="11" width="11" height="11" fill="#be123c"/>
      <rect x="11" y="11" width="23" height="11" fill="#e11d48"/>
      <rect x="34" y="11" width="23" height="11" fill="#be123c"/>
      <rect x="57" y="11" width="11" height="11" fill="#e11d48"/>
      <!-- Row 3 -->
      <rect x="0" y="22" width="23" height="11" fill="#e11d48"/>
      <rect x="23" y="22" width="22" height="11" fill="#be123c"/>
      <rect x="45" y="22" width="23" height="11" fill="#e11d48"/>
      <!-- Row 4 -->
      <rect x="0" y="33" width="11" height="11" fill="#be123c"/>
      <rect x="11" y="33" width="23" height="11" fill="#e11d48"/>
      <rect x="34" y="33" width="23" height="11" fill="#be123c"/>
      <rect x="57" y="33" width="11" height="11" fill="#e11d48"/>
    </g>
    <!-- Label -->
    <text x="34" y="58" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Firewall</text>
  </g>

  <!-- Arrow between Firewall and Server Network -->
  <line x1="354" y1="168" x2="384" y2="168" stroke="#1d4ed8" stroke-width="2.5" marker-start="url(#arrow-left)" marker-end="url(#arrow-right)"/>

  <!-- ======================================================== -->
  <!-- 3. SERVER NETWORK (Application Segment)                  -->
  <!-- ======================================================== -->
  <g id="server-network">
    <!-- Outer dashed container -->
    <rect x="390" y="12" width="375" height="315" rx="14" ry="14"
          fill="#f0f7ff" stroke="#60a5fa" stroke-width="2.5" stroke-dasharray="7,5"/>
    
    <!-- Header Titles -->
    <text x="577" y="38" text-anchor="middle" font-size="16" font-weight="800" fill="#0f172a" letter-spacing="0.5">SERVER NETWORK</text>
    <text x="577" y="56" text-anchor="middle" font-size="13" font-weight="600" fill="#1e40af">(Application Segment)</text>

    <!-- 3A. Web / Application Server -->
    <g transform="translate(425, 96)">
      <!-- Server Tower Case -->
      <rect x="10" y="0" width="60" height="92" rx="4" fill="#0f172a" stroke="#334155" stroke-width="2"/>
      
      <!-- DVD / Drive Slot -->
      <rect x="18" y="10" width="44" height="6" rx="1" fill="#334155"/>
      <rect x="18" y="20" width="44" height="6" rx="1" fill="#334155"/>
      
      <!-- Ventilation Grill -->
      <line x1="18" y1="34" x2="62" y2="34" stroke="#1e293b" stroke-width="2"/>
      <line x1="18" y1="40" x2="62" y2="40" stroke="#1e293b" stroke-width="2"/>
      <line x1="18" y1="46" x2="62" y2="46" stroke="#1e293b" stroke-width="2"/>
      
      <!-- Status Lights -->
      <circle cx="22" cy="62" r="3" fill="#22c55e"/> <!-- Green Power -->
      <circle cx="32" cy="62" r="3" fill="#38bdf8"/> <!-- Blue Activity -->
      <circle cx="42" cy="62" r="3" fill="#f59e0b"/> <!-- Yellow Status -->
      
      <!-- Power Button -->
      <circle cx="58" cy="62" r="4" fill="#475569" stroke="#94a3b8" stroke-width="1"/>

      <!-- Lower Vent -->
      <rect x="18" y="74" width="44" height="10" rx="2" fill="#1e293b"/>
      
      <!-- Server Labels -->
      <text x="40" y="112" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Web / Application</text>
      <text x="40" y="128" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Server</text>
      <text x="40" y="145" text-anchor="middle" font-size="11.5" font-weight="600" fill="#2563eb">(FastAPI / React)</text>
    </g>

    <!-- Horizontal Bidirectional Arrow between App Server and DB Server -->
    <line x1="535" y1="150" x2="598" y2="150" stroke="#1d4ed8" stroke-width="2.5" marker-start="url(#arrow-left)" marker-end="url(#arrow-right)"/>

    <!-- 3B. Database Server (Cylinder) -->
    <g transform="translate(620, 96)">
      <!-- Cylinder 3D Stack -->
      <!-- Bottom Layer -->
      <path d="M 0 54 A 32 12 0 0 0 64 54 L 64 72 A 32 12 0 0 1 0 72 Z" fill="#0284c7"/>
      <ellipse cx="32" cy="54" rx="32" ry="12" fill="#38bdf8"/>
      
      <!-- Middle Layer -->
      <path d="M 0 28 A 32 12 0 0 0 64 28 L 64 46 A 32 12 0 0 1 0 46 Z" fill="#0284c7"/>
      <ellipse cx="32" cy="28" rx="32" ry="12" fill="#38bdf8"/>
      
      <!-- Top Layer -->
      <path d="M 0 2 A 32 12 0 0 0 64 2 L 64 20 A 32 12 0 0 1 0 20 Z" fill="#0284c7"/>
      <ellipse cx="32" cy="2" rx="32" ry="12" fill="#7dd3fc"/>

      <!-- Subtle cylinder outline -->
      <path d="M 0 2 L 0 72 A 32 12 0 0 0 64 72 L 64 2" fill="none" stroke="#0369a1" stroke-width="1.5"/>

      <!-- DB Server Labels -->
      <text x="32" y="112" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Database</text>
      <text x="32" y="128" text-anchor="middle" font-size="13" font-weight="700" fill="#0f172a">Server</text>
      <text x="32" y="145" text-anchor="middle" font-size="11.5" font-weight="600" fill="#2563eb">(Supabase PostgreSQL)</text>
    </g>
  </g>

  <!-- Arrow between Database Server and External Network -->
  <line x1="765" y1="168" x2="805" y2="168" stroke="#1d4ed8" stroke-width="2.5" marker-start="url(#arrow-left)" marker-end="url(#arrow-right)"/>

  <!-- ======================================================== -->
  <!-- 4. EXTERNAL NETWORK (Reference & Updates)                -->
  <!-- ======================================================== -->
  <g id="external-network">
    <!-- Outer dashed container -->
    <rect x="808" y="12" width="180" height="315" rx="14" ry="14"
          fill="#fbf5ff" stroke="#c084fc" stroke-width="2.5" stroke-dasharray="7,5"/>
    
    <!-- Header Titles -->
    <text x="898" y="38" text-anchor="middle" font-size="15" font-weight="800" fill="#0f172a" letter-spacing="0.5">EXTERNAL NETWORK</text>
    <text x="898" y="56" text-anchor="middle" font-size="12.5" font-weight="600" fill="#7e22ce">(Reference &amp; Updates)</text>

    <!-- Cloud with Globe inside -->
    <g transform="translate(845, 102)">
      <!-- Cloud Body -->
      <path d="M 22 55 
               A 22 22 0 0 1 20 20 
               A 28 28 0 0 1 65 10 
               A 25 25 0 0 1 95 32 
               A 20 20 0 0 1 90 55 
               Z" 
            fill="#ffffff" stroke="#9333ea" stroke-width="2.5" filter="url(#card-shadow)"/>
      
      <!-- Globe Inside Cloud -->
      <g transform="translate(42, 18)" stroke="#9333ea" stroke-width="1.5" fill="none">
        <circle cx="16" cy="16" r="14" fill="#f3e8ff"/>
        <ellipse cx="16" cy="16" rx="6" ry="14"/>
        <line x1="2" y1="16" x2="30" y2="16"/>
        <line x1="5" y1="9" x2="27" y2="9"/>
        <line x1="5" y1="23" x2="27" y2="23"/>
      </g>

      <!-- Labels -->
      <text x="56" y="82" text-anchor="middle" font-size="14" font-weight="700" fill="#0f172a">Internet</text>
      <text x="56" y="99" text-anchor="middle" font-size="10.5" font-weight="600" fill="#6b21a8">(Standards NIST/OWASP,</text>
      <text x="56" y="113" text-anchor="middle" font-size="10.5" font-weight="600" fill="#6b21a8">Reports, Cloud API)</text>
    </g>
  </g>
</svg>
'''

out_svg_path = os.path.abspath("network_topology.svg")
with open(out_svg_path, "w", encoding="utf-8") as f:
    f.write(SVG_CONTENT)
print(f"Successfully generated SVG: {out_svg_path}")

# Render to high-res PNG using headless Chrome
out_png_path = os.path.abspath("network_topology_sample_style.png")
chrome_cmd = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "--headless=new",
    "--disable-gpu",
    "--window-size=1200,450",
    f"--screenshot={out_png_path}",
    out_svg_path
]
subprocess.run(chrome_cmd, check=True)
print(f"Successfully rendered PNG: {out_png_path}")
