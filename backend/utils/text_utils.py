import re
from typing import List

def split_text_simple(text: str, max_tokens=400, overlap_tokens=50) -> List[str]:
    words = text.split()
    max_w = max_tokens
    overlap = overlap_tokens
    chunks = []
    i = 0
    while i < len(words):
        chunks_words = words[i : i + max_w]
        chunks.append(" ".join(chunks_words))
        if i + max_w >= len(words):
            break
        i = i + max_w - overlap
    
    return chunks

