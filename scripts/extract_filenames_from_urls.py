# scripts/extract_filenames_from_urls.py
with open("image_urls.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

filenames = []
for line in lines:
    line = line.strip()
    if line:
        name = line.split("/")[-1].split("?")[0].split("#")[0]
        filenames.append(name)

# 重複排除 & ソート
filenames = sorted(set(filenames))

# 保存
with open("image_filenames.txt", "w", encoding="utf-8") as f:
    for name in filenames:
        f.write(name + "\n")

print(f"{len(filenames)} 件の画像ファイル名を抽出しました -> image_filenames.txt")