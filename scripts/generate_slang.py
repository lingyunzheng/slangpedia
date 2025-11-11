import os
import requests
from datetime import datetime
from slugify import slugify

API_KEY = os.getenv("SILICONFLOW_API_KEY")

def get_trending_slang():
    return [
        "cap", "snatched", "ate", "rizz", "based",
        "no cap", "mid", "simp", "sus", "touch grass",
        "vibe check", "lowkey", "highkey", "bet", "gyatt",
        "delulu", "bruh", "yeet", "ratio", "skibidi"
    ]

def generate_post(word):
    url = "https://api.siliconflow.cn/v1/chat/completions"
    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "user", "content": f"""
Explain the slang: {word}.
Output bilingual structured content in markdown:

# What does "{word}" mean?（{word} 是什么意思？）

**English Meaning:**  
(short explanation)

**中文解释：**  
(中文简短解释)

### Examples / 例句
1) English sentence  
   中文翻译
2) English sentence  
   中文翻译

### Origin / 来源背景
(short origin)

### Synonyms / 相似表达
(list 3-5)
            """}
        ]
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    r = requests.post(url, json=payload, headers=headers).json()
    return r["choices"][0]["message"]["content"]

def save_post(word, content):
    slug = slugify(f"what-does-{word}-mean")
    date = datetime.utcnow().strftime("%Y-%m-%d")
    md = f"""---
title: "What Does '{word}' Mean? ({word} 是什么意思？)"
slug: "{slug}"
date: {date}
tags:
  - slang
  - internet
  - tiktok
---

{content}
"""
    os.makedirs("content/slang", exist_ok=True)
    with open(f"content/slang/{slug}.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    for w in get_trending_slang():
        save_post(w, generate_post(w))
