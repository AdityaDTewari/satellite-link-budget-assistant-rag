from .retriever import retrieve
from .model_runner import call_llm
import textwrap

SYSTEM_PROMPT = """
You are an assistant specialized in satellite link budget calculations and documentation.
You must answer concisely and cite the retrieved document IDs when using retrieved content.
If you cannot answer, say you don't know and provide steps to compute/estimate.
"""

PROMPT_TEMPLATE = """
{system_prompt}

Context (retrieved documents):
{context}

Question:
{question}

Instructions:
- Use the context above. Quote the document id(s) you used: [doc_id].
- If numerical calculation is needed, show the steps.
- Provide a short answer and then the calculation details (if any).
"""

def build_context_snippets(retrieved):
    lines = []
    for r in retrieved:
        excerpt = r["text"][:600].replace("\n", " ")
        lines.append(f"[{r['id']} | {r['source']}] (score=r['score']:.3f)\n{excerpt}\n")
    return "\n---\n".join(lines)

def answer_query(question: str, top_k: int=4) -> str:
    retrieved = retrieve(question, top_k=top_k)
    context = build_context_snippets(retrieved)
    prompt = PROMPT_TEMPLATE.format(
        system_prompt=SYSTEM_PROMPT.strip(),
        context=context,
        question=question
    )

    resp = call_llm(prompt)
    return resp

if __name__ == "__main__":
    print("=== RAG Runner Test ===\n")
    
    # Example query
    query = "How to compute free-space path loss at 12 GHz for GEO satellites?"
    top_k = 3
    
    print(f"Query: {query}\n")
    
    answer = answer_query(query, top_k=top_k)
    
    print("Answer from RAG system:\n")
    print(answer)