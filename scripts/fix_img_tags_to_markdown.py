import os
import re

POSTS_DIR = "../content/posts"

def extract_filename(url):
    filename = os.path.basename(url)
    # サムネイルサイズ（例: -576x1024）を除去
    return re.sub(r"-\d+x\d+(?=\.\w{3,4}$)", "", filename)

def convert_img_tag_to_markdown(content):
    # <img ... src="..."> をすべて抽出
    pattern = re.compile(r'<img[^>]*src="([^"]+)"[^>]*>', re.IGNORECASE)
    return pattern.sub(lambda m: f"![](images/{extract_filename(m.group(1))})", content)

def process_md_files():
    for root, _, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".md"):
                md_path = os.path.join(root, file)
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()

                new_content = convert_img_tag_to_markdown(content)

                if new_content != content:
                    with open(md_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"✅ 変換: {md_path}")
                else:
                    print(f"— 変更なし: {md_path}")

if __name__ == "__main__":
    process_md_files()