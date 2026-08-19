import sys
import asyncio
from typing import Dict, List, Any
from rich.console import Console
from modules.scraper.base_scraper import scrape_web_page
from modules.scraper.llm_extractor import extract_scholarships_from_text
from modules.database import get_connection, DB_PATH

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()



def upsert_scholarships(scholarships_list: List[Dict[str, Any]], db_path: str = DB_PATH) -> int:
    """
    Idempotent Ingestion Shield:
    Inserts or updates master scholarship data into SQLite.
    Guarantees user bookmarks, priority flags, and notes in user_scholarship_flags
    are NEVER overwritten or damaged.
    """
    import json
    from modules.database import init_db
    init_db(db_path)

    conn = get_connection(db_path)
    cursor = conn.cursor()


    inserted_count = 0
    for s in scholarships_list:
        s_id = s.get("id", f"scraped_{int(asyncio.get_event_loop().time())}")
        degrees_json = json.dumps(s.get("target_degrees", ["S1", "S2"]))
        countries_json = json.dumps(s.get("target_countries", ["Indonesia"]))
        docs_json = json.dumps(s.get("required_documents", ["Transkrip", "KTP"]))

        cursor.execute("""
        INSERT INTO scholarships (
            id, name, provider, funding_type, target_degrees, target_countries,
            min_gpa, min_ielts, min_toefl_ibt, max_age, min_work_exp_years,
            required_documents, deadline_date, source_url, description
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            provider = excluded.provider,
            funding_type = excluded.funding_type,
            target_degrees = excluded.target_degrees,
            target_countries = excluded.target_countries,
            min_gpa = excluded.min_gpa,
            min_ielts = excluded.min_ielts,
            deadline_date = excluded.deadline_date,
            description = excluded.description,
            updated_at = CURRENT_TIMESTAMP
        """, (
            s_id,
            s.get("name", "Beasiswa Terdeteksi"),
            s.get("provider", "Penyelenggara Web"),
            s.get("funding_type", "Fully Funded"),
            degrees_json,
            countries_json,
            float(s.get("min_gpa", 3.0)),
            float(s.get("min_ielts", 6.0)),
            float(s.get("min_toefl_ibt", 80.0)),
            int(s.get("max_age", 35)),
            int(s.get("min_work_exp_years", 0)),
            docs_json,
            s.get("deadline_date", "2026-12-31"),
            s.get("source_url", ""),
            s.get("description", "Data terdeteksi otomatis oleh scraper.")
        ))
        inserted_count += 1

    conn.commit()
    conn.close()
    return inserted_count


def log_scrape_event(source_name: str, status: str, scraped: int, inserted: int, err_msg: str = "", db_path: str = DB_PATH):
    """Record activity log entry in scrape_logs table."""
    conn = get_connection(db_path)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO scrape_logs (source_name, status, records_scraped, records_inserted, error_message)
    VALUES (?, ?, ?, ?, ?)
    """, (source_name, status, scraped, inserted, err_msg))
    conn.commit()
    conn.close()


async def run_scraper_pipeline(url: str) -> Dict[str, Any]:
    """
    Run full End-to-End Scraper Ingestion Pipeline:
    1. Robots.txt politeness check
    2. Playwright DOM scraping
    3. LLM/Regex JSON extraction
    4. Idempotent SQLite upsert
    5. Audit logging in scrape_logs
    """
    console.print(f"\n[bold cyan]🌐 Menjalankan Pipeline Scraper untuk URL: {url}[/bold cyan]")
    
    scrape_res = await scrape_web_page(url)
    if not scrape_res["success"]:
        log_scrape_event(url, "FAILED", 0, 0, scrape_res["error"])
        return {"status": "FAILED", "inserted": 0, "error": scrape_res["error"]}

    extracted = extract_scholarships_from_text(scrape_res["inner_text"], source_url=url)
    if not extracted:
        log_scrape_event(url, "EMPTY", 0, 0, "Tidak ada data beasiswa yang terdeteksi.")
        return {"status": "EMPTY", "inserted": 0, "error": "No items extracted"}

    inserted = upsert_scholarships(extracted)
    log_scrape_event(url, "SUCCESS", len(extracted), inserted)

    console.print(f"[bold green]✅ Ingestion Pipeline Berhasil: {inserted} Data Beasiswa Terupdate di Database Master![/bold green]")
    return {"status": "SUCCESS", "inserted": inserted, "items": extracted}


def run_pipeline_sync(url: str) -> Dict[str, Any]:
    """Synchronous entry point for TUI integration."""
    return asyncio.run(run_scraper_pipeline(url))
