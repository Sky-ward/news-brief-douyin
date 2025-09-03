from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from zoneinfo import ZoneInfo

JST = ZoneInfo("Asia/Tokyo")

HEADER_TMPL = "1) 今日游戏资讯简报（JST 日期：{date})\n"


def render_brief(items: List[Dict[str, Any]]) -> str:
    today = datetime.now(JST).strftime("%Y-%m-%d")
    lines = [HEADER_TMPL.format(date=today)]
    for it in items:
        prefix = "【突发】" if it.get("is_breaking") else ""
        line = (
            f"- {prefix}{it['summary_zh']} "
            f"来源：{it['source']}（{it['link']}）；"
            f"发布时间：{it['published_jst'].strftime('%Y-%m-%d %H:%M JST')}；"
            f"标签{it['tag']}。"
        )
        lines.append(line)
    return "\n".join(lines)


def pick_top_for_tiktok(
    items: List[Dict[str, Any]], n: int = 4
) -> List[Dict[str, Any]]:
    # choose breaking first, then score
    breakings = [it for it in items if it.get("is_breaking")]
    rest = [it for it in items if not it.get("is_breaking")]
    top = breakings[:n] + rest[: max(0, n - len(breakings))]
    return top[:n]


def render_tiktok(items: List[Dict[str, Any]]) -> str:
    top4 = pick_top_for_tiktok(items, 4)
    today_kw = (
        "、".join([it.get("tag", "【国际】").strip("【】") for it in top4][:3])
        or "全球要闻"
    )
    lines = []
    lines.append("2) 抖音短视频逐字稿（45–60 秒）\n")
    # Hook
    lines.append("- Hook（0–3s）  ")
    lines.append(f"口播：今天游戏圈关键词——{today_kw}。  ")
    lines.append(f"屏幕大字：{today_kw.replace('、','｜')}  ")
    lines.append("B-roll：主机、PC、手游游戏画面快切  ")
    lines.append("SFX：轻击+上扬提示音\n")
    # Quick takes
    for i, it in enumerate(top4, start=1):
        lines.append(f"- 快讯{i}（{3+ (i-1)*11}–{3+i*11}s）  ")
        lines.append(f"口播：{it['summary_zh']}  ")
        lines.append(f"屏幕大字：{it['tag'].strip('【】')}快讯  ")
        lines.append("B-roll：相关游戏实机、预告或电竞镜头（避免剧透/不当内容）  ")
        lines.append("转场SFX：whoosh\n")
    # Wrap + CTA
    lines.append("- Wrap（45–55s）  ")
    lines.append("口播：以上是今日游戏动态，信息或有更新，以官方渠道为准。  ")
    lines.append("屏幕大字：信息随时更新\n")
    lines.append("- CTA（55–60s）  ")
    lines.append("口播：关注我，60秒掌握游戏圈。  ")
    lines.append("屏幕大字：关注｜收藏\n")
    # Extras
    lines.append("封面标题（≤14字）：今日游戏资讯速览")
    lines.append(
        "视频说明/Caption（≤80字）：一分钟看游戏圈：精选主机、PC、手游与电竞动态，更多详见来源。"
    )
    lines.append("话题标签：#游戏资讯 #主机游戏 #PC游戏 #手游 #电竞")
    return "\n".join(lines)


def render_sources(items: List[Dict[str, Any]]) -> str:
    seen = set()
    lines = ["\n3) 元信息与可复用", "- 今日使用的来源清单（媒体名 + 链接）："]
    for it in items:
        key = (it["source"], it["link"])
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"  - {it['source']}：{it['link']}")
    return "\n".join(lines)
