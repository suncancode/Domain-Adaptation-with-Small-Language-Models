"""
Shakespeare-aware RAG chatbot.

Connects the retrieval pipeline to the Claude API (claude-haiku-4-5-20251001)
for answer generation. Supports two modes:

  1. Standard QA       — beginner-friendly explanation grounded in retrieved scenes
  2. Stylised response — short Shakespearean-style creative output (<=150 words)
                         clearly labelled as creative, not evidence

Usage:
    python src/rag_chatbot.py

Requires:
    pip install anthropic sentence-transformers scikit-learn numpy
    Set environment variable: ANTHROPIC_API_KEY=sk-ant-...
"""

from __future__ import annotations

import os
import re
from typing import Any, Dict, List, Tuple

from config import DEFAULT_TOP_K, EMBEDDING_MODEL_NAME, PROMPT_DIR
from chunking import create_chunks, format_chunk_for_display
from data_loader import load_scene_chunks
from retrieval import EmbeddingRetriever
from llm import generate, get_backend_info

Chunk = Dict[str, Any]


# ---------------------------------------------------------------------------
# Detect stylised generation requests
# ---------------------------------------------------------------------------

STYLE_KEYWORDS = [
    "shakespearean", "shakespeare style", "in the style of",
    "write as", "respond as", "speak as", "iambic", "thee", "thou",
    "hath", "doth", "stylised", "stylized", "creative", "poetic",
    "generate a", "write a short",
]


def _is_stylised_request(query: str) -> bool:
    """Return True if the query is asking for a Shakespearean-style response."""
    q = query.lower()
    return any(kw in q for kw in STYLE_KEYWORDS)


# ---------------------------------------------------------------------------
# Prompt builders
# ---------------------------------------------------------------------------

def _load_system_prompt() -> str:
    path = PROMPT_DIR / "system_prompt.txt"
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    # Fallback if file not found
    return (
        "You are a Shakespeare-aware assistant. "
        "Use the retrieved context to answer beginner-friendly questions. "
        "Do not invent unsupported details. "
        "If context is insufficient, say so clearly."
    )


def build_rag_prompt(query: str, retrieved: List[Tuple[Chunk, float]]) -> str:
    """Build a standard QA prompt with retrieved context."""
    context_blocks = []
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        context_blocks.append(
            f"[Context {rank} | similarity={score:.4f}]\n"
            f"{format_chunk_for_display(chunk)}"
        )
    context = "\n\n".join(context_blocks)

    return (
        f"Retrieved context:\n{context}\n\n"
        f"User question:\n{query}\n\n"
        f"Answer:"
    )


def build_stylised_prompt(query: str, retrieved: List[Tuple[Chunk, float]]) -> str:
    """
    Build a prompt specifically for Shakespearean-style creative generation.
    Instructs the model to stay under 150 words and label the output clearly.
    """
    context_blocks = []
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        context_blocks.append(
            f"[Context {rank}]\n{format_chunk_for_display(chunk)}"
        )
    context = "\n\n".join(context_blocks)

    return (
        f"Retrieved context (for thematic grounding only):\n{context}\n\n"
        f"User request:\n{query}\n\n"
        "Instructions:\n"
        "- Write a short creative response in Shakespearean style (thee, thou, hath, doth, etc.).\n"
        "- Keep it under 150 words.\n"
        "- Begin your response with: [CREATIVE — Shakespearean style, not textual evidence]\n"
        "- After the creative response, add a brief plain-English explanation of what it means.\n\n"
        "Response:"
    )


# ---------------------------------------------------------------------------
# Claude API call
# ---------------------------------------------------------------------------

def generate_answer(system_prompt: str, user_prompt: str) -> str:
    """
    Generate an answer using the configured LLM backend (Ollama or Anthropic).
    Backend is set in config.py via LLM_BACKEND.
    """
    return generate(system_prompt, user_prompt)


# ---------------------------------------------------------------------------
# Main chatbot loop
# ---------------------------------------------------------------------------

def answer_question(
    query: str,
    retriever: EmbeddingRetriever,
    top_k: int = DEFAULT_TOP_K,
    verbose: bool = True,
) -> Dict[str, Any]:
    """
    Full RAG pipeline for one question.

    Returns a dict with:
        query, retrieved_chunks, prompt, answer, is_stylised
    """
    system_prompt = _load_system_prompt()
    is_stylised   = _is_stylised_request(query)

    # Retrieve top-k relevant scenes
    retrieved = retriever.retrieve(query, top_k=top_k)

    # Build appropriate prompt
    if is_stylised:
        user_prompt = build_stylised_prompt(query, retrieved)
    else:
        user_prompt = build_rag_prompt(query, retrieved)

    # Generate answer
    answer = generate_answer(system_prompt, user_prompt)

    if verbose:
        print("\n" + "=" * 70)
        print(f"Question: {query}")
        print("=" * 70)

        print("\n--- Retrieved Evidence ---")
        for rank, (chunk, score) in enumerate(retrieved, start=1):
            print(f"\nRank {rank} | Score: {score:.4f}")
            print(format_chunk_for_display(chunk))

        print("\n--- Generated Answer ---")
        print(answer)
        print()

    return {
        "query":            query,
        "retrieved_chunks": retrieved,
        "user_prompt":      user_prompt,
        "answer":           answer,
        "is_stylised":      is_stylised,
    }


def main() -> None:
    print("=" * 70)
    print("Shakespeare-aware RAG Chatbot")
    print(f"LLM Backend: {get_backend_info()}")
    print("=" * 70)
    print("Type 'quit' to exit.")
    print("Tip: Add 'in Shakespearean style' to get a stylised response.\n")

    # Load or build index
    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME)
    if retriever.index_exists():
        print("Loading saved index...")
        retriever.load_index()
    else:
        print("No saved index found. Building from scratch...")
        records = load_scene_chunks()
        chunks  = create_chunks(records, strategy="scene")
        retriever.build_index(chunks)

    print("\nReady. Ask any question about Hamlet, Macbeth, or Romeo and Juliet.\n")

    while True:
        try:
            query = input("Question: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query:
            continue
        if query.lower() in {"quit", "exit", "q"}:
            break

        answer_question(query, retriever)


if __name__ == "__main__":
    main()