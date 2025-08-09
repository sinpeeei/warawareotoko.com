import os
import re
import requests
from pathlib import Path

# postsディレクトリ
posts_dir = Path("content/posts")

# すべてのpost-****/index.mdを探索
for post_dir in posts_dir.iterdir():
    md_file = post_dir / "index.md"
    if md_file.exists():
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Markdownから画像URLを抽出（httpで始まり .jpg/.png/.jpeg で終わるもの）
        image_urls = re.findall(r"https?://[^\s)]+?\.(?:jpg|jpeg|png)", content, re.IGNORECASE)

        if image_urls:
            image_folder = post_dir / "images"
            image_folder.mkdir(exist_ok=True)

            for url in image_urls:
                filename = url.split("/")[-1]
                image_path = image_folder / filename

                if not image_path.exists():
                    try:
                        print(f"🔽 Downloading: {url}")
                        response = requests.get(url, timeout=10)
                        with open(image_path, "wb") as f:
                            f.write(response.content)
                    except Exception as e:
                        print(f"❌ Error downloading {url}: {e}")