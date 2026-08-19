import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()


def generate_rule_based_advice(user: Dict[str, Any], match_results: List[Dict[str, Any]]) -> List[str]:
    """
    Generate clean, concise, and easily understandable AI Gap Analysis advice.
    """
    advice_list = []
    
    if not match_results:
        return ["Belum ada data beasiswa."]

    top_match = match_results[0]
    ielts = user.get("ielts_score", 6.5)
    exp = user.get("work_exp_years", 0)
    pubs = user.get("publications_count", 0)

    # 1. Target Top Match
    advice_list.append(
        f"🎯 [bold yellow]Target Utama[/]: {top_match['scholarship_name']} ([green]{top_match['fit_score']}% Match[/])"
    )

    # 2. IELTS Gap Advice
    if ielts < 7.0:
        boosted = min(95.0, top_match['fit_score'] + 10.0)
        advice_list.append(
            f"📈 [bold cyan]IELTS ({ielts})[/]: Tingkatkan ke 7.0+ ➔ Peluang naik ke ~[bold green]{boosted:.1f}%[/]"
        )

    # 3. Research Publication Gap Advice
    if pubs == 0:
        advice_list.append(
            "📝 [bold cyan]Publikasi[/]: Tambahkan 1 paper/jurnal riset untuk memperkuat aplikasi."
        )

    # 4. Work Experience Gap Advice
    if exp < 2:
        advice_list.append(
            f"💼 [bold cyan]Pengalaman ({exp} th)[/]: Perbanyak bukti leadership & kegiatan sosial."
        )

    # 5. Requirement Warning
    missing_items = []
    for m in match_results:
        if m.get("missing_reqs"):
            missing_items.extend(m["missing_reqs"])

    if missing_items:
        unique_missing = list(set(missing_items))[:2]
        advice_list.append(
            f"⚠️ [bold red]Catatan Syarat[/]: {'; '.join(unique_missing)}"
        )

    return advice_list



def get_ai_gap_analysis(user: Dict[str, Any], match_results: List[Dict[str, Any]]) -> List[str]:
    """
    Generate gap analysis using Gemini Flash API if GEMINI_API_KEY is available,
    otherwise fallback seamlessly to the built-in advisor engine.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "your_google_gemini_api_key_here":
        return generate_rule_based_advice(user, match_results)

    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Kamu adalah pakar konsultan beasiswa internasional (AI Gap Advisor).
        Berikut adalah data profil pendaftar:
        - Nama: {user.get('name')}
        - IPK: {user.get('gpa')}
        - IELTS: {user.get('ielts_score')}
        - Usia: {user.get('age')}
        - Jenjang Target: {user.get('target_degree')}
        - Pengalaman Kerja: {user.get('work_exp_years')} tahun
        - Publikasi Riset: {user.get('publications_count')}
        - Negara Target: {', '.join(user.get('target_countries', []))}

        Berikut adalah top 3 hasil pencocokan beasiswa:
        {match_results[:3]}

        Berikan 4-5 poin ringkas, konkret, dan motivatif (dalam bahasa Indonesia) mengenai:
        1. Evaluasi singkat posisi peluang beasiswa pendaftar.
        2. Langkah konkret peningkatan skor (IELTS / Riset / Portfolio).
        3. Strategi pemilihan beasiswa (Safety, Target, Reach).

        Gunakan format bullet list dengan emoji.
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response and response.text:
            lines = [line.strip() for line in response.text.split("\n") if line.strip()]
            return lines

    except Exception:
        pass

    return generate_rule_based_advice(user, match_results)
