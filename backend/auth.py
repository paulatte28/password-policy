import os
import datetime
import secrets
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, UserSession, LoginState, ActivePolicy

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY and (os.getenv("VERCEL") or os.getenv("RENDER")):
    raise RuntimeError("JWT_SECRET must be set for deployment")
SECRET_KEY = SECRET_KEY or "local-development-only-change-this-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token", auto_error=False)

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    if len(pwd_bytes) > 72:
        raise ValueError("Password must be at most 72 UTF-8 bytes")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: datetime.timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        session_id = payload.get("jti")
        if email is None or session_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    session = db.get(UserSession, session_id)
    user = db.query(User).filter(User.email == email).first()
    if not session or session.expires_at <= datetime.datetime.utcnow() or not user or session.user_id != user.id:
        raise HTTPException(status_code=401, detail="Session expired or signed out")
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    if request.url.path not in ("/api/auth/me", "/api/auth/logout", "/api/auth/change-password"):
        state = db.get(LoginState, user.id)
        active = db.get(ActivePolicy, 1)
        expired = False
        if active and state and state.password_changed_at:
            import json
            days = json.loads(active.rules_json).get("max_password_age_days", 0)
            expired = bool(days and datetime.datetime.utcnow() > state.password_changed_at + datetime.timedelta(days=days))
        if state and (state.must_change_password or expired):
            raise HTTPException(status_code=403, detail="Change your password before continuing")
    return user

def require_role(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation not permitted. Required role: {', '.join(allowed_roles)}"
            )
        return current_user
    return role_checker

require_admin = require_role(["Administrator"])
require_analyst_or_admin = require_role(["Administrator", "Security Analyst"])
