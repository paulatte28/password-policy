import os
import json
import csv
import io
import datetime
import secrets
from typing import List, Optional
from fastapi import FastAPI, Depends, Header, HTTPException, Query, status, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.database import engine, Base, get_db
from backend.models import User, PolicySetting, StandardDefinition, EvaluationReport, AuditLog, ActivePolicy, LoginState, PasswordHistory, UserSession
from backend.schemas import (
    LoginRequest, TokenResponse, UserResponse, UserCreate, UserUpdate, PasswordChange,
    PolicyInput, PolicyEvaluateRequest, EvaluationResult, StandardUpdate
)
from backend.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_admin, require_analyst_or_admin
)
from backend.compliance_engine import evaluate_policy
from backend.seed_data import seed_database
from backend.policy_enforcement import get_active_policy, get_login_state, validate_password, remember_password

# Create tables
Base.metadata.create_all(bind=engine)

# Seed database on initial startup
with Session(bind=engine) as db:
    seed_database(db)

app = FastAPI(
    title="PasswordPolicy Checker API",
    description="Backend API for Evaluating Password Policy Compliance and Security Risks (IT23/L #23)",
    version="2.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

@app.get("/docs", include_in_schema=False)
def docs_redirect():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/api/docs")

# Enable CORS for React frontend (Vite default port 5173, 5174, 3000, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ALLOWED_ROLES = ("Administrator", "Security Analyst", "Auditor")

def normalize_role(role: Optional[str]) -> Optional[str]:
    if role == "Viewer":
        return "Auditor"
    return role

def record_audit(db: Session, action: str, details: str, user_name: str, user_role: str, ip: str = "127.0.0.1", score: Optional[float] = None, commit: bool = True):
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
    if commit:
        db.commit()

# -------------------------------------------------------------
# AUTHENTICATION ENDPOINTS
# -------------------------------------------------------------
@app.post("/api/auth/login", response_model=TokenResponse)
def login(creds: LoginRequest, request: Request, db: Session = Depends(get_db)):
    now = datetime.datetime.utcnow()
    client_ip = request.client.host if request.client else "127.0.0.1"
    normalized_email = creds.email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()
    if not user or not user.is_active:
        record_audit(db, "LOGIN_FAILED", f"Failed sign-in attempt for email '{normalized_email}' (unknown or inactive account).", normalized_email or "Unknown", "Unauthenticated", client_ip)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    state = get_login_state(db, user.id)
    if state.locked_until and state.locked_until > now:
        record_audit(db, "LOGIN_FAILED", f"Blocked sign-in attempt for locked account {user.email}.", user.full_name, user.role, client_ip)
        raise HTTPException(status_code=429, detail="Account temporarily locked. Try again later.")
    policy = get_active_policy(db)
    if not verify_password(creds.password, user.hashed_password):
        window = (policy.lockout_reset_min if policy else 15)
        if state.last_failed_at and now > state.last_failed_at + datetime.timedelta(minutes=window):
            state.failed_attempts = 0
        state.failed_attempts += 1
        state.last_failed_at = now
        limit = policy.max_failed_attempts if policy else 5
        if limit and state.failed_attempts >= limit:
            state.locked_until = now + datetime.timedelta(minutes=policy.lockout_duration_min if policy else 15)
            state.failed_attempts = 0
        if state.locked_until and state.locked_until > now:
            record_audit(db, "ACCOUNT_LOCKED", f"Account {user.email} temporarily locked after failed sign-in attempts.", user.full_name, user.role, client_ip, commit=False)
        else:
            record_audit(db, "LOGIN_FAILED", f"Invalid password attempt for {user.email}.", user.full_name, user.role, client_ip, commit=False)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    state.failed_attempts = 0
    state.locked_until = None
    state.last_failed_at = None
    session_id = secrets.token_hex(32)
    token = create_access_token({"sub": user.email, "jti": session_id})
    db.add(UserSession(id=session_id, user_id=user.id, expires_at=now + datetime.timedelta(hours=24)))
    record_audit(db, "USER_LOGIN", f"User {user.full_name} ({user.email}) logged in successfully.", user.full_name, user.role, client_ip, commit=False)
    db.commit()

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "department": user.department,
            "must_change_password": bool(state.must_change_password or (policy and policy.max_password_age_days and state.password_changed_at and now > state.password_changed_at + datetime.timedelta(days=policy.max_password_age_days)))
        }
    }

@app.get("/api/auth/me")
def get_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    state = get_login_state(db, current_user.id)
    policy = get_active_policy(db)
    now = datetime.datetime.utcnow()
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "department": current_user.department,
        "must_change_password": bool(state.must_change_password or (policy and policy.max_password_age_days and state.password_changed_at and now > state.password_changed_at + datetime.timedelta(days=policy.max_password_age_days)))
    }


