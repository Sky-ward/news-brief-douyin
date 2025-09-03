
# Daily International News → Chinese Brief + Douyin Script

**Goal**: Fetch top international news from reputable outlets within the last 24h, convert timestamps to **Asia/Tokyo (JST)**, generate:
1) `/out/brief_JST.md` — 6–8 items, each: 1-sentence Chinese summary + source link + JST time + tags (major breaking put on top).
2) `/out/tiktok_script.md` — 45–60s Douyin-ready script: Hook, 3–4 quick takes (each with on-screen text, B-roll hints, SFX), Wrap, CTA.

Optionally push the results to Telegram (or email).

---

## How to run locally

```bash
# 1) Python 3.10+ recommended
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2) Set environment (choose at least one translator)
export TZ=Asia/Tokyo
export OPENAI_API_KEY=sk-...         # for LLM translation/summarization to Chinese (preferred)
# or
export DEEPL_API_KEY=your_deepl_key   # optional fallback for translation (not implemented by default)

# Optional: Telegram push
export TELEGRAM_BOT_TOKEN=123456:ABC...
export TELEGRAM_CHAT_ID=123456789

# 3) Run
make all
# Artifacts: ./out/brief_JST.md  and  ./out/tiktok_script.md
```

> If no translation key is provided, titles/abstracts remain English with a note.
> For stable, repeatable runs in CI, set **OPENAI_API_KEY** as a GitHub **Secret**.

---

## GitHub Actions (08:30 JST daily)

This repo includes `.github/workflows/news_digest.yml` with a cron schedule:
- `30 23 * * *` (UTC) → 08:30 (JST) of the next day.

### Required GitHub Secrets
- `OPENAI_API_KEY` — for Chinese summaries.
- (Optional) `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` — to send the results to Telegram.

---

## Project structure

```
intl_news/
  __init__.py
  config.py           # feeds, constants, tagging
  fetch.py            # parse RSS feeds with feedparser
  normalize.py        # normalize entries, dedupe, 24h filter, JST conversion
  summarize.py        # 1-sentence Chinese summary via OpenAI (fallback: English)
  render.py           # brief markdown + Douyin script markdown
  push.py             # Telegram push
scripts/
  run_all.py          # orchestrates fetch→summarize→render→push
out/                  # artifacts
.github/workflows/
  news_digest.yml     # daily cron at 08:30 JST (23:30 UTC)
AGENTS.md             # this file
README.md             # same as AGENTS.md for convenience
Makefile
requirements.txt
```

---

## Acceptance criteria

- 6–8 “international/global” level items in the brief.
- Each item: **1-sentence Chinese summary**, **source media + link**, **JST time**, **tags**.
- At least one “major breaking” (if any) rises to the top.
- Douyin script (45–60s): Hook (≤3s) + 3–4 quick takes (8–12s each) + Wrap + CTA, with **on-screen text**, **B-roll** hints, **SFX** per take.
- A “Sources Today” section listing media+links.
- All timestamps are **JST**.
- If LLM is unavailable, the pipeline still runs, but marks items as “(未翻译)”.
```

