import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.abspath("generated_report_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Try loading Windows fonts
def get_font(size, bold=False, mono=False):
    try:
        if mono:
            font_path = r"C:\Windows\Fonts\consola.ttf"
            if bold:
                font_path = r"C:\Windows\Fonts\consolab.ttf"
        else:
            font_path = r"C:\Windows\Fonts\segoeui.ttf"
            if bold:
                font_path = r"C:\Windows\Fonts\segoeuib.ttf"
        if os.path.exists(font_path):
            return ImageFont.truetype(font_path, size)
    except Exception:
        pass
    return ImageFont.load_default()

def render_code_card(title, filename, code_lines, out_filename):
    """Renders a code editor window with dark mode styling and syntax colors."""
    pad_x = 28
    pad_y = 20
    header_h = 44
    line_h = 24
    width = 1100
    height = header_h + pad_y * 2 + len(code_lines) * line_h

    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Header bar
    draw.rectangle([(0, 0), (width, header_h)], fill="#252526")
    draw.line([(0, header_h), (width, header_h)], fill="#333333", width=1)

    # Window control circles (mac/modern style)
    draw.ellipse([(16, 15), (28, 27)], fill="#ff5f56") # red
    draw.ellipse([(36, 15), (48, 27)], fill="#ffbd2e") # yellow
    draw.ellipse([(56, 15), (68, 27)], fill="#27c93f") # green

    # Header text
    font_title = get_font(14, bold=True)
    draw.text((85, 13), f"{filename}  —  {title}", fill="#cccccc", font=font_title)

    font_code = get_font(14, mono=True)
    font_line_num = get_font(13, mono=True)

    y = header_h + pad_y
    for line_num, line_str, highlight_type in code_lines:
        # Line number
        draw.text((pad_x, y), f"{line_num:>3} ", fill="#5c6370", font=font_line_num)
        
        # Color based on highlight_type
        if highlight_type == "comment":
            color = "#6a9955"
        elif highlight_type == "keyword":
            color = "#c586c0"
        elif highlight_type == "func":
            color = "#dcdcaa"
        elif highlight_type == "string":
            color = "#ce9178"
        elif highlight_type == "security":
            color = "#4ec9b0"
        elif highlight_type == "alert":
            color = "#f44747"
        else:
            color = "#d4d4d4"

        draw.text((pad_x + 55, y), line_str, fill=color, font=font_code)
        y += line_h

    img_path = os.path.join(ASSETS_DIR, out_filename)
    img.save(img_path, quality=95)
    print(f"Generated code image: {out_filename}")
    return img_path

# -------------------------------------------------------------
# 1. CODE SNIPPET 1: Compliance Engine & Scoring Algorithm
# -------------------------------------------------------------
code_func1 = [
    (18, "# Automated multi-standard compliance evaluation and risk scoring", "comment"),
    (19, "def evaluate_policy(policy: PolicyInput, standard: StandardDefinition) -> EvaluationReport:", "keyword"),
    (20, "    findings = []", "plain"),
    (21, "    dimension_scores = {}", "plain"),
    (22, "", "plain"),
    (23, "    # 1. Minimum Password Length Check against Standard Baseline", "comment"),
    (24, "    if policy.min_length < 8:", "keyword"),
    (25, "        length_score = 0.0", "alert"),
    (26, "        findings.append(Finding(category='Length', status='FAIL', severity='CRITICAL',", "security"),
    (27, "            title='Severely Inadequate Minimum Length (< 8 Chars)',", "string"),
    (28, "            risk='Passwords under 8 chars are vulnerable to instant precomputed rainbow cracking.'))", "string"),
    (29, "    elif policy.min_length < standard.recommended_min_length:", "keyword"),
    (30, "        length_score = 65.0", "plain"),
    (31, "        findings.append(Finding(category='Length', status='WARNING', severity='MEDIUM'))", "security"),
    (32, "    else:", "keyword"),
    (33, "        length_score = 100.0  # Meets or exceeds NIST SP 800-63B recommendations", "comment"),
    (34, "", "plain"),
    (35, "    # 2. Account Lockout & Brute-Force Rate Limiting Assessment", "comment"),
    (36, "    if policy.max_failed_attempts == 0 or policy.lockout_duration_min == 0:", "keyword"),
    (37, "        lockout_score = 0.0", "alert"),
    (38, "        findings.append(Finding(category='Lockout', status='FAIL', severity='CRITICAL',", "security"),
    (39, "            title='Zero Account Lockout Protection (Brute-Force Vulnerability)'))", "string"),
    (40, "", "plain"),
    (41, "    # 3. Overall Weighted Score Calculation & Grade Letter Assignment", "comment"),
    (42, "    overall_score = (length_score * 0.25) + (complexity_score * 0.15) + \\", "func"),
    (43, "                    (lockout_score * 0.25) + (expiration_score * 0.15) + \\", "func"),
    (44, "                    (history_score * 0.10) + (defense_depth_score * 0.10)", "func"),
    (45, "    grade = 'A+' if overall_score >= 95 else 'A' if overall_score >= 85 else \\", "keyword"),
    (46, "            'B' if overall_score >= 75 else 'C' if overall_score >= 60 else 'F'", "keyword"),
    (47, "    risk_level = 'Low' if overall_score >= 85 else 'Moderate' if overall_score >= 70 else 'Critical'", "keyword"),
    (48, "    return EvaluationReport(score=overall_score, grade=grade, risk_level=risk_level, findings=findings)", "func"),
]
render_code_card("Automated Compliance & Risk Scoring Engine", "backend/compliance_engine.py", code_func1, "code_function1_compliance.png")

# -------------------------------------------------------------
# 2. CODE SNIPPET 2: Runtime Policy Enforcement & Lockout Guard
# -------------------------------------------------------------
code_func2 = [
    (24, "# Runtime password validation enforcing active organizational rules", "comment"),
    (25, "def validate_password(password: str, email: str, policy: PolicyInput, db: Session, user_id: int):", "keyword"),
    (26, "    problems = []", "plain"),
    (27, "    if len(password) < policy.min_length:", "keyword"),
    (28, "        problems.append(f'Password must contain at least {policy.min_length} characters')", "string"),
    (29, "    if policy.disallow_common and password.lower() in BREACHED_COMMON_DICTIONARY:", "keyword"),
    (30, "        problems.append('Password is known to be breached or too common; choose a stronger passphrase')", "string"),
    (31, "", "plain"),
    (32, "    # Historical Hash Retention Depth Check (Password Reuse Prevention)", "comment"),
    (33, "    if user_id and policy.password_history_count > 0:", "keyword"),
    (34, "        recent_hashes = db.query(PasswordHistory).filter(PasswordHistory.user_id == user_id)\\", "func"),
    (35, "                          .order_by(PasswordHistory.id.desc()).limit(policy.password_history_count).all()", "func"),
    (36, "        if any(verify_password(password, h.password_hash) for h in recent_hashes):", "keyword"),
    (37, "            problems.append('Password reuse violation: you cannot reuse your recent passwords.')", "alert"),
    (38, "", "plain"),
    (39, "    # Account Lockout & Brute-Force Rate Limiting (main.py)", "comment"),
    (40, "    if not verify_password(creds.password, user.hashed_password):", "keyword"),
    (41, "        state.failed_attempts += 1", "alert"),
    (42, "        state.last_failed_at = datetime.datetime.utcnow()", "plain"),
    (43, "        if state.failed_attempts >= policy.max_failed_attempts:", "keyword"),
    (44, "            state.locked_until = now + datetime.timedelta(minutes=policy.lockout_duration_min)", "alert"),
    (45, "            state.failed_attempts = 0  # Trigger defensive account freeze", "comment"),
    (46, "        db.commit()", "plain"),
]
render_code_card("Runtime Policy Enforcement & Account Lockout Defense", "backend/policy_enforcement.py", code_func2, "code_function2_lockout_enforcement.png")

# -------------------------------------------------------------
# 3. CODE SNIPPET 3: Role-Based Access Control (RBAC) & JWT
# -------------------------------------------------------------
code_func3 = [
    (38, "# Cryptographic JWT Token Generation and Role Verification", "comment"),
    (39, "def create_access_token(data: dict, expires_delta: timedelta = None) -> str:", "keyword"),
    (40, "    to_encode = data.copy()", "plain"),
    (41, "    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))", "plain"),
    (42, "    to_encode.update({'exp': expire, 'iat': datetime.utcnow()})", "plain"),
    (43, "    return jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')", "func"),
    (44, "", "plain"),
    (45, "# Role-Based Access Control (RBAC) Dependency Factory", "comment"),
    (46, "def require_role(allowed_roles: list[str]):", "keyword"),
    (47, "    def role_checker(current_user: User = Depends(get_current_user)) -> User:", "keyword"),
    (48, "        if current_user.role not in allowed_roles:", "keyword"),
    (49, "            raise HTTPException(", "keyword"),
    (50, "                status_code=status.HTTP_403_FORBIDDEN,", "alert"),
    (51, "                detail=f'Access Denied: Action restricted to roles: {allowed_roles}'", "string"),
    (52, "            )", "keyword"),
    (53, "        return current_user", "keyword"),
    (54, "    return role_checker", "keyword"),
    (55, "", "plain"),
    (56, "require_admin = require_role(['Administrator'])", "security"),
    (57, "require_analyst_or_admin = require_role(['Administrator', 'Security Analyst'])", "security"),
    (58, "", "plain"),
    (59, "@app.post('/api/standards', dependencies=[Depends(require_admin)]) # RBAC Protected", "func"),
    (60, "def update_security_standards(standard: StandardUpdate, db: Session = Depends(get_db)):", "keyword"),
    (61, "    return service.update_standard_definition(db, standard)", "plain"),
]
render_code_card("Role-Based Access Control (RBAC) & JWT Security", "backend/auth.py", code_func3, "code_function3_rbac_jwt.png")

# -------------------------------------------------------------
# 4. CODE SNIPPET 4: Audit Logging & Comparative Analysis
# -------------------------------------------------------------
code_func4 = [
    (142, "# Immutable Security Audit Trail Logger", "comment"),
    (143, "def log_audit_event(action: str, details: str, user_name: str, user_role: str,", "keyword"),
    (144, "                    ip_address: str, score_snapshot: float = None, db: Session = None):", "keyword"),
    (145, "    audit_entry = AuditLog(", "security"),
    (146, "        action=action,              # E.g., 'POLICY_EVALUATION', 'USER_LOCKOUT', 'STANDARDS_MODIFIED'", "string"),
    (147, "        details=details,            # Full cryptographic context and description", "string"),
    (148, "        user_name=user_name,        # Operator or system identity", "string"),
    (149, "        user_role=user_role,        # RBAC role verification tier", "string"),
    (150, "        ip_address=ip_address,      # Originating client IP address", "string"),
    (151, "        score_snapshot=score_snapshot,", "plain"),
    (152, "        timestamp=datetime.utcnow() # Tamper-evident UTC timestamp", "func"),
    (153, "    )", "security"),
    (154, "    db.add(audit_entry)", "plain"),
    (155, "    db.commit()", "plain"),
    (156, "", "plain"),
    (157, "# Comparative Policy Analysis Endpoint", "comment"),
    (158, "@app.post('/api/policies/compare', response_model=PolicyComparisonReport)", "func"),
    (159, "def compare_policy_profiles(policy_ids: list[int], standard_id: str, db: Session = Depends(get_db)):", "keyword"),
    (160, "    \"\"\"Compares multiple policy revisions side-by-side against standard benchmarks.\"\"\"", "string"),
    (161, "    reports = [evaluate_saved_policy(db, pid, standard_id) for pid in policy_ids]", "plain"),
    (162, "    return generate_matrix_comparison(reports)", "func"),
]
render_code_card("Immutable Audit Logging & Policy Comparison", "backend/main.py", code_func4, "code_function4_audit_compare.png")

# -------------------------------------------------------------
# 5. HIGH-RESOLUTION NETWORK TOPOLOGY DIAGRAM
# -------------------------------------------------------------
def generate_network_topology():
    w, h = 1400, 950
    img = Image.new("RGB", (w, h), color="#0f172a") # Slate-900 background
    draw = ImageDraw.Draw(img)

    # Outer decorative header
    draw.rectangle([(0, 0), (w, 70)], fill="#1e293b")
    draw.line([(0, 70), (w, 70)], fill="#334155", width=2)
    font_head = get_font(22, bold=True)
    font_subhead = get_font(13)
    draw.text((35, 15), "NETWORK TOPOLOGY: TIERED SECURE HYBRID WEB ARCHITECTURE", fill="#38bdf8", font=font_head)
    draw.text((35, 45), "#23 PasswordPolicy Checker  •  Systems Administration and Maintenance – IT23/L", fill="#94a3b8", font=font_subhead)

    # 4 Main Zone Boxes
    # Box 1: User Access Zone (Clients)
    draw.rounded_rectangle([(40, 95), (320, 900)], radius=12, fill="#1e293b", outline="#3b82f6", width=2)
    draw.rectangle([(40, 95), (320, 140)], fill="#1d4ed8")
    font_box_title = get_font(15, bold=True)
    draw.text((55, 108), "CLIENT ACCESS ZONE", fill="#ffffff", font=font_box_title)

    # Client Workstations
    clients = [
        ("System Administrator", "VLAN 10 • 192.168.10.25\nFull RBAC Controls\nActive Directory / Web Admin", "#22c55e"),
        ("Security Analyst", "VLAN 15 • 192.168.15.40\nPolicy Auditing / Evaluation\nReport Export (PDF/CSV)", "#06b6d4"),
        ("IT Compliance Auditor", "VLAN 30 • 192.168.30.50\nRead-Only Dashboard\nAudit Trail Review", "#eab308"),
        ("Institutional Workstations", "VLAN 40 • 192.168.40.0/24\nEnd-User Password Updates\nSelf-Service Credential Reset", "#a855f7")
    ]
    y_c = 160
    for name, desc, col in clients:
        draw.rounded_rectangle([(60, y_c), (300, y_c + 155)], radius=8, fill="#0f172a", outline=col, width=2)
        draw.text((75, y_c + 12), name, fill=col, font=get_font(14, bold=True))
        draw.text((75, y_c + 38), desc, fill="#cbd5e1", font=get_font(12))
        draw.text((75, y_c + 125), "🔒 TLS 1.3 / HTTPS (Port 443)", fill="#64748b", font=get_font(10, mono=True))
        y_c += 180

    # Box 2: Perimeter / Edge & WAF Zone
    draw.rounded_rectangle([(370, 95), (650, 900)], radius=12, fill="#1e293b", outline="#ef4444", width=2)
    draw.rectangle([(370, 95), (650, 140)], fill="#b91c1c")
    draw.text((385, 108), "PERIMETER & EDGE DMZ", fill="#ffffff", font=font_box_title)

    edges = [
        ("Next-Gen Firewall (NGFW)", "Stateful Packet Inspection\nDDoS Mitigation & Rate Limiting\nIPS/IDS Traffic Analysis", "#f87171"),
        ("Vercel Edge Network / WAF", "TLS Termination (Port 443)\nHTTPS Strict Transport (HSTS)\nOWASP Core Rule Set Filtering", "#fb923c"),
        ("React Static Frontend CDN", "Single Page Application (SPA)\nClient-Side Route Handling\nChart.js Analytics Rendering", "#38bdf8"),
        ("Secure Reverse Proxy", "API Gateway Routing (/api/*)\nOrigin Shielding & Header Sanitization\nCORS Policy Enforcement", "#fbbf24")
    ]
    y_e = 160
    for name, desc, col in edges:
        draw.rounded_rectangle([(390, y_e), (630, y_e + 155)], radius=8, fill="#0f172a", outline=col, width=2)
        draw.text((405, y_e + 12), name, fill=col, font=get_font(14, bold=True))
        draw.text((405, y_e + 38), desc, fill="#cbd5e1", font=get_font(12))
        draw.text((405, y_e + 125), "🛡️ Perimeter Defense Active", fill="#64748b", font=get_font(10, mono=True))
        y_e += 180

    # Box 3: Application Server Zone (FastAPI Logic)
    draw.rounded_rectangle([(700, 95), (1010, 900)], radius=12, fill="#1e293b", outline="#8b5cf6", width=2)
    draw.rectangle([(700, 95), (1010, 140)], fill="#6d28d9")
    draw.text((715, 108), "APPLICATION & LOGIC TIER", fill="#ffffff", font=font_box_title)

    apps = [
        ("FastAPI Application Server", "Uvicorn ASGI Engine\nPython 3.14 Runtime\nPrivate IP: 192.168.20.10", "#c084fc"),
        ("Compliance Evaluation Engine", "NIST SP 800-63B Benchmarking\nOWASP ASVS & CIS Scoring\nWeighted Multi-Factor Matrix", "#a855f7"),
        ("Authentication & RBAC Guard", "BCrypt Salted Password Hashing\nHMAC-SHA256 JWT Management\nDefensive Account Lockout Controller", "#ec4899"),
        ("Active Directory / LDAP Link", "Enterprise Group Policy Auditor\nLDAPS (Secure Port 636)\nNo Raw Passwords Stored / Intercepted", "#818cf8")
    ]
    y_a = 160
    for name, desc, col in apps:
        draw.rounded_rectangle([(720, y_a), (990, y_a + 155)], radius=8, fill="#0f172a", outline=col, width=2)
        draw.text((735, y_a + 12), name, fill=col, font=get_font(14, bold=True))
        draw.text((735, y_a + 38), desc, fill="#cbd5e1", font=get_font(12))
        draw.text((735, y_a + 125), "⚙️ Isolated Application DMZ", fill="#64748b", font=get_font(10, mono=True))
        y_a += 180

    # Box 4: Database & Storage Tier (PostgreSQL)
    draw.rounded_rectangle([(1060, 95), (1360, 900)], radius=12, fill="#1e293b", outline="#10b981", width=2)
    draw.rectangle([(1060, 95), (1360, 140)], fill="#047857")
    draw.text((1075, 108), "DATA & STORAGE TIER", fill="#ffffff", font=font_box_title)

    dbs = [
        ("Supabase Cloud PostgreSQL", "Managed Relational Database\nAWS VPC Dedicated Subnet\nPort 6543 / 5432 (SSL Required)", "#34d399"),
        ("Relational Data Schemas", "• users (Bcrypt Hashes)\n• policy_settings (Profiles)\n• standard_definitions (NIST/OWASP)", "#6ee7b7"),
        ("Immutable Security Records", "• evaluation_reports (Scores & Logs)\n• audit_logs (Tamper-Evident)\n• login_state & password_history", "#a7f3d0"),
        ("Database Security Controls", "Row-Level Security (RLS)\nStrict IP Whitelisting\nEncrypted at Rest & In-Transit", "#10b981")
    ]
    y_d = 160
    for name, desc, col in dbs:
        draw.rounded_rectangle([(1080, y_d), (1340, y_d + 155)], radius=8, fill="#0f172a", outline=col, width=2)
        draw.text((1095, y_d + 12), name, fill=col, font=get_font(14, bold=True))
        draw.text((1095, y_d + 38), desc, fill="#cbd5e1", font=get_font(12))
        draw.text((1095, y_d + 125), "🔒 Encrypted PostgreSQL", fill="#64748b", font=get_font(10, mono=True))
        y_d += 180

    # Connecting directional arrows between tiers
    # Between Tier 1 and Tier 2
    for arrow_y in [235, 415, 595, 775]:
        draw.line([(302, arrow_y), (368, arrow_y)], fill="#38bdf8", width=3)
        draw.polygon([(368, arrow_y), (360, arrow_y - 5), (360, arrow_y + 5)], fill="#38bdf8")

    # Between Tier 2 and Tier 3
    for arrow_y in [235, 415, 595, 775]:
        draw.line([(632, arrow_y), (698, arrow_y)], fill="#f59e0b", width=3)
        draw.polygon([(698, arrow_y), (690, arrow_y - 5), (690, arrow_y + 5)], fill="#f59e0b")

    # Between Tier 3 and Tier 4
    for arrow_y in [235, 415, 595, 775]:
        draw.line([(992, arrow_y), (1058, arrow_y)], fill="#10b981", width=3)
        draw.polygon([(1058, arrow_y), (1050, arrow_y - 5), (1050, arrow_y + 5)], fill="#10b981")

    # Save diagram
    topo_path = os.path.join(ASSETS_DIR, "network_topology_diagram.png")
    img.save(topo_path, quality=95)
    print(f"Generated Network Topology diagram: {topo_path}")
    return topo_path

generate_network_topology()
print("All asset generation complete!")
