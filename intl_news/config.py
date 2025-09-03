from dataclasses import dataclass
from typing import List, Dict
from datetime import timezone

JST_TZ = "Asia/Tokyo"

# Reputable sources (RSS)
FEEDS: Dict[str, str] = {
    "Reuters World": "https://www.reuters.com/world/rss",
    "BBC World": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "The Guardian World": "https://www.theguardian.com/world/rss",
    "Al Jazeera Top": "https://www.aljazeera.com/xml/rss/all.xml",
}

# Simple region/topic tagging by keyword
TAGS = [
    ("【中东】", ["Gaza","Israel","Hamas","Lebanon","Iran","Iraq","Syria","Middle East","Gulf"]),
    ("【欧洲】", ["EU","Europe","European","Germany","France","UK","Britain","Ukraine","Russia","NATO","Belarus","Poland"]),
    ("【美洲】", ["United States","US ","U.S.","Mexico","Brazil","Argentina","Venezuela","Canada","Caribbean"]),
    ("【亚洲】", ["China","Beijing","Japan","Tokyo","Korea","Seoul","India","South Asia","Pakistan","Philippines","Indonesia","Malaysia","Singapore","Hong Kong","Taiwan","Vietnam","Thailand"]),
    ("【非洲】", ["Africa","Kenya","Nigeria","South Africa","Ethiopia","Sudan","Congo"]),
    ("【市场】", ["stocks","bonds","yields","equities","markets","gold","oil","WTI","Brent","inflation","rate","Fed","ECB"]),
    ("【科技】", ["AI","tech","technology","Google","Apple","Microsoft","chip","semiconductor","OpenAI","Nvidia","Meta","TikTok","X ","Twitter"]),
    ("【气候】", ["climate","heatwave","storm","hurricane","typhoon","La Nina","El Nino","flood","wildfire","drought","WMO"]),
    ("【人道/灾害】", ["earthquake","quake","landslide","famine","epidemic","outbreak","tsunami","death toll","casualties"]),
    ("【冲突/安全】", ["war","conflict","missile","drone","attack","strike","ceasefire","military","troops","army","navy"]),
]

# Keywords to flag "breaking"
BREAKING_HINTS = [
    "earthquake","blast","explosion","killed","death toll","state of emergency","magnitude","7.0","evacuate","ceasefire collapses","strike kills",
]

MAX_ITEMS = 8
MIN_ITEMS = 6