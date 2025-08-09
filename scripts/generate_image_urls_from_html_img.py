import os
import re

CONTENT_DIR = "content/posts"

# src="{{ ... }}" を src="/images/ファイル名" に変換
TEMPLATE_IMG_PATTERN = re.compile(r'<img[^>]*src="\{\{\s*(.*?)\s*(\|\s*\w+)?\s*\}\}"[^>]*>', re.IGNORECASE)
RELURL_RESIDUE_PATTERN = re.compile(r'\s*\|\s*\w+')

for root, dirs, files in os.walk(CONTENT_DIR):
    for file in files:
        if file == "index.md":
            md_path = os.path.join(root, file)
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Hugoテンプレの src を正しいパスへ変換
            def replacer(match):
                inner = match.group(1)
                filename = os.path.basename(inner)
                return f'<img src="/images/{filename}" alt="">'

            new_content = TEMPLATE_IMG_PATTERN.sub(replacer, content)

            # 2. まだ残っている `| relURL` 的な構文を削除
            new_content = new_content.replace('| relURL', '').replace('| absURL', '')

            # 保存
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(new_content)

print("テンプレ構文と relURL の残骸をすべて修正しました。")