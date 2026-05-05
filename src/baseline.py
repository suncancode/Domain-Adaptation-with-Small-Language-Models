"""
Baseline system for comparison with the RAG system.

Strategy: prompt-only generation WITHOUT retrieval.
The model answers using only its general knowledge — no Shakespeare text provided.

This is the standard academic baseline: it lets us measure how much the
RAG pipeline actually helps over a plain LLM call.

Comparison logic:
    Baseline  →  Claude API  +  NO retrieved context
    RAG       →  Claude API  +  retrieved scene passages

Any difference in output quality is attributable to retrieval.

Usage:
    python src/baseline.py
    python src/baseline.py --question "Who is Hamlet?"

Requires:
    pip install anthropic
    Set environment variable: ANTHROPIC_API_KEY=sk-ant-...
"""

from __future__ import annotations

import sys
from typing import Dict

from llm import generate, get_backend_info


# ---------------------------------------------------------------------------
# System prompt for baseline (same base instructions, but no context slot)
# ---------------------------------------------------------------------------

BASELINE_SYSTEM_PROMPT = """You are a Shakespeare-aware assistant.
Answer the user's question using your general knowledge of Shakespeare's plays.
Your answer must be beginner-friendly and easy to understand.
Do not invent details you are not confident about — if unsure, say so.
If asked to produce a Shakespearean-style response, keep it under 150 words
and make clear that it is creative output, not textual evidence."""


def build_baseline_prompt(query: str) -> str:
    """
    Prompt without any retrieved context.
    The model must rely entirely on its pretrained knowledge.
    """
    return (
        f"User question:\n{query}\n\n"
        "Answer (based on your knowledge of Shakespeare's plays):"
    )


# ---------------------------------------------------------------------------
# Claude API call (same function signature as rag_chatbot for easy comparison)
# ---------------------------------------------------------------------------

def generate_baseline_answer(query: str) -> str:
    """Generate an answer using only the LLM — no retrieval context."""
    return generate(BASELINE_SYSTEM_PROMPT, build_baseline_prompt(query))


# ---------------------------------------------------------------------------
# Run baseline on one question and return structured result
# ---------------------------------------------------------------------------

def answer_question_baseline(
    query: str,
    verbose: bool = True,
) -> Dict[str, str]:
    """
    Run the baseline (no retrieval) on one question.

    Returns a dict with: query, prompt, answer, system
    """
    user_prompt = build_baseline_prompt(query)
    answer      = generate_baseline_answer(query)

    if verbose:
        print("\n" + "=" * 70)
        print(f"[BASELINE] Question: {query}")
        print("=" * 70)
        print("(No retrieved context — model uses general knowledge only)")
        print("\n--- Baseline Answer ---")
        print(answer)
        print()

    return {
        "query":   query,
        "prompt":  user_prompt,
        "answer":  answer,
        "system":  "baseline",
    }


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------

def main() -> None:
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[2:]) if sys.argv[1] == "--question" else " ".join(sys.argv[1:])
    else:
        question = "Who is Hamlet?"

    print("=" * 70)
    print("Shakespeare Baseline System (no retrieval)")
    print(f"LLM Backend: {get_backend_info()}")
    print("=" * 70)

    answer_question_baseline(question)


if __name__ == "__main__":
    main()