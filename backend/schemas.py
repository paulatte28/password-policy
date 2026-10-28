from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Auth schemas
class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    department: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str
    full_name: str
    role: str = "Viewer" # Administrator, Security Analyst, Viewer
    department: Optional[str] = None
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

# Policy Schemas
class PolicyInput(BaseModel):
    name: str = Field(..., example="Enterprise Active Directory Baseline")
    description: Optional[str] = None
    min_length: int = Field(8, ge=1, le=128)
    max_length: int = Field(64, ge=8, le=256)
    require_uppercase: bool = True
    require_lowercase: bool = True
    require_digit: bool = True
    require_special: bool = True
    min_categories: int = Field(3, ge=1, le=4)
    max_failed_attempts: int = Field(5, ge=0, le=50) # 0 = no lockout
    lockout_duration_min: int = Field(15, ge=0, le=1440)
    lockout_reset_min: int = Field(15, ge=0, le=1440)
    max_password_age_days: int = Field(90, ge=0, le=730) # 0 = never
    min_password_age_days: int = Field(1, ge=0, le=30)
    password_history_count: int = Field(5, ge=0, le=50)
    disallow_common: bool = True
    disallow_username: bool = True
    require_mfa: bool = False

class PolicyEvaluateRequest(PolicyInput):
    standard_id: str = "NIST_SP_800_63B"
    save_report: bool = True

class Finding(BaseModel):
    rule_category: str # Length, Complexity, Lockout, Expiration, Reuse, Hygiene
    title: str
    status: str # PASS, WARNING, FAIL
    severity: str # LOW, MEDIUM, HIGH, CRITICAL, INFO
    current_value: str
    standard_requirement: str
    risk_description: str
    recommendation: str

class ScoresBreakdown(BaseModel):
    length_score: float
    complexity_score: float
    lockout_score: float
    expiration_score: float
    reuse_score: float
    hygiene_score: float

class EvaluationResult(BaseModel):
    id: Optional[int] = None
    policy_name: str
    standard_id: str
    standard_name: str
    overall_compliance_score: float
    grade_letter: str
    risk_level: str
    executive_summary: str
    scores_breakdown: ScoresBreakdown
    findings: List[Finding]
    passed_count: int
    warning_count: int
    failed_count: int
    evaluated_at: datetime
    evaluated_by: str

class StandardUpdate(BaseModel):
    recommended_min_length: int
    requires_complexity: bool
    max_failed_attempts_threshold: int
    min_lockout_duration_minutes: int
    recommended_max_password_age_days: int
    recommended_password_history_count: int
    requires_breached_dictionary_check: bool
    mfa_recommendation: str

class AuditLogResponse(BaseModel):
    id: int
    action: str
    details: Optional[str]
    user_name: str
    user_role: str
    ip_address: str
    score_snapshot: Optional[float]
    timestamp: datetime

    class Config:
        from_attributes = True
