"""
Evaluation script — runs both baseline and RAG systems on all questions
and saves results to a CSV file for scoring.

Loads two question sets:
    results/instructor_questions.json   (5 questions, provided by instructor)
    results/group_questions.json        (5-10 questions, designed by your group)

Output:
    results/evaluation_results.csv      (one row per question × system)

Usage:
    python src/evaluate.py              # run all questions
    python src/evaluate.py --dry-run    # preview questions only, no API calls
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from config import EMBEDDING_MODEL_NAME, DEFAULT_TOP_K, RESULTS_DIR
from chunking import create_chunks
from data_loader import load_scene_chunks
from retrieval import EmbeddingRetriever
from baseline import answer_question_baseline
from rag_chatbot import answer_question


INSTRUCTOR_QUESTIONS_PATH = RESULTS_DIR / "instructor_questions.json"
GROUP_QUESTIONS_PATH      = RESULTS_DIR / "group_questions.json"
OUTPUT_PATH               = RESULTS_DIR / "evaluation_results.csv"

CSV_FIELDNAMES = [
    "question_id",
    "question",
    "question_type",
    "expected_focus",
    "question_source",          # "instructor" or "group"
    "system",                   # "baseline" or "rag"
    "retrieved_passages",
    "generated_response",
    "correctness_score",        # 1-5
    "grounding_score",          # 1-5
    "retrieval_relevance_score",# 1-5 (N/A for baseline)
    "usefulness_score",         # 1-5
    "style_quality_score",      # 1-5 (stylised questions only, else N/A)
    "comments",
]


# ---------------------------------------------------------------------------
# Load questions
# ---------------------------------------------------------------------------

def load_questions() -> List[Dict[str, str]]:
    """Load instructor + group questions. Group questions are optional."""
    questions = []

    # Instructor questions (required)
    if not INSTRUCTOR_QUESTIONS_PATH.exists():
        raise FileNotFoundError(
            f"Instructor questions not found: {INSTRUCTOR_QUESTIONS_PATH}"
        )
    with INSTRUCTOR_QUESTIONS_PATH.open("r", encoding="utf-8") as f:
        instructor_qs = json.load(f)
    for q in instructor_qs:
        q["source"] = "instructor"
    questions.extend(instructor_qs)
    print(f"  Loaded {len(instructor_qs)} instructor questions")

    # Group questions (optional but required for full marks)
    if GROUP_QUESTIONS_PATH.exists():
        with GROUP_QUESTIONS_PATH.open("r", encoding="utf-8") as f:
            group_qs = json.load(f)
        for q in group_qs:
            q["source"] = "group"
        questions.extend(group_qs)
        print(f"  Loaded {len(group_qs)} group questions")
    else:
        print(f"  [WARNING] Group questions not found: {GROUP_QUESTIONS_PATH}")
        print(f"  Create this file with 5-10 questions to meet assignment requirements.")

    print(f"  Total: {len(questions)} questions\n")
    return questions


# ---------------------------------------------------------------------------
# Format retrieved passages for CSV
# ---------------------------------------------------------------------------

def _format_retrieved_for_csv(retrieved: List) -> str:
    lines = []
    for rank, (chunk, score) in enumerate(retrieved, start=1):
        play    = chunk.get("play", "?")
        act     = chunk.get("act", "?")
        scene   = chunk.get("scene", "?")
        speaker = chunk.get("speaker", "")
        summary = chunk.get("scene_summary", "")[:80]
        info    = f"{play} Act {act} Sc {scene}"
        if speaker:
            info += f" [{speaker}]"
        lines.append(f"[{rank}] {info} (score={score:.4f}) — {summary}")
    return " | ".join(lines)


# ---------------------------------------------------------------------------
# Run one question through both systems
# ---------------------------------------------------------------------------

def evaluate_question(
    question: Dict[str, str],
    retriever: EmbeddingRetriever,
    top_k: int = DEFAULT_TOP_K,
) -> List[Dict[str, Any]]:
    qid      = question.get("question_id", "")
    qtext    = question.get("question", "")
    qtype    = question.get("type", "")
    expected = question.get("expected_focus", "")
    source   = question.get("source", "instructor")
    is_style = qtype == "stylised_generation"

    rows = []

    # --- Baseline (no retrieval) ---
    print(f"    Running BASELINE...")
    b = answer_question_baseline(qtext, verbose=False)
    rows.append({
        "question_id":               qid,
        "question":                  qtext,
        "question_type":             qtype,
        "expected_focus":            expected,
        "question_source":           source,
        "system":                    "baseline",
        "retrieved_passages":        "N/A",
        "generated_response":        b["answer"],
        "correctness_score":         "",
        "grounding_score":           "N/A",
        "retrieval_relevance_score": "N/A",
        "usefulness_score":          "",
        "style_quality_score":       "" if is_style else "N/A",
        "comments":                  "",
    })

    # --- RAG (with retrieval) ---
    print(f"    Running RAG...")
    r = answer_question(qtext, retriever, top_k=top_k, verbose=False)
    rows.append({
        "question_id":               qid,
        "question":                  qtext,
        "question_type":             qtype,
        "expected_focus":            expected,
        "question_source":           source,
        "system":                    "rag",
        "retrieved_passages":        _format_retrieved_for_csv(r["retrieved_chunks"]),
        "generated_response":        r["answer"],
        "correctness_score":         "",
        "grounding_score":           "",
        "retrieval_relevance_score": "",
        "usefulness_score":          "",
        "style_quality_score":       "" if is_style else "N/A",
        "comments":                  "",
    })

    return rows


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_evaluation(dry_run: bool = False) -> None:
    print("=" * 70)
    print("Shakespeare RAG — Evaluation")
    print("=" * 70)
    print()

    questions = load_questions()

    if dry_run:
        print("[DRY RUN] Questions only, no API calls:\n")
        for q in questions:
            src = q.get("source", "?")
            print(f"  [{q['question_id']}] ({src}) [{q.get('type','?')}]")
            print(f"    {q['question']}")
        print(f"\nTotal: {len(questions)} questions × 2 systems = {len(questions)*2} rows")
        return

    # Load scene-level retriever
    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME, strategy="scene")
    if retriever.index_exists():
        print("Loading saved index...")
        retriever.load_index()
    else:
        print("Building index from scratch...")
        records = load_scene_chunks()
        chunks  = create_chunks(records, strategy="scene")
        retriever.build_index(chunks)

    # Run all questions
    all_rows: List[Dict[str, Any]] = []
    total = len(questions)
    print(f"\nRunning {total} questions × 2 systems = {total*2} LLM calls...\n")

    for i, question in enumerate(questions, start=1):
        qid   = question.get("question_id", "?")
        qtext = question.get("question", "")[:55]
        src   = question.get("source", "?")
        print(f"[{i}/{total}] {qid} ({src}) — {qtext}")
        rows = evaluate_question(question, retriever)
        all_rows.extend(rows)

    # Save CSV
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\n{'='*70}")
    print(f"Results saved to: {OUTPUT_PATH}")
    print(f"Total rows: {len(all_rows)} ({total} questions × 2 systems)")
    print()
    print("Next step: open evaluation_results.csv and fill in scores (1-5).")
    print()
    print("Scoring guide:")
    print("  correctness_score         1=wrong  3=partial  5=fully correct")
    print("  grounding_score           1=no evidence cited  5=well grounded")
    print("  retrieval_relevance_score 1=irrelevant  5=highly relevant")
    print("  usefulness_score          1=confusing  5=very helpful for beginner")
    print("  style_quality_score       1=not Shakespearean  5=excellent style")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run_evaluation(dry_run=dry_run)