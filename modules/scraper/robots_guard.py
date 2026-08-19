import urllib.robotparser
from urllib.parse import urlparse
from typing import Dict
from rich.console import Console

console = Console()

# In-memory cache for parsed robots.txt rules
_robots_cache: Dict[str, urllib.robotparser.RobotFileParser] = {}


def get_domain_robots_parser(url: str) -> urllib.robotparser.RobotFileParser:
    """Fetch and parse robots.txt for a given target domain."""
    parsed = urlparse(url)
    domain = f"{parsed.scheme}://{parsed.netloc}"

    if domain in _robots_cache:
        return _robots_cache[domain]

    robots_url = f"{domain}/robots.txt"
    parser = urllib.robotparser.RobotFileParser()
    parser.set_url(robots_url)

    try:
        parser.read()
    except Exception as err:
        # If robots.txt cannot be fetched or doesn't exist, allow scraping by default
        console.print(f"[dim yellow]ℹ️ robots.txt tidak ditemukan untuk {domain} ({err}). Melanjutkan dengan izin default.[/dim yellow]")

    _robots_cache[domain] = parser
    return parser


def is_allowed(target_url: str, user_agent: str = "*") -> bool:
    """
    Check if scraping target_url is allowed by robots.txt politeness rules.
    Returns True if permitted, False if disallowed.
    """
    try:
        parser = get_domain_robots_parser(target_url)
        allowed = parser.can_fetch(user_agent, target_url)
        return allowed if allowed is not None else True
    except Exception:
        return True


def get_crawl_delay(target_url: str, user_agent: str = "*") -> float:
    """Retrieve recommended crawl delay (seconds) from robots.txt or default to 1.0s."""
    try:
        parser = get_domain_robots_parser(target_url)
        delay = parser.crawl_delay(user_agent)
        return float(delay) if delay else 1.0
    except Exception:
        return 1.0


if __name__ == "__main__":
    test_url = "https://beasiswaunggulan.kemdikbud.go.id"
    print(f"Is {test_url} allowed? ->", is_allowed(test_url))
