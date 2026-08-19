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
        f"• [bold yellow][TARGET UTAMA][/bold yellow]: [bold white]{top_match['scholarship_name']}[/bold white] ([bold green]{top_match['fit_score']:.1f}% Match[/bold green])"
    )

    # 2. IELTS Gap Advice
    if ielts < 7.0:
        boosted = min(95.0, top_match['fit_score'] + 10.0)
        advice_list.append(
            f"• [bold cyan][IELTS ({ielts})][/bold cyan]: Tingkatkan ke 7.0+ ➔ Peluang naik ke ~[bold green]{boosted:.1f}%[/bold green]"
        )

    # 3. Research Publication Gap Advice
    if pubs == 0:
        advice_list.append(
            "• [bold cyan][PUBLIKASI][/bold cyan]: Tambahkan 1 paper/jurnal riset untuk memperkuat aplikasi."
        )

    # 4. Work Experience Gap Advice
    if exp < 2:
        advice_list.append(
            f"• [bold cyan][PENGALAMAN ({exp} th)][/bold cyan]: Perbanyak bukti leadership & kegiatan sosial."
        )

    # 5. Requirement Warning
    missing_items = []
    for m in match_results:
        if m.get("missing_reqs"):
            missing_items.extend(m["missing_reqs"])

    if missing_items:
        unique_missing = list(set(missing_items))[:2]
        advice_list.append(
            f"• [bold red][CATATAN SYARAT][/bold red]: {'; '.join(unique_missing)}"
        )



    return advice_list



def get_ai_gap_analysis(user: Dict[str, Any], match_results: List[Dict[str, Any]]) -> List[str]:
    """
    Generate gap analysis using DeepSeek API or Gemini API,
    otherwise fallback seamlessly to the built-in rule-based advisor engine.
    """
    from modules.ai_client import generate_llm_text

    system_instruction = (
        "Kamu adalah pakar konsultan beasiswa internasional (AI Gap Advisor). "
        "Gunakan format Markdown standard dengan bullet points ('-') dan teks bold. "
        "DILARANG keras menggunakan emoticon/emoji mobile (seperti 🎯, 📈, 🗣️, 💡). "
        "Gunakan penanda teks TUI seperti [POSISI], [PORTOFOLIO], [IELTS], [STRATEGI]."
    )
    prompt = f"""
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

    Berikan 4-5 poin ringkas, konkret, dan motivatif (dalam bahasa Indonesia):
    - [POSISI]: Evaluasi singkat posisi peluang beasiswa pendaftar.
    - [PORTOFOLIO]: Langkah konkret peningkatan skor (IELTS / Riset / Portfolio).
    - [STRATEGI]: Strategi pemilihan beasiswa (Safety, Target, Reach).
    - [LEADERSHIP]: Catatan usia dan pengalaman.

    Format output dalam Markdown standard dengan bullet list '-'. JANGAN GUNAKAN EMOJI.
    """

    res_text = generate_llm_text(prompt, system_instruction=system_instruction)
    if res_text:
        lines = [line.strip() for line in res_text.split("\n") if line.strip()]
        if lines:
            return lines

    return generate_rule_based_advice(user, match_results)


