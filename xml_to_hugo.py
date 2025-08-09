import os
import re
from bs4 import BeautifulSoup
from pathlib import Path
import frontmatter

EXPORT_DIR = Path("export_posts")
EXPORT_DIR.mkdir(exist_ok=True)

# ✅ 修正済：現在の作業ディレクトリにあるXMLを参照
XML_PATH = Path("WordPress.2025-07-06.xml")
soup = BeautifulSoup(XML_PATH.read_text(), "xml")

for item in soup.find_all("item"):
    title = item.title.text.strip().replace("/", "_")
    link = item.link.text.strip()
    date = item.pubDate.text.strip()
    content_encoded = item.find("content:encoded")
    content = content_encoded.text.strip() if content_encoded else ""

    # slug を生成（post-1234 形式）
    post_id_tag = item.find("wp:post_id")
    if not post_id_tag:
        continue
    slug = f"post-{post_id_tag.text.strip()}"

    # カテゴリとタグを分ける
    categories = []
    tags = []
    for cat in item.find_all("category"):
        domain = cat.get("domain")
        if domain == "category":
            categories.append(cat.text.strip())
        elif domain == "post_tag":
            tags.append(cat.text.strip())

    # 投稿タイプが "post" のものだけを対象にする
    post_type = item.find("wp:post_type")
    if not post_type or post_type.text.strip() != "post":
        continue

    # Markdown Front Matter を構築
    post = frontmatter.Post(content)
    post["title"] = title
    post["date"] = date
    post["slug"] = slug
    if categories:
        post["categories"] = categories
    if tags:
        post["tags"] = tags

    # ファイル保存
    output_path = EXPORT_DIR / slug
    output_path.mkdir(exist_ok=True)
    with open(output_path / "index.md", "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))