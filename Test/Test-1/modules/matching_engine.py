import math
from typing import Dict, List, Any, Tuple

def evaluate_hard_requirements(user: Dict[str, Any], scholarship: Dict[str, Any]) -> Tuple[bool, List[str], str]:
    """
    Check if the user profile satisfies hard requirements of the scholarship.
    Returns (is_qualified, list_of_missing_requirements, status_label).
    """
    missing = []

    # 1. Degree check
    target_degree = user.get("target_degree", "S2")
    allowed_degrees = scholarship.get("target_degrees", [])
    if allowed_degrees and target_degree not in allowed_degrees:
        missing.append(f"Jenjang {target_degree} tidak didukung (butuh: {', '.join(allowed_degrees)})")

    # 2. Age check
    user_age = user.get("age", 25)
    max_age = scholarship.get("max_age", 99)
    if user_age > max_age:
        missing.append(f"Usia ({user_age} th) melebihi batas maksimum ({max_age} th)")

    # 3. GPA check
    user_gpa = user.get("gpa", 0.0)
    min_gpa = scholarship.get("min_gpa", 0.0)
    if user_gpa < min_gpa:
        missing.append(f"IPK ({user_gpa:.2f}) di bawah syarat minimum ({min_gpa:.2f})")

    # 4. IELTS / Language check
    user_ielts = user.get("ielts_score", 0.0)
    user_toefl = user.get("toefl_ibt_score", 0.0)
    min_ielts = scholarship.get("min_ielts", 0.0)
    min_toefl = scholarship.get("min_toefl_ibt", 0.0)

    language_passed = (user_ielts >= min_ielts) or (min_toefl > 0 and user_toefl >= min_toefl)
    if not language_passed and min_ielts > 0:
        missing.append(f"IELTS ({user_ielts}) di bawah syarat minimum ({min_ielts})")

    # 5. Work experience check
    user_exp = user.get("work_exp_years", 0)
    min_exp = scholarship.get("min_work_exp_years", 0)
    if user_exp < min_exp:
        missing.append(f"Pengalaman kerja ({user_exp} th) di bawah batas ({min_exp} th)")

    is_qualified = len(missing) == 0

    if is_qualified:
        status_label = "Syarat Terpenuhi"
    elif len(missing) == 1:
        status_label = "1 Syarat Belum"
    else:
        status_label = "Perlu Syarat Extra"

    return is_qualified, missing, status_label



def calculate_fit_score(user: Dict[str, Any], scholarship: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate weighted match fit score (%) and classify into Safety, Target, or Reach.
    """
    is_qualified, missing_reqs, status_label = evaluate_hard_requirements(user, scholarship)

    # 1. Academic Score (35%)
    user_gpa = user.get("gpa", 3.0)
    min_gpa = scholarship.get("min_gpa", 3.0)
    gpa_ratio = (user_gpa / max(min_gpa, 2.0)) if min_gpa > 0 else 1.0
    s_academic = min(100.0, gpa_ratio * 80.0 + (user_gpa - min_gpa) * 20.0)

    # 2. Language Score (25%)
    user_ielts = user.get("ielts_score", 6.5)
    min_ielts = scholarship.get("min_ielts", 6.5)
    ielts_ratio = (user_ielts / max(min_ielts, 5.0)) if min_ielts > 0 else 1.0
    s_language = min(100.0, ielts_ratio * 80.0 + (user_ielts - min_ielts) * 15.0)

    # 3. Work Experience Score (20%)
    user_exp = user.get("work_exp_years", 0)
    min_exp = scholarship.get("min_work_exp_years", 0)
    if user_exp >= min_exp:
        s_experience = min(100.0, 80.0 + (user_exp - min_exp) * 10.0)
    else:
        s_experience = max(40.0, 80.0 - (min_exp - user_exp) * 20.0)

    # 4. Achievement & Country Match Score (20%)
    pubs = user.get("publications_count", 0)
    s_pubs = min(40.0, pubs * 20.0)

    user_countries = user.get("target_countries", [])
    scho_countries = scholarship.get("target_countries", [])
    country_overlap = any(c in scho_countries for c in user_countries) if user_countries else True
    s_country = 60.0 if country_overlap else 30.0

    s_achievement = s_pubs + s_country

    # Total Fit Score Calculation
    raw_fit_score = (0.35 * s_academic) + (0.25 * s_language) + (0.20 * s_experience) + (0.20 * s_achievement)
    
    # Penalize fit score if hard requirements are missing
    if not is_qualified:
        raw_fit_score = raw_fit_score * (0.85 ** len(missing_reqs))

    fit_score = round(max(10.0, min(99.0, raw_fit_score)), 1)

    # Opportunity Classifier
    if fit_score >= 80.0:
        category = "Safety"
        badge = "🟢 Safety (≥80%)"
        quadrant = "Rekomendasi Utama"
    elif fit_score >= 60.0:
        category = "Target"
        badge = "🟡 Target (60-79%)"
        quadrant = "Prioritas Penting"
    else:
        category = "Reach"
        badge = "🔴 Reach (<60%)"
        quadrant = "Tantangan Tinggi"

    return {
        "scholarship_id": scholarship.get("id"),
        "scholarship_name": scholarship.get("name"),
        "provider": scholarship.get("provider"),
        "funding_type": scholarship.get("funding_type"),
        "fit_score": fit_score,
        "category": category,
        "badge": badge,
        "quadrant": quadrant,
        "is_qualified": is_qualified,
        "missing_reqs": missing_reqs,
        "status_label": status_label,
        "breakdown": {
            "academic": round(s_academic, 1),
            "language": round(s_language, 1),
            "experience": round(s_experience, 1),
            "achievement": round(s_achievement, 1)
        }
    }


def run_full_matching(user_profile: Dict[str, Any], scholarships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Run matching algorithm across all scholarships and return sorted results by score.
    """
    results = []
    for s in scholarships:
        res = calculate_fit_score(user_profile, s)
        results.append(res)
    
    # Sort descending by fit score
    results.sort(key=lambda x: x["fit_score"], reverse=True)
    return results
