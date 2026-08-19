import os
import sys
from typing import Dict, List, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.style import Style
import plotext as plt

# Reconfigure Windows stdout encoding for UTF-8 emoji & VT100 ANSI terminal support
if sys.platform == "win32":
    try:
        os.system('')  # Enable VT100 escape sequence processing in Windows CMD/PowerShell
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()


def clear_screen():
    """Clear terminal screen cleanly using Rich console without subshell VT artifacts."""
    try:
        console.clear()
    except Exception:
        os.system('cls' if os.name == 'nt' else 'clear')


def soft_clear_screen():
    """Reposition cursor to home (top-left) to enable smooth zero-flicker screen updates."""
    try:
        sys.stdout.write("\033[H")
        sys.stdout.flush()
    except Exception:
        console.clear()




def render_banner():
    """Render application header banner using Rich."""
    banner_text = Text()
    banner_text.append("BEASISWA CHECKER ANALYTICS\n", style="bold cyan")
    banner_text.append("Platform Cerdas Analitik, Pencocokan Beasiswa & AI Gap Advisor (Terminal Edition)", style="dim white")
    
    panel = Panel(
        Align.center(banner_text),
        border_style="bright_blue",
        padding=(0, 2)
    )
    console.print(panel)


def render_user_profile_card(user: Dict[str, Any]):
    """Render current user profile overview in a styled panel."""
    countries_str = ", ".join(user.get("target_countries", []))
    
    info_text = (
        f"[bold yellow]Nama:[/] {user.get('name', 'N/A')}  |  "
        f"[bold yellow]Jenjang:[/] {user.get('target_degree', 'N/A')}  |  "
        f"[bold yellow]Jurusan:[/] {user.get('major_field', 'N/A')}  |  "
        f"[bold yellow]IPK:[/] [green]{user.get('gpa', 0.0):.2f}[/]  |  "
        f"[bold yellow]IELTS:[/] [green]{user.get('ielts_score', 0.0)}[/]  |  "
        f"[bold yellow]Pengalaman:[/] {user.get('work_exp_years', 0)} Th  |  "
        f"[bold yellow]Target:[/] {countries_str}"
    )

    panel = Panel(
        Align.center(info_text),
        title="[bold green]Profil Pendaftar Saat Ini[/]",
        border_style="green",
        padding=(0, 1)
    )
    console.print(panel)


def make_progress_bar(score: float) -> str:
    """Create ASCII progress bar for match score percentage."""
    filled = int(score / 10)
    empty = 10 - filled
    return f"[{'=' * filled}{'.' * empty}]"


def render_matching_scores_table(match_results: List[Dict[str, Any]], top_n: int = 10):
    """Render top matching scholarships table using Rich."""
    table = Table(
        title="[bold yellow]Matriks Analisis & Skor Kecocokan Beasiswa[/]",
        header_style="bold cyan",
        border_style="bright_black"
    )

    table.add_column("Rank", justify="center", style="bold white")
    table.add_column("Beasiswa", style="bold yellow")
    table.add_column("Penyelenggara", style="dim white")
    table.add_column("Jenjang", justify="center")
    table.add_column("Pendanaan", justify="center")
    table.add_column("Score (%)", justify="right", style="bold green")
    table.add_column("Kategori Fit", justify="center")
    table.add_column("Progress Bar", justify="center")

    for idx, res in enumerate(match_results[:top_n], start=1):
        cat = res["fit_category"]
        if cat == "Safety":
            cat_styled = "[bold green]Safety[/]"
        elif cat == "Target":
            cat_styled = "[bold yellow]Target[/]"
        else:
            cat_styled = "[bold red]Reach[/]"

        table.add_row(
            str(idx),
            res["scholarship_name"],
            res.get("provider", "N/A"),
            ", ".join(res.get("target_degrees", [])),
            res.get("funding_type", "Fully Funded"),
            f"{res['fit_score']:.1f}%",
            cat_styled,
            make_progress_bar(res["fit_score"])
        )

    console.print(table)


render_matching_table = render_matching_scores_table



def render_plotext_analytics_chart(match_results: List[Dict[str, Any]], top_n: int = 6):
    """Render horizontal bar chart inside terminal using plotext."""
    if not match_results:
        return

    top_matches = match_results[:top_n]
    names = [m["scholarship_name"][:18] for m in reversed(top_matches)]
    scores = [m["fit_score"] for m in reversed(top_matches)]

    plt.clear_figure()
    plt.bar(names, scores, orientation="horizontal", color="cyan")
    plt.title("Analisis Visualisasi Top Match Scores (%)")
    plt.theme("dark")
    plt.plotsize(60, 10)
    plt.show()
    print()


