from pathlib import Path
from typing import Dict, List

import yaml

JST_TZ = "Asia/Tokyo"

# built-in defaults
DEFAULT_FEEDS = {
    "IGN": "https://feeds.ign.com/ign/all",
    "GameSpot": "https://www.gamespot.com/feeds/news/",
    "Polygon": "https://www.polygon.com/rss/index.xml",
    "Eurogamer": "https://www.eurogamer.net/feed",
    "PC Gamer": "https://www.pcgamer.com/rss/",
    "Rock Paper Shotgun": "https://www.rockpapershotgun.com/feed",
    "The Verge Games": "https://www.theverge.com/games/rss/index.xml",
    "Dot Esports": "https://dotesports.com/feed",
    "HLTV": "https://www.hltv.org/rss/news",
    "PlayStation Blog": "https://blog.playstation.com/feed/",
    "Xbox Wire": "https://news.xbox.com/en-us/feed/",
    "Nintendo News": "https://www.nintendo.com/whatsnew/feed",
    "Steam News": "https://store.steampowered.com/feeds/news.xml",
    "PocketGamer.biz": "https://www.pocketgamer.biz/rss/",
}

DEFAULT_TAGS = [
    (
        "【发售/延期】",
        [
            "release",
            "launch",
            "launches",
            "delayed",
            "delay",
            "postponed",
            "out now",
            "coming",
        ],
    ),
    ("【更新/补丁】", ["update", "patch", "version", "dlc", "season", "hotfix"]),
    (
        "【电竞】",
        ["esports", "tournament", "league", "championship", "match", "roster", "team"],
    ),
    (
        "【行业/资本】",
        [
            "acquire",
            "acquisition",
            "merger",
            "funding",
            "investment",
            "revenue",
            "earnings",
            "IPO",
            "market",
        ],
    ),
]

DEFAULT_BREAKING = [
    "launch",
    "release",
    "delay",
    "delayed",
    "patch",
    "update",
    "tournament",
    "championship",
    "acquisition",
    "funding",
]

CONFIG_DIR = Path("config")


def _load_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return None


feeds_yaml = _load_yaml(CONFIG_DIR / "feeds_gaming.yaml")
if feeds_yaml:
    FEEDS: Dict[str, str] = {
        item["name"]: item["url"] for item in feeds_yaml if item.get("enabled", True)
    }
else:
    FEEDS = DEFAULT_FEEDS


_tags_yaml = _load_yaml(CONFIG_DIR / "tags.yaml")
if _tags_yaml:
    TAGS: List = [(it["tag"], it.get("keywords", [])) for it in _tags_yaml]
else:
    TAGS = DEFAULT_TAGS

_breaking_yaml = _load_yaml(CONFIG_DIR / "breaking.yaml")
if _breaking_yaml:
    BREAKING_HINTS: List[str] = list(_breaking_yaml)
else:
    BREAKING_HINTS = DEFAULT_BREAKING

MAX_ITEMS = 8
MIN_ITEMS = 6
