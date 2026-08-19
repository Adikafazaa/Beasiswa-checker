import sys
from typing import Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt

console = Console()

MENU_ITEMS = [
    ("1", "Dashboard"),
    ("2", "Profil"),
    ("3", "Filter"),
    ("4", "Bookmark"),
    ("5", "Fitur AI & Scraper"),
    ("0", "Keluar")
]






def read_key() -> str:
    """
    Read a single keypress or arrow key cross-platform (Windows / Linux / macOS).
    Returns 'UP', 'DOWN', 'LEFT', 'RIGHT', 'ENTER', or character pressed ('1', '2', '3', '4', '5', '0').
    Guaranteed to return a non-None string.
    """
    try:
        if sys.platform == "win32":
            import msvcrt
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                if ch2 == b'H':
                    return "UP"
                elif ch2 == b'P':
                    return "DOWN"
                elif ch2 == b'K':
                    return "LEFT"
                elif ch2 == b'M':
                    return "RIGHT"
                return ""
            elif ch in (b'\r', b'\n'):
                return "ENTER"
            else:
                try:
                    return ch.decode('utf-8', errors='ignore')
                except Exception:
                    return ""
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch2 = sys.stdin.read(2)
                    if ch2 == '[A':
                        return "UP"
                    elif ch2 == '[B':
                        return "DOWN"
                    elif ch2 == '[D':
                        return "LEFT"
                    elif ch2 == '[C':
                        return "RIGHT"
                elif ch in ('\r', '\n'):
                    return "ENTER"
                return ch or ""
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception:
        return ""


def handle_dashboard_navigation(current_index: int = 0) -> Tuple[str, int, str]:
    """
    Handle interactive arrow key navigation without printing extra text below the grid.
    Returns (action_type, selected_index, selected_key).
    action_type can be 'NAVIGATE', 'PAGE_NEXT', 'PAGE_PREV', or 'SELECT'.
    """
    key = read_key()
    if not key:
        return ("NAVIGATE", current_index, MENU_ITEMS[current_index][0])

    key_lower = key.lower()

    if key_lower == 'e':
        return ("EXPAND_AI", current_index, "E")


    elif key_lower in ('n', ']'):
        return ("PAGE_NEXT", current_index, MENU_ITEMS[current_index][0])

    elif key_lower in ('p', '['):
        return ("PAGE_PREV", current_index, MENU_ITEMS[current_index][0])


    elif key in ("UP", "LEFT"):
        new_index = (current_index - 1) % len(MENU_ITEMS)
        return ("NAVIGATE", new_index, MENU_ITEMS[new_index][0])

    elif key in ("DOWN", "RIGHT"):
        new_index = (current_index + 1) % len(MENU_ITEMS)
        return ("NAVIGATE", new_index, MENU_ITEMS[new_index][0])

    elif key == "ENTER":
        return ("SELECT", current_index, MENU_ITEMS[current_index][0])

    elif key in ["1", "2", "3", "4", "5", "6", "0"]:

        for idx, (k, _) in enumerate(MENU_ITEMS):
            if k == key:
                return ("SELECT", idx, key)

    return ("NAVIGATE", current_index, MENU_ITEMS[current_index][0])

