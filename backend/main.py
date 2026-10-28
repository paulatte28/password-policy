import os
import json
import csv
import io
import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from backend.database import engine, Base, get_db
from backend.models import User, PolicySetting, StandardDefinition, EvaluationReport, AuditLog
from backend.schemas import (
    LoginRequest, TokenResponse, UserResponse, UserCreate, UserUpdate,
    PolicyInput, PolicyEvaluateRequest, EvaluationResult, StandardUpdate, AuditLogResponse
)
from backend.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, get_optional_user, require_admin, require_analyst_or_admin
)
from backend.compliance_engine import evaluate_policy
from backend.seed_data import seed_database

load_dotenv()

# Create tables
Base.metadata.create_all(bind=engine)

# Seed database on initial startup
with Session(bind=engine) as db:
    seed_database(db)

app = FastAPI(
    title="PasswordPolicy Checker API",
    description="Backend API for Evaluating Password Policy Compliance and Security Risks (IT23/L #23)",
    version="2.0.0"
)

# Enable CORS for React frontend (Vite default port 5173, 5174, 3000, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def record_audit(db: Session, action: str, details: str, user_name: str, user_role: str, ip: str = "127.0.0.1", score: Optional[float] = None):
    audit = AuditLog(
        action=action,
        details=details,
        user_name=user_name,
        user_role=user_role,
        ip_address=ip,
        score_snapshot=score,
        timestamp=datetime.datetime.utcnow()
    )
    db.add(audit)
    db.commit()

# -------------------------------------------------------------
# AUTHENTICATION ENDPOINTS
# -------------------------------------------------------------
@app.post("/api/auth/login", response_model=TokenResponse)
def login(creds: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not verify_password(creds.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated. Contact an administrator."
        )

    token = create_access_token({"sub": user.email, "role": user.role, "name": user.full_name})
    
    # Audit log
    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "USER_LOGIN", f"User {user.full_name} ({user.email}) logged in successfully.", user.full_name, user.role, client_ip)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "department": user.department
        }
    }

@app.get("/api/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "department": current_user.department
    }

# -------------------------------------------------------------
# USER MANAGEMENT (ADMINISTRATOR ONLY)
# -------------------------------------------------------------
@app.get("/api/users", response_model=List[UserResponse])
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id.asc()).all()

@app.post("/api/users", response_model=UserResponse)
def create_user(u: UserCreate, request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == u.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    
    new_user = User(
        email=u.email,
        full_name=u.full_name,
        role=u.role,
        department=u.department,
        hashed_password=hash_password(u.password),
        is_active=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "CREATE_USER", f"Admin created user {new_user.email} with role {new_user.role}", current_user.full_name, current_user.role, client_ip)
    return new_user

@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, u: UserUpdate, request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if u.full_name is not None: user.full_name = u.full_name
    if u.role is not None: user.role = u.role
    if u.department is not None: user.department = u.department
    if u.is_active is not None: user.is_active = u.is_active
    if u.password: user.hashed_password = hash_password(u.password)

    db.commit()
    db.refresh(user)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "UPDATE_USER", f"Admin updated user {user.email}", current_user.full_name, current_user.role, client_ip)
    return user

# -------------------------------------------------------------
# STANDARDS ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/standards")
def get_standards(db: Session = Depends(get_db)):
    return db.query(StandardDefinition).all()

@app.get("/api/standards/{standard_id}")
def get_standard_by_id(standard_id: str, db: Session = Depends(get_db)):
    std = db.query(StandardDefinition).filter(StandardDefinition.id == standard_id).first()
    if not std:
        raise HTTPException(status_code=404, detail="Standard not found")
    return std

@app.put("/api/standards/{standard_id}")
def update_standard(standard_id: str, payload: StandardUpdate, request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    std = db.query(StandardDefinition).filter(StandardDefinition.id == standard_id).first()
    if not std:
        raise HTTPException(status_code=404, detail="Standard not found")
    
    std.recommended_min_length = payload.recommended_min_length
    std.requires_complexity = payload.requires_complexity
    std.max_failed_attempts_threshold = payload.max_failed_attempts_threshold
    std.min_lockout_duration_minutes = payload.min_lockout_duration_minutes
    std.recommended_max_password_age_days = payload.recommended_max_password_age_days
    std.recommended_password_history_count = payload.recommended_password_history_count
    std.requires_breached_dictionary_check = payload.requires_breached_dictionary_check
    std.mfa_recommendation = payload.mfa_recommendation
    std.updated_at = datetime.datetime.utcnow()

    db.commit()
    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "UPDATE_STANDARD", f"Updated standard limits for {std.name}", current_user.full_name, current_user.role, client_ip)
    return std

# -------------------------------------------------------------
# POLICY EVALUATION & SAMPLES
# -------------------------------------------------------------
@app.get("/api/policies/samples")
def get_policy_samples(db: Session = Depends(get_db)):
    presets = db.query(PolicySetting).filter(PolicySetting.is_sample_preset == True).all()
    return presets

