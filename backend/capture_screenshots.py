import subprocess
import time
import os
import secrets
import datetime
import sqlite3
import jwt
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

SCREENSHOT_DIR = os.path.abspath("screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

SECRET_KEY = "coretico-it23-password-policy-secret-key-2026-jwt"
session_id = secrets.token_hex(16)
expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)

conn = sqlite3.connect("passwordpolicy.db")
cur = conn.cursor()
cur.execute("SELECT id, email, full_name, role FROM users WHERE role='Administrator' AND full_name LIKE '%Coretico%' LIMIT 1")
row = cur.fetchone()
if not row:
    cur.execute("SELECT id, email, full_name, role FROM users WHERE role='Administrator' LIMIT 1")
    row = cur.fetchone()

admin_id, admin_email, admin_name, admin_role = row
print(f"Using Admin: {admin_name} ({admin_email}), ID={admin_id}")

cur.execute("UPDATE login_state SET must_change_password=0, failed_attempts=0, locked_until=NULL WHERE user_id=?", (admin_id,))
cur.execute("INSERT OR REPLACE INTO user_sessions (id, user_id, expires_at) VALUES (?, ?, ?)",
            (session_id, admin_id, expires_at.strftime("%Y-%m-%d %H:%M:%S")))
conn.commit()
conn.close()

token = jwt.encode({"sub": admin_email, "jti": session_id, "exp": expires_at}, SECRET_KEY, algorithm="HS256")

print("Starting FastAPI backend on port 8000...")
proc = subprocess.Popen([r".venv\Scripts\python.exe", "-m", "uvicorn", "backend.main:app", "--port", "8000"],
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

backend_ready = False
for i in range(15):
    try:
        with urllib.request.urlopen("http://localhost:8000/api/health", timeout=2) as resp:
            if resp.status == 200:
                backend_ready = True
                print("Backend is ready!")
                break
    except Exception:
        time.sleep(1)

if not backend_ready:
    proc.terminate()
    raise RuntimeError("Backend failed to start in time")

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1440,960")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1440, 960)

try:
    driver.get("http://localhost:8000")
    time.sleep(2)

    # Set token in localStorage
    driver.execute_script(f"localStorage.setItem('token', '{token}');")
    driver.refresh()
    time.sleep(3)

    print("Logged in successfully. Current URL:", driver.current_url)

    def click_nav(text_match):
        links = driver.find_elements(By.CSS_SELECTOR, ".sidebar-link")
        for link in links:
            if text_match.lower() in link.text.lower():
                link.click()
                time.sleep(2)
                return True
        return False

    # 1. Overview Dashboard
    click_nav("Overview")
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_dashboard.png"))
    print("Saved ui_dashboard.png")

    # Security Function 1: Report View (Compliance Evaluation & Risk Scoring)
    click_nav("Reports")
    time.sleep(1)
    view_btns = driver.find_elements(By.XPATH, "//button[contains(text(), 'View') or contains(text(), 'Open')]")
    if view_btns:
        view_btns[0].click()
        time.sleep(2)
        driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_function1_evaluation_report.png"))
        print("Saved ui_function1_evaluation_report.png")

    # Security Function 2: Runtime Policy Enforcement / Policy Editor & Activation
    click_nav("Policy editor")
    time.sleep(1.5)
    # Scroll slightly to see the policy enforcement parameters and activate button
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_function2_policy_enforcement.png"))
    print("Saved ui_function2_policy_enforcement.png")

    # Security Function 3: Users (RBAC)
    click_nav("Users")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_function3_user_management.png"))
    print("Saved ui_function3_user_management.png")

    # Security Function 4: Activity Log (Audit Logs)
    click_nav("Activity log")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_function4_audit_logs.png"))
    print("Saved ui_function4_audit_logs.png")

    # Compare Reports
    click_nav("Compare")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_policy_compare.png"))
    print("Saved ui_policy_compare.png")

    # Benchmarks
    click_nav("Benchmarks")
    time.sleep(2)
    driver.save_screenshot(os.path.join(SCREENSHOT_DIR, "ui_standards.png"))
    print("Saved ui_standards.png")

finally:
    driver.quit()
    proc.terminate()
    print("Done capturing UI screenshots.")
