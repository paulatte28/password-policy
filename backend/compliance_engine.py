import json
from typing import Tuple, List, Dict, Any
from backend.models import StandardDefinition, PolicySetting
from backend.schemas import PolicyInput, Finding, ScoresBreakdown, EvaluationResult

def evaluate_policy(policy: PolicyInput, standard: StandardDefinition) -> Dict[str, Any]:
    findings: List[Finding] = []

    # -------------------------------------------------------------
    # 1. PASSWORD LENGTH CHECK
    # -------------------------------------------------------------
    length_score = 100.0
    rec_len = standard.recommended_min_length
    
    if policy.min_length < 8:
        length_score = 20.0
        findings.append(Finding(
            rule_category="Length",
            title="Critically Inadequate Minimum Password Length",
            status="FAIL",
            severity="CRITICAL",
            current_value=f"{policy.min_length} characters",
            standard_requirement=f"Minimum {rec_len} characters ({standard.name})",
            risk_description="Passwords shorter than 8 characters can be cracked within minutes or seconds using modern offline GPU clusters and rainbow tables.",
            recommendation=f"Increase minimum password length immediately to at least {rec_len} characters (or 15+ for passphrases)."
        ))
    elif policy.min_length < rec_len:
        deficit = rec_len - policy.min_length
        length_score = max(40.0, 100.0 - (deficit * 15.0))
        findings.append(Finding(
            rule_category="Length",
            title="Sub-optimal Minimum Password Length",
            status="WARNING",
            severity="HIGH",
            current_value=f"{policy.min_length} characters",
            standard_requirement=f"Recommended {rec_len}+ characters ({standard.name})",
            risk_description="While meeting bare legacy minimums, passwords under recommended length remain susceptible to distributed brute-force attacks.",
            recommendation=f"Elevate minimum length to at least {rec_len} characters to align with {standard.name} guidance."
        ))
    else:
        length_score = 100.0
        findings.append(Finding(
            rule_category="Length",
            title="Adequate Minimum Length Benchmark Met",
            status="PASS",
            severity="LOW",
            current_value=f"{policy.min_length} characters",
            standard_requirement=f"Minimum {rec_len} characters",
            risk_description="Adequate length provides sufficient exponential entropy against brute-force attacks.",
            recommendation="Maintain current length policy; consider incentivizing multi-word passphrases (16+ chars)."
        ))

    # Check maximum length truncation risk
    if policy.max_length < 64:
        length_score -= 10.0
        findings.append(Finding(
            rule_category="Length",
            title="Arbitrary Upper Length Limit Truncation Risk",
            status="WARNING",
            severity="MEDIUM",
            current_value=f"Max {policy.max_length} characters",
            standard_requirement="Support at least 64+ characters (NIST SP 800-63B)",
            risk_description="Low maximum lengths artificially prevent users from utilizing long passphrases and password managers.",
            recommendation="Permit maximum password lengths of at least 64 characters (or up to 128 characters)."
        ))

    # -------------------------------------------------------------
    # 2. PASSWORD COMPLEXITY CHECK
    # -------------------------------------------------------------
    complexity_score = 100.0
    active_cats = sum([
        1 if policy.require_uppercase else 0,
        1 if policy.require_lowercase else 0,
        1 if policy.require_digit else 0,
        1 if policy.require_special else 0
    ])

    if standard.requires_complexity:
        if active_cats < 3:
            complexity_score = 40.0
            findings.append(Finding(
                rule_category="Complexity",
                title="Insufficient Character Composition Rules",
                status="FAIL",
                severity="HIGH",
                current_value=f"{active_cats} of 4 character categories required",
                standard_requirement="At least 3-4 categories (Upper, Lower, Number, Symbol)",
                risk_description="Absence of character diversity allows predictable single-charset patterns easily matched by common wordlists.",
                recommendation="Enforce requirements for at least 3 character types including numbers and special symbols."
            ))
        else:
            findings.append(Finding(
                rule_category="Complexity",
                title="Character Complexity Verification Passed",
                status="PASS",
                severity="LOW",
                current_value=f"{active_cats} categories active",
                standard_requirement="Character category diversity enforced",
                risk_description="Diversity enhances password search space when paired with adequate length.",
                recommendation="Ensure error messages guide users to create mnemonic passphrases rather than predictable substitutes (e.g. 'P@ssword1')."
            ))
    else:
        # NIST SP 800-63B philosophy: Composition rules often encourage predictable substitutions (e.g. P@ssword1!)
        if active_cats == 4 and policy.min_length < 12:
            complexity_score = 75.0
            findings.append(Finding(
                rule_category="Complexity",
                title="Strict Composition Rules on Short Passwords (NIST Observation)",
                status="WARNING",
                severity="MEDIUM",
                current_value="Strict 4-category rule with short length",
                standard_requirement="Prioritize length over rigid character rules",
                risk_description="NIST SP 800-63B notes that rigid composition rules lead users to choose predictable patterns rather than truly strong passphrases.",
                recommendation="Consider relaxing rigid character rules in favor of longer minimum length (>= 12-15) and breached password list checking."
            ))
        else:
            findings.append(Finding(
                rule_category="Complexity",
                title="Balanced Complexity Posture",
                status="PASS",
                severity="LOW",
                current_value=f"{active_cats} categories configured",
                standard_requirement="Aligned with modern usability guidance",
                risk_description="Composition rules are appropriately balanced.",
                recommendation="Pair policy with breached dictionary screening."
            ))

    # -------------------------------------------------------------
    # 3. ACCOUNT LOCKOUT CHECK
    # -------------------------------------------------------------
    lockout_score = 100.0
    if policy.max_failed_attempts == 0:
        lockout_score = 0.0
        findings.append(Finding(
            rule_category="Lockout",
            title="Critical Security Vulnerability: No Account Lockout Configured",
            status="FAIL",
            severity="CRITICAL",
            current_value="Lockout Disabled (0 attempts allowed)",
            standard_requirement=f"Lockout after max {standard.max_failed_attempts_threshold} consecutive failures",
            risk_description="Systems without rate limiting or lockout thresholds are defenseless against automated online dictionary attacks and credential stuffing.",
            recommendation=f"Configure account lockout to trigger after {standard.max_failed_attempts_threshold} failed attempts with a minimum {standard.min_lockout_duration_minutes}-minute lockout duration."
        ))
    elif policy.max_failed_attempts > standard.max_failed_attempts_threshold:
        lockout_score = 60.0
        findings.append(Finding(
            rule_category="Lockout",
            title="Excessive Failed Attempt Threshold",
            status="WARNING",
            severity="HIGH",
            current_value=f"{policy.max_failed_attempts} failed attempts allowed",
            standard_requirement=f"Threshold of {standard.max_failed_attempts_threshold} or fewer attempts",
            risk_description="High attempt thresholds grant attackers broader leeway to guess passwords before detection triggers.",
            recommendation=f"Tighten failed attempt limit to {standard.max_failed_attempts_threshold} consecutive failures."
        ))
    else:
        if policy.lockout_duration_min < standard.min_lockout_duration_minutes:
            lockout_score = 75.0
            findings.append(Finding(
                rule_category="Lockout",
                title="Brief Lockout Duration Window",
                status="WARNING",
                severity="MEDIUM",
                current_value=f"{policy.lockout_duration_min} minutes lockout",
                standard_requirement=f"At least {standard.min_lockout_duration_minutes} minutes duration",
                risk_description="Brief lockouts allow automated bots to resume guessing too quickly.",
                recommendation=f"Increase lockout duration to at least {standard.min_lockout_duration_minutes} minutes or implement exponential back-off delays."
            ))
        else:
            findings.append(Finding(
                rule_category="Lockout",
                title="Account Lockout & Brute-Force Defense Active",
                status="PASS",
                severity="LOW",
                current_value=f"Lockout after {policy.max_failed_attempts} fails for {policy.lockout_duration_min} mins",
                standard_requirement="Robust lockout threshold and duration",
                risk_description="Effective barrier against automated credential guessing.",
                recommendation="Combine with CAPTCHA or anomaly-based behavioral detection on repeated locks."
            ))

    # -------------------------------------------------------------
    # 4. PASSWORD EXPIRATION CHECK
    # -------------------------------------------------------------
    expiration_score = 100.0
    if standard.recommended_max_password_age_days == 0:
        # NIST SP 800-63B standard: Periodic rotation is counterproductive unless compromise detected
        if policy.max_password_age_days > 0 and policy.max_password_age_days < 60:
            expiration_score = 70.0
            findings.append(Finding(
                rule_category="Expiration",
                title="Excessively Frequent Password Expiration (NIST Guideline Deviation)",
                status="WARNING",
                severity="MEDIUM",
                current_value=f"Rotates every {policy.max_password_age_days} days",
                standard_requirement="NIST SP 800-63B advises against arbitrary periodic rotation",
                risk_description="Forcing users to rotate passwords every 30-45 days reliably induces predictable pattern modifications (e.g. Summer2025! -> Summer2026!).",
                recommendation="Extend expiration interval or replace periodic rotation with dynamic breach monitoring and MFA."
            ))
        else:
            findings.append(Finding(
                rule_category="Expiration",
                title="Modern Expiration Cycle Aligned",
                status="PASS",
                severity="LOW",
                current_value="No arbitrary aggressive rotation" if policy.max_password_age_days == 0 else f"{policy.max_password_age_days} days",
                standard_requirement="Avoid counterproductive rotation without cause",
                risk_description="Avoids user fatigue while maintaining credential integrity.",
                recommendation="Enforce password reset only upon suspected account compromise or leaked credential alerts."
            ))
    else:
        # Standards requiring periodic change (e.g. PCI-DSS, OWASP ASVS)
        if policy.max_password_age_days == 0:
            expiration_score = 50.0
            findings.append(Finding(
                rule_category="Expiration",
                title="Passwords Never Expire Under Compliance Standard",
                status="WARNING",
                severity="HIGH",
                current_value="Passwords never expire",
                standard_requirement=f"Maximum age of {standard.recommended_max_password_age_days} days ({standard.name})",
                risk_description="Dormant or compromised credentials remain valid indefinitely.",
                recommendation=f"Set maximum password age to {standard.recommended_max_password_age_days} days to satisfy {standard.name}."
            ))
        elif policy.max_password_age_days > standard.recommended_max_password_age_days:
            expiration_score = 70.0
            findings.append(Finding(
                rule_category="Expiration",
                title="Extended Password Lifespan Exceeds Threshold",
                status="WARNING",
                severity="MEDIUM",
                current_value=f"{policy.max_password_age_days} days",
                standard_requirement=f"Max {standard.recommended_max_password_age_days} days",
                risk_description="Long intervals increase the window of opportunity for intercepted credentials.",
                recommendation=f"Align expiration threshold to {standard.recommended_max_password_age_days} days."
            ))
        else:
            findings.append(Finding(
                rule_category="Expiration",
                title="Password Expiration Schedule Compliant",
                status="PASS",
                severity="LOW",
                current_value=f"Expires every {policy.max_password_age_days} days",
                standard_requirement=f"Complies with {standard.name}",
                risk_description="Periodic rotation schedule meets regulatory baseline.",
                recommendation="Ensure minimum password age is at least 1 day to prevent immediate cycling."
            ))

    # -------------------------------------------------------------
    # 5. PASSWORD REUSE (HISTORY) CHECK
    # -------------------------------------------------------------
    reuse_score = 100.0
    rec_hist = standard.recommended_password_history_count
    if policy.password_history_count == 0:
        reuse_score = 25.0
        findings.append(Finding(
            rule_category="Reuse",
            title="No Password History Enforced (Immediate Reuse Vulnerability)",
            status="FAIL",
            severity="HIGH",
            current_value="History = 0 (Immediate reuse allowed)",
            standard_requirement=f"Remember at least {rec_hist} previous passwords",
            risk_description="Users can immediately re-enter their previously compromised or weak passwords, nullifying expiration and remediation policies.",
            recommendation=f"Configure password history to remember at least {rec_hist} previous passwords."
        ))
    elif policy.password_history_count < rec_hist:
        reuse_score = 65.0
        findings.append(Finding(
            rule_category="Reuse",
            title="Limited Password History Depth",
            status="WARNING",
            severity="MEDIUM",
            current_value=f"History remembers {policy.password_history_count} passwords",
            standard_requirement=f"Recommended {rec_hist}+ passwords remembered",
            risk_description="Short history depth allows rapid recycling through a small rotation cycle.",
            recommendation=f"Increase history count to at least {rec_hist} previous entries."
        ))
    else:
        findings.append(Finding(
            rule_category="Reuse",
            title="Password Reuse History Protection Active",
            status="PASS",
            severity="LOW",
            current_value=f"Remembers last {policy.password_history_count} passwords",
            standard_requirement=f"History depth >= {rec_hist}",
            risk_description="Prevents users from cycling back to historic passwords.",
            recommendation="Pair with minimum password age (1 day) so users cannot change passwords 5 times in a minute to restore their favorite password."
        ))

    # -------------------------------------------------------------
    # 6. HYGIENE & DEFENSE-IN-DEPTH CHECKS
    # -------------------------------------------------------------
    hygiene_score = 100.0
    if not policy.disallow_common:
        hygiene_score -= 35.0
        findings.append(Finding(
            rule_category="Hygiene",
            title="Breached & Common Dictionary Screening Disabled",
            status="FAIL",
            severity="CRITICAL",
            current_value="Common passwords permitted",
            standard_requirement="Mandatory check against breached/common password lists (NIST SP 800-63B / OWASP)",
            risk_description="Permits notoriously breached passwords (e.g. 'Password123!', 'Admin@2026') regardless of length or complexity.",
            recommendation="Enable dictionary screening against top compromised password databases (HaveIBeenPwned / SecLists)."
        ))
    else:
        findings.append(Finding(
            rule_category="Hygiene",
            title="Breached Dictionary Screening Active",
            status="PASS",
            severity="LOW",
            current_value="Disallows common & breached passwords",
            standard_requirement="Screens against known dictionaries",
            risk_description="Eliminates the #1 attack vector of credential stuffing.",
            recommendation="Ensure the dictionary is periodically refreshed with newly leaked breach corpuses."
        ))

    if not policy.disallow_username:
        hygiene_score -= 25.0
        findings.append(Finding(
            rule_category="Hygiene",
            title="Username & Identity Context Not Filtered",
            status="WARNING",
            severity="MEDIUM",
            current_value="Username substrings permitted in password",
            standard_requirement="Disallow username, email handle, or organization name in password",
            risk_description="Allows easily predictable contextual passwords such as 'Alex@2026' or 'CompanyAdmin!'.",
            recommendation="Enforce validation that rejects passwords containing username or email tokens."
        ))

    if policy.require_mfa:
        hygiene_score = min(100.0, hygiene_score + 10.0)
        findings.append(Finding(
            rule_category="Hygiene",
            title="Multi-Factor Authentication (MFA) Enforced",
            status="PASS",
            severity="LOW",
            current_value="MFA Required alongside password",
            standard_requirement="Defense-in-depth authentication",
            risk_description="Provides resilience even in the event of primary credential leakage.",
            recommendation="Adopt FIDO2 / WebAuthn or TOTP authenticators over SMS OTP."
        ))
    else:
        if standard.mfa_recommendation == "Required":
            hygiene_score -= 20.0
            findings.append(Finding(
                rule_category="Hygiene",
                title="MFA Not Required Under High-Security Baseline",
                status="WARNING",
                severity="HIGH",
                current_value="Single-factor password only",
                standard_requirement=f"MFA Required ({standard.name})",
                risk_description="Passwords alone without secondary verification leave accounts vulnerable to phishing and session hijacking.",
                recommendation="Mandate Multi-Factor Authentication (MFA) for administrative and privileged user accounts."
            ))

    hygiene_score = max(0.0, min(100.0, hygiene_score))

    # -------------------------------------------------------------
    # OVERALL SCORE & RISK CALCULATION
    # -------------------------------------------------------------
    # Weighted average:
    # Length: 30%, Lockout: 25%, Complexity: 15%, Expiration: 10%, Reuse: 10%, Hygiene: 10%
    overall_score = (
        (length_score * 0.30) +
        (lockout_score * 0.25) +
        (complexity_score * 0.15) +
        (expiration_score * 0.10) +
        (reuse_score * 0.10) +
        (hygiene_score * 0.10)
    )
    overall_score = round(max(0.0, min(100.0, overall_score)), 1)

    # Letter Grade
    if overall_score >= 93.0:
        grade_letter = "A+"
    elif overall_score >= 85.0:
        grade_letter = "A"
    elif overall_score >= 75.0:
        grade_letter = "B"
    elif overall_score >= 65.0:
        grade_letter = "C"
    elif overall_score >= 50.0:
        grade_letter = "D"
    else:
        grade_letter = "F"

    # Risk Level
    crit_count = sum(1 for f in findings if f.severity == "CRITICAL" and f.status == "FAIL")
    high_count = sum(1 for f in findings if f.severity == "HIGH" and f.status in ["FAIL", "WARNING"])
    
    if crit_count > 0 or overall_score < 50.0:
        risk_level = "Critical"
    elif high_count > 1 or overall_score < 70.0:
        risk_level = "High"
    elif overall_score < 85.0:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    passed_count = sum(1 for f in findings if f.status == "PASS")
    warning_count = sum(1 for f in findings if f.status == "WARNING")
    failed_count = sum(1 for f in findings if f.status == "FAIL")

    # Executive Summary Text
    exec_summary = (
        f"Policy '{policy.name}' achieved a compliance rating of {overall_score}/100 (Grade {grade_letter}) "
        f"against benchmark standard '{standard.name}'. The calculated security posture reflects a {risk_level} Risk Level. "
        f"The evaluation uncovered {failed_count} failing condition(s), {warning_count} warning(s), and {passed_count} compliant rule(s)."
    )
    if crit_count > 0:
        exec_summary += " Immediate remediation is recommended for critical vulnerabilities in length, lockout, or dictionary screening."

    scores_breakdown = ScoresBreakdown(
        length_score=round(length_score, 1),
        complexity_score=round(complexity_score, 1),
        lockout_score=round(lockout_score, 1),
        expiration_score=round(expiration_score, 1),
        reuse_score=round(reuse_score, 1),
        hygiene_score=round(hygiene_score, 1)
    )

    return {
        "overall_compliance_score": overall_score,
        "grade_letter": grade_letter,
        "risk_level": risk_level,
        "executive_summary": exec_summary,
        "scores_breakdown": scores_breakdown,
        "findings": findings,
        "passed_count": passed_count,
        "warning_count": warning_count,
        "failed_count": failed_count
    }
