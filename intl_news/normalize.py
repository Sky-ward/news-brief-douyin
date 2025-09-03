from __future__ import annotations
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import hashlib
import re

from .config import MAX_ITEMS, MIN_ITEMS, BREAKING_HINTS

JST = ZoneInfo("Asia/Tokyo")

def dedupe(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for it in items:
        key = hashlib.md5((it.get("title","") + "|" + (it.get("link","") or "")).encode("utf-8")).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out

def within_24h_jst(dt: datetime, now_jst: datetime) -> bool:
    if not dt:
        return False
    dt_jst = dt.astimezone(JST)
    return (now_jst - dt_jst) <= timedelta(hours=24)

def filter_and_sort(items: List[Dict[str, Any]], now: datetime | None = None) -> List[Dict[str, Any]]:
    now_jst = (now or datetime.now(tz=JST))
    # 24h filter
    items = [it for it in items if it.get("published") and within_24h_jst(it["published"], now_jst)]
    # score by recency + breaking hints
    scored: List[Tuple[float, Dict[str, Any]]] = []
    for it in items:
        dt = it["published"].astimezone(JST)
        age_hours = (now_jst - dt).total_seconds() / 3600.0
        recency_score = max(0.0, 24.0 - age_hours)  # newer = higher
        text = (it.get("title","") + " " + it.get("summary","")).lower()
        breaking_bonus = 8.0 if any(k in text for k in BREAKING_HINTS) else 0.0
        total = recency_score + breaking_bonus
        it["published_jst"] = dt
        it["score"] = total
        it["is_breaking"] = breaking_bonus > 0
        scored.append((total, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    ranked = [it for _, it in scored]
    # pick top N
    if len(ranked) < MIN_ITEMS:
        ranked = ranked[:MIN_ITEMS]
    else:
        ranked = ranked[:MAX_ITEMS]
    # ensure any breaking item goes to top (stable)
    breakings = [it for it in ranked if it.get("is_breaking")]
    non_breakings = [it for it in ranked if not it.get("is_breaking")]
    return breakings + [it for it in non_breakings if it not in breakings]