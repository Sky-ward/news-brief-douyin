from __future__ import annotations
from typing import Dict, Any, List
import os
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = (
    "你是资深国际新闻编辑。请用**简洁中文**将英文新闻浓缩为**1句话**（不超过36个汉字），"
    "保持中立客观，不做推测；输出不含主观形容词，不带表情符号。"
)

def _compose_prompt(title: str, summary: str) -> str:
    text = f"标题：{title}\n摘要：{summary}\n请用中文写出1句简报。"
    return text

def _tagging(text_en: str) -> str:
    # Simple keyword tagging (fallback if model not used for tagging)
    from .config import TAGS
    t = text_en
    for tag, kws in TAGS:
        if any(k.lower() in t.lower() for k in kws):
            return tag
    return "【国际】"

def _format_time_jst(dt) -> str:
    return dt.strftime("%Y-%m-%d %H:%M JST")

def _openai_client():
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=1, max=6))
def _llm_summarize(client, title: str, summary: str) -> str:
    # Use the Responses API (new SDK)
    r = client.chat.completions.create(
        model="gpt-5.1-mini",  # lightweight, adjust if needed
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":_compose_prompt(title, summary)}
        ],
        temperature=0.2,
        max_tokens=60,
    )
    return r.choices[0].message.content.strip()

def summarize_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    client = _openai_client()
    out = []
    for it in items:
        title = it.get("title","")
        summary = it.get("summary","")
        if client:
            try:
                zh = _llm_summarize(client, title, summary)
                it["summary_zh"] = zh
            except Exception:
                it["summary_zh"] = f"(未翻译){title.strip()}"
        else:
            it["summary_zh"] = f"(未翻译){title.strip()}"
        it["tag"] = _tagging(title + " " + summary)
        out.append(it)
    return out