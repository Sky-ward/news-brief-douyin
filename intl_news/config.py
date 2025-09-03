from dataclasses import dataclass
from typing import List, Dict
from datetime import timezone

JST_TZ = "Asia/Tokyo"

# Reputable sources (RSS)
FEEDS: Dict[str, str] = {
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

# Simple region/topic tagging by keyword
TAGS = [
    ("【发售/延期】", ["release","launch","launches","delayed","delay","postponed","out now","coming"]),
    ("【更新/补丁】", ["update","patch","version","dlc","season","hotfix"]),
    ("【电竞】", ["esports","tournament","league","championship","match","roster","team"]),
    ("【行业/资本】", ["acquire","acquisition","merger","funding","investment","revenue","earnings","IPO","market"]),
]

# Keywords to flag "breaking"
BREAKING_HINTS = [
    "launch","release","delay","delayed","patch","update","tournament","championship","acquisition","funding",
]

MAX_ITEMS = 8
MIN_ITEMS = 6