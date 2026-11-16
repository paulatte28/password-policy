import os
import re
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.abspath("generated_report_assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

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

def highlight_python_line(line_str):
    """Simple syntax classification for VS Code dark theme styling."""
    stripped = line_str.strip()
    if stripped.startswith("#"):
        return "comment"
    if stripped.startswith("@"):
        return "decorator"
    if any(stripped.startswith(k + " ") or stripped == k for k in ["def", "class", "return", "if", "elif", "else", "try", "except", "import", "from", "for", "in", "with", "raise"]):
        return "keyword"
    if "status.HTTP" in line_str or "CRITICAL" in line_str or "FAIL" in line_str:
        return "alert"
    if any(t in line_str for t in ["Column", "Integer", "String", "Boolean", "Float", "DateTime", "Session", "Base", "User", "AuditLog", "StandardDefinition"]):
        return "type"
    return "plain"

def render_authentic_code_card(title, filepath, line_ranges, out_filename):
    """
    Reads actual lines directly from the authentic file on disk and renders a VS Code window card.
    line_ranges: list of tuples (start_line, end_line) 1-indexed inclusive.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        all_lines = f.readlines()

    selected_lines = []
    for r_idx, (start, end) in enumerate(line_ranges):
        if r_idx > 0:
            selected_lines.append((0, "    # ... [Implementation continues] ...", "comment"))
        for l_num in range(start, min(end + 1, len(all_lines) + 1)):
            raw_line = all_lines[l_num - 1].rstrip("\r\n")
            hl_type = highlight_python_line(raw_line)
            selected_lines.append((l_num, raw_line, hl_type))

    pad_x = 28
    pad_y = 18
    header_h = 42
    line_h = 24
    width = 1120
    height = header_h + pad_y * 2 + len(selected_lines) * line_h

    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Window header bar
    draw.rectangle([(0, 0), (width, header_h)], fill="#252526")
    draw.line([(0, header_h), (width, header_h)], fill="#333333", width=1)

    # Window control dots
    draw.ellipse([(16, 14), (28, 26)], fill="#ff5f56") # red
    draw.ellipse([(36, 14), (48, 26)], fill="#ffbd2e") # yellow
    draw.ellipse([(56, 14), (68, 26)], fill="#27c93f") # green

    # Header label
    font_title = get_font(13, bold=True)
    rel_path = os.path.relpath(filepath, os.getcwd()).replace("\\", "/")
    draw.text((85, 12), f"{rel_path}  —  {title}", fill="#cccccc", font=font_title)

    font_code = get_font(13.5, mono=True)
    font_line_num = get_font(12.5, mono=True)

    y = header_h + pad_y
    for line_num, line_str, hl_type in selected_lines:
        # Line number
        if line_num > 0:
            draw.text((pad_x, y), f"{line_num:>3} ", fill="#606775", font=font_line_num)
        else:
            draw.text((pad_x, y), "    ", fill="#606775", font=font_line_num)

        # Syntax colors matching VS Code Dark+
        if hl_type == "comment":
            color = "#6a9955"
        elif hl_type == "decorator":
            color = "#dcdcaa"
        elif hl_type == "keyword":
            color = "#c586c0"
        elif hl_type == "type":
            color = "#4ec9b0"
        elif hl_type == "alert":
            color = "#f44747"
        else:
            color = "#d4d4d4"

        draw.text((pad_x + 55, y), line_str, fill=color, font=font_code)
        y += line_h

    out_path = os.path.join(ASSETS_DIR, out_filename)
    img.save(out_path, quality=95)
    print(f"Generated authentic code screenshot: {out_filename} ({width}x{height})")
    return out_path

# ==============================================================================
# 1. FUNCTION 1: backend/compliance_engine.py
# Lines 6-26 (evaluate_policy & length check) and lines 361-386 (overall score calculation)
# ==============================================================================
render_authentic_code_card(
    "Policy Evaluation Engine & Weighted Risk Scoring",
    os.path.abspath("backend/compliance_engine.py"),
    [(6, 26), (361, 386)],
    "code_function1_compliance.png"
)

# ==============================================================================
# 2. FUNCTION 2: backend/main.py
# Lines 167-200 (Standards Management Endpoints: GET & PUT /api/standards)
# ==============================================================================
render_authentic_code_card(
    "Cybersecurity Benchmark Standards Configuration Service",
    os.path.abspath("backend/main.py"),
    [(167, 200)],
    "code_function2_standards.png"
)

# ==============================================================================
# 3. FUNCTION 3: backend/auth.py
# Lines 21-39 (Password hashing & JWT) and lines 81-92 (RBAC role checker & dependencies)
# ==============================================================================
render_authentic_code_card(
    "Role-Based Access Control (RBAC) & JWT Token Security",
    os.path.abspath("backend/auth.py"),
    [(21, 39), (81, 92)],
    "code_function3_rbac_jwt.png"
)

# ==============================================================================
# 4. FUNCTION 4: backend/main.py
# Lines 71-82 (record_audit helper) and lines 423-424, 439-441 (GET /api/audit)
# ==============================================================================
render_authentic_code_card(
    "Immutable Security Audit Logging Service",
    os.path.abspath("backend/main.py"),
    [(71, 82), (439, 442)],
    "code_function4_audit_logs.png"
)

print("All authentic code screenshots generated directly from real files!")
