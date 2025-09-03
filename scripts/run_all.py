from __future__ import annotations
import argparse, os, pathlib
from datetime import datetime
from zoneinfo import ZoneInfo

from intl_news.fetch import fetch_all
from intl_news.normalize import dedupe, filter_and_sort
from intl_news.summarize import summarize_items
from intl_news.render import render_brief, render_tiktok, render_sources
from intl_news.push import push_telegram

OUT = pathlib.Path("out")
OUT.mkdir(exist_ok=True, parents=True)

def step_fetch():
    items = fetch_all()
    # Save raw for debugging
    (OUT / "raw_count.txt").write_text(str(len(items)), encoding="utf-8")
    return items

def step_summarize(items):
    items2 = dedupe(items)
    items3 = filter_and_sort(items2)
    items4 = summarize_items(items3)
    return items4

def step_render(items):
    brief = render_brief(items)
    tiktok = render_tiktok(items)
    sources = render_sources(items)
    (OUT / "brief_JST.md").write_text(brief + "\n\n" + sources + "\n", encoding="utf-8")
    (OUT / "tiktok_script.md").write_text(tiktok + "\n\n" + sources + "\n", encoding="utf-8")
    return brief, tiktok

def step_push(brief, tiktok):
    # Push only brief (tiktok can be longer than telegram limit)
    push_telegram(brief)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", choices=["fetch","summarize","render","push"], default=None)
    args = ap.parse_args()

    if args.step == "fetch":
        step_fetch()
        return

    # full pipeline
    raw = step_fetch()
    items = step_summarize(raw)
    brief, tiktok = step_render(items)

    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        step_push(brief, tiktok)
    print("Done. See ./out/brief_JST.md and ./out/tiktok_script.md")

if __name__ == "__main__":
    main()