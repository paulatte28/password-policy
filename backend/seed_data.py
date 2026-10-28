import json
import datetime
from sqlalchemy.orm import Session
from backend.models import User, PolicySetting, StandardDefinition, EvaluationReport, AuditLog
from backend.auth import hash_password
from backend.compliance_engine import evaluate_policy
from backend.schemas import PolicyInput

def seed_database(db: Session):
    # 1. Seed Users
    if not db.query(User).first():
        users_data = [
            {
                "email": "admin@passwordpolicy.local",
                "full_name": "Kristine Paula S. Coretico",
                "role": "Administrator",
                "department": "Systems Administration & Security Unit",
                "password": "Admin@123456"
            },
            {
                "email": "analyst@passwordpolicy.local",
                "full_name": "Alex Vance",
                "role": "Security Analyst",
                "department": "IT Security & Assurance",
                "password": "Analyst@123456"
            },
            {
                "email": "viewer@passwordpolicy.local",
                "full_name": "Jordan Lee",
                "role": "Viewer",
                "department": "IT Audit & Compliance",
                "password": "Viewer@123456"
            }
        ]
        for u in users_data:
            user = User(
                email=u["email"],
                full_name=u["full_name"],
                role=u["role"],
                department=u["department"],
                hashed_password=hash_password(u["password"]),
                is_active=True,
                created_at=datetime.datetime.utcnow()
            )
            db.add(user)
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

        # Run initial evaluations for the seeded presets so reports are available on initial launch!
        nist_std = db.query(StandardDefinition).filter_by(id="NIST_SP_800_63B").first()
        for p in presets:
            p_input = PolicyInput(
                name=p.name,
                description=p.description,
                min_length=p.min_length,
                max_length=p.max_length,
                require_uppercase=p.require_uppercase,
                require_lowercase=p.require_lowercase,
                require_digit=p.require_digit,
                require_special=p.require_special,
                min_categories=p.min_categories,
                max_failed_attempts=p.max_failed_attempts,
                lockout_duration_min=p.lockout_duration_min,
                lockout_reset_min=p.lockout_reset_min,
                max_password_age_days=p.max_password_age_days,
                min_password_age_days=p.min_password_age_days,
                password_history_count=p.password_history_count,
                disallow_common=p.disallow_common,
                disallow_username=p.disallow_username,
                require_mfa=p.require_mfa
            )
            eval_res = evaluate_policy(p_input, nist_std)
            report = EvaluationReport(
                policy_name=p.name,
                standard_id=nist_std.id,
                standard_name=nist_std.name,
                overall_compliance_score=eval_res["overall_compliance_score"],
                grade_letter=eval_res["grade_letter"],
                risk_level=eval_res["risk_level"],
                executive_summary=eval_res["executive_summary"],
                findings_json=json.dumps([f.dict() for f in eval_res["findings"]]),
                scores_breakdown_json=json.dumps(eval_res["scores_breakdown"].dict()),
                policy_snapshot_json=json.dumps(p_input.dict()),
                passed_count=eval_res["passed_count"],
                warning_count=eval_res["warning_count"],
                failed_count=eval_res["failed_count"],
                evaluated_by_user="Kristine Paula S. Coretico",
                evaluated_at=p.created_at + datetime.timedelta(minutes=10)
            )
            db.add(report)

            # Audit log
            audit = AuditLog(
                action="POLICY_EVALUATION",
                details=f"Evaluated '{p.name}' against {nist_std.name}. Score: {eval_res['overall_compliance_score']}% ({eval_res['grade_letter']})",
                user_name="Kristine Paula S. Coretico",
                user_role="Administrator",
                score_snapshot=eval_res["overall_compliance_score"],
                timestamp=report.evaluated_at
            )
            db.add(audit)
        db.commit()
