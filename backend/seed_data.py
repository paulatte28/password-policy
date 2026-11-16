import datetime
import os
from sqlalchemy.orm import Session
from backend.models import User, PolicySetting, StandardDefinition
from backend.auth import hash_password, verify_password

def seed_database(db: Session):
    # Disable accounts that still have the publicly documented demo passwords.
    for email, password in (
        ("admin@passwordpolicy.local", "Admin@123456"),
        ("analyst@passwordpolicy.local", "Analyst@123456"),
        ("viewer@passwordpolicy.local", "Viewer@123456"),
    ):
        demo = db.query(User).filter(User.email == email).first()
        if demo and verify_password(password, demo.hashed_password):
            demo.is_active = False
    db.commit()

    # Initial administrator is supplied privately through environment variables.
    email = os.getenv("BOOTSTRAP_ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("BOOTSTRAP_ADMIN_PASSWORD", "")
    if email and password and not db.query(User).filter(User.role == "Administrator", User.is_active == True).first():
        if len(password) < 15 or len(password.encode("utf-8")) > 72:
            raise RuntimeError("BOOTSTRAP_ADMIN_PASSWORD must be 15-72 UTF-8 bytes")
        admin = db.query(User).filter(User.email == email).first()
        if admin is None:
            admin = User(email=email, full_name="Administrator", role="Administrator", hashed_password=hash_password(password), is_active=True)
            db.add(admin)
        else:
            admin.hashed_password = hash_password(password)
            admin.role = "Administrator"
            admin.is_active = True
        db.commit()

    # 2. Seed Standards
    if not db.query(StandardDefinition).first():
        standards = [
            StandardDefinition(
                id="NIST_SP_800_63B",
                name="NIST SP 800-63B Guidelines",
                subtitle="Digital Identity Guidelines: Authentication and Lifecycle Management",
                description="The premier modern benchmark for identity and authentication published by the National Institute of Standards and Technology. Recommends passphrase length (>=8 chars, 12-15+ recommended), screening against breached dictionaries, avoiding arbitrary periodic expiration, and eliminating counterproductive character composition rules.",
                publisher="National Institute of Standards and Technology (NIST)",
                recommended_min_length=12,
                requires_complexity=False,
                max_failed_attempts_threshold=5,
                min_lockout_duration_minutes=15,
                recommended_max_password_age_days=0, # 0 = No arbitrary rotation
                recommended_password_history_count=5,
                requires_breached_dictionary_check=True,
                mfa_recommendation="Required",
                is_custom_editable=False,
                updated_at=datetime.datetime.utcnow()
            ),
            StandardDefinition(
                id="OWASP_ASVS",
                name="OWASP ASVS v4.0",
                subtitle="Application Security Verification Standard - Authentication Verification",
                description="The Open Web Application Security Project standard for secure authentication. Emphasizes passwords of at least 12 characters, strong lockout defenses against brute force, secure password history, and defense-in-depth against credential stuffing.",
                publisher="OWASP Foundation",
                recommended_min_length=12,
                requires_complexity=True,
                max_failed_attempts_threshold=5,
                min_lockout_duration_minutes=30,
                recommended_max_password_age_days=90,
                recommended_password_history_count=10,
                requires_breached_dictionary_check=True,
                mfa_recommendation="Required",
                is_custom_editable=False,
                updated_at=datetime.datetime.utcnow()
            ),
            StandardDefinition(
                id="CIS_BENCHMARK",
                name="CIS Security Benchmark v8",
                subtitle="Center for Internet Security Critical Security Controls",
                description="Rigorous institutional controls requiring minimum 14-character passwords, strict lockout after 5 invalid attempts, and extensive password history retention.",
                publisher="Center for Internet Security",
                recommended_min_length=14,
                requires_complexity=True,
                max_failed_attempts_threshold=5,
                min_lockout_duration_minutes=15,
                recommended_max_password_age_days=90,
                recommended_password_history_count=12,
                requires_breached_dictionary_check=True,
                mfa_recommendation="Required",
                is_custom_editable=False,
                updated_at=datetime.datetime.utcnow()
            ),
            StandardDefinition(
                id="CUSTOM_ORG",
                name="Custom Organizational Baseline",
                subtitle="Configurable Internal Password Policy Specification",
                description="User-defined baseline designed for institutional adjustments, custom audit rules, and educational demonstrations.",
                publisher="Internal Systems Administration Unit",
                recommended_min_length=10,
                requires_complexity=True,
                max_failed_attempts_threshold=5,
                min_lockout_duration_minutes=15,
                recommended_max_password_age_days=90,
                recommended_password_history_count=5,
                requires_breached_dictionary_check=True,
                mfa_recommendation="Recommended",
                is_custom_editable=True,
                updated_at=datetime.datetime.utcnow()
            )
        ]
        db.add_all(standards)
        db.commit()

    # 3. Seed Sample Presets (Weak, Moderate, Strong)
    if not db.query(PolicySetting).first():
        presets = [
            PolicySetting(
                name="Weak Legacy Policy",
                description="Typical outdated legacy configuration with 6-character requirement, no account lockout, arbitrary 30-day rotation, and no dictionary check.",
                min_length=6,
                max_length=16,
                require_uppercase=False,
                require_lowercase=True,
                require_digit=True,
                require_special=False,
                min_categories=2,
                max_failed_attempts=0, # No lockout!
                lockout_duration_min=0,
                lockout_reset_min=0,
                max_password_age_days=30,
                min_password_age_days=0,
                password_history_count=0, # Immediate reuse!
                disallow_common=False,
                disallow_username=False,
                require_mfa=False,
                is_sample_preset=True,
                preset_key="weak",
                created_by_user="Kristine Paula S. Coretico",
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=7)
            ),
            PolicySetting(
                name="Moderate Enterprise Baseline",
                description="Common corporate configuration with 8 characters, 3 character categories, 10-attempt lockout, 90-day expiration, and basic history.",
                min_length=8,
                max_length=64,
                require_uppercase=True,
                require_lowercase=True,
                require_digit=True,
                require_special=False,
                min_categories=3,
                max_failed_attempts=10,
                lockout_duration_min=15,
                lockout_reset_min=15,
                max_password_age_days=90,
                min_password_age_days=1,
                password_history_count=3,
                disallow_common=True,
                disallow_username=True,
                require_mfa=False,
                is_sample_preset=True,
                preset_key="moderate",
                created_by_user="Kristine Paula S. Coretico",
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=5)
            ),
            PolicySetting(
                name="Strong NIST SP 800-63B Passphrase Policy",
                description="Modern security baseline featuring 15+ character passphrases, strict 5-attempt lockout, breach dictionary filtering, username exclusion, and MFA.",
                min_length=15,
                max_length=128,
                require_uppercase=True,
                require_lowercase=True,
                require_digit=True,
                require_special=True,
                min_categories=3,
                max_failed_attempts=5,
                lockout_duration_min=30,
                lockout_reset_min=30,
                max_password_age_days=0, # No arbitrary rotation
                min_password_age_days=1,
                password_history_count=10,
                disallow_common=True,
                disallow_username=True,
                require_mfa=True,
                is_sample_preset=True,
                preset_key="strong",
                created_by_user="Kristine Paula S. Coretico",
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=2)
            )
        ]
        db.add_all(presets)
        db.commit()
