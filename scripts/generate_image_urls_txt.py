import os
import re

# 抽出対象のフォルダ
CONTENT_DIR = "content/posts"

# 出力ファイル
OUTPUT_FILE = "image_urls.txt"

# 抽出対象の拡張子
TARGET_EXT = ".md"

# URL抽出用の正規表現（Markdown & HTML対応）
markdown_img_pattern = re.compile(r"!\[.*?\]\((https?://[^\s)]+)\)")
html_img_pattern = re.compile(r'<img\s+[^>]*src=["\'](https?://[^"\']+)["\']')

image_urls = set()

# 各.mdファイルを走査
for root, _, files in os.walk(CONTENT_DIR):
    for file in files:
        if file.endswith(TARGET_EXT):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

                # Markdown形式
                markdown_matches = markdown_img_pattern.findall(content)
                image_urls.update(markdown_matches)

                # HTML形式
                html_matches = html_img_pattern.findall(content)
                image_urls.update(html_matches)

# 結果を出力
with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    for url in sorted(image_urls):
        out.write(url + "\n")

print(f"{len(image_urls)} 件の画像URLを抽出しました -> {OUTPUT_FILE}")