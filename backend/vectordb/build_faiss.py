import faiss
import numpy as np
import json
from pathlib import Path

EMB_DIR = Path(__file__).resolve().parents[1] / "embeddings"
OUT_DIR = Path(__file__).resolve().parents[1] / "vectordb"
OUT_DIR.mkdir(exist_ok=True)

def main():
    emb = np.load(EMB_DIR / "embeddings.npy")
    ids = json.loads((EMB_DIR / "ids.json").read_text())
    d = emb.shape[1]
    index = faiss.IndexFlatIP(d)
    faiss.normalize_L2(emb)
    index.add(emb)
    faiss.write_index(index, str(OUT_DIR / "index.faiss"))
    with open(OUT_DIR / "ids.json", "w") as fh:
        json.dump(ids, fh)
    print(f"Build FAISS index with {index.ntotal} vectors")

if __name__ == "__main__":
    main()