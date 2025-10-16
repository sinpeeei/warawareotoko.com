#!/usr/bin/env python3
import re, sys, pathlib, shutil

ROOT = pathlib.Path("content/posts")
DRY = "--dry-run" in sys.argv

def fix_text(txt):
    orig = txt
    txt = re.sub(r"<!--\s*\/?wp:[^>]*-->\s*", "", txt)
    txt = re.sub(r"<h([1-6])>.*?<b>(.*?)<\/b>.*?<\/h\1>",
                 lambda m: "\n" + "#"*int(m.group(1)) + " " + re.sub(r"\s+", " ", m.group(2)).strip() + "\n",
                 txt, flags=re.S|re.I)
    txt = re.sub(r"<h([1-6])>(.*?)<\/h\1>",
                 lambda m: "\n" + "#"*int(m.group(1)) + " " + re.sub(r"\s+", " ", m.group(2)).strip() + "\n",
                 txt, flags=re.S|re.I)
    txt = re.sub(r"(?:<br\s*\/?>\s*){2,}", "\n\n", txt, flags=re.I)
    return txt if txt != orig else None

changed = 0
for md in ROOT.rglob("index.md"):
    text = md.read_text(encoding="utf-8", errors="ignore")
    fixed = fix_text(text)
    if fixed is not None:
        if DRY:
            print(f"[would-fix] {md}")
        else:
            backup = pathlib.Path("_backup/hfix") / f"{md.parent.name}_index.md"
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(md, backup)
            md.write_text(fixed, encoding="utf-8")
            print(f"[fixed] {md}")
            changed += 1

if not DRY:
    print(f"\nDone. files_fixed={changed}")
