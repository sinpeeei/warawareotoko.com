import os
import re

CONTENT_DIR = "content/posts"

# パターン1: <img src="/images/xxx.jpg" | relURL" → <img src="/images/xxx.jpg"
BROKEN_SRC_PATTERN = re.compile(r'src="(/images/[^"]+?)"\s*\|\s*\w+"')

# パターン2: 変な空白や | absURL も対応（閉じクォートがないパターンも含む）
BROKEN_SRC_PATTERN2 = re.compile(r'src="(/images/[^"]+?)"\s*\|\s*\w+\s*"?')

for root, dirs, files in os.walk(CONTENT_DIR):
    for file in files:
        if file == "index.md":
            md_path = os.path.join(root, file)
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            new_content = BROKEN_SRC_PATTERN.sub(r'src="\1"', content)
            new_content = BROKEN_SRC_PATTERN2.sub(r'src="\1"', new_content)

            if new_content != content:
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("すべての壊れた画像タグを修正しました！")