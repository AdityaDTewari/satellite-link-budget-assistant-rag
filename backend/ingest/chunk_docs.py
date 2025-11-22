import json
from pathlib import Path
from tqdm import tqdm
from backend.utils.text_utils import split_text_simple

CHUNK_IN = Path(__file__).resolve().parents[1] / "chunks" / "docs"
CHUNK_OUT = Path(__file__).resolve().parents[1] / "chunks" / "doc_chunks"
CHUNK_OUT.mkdir(exist_ok=True)

def main():
    files = list(CHUNK_IN.glob("*.json"))
    chunk_manifest = []
    for f in tqdm(files):
        if "manifest" in f.name:
            continue
        doc = json.loads(f.read_text())
        text = doc.get("text", "")
        chunks = split_text_simple(text, max_tokens=300, overlap_tokens=50)
        for i, c in enumerate(chunks):
            chunk_meta = {
                "id": f"{f.stem}__{i}",
                "source": doc.get("source"),
                "chunk_index": i,
                "text": c
            }
            outp = CHUNK_OUT / f"{chunk_meta['id']}.json"
            outp.write_text(json.dumps(chunk_meta, ensure_ascii=False))
            chunk_manifest.append(chunk_meta)
        (CHUNK_OUT / "chunk_manifest.json").write_text(json.dumps(chunk_manifest, ensure_ascii=False))
    print(f"Created {len(chunk_manifest)} chunks in {CHUNK_OUT}")

if __name__ == "__main__":
    main()