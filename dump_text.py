import json, os, glob

os.makedirs("text", exist_ok=True)
for jf in glob.glob("extracted/*.json"):
    with open(jf, encoding="utf-8") as f:
        data = json.load(f)
    base = os.path.splitext(os.path.basename(jf))[0]
    out = os.path.join("text", base + ".txt")
    with open(out, "w", encoding="utf-8") as f:
        for p in data["pages"]:
            f.write(f"\n===== PAGE {p['page']} =====\n")
            f.write(p["text"].strip() + "\n")
    print(out, "written")
