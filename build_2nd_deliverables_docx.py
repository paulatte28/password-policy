import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

TEMPLATE_PATH = r"c:\Users\Admin\Downloads\IT23_2ndDeliverables_Functions.docx"
OUTPUT_PATH1 = r"c:\Users\Admin\Downloads\IT23_2ndDeliverables_Functions.docx"
OUTPUT_PATH2 = r"c:\Users\Admin\Downloads\CORETICO_IT23_2ndDeliverables.docx"
OUTPUT_PATH3 = r"c:\Users\Admin\Documents\4th Year\IT23\password-policy\CORETICO_IT23_2ndDeliverables.docx"

ASSETS_DIR = os.path.abspath("generated_report_assets")
SCREENSHOTS_DIR = os.path.abspath("screenshots")
PRESERVED_DIR = os.path.abspath("preserved_assets")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def clear_cell(cell):
    p = cell.paragraphs[0]
    p.text = ""
    for p_extra in cell.paragraphs[1:]:
        p_extra._element.getparent().remove(p_extra._element)

def add_heading(cell, text, level=1):
    if len(cell.paragraphs) == 1 and cell.paragraphs[0].text == "":
        p = cell.paragraphs[0]
    else:
        p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(6) if level == 1 else Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.bold = True
    run.font.name = "Calibri"
    run.font.size = Pt(10.5) if level == 1 else Pt(9.5)
    run.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A) if level == 1 else RGBColor(0x1E, 0x3A, 0x8A)
    return p

def add_paragraph(cell, text="", bold_prefix="", space_before=0, space_after=3):
    if len(cell.paragraphs) == 1 and cell.paragraphs[0].text == "":
        p = cell.paragraphs[0]
    else:
        p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.bold = True
        r_b.font.name = "Calibri"
        r_b.font.size = Pt(9.5)
        r_b.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)
    if text:
        r_t = p.add_run(text)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(9.5)
        r_t.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_bullet(cell, title, desc):
    p = cell.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.18)
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    
    r_bullet = p.add_run("▪ ")
    r_bullet.bold = True
    r_bullet.font.name = "Calibri"
    r_bullet.font.size = Pt(9.5)
    r_bullet.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)

    r_title = p.add_run(f"{title}: ")
    r_title.bold = True
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(9.5)
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    r_desc = p.add_run(desc)
    r_desc.font.name = "Calibri"
    r_desc.font.size = Pt(9.5)
    r_desc.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    return p

