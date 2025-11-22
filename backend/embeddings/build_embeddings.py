import json
from pathlib import Path
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np

CHUNKS_DIR = Path(__file__).resolve().parents[1] / "chunks" / "doc_chunks"
OUT_DIR = Path(__file__).resolve().parents[1] / "embeddings"
OUT_DIR.mkdir(exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

def main():
    chunk_files = [p for p in CHUNKS_DIR.glob("*.json") if "manifest" not in p.name]
    texts = []
    ids = []
    metas = []
    for f in tqdm(chunk_files):
        j = json.loads(f.read_text())
        texts.append(j["text"])
        ids.append(j["id"])
        metas.append({
            "id": j["id"],
            "source": j["source"],
            "chunk_index": j["chunk_index"]
        })
    
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    np.save(OUT_DIR / "embeddings.npy", embeddings)
    with open(OUT_DIR / "ids.json", 'w') as fh:
        json.dump(ids, fh)
    with open(OUT_DIR / "meta.json", "w") as fh:
        json.dump(metas, fh, ensure_ascii=False)
    print(f"Saced embeddings for {len(ids)} chunks")

if __name__ == "__main__":
    main()