@app.post("/api/policies/evaluate")
def evaluate_policy_endpoint(
    req: PolicyEvaluateRequest,
    request: Request,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    std = db.query(StandardDefinition).filter(StandardDefinition.id == req.standard_id).first()
    if not std:
        std = db.query(StandardDefinition).filter(StandardDefinition.id == "NIST_SP_800_63B").first()

    eval_result = evaluate_policy(req, std)
    evaluator_name = current_user.full_name if current_user else "Security Analyst"
    evaluator_role = current_user.role if current_user else "Security Analyst"

    report_id = None
    if req.save_report:
        report = EvaluationReport(
            policy_name=req.name,
            standard_id=std.id,
            standard_name=std.name,
            overall_compliance_score=eval_result["overall_compliance_score"],
            grade_letter=eval_result["grade_letter"],
            risk_level=eval_result["risk_level"],
            executive_summary=eval_result["executive_summary"],
            findings_json=json.dumps([f.dict() for f in eval_result["findings"]]),
            scores_breakdown_json=json.dumps(eval_result["scores_breakdown"].dict()),
            policy_snapshot_json=json.dumps(req.dict()),
            passed_count=eval_result["passed_count"],
            warning_count=eval_result["warning_count"],
            failed_count=eval_result["failed_count"],
            evaluated_by_user=evaluator_name,
            evaluated_at=datetime.datetime.utcnow()
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        report_id = report.id

        client_ip = request.client.host if request.client else "127.0.0.1"
        record_audit(
            db, "POLICY_EVALUATION",
            f"Evaluated policy '{req.name}' against {std.name}. Score: {eval_result['overall_compliance_score']}% ({eval_result['grade_letter']})",
            evaluator_name, evaluator_role, client_ip, eval_result["overall_compliance_score"]
        )

    return {
        "id": report_id,
        "policy_name": req.name,
        "standard_id": std.id,
        "standard_name": std.name,
        "overall_compliance_score": eval_result["overall_compliance_score"],
        "grade_letter": eval_result["grade_letter"],
        "risk_level": eval_result["risk_level"],
        "executive_summary": eval_result["executive_summary"],
        "scores_breakdown": eval_result["scores_breakdown"],
        "findings": eval_result["findings"],
        "passed_count": eval_result["passed_count"],
        "warning_count": eval_result["warning_count"],
        "failed_count": eval_result["failed_count"],
        "evaluated_at": datetime.datetime.utcnow(),
        "evaluated_by": evaluator_name
    }

@app.post("/api/policies/import")
async def import_policy_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = await file.read()
    
    if filename.endswith(".json"):
        try:
            data = json.loads(content.decode("utf-8"))
            return data
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON file format: {str(e)}")
    
    elif filename.endswith(".csv"):
        try:
            text = content.decode("utf-8-sig")
            reader = csv.DictReader(io.StringIO(text))
            rows = list(reader)
            if not rows:
                raise HTTPException(status_code=400, detail="CSV file is empty")
            row = rows[0]
            # Map common headers to policy keys
            def get_val(keys, default):
                for k in keys:
                    for rk in row.keys():
                        if rk.strip().lower() == k.strip().lower():
                            val = row[rk].strip()
                            if isinstance(default, bool):
                                return val.lower() in ["1", "true", "yes", "y", "enable", "enabled"]
                            elif isinstance(default, int):
                                try: return int(val)
                                except: return default
                            return val
                return default

            parsed_policy = {
                "name": get_val(["name", "policy_name", "policy"], "Imported Policy"),
                "description": get_val(["description", "desc"], "Imported from CSV"),
                "min_length": get_val(["min_length", "minimum_length", "length", "minlen"], 8),
                "max_length": get_val(["max_length", "maximum_length", "maxlen"], 64),
                "require_uppercase": get_val(["require_uppercase", "uppercase", "upper"], True),
                "require_lowercase": get_val(["require_lowercase", "lowercase", "lower"], True),
                "require_digit": get_val(["require_digit", "numbers", "digit", "digits"], True),
                "require_special": get_val(["require_special", "special", "symbols", "symbol"], True),
                "min_categories": get_val(["min_categories", "categories"], 3),
                "max_failed_attempts": get_val(["max_failed_attempts", "lockout_threshold", "lockout"], 5),
                "lockout_duration_min": get_val(["lockout_duration_min", "lockout_duration", "duration"], 15),
                "lockout_reset_min": get_val(["lockout_reset_min", "reset_duration"], 15),
                "max_password_age_days": get_val(["max_password_age_days", "max_age", "expiration", "expire_days"], 90),
                "min_password_age_days": get_val(["min_password_age_days", "min_age"], 1),
                "password_history_count": get_val(["password_history_count", "history", "history_count"], 5),
                "disallow_common": get_val(["disallow_common", "dictionary_check"], True),
                "disallow_username": get_val(["disallow_username", "no_username"], True),
                "require_mfa": get_val(["require_mfa", "mfa"], False),
            }
            return parsed_policy
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Only .json and .csv files are supported")

# -------------------------------------------------------------
# EVALUATION REPORTS & EXPORT
# -------------------------------------------------------------
@app.get("/api/reports")
def list_reports(db: Session = Depends(get_db)):
    reports = db.query(EvaluationReport).order_by(EvaluationReport.evaluated_at.desc()).all()
    results = []
    for r in reports:
        results.append({
            "id": r.id,
            "policy_name": r.policy_name,
            "standard_id": r.standard_id,
            "standard_name": r.standard_name,
            "overall_compliance_score": r.overall_compliance_score,
            "grade_letter": r.grade_letter,
            "risk_level": r.risk_level,
            "passed_count": r.passed_count,
            "warning_count": r.warning_count,
            "failed_count": r.failed_count,
            "evaluated_by_user": r.evaluated_by_user,
            "evaluated_at": r.evaluated_at
        })
    return results

@app.get("/api/reports/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    r = db.query(EvaluationReport).filter(EvaluationReport.id == report_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return {
        "id": r.id,
        "policy_name": r.policy_name,
        "standard_id": r.standard_id,
        "standard_name": r.standard_name,
        "overall_compliance_score": r.overall_compliance_score,
        "grade_letter": r.grade_letter,
        "risk_level": r.risk_level,
        "executive_summary": r.executive_summary,
        "findings": json.loads(r.findings_json),
        "scores_breakdown": json.loads(r.scores_breakdown_json),
        "policy_snapshot": json.loads(r.policy_snapshot_json),
        "passed_count": r.passed_count,
        "warning_count": r.warning_count,
        "failed_count": r.failed_count,
        "evaluated_by_user": r.evaluated_by_user,
        "evaluated_at": r.evaluated_at
    }

@app.get("/api/reports/{report_id}/export-csv")
def export_report_csv(report_id: int, db: Session = Depends(get_db)):
    r = db.query(EvaluationReport).filter(EvaluationReport.id == report_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")
    
    findings = json.loads(r.findings_json)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["PasswordPolicy Checker Compliance Report"])
    writer.writerow(["Report ID", r.id])
    writer.writerow(["Policy Name", r.policy_name])
    writer.writerow(["Standard", r.standard_name])
    writer.writerow(["Compliance Score", f"{r.overall_compliance_score}% (Grade {r.grade_letter})"])
    writer.writerow(["Risk Level", r.risk_level])
    writer.writerow(["Evaluator", r.evaluated_by_user])
    writer.writerow(["Timestamp", r.evaluated_at.isoformat()])
    writer.writerow([])
    writer.writerow(["Category", "Finding Title", "Status", "Severity", "Current Setting", "Standard Requirement", "Risk Description", "Recommendation"])
    for f in findings:
        writer.writerow([
            f.get("rule_category", ""),
            f.get("title", ""),
            f.get("status", ""),
            f.get("severity", ""),
            f.get("current_value", ""),
            f.get("standard_requirement", ""),
            f.get("risk_description", ""),
            f.get("recommendation", "")
        ])
    
    content = output.getvalue()
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=compliance_report_{r.id}.csv"}
    )

# -------------------------------------------------------------
# DASHBOARD STATS & AUDIT LOGS
# -------------------------------------------------------------
@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_evals = db.query(EvaluationReport).count()
    reports = db.query(EvaluationReport).all()
    avg_score = round(sum(r.overall_compliance_score for r in reports) / total_evals, 1) if total_evals > 0 else 0.0
    
    risk_counts = {"Low": 0, "Moderate": 0, "High": 0, "Critical": 0}
    grade_counts = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for r in reports:
        if r.risk_level in risk_counts:
            risk_counts[r.risk_level] += 1
        if r.grade_letter in grade_counts:
            grade_counts[r.grade_letter] += 1

    standards_count = db.query(StandardDefinition).count()
    recent_reports = db.query(EvaluationReport).order_by(EvaluationReport.evaluated_at.desc()).limit(5).all()

    return {
        "total_evaluations": total_evals,
        "average_compliance_score": avg_score,
        "risk_breakdown": risk_counts,
        "grade_breakdown": grade_counts,
        "standards_count": standards_count,
        "recent_evaluations": [
            {
                "id": r.id,
                "policy_name": r.policy_name,
                "standard_name": r.standard_name,
                "overall_compliance_score": r.overall_compliance_score,
                "grade_letter": r.grade_letter,
                "risk_level": r.risk_level,
                "evaluated_at": r.evaluated_at
            }
            for r in recent_reports
        ]
    }

@app.get("/api/audit", response_model=List[AuditLogResponse])
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "PasswordPolicy Checker",
        "project": "#23 IT23/L",
        "author": "Kristine Paula S. Coretico",
        "engine": "FastAPI + SQLAlchemy + React"
    }

# Mount React static build if present (for single-service deployment on Render)
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    images_dir = os.path.join(frontend_dist, "images")
    if os.path.exists(images_dir):
        app.mount("/images", StaticFiles(directory=images_dir), name="images")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        # Do not intercept api routes or docs
        if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="Not Found")
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dist, "index.html"))