def add_image_with_caption(cell, img_path, width=Inches(5.0), caption=""):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(img_path, width=width)
    if caption:
        p_cap = cell.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1)
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run(caption)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(8.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

def populate_deliverables_document():
    doc = docx.Document(TEMPLATE_PATH)
    t = doc.tables[0]

    # ROW 0: Title Header
    c0 = t.rows[0].cells[0]
    c1 = t.rows[0].cells[1]
    # Keep row 0 text clean
    c0.paragraphs[0].text = "Security Functions and Network Layout -2nd Deliverables"
    c0.paragraphs[0].runs[0].font.bold = True
    c0.paragraphs[0].runs[0].font.size = Pt(14)
    c0.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_cell_background(c0, "F1F5F9")
    if c1 != c0:
        c1.paragraphs[0].text = "Security Functions and Network Layout -2nd Deliverables"
        set_cell_background(c1, "F1F5F9")

    # ROW 1: NAME
    clear_cell(t.rows[1].cells[0])
    add_paragraph(t.rows[1].cells[0], bold_prefix="NAME")
    clear_cell(t.rows[1].cells[1])
    p1 = add_paragraph(t.rows[1].cells[1], bold_prefix="KRISTINE PAULA S. CORETICO")
    p1.runs[0].font.size = Pt(13)

    # ROW 2: PROJECT TITLE (specific)
    clear_cell(t.rows[2].cells[0])
    add_paragraph(t.rows[2].cells[0], bold_prefix="PROJECT TITLE\n(specific)")
    clear_cell(t.rows[2].cells[1])
    p2 = add_paragraph(t.rows[2].cells[1], bold_prefix="PasswordPolicy Checker: A Web-Based System for Evaluating Password Policy Compliance and Security Risks")
    p2.runs[0].font.size = Pt(11)

    # ROW 3: SUBJECT / CODE / TIME
    clear_cell(t.rows[3].cells[0])
    add_paragraph(t.rows[3].cells[0], bold_prefix="SUBJECT:\nCODE:\nTIME:")
    clear_cell(t.rows[3].cells[1])
    add_paragraph(t.rows[3].cells[1], text="System Administration and Maintenance – IT23/L\n3493\n7:30-9:30PM")

    # ROW 4: PROJECT NAME
    clear_cell(t.rows[4].cells[0])
    add_paragraph(t.rows[4].cells[0], bold_prefix="PROJECT NAME")
    clear_cell(t.rows[4].cells[1])
    add_paragraph(t.rows[4].cells[1], bold_prefix="#23 PasswordPolicy Checker")

    # ROW 5: Project Overview
    clear_cell(t.rows[5].cells[0])
    add_paragraph(t.rows[5].cells[0], bold_prefix="Project Overview")
    c5 = t.rows[5].cells[1]
    clear_cell(c5)

    add_heading(c5, "Project Description, Purpose, and Scope:")
    add_paragraph(c5, "PasswordPolicy Checker (#23) is a web-based compliance evaluation system built for system administrators, IT security analysts, and compliance auditors. Its purpose is to evaluate organizational password policy settings—including minimum length, character complexity, account lockout thresholds, password expiration, password history depth, and defense-in-depth hygiene—against established cybersecurity standards (NIST SP 800-63B, OWASP ASVS, and CIS Benchmarks). The system computes a compliance score (0–100), assigns a letter grade (A+ to F) and risk level, and outputs actionable findings. The scope is strictly limited to policy configuration evaluation: the system never requests, tests, or stores real user passwords.")

    add_heading(c5, "Relevant Real-World Cyberattack:")
    add_paragraph(c5, "Colonial Pipeline Ransomware Attack (2021): In May 2021, Colonial Pipeline Company suffered a major DarkSide ransomware intrusion after attackers accessed a legacy VPN account using a single-factor password found in a dark web breach dump.")
    add_bullet(c5, "Source Citations", "CISA & FBI Joint Cybersecurity Advisory AA21-131A (https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-131a); U.S. Senate Homeland Security Committee Testimony of CEO Joseph Blount (June 8, 2021); Mandiant Incident Response Findings (2021).")
    add_bullet(c5, "Verified Facts", "Attackers entered via an inactive legacy VPN account that lacked Multi-Factor Authentication (MFA), used a previously leaked/reused password, and had no automated expiration or breach screening—forcing a 6-day shutdown of 5,500 miles of U.S. fuel pipeline and a 75-Bitcoin (~$4.4M) ransom payment.")
    add_bullet(c5, "Proposed System Features", "PasswordPolicy Checker directly evaluates password policy settings to catch these exact gaps before an attack occurs—flagging missing MFA, zero password history/reuse limits, disabled breached/common dictionary checks, weak minimum lengths (< 8 chars), and missing account lockout controls.")

    add_heading(c5, "Objectives: (as is)")
    add_paragraph(c5, "• Document and analyze selected real-world Cyberattacks.\n• Identify the attack methods, vulnerabilities, and impact.\n• Present the incident response and mitigation actions taken.\n• Derive lessons learned and security recommendation.")

    # ROW 6: Case Study basis (Nested 2-column table matching template format)
    clear_cell(t.rows[6].cells[0])
    add_paragraph(t.rows[6].cells[0], bold_prefix="Case Study basis")
    c6 = t.rows[6].cells[1]
    clear_cell(c6)

    case_rows = [
        (
            "Real-world incident",
            "Name: Colonial Pipeline Ransomware Attack\n"
            "Year: 2021 (April 29 – May 12, 2021)\n"
            "Affected Organization: Colonial Pipeline Company (USA)\n"
            "Credible Sources:\n"
            "• CISA & FBI Joint Advisory AA21-131A: https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-131a\n"
            "• U.S. Senate Committee on Homeland Security Testimony of CEO Joseph Blount (June 8, 2021)\n"
            "• Mandiant Forensic Investigation Report (June 2021)"
        ),
        (
            "Attack analysis (own)",
            "• Attack Type: Credential compromise (password reuse from dark web leak) followed by DarkSide Ransomware-as-a-Service (RaaS) deployment and double extortion.\n"
            "• Entry Point: An inactive legacy employee VPN account that remained enabled on the external gateway without Multi-Factor Authentication (MFA).\n"
            "• Vulnerabilities: Password reuse across external breaches, absence of MFA, lack of breached-password screening, and failure to expire or deactivate dormant credentials.\n"
            "• Impact: 6-day shutdown of 5,500 miles of fuel pipeline supplying ~45% of the U.S. East Coast's fuel, widespread supply shortages, federal emergency declaration across 18 states, 100 GB of data stolen, and 75 Bitcoin (~$4.4M) ransom paid.\n"
            "• Timeline: Apr 29, 2021 (initial VPN login via leaked password) → May 6, 2021 (~100 GB exfiltrated) → May 7, 2021 (ransomware executed; pipeline shut down) → May 12, 2021 (operations restarted) → Jun 7, 2021 (DOJ/FBI seized 63.7 BTC)."
        ),
        (
            "Response and lessons learned (own)",
            "• Detection & Containment: Upon discovering the ransom note on May 7, Colonial Pipeline disconnected IT from Operational Technology (OT) systems, halted all pipeline operations to prevent spread, and engaged Mandiant, CISA, and the FBI.\n"
            "• Recovery: Paid initial ransom to obtain a decryption tool, restored enterprise billing/IT systems from backups, and resumed pipeline flow by May 12, 2021; DOJ later recovered 63.7 BTC.\n"
            "• Preventive Controls: Decommissioned all legacy single-factor VPN accounts, enforced phishing-resistant MFA, mandated enterprise-wide password resets, banned breached/reused passwords, and instituted regular policy and account audits."
        ),
        (
            "Project connection (own)",
            "PasswordPolicy Checker (#23) directly addresses the root policy failures behind the Colonial Pipeline breach by auditing organizational password rules against NIST SP 800-63B, OWASP ASVS, and CIS Benchmarks:\n"
            "• Prevents Password Reuse & Weak Passwords: Flags password_history_count = 0, disabled common/breached dictionary checks, and short minimum lengths (< 8 chars) as security failures.\n"
            "• Enforces MFA & Lockout Hygiene: Checks whether Multi-Factor Authentication (require_mfa) and failed-attempt account lockout thresholds (max_failed_attempts) are configured.\n"
            "• Supports Continuous Auditing: Provides a mathematical compliance score (0–100), risk level, actionable recommendations, and an immutable audit log so administrators catch policy gaps before attackers exploit them."
        ),
    ]

    nested = c6.add_table(rows=len(case_rows), cols=2)
    nested.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = nested._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        '</w:tblBorders>'
    )
    tblPr.append(borders)

    for idx, (label, body) in enumerate(case_rows):
        row = nested.rows[idx]
        left_cell = row.cells[0]
        right_cell = row.cells[1]
        left_cell.width = Inches(1.45)
        right_cell.width = Inches(3.85)
        set_cell_background(left_cell, "F1F5F9")
        clear_cell(left_cell)
        clear_cell(right_cell)
        add_paragraph(left_cell, bold_prefix=label, space_before=2, space_after=2)
        add_paragraph(right_cell, text=body, space_before=2, space_after=2)

    # ROW 7: Technologies and Framework
    clear_cell(t.rows[7].cells[0])
    add_paragraph(t.rows[7].cells[0], bold_prefix="Technologies and Framework:")
    c7 = t.rows[7].cells[1]
    clear_cell(c7)

    add_paragraph(c7, "Programming Language", bold_prefix="• ")
    add_paragraph(c7, "- Python (FastAPI backend, compliance engine, policy evaluation, BCrypt hashing)\n- JavaScript (ES6+, React, Vite, Chart.js interactive charts)\n- SQL (PostgreSQL relational schema and migrations)")

    add_paragraph(c7, "Backend Technologies & Security Libraries", bold_prefix="• ")
    add_paragraph(c7, "- FastAPI (High-performance asynchronous Python web framework)\n- SQLAlchemy (Object Relational Mapping for relational database management)\n- Pydantic & Pydantic-Settings (Data validation, schema enforcement, environment parsing)\n- Passlib & BCrypt (Salted cryptographic password hashing and verification)\n- PyJWT (JSON Web Token generation, expiration, and cryptographic signature validation)\n- Uvicorn (ASGI web server implementation)")

    add_paragraph(c7, "Frontend Technologies & UI Libraries", bold_prefix="• ")
    add_paragraph(c7, "- React (Component-based user interface architecture)\n- Vite (Next-generation high-speed frontend build tool and development server)\n- HTML5 & CSS3 (Modern responsive cybersecurity UI design tokens)\n- Chart.js & React-Chartjs-2 (Dynamic data visualization, radar charts, score distribution charts)\n- Lucide React (Cybersecurity UI iconography)")

    add_paragraph(c7, "Database & Cloud Infrastructure", bold_prefix="• ")
    add_paragraph(c7, "- Supabase PostgreSQL (Managed cloud relational database with connection pooling and SSL encryption)\n- SQLite (Embedded relational database for local development and offline testing)\n- Vercel (Production cloud deployment and edge serverless hosting)")

    add_paragraph(c7, "Development & Collaboration Tools", bold_prefix="• ")
    add_paragraph(c7, "- Visual Studio Code (Primary Integrated Development Environment)\n- Git & GitHub (Version control, branch management, CI/CD automated keepalive workflows)\n- Swagger UI / OpenAPI (Interactive RESTful API documentation at /docs)")

    # ROW 8: Detection Techniques
    clear_cell(t.rows[8].cells[0])
    add_paragraph(t.rows[8].cells[0], bold_prefix="Detection Techniques\n(Policy Checks)")
    c8 = t.rows[8].cells[1]
    clear_cell(c8)

    add_bullet(c8, "Password Length & Minimum Entropy Evaluation", "Evaluates minimum length settings against industry benchmarks (NIST SP 800-63B recommends ≥ 8 characters for general users, ≥ 15 for administrative accounts; CIS Benchmark mandates ≥ 14 characters). Passwords < 8 characters are flagged as Critical Failures due to vulnerability to precomputed rainbow table and GPU-accelerated hash cracking.")
    add_bullet(c8, "Password Complexity & Character Diversity Verification", "Analyzes requirements for uppercase letters, lowercase letters, numeric digits, and special symbols. Evaluates minimum character categories required; balances brute-force keyspace expansion with NIST usability recommendations against overly burdensome composition rules that cause user workarounds.")
    add_bullet(c8, "Account Lockout & Brute-Force Rate Limiting Analysis", "Evaluates failed-attempt thresholds (maximum failed attempts before lockout) and lockout durations (in minutes). Detects vulnerability to automated online password guessing, dictionary attacks, and distributed password spraying. Policies with 0 lockout or no threshold are flagged as Critical Failures.")
    add_bullet(c8, "Password Expiration & Lifecycle Aging Assessment", "Evaluates maximum password validity age (e.g., 90 days vs NIST guidance). Flags obsolete policies that mandate frequent arbitrary password changes (e.g., every 30-60 days) which research proves leads users to select predictable incrementing patterns (e.g., Spring2026!), while ensuring minimum age controls prevent rapid cycling through password history.")
    add_bullet(c8, "Password Reuse & Historical Retention Depth Detection", "Analyzes the depth of retained previous password hashes (password_history_count). Flags policy gaps where historical depth is 0 or < 5, enabling users to immediately revert to old or compromised passwords following a forced reset.")
    add_bullet(c8, "Defense-in-Depth & Breached Dictionary Screening", "Checks whether policy mandates screening against common/known breached password dictionaries (such as RockYou and HaveIBeenPwned corpora). Validates exclusion of usernames, system identifiers, and predictable institutional names, alongside Multi-Factor Authentication (MFA) enforcement.")

    # ROW 9: Required Data
    clear_cell(t.rows[9].cells[0])
    add_paragraph(t.rows[9].cells[0], bold_prefix="Required Data")
    c9 = t.rows[9].cells[1]
    clear_cell(c9)

    add_paragraph(c9, "Sample Data Structures Implemented in System Database:", bold_prefix="• ")
    add_bullet(c9, "User Information (users table)", "Stores administrative accounts, roles, departments, and active statuses. Passwords stored strictly as salted BCrypt hashes ($2b$12$...). Sample: { id: 1, email: 'admin@passwordpolicy.local', full_name: 'Kristine Paula S. Coretico', role: 'Administrator', department: 'Systems Administration & Security Unit', is_active: True }")
    add_bullet(c9, "Policy Configuration Profiles (policy_settings table)", "Stores password policy configurations across all 6 dimensions. Sample: { id: 1, name: 'Enterprise Baseline Policy', min_length: 12, max_length: 64, require_uppercase: True, require_digit: True, max_failed_attempts: 5, lockout_duration_min: 15, password_history_count: 5, require_mfa: True }")
    add_bullet(c9, "Standard Definitions (standard_definitions table)", "Benchmark thresholds for NIST SP 800-63B, OWASP ASVS, CIS Benchmark, and Custom Organizational Standards. Sample: { id: 'NIST_SP_800_63B', name: 'NIST SP 800-63B Guidelines', publisher: 'NIST', recommended_min_length: 12, max_failed_attempts_threshold: 5, min_lockout_duration_minutes: 15, recommended_max_password_age_days: 0, requires_breached_dictionary_check: True }")
    add_bullet(c9, "Evaluation Reports & Compliance Metrics (evaluation_reports table)", "Compliance assessment records containing scores, letter grades, risk levels, and findings. Sample: { id: 5, policy_name: 'Enterprise Password Policy', standard_name: 'NIST SP 800-63B Guidelines', overall_compliance_score: 98.0, grade_letter: 'A+', risk_level: 'Low', evaluated_by_user: 'Alex Vance', evaluated_at: '2026-11-14 06:27:52' }")
    add_bullet(c9, "System Activity Logs (audit_logs table)", "Immutable audit records tracking all system operations: action type, description, actor identity, user role, client IP address, score snapshot, and UTC timestamp. Sample: { id: 34, action: 'POLICY_EVALUATION', details: 'Evaluated policy against NIST SP 800-63B. Score: 98.0% (A+)', user_name: 'Alex Vance', user_role: 'Security Analyst', ip_address: '127.0.0.1', timestamp: '2026-11-14 06:27:52' }")

    # ROW 10: Target Users
    clear_cell(t.rows[10].cells[0])
    add_paragraph(t.rows[10].cells[0], bold_prefix="Target Users")
    c10 = t.rows[10].cells[1]
    clear_cell(c10)
    add_bullet(c10, "System Administrators", "Network and systems administrators responsible for managing Windows Active Directory Group Policy Objects (GPO), Linux PAM configurations, and cloud identity access management systems.")
    add_bullet(c10, "IT Security Officers / Cybersecurity Analysts", "Information security teams evaluating institutional credential hygiene, conducting vulnerability assessments, and defining organizational baseline standards.")
    add_bullet(c10, "IT Auditors & Compliance Officers", "Internal and external auditors validating organizational compliance against regulatory frameworks such as NIST SP 800-63B, ISO/IEC 27001, PCI-DSS, and HIPAA.")
    add_bullet(c10, "Educational Institutions (IT Departments)", "University and collegiate IT departments managing campus networks, student information systems (SIS), faculty portals, and laboratory authentication services.")
    add_bullet(c10, "IT Students, Educators, and Trainers", "Academic instructors and students in Systems Administration and Maintenance (IT23/L) studying identity security, password entropy, and brute-force mitigation.")

    # ROW 11: User Roles (RBAC)
    clear_cell(t.rows[11].cells[0])
    add_paragraph(t.rows[11].cells[0], bold_prefix="User Roles\n(RBAC)")
    c11 = t.rows[11].cells[1]
    clear_cell(c11)

    add_bullet(c11, "Administrator", "• Provision, manage, and deactivate user accounts and assign RBAC roles (Administrator, Security Analyst, Viewer).\n• Edit and customize security standard thresholds and benchmarks (NIST, OWASP, CIS, Custom Organization baseline).\n• Access all policy evaluations, comparative analytics, and immutable system audit logs.")
    add_bullet(c11, "Security Analyst", "• Create, configure, test, and import password policy settings (via JSON/CSV or interactive form).\n• Select security standards and execute automated compliance evaluations.\n• Review detailed vulnerability findings, risk severities, and remediation recommendations.\n• Compare policies side-by-side and export formal audit reports in PDF and CSV formats.")
    add_bullet(c11, "Viewer / Auditor", "• Read-only access to the central security dashboard and analytics overview.\n• Review historical evaluation reports, compliance trends, and published audit scores.\n• Cannot modify policies, alter security standards, or change user account configurations.")

    # ROW 12: Preserved as blank spacer row exactly as in template IT23_2ndDeliverables_Functions.docx
    clear_cell(t.rows[12].cells[0])
    clear_cell(t.rows[12].cells[1])

    # ROW 13: Security Function 1
    clear_cell(t.rows[13].cells[0])
    add_paragraph(t.rows[13].cells[0], bold_prefix="Security Functions\n(NAME and Description)\n\n(Screenshot – UI and Codes)")
    c13 = t.rows[13].cells[1]
    clear_cell(c13)

    add_heading(c13, "Security Function 1: Automated Multi-Standard Compliance Evaluation Engine & Risk Scoring")
    add_paragraph(c13, "Description: Evaluates password policy settings (length, complexity, lockout, expiration, reuse, and hygiene) against standards like NIST SP 800-63B, OWASP, and CIS. It calculates a compliance score from 0 to 100, assigns a letter grade (A+ to F), and provides clear Pass, Warning, or Fail findings with recommendations to fix security gaps.")
    
    ui_fn1 = os.path.join(SCREENSHOTS_DIR, "ui_function1_evaluation_report.png")
    if os.path.exists(ui_fn1):
        add_image_with_caption(c13, ui_fn1, width=Inches(5.1), caption="UI Screenshot 1: Evaluation Report View showing 98.0% Score (A+), Dimension Breakdown, and Findings")
    
    code_fn1 = os.path.join(ASSETS_DIR, "code_function1_compliance.png")
    if os.path.exists(code_fn1):
        add_image_with_caption(c13, code_fn1, width=Inches(5.1), caption="Code Screenshot 1: backend/compliance_engine.py — Policy Evaluation & Weighted Scoring Logic")

    # ROW 14: Security Function 2
    clear_cell(t.rows[14].cells[0])
    add_paragraph(t.rows[14].cells[0], bold_prefix="Security Functions\n(NAME and Description)\n\n(Screenshot – UI and Codes)")
    c14 = t.rows[14].cells[1]
    clear_cell(c14)

    add_heading(c14, "Security Function 2: Multi-Standard Cybersecurity Benchmark Management & Baseline Configuration")
    add_paragraph(c14, "Description: Allows administrators to view and customize security baseline thresholds for NIST, OWASP, CIS, and custom organization rules. Thresholds like minimum length, failed-attempt limits, and lockout times are stored in the database, so policies can be checked against tailored institutional guidelines.")
    
    ui_fn2 = os.path.join(SCREENSHOTS_DIR, "ui_function2_standards.png")
    if os.path.exists(ui_fn2):
        add_image_with_caption(c14, ui_fn2, width=Inches(5.1), caption="UI Screenshot 2: Benchmarks / Standards Manager Interface showing NIST, OWASP, CIS, and Custom Organization Baselines")
    
    code_fn2 = os.path.join(ASSETS_DIR, "code_function2_standards.png")
    if os.path.exists(code_fn2):
        add_image_with_caption(c14, code_fn2, width=Inches(5.1), caption="Code Screenshot 2: backend/main.py — Cybersecurity Standards Management Service & Benchmark Threshold Updates")

    # ROW 15: Security Function 3
    clear_cell(t.rows[15].cells[0])
    add_paragraph(t.rows[15].cells[0], bold_prefix="Security Functions\n(NAME and Description)\n\n(Screenshot – UI and Codes)")
    c15 = t.rows[15].cells[1]
    clear_cell(c15)

    add_heading(c15, "Security Function 3: Role-Based Access Control (RBAC) & Secure JWT Session Authentication")
    add_paragraph(c15, "Description: Restricts system access across three roles: Administrator (manages users and standards), Security Analyst (evaluates policies and exports reports), and Viewer (read-only). Uses secure JWT tokens for login sessions, hashes staff passwords with salted BCrypt, and protects endpoints using role checks.")
    
    ui_fn3 = os.path.join(SCREENSHOTS_DIR, "ui_function3_user_management.png")
    if os.path.exists(ui_fn3):
        add_image_with_caption(c15, ui_fn3, width=Inches(5.1), caption="UI Screenshot 3: User Management Interface showing Staff Accounts, RBAC Role Assignments, Departments, and Status Toggles")
    
    code_fn3 = os.path.join(ASSETS_DIR, "code_function3_rbac_jwt.png")
    if os.path.exists(code_fn3):
        add_image_with_caption(c15, code_fn3, width=Inches(5.1), caption="Code Screenshot 3: backend/auth.py — BCrypt Password Hashing, JWT Generation, Token Validation & RBAC Role Enforcement")

    # ROW 16: Security Function 4
    clear_cell(t.rows[16].cells[0])
    add_paragraph(t.rows[16].cells[0], bold_prefix="Security Functions\n(NAME and Description)\n\n(Screenshot – UI and Codes)")
    c16 = t.rows[16].cells[1]
    clear_cell(c16)

    add_heading(c16, "Security Function 4: Immutable Security Audit Logging & Compliance Traceability")
    add_paragraph(c16, "Description: Automatically records all important system actions—including user logins, account updates, policy checks, and standard modifications—into an audit log table. Each entry captures the user, role, action, IP address, score snapshot, and timestamp for audit tracking and accountability.")
    
    ui_fn4 = os.path.join(SCREENSHOTS_DIR, "ui_function4_audit_logs.png")
    if os.path.exists(ui_fn4):
        add_image_with_caption(c16, ui_fn4, width=Inches(5.1), caption="UI Screenshot 4: Activity Log View showing Chronological Immutable Security Audit Trail with Actor, Role, IP, and Timestamp Badges")
    
    code_fn4 = os.path.join(ASSETS_DIR, "code_function4_audit_logs.png")
    if os.path.exists(code_fn4):
        add_image_with_caption(c16, code_fn4, width=Inches(5.1), caption="Code Screenshot 4: backend/main.py — Immutable Security Audit Logging Service (record_audit Helper & Audit Log API Endpoint)")

    # ROW 17: Network Topology (Type)
    clear_cell(t.rows[17].cells[0])
    add_paragraph(t.rows[17].cells[0], bold_prefix="Network Topology\n(Type)")
    c17 = t.rows[17].cells[1]
    clear_cell(c17)

    topo_img = os.path.abspath("topology_3tier_horizontal.png")
    if os.path.exists(topo_img):
        add_image_with_caption(c17, topo_img, width=Inches(5.2), caption="Figure 2: 3-Tier Web Architecture Topology — #23 PasswordPolicy Checker")

    add_heading(c17, "Network Topology Type: 3-Tier Web Architecture (Hierarchical Client-Server Model)")
    add_paragraph(c17, "Discuss your plans and how you intend to implement this in your project:")
    add_paragraph(c17, "The system implements a standard, clean 3-Tier Web Architecture. This separates the user interface, business logic, and database into three distinct, manageable layers. This structure keeps the system simple to understand, modular, and easy to maintain.")

    add_bullet(c17, "Tier 1: Presentation Tier (Client Web Layer)", 
               "• Users & Devices: Authorized users (Administrator, Security Analyst, Viewer) connect to the system using standard modern web browsers (Google Chrome, Microsoft Edge, Mozilla Firefox).\n"
               "• React + Vite Frontend: The user interface is built with React and Vite. It runs locally at http://localhost:5173 (and deployed in production on Vercel). It provides clean interactive forms for configuring password policy rules (minimum length, special characters, expiration days, lockout thresholds), imports JSON/CSV files, and renders visual compliance charts using Chart.js.\n"
               "• Communication: The frontend sends user requests to the backend server via HTTP/HTTPS REST API calls, transmitting data as lightweight JSON objects.")

    add_bullet(c17, "Tier 2: Application Tier (Business Logic Layer)", 
               "• FastAPI Backend Server: The core backend service is developed in Python 3.14 using the FastAPI framework, served by Uvicorn at http://localhost:8000. It processes all incoming API requests asynchronously.\n"
               "• Compliance Evaluation Engine: When a user evaluates a policy, this engine analyzes the parameters against benchmark cybersecurity standards (NIST SP 800-63B, OWASP ASVS, CIS Benchmarks). It computes a normalized risk score (0–100), assigns an audit grade (A through F), and generates specific remediation recommendations.\n"
               "• Authentication & Security Controller: Manages user login sessions using cryptographically signed JSON Web Tokens (JWT). User passwords are verified against salted BCrypt hashes. To protect against brute-force password guessing, it enforces account lockout logic after consecutive failed attempts.")

    add_bullet(c17, "Tier 3: Data Tier (Storage Layer)", 
               "• Local SQLite Database: For local development, testing, and offline demonstrations, the system uses an embedded SQLite database (passwordpolicy.db), requiring zero external configuration.\n"
               "• Cloud Supabase PostgreSQL: For production deployment, the backend connects to a managed PostgreSQL database hosted on Supabase (AWS), providing persistent storage across distributed devices.\n"
               "• Data Persistence: Both database options use SQLAlchemy ORM to safely store user accounts, customized password policies, historical password hashes (to enforce reuse limits), evaluation records, and immutable security audit logs without risking SQL injection.")

    add_bullet(c17, "Implementation Plan & Network Data Flow", 
               "1. User Action: A staff member opens their browser, signs in, and enters or uploads password policy parameters.\n"
               "2. API Transmission: The React frontend issues an HTTP POST request containing JSON data to the FastAPI backend.\n"
               "3. Processing & Evaluation: The backend validates JWT authentication, checks user permissions, executes the evaluation algorithms, and logs the security event.\n"
               "4. Database Record: The backend saves the evaluation results and audit log entries into the database via SQLAlchemy ORM.\n"
               "5. Response to Client: The backend returns the calculated score, grade, and gap analysis back to the React UI, which immediately renders interactive visual graphs for the user.")

    # ROW 18: System Flow (Final Flow)
    clear_cell(t.rows[18].cells[0])
    add_paragraph(t.rows[18].cells[0], bold_prefix="System Flow\n(Final Flow)")
    c18 = t.rows[18].cells[1]
    clear_cell(c18)

    flow_img = os.path.join(PRESERVED_DIR, "system-flow.png")
    if os.path.exists(flow_img):
        add_image_with_caption(c18, flow_img, width=Inches(4.4), caption="Figure 3: Final System Flow Architecture — #23 PasswordPolicy Checker")

    add_heading(c18, "Final System Flow Architectural Discussion:")
    add_paragraph(c18, "The system execution workflow is structured into a logical, sequential security pipeline ensuring rigorous role segregation and end-to-end data integrity:")

    add_bullet(c18, "Step 1: Authentication & Role Validation", "The user accesses the application and authenticates using their institutional email and password. The FastAPI backend verifies credentials using BCrypt salted hash matching, evaluates active account lockout states, and issues a cryptographically signed JSON Web Token (JWT) encoding user ID, email, and RBAC role. The client stores the token in secure browser storage.")
    add_bullet(c18, "Step 2: Central Security Dashboard (Home Screen)", "Upon successful authentication, the user lands on the role-aware Dashboard. The dashboard renders high-level cybersecurity health indicators, recent evaluation reports, overall compliance score averages, and active policy indicators.")
    add_bullet(c18, "Step 3: Role-Segregated Functional Paths", "• Security Analyst Path: The analyst creates or imports a password policy (JSON/CSV). The system validates input boundaries, prompts for benchmark standard selection (NIST SP 800-63B, OWASP, CIS, Custom), and triggers the Compliance Engine. The engine audits length, complexity, lockout, expiration, and reuse, detects gaps, and computes the 0–100 score and grade.\n• Administrator Path: The administrator manages user accounts, modifies security standard thresholds, activates policies for live system enforcement, and reviews enterprise audit trails.\n• Viewer / Auditor Path: Viewers have read-only access to browse dashboards, inspect historical reports, and view compliance matrices without editing rights.")
    add_bullet(c18, "Step 4: Immutable Persistence & Audit Logging", "Every evaluation result, policy configuration update, user role alteration, and authentication event is permanently committed to PostgreSQL with actor identity, client IP, timestamp, and score snapshot.")
    add_bullet(c18, "Step 5: Comparative Analysis & Report Export", "Users compare multiple policy revisions side-by-side to identify security enhancements or regressions, and export formal compliance audit reports in industry-standard PDF and CSV formats.")

    # ROW 19: Date Submitted
    clear_cell(t.rows[19].cells[0])
    add_paragraph(t.rows[19].cells[0], bold_prefix="Date Submitted:")
    clear_cell(t.rows[19].cells[1])
    add_paragraph(t.rows[19].cells[1], bold_prefix="November 15, 2026")

    # ROW 20: Teacher's Feedback
    clear_cell(t.rows[20].cells[0])
    add_paragraph(t.rows[20].cells[0], bold_prefix="Teacher’s Feedback")
    c20 = t.rows[20].cells[1]
    clear_cell(c20)
    add_paragraph(c20, text="_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n_________________________________________________________________\n\n________________________________            __________________________\nStudent’s Signature (after feedbacking)                       Teacher’s Signature")

    # Save to all target locations
    save_targets = [
        (OUTPUT_PATH2, "Downloads CORETICO Deliverables"),
        (OUTPUT_PATH3, "Project Workspace Deliverables"),
        (r"c:\Users\Admin\Downloads\IT23_2ndDeliverables_Functions_Completed.docx", "Downloads Completed Deliverables"),
        (OUTPUT_PATH1, "Original Template Path")
    ]
    for path, label in save_targets:
        try:
            doc.save(path)
            print(f"Successfully saved [{label}]: {path}")
        except PermissionError:
            print(f"Could not save [{label}] to {path} because the file is currently open in Microsoft Word. Saved to alternatives.")
        except Exception as e:
            print(f"Error saving to {path}: {e}")

if __name__ == "__main__":
    populate_deliverables_document()
    print("Document generation fully complete!")
