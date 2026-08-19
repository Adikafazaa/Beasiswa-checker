import os
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DB_PATH = os.path.join(DB_DIR, "scholarships.db")


def get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Ensure data directory exists and return a SQLite database connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """Initialize database tables and populate seed data if empty."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Create scholarships table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scholarships (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        provider TEXT NOT NULL,
        funding_type TEXT NOT NULL,
        target_degrees TEXT NOT NULL,
        target_countries TEXT NOT NULL,
        min_gpa REAL,
        min_ielts REAL,
        min_toefl_ibt REAL,
        max_age INTEGER,
        min_work_exp_years INTEGER DEFAULT 0,
        required_documents TEXT,
        deadline_date TEXT,
        source_url TEXT,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create user_profiles table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profiles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        gpa REAL NOT NULL,
        ielts_score REAL NOT NULL,
        toefl_ibt_score REAL DEFAULT 0.0,
        age INTEGER NOT NULL,
        target_degree TEXT NOT NULL,
        major_field TEXT,
        work_exp_years INTEGER DEFAULT 0,
        publications_count INTEGER DEFAULT 0,
        target_countries TEXT NOT NULL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    
    # Check if scholarships table is empty, if so populate seed data
    cursor.execute("SELECT COUNT(*) as count FROM scholarships")
    if cursor.fetchone()["count"] == 0:
        seed_default_scholarships(conn)

    # Check if user profile exists, if not populate default sample profile
    cursor.execute("SELECT COUNT(*) as count FROM user_profiles")
    if cursor.fetchone()["count"] == 0:
        seed_default_profile(conn)

    conn.close()


def seed_default_scholarships(conn: sqlite3.Connection) -> None:
    """Insert default curated scholarship data into scholarships table."""
    seed_data = [
        (
            "chevening_uk",
            "Chevening UK Scholarship",
            "UK Foreign, Commonwealth & Development Office",
            "Fully Funded",
            json.dumps(["S2"]),
            json.dumps(["UK"]),
            3.3,
            6.5,
            79.0,
            99,
            2,
            json.dumps(["Passport", "Degree Certificate", "Transcripts", "2 Recommendation Letters", "4 Essays"]),
            "2026-11-03",
            "https://www.chevening.org",
            "Beasiswa bergengsi dari Pemerintah Inggris untuk program Magister (S2) selama 1 tahun di universitas terkemuka UK."
        ),
        (
            "lpdp_reguler",
            "LPDP Reguler (Magister / Doktor)",
            "Kementerian Keuangan RI",
            "Fully Funded",
            json.dumps(["S2", "S3"]),
            json.dumps(["UK", "USA", "Europe", "Australia", "Asia", "Indonesia"]),
            3.0,
            6.5,
            80.0,
            35,
            0,
            json.dumps(["KTP/Paspor", "Ijazah & Transkrip", "Sertifikat Bahasa", "Esai Komitmen", "Surat Rekomendasi"]),
            "2026-06-30",
            "https://lpdp.kemenkeu.go.id",
            "Beasiswa penuh dari Pemerintah Indonesia untuk anak bangsa yang ingin melanjutkan studi S2/S3 di dalam atau luar negeri."
        ),
        (
            "erasmus_mundus",
            "Erasmus Mundus Joint Master",
            "European Union",
            "Fully Funded",
            json.dumps(["S2"]),
            json.dumps(["Europe", "UK"]),
            3.2,
            6.5,
            90.0,
            99,
            0,
            json.dumps(["CV Europass", "Motivation Letter", "2 Recommendation Letters", "Transcripts", "IELTS/TOEFL"]),
            "2026-12-15",
            "https://ec.europa.eu/erasmus-plus",
            "Beasiswa Uni Eropa yang memungkinkan mahasiswa belajar di konsorsium 2-3 universitas di negara Eropa berbeda."
        ),
        (
            "gates_cambridge",
            "Gates Cambridge Scholarship",
            "Bill & Melinda Gates Foundation",
            "Fully Funded",
            json.dumps(["S2", "S3"]),
            json.dumps(["UK"]),
            3.8,
            7.5,
            110.0,
            99,
            1,
            json.dumps(["Research Proposal", "Gates Statement", "3 Reference Letters", "Academic Transcripts"]),
            "2026-10-14",
            "https://www.gatescambridge.org",
            "Beasiswa paling kompetitif untuk studi pascasarjana di University of Cambridge dengan fokus pada kepemimpinan dan komitmen sosial."
        ),
        (
            "australia_awards",
            "Australia Awards Scholarships (AAS)",
            "Australian Department of Foreign Affairs and Trade",
            "Fully Funded",
            json.dumps(["S2", "S3"]),
            json.dumps(["Australia"]),
            2.9,
            6.0,
            78.0,
            45,
            2,
            json.dumps(["Ijazah & Transkrip", "Sertifikat IELTS/TOEFL", "KTP/Paspor", "Esai Kontribusi"]),
            "2026-04-30",
            "https://www.australiaawardsindonesia.org",
            "Beasiswa penuh dari Pemerintah Australia untuk pembangunan SDM Indonesia melalui jenjang Master dan PhD."
        ),
        (

            "mext_embassy",
            "MEXT Research Student Scholarship",
            "Pemerintah Jepang (Monbukagakusho)",
            "Fully Funded",
            json.dumps(["S2", "S3"]),
            json.dumps(["Japan", "Asia"]),
            3.2,
            6.0,
            80.0,
            34,
            0,
            json.dumps(["Lembar Aplikasi", "Rencana Penelitian (Research Plan)", "Rekomendasi Dekan", "Transkrip Nilai"]),
            "2026-05-15",
            "https://www.id.emb-japan.go.jp",
            "Beasiswa Pemerintah Jepang untuk program riset pascasarjana dengan fasilitasi bebas biaya kuliah dan tunjangan bulanan."
        ),

        (
            "beasiswa_unggulan",
            "Beasiswa Unggulan Kemdikbud",
            "Kementerian Pendidikan & Kebudayaan RI",
            "Fully Funded",
            json.dumps(["S1", "S2", "S3"]),
            json.dumps(["Indonesia"]),
            3.0,
            0.0,
            0.0,
            35,
            0,
            json.dumps(["KTP", "KTM / Surat Diterima PT", "Transkrip Nilai / Rapor", "Esai Kemajuan Bangsa", "Sertifikat Prestasi"]),
            "2026-08-15",
            "https://beasiswaunggulan.kemdikbud.go.id",
            "Beasiswa penuh dari Kemdikbudristek untuk mahasiswa berprestasi jenjang S1, S2, dan S3 di perguruan tinggi terakreditasi."
        ),
        (
            "djarum_beasiswa_plus",
            "Djarum Beasiswa Plus (S1)",
            "Djarum Foundation",
            "Partial Funded",
            json.dumps(["S1"]),
            json.dumps(["Indonesia"]),
            3.0,
            0.0,
            0.0,
            25,
            0,
            json.dumps(["Form Pendaftaran Online", "Transkrip Nilai Semester 4", "Surat Keterangan Aktif Organisasi", "Foto 4x6"]),
            "2026-05-30",
            "https://djarumbeasiswaplus.org",
            "Beasiswa prestasi plus pelatihan soft skills (leadership, character building, nation building) untuk mahasiswa S1 semester 4."
        ),
        (
            "karya_salemba_empat",
            "Beasiswa Karya Salemba Empat (KSE)",
            "Yayasan Karya Salemba Empat",
            "Partial Funded",
            json.dumps(["S1"]),
            json.dumps(["Indonesia"]),
            3.0,
            0.0,
            0.0,
            23,
            0,
            json.dumps(["Form KSE", "KTP / KTM", "Slip Gaji Orang Tua", "Transkrip IPK", "Esai Motivasi"]),
            "2026-04-25",
            "https://kse.or.id",
            "Beasiswa pendidikan dan tunjangan hidup bagi mahasiswa S1 di 35 Perguruan Tinggi Negeri mitra KSE di Indonesia."
        ),
        (
            "mext_undergraduate",
            "MEXT Undergraduate Scholarship (Gakubu S1)",
            "Pemerintah Jepang (Monbukagakusho)",
            "Fully Funded",
            json.dumps(["S1"]),
            json.dumps(["Japan", "Asia"]),
            3.2,
            6.0,
            75.0,
            24,
            0,
            json.dumps(["Form Aplikasi MEXT S1", "Transkrip SMA / PT", "Surat Rekomendasi Sekolah", "Sertifikat Bahasa"]),
            "2026-05-20",
            "https://www.id.emb-japan.go.jp",
            "Beasiswa kuliah S1 penuh di universitas Jepang selama 5 tahun (termasuk 1 tahun persiapan bahasa Jepang)."
        ),
        (
            "fulbright_ugrad",
            "Global UGRAD Exchange Scholarship",
            "AMINEF / US Department of State",
            "Fully Funded",
            json.dumps(["S1"]),
            json.dumps(["USA"]),
            3.0,
            6.0,
            75.0,
            25,
            0,
            json.dumps(["2 Surat Rekomendasi", "Transkrip Akademik", "Esai Motivasi", "KTP / Paspor"]),
            "2026-12-31",
            "https://www.aminef.or.id",
            "Program pertukaran mahasiswa S1 selama 1 semester di universitas ternama Amerika Serikat."
        ),
        (
            "bca_finance_scholarship",
            "BCA Finance Scholarship (S1)",
            "PT BCA Finance",
            "Partial Funded",
            json.dumps(["S1"]),
            json.dumps(["Indonesia"]),
            3.2,
            0.0,
            0.0,
            25,
            0,
            json.dumps(["Surat Keterangan Tidak Mampu / Slip Gaji", "Transkrip IPK", "KTP / KTM"]),
            "2026-07-15",
            "https://bcafinance.co.id",
            "Bantuan dana pendidikan hingga lulus semester 8 untuk mahasiswa S1 PTN/PTS di seluruh Indonesia."
        )
    ]

    conn.executemany("""
    INSERT OR IGNORE INTO scholarships (
        id, name, provider, funding_type, target_degrees, target_countries,
        min_gpa, min_ielts, min_toefl_ibt, max_age, min_work_exp_years,
        required_documents, deadline_date, source_url, description
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, seed_data)
    conn.commit()



