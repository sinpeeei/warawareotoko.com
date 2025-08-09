import re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
POSTS = ROOT / "content" / "posts"

# ① 置換対象となる旧 URL パターン ── http / https 両対応
IMG_RE = re.compile(
    r"https?://(?:www\.)?warawareotoko\.com/wp-content/uploads/\d{4}/\d{2}/([^\"')]+?\.(?:jpe?g|png|gif))",
    flags=re.IGNORECASE,
)

def convert(match: re.Match) -> str:
    """マッチしたフル URL → images/ファイル名 へ置換"""
    filename = match.group(1).split("/")[-1]
    return f"images/{filename}"

def process_file(md_path: pathlib.Path):
    text = md_path.read_text(encoding="utf-8")
    new_text = IMG_RE.sub(convert, text)
    if new_text != text:
        md_path.write_text(new_text, encoding="utf-8")
        print(f"✔  updated {md_path.relative_to(ROOT)}")

for md in POSTS.rglob("index.md"):
    process_file(md)

print("✅  replace_image_links.py finished")