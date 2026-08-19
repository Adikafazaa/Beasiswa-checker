import sqlite3
import os
from datetime import datetime
from rich.console import Console

console = Console()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_DIR = os.path.join(PROJECT_ROOT, "data")
DB_PATH = os.path.join(DB_DIR, "scholarships.db")



def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Connect to SQLite database with WAL mode and foreign keys enabled."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def run_migrations(db_path: str = DB_PATH) -> None:
    """
    Zero-dependency Migration Engine:
    Initializes and verifies the 6 core database tables specified in Brainstorm Revision:
    1. schema_migrations
    2. user_profiles
    3. scholarships
    4. user_scholarship_flags (Multi-User Bookmark & Notes isolation)
    5. user_match_history
    6. scrape_logs
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # 1. Table schema_migrations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schema_migrations (
        version INTEGER PRIMARY KEY,
        description TEXT NOT NULL,
        applied_at TEXT NOT NULL
    );
    """)

    # 2. Table user_profiles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gpa REAL NOT NULL DEFAULT 3.0,
        ielts_score REAL NOT NULL DEFAULT 6.5,
        toefl_ibt_score REAL NOT NULL DEFAULT 80.0,
        age INTEGER NOT NULL DEFAULT 24,
        target_degree TEXT NOT NULL DEFAULT 'S2',
        major_field TEXT NOT NULL DEFAULT 'General',
        work_exp_years INTEGER NOT NULL DEFAULT 0,
        publications_count INTEGER NOT NULL DEFAULT 0,
        target_countries TEXT NOT NULL DEFAULT '[]',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """)

    try:
        cursor.execute("ALTER TABLE user_profiles ADD COLUMN last_ai_analysis TEXT DEFAULT '';")
    except Exception:
        pass

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scholarships (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        provider TEXT NOT NULL,
        funding_type TEXT NOT NULL DEFAULT 'Fully Funded',
        target_degrees TEXT NOT NULL DEFAULT '[]',
        target_countries TEXT NOT NULL DEFAULT '[]',
        min_gpa REAL DEFAULT 0.0,
        min_ielts REAL DEFAULT 0.0,
        min_toefl_ibt REAL DEFAULT 0.0,
        max_age INTEGER DEFAULT 99,
        min_work_exp_years INTEGER DEFAULT 0,
        required_documents TEXT DEFAULT '[]',
        deadline_date TEXT DEFAULT '2026-12-31',
        source_url TEXT DEFAULT '',
        description TEXT DEFAULT '',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    try:
        cursor.execute("ALTER TABLE scholarships ADD COLUMN updated_at TEXT DEFAULT '';")
    except Exception:
        pass



    # 4. Table user_scholarship_flags (Isolated Bookmark, Priority & Personal Notes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_scholarship_flags (
        user_id TEXT NOT NULL,
        scholarship_id TEXT NOT NULL,
        is_bookmarked INTEGER NOT NULL DEFAULT 0,
        priority TEXT NOT NULL DEFAULT 'NONE',
        status TEXT NOT NULL DEFAULT 'SAVED',
        user_notes TEXT DEFAULT '',
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id, scholarship_id),
        FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
    );
    """)

    # 5. Table user_match_history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_match_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        scholarship_id TEXT NOT NULL,
        fit_score REAL NOT NULL,
        category TEXT NOT NULL,
        calculated_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user_profiles(id) ON DELETE CASCADE,
        FOREIGN KEY (scholarship_id) REFERENCES scholarships(id) ON DELETE CASCADE
    );
    """)

    # 6. Table scrape_logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scrape_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_name TEXT NOT NULL,
        status TEXT NOT NULL,
        records_scraped INTEGER DEFAULT 0,
        records_inserted INTEGER DEFAULT 0,
        error_message TEXT DEFAULT '',
        scraped_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Record migration version 1
    cursor.execute("SELECT COUNT(*) FROM schema_migrations WHERE version = 1")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO schema_migrations (version, description, applied_at) VALUES (?, ?, ?)",
            (1, "Initial 6-table multi-user schema", datetime.now().isoformat())
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    run_migrations()
    print("Database migrations verified successfully!")
