import json
import datetime
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.auth import verify_password
from backend.models import ActivePolicy, LoginState, PasswordHistory
from backend.schemas import PolicyInput

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "123456789", "qwerty",
    "abc123", "admin", "admin123", "admin@123", "admin@123456", "analyst@123456",
    "viewer@123456", "letmein", "welcome", "monkey", "dragon", "111111", "iloveyou",
    "passw0rd", "p@ssword", "p@ssw0rd", "changeme", "default", "root", "toor",
}


def get_active_policy(db: Session) -> Optional[PolicyInput]:
    active = db.get(ActivePolicy, 1)
    if not active:
        return None
    return PolicyInput(**json.loads(active.rules_json))


def get_login_state(db: Session, user_id: int) -> LoginState:
    state = db.get(LoginState, user_id)
    if state is None:
        state = LoginState(
            user_id=user_id,
            failed_attempts=0,
            password_changed_at=datetime.datetime.utcnow(),
            must_change_password=False,
        )
        db.add(state)
        db.flush()
    return state


def remember_password(db: Session, user_id: int) -> None:
    state = get_login_state(db, user_id)
    state.password_changed_at = datetime.datetime.utcnow()
    state.must_change_password = False


def validate_password(
    password: str,
    email: str,
    policy: Optional[PolicyInput],
    db: Session,
    user_id: Optional[int] = None,
    enforce_age: bool = True,
) -> None:
    if len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password must be at most 72 UTF-8 bytes")

    if policy is None:
        if len(password) < 8:
            raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
        return

    problems = []
    if len(password) < policy.min_length:
        problems.append(f"at least {policy.min_length} characters")
    if policy.max_length and len(password) > policy.max_length:
        problems.append(f"at most {policy.max_length} characters")

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if policy.require_uppercase and not has_upper:
        problems.append("an uppercase letter")
    if policy.require_lowercase and not has_lower:
        problems.append("a lowercase letter")
    if policy.require_digit and not has_digit:
        problems.append("a digit")
    if policy.require_special and not has_special:
        problems.append("a special character")

    categories = sum([has_upper, has_lower, has_digit, has_special])
    if categories < policy.min_categories:
        problems.append(f"at least {policy.min_categories} character categories")

    if policy.disallow_username and email:
        local_part = email.split("@")[0].lower()
        if local_part and len(local_part) >= 3 and local_part in password.lower():
            problems.append("must not contain your username/email")

    if policy.disallow_common and password.lower() in COMMON_PASSWORDS:
        problems.append("must not be a common/breached password")

    if user_id and policy.password_history_count > 0:
        recent_hashes = (
            db.query(PasswordHistory)
            .filter(PasswordHistory.user_id == user_id)
            .order_by(PasswordHistory.id.desc())
            .limit(policy.password_history_count)
            .all()
        )
        if any(verify_password(password, h.password_hash) for h in recent_hashes):
            problems.append(f"cannot reuse any of your last {policy.password_history_count} passwords")

    if enforce_age and user_id and policy.min_password_age_days > 0:
        state = get_login_state(db, user_id)
        if not state.must_change_password and state.password_changed_at:
            earliest = state.password_changed_at + datetime.timedelta(days=policy.min_password_age_days)
            if datetime.datetime.utcnow() < earliest:
                problems.append(f"cannot change password more than once every {policy.min_password_age_days} day(s)")

    if problems:
        raise HTTPException(status_code=400, detail="Password policy violation: " + "; ".join(problems))
