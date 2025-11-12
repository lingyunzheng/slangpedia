import os

def clean_md_file(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        # 去掉开头 4 个以上的空格或 tab
        cleaned.append(line.lstrip())

    with open(path, "w", encoding="utf-8") as f:
        f.writelines(cleaned)
    print(f"✅ Cleaned: {path}")

def clean_all():
    base_dir = "content/slang"
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                clean_md_file(os.path.join(root, file))

if __name__ == "__main__":
    clean_all()