render_terminal_chart = render_plotext_analytics_chart



def render_ai_advice_panel(advice_list: Any):
    """Render AI Gap Analysis advice in a Rich Panel with vibrant colors."""
    from rich.console import Group
    from rich.markdown import Markdown

    if isinstance(advice_list, list):
        advice_lines = advice_list
    else:
        advice_lines = [l.strip() for l in str(advice_list).split("\n") if l.strip()]

    renderables = []
    for line in advice_lines:
        try:
            if "[" in line and "]" in line:
                renderables.append(Text.from_markup(line))
            else:
                renderables.append(Text(line, style="white"))
        except Exception:
            renderables.append(Text(line, style="white"))

    panel = Panel(
        Group(*renderables),
        title="[bold yellow]AI Gap Analysis & Rekomendasi Action Plan[/bold yellow]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(panel)


def render_expanded_ai_view(user: Dict[str, Any], offline_advice: List[str]):
    """Render full expanded dual-perspective AI Analysis screen (Built-in Rule Engine + DeepSeek AI Report)."""
    from rich.console import Group

    # 1. Built-in Rule-Based Panel
    rule_renderables = []
    for line in offline_advice:
        try:
            if "[" in line and "]" in line:
                rule_renderables.append(Text.from_markup(line))
            else:
                rule_renderables.append(Text(line, style="white"))
        except Exception:
            rule_renderables.append(Text(line, style="white"))

    rule_panel = Panel(
        Group(*rule_renderables),
        title="[bold cyan]Built-in Quick Action Plan (0-Token Rule Engine)[/bold cyan]",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(rule_panel)
    print()

    # 2. DeepSeek AI Analysis Panel
    ai_text = user.get("last_ai_analysis", "").strip()
    if ai_text:
        ai_lines = [l.strip() for l in ai_text.split("\n") if l.strip()]
        ai_renderables = []
        for line in ai_lines:
            try:
                if "[" in line and "]" in line:
                    ai_renderables.append(Text.from_markup(line))
                else:
                    ai_renderables.append(Text(line, style="white"))
            except Exception:
                ai_renderables.append(Text(line, style="white"))

        ai_panel = Panel(
            Group(*ai_renderables),
            title="[bold yellow]DeepSeek AI Comprehensive Gap Analysis Report[/bold yellow]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print(ai_panel)
    else:
        info_panel = Panel(
            "[yellow]DeepSeek AI Analysis belum dipanggil untuk profil ini.\n"
            "Silakan pilih menu [5] Fitur AI & Scraper -> [1] Generasi Analisis AI DeepSeek untuk me-generate report AI.[/yellow]",
            title="[bold yellow]DeepSeek AI Comprehensive Report[/bold yellow]",
            border_style="dim yellow",
            padding=(1, 2)
        )
        console.print(info_panel)


def render_scholarship_list_table(scholarships: List[Dict[str, Any]], filter_info: str = "Semua Beasiswa", page: int = 1, page_size: int = 8):

    """Render clean, paginated panelled search & filter database table with row index numbers."""
    import math
    from rich.console import Group

    total_items = len(scholarships)
    total_pages = max(1, math.ceil(total_items / page_size)) if total_items > 0 else 1
    current_page = max(1, min(page, total_pages))
    
    start_idx = (current_page - 1) * page_size
    end_idx = min(start_idx + page_size, total_items)
    page_items = scholarships[start_idx:end_idx] if total_items > 0 else []

    table = Table(
        header_style="bold magenta",
        border_style="bright_black",
        show_lines=True,
        expand=True
    )

    table.add_column("No", style="bold cyan", justify="center", width=4)
    table.add_column("Nama Beasiswa", style="bold yellow", ratio=4)
    table.add_column("Penyelenggara", style="cyan", ratio=3)
    table.add_column("Pendanaan", style="bold green", justify="center", ratio=2)
    table.add_column("Jenjang", justify="center", ratio=2)
    table.add_column("Min IPK", justify="center", ratio=1)
    table.add_column("Min IELTS", justify="center", ratio=1)
    table.add_column("Deadline", justify="center", ratio=2)

    for idx, s in enumerate(page_items, start=1):
        table.add_row(
            f"[{idx}]",
            f"[bold yellow]{s['name']}[/]",
            s["provider"],
            f"[bold green]{s['funding_type']}[/]",
            ", ".join(s["target_degrees"]),
            f"{s['min_gpa']:.2f}",
            f"{s['min_ielts']}",
            s["deadline_date"]
        )

    item_range_str = f"{start_idx + 1}-{end_idx}" if total_items > 0 else "0"
    pagination_str = (
        f"  [bold yellow][P] ◀ Hal. Sebelum[/bold yellow]   │   "
        f"[bold white]Halaman {current_page} dari {total_pages}[/bold white] [dim](Data {item_range_str} dari {total_items} Beasiswa)[/dim]   │   "
        f"[bold yellow]Hal. Berikutnya ▶ [N][/bold yellow]  "
    )

    panel_group = Group(
        table,
        Align.center(pagination_str)
    )

    panel = Panel(
        panel_group,
        title=f"[bold cyan]Database Master Beasiswa ({len(scholarships)} Ditemukan - Filter: {filter_info})[/bold cyan]",
        border_style="cyan"
    )
    console.print(panel)
    return current_page, total_pages, page_items



def render_scholarship_detail_card(s: Dict[str, Any], is_bookmarked: bool = False):
    """Render comprehensive detail card for a selected scholarship entry using TUI symbols."""
    bm_badge = "[bold yellow][BOOKMARKED][/bold yellow]" if is_bookmarked else "[dim][NO BOOKMARK][/dim]"
    degrees = ", ".join(s.get("target_degrees", [])) or "Semua"
    countries = ", ".join(s.get("target_countries", [])) or "Global"
    docs = "\n  - " + "\n  - ".join(s.get("required_documents", [])) if s.get("required_documents") else " Tidak ada rincian"

    detail_text = (
        f"[bold white]Penyelenggara[/bold white] : [bold cyan]{s.get('provider')}[/bold cyan]\n"
        f"[bold white]Jenis Pendanaan[/bold white]: [bold green]{s.get('funding_type')}[/bold green] | Status: {bm_badge}\n"
        f"[bold white]Target Jenjang [/bold white]: {degrees}\n"
        f"[bold white]Negara Target  [/bold white]: {countries}\n\n"
        f"[bold yellow]Syarat Minimal Akademik & Bahasa:[/bold yellow]\n"
        f"  - IPK Minimal     : [cyan]{s.get('min_gpa', 0.0):.2f}[/cyan]\n"
        f"  - IELTS Minimal   : [cyan]{s.get('min_ielts', 0.0)}[/cyan] | TOEFL iBT Minimal: [cyan]{s.get('min_toefl_ibt', 0.0)}[/cyan]\n"
        f"  - Batas Usia      : [cyan]{s.get('max_age', 99)} Tahun[/cyan] | Pengalaman Kerja: [cyan]{s.get('min_work_exp_years', 0)} Tahun[/cyan]\n\n"
        f"[bold yellow]Dokumen Persyaratan:[/bold yellow]{docs}\n\n"
        f"[bold white]Deadline Pendaftaran[/bold white]: [bold red]{s.get('deadline_date', 'TBA')}[/bold red]\n"
        f"[bold white]Portal Resmi        [/bold white]: [underline blue]{s.get('source_url', '-')}[/underline blue]\n\n"
        f"[italic white]Deskripsi:[/italic white]\n{s.get('description', '-')}"
    )

    panel = Panel(
        detail_text,
        title=f"[bold yellow]Detail Beasiswa: {s.get('name')}[/bold yellow]",
        border_style="yellow"
    )
    console.print(panel)



def render_bookmarked_scholarships_table(bookmarks: List[Dict[str, Any]], user_name: str = "Pendaftar"):
    """Render table of user's saved bookmarks, application status, priority, and personal notes."""
    table = Table(
        header_style="bold yellow",
        border_style="bright_black",
        show_lines=True,
        expand=True
    )

    table.add_column("Beasiswa", style="bold yellow", ratio=4)
    table.add_column("Penyelenggara", style="cyan", ratio=3)
    table.add_column("Status Aplikasi", style="bold green", justify="center", ratio=2)
    table.add_column("Prioritas", style="bold magenta", justify="center", ratio=2)
    table.add_column("Catatan Pribadi", style="italic white", ratio=4)

    if not bookmarks:
        table.add_row(
            "[dim]Belum ada beasiswa yang ditandai (Bookmark)[/dim]",
            "-", "-", "-", "-"
        )
    else:
        for b in bookmarks:
            prio = b.get("priority", "NONE")
            prio_styled = f"[magenta]{prio}[/]" if prio != "NONE" else "[dim]-[/dim]"
            stat = b.get("app_status", "SAVED")
            notes = b.get("user_notes", "") or "[dim]Belum ada catatan[/dim]"
            
            table.add_row(
                f"[bold white]{b['name']}[/]",
                b["provider"],
                f"[bold green][{stat}][/bold green]",
                prio_styled,
                notes
            )

    panel = Panel(
        table,
        title=f"[bold yellow]Daftar Beasiswa Tersimpan & Catatan (Profil: {user_name})[/bold yellow]",
        border_style="yellow"
    )
    console.print(panel)




def create_user_info_panel(user: Dict[str, Any]) -> Panel:
    """Create User-Info panel matching exact wireframe spec."""
    countries_str = ", ".join(user.get("target_countries", []))
    lines = [
        f"[bold white]Nama       :[/] {user.get('name', 'Adika')}",
        f"[bold white]Jenjang    :[/] {user.get('target_degree', 'S2')}",
        f"[bold white]Target     :[/] {countries_str}",
        f"[bold white]IPK        :[/] [bold green]{user.get('gpa', 0.0):.2f}[/]",
        f"[bold white]IELTS      :[/] [bold green]{user.get('ielts_score', 0.0)}[/]",
        f"[bold white]Pengalaman :[/] {user.get('work_exp_years', 0)} Th"
    ]
    return Panel(
        "\n".join(lines),
        title="[bold bright_white]Informasi Pendaftar[/]",
        border_style="bright_blue",
        padding=(1, 2)
    )


def create_analysis_action_panel(advice_list: List[str]) -> Panel:
    """Create Analysis-&-Action panel matching exact wireframe spec."""
    content = "\n".join(advice_list)
    return Panel(
        content,
        title="[bold yellow]Analisis & Rekomendasi AI[/]",
        border_style="yellow",
        padding=(1, 2)
    )


from rich.layout import Layout

import math
from rich.console import Group

def render_wireframe_dashboard(
    user: Dict[str, Any],
    match_results: List[Dict[str, Any]],
    advice_list: List[str],
    selected_index: int = 0,
    page: int = 1,
    page_size: int = 8
):
    """
    Render Paginated Dashboard layout matching exact wireframe spec:
    - Top Header Bar
    - Middle Section: Paginated Main Table (Left, 8 items per page) + Informational Panels (Right)
    - Bottom Section: Horizontal Navigation Bar with pointer highlighting
    """
    layout = Layout()

    # Split into Top Header, Middle Main Section, Bottom Navigation Bar
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="middle", ratio=1),
        Layout(name="bottom_nav", size=3)
    )

    # Middle Section: Left Main Table Area (Wider, 75%) + Right Sidebar (Tightened, 25%)
    layout["middle"].split_row(
        Layout(name="table_area", ratio=3),
        Layout(name="right_sidebar", ratio=1)
    )

    # Right Sidebar: User-Info (top) + Analysis-&-Action (bottom)
    layout["middle"]["right_sidebar"].split_column(
        Layout(name="user_info", size=9),
        Layout(name="analysis_action", ratio=1)
    )

    # 1. Top Header Content
    header_text = Text("🎓 SCHOLARSHIP ANALYTICS & MATCHING DASHBOARD", style="bold cyan")
    layout["header"].update(
        Panel(Align.center(header_text), border_style="bright_blue")
    )

    # 2. Paginated Table Area Content (Capped to 8 items per page)
    console_h = console.height if console and console.height else 32
    avail_table_h = max(9, console_h - 15)
    calculated_rows = min(8, max(3, avail_table_h // 3))
    effective_page_size = 8

    total_items = len(match_results)
    total_pages = max(1, math.ceil(total_items / effective_page_size)) if total_items > 0 else 1
    current_page = max(1, min(page, total_pages))
    
    start_idx = (current_page - 1) * effective_page_size
    end_idx = min(start_idx + effective_page_size, total_items)
    page_items = match_results[start_idx:end_idx] if total_items > 0 else []

    table = Table(
        expand=True,
        border_style="bright_black",
        header_style="bold magenta",
        show_lines=True
    )
    table.add_column("Nama Beasiswa", style="bold white", ratio=4)
    table.add_column("Penyelenggara", style="cyan", ratio=4)
    table.add_column("Pendanaan", style="bold green", justify="center", ratio=2)
    table.add_column("Match (%)", justify="center", ratio=2)
    table.add_column("Kategori", justify="center", ratio=2)
    table.add_column("Status Syarat", justify="center", ratio=3)

    for res in page_items:
        cat = res["category"]
        if cat == "Safety":
            score_styled = f"[bold green]{res['fit_score']}%[/]"
            cat_styled = "[green]🟢 Safety[/]"
        elif cat == "Target":
            score_styled = f"[bold yellow]{res['fit_score']}%[/]"
            cat_styled = "[yellow]🟡 Target[/]"
        else:
            score_styled = f"[bold red]{res['fit_score']}%[/]"
            cat_styled = "[red]🔴 Reach[/]"

        funding = res.get("funding_type", "Fully Funded")

        table.add_row(
            res["scholarship_name"],
            res.get("provider", "N/A"),
            f"[bold green]{funding}[/]",
            score_styled,
            cat_styled,
            res["status_label"]
        )

    # Wireframe pagination footer string anchored with breathing space inside panel
    item_range_str = f"{start_idx + 1}-{end_idx}" if total_items > 0 else "0"
    pagination_str = (
        f"  [bold yellow][P] ◀ Hal. Sebelum[/bold yellow]   │   "
        f"[bold white]Halaman {current_page} dari {total_pages}[/bold white] [dim](Data {item_range_str} dari {total_items} Beasiswa)[/dim]   │   "
        f"[bold yellow]Hal. Berikutnya ▶ [N][/bold yellow]  "
    )

    rendered_rows = len(page_items)
    missing_rows = max(0, calculated_rows - rendered_rows)
    filler_text = "\n" * (missing_rows * 2) if missing_rows > 0 else ""

    table_group = Group(
        table,
        Text(filler_text),
        Align.center(pagination_str)
    )

    layout["middle"]["table_area"].update(
        Panel(table_group, title=f"[bold cyan]Matriks Analisis Beasiswa (Halaman {current_page}/{total_pages})[/bold cyan]", border_style="cyan")
    )

    # 3. User-Info Content
    countries_str = ", ".join(user.get("target_countries", []))
    user_info_lines = (
        f"Nama       : {user.get('name', 'Adika')}\n"
        f"Jenjang    : {user.get('target_degree', 'S2')}\n"
        f"Target     : {countries_str}\n"
        f"IPK        : {user.get('gpa', 0.0):.2f}\n"
        f"IELTS      : {user.get('ielts_score', 0.0)}\n"
        f"Pengalaman : {user.get('work_exp_years', 0)} Th"
    )
    layout["middle"]["right_sidebar"]["user_info"].update(
        Panel(user_info_lines, title="Informasi Pendaftar", border_style="white")
    )

    # 4. Analysis-&-Action Content
    if user.get("last_ai_analysis"):
        raw_advice = user.get("last_ai_analysis")
    else:
        raw_advice = advice_list

    if isinstance(raw_advice, str):
        advice_lines = [l.strip() for l in raw_advice.split("\n") if l.strip()]
    else:
        advice_lines = raw_advice

    # Cap lines at max 7 to fit nicely inside terminal height
    fitted_lines = advice_lines[:7]
    renderables = []
    for line in fitted_lines:
        try:
            if "[" in line and "]" in line:
                renderables.append(Text.from_markup(line))
            else:
                renderables.append(Text(line, style="white"))
        except Exception:
            renderables.append(Text(line, style="white"))

    renderables.append(Text("\n[Tekan E] Perluas & Baca Dual AI Report", style="dim yellow"))

    layout["middle"]["right_sidebar"]["analysis_action"].update(
        Panel(
            Group(*renderables),
            title="[bold yellow]Analisis & Rekomendasi AI[/bold yellow]",
            border_style="yellow"
        )
    )




    # 5. Bottom Navigasi Content (Horizontal pointer navigation)
    from cli.menus import MENU_ITEMS

    nav_parts = []
    for idx, (key, label) in enumerate(MENU_ITEMS):
        if idx == selected_index:
            nav_parts.append(f"[bold white on dark_blue]▶ [{key}] {label}[/]")
        else:
            nav_parts.append(f"[{key}] {label}")

    nav_text = "  ".join(nav_parts)
    layout["bottom_nav"].update(
        Panel(Align.center(nav_text), title="[bold yellow]Navigasi Menu (Gunakan Panah ↑ ↓ ← → dan Enter)[/bold yellow]", border_style="yellow")
    )

    console.print(layout)




def render_back_button_prompt(label: str = "Kembali ke Dashboard Analytics"):
    """
    Render interactive back button pointer banner for UI feedback.
    """
    text = Text()
    text.append(" ▶ ", style="bold green")
    text.append(f"[ {label} (Tekan Enter) ]", style="bold white on green")

    panel = Panel(
        Align.center(text),
        border_style="green",
        padding=(0, 2)
    )
    console.print(panel)




