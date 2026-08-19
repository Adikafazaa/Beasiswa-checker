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

# Reconfigure Windows stdout encoding for UTF-8 emoji support
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()


def clear_screen():
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def render_banner():
    """Render application header banner using Rich."""
    banner_text = Text()
    banner_text.append("🎓 BEASISWA CHECKER ANALYTICS 🎓\n", style="bold cyan")
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
        title="[bold green]👤 Profil Pendaftar Saat Ini[/]",
        border_style="green",
        padding=(0, 1)
    )
    console.print(panel)


def make_progress_bar(score: float) -> str:
    """Create ASCII progress bar for match score percentage."""
    filled = int(score / 10)
    unfilled = 10 - filled
    return f"[{'█' * filled}{' ' * unfilled}]"


def render_matching_table(match_results: List[Dict[str, Any]]):
    """Render matching analytics table with colored badges and progress bars."""
    table = Table(
        title="📊 Hasil Analytics & Matrix Kecocokan Beasiswa",
        header_style="bold magenta",
        border_style="bright_black",
        expand=True
    )

    table.add_column("Kategori Peluang", style="bold", justify="left")
    table.add_column("Nama Beasiswa", style="bold white")
    table.add_column("Peluang (%)", justify="center")
    table.add_column("Status Syarat", justify="center")
    table.add_column("Kuadran Rekomendasi", justify="left")

    for res in match_results:
        cat = res["category"]
        if cat == "Safety":
            cat_styled = f"[green]🟢 {res['badge']}[/]"
            score_styled = f"[bold green]{res['fit_score']}%[/] [green]{make_progress_bar(res['fit_score'])}[/]"
        elif cat == "Target":
            cat_styled = f"[yellow]🟡 {res['badge']}[/]"
            score_styled = f"[bold yellow]{res['fit_score']}%[/] [yellow]{make_progress_bar(res['fit_score'])}[/]"
        else:
            cat_styled = f"[red]🔴 {res['badge']}[/]"
            score_styled = f"[bold red]{res['fit_score']}%[/] [red]{make_progress_bar(res['fit_score'])}[/]"

        if res["is_qualified"]:
            status_styled = f"[green]{res['status_label']}[/]"
        else:
            status_styled = f"[yellow]{res['status_label']}[/]"

        table.add_row(
            cat_styled,
            res["scholarship_name"],
            score_styled,
            status_styled,
            res["quadrant"]
        )

    console.print(table)


def render_terminal_chart(match_results: List[Dict[str, Any]]):
    """Render ASCII/Unicode score distribution chart using Plotext."""
    if not match_results:
        return

    console.print("\n[bold cyan]📈 Visualisasi Sebaran Skor Peluang Beasiswa (Plotext Chart)[/bold cyan]")
    
    names = [m["scholarship_name"].split(" ")[0] for m in match_results[:6]]
    scores = [m["fit_score"] for m in match_results[:6]]

    plt.clf()
    plt.bar(names, scores, color="cyan", width=0.5)
    plt.title("Skor Match (%) per Beasiswa")
    plt.ylim(0, 100)
    plt.plotsize(65, 11)
    plt.theme("dark")
    plt.show()
    print()


def render_ai_advice_panel(advice_list: List[str]):
    """Render AI Gap Analysis advice in a Rich Panel."""
    content = "\n".join(advice_list)
    panel = Panel(
        content,
        title="[bold yellow]💡 AI Gap Analysis & Rekomendasi Action Plan[/]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(panel)


def render_scholarship_list_table(scholarships: List[Dict[str, Any]], filter_info: str = "Semua Beasiswa"):
    """Render clean, panelled search & filter database table with row break lines."""
    table = Table(
        header_style="bold magenta",
        border_style="bright_black",
        show_lines=True,
        expand=True
    )

    table.add_column("Nama Beasiswa", style="bold yellow", ratio=4)
    table.add_column("Penyelenggara", style="cyan", ratio=4)
    table.add_column("Pendanaan", style="bold green", justify="center", ratio=2)
    table.add_column("Jenjang", justify="center", ratio=2)
    table.add_column("Min IPK", justify="center", ratio=1)
    table.add_column("Min IELTS", justify="center", ratio=1)
    table.add_column("Deadline", justify="center", ratio=2)

    for s in scholarships:
        table.add_row(
            f"[bold yellow]{s['name']}[/]",
            s["provider"],
            f"[bold green]{s['funding_type']}[/]",
            ", ".join(s["target_degrees"]),
            f"{s['min_gpa']:.2f}",
            f"{s['min_ielts']}",
            s["deadline_date"]
        )

    panel = Panel(
        table,
        title=f"[bold cyan]📚 Database Master Beasiswa ({len(scholarships)} Ditemukan - Filter: {filter_info})[/bold cyan]",
        border_style="cyan"
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
    advice_text = "\n".join(advice_list)
    layout["middle"]["right_sidebar"]["analysis_action"].update(
        Panel(advice_text, title="Analisis & Rekomendasi AI", border_style="white")
    )

    # 5. Bottom Navigasi Content (Horizontal pointer navigation)
    menu_items = [
        ("1", "Dashboard"),
        ("2", "Kelola Profil"),
        ("3", "Cari & Filter"),
        ("4", "Scraper Web"),
        ("5", "AI Advisor"),
        ("0", "Keluar")
    ]

    nav_parts = []
    for idx, (key, label) in enumerate(menu_items):
        if idx == selected_index:
            nav_parts.append(f"[bold white on dark_blue] ▶ [{key}] {label} [/]")
        else:
            nav_parts.append(f"  [{key}] {label}  ")

    nav_text = "   ".join(nav_parts)
    layout["bottom_nav"].update(
        Panel(Align.center(nav_text), title="[bold yellow]Menu Utama (Gunakan Tombol Panah ↑ ↓ ← → dan Enter)[/bold yellow]", border_style="yellow")
    )

    console.print(layout)







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
        Panel(user_info_lines, title="User-Info", border_style="white")
    )

    # 4. Analysis-&-Action Content
    advice_text = "\n".join(advice_list)
    layout["middle"]["right_sidebar"]["analysis_action"].update(
        Panel(advice_text, title="Analysis-&-Action", border_style="white")
    )

    # 5. Bottom Navigasi Content (Horizontal pointer navigation)
    menu_items = [
        ("1", "Dashboard"),
        ("2", "Edit Profil"),
        ("3", "Filter Beasiswa"),
        ("4", "Scraper"),
        ("5", "AI Advisor"),
        ("0", "Keluar")
    ]

    nav_parts = []
    for idx, (key, label) in enumerate(menu_items):
        if idx == selected_index:
            nav_parts.append(f"[bold white on dark_blue] ▶ [{key}] {label} [/]")
        else:
            nav_parts.append(f"  [{key}] {label}  ")

    nav_text = "   ".join(nav_parts)
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




