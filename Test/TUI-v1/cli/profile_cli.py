from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, FloatPrompt, IntPrompt

console = Console()


def prompt_user_profile_inputs(current_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Interactively prompt user to choose specific fields to edit or edit all at once.
    Falls back cleanly to Rich prompts for maximum terminal compatibility.
    """
    if current_profile is None:
        current_profile = {}

    profile = dict(current_profile)

    while True:
        console.print("\n[bold yellow]✏️ MENU PENGATURAN / EDIT PROFIL PENDAFTAR[/bold yellow]")
        console.print("[dim]Pilih item spesifik yang ingin diubah, atau pilih 'Edit SEMUA Data'.[/dim]\n")

        countries_str = ", ".join(profile.get("target_countries", []))
        options = [
            f"[1] Nama Lengkap             : {profile.get('name', 'Adika')}",
            f"[2] IPK Saat Ini             : {profile.get('gpa', 3.65):.2f}",
            f"[3] Skor IELTS               : {profile.get('ielts_score', 6.5)}",
            f"[4] Skor TOEFL iBT           : {profile.get('toefl_ibt_score', 85.0)}",
            f"[5] Usia (Tahun)             : {profile.get('age', 24)} Th",
            f"[6] Target Jenjang          : {profile.get('target_degree', 'S2')}",
            f"[7] Jurusan / Bidang Studi   : {profile.get('major_field', 'Computer Science')}",
            f"[8] Pengalaman Kerja        : {profile.get('work_exp_years', 2)} Th",
            f"[9] Publikasi Riset          : {profile.get('publications_count', 1)} Paper",
            f"[10] Negara Target Beasiswa  : {countries_str}",
            "[A] ✏️ Edit SEMUA Bidang Sekaligus",
            "[0] 💾 Selesai & Simpan Perubahan"
        ]

        try:
            from InquirerPy import inquirer
            from InquirerPy.validator import NumberValidator
            from InquirerPy.base.control import Choice

            choice = inquirer.select(
                message="Pilih kolom profil yang ingin Anda ubah:",
                choices=options,
                default=options[-1]
            ).execute()

            if "[0]" in choice:
                break

            elif "[1]" in choice:
                profile["name"] = inquirer.text(
                    message="Nama Lengkap Pendaftar:",
                    default=profile.get("name", "Adika")
                ).execute()

            elif "[2]" in choice:
                profile["gpa"] = float(inquirer.text(
                    message="IPK Saat Ini (0.00 - 4.00):",
                    default=str(profile.get("gpa", 3.65)),
                    validate=NumberValidator(float_allowed=True)
                ).execute())

            elif "[3]" in choice:
                profile["ielts_score"] = float(inquirer.text(
                    message="Skor IELTS Saat Ini (0.0 - 9.0):",
                    default=str(profile.get("ielts_score", 6.5)),
                    validate=NumberValidator(float_allowed=True)
                ).execute())

            elif "[4]" in choice:
                profile["toefl_ibt_score"] = float(inquirer.text(
                    message="Skor TOEFL iBT Saat Ini (0 - 120):",
                    default=str(profile.get("toefl_ibt_score", 85.0)),
                    validate=NumberValidator(float_allowed=True)
                ).execute())

            elif "[5]" in choice:
                profile["age"] = int(inquirer.text(
                    message="Usia (Tahun):",
                    default=str(profile.get("age", 24)),
                    validate=NumberValidator()
                ).execute())

            elif "[6]" in choice:
                profile["target_degree"] = inquirer.select(
                    message="Target Jenjang Pendidikan:",
                    choices=["S1", "S2", "S3"],
                    default=profile.get("target_degree", "S2")
                ).execute()

            elif "[7]" in choice:
                profile["major_field"] = inquirer.text(
                    message="Jurusan / Bidang Studi Target:",
                    default=profile.get("major_field", "Computer Science")
                ).execute()

            elif "[8]" in choice:
                profile["work_exp_years"] = int(inquirer.text(
                    message="Pengalaman Kerja (Tahun):",
                    default=str(profile.get("work_exp_years", 2)),
                    validate=NumberValidator()
                ).execute())

            elif "[9]" in choice:
                profile["publications_count"] = int(inquirer.text(
                    message="Jumlah Publikasi / Jurnal Riset:",
                    default=str(profile.get("publications_count", 1)),
                    validate=NumberValidator()
                ).execute())

            elif "[10]" in choice:
                current_countries = profile.get("target_countries", ["UK", "Europe"])
                if isinstance(current_countries, str):
                    current_countries = [current_countries]
                available_countries = ["UK", "Europe", "USA", "Australia", "Japan", "Indonesia"]
                country_choices = [
                    Choice(value=c, name=c, enabled=(c in current_countries))
                    for c in available_countries
                ]
                selected = inquirer.checkbox(
                    message="Pilih Negara Tujuan Beasiswa (Spasi untuk Centang, Enter untuk Konfirmasi):",
                    choices=country_choices
                ).execute()
                profile["target_countries"] = selected if selected else current_countries

            elif "[A]" in choice:
                profile["name"] = inquirer.text(message="Nama Lengkap:", default=profile.get("name", "Adika")).execute()
                profile["gpa"] = float(inquirer.text(message="IPK:", default=str(profile.get("gpa", 3.65)), validate=NumberValidator(float_allowed=True)).execute())
                profile["ielts_score"] = float(inquirer.text(message="IELTS:", default=str(profile.get("ielts_score", 6.5)), validate=NumberValidator(float_allowed=True)).execute())
                profile["toefl_ibt_score"] = float(inquirer.text(message="TOEFL iBT:", default=str(profile.get("toefl_ibt_score", 85.0)), validate=NumberValidator(float_allowed=True)).execute())
                profile["age"] = int(inquirer.text(message="Usia:", default=str(profile.get("age", 24)), validate=NumberValidator()).execute())
                profile["target_degree"] = inquirer.select(message="Jenjang:", choices=["S1", "S2", "S3"], default=profile.get("target_degree", "S2")).execute()
                profile["major_field"] = inquirer.text(message="Jurusan:", default=profile.get("major_field", "Computer Science")).execute()
                profile["work_exp_years"] = int(inquirer.text(message="Pengalaman Kerja:", default=str(profile.get("work_exp_years", 2)), validate=NumberValidator()).execute())
                profile["publications_count"] = int(inquirer.text(message="Publikasi:", default=str(profile.get("publications_count", 1)), validate=NumberValidator()).execute())
                break

        except Exception:
            # Fallback to Rich prompts
            sel = Prompt.ask("Masukkan nomor bidang yang ingin diubah (1-10, A=Semua, 0=Selesai)", default="0")
            if sel == "0":
                break
            elif sel == "1":
                profile["name"] = Prompt.ask("Nama Lengkap", default=profile.get("name", "Adika"))
            elif sel == "2":
                profile["gpa"] = FloatPrompt.ask("IPK", default=profile.get("gpa", 3.65))
            elif sel == "3":
                profile["ielts_score"] = FloatPrompt.ask("Skor IELTS", default=profile.get("ielts_score", 6.5))
            elif sel == "4":
                profile["toefl_ibt_score"] = FloatPrompt.ask("Skor TOEFL iBT", default=profile.get("toefl_ibt_score", 85.0))
            elif sel == "5":
                profile["age"] = IntPrompt.ask("Usia", default=profile.get("age", 24))
            elif sel == "6":
                profile["target_degree"] = Prompt.ask("Jenjang (S1/S2/S3)", default=profile.get("target_degree", "S2"))
            elif sel == "7":
                profile["major_field"] = Prompt.ask("Jurusan", default=profile.get("major_field", "Computer Science"))
            elif sel == "8":
                profile["work_exp_years"] = IntPrompt.ask("Pengalaman Kerja", default=profile.get("work_exp_years", 2))
            elif sel == "9":
                profile["publications_count"] = IntPrompt.ask("Publikasi", default=profile.get("publications_count", 1))
            elif sel == "10":
                c_str = Prompt.ask("Negara Target (pisah koma)", default=", ".join(profile.get("target_countries", ["Indonesia"])))
                profile["target_countries"] = [c.strip() for c in c_str.split(",") if c.strip()]
            elif sel.upper() == "A":
                profile["name"] = Prompt.ask("Nama Lengkap", default=profile.get("name", "Adika"))
                profile["gpa"] = FloatPrompt.ask("IPK", default=profile.get("gpa", 3.65))
                profile["ielts_score"] = FloatPrompt.ask("Skor IELTS", default=profile.get("ielts_score", 6.5))
                break

    summary_lines = (
        f"[bold yellow]Nama Lengkap[/]     : {profile['name']}\n"
        f"[bold yellow]IPK Saat Ini[/]     : [bold green]{profile['gpa']:.2f}[/]\n"
        f"[bold yellow]Skor IELTS[/]      : [bold green]{profile['ielts_score']}[/]\n"
        f"[bold yellow]Skor TOEFL iBT[/]  : {profile['toefl_ibt_score']}\n"
        f"[bold yellow]Usia[/]            : {profile['age']} Tahun\n"
        f"[bold yellow]Jenjang Target[/]  : {profile['target_degree']}\n"
        f"[bold yellow]Jurusan Target[/]  : {profile['major_field']}\n"
        f"[bold yellow]Pengalaman Kerja[/]: {profile['work_exp_years']} Tahun\n"
        f"[bold yellow]Publikasi Riset[/] : {profile['publications_count']} Paper\n"
        f"[bold yellow]Negara Target[/]   : {', '.join(profile['target_countries'])}"
    )

    console.print(Panel(
        summary_lines,
        title="[bold green]✅ Summary Updates Profil Berhasil Disimpan![/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    return profile


def manage_user_profiles(current_profile: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Interface Pengelola Profil Pendaftar (Multi-User):
    - Ubah data profil aktif
    - Ganti ke profil lain
    - Tambah profil pendaftar baru
    - Hapus profil pendaftar
    """
    from modules.database import get_all_user_profiles, save_user_profile, delete_user_profile, get_user_profile
    from cli.views import clear_screen, render_banner, render_user_profile_card

    if current_profile is None:
        current_profile = get_user_profile() or {}

    active_profile = dict(current_profile)

    while True:
        clear_screen()
        render_banner()
        render_user_profile_card(active_profile)

        all_profiles = get_all_user_profiles()
        active_name = active_profile.get("name", "Pengguna Utama")

        console.print(f"\n[bold cyan]👤 PENGELOLA PROFIL PENDAFTAR[/bold cyan] [dim](Profil Aktif Saat Ini: [bold yellow]{active_name}[/bold yellow])[/dim]")
        
        main_options = [
            f"[1] ✏️ Ubah Data Profil Aktif ({active_name})",
            f"[2] 🔄 Ganti Profil Aktif (Total: {len(all_profiles)} Profil Tersimpan)",
            "[3] ➕ Tambah Profil Pendaftar Baru",
            "[4] 🗑️ Hapus Profil Pendaftar",
            "[0] ⬅️ Kembali ke Dashboard Utama"
        ]

        try:
            from InquirerPy import inquirer

            sel = inquirer.select(
                message="Silakan pilih menu kelola profil:",
                choices=main_options,
                default=main_options[0]
            ).execute()

            if "[0]" in sel:
                break

            elif "[1]" in sel:
                clear_screen()
                render_banner()
                active_profile = prompt_user_profile_inputs(active_profile)
                save_user_profile(active_profile)

            elif "[2]" in sel:
                clear_screen()
                render_banner()
                profile_choices = [
                    f"[{p['id']}] {p['name']} ({p.get('target_degree', 'S1')}, IPK {p.get('gpa', 0.0):.2f})"
                    for p in all_profiles
                ]
                profile_choices.append("[CANCEL] ⬅️ Batal")
                
                chosen = inquirer.select(
                    message="Silakan pilih profil pendaftar yang ingin diaktifkan:",
                    choices=profile_choices
                ).execute()

                if "[CANCEL]" not in chosen:
                    target_id = chosen.split("]")[0].replace("[", "")
                    switched = get_user_profile(user_id=target_id)
                    if switched:
                        active_profile = switched
                        save_user_profile(active_profile)

            elif "[3]" in sel:
                clear_screen()
                render_banner()
                from datetime import datetime
                new_id = f"user_{int(datetime.now().timestamp())}"
                new_profile = {
                    "id": new_id,
                    "name": "Pendaftar Baru",
                    "gpa": 3.50,
                    "ielts_score": 7.0,
                    "toefl_ibt_score": 90.0,
                    "age": 22,
                    "target_degree": "S2",
                    "major_field": "Ilmu Komputer",
                    "work_exp_years": 1,
                    "publications_count": 0,
                    "target_countries": ["UK", "Europe"]
                }
                new_profile = prompt_user_profile_inputs(new_profile)
                save_user_profile(new_profile)
                active_profile = get_user_profile(user_id=new_profile["id"]) or new_profile

            elif "[4]" in sel:
                clear_screen()
                render_banner()
                deletable = [
                    f"[{p['id']}] {p['name']}"
                    for p in all_profiles if p['id'] != active_profile.get('id')
                ]
                if not deletable:
                    console.print("\n[yellow]⚠️ Tidak ada profil lain yang dapat dihapus (Profil aktif tidak dapat dihapus).[/yellow]")
                    Prompt.ask("Tekan Enter untuk kembali")
                else:
                    deletable.append("[CANCEL] ⬅️ Batal")
                    target = inquirer.select(message="Pilih profil yang ingin dihapus:", choices=deletable).execute()
                    if "[CANCEL]" not in target:
                        del_id = target.split("]")[0].replace("[", "")
                        delete_user_profile(del_id)

        except Exception:
            # Fallback for non-interactive TTY
            active_profile = prompt_user_profile_inputs(active_profile)
            save_user_profile(active_profile)
            break

    return active_profile