@app.post("/api/auth/logout")
def logout(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    import jwt
    from backend.auth import SECRET_KEY, ALGORITHM
    token = request.headers.get("authorization", "").removeprefix("Bearer ")
    session_id = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["jti"]
    db.delete(db.get(UserSession, session_id))
    db.commit()
    return {"message": "Signed out"}


@app.post("/api/auth/change-password")
def change_password(payload: PasswordChange, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    policy = get_active_policy(db)
    validate_password(payload.new_password, current_user.email, policy, db, current_user.id)
    if verify_password(payload.new_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Choose a different password")
    db.add(PasswordHistory(user_id=current_user.id, password_hash=current_user.hashed_password))
    current_user.hashed_password = hash_password(payload.new_password)
    remember_password(db, current_user.id)
    db.query(UserSession).filter(UserSession.user_id == current_user.id).delete(synchronize_session=False)
    db.commit()
    record_audit(db, "PASSWORD_CHANGED", f"User {current_user.email} changed their password", current_user.full_name, current_user.role, request.client.host if request.client else "127.0.0.1")
    return {"message": "Password changed. Sign in again."}

# -------------------------------------------------------------
# USER MANAGEMENT (ADMINISTRATOR ONLY)
# -------------------------------------------------------------
@app.get("/api/users", response_model=List[UserResponse])
def list_users(current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.id.asc()).all()


@app.post("/api/users/seed-demo")
def seed_demo_users(request: Request, response: Response, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Provision the three example roles without reusable public passwords."""
    from string import ascii_letters, digits
    from backend.policy_enforcement import get_active_policy, get_login_state, validate_password

    policy = get_active_policy(db)
    length = min(72, max(20, policy.min_length if policy else 15), policy.max_length if policy else 72)
    if length < 4 or (policy and policy.min_length > length):
        raise HTTPException(status_code=400, detail="Active policy cannot generate a usable temporary password")

    examples = (
        ("admin@passwordpolicy.local", "Kristine Paula S. Coretico", "Administrator", "Systems Administration & Security Unit", "Admin@123456"),
        ("analyst@passwordpolicy.local", "Alex Vance", "Security Analyst", "IT Security & Assurance", "Analyst@123456"),
        ("viewer@passwordpolicy.local", "Jordan Lee", "Auditor", "IT Audit & Compliance", "Viewer@123456"),
    )
    created, skipped = [], []
    alphabet = ascii_letters + digits + "!@#$%*?"
    for email, name, role, department, old_demo_password in examples:
        user = db.query(User).filter(User.email == email).first()
        if user and (user.is_active or not verify_password(old_demo_password, user.hashed_password)):
            skipped.append(email)
            continue
        for _ in range(10):
            characters = [secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZ"), secrets.choice("abcdefghjkmnpqrstuvwxyz"), secrets.choice(digits), secrets.choice("!@#$%*?")]
            characters += [secrets.choice(alphabet) for _ in range(length - 4)]
            secrets.SystemRandom().shuffle(characters)
            password = "".join(characters)
            try:
                validate_password(password, email, policy, db)
                break
            except HTTPException:
                continue
        else:
            raise HTTPException(status_code=400, detail="Could not generate a password that satisfies the active policy")
        password_hash = hash_password(password)
        if user is None:
            user = User(email=email, full_name=name, role=role, department=department, hashed_password=password_hash, is_active=True)
            db.add(user)
            db.flush()
        else:
            user.hashed_password = password_hash
        user.is_active = True
        state = get_login_state(db, user.id)
        state.must_change_password = True
        state.failed_attempts = 0
        state.locked_until = None
        db.query(UserSession).filter(UserSession.user_id == user.id).delete(synchronize_session=False)
        created.append({"email": email, "role": role, "temporary_password": password})
    db.commit()
    if created:
        record_audit(db, "SEED_DEMO_USERS", f"Provisioned {len(created)} demo accounts", current_user.full_name, current_user.role, request.client.host if request.client else "127.0.0.1")
    response.headers["Cache-Control"] = "no-store"
    return {"created": created, "skipped": skipped}

@app.post("/api/users", response_model=UserResponse)
def create_user(u: UserCreate, request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    email = u.email.strip().lower()
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    validate_password(u.password, email, get_active_policy(db), db)
    role_val = normalize_role(u.role)
    if role_val not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    new_user = User(
        email=email,
        full_name=u.full_name,
        role=role_val,
        department=u.department,
        hashed_password=hash_password(u.password),
        is_active=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(new_user)
    db.flush()
    remember_password(db, new_user.id)
    get_login_state(db, new_user.id).must_change_password = True

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "CREATE_USER", f"Admin created user {new_user.email} with role {new_user.role}", current_user.full_name, current_user.role, client_ip, commit=False)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, u: UserUpdate, request: Request, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    normalized_role = normalize_role(u.role) if u.role is not None else None
    if normalized_role is not None and normalized_role not in ALLOWED_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")
    if user.role == "Administrator" and (normalized_role not in (None, "Administrator") or u.is_active is False):
        admins = db.query(User).filter(User.role == "Administrator", User.is_active == True).count()
        if admins <= 1:
            raise HTTPException(status_code=400, detail="At least one active administrator is required")
    if u.full_name is not None: user.full_name = u.full_name
    if normalized_role is not None: user.role = normalized_role
    if u.department is not None: user.department = u.department
    if u.is_active is not None: user.is_active = u.is_active
    if u.password:
        validate_password(u.password, user.email, get_active_policy(db), db, user.id, enforce_age=False)
        if verify_password(u.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Choose a different password")
        db.add(PasswordHistory(user_id=user.id, password_hash=user.hashed_password))
        user.hashed_password = hash_password(u.password)
        remember_password(db, user.id)
        get_login_state(db, user.id).must_change_password = True
        db.query(UserSession).filter(UserSession.user_id == user.id).delete(synchronize_session=False)

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "UPDATE_USER", f"Admin updated user {user.email}", current_user.full_name, current_user.role, client_ip, commit=False)
    db.commit()
    db.refresh(user)
    return user

# -------------------------------------------------------------
# STANDARDS ENDPOINTS
# -------------------------------------------------------------
@app.get("/api/standards", dependencies=[Depends(get_current_user)])
def get_standards(db: Session = Depends(get_db)):
    return db.query(StandardDefinition).all()

@app.get("/api/standards/{standard_id}", dependencies=[Depends(get_current_user)])
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

    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(db, "UPDATE_STANDARD", f"Updated standard limits for {std.name}", current_user.full_name, current_user.role, client_ip, commit=False)
    db.commit()
    return std

# -------------------------------------------------------------
# POLICY EVALUATION & SAMPLES
# -------------------------------------------------------------
@app.get("/api/policies/active")
def active_policy(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    policy = get_active_policy(db)
    return policy.model_dump() if policy else None


@app.put("/api/policies/active")
def activate_policy(payload: PolicyInput, request: Request, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    if payload.min_length > payload.max_length:
        raise HTTPException(status_code=400, detail="Minimum length cannot exceed maximum length")
    if payload.require_mfa:
        raise HTTPException(status_code=400, detail="MFA cannot be activated because this app has no second-factor verification yet")
    if payload.max_failed_attempts and payload.lockout_duration_min == 0:
        raise HTTPException(status_code=400, detail="Lockout duration must be greater than zero")
    active = db.get(ActivePolicy, 1)
    if active is None:
        active = ActivePolicy(id=1)
        db.add(active)
    active.rules_json = payload.model_dump_json()
    active.activated_at = datetime.datetime.utcnow()
    for user in db.query(User).filter(User.is_active == True).all():
        get_login_state(db, user.id).must_change_password = True
    record_audit(db, "ACTIVATE_POLICY", f"Activated policy '{payload.name}' for application accounts", current_user.full_name, current_user.role, request.client.host if request.client else "127.0.0.1", commit=False)
    db.commit()
    return {"message": "Policy activated. Users must change passwords at next sign-in.", "policy": payload.model_dump()}


@app.get("/api/policies/samples", dependencies=[Depends(get_current_user)])
def get_policy_samples(db: Session = Depends(get_db)):
    presets = db.query(PolicySetting).filter(PolicySetting.is_sample_preset == True).all()
    return presets

@app.post("/api/policies/evaluate")
def evaluate_policy_endpoint(
    req: PolicyEvaluateRequest,
    request: Request,
    current_user: User = Depends(require_analyst_or_admin),
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
        db.flush()
        report_id = report.id

        client_ip = request.client.host if request.client else "127.0.0.1"
        record_audit(
            db, "POLICY_EVALUATION",
            f"Evaluated policy '{req.name}' against {std.name}. Score: {eval_result['overall_compliance_score']}% ({eval_result['grade_letter']})",
            evaluator_name, evaluator_role, client_ip, eval_result["overall_compliance_score"],
            commit=False
        )
        db.commit()

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
async def import_policy_file(
    request: Request,
    file: UploadFile = File(...),
    current_user: User = Depends(require_analyst_or_admin),
    db: Session = Depends(get_db),
):
    filename = file.filename.lower()
    content = await file.read()
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    if filename.endswith(".json"):
        try:
            data = json.loads(content.decode("utf-8"))
            record_audit(
                db, "POLICY_IMPORTED",
                f"Imported external JSON policy file '{file.filename}'.",
                current_user.full_name, current_user.role, client_ip
            )
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
            record_audit(
                db, "POLICY_IMPORTED",
                f"Imported external CSV policy file '{file.filename}'.",
                current_user.full_name, current_user.role, client_ip
            )
            return parsed_policy
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to parse CSV file: {str(e)}")
    else:
        raise HTTPException(status_code=400, detail="Only .json and .csv files are supported")

# -------------------------------------------------------------
# EVALUATION REPORTS & EXPORT
# -------------------------------------------------------------
@app.get("/api/reports", dependencies=[Depends(get_current_user)])
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

@app.get("/api/reports/{report_id}", dependencies=[Depends(get_current_user)])
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
def export_report_csv(
    report_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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
    client_ip = request.client.host if request.client else "127.0.0.1"
    record_audit(
        db, "REPORT_EXPORTED",
        f"Exported CSV report #{r.id} ('{r.policy_name}', Score: {r.overall_compliance_score}%).",
        current_user.full_name, current_user.role, client_ip, r.overall_compliance_score
    )
    return Response(
        content=content,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=compliance_report_{r.id}.csv"}
    )

# -------------------------------------------------------------
# DASHBOARD STATS & AUDIT LOGS
# -------------------------------------------------------------
@app.get("/api/dashboard/stats", dependencies=[Depends(get_current_user)])
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

@app.get("/api/audit", dependencies=[Depends(require_admin)])
def get_audit_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=100),
    search: str = Query("", max_length=100),
    action: str = Query("", max_length=100),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog)
    if search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(or_(
            AuditLog.action.ilike(term), AuditLog.details.ilike(term),
            AuditLog.user_name.ilike(term), AuditLog.user_role.ilike(term),
            AuditLog.ip_address.ilike(term),
        ))
    if action:
        query = query.filter(AuditLog.action == action)
    total = query.count()
    items = query.order_by(AuditLog.timestamp.desc(), AuditLog.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    actions = [row[0] for row in db.query(AuditLog.action).distinct().order_by(AuditLog.action).all()]
    return {"items": items, "total": total, "page": page, "page_size": page_size, "actions": actions}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "PasswordPolicy Checker",
        "project": "#23 IT23/L",
        "author": "Kristine Paula S. Coretico",
        "engine": "FastAPI + SQLAlchemy + React"
    }

@app.get("/api/integrations/status", dependencies=[Depends(get_current_user)])
def get_integrations_status(db: Session = Depends(get_db)):
    dialect = db.get_bind().dialect.name
    standards_count = db.query(StandardDefinition).count()
    keepalive_enabled = bool(os.getenv("KEEPALIVE_TOKEN"))
    return {
        "database": {
            "provider": "Supabase PostgreSQL (Third-Party Cloud SSL)" if dialect == "postgresql" else "Local SQLite (Embedded)",
            "dialect": dialect,
            "connected": True,
        },
        "benchmarks": {
            "provider": "NIST SP 800-63B, OWASP ASVS v4.0, CIS v8",
            "count": standards_count,
            "status": "Active",
        },
        "policy_import": {
            "endpoint": "/api/policies/import",
            "formats": ["JSON", "CSV"],
            "sources": ["Active Directory GPO", "Linux PAM", "Cloud IAM"],
            "status": "Ready",
        },
        "openapi": {
            "docs_url": "/api/docs",
            "protocol": "REST / HTTPS JSON",
            "status": "Available",
        },
        "hibp": {
            "provider": "Have I Been Pwned (HIBP) Pwned Passwords API",
            "method": "SHA-1 k-anonymity (5-char prefix)",
            "status": "Active",
        },
        "keepalive": {
            "provider": "GitHub Actions Scheduler",
            "configured": keepalive_enabled,
            "status": "Configured" if keepalive_enabled else "Local Mode",
        },
    }

@app.get("/api/keepalive", include_in_schema=False)
def keepalive(
    db: Session = Depends(get_db),
    keepalive_token: Optional[str] = Header(default=None, alias="X-Keepalive-Token"),
):
    configured_token = os.getenv("KEEPALIVE_TOKEN")
    if not configured_token:
        raise HTTPException(status_code=503, detail="Keepalive is not configured")
    if not keepalive_token or not secrets.compare_digest(keepalive_token, configured_token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if db.get_bind().dialect.name != "postgresql":
        raise HTTPException(status_code=503, detail="PostgreSQL is not connected")

    # Read an application table so this checks real database activity.
    db.query(StandardDefinition.id).limit(1).first()
    return {"status": "ok"}

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

