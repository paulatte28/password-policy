import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, DateTime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="Viewer") # Administrator, Security Analyst, Viewer
    department = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class PolicySetting(Base):
    __tablename__ = "policy_settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # 1. Password Length
    min_length = Column(Integer, default=8)
    max_length = Column(Integer, default=64)

    # 2. Password Complexity
    require_uppercase = Column(Boolean, default=True)
    require_lowercase = Column(Boolean, default=True)
    require_digit = Column(Boolean, default=True)
    require_special = Column(Boolean, default=True)
    min_categories = Column(Integer, default=3)

    # 3. Account Lockout
    max_failed_attempts = Column(Integer, default=5)
    lockout_duration_min = Column(Integer, default=15)
    lockout_reset_min = Column(Integer, default=15)

    # 4. Password Expiration
    max_password_age_days = Column(Integer, default=90) # 0 = never expires
    min_password_age_days = Column(Integer, default=1)

    # 5. Password Reuse (History)
    password_history_count = Column(Integer, default=5)

    # Security Hygiene & Defense-in-depth
    disallow_common = Column(Boolean, default=True)
    disallow_username = Column(Boolean, default=True)
    require_mfa = Column(Boolean, default=False)

    is_sample_preset = Column(Boolean, default=False)
    preset_key = Column(String(50), nullable=True) # weak, moderate, strong
    created_by_user = Column(String(255), default="System")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class StandardDefinition(Base):
    __tablename__ = "standard_definitions"

    id = Column(String(100), primary_key=True) # NIST_SP_800_63B, OWASP_ASVS, CIS_BENCHMARK, CUSTOM_ORG
    name = Column(String(255), nullable=False)
    subtitle = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    publisher = Column(String(255), nullable=True)
    
    recommended_min_length = Column(Integer, default=12)
    requires_complexity = Column(Boolean, default=False)
    max_failed_attempts_threshold = Column(Integer, default=5)
    min_lockout_duration_minutes = Column(Integer, default=15)
    recommended_max_password_age_days = Column(Integer, default=0) # 0 = NIST guidance: do not force arbitrary periodic rotation
    recommended_password_history_count = Column(Integer, default=5)
    requires_breached_dictionary_check = Column(Boolean, default=True)
    mfa_recommendation = Column(String(100), default="Required")
    is_custom_editable = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class EvaluationReport(Base):
    __tablename__ = "evaluation_reports"

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String(255), nullable=False)
    standard_id = Column(String(100), nullable=False)
    standard_name = Column(String(255), nullable=False)

    overall_compliance_score = Column(Float, nullable=False) # 0 to 100
    grade_letter = Column(String(5), nullable=False) # A+, A, B, C, D, F
    risk_level = Column(String(50), nullable=False) # Low, Moderate, High, Critical
    executive_summary = Column(Text, nullable=True)

    findings_json = Column(Text, nullable=False) # List of findings with severity, impact, recommendation
    scores_breakdown_json = Column(Text, nullable=False) # Scores per dimension (Length, Complexity, Lockout, Expiration, Reuse, Hygiene)
    policy_snapshot_json = Column(Text, nullable=False)

    passed_count = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)

    evaluated_by_user = Column(String(255), default="Anonymous")
    evaluated_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    user_name = Column(String(255), nullable=False)
    user_role = Column(String(50), nullable=False)
    ip_address = Column(String(100), default="127.0.0.1")
    score_snapshot = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
