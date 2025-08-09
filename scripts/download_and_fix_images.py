import os
import re
import requests
from urllib.parse import urlparse

content_root = "content/posts"

def download_image(img_url, save_path):
    try:
        r = requests.get(img_url, timeout=10)
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(r.content)
        print(f"[OK] ダウンロード: {img_url} → {save_path}")
    except Exception as e:
        print(f"[NG] 失敗: {img_url} → {e}")

def process_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    img_urls = re.findall(r'!\[.*?\]\((https://[^\)]+)\)', content)
    if not img_urls:
        return

    post_dir = os.path.dirname(md_path)
    images_dir = os.path.join(post_dir, "images")
    os.makedirs(images_dir, exist_ok=True)

    for url in img_urls:
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        local_path = os.path.join("images", filename)
        full_save_path = os.path.join(images_dir, filename)

        # 画像をダウンロード
        download_image(url, full_save_path)

        # Markdown の画像URLを置換
        content = content.replace(url, local_path)

    # 上書き保存
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[更新] {md_path}")

def walk_and_process(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file == "index.md":
                md_path = os.path.join(root, file)
                process_markdown(md_path)

if __name__ == "__main__":
    walk_and_process(content_root)