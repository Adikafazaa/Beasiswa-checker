import os
import json
import httpx
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()
console = Console()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "auto").lower()
AI_MODEL = os.getenv("AI_MODEL", os.getenv("GEMINI_MODEL", "deepseek-v4-flash"))


def generate_llm_text(prompt: str, system_instruction: str = "") -> Optional[str]:
    """
    Generate completion text using DeepSeek API or Google Gemini API.
    Supports standard OpenAI-compatible DeepSeek endpoints (https://api.deepseek.com/chat/completions).
    """
    # 1. Try DeepSeek API if DEEPSEEK_API_KEY is configured
    if (DEEPSEEK_API_KEY and DEEPSEEK_API_KEY != "your_deepseek_api_key_here") or AI_PROVIDER == "deepseek":
        try:
            headers = {
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            }
            messages = []
            if system_instruction:
                messages.append({"role": "system", "content": system_instruction})
            messages.append({"role": "user", "content": prompt})

            model_to_use = AI_MODEL if AI_MODEL else "deepseek-chat"
            payload = {
                "model": model_to_use,
                "messages": messages,
                "temperature": 0.7
            }

            url = f"{DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions"
            with httpx.Client(timeout=15.0) as client:
                resp = client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    console.print(f"[dim yellow]ℹ️ DeepSeek API returned status {resp.status_code}: {resp.text}[/dim yellow]")
        except Exception as err:
            console.print(f"[dim yellow]ℹ️ DeepSeek API call encountered error/timeout: {err}[/dim yellow]")



    # 2. Fallback to Google Gemini API if GEMINI_API_KEY is configured
    if (GEMINI_API_KEY and GEMINI_API_KEY != "your_google_gemini_api_key_here") or AI_PROVIDER == "gemini":
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_API_KEY)
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
            response = client.models.generate_content(
                model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
                contents=full_prompt
            )
            if response and response.text:
                return response.text
        except Exception as err:
            console.print(f"[dim yellow]ℹ️ Gemini API call encountered error: {err}[/dim yellow]")

    return None
