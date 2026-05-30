import fitz  # PyMuPDF
import os
import json

pdf_files = [
    "2026TCCC指南.pdf",
    "2.Prolonged Casualty Care Guidelines.pdf",
    "3.Damage Control Resuscitation.pdf",
    "ATP 4-02.11 2026年4月《伤员响应、战术战斗伤员护理与急救》.pdf",
]

os.makedirs("extracted", exist_ok=True)

summary = {}
for pdf in pdf_files:
    doc = fitz.open(pdf)
    n = doc.page_count
    pages = []
    total_chars = 0
    for i in range(n):
        text = doc[i].get_text("text")
        pages.append({"page": i + 1, "text": text})
        total_chars += len(text)
    base = os.path.splitext(os.path.basename(pdf))[0]
    out = os.path.join("extracted", base + ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"file": pdf, "page_count": n, "pages": pages}, f, ensure_ascii=False, indent=1)
    summary[pdf] = {"pages": n, "total_chars": total_chars, "avg_chars_per_page": total_chars // max(n, 1)}
    print(f"{pdf}: {n} pages, {total_chars} chars")
    doc.close()

print("\n=== SUMMARY ===")
print(json.dumps(summary, ensure_ascii=False, indent=2))
