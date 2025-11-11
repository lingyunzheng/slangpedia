import os
import requests
from datetime import datetime
from slugify import slugify

API_KEY = os.getenv("SILICONFLOW_API_KEY")

def get_slang_list():
    with open("data/slang_words.txt", "r", encoding="utf-8") as f:
        words = [w.strip() for w in f.readlines() if w.strip()]
    return list(set(words))



def generate_batch(words):
    url = "https://api.siliconflow.cn/v1/chat/completions"
    prompt = "Generate bilingual slang explanations in markdown for:\n" + "\n".join(words)
    payload = {"model": "Qwen/Qwen2.5-7B-Instruct","messages":[{"role":"user","content":prompt}]}
    r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {API_KEY}"}).json()
    return r["choices"][0]["message"]["content"]

def save_post(word, content):
    slug = slugify(f"what-does-{word}-mean")
    date = datetime.utcnow().strftime("%Y-%m-%d")
    md = f"""---
title: "What Does '{word}' Mean? ({word} 是什么意思？)"
slug: "{slug}"
date: {date}
tags: [slang, internet, tiktok]
---

{content}

**See also:**
- /slang/
"""
    os.makedirs("content/slang", exist_ok=True)
    with open(f"content/slang/{slug}.md", "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    words = get_slang_list()
    text = generate_batch(words)  # 🔥 一次生成全部内容
    blocks = text.split("# What does")
    for block in blocks:
        block = block.strip()
        if not block: continue
        first_word = block.split('"')[1] if '"' in block else block.split()[0]
        save_post(first_word, "# What does " + block)
