import sys
import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright
from rich.console import Console
from modules.scraper.robots_guard import is_allowed, get_crawl_delay
from modules.scraper.session_manager import get_session_file_path, has_valid_session

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()



async def scrape_web_page(
    url: str,
    session_name: Optional[str] = None,
    headless: bool = True,
    wait_until: str = "domcontentloaded"
) -> Dict[str, Any]:
    """
    Fetch a web page using async Playwright Chromium.
    Returns dict containing url, title, raw_html, inner_text, and success status.
    """
    if not is_allowed(url):
        console.print(f"[bold yellow]⚠️ Target URL {url} dilarang oleh aturan robots.txt. Mengabaikan scraping.[/bold yellow]")
        return {
            "url": url,
            "title": "Disallowed by robots.txt",
            "raw_html": "",
            "inner_text": "",
            "success": False,
            "error": "Disallowed by robots.txt"
        }

    delay = get_crawl_delay(url)
    if delay > 0:
        await asyncio.sleep(min(delay, 2.0))

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            
            context_kwargs = {
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }

            if session_name and has_valid_session(session_name):
                storage_path = get_session_file_path(session_name)
                context_kwargs["storage_state"] = storage_path
                console.print(f"[dim cyan]🔒 Memuat sesi autentikasi dari: {session_name}[/dim cyan]")

            context = await browser.new_context(**context_kwargs)
            page = await context.new_page()

            await page.goto(url, wait_until=wait_until, timeout=30000)
            title = await page.title()
            inner_text = await page.evaluate("() => document.body.innerText")
            raw_html = await page.content()

            await browser.close()

            return {
                "url": url,
                "title": title,
                "raw_html": raw_html,
                "inner_text": inner_text[:15000],  # Truncate text for LLM token efficiency
                "success": True,
                "error": ""
            }

    except Exception as err:
        console.print(f"[bold red]❌ Gagal melakukan scraping pada {url}: {err}[/bold red]")
        return {
            "url": url,
            "title": "",
            "raw_html": "",
            "inner_text": "",
            "success": False,
            "error": str(err)
        }


def fetch_page_sync(url: str, session_name: Optional[str] = None) -> Dict[str, Any]:
    """Synchronous helper wrapper for scrape_web_page."""
    return asyncio.run(scrape_web_page(url, session_name=session_name))