def seed_default_profile(conn: sqlite3.Connection) -> None:
    """Insert default initial user profile."""
    default_profile = (
        "default_user",
        "Adika",
        3.65,
        6.5,
        85.0,
        24,
        "S2",
        "Computer Science",
        2,
        1,
        json.dumps(["UK", "Europe", "Australia"])
    )

    conn.execute("""
    INSERT INTO user_profiles (
        id, name, gpa, ielts_score, toefl_ibt_score, age, target_degree,
        major_field, work_exp_years, publications_count, target_countries
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, default_profile)
    conn.commit()


def get_user_profile(user_id: str = None, db_path: str = DB_PATH) -> Optional[Dict[str, Any]]:
    """Retrieve user profile by ID or the most recently updated profile."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    if user_id:
        cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
    else:
        cursor.execute("SELECT * FROM user_profiles ORDER BY updated_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    profile = dict(row)
    if isinstance(profile["target_countries"], str):
        try:
            profile["target_countries"] = json.loads(profile["target_countries"])
        except json.JSONDecodeError:
            profile["target_countries"] = [profile["target_countries"]]
    return profile


def get_all_user_profiles(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Retrieve all user profiles from SQLite."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_profiles ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()

    profiles = []
    for row in rows:
        p = dict(row)
        if isinstance(p["target_countries"], str):
            try:
                p["target_countries"] = json.loads(p["target_countries"])
            except json.JSONDecodeError:
                p["target_countries"] = [p["target_countries"]]
        profiles.append(p)
    return profiles


def delete_user_profile(user_id: str, db_path: str = DB_PATH) -> bool:
    """Delete a user profile by ID."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user_profiles WHERE id = ?", (user_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted


def save_user_profile(profile_data: Dict[str, Any], db_path: str = DB_PATH) -> None:
    """Save or update the user profile."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    countries_json = json.dumps(profile_data.get("target_countries", ["UK", "Europe"]))
    profile_id = profile_data.get("id")
    if not profile_id:
        clean_name = profile_data.get("name", "user").lower().replace(" ", "_")
        profile_id = f"user_{clean_name}_{int(datetime.now().timestamp())}"

    cursor.execute("""
    INSERT OR REPLACE INTO user_profiles (
        id, name, gpa, ielts_score, toefl_ibt_score, age, target_degree,
        major_field, work_exp_years, publications_count, target_countries, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        profile_id,
        profile_data.get("name", "Pengguna"),
        profile_data.get("gpa", 3.0),
        profile_data.get("ielts_score", 6.5),
        profile_data.get("toefl_ibt_score", 80.0),
        profile_data.get("age", 25),
        profile_data.get("target_degree", "S2"),
        profile_data.get("major_field", "General"),
        profile_data.get("work_exp_years", 0),
        profile_data.get("publications_count", 0),
        countries_json,
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()



def get_all_scholarships(db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Retrieve all scholarships from SQLite."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scholarships ORDER BY name ASC")
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        item = dict(r)
        item["target_degrees"] = json.loads(item["target_degrees"]) if item["target_degrees"] else []
        item["target_countries"] = json.loads(item["target_countries"]) if item["target_countries"] else []
        item["required_documents"] = json.loads(item["required_documents"]) if item["required_documents"] else []
        results.append(item)

    return results
