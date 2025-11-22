import faiss, json, numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from typing import List

EMB_DIR = Path(__file__).resolve().parents[1] / "embeddings"
VECT_DIR = Path(__file__).resolve().parents[1] / "vectordb"

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def load_index():
    index = faiss.read_index(str(VECT_DIR / "index.faiss"))
    with open(VECT_DIR / "ids.json") as fh:
        ids = json.load(fh)
    return index, ids

def retrieve(query: str, top_k: int = 4) -> List[dict]:
    q_emb = embed_model.encode([query], convert_to_numpy=True)
    q_emb = q_emb.astype("float32")
    faiss.normalize_L2(q_emb)
    index, ids = load_index()
    D, I = index.search(q_emb, top_k)
    results = []

    for score, idx in zip(D[0], I[0]):
        if idx < 0:
            continue
        chunk_id = ids[idx]

        chunk_file = Path(__file__).resolve().parents[1] / "chunks" / "doc_chunks" / f"{chunk_id}.json"

        if chunk_file.exists():
            j = json.loads(chunk_file.read_text())
            results.append({
                "id": chunk_id,
                "score": float(score),
                "text": j["text"],
                "source": j["source"]
            })
    
    return results

if __name__ == "__main__":
    query = "How to calculate free-space path loss at 12 GHz?"
    top_k = 3
    print(f"Testing retrieval for query:\n'{query}'\n")
    
    top_chunks = retrieve(query, top_k=top_k)
    
    if not top_chunks:
        print("No chunks retrieved. Check FAISS index and chunk files.")
    else:
        for r in top_chunks:
            print(f"ID: {r['id']}, Score: {r['score']:.3f}, Source: {r['source']}")
            print(f"Text snippet: {r['text'][:150]}...\n")