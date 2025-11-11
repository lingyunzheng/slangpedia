import requests

def fetch_trending():
    try:
        data = requests.get("https://api.urbandictionary.com/v0/trending").json()
        return [item["word"] for item in data.get("list", [])]
    except:
        return []

existing = set(open("data/slang_words.txt","r",encoding="utf-8").read().splitlines())
new_words = set(fetch_trending())

merged = sorted(existing | new_words)

with open("data/slang_words.txt","w",encoding="utf-8") as f:
    f.write("\n".join(merged))
