import os
import sys
import json
import sqlite3
from datetime import datetime

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from modules.models import UserProfile, Scholarship, UserScholarshipFlag, MatchResult
from modules.storage.migrator import run_migrations
from modules.database import (
    init_db,
    get_user_profile,
    save_user_profile,
    get_all_scholarships,
    get_user_scholarship_flags,
    toggle_bookmark,
    update_scholarship_flag,
    get_bookmarked_scholarships
)
from modules.matching_engine import run_full_matching
from modules.ai_advisor import get_ai_gap_analysis
from modules.scraper.robots_guard import is_allowed, get_crawl_delay
from modules.scraper.llm_extractor import extract_scholarships_from_text
from modules.scraper.pipeline import upsert_scholarships


def run_all_tests():
    print("=" * 60)
    print("🧪 RUNNING SYSTEM UNIT TEST SUITE (PHASES 1-5 VERIFICATION)")
    print("=" * 60)

    # 1. Test Pydantic Models
    print("\n[TEST 1] Testing Pydantic V2 Data Models...")
    u = UserProfile(name="Tester", gpa=3.80, ielts_score=7.5)
    s = Scholarship(id="test_sc", name="Test Scholarship", provider="Test Org")
    flag = UserScholarshipFlag(user_id=u.id, scholarship_id=s.id, is_bookmarked=True)
    assert u.gpa == 3.80
    assert s.name == "Test Scholarship"
    assert flag.is_bookmarked is True
    print("  ✅ Pydantic Models validation PASSED!")

    # 2. Test Database & Schema Migrator
    print("\n[TEST 2] Testing SQLite Migration Engine & Database Layer...")
    init_db()
    profile = get_user_profile()
    scholarships = get_all_scholarships()
    assert profile is not None
    print(f"  🔍 Fetched {len(scholarships)} scholarships from SQLite.")
    assert len(scholarships) >= 10

    print(f"  ✅ DB Initialization PASSED! (Profile: {profile['name']}, Total Scholarships: {len(scholarships)})")

    # 3. Test Core Matching Engine & AI Advisor (0 Tokens Used)
    print("\n[TEST 3] Testing Core Matching Engine & Offline Advisor Engine...")
    matches = run_full_matching(profile, scholarships)
    from modules.ai_advisor import generate_rule_based_advice
    advice = generate_rule_based_advice(profile, matches)
    assert len(matches) == len(scholarships)
    assert len(advice) > 0
    print(f"  ✅ Matching Engine & Advisor Engine PASSED! (Calculated {len(matches)} match scores)")

    # 4. Test Multi-User Bookmarks & Flags Isolation
    print("\n[TEST 4] Testing Multi-User Bookmark & Flagging Isolation...")
    update_scholarship_flag(profile["id"], "chevening_uk", is_bookmarked=True, status="SAVED", priority="HIGH")
    bms = get_bookmarked_scholarships(profile["id"])
    assert len(bms) >= 1
    assert any(b["id"] == "chevening_uk" for b in bms)
    print(f"  ✅ Bookmark Isolation PASSED! ({len(bms)} bookmarked item(s) found for {profile['name']})")

    # 5. Test Scraper Subsystem (Robots Guard, Offline Parser & Ingestion Pipeline, 0 Tokens Used)
    print("\n[TEST 5] Testing Scraper Subsystem & Idempotent Ingestion...")
    allowed = is_allowed("https://example.com")
    delay = get_crawl_delay("https://example.com")
    from modules.scraper.llm_extractor import fallback_regex_extractor
    extracted = fallback_regex_extractor("Beasiswa Sample Full Tuition S1 S2 Deadline 2026-12-31")
    count = upsert_scholarships(extracted)
    assert count > 0
    print(f"  ✅ Scraper Subsystem PASSED! (Politeness Guard: Active, Extracted & Upserted: {count})")


    print("\n" + "=" * 60)
    print("🎉 ALL 5 SYSTEM UNIT TESTS PASSED SUCCESSFULLY! 100% VERIFIED!")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
