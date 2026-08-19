import os
import json
from typing import Optional
from rich.console import Console

console = Console()

SESSIONS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sessions")


def get_session_file_path(session_name: str = "default_session") -> str:
    """Return absolute path for a session JSON storage state file."""
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    clean_name = session_name.lower().replace(" ", "_")
    return os.path.join(SESSIONS_DIR, f"{clean_name}.json")


def has_valid_session(session_name: str = "default_session") -> bool:
    """Check if session JSON file exists and contains valid cookies/storage state."""
    file_path = get_session_file_path(session_name)
    if not os.path.exists(file_path):
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return isinstance(data, dict) and ("cookies" in data or "origins" in data)
    except Exception:
        return False


def save_storage_state(storage_state_data: dict, session_name: str = "default_session") -> str:
    """Save Playwright storage state dict to JSON file."""
    file_path = get_session_file_path(session_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(storage_state_data, f, indent=2)
    console.print(f"[bold green]✅ Auth Session cookie tersimpan di: {file_path}[/bold green]")
    return file_path
