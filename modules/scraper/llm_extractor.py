import os
import json
import re
from typing import Dict, List, Any
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def extract_scholarships_from_text(page_text: str, source_url: str = "") -> List[Dict[str, Any]]:
    """
    Extract structured scholarship objects from web page text.
    Uses DeepSeek API / Gemini API if configured,
    otherwise falls back to rule-based regex pattern extraction.
    """
    from modules.ai_client import generate_llm_text

    sys_inst = "Ekstrak data beasiswa dari teks web page menjadi format JSON array murni."
    prompt = (
        "Ekstrak data beasiswa dari teks berikut menjadi format JSON array murni.\n"
        "Setiap elemen harus memiliki atribut:\n"
        "- id: slug_unik (huruf kecil, tanpa spasi)\n"
        "- name: Nama Lengkap Beasiswa\n"
        "- provider: Penyelenggara / Yayasan / Kementerian\n"
        "- funding_type: Fully Funded atau Partial Funded\n"
        "- target_degrees: list string contoh ['S1', 'S2']\n"
        "- target_countries: list string contoh ['Indonesia', 'Japan']\n"
        "- min_gpa: float angka (default 3.0)\n"
        "- min_ielts: float angka (default 6.0)\n"
        "- deadline_date: YYYY-MM-DD\n"
        "- description: ringkasan singkat\n\n"
        f"Teks Web Page:\n{page_text[:10000]}"
    )

    res_text = generate_llm_text(prompt, system_instruction=sys_inst)
    if res_text:
        try:
            raw_text = res_text.strip()
            if raw_text.startswith("```"):
                raw_text = re.sub(r"^```(json)?\n?", "", raw_text)
                raw_text = re.sub(r"\n?```$", "", raw_text)

            parsed = json.loads(raw_text)
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict):
                return [parsed]
        except Exception as err:
            console.print(f"[dim yellow]ℹ️ LLM JSON parser encounter: {err}. Menggunakan fallback regex parser.[/dim yellow]")

    # Structured Regex Fallback Parser
    return fallback_regex_extractor(page_text, source_url)



def fallback_regex_extractor(page_text: str, source_url: str = "") -> List[Dict[str, Any]]:
    """Rule-based regex fallback extractor for scholarship data."""
    results = []

    # Detect common scholarship keywords
    lines = page_text.split("\n")
    title_matches = [line.strip() for line in lines if "beasiswa" in line.lower() or "scholarship" in line.lower()]

    if title_matches:
        for idx, title in enumerate(title_matches[:3]):
            clean_title = re.sub(r"[^\w\s-]", "", title)[:60].strip()
            if not clean_title or len(clean_title) < 5:
                continue
                
            slug_id = clean_title.lower().replace(" ", "_")
            results.append({
                "id": f"scraped_{slug_id}_{idx+1}",
                "name": clean_title,
                "provider": "Penyelenggara Terdeteksi",
                "funding_type": "Fully Funded" if "full" in page_text.lower() else "Partial Funded",
                "target_degrees": ["S1", "S2"] if "s1" in page_text.lower() else ["S2"],
                "target_countries": ["Indonesia", "International"],
                "min_gpa": 3.0,
                "min_ielts": 6.0,
                "min_toefl_ibt": 80.0,
                "max_age": 35,
                "min_work_exp_years": 0,
                "required_documents": ["Form Aplikasi", "Transkrip Nilai", "KTP / Paspor"],
                "deadline_date": "2026-12-31",
                "source_url": source_url,
                "description": f"Data beasiswa terdeteksi dari hasil scraping {source_url or 'portal web'}."
            })

    return results
