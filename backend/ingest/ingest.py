import os
import json
from pathlib import Path
from PyPDF2 import PdfReader
from tqdm import tqdm

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
OUT_DIR = Path(__file__).resolve().parents[1] / "chunks" / "docs"
OUT_DIR.mkdir(exist_ok=True)

SUPPORTED = [".pdf", ".txt", ".md"]

def extract_text_from_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for p in reader.pages:
        text = p.extract_text()
        if text:
            pages.append(text)
    
    return "\n".join(pages)

def normalize_file(path: Path) -> dict:
    ext = path.suffix.lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    else:
        text = path.read_text(encoding="utf-8", errors="ignore")
    
    return {
        "source": str(path.name),
        "text": text
    }

def main():
    manifest = []
    for file in tqdm(list(DATA_DIR.iterdir())):
        if file.suffix.lower() not in SUPPORTED:
            continue
        doc = normalize_file(file)
        target = OUT_DIR / f"{file.stem}.json"
        target.write_text(json.dumps(doc, ensure_ascii=False))
        manifest.append({
            "source": file.name,
            "out": str(target)
        })
    
    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Normalized {len(manifest)} files -> {OUT_DIR}")

if __name__ == "__main__":
    main()