"""
Chunking utilities for the Shakespeare RAG system.

Two strategies are implemented:

  1. scene_chunks (default, recommended)
     One chunk per scene. The embedded text combines the scene_summary
     (modern English) with the original text. This bridges the gap between
     a user asking in plain English and Shakespeare's archaic language.

  2. utterance_chunks
     One chunk per speaker turn. Higher precision for specific quotes,
     but lower context per chunk. Useful for retrieval re-ranking experiments.

The 'enriched text' pattern (summary + original) is the key design decision:
  - scene_summary is modern English  → matches user queries well
  - original text is Shakespeare     → provides grounded evidence
  - combining both gives the best of both worlds for embedding
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

Record = Dict[str, Any]
Chunk  = Dict[str, Any]


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _clean_text(text: str) -> str:
    """Remove Project Gutenberg copyright notices."""
    markers = [
        "[SHAKESPEARE IS COPYRIGHT",
        "COMMERCIALLY. PROHIBITED",
        "WITH PERMISSION. ELECTRONIC",
    ]
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    return text.strip()

def _make_enriched_text(record: Record) -> str:
    """
    Combine scene_summary (modern English) and original text into one
    string for embedding. This improves retrieval because user questions
    are in plain English, not Shakespearean.

    Format:
        Summary: <scene_summary>
        Keywords: <kw1, kw2, ...>

        <original scene text>
    """
    parts: List[str] = []

    summary = record.get("scene_summary", "").strip()
    if summary:
        parts.append(f"Summary: {summary}")

    keywords = record.get("keywords", [])
    if keywords:
        parts.append(f"Keywords: {', '.join(keywords)}")

    if parts:
        parts.append("")          # blank line separator

    text = _clean_text(record.get("text", ""))
    if text:
        parts.append(text)

    return "\n".join(parts)


def _build_chunk_id(record: Record, index: int) -> str:
    """Generate a stable chunk ID from available fields."""
    return (
        record.get("scene_id")
        or record.get("utterance_id")
        or record.get("source_id")
        or f"chunk_{index:06d}"
    )


# ---------------------------------------------------------------------------
# Strategy 1 — Scene-level chunks (recommended)
# ---------------------------------------------------------------------------

def create_scene_chunks(records: List[Record]) -> List[Chunk]:
    """
    Convert scene-level records into retrieval chunks.

    Each chunk has:
        chunk_id    — unique identifier
        play        — play title
        act         — act number
        scene       — scene number
        location    — scene location string
        scene_summary — modern English summary (also in text)
        keywords    — list of thematic keywords
        text        — ENRICHED: summary + keywords + original text
        raw_text    — original scene text only (for display)
        metadata    — full original record
    """
    chunks: List[Chunk] = []

    for i, record in enumerate(records):
        enriched = _make_enriched_text(record)
        if not enriched.strip():
            continue

        chunk: Chunk = {
            "chunk_id":     _build_chunk_id(record, i),
            "play":         record.get("play", record.get("play_key", "Unknown")),
            "act":          record.get("act"),
            "scene":        record.get("scene"),
            "location":     record.get("location", ""),
            "scene_summary": record.get("scene_summary", ""),
            "keywords":     record.get("keywords", []),
            "text":         enriched,          # ← used for embedding
            "raw_text":     _clean_text(record.get("text", "")),  # ← used for display
            "metadata":     record,
        }
        chunks.append(chunk)

    return chunks


# ---------------------------------------------------------------------------
# Strategy 2 — Utterance-level chunks (fine-grained, optional)
# ---------------------------------------------------------------------------

def create_utterance_chunks(records: List[Record]) -> List[Chunk]:
    """
    Convert utterance-level records into retrieval chunks.

    Each chunk represents a single speaker turn.
    The scene_summary is prepended to aid retrieval.

    Skips STAGE_DIRECTION entries (not useful for QA).
    """
    chunks: List[Chunk] = []

    for i, record in enumerate(records):
        speaker = record.get("speaker", "")
        if speaker == "STAGE_DIRECTION":
            continue

        text = _clean_text(record.get("text", "")).strip()
        if not text:
            continue

        summary = record.get("scene_summary", "").strip()
        enriched = f"Summary: {summary}\n\n{speaker}: {text}" if summary else f"{speaker}: {text}"

        chunk: Chunk = {
            "chunk_id":     _build_chunk_id(record, i),
            "play":         record.get("play", record.get("play_key", "Unknown")),
            "act":          record.get("act"),
            "scene":        record.get("scene"),
            "location":     record.get("location", ""),
            "speaker":      speaker,
            "scene_summary": summary,
            "keywords":     record.get("keywords", []),
            "text":         enriched,
            "raw_text":     f"{speaker}: {text}",
            "metadata":     record,
        }
        chunks.append(chunk)

    return chunks


# ---------------------------------------------------------------------------
# Default entry point (used by build_index and rag_chatbot)
# ---------------------------------------------------------------------------

def create_chunks(records: List[Record], strategy: str = "scene") -> List[Chunk]:
    """
    Create retrieval chunks from records.

    Args:
        records:  list of scene or utterance records
        strategy: "scene" (default) or "utterance"

    Returns:
        List of chunk dicts ready for embedding.
    """
    if strategy == "utterance":
        return create_utterance_chunks(records)
    return create_scene_chunks(records)


# ---------------------------------------------------------------------------
# Display helper
# ---------------------------------------------------------------------------

def format_chunk_for_display(chunk: Chunk) -> str:
    """
    Format a retrieved chunk for display to the user.
    Shows provenance metadata and the original (non-enriched) text.
    """
    play    = chunk.get("play", "Unknown play")
    act     = chunk.get("act", "?")
    scene   = chunk.get("scene", "?")
    loc     = chunk.get("location", "")
    speaker = chunk.get("speaker", "")
    summary = chunk.get("scene_summary", "")

    # Build header line
    header = f"{play} | Act {act}, Scene {scene}"
    if loc:
        header += f" | {loc}"
    if speaker:
        header += f" | Speaker: {speaker}"

    lines = [f"[{header}]"]

    if summary:
        lines.append(f"Scene summary: {summary}")

    lines.append("")
    lines.append(chunk.get("raw_text", chunk.get("text", "")))

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from data_loader import load_scene_chunks, load_utterances

    print("=== Scene-level chunks ===")
    scene_records = load_scene_chunks()
    scene_chunks = create_chunks(scene_records, strategy="scene")
    print(f"Created {len(scene_chunks)} scene chunks")
    print("\nSample chunk text (first 400 chars):")
    print(scene_chunks[0]["text"][:400])
    print("\nFormatted display:")
    print(format_chunk_for_display(scene_chunks[0]))

    print("\n=== Utterance-level chunks ===")
    utt_records = load_utterances()
    utt_chunks = create_chunks(utt_records, strategy="utterance")
    print(f"Created {len(utt_chunks)} utterance chunks")