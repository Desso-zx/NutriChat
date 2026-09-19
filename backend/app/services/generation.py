import ollama

from app.core.config import settings


def build_prompt(query: str, retrieved_chunks) -> str:
    """Assemble a context block with source labels + the instruction prompt."""
    context_blocks = []
    for i, (chunk, metadata, _distance) in enumerate(retrieved_chunks):
        source = metadata.get("source", "Unknown Source")
        context_blocks.append(f"[Source {i}: {source}]\n{chunk}")
    context_text = "\n\n".join(context_blocks)

    prompt = f"""You are NutriChat, a nutrition assistant. Answer the question using ONLY the context below.

Rules:
- If the context does not contain the answer, say "I don't have enough information in my sources to answer that." Do not guess or use outside knowledge.
- When you use a fact, cite it with the source label it came from, e.g. (Source 1).
- Be concise and direct.

Context:
{context_text}

Question: {query}

Answer:"""
    return prompt


def generate_answer(query: str, retrieved_chunks) -> dict:
    """Full generation step: build prompt -> call Ollama -> return answer + sources."""
    prompt = build_prompt(query, retrieved_chunks)

    response = ollama.chat(
        model=settings.llm_model,
        messages=[{"role": "user", "content": prompt}],
    )
    answer = response["message"]["content"]
    sources = sorted({meta.get("source", "unknown") for _c, meta, _d in retrieved_chunks})

    return {"answer": answer, "sources": sources}