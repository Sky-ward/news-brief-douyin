import sys
from datetime import datetime, timedelta
from pathlib import Path

from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from intl_news.normalize import within_24h_jst


def test_within_24h():
    now = datetime(2024, 1, 1, tzinfo=ZoneInfo("Asia/Tokyo"))
    inside = now - timedelta(hours=23)
    outside = now - timedelta(hours=25)
    assert within_24h_jst(inside, now)
    assert not within_24h_jst(outside, now)
