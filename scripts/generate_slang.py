import os
import requests
from datetime import datetime
from slugify import slugify
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def get_trending_slang():
    try:
        data = requests.get("https://api.urbandictionary.com/v0/trending").json()
        if "list" in data and len(data["list"]) > 0:
            return [item["word"] for item in data["list"]][:30]
    except:
        pass

    # 备用：使用一个可控的稳定词库
    fallback = [
        "cap", "snatched", "ate", "rizz", "based",
        "no cap", "mid", "simp", "sus", "touch grass",
        "vibe check", "lowkey", "highkey", "bet", "gyatt",
        "delulu", "bruh", "yeet", "ratio", "skibidi"
    ]
    return fallback


def generate_post(word):
    prompt = f"""
Explain the slang: {word}.
Output bilingual structured content in markdown:

# What does "{word}" mean?（{word} 是什么意思？）

**English Meaning:**  
(brief meaning)

**中文解释：**  
(short meaning)

### Examples / 例句
1) English  
   Chinese
2) English  
   Chinese

### Origin / 来源背景
(short origin)

### Synonyms / 相似表达
3-5 similar words
"""
    r = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

def save_post(word, content):
    slug = slugify(f"what-does-{word}-mean")
    date = datetime.utcnow().strftime("%Y-%m-%d")
    path = f"content/slang/{slug}.md"
    md = f"---\ntitle: \"What Does '{word}' Mean? ({word} 是什么意思？)\"\ndate: {date}\nslug: \"{slug}\"\ntags: [\"slang\", \"internet\", \"tiktok\"]\n---\n\n" + content
    os.makedirs("content/slang", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)

if __name__ == "__main__":
    words = get_trending_slang()
    for w in words:
        text = generate_post(w)
        save_post(w, text)
