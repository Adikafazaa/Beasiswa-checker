import sys
import time

# Reconfigure Windows stdout encoding for UTF-8 emoji support and maximize console window
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE (3)
    except Exception:
        pass


from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt


from modules.database import (
    init_db,
    get_user_profile,
    save_user_profile,
    get_all_scholarships
)
from modules.matching_engine import run_full_matching
from modules.ai_advisor import get_ai_gap_analysis
from cli.views import (
    clear_screen,
    render_banner,
    render_user_profile_card,
    render_matching_table,
    render_terminal_chart,
    render_ai_advice_panel,
    render_scholarship_list_table,
    render_wireframe_dashboard,
    render_back_button_prompt
)
from cli.profile_cli import prompt_user_profile_inputs, manage_user_profiles

from cli.menus import handle_dashboard_navigation, read_key

console = Console()


def run_analytics_dashboard(user_profile, scholarships):
    """Render full matching analytics dashboard matching exact wireframe layout."""
    clear_screen()
    
    with console.status("[bold green]Menghitung kalkulasi skor kecocokan beasiswa...[/bold green]"):
        match_results = run_full_matching(user_profile, scholarships)
        advice_list = get_ai_gap_analysis(user_profile, match_results)
        time.sleep(0.3)

    render_wireframe_dashboard(user_profile, match_results, advice_list)


def main():
    """Main application entry point."""
    clear_screen()
    render_banner()
    console.print("[bold green]Inisialisasi Database & System Core...[/bold green]")
    init_db()
    time.sleep(0.3)

    user_profile = get_user_profile()
    scholarships = get_all_scholarships()

    selected_index = 0
    current_action = "1"
    current_page = 1

    while True:
        clear_screen()
        match_results = run_full_matching(user_profile, scholarships)
        advice_list = get_ai_gap_analysis(user_profile, match_results)

        if current_action == "1":
            # 1. Dashboard Analytics Layout with highlighted Navigasi pointer & paginated table
            render_wireframe_dashboard(
                user_profile,
                match_results,
                advice_list,
                selected_index=selected_index,
                page=current_page,
                page_size=8
            )





        elif current_action == "2":
            # 2. Edit & Kelola Profil Pendaftar (Multi-User Profile Manager)
            render_banner()
            render_user_profile_card(user_profile)
            user_profile = manage_user_profiles(user_profile)
            render_back_button_prompt("Kembali ke Dashboard Analytics")
            read_key()
            current_action = "1"
            selected_index = 0
            continue


        elif current_action == "3":
            # 3. Cari & Filter Database Beasiswa
            render_banner()
            
            try:
                from InquirerPy import inquirer
                filter_choice = inquirer.select(
                    message="Pilih Metode Filter / Pencarian Beasiswa:",
                    choices=[
                        "[0] 📋 Tampilkan Semua Beasiswa",
                        "[1] 🎓 Filter Berdasarkan Jenjang (S1 / S2 / S3)",
                        "[2] 💰 Filter Berdasarkan Pendanaan (Fully / Partial)",
                        "[3] 🔍 Cari Berdasarkan Kata Kunci (Nama / Penyelenggara / Negara)"
                    ],
                    default="[0] 📋 Tampilkan Semua Beasiswa"
                ).execute()
            except Exception:
                filter_choice = "[0]"

            filtered = scholarships
            filter_label = "Semua Beasiswa"

            if "[1]" in filter_choice:
                deg = inquirer.select(message="Pilih Target Jenjang:", choices=["S1", "S2", "S3"]).execute()
                filtered = [s for s in scholarships if deg in s.get("target_degrees", [])]
                filter_label = f"Jenjang {deg}"

            elif "[2]" in filter_choice:
                fund = inquirer.select(message="Pilih Jenis Pendanaan:", choices=["Fully Funded", "Partial Funded"]).execute()
                filtered = [s for s in scholarships if s.get("funding_type") == fund]
                filter_label = f"Pendanaan {fund}"

            elif "[3]" in filter_choice:
                kw = inquirer.text(message="Masukkan kata kunci pencarian (Nama/Negara/Penyelenggara):").execute().strip().lower()
                if kw:
                    filtered = [
                        s for s in scholarships 
                        if kw in s["name"].lower() or kw in s["provider"].lower() or any(kw in c.lower() for c in s.get("target_countries", []))
                    ]
                    filter_label = f"Kata Kunci '{kw}'"

            render_scholarship_list_table(filtered, filter_info=filter_label)
            render_back_button_prompt("Kembali ke Dashboard Utama")
            read_key()
            current_action = "1"
            selected_index = 0
            continue


        elif current_action == "4":
            # 4. Scraper Beasiswa
            render_banner()
            scraper_info = (
                "[bold cyan]🌐 Playwright Web Scraper & Auth Session Launcher[/bold cyan]\n\n"
                "Modul ini memungkinkan Anda membuka sesi browser Chromium untuk:\n"
                "• Login 1x secara manual ke portal beasiswa / jejaring sosial.\n"
                "• Menyimpan status cookies ke [yellow]data/sessions/session.json[/yellow].\n"
                "• Menjalankan scraper otomatis & ekstraksi teks via Gemini LLM.\n\n"
                "[dim]Status: Scraper script terintegrasi di folder scraper/.[/dim]"
            )
            console.print(Panel(scraper_info, title="Scraper Module", border_style="cyan"))
            render_back_button_prompt("Kembali ke Dashboard Utama")
            read_key()
            current_action = "1"
            selected_index = 0
            continue

        elif current_action == "5":
            # 5. AI Gap Analysis Advisor
            render_banner()
            render_user_profile_card(user_profile)
            render_ai_advice_panel(advice_list)
            render_back_button_prompt("Kembali ke Dashboard Utama")
            read_key()
            current_action = "1"
            selected_index = 0
            continue

        # Read native keypress (Up/Down Arrow keys move pointer inside Navigasi box, Enter selects, N/P page)
        event_type, new_idx, key_code = handle_dashboard_navigation(selected_index)

        if event_type == "PAGE_NEXT":
            current_page += 1
            current_action = "1"
            continue

        elif event_type == "PAGE_PREV":
            current_page = max(1, current_page - 1)
            current_action = "1"
            continue

        if key_code == "0" and event_type == "SELECT":
            clear_screen()
            console.print(Panel(
                "[bold cyan]Terima kasih telah menggunakan Beasiswa Checker Analytics![/bold cyan]\n"
                "[yellow]Semoga sukses mendapatkan beasiswa impian Anda! 🎓✨[/yellow]",
                border_style="green"
            ))
            sys.exit(0)

        selected_index = new_idx
        if event_type == "SELECT":
            current_action = key_code
        else:
            current_action = "1"






if __name__ == "__main__":
    main()
