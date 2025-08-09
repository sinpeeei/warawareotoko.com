import os
import re

CONTENT_DIR = "content/posts"

# src="{{ ... }}" を src="/images/ファイル名" に変換
TEMPLATE_IMG_PATTERN = re.compile(r'<img[^>]*src="\{\{\s*(.*?)\s*\}\}"[^>]*>', re.IGNORECASE)

for root, dirs, files in os.walk(CONTENT_DIR):
    for file in files:
        if file == "index.md":
            md_path = os.path.join(root, file)
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # 修正対象があるか
            if '{{' in content:
                new_content = content

                # ファイル名を取得できる形式なら置換
                def replacer(match):
                    inner = match.group(1)
                    filename = os.path.basename(inner)
                    return f'<img src="/images/{filename}" alt="">'

                new_content = TEMPLATE_IMG_PATTERN.sub(replacer, content)

                # 保存
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

print("テンプレ構文の <img> タグを修正しました。")