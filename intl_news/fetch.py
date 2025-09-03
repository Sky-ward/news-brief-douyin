from typing import List, Dict, Any
import feedparser
from datetime import datetime, timedelta, timezone
from dateutil import parser as dtparser
from zoneinfo import ZoneInfo
from .config import FEEDS

def _parse_time(entry) -> datetime | None:
    # Try published / updated fields
    for key in ("published", "updated", "pubDate"):
        val = entry.get(key)
        if val:
            try:
                dt = dtparser.parse(val)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                return dt
            except Exception:
                pass
    # Try structured time
    for key in ("published_parsed","updated_parsed"):
        st = entry.get(key)
        if st:
            try:
                return datetime(*st[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None

def fetch_all() -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for source, url in FEEDS.items():
        d = feedparser.parse(url)
        for e in d.entries[:50]:  # cap
            dt = _parse_time(e)
            link = e.get("link") or ""
            title = (e.get("title") or "").strip()
            summary = (e.get("summary") or e.get("description") or "").strip()
            items.append({
                "source": source,
                "link": link,
                "title": title,
                "summary": summary,
                "published": dt,
            })
    return items