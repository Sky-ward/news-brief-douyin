from __future__ import annotations
import os, requests, pathlib

BOT = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT = os.getenv("TELEGRAM_CHAT_ID")

def push_telegram(text: str) -> None:
    if not (BOT and CHAT):
        print("Telegram not configured; skip push.")
        return
    url = f"https://api.telegram.org/bot{BOT}/sendMessage"
    resp = requests.post(url, json={
        "chat_id": CHAT,
        "text": text[:4000],  # Telegram message limit handling
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }, timeout=15)
    resp.raise_for_status()
    print("Telegram push ok.")