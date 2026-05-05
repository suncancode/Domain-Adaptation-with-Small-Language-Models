"""
Data loading utilities for the Shakespeare RAG system.

Supports two loading strategies:
  1. load_all_plays()       — loads from the main JSON files (scenes + utterances nested)
  2. load_scene_chunks()    — loads from pre-built *_scene_chunks.jsonl files (recommended)

The scene_chunks JSONL files are flat, one record per scene, and are the
primary source used for RAG retrieval.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from config import DATA_DIR, PLAY_FILES


Record = Dict[str, Any]

# Paths to the pre-built scene-level JSONL files
SCENE_CHUNK_FILES = {
    "hamlet":          DATA_DIR / "hamlet_scene_chunks.jsonl",
    "macbeth":         DATA_DIR / "macbeth_scene_chunks.jsonl",
    "romeo_and_juliet": DATA_DIR / "romeo_and_juliet_scene_chunks.jsonl",
}

UTTERANCE_FILES = {
    "hamlet":          DATA_DIR / "hamlet_utterances.jsonl",
    "macbeth":         DATA_DIR / "macbeth_utterances.jsonl",
    "romeo_and_juliet": DATA_DIR / "romeo_and_juliet_utterances.jsonl",
}


# ---------------------------------------------------------------------------
# Strategy 1 — load from main JSON (scenes nested inside each file)
# ---------------------------------------------------------------------------

def _extract_scenes(obj: Any) -> List[Record]:
    """Extract scene-level records from a JSON object."""
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for key in ["scenes", "records", "data"]:
            if key in obj and isinstance(obj[key], list):
                return obj[key]
    raise ValueError(
        "Could not extract scene records. Expected a list or a dict with a 'scenes' key."
    )


def load_json_scenes(path: Path) -> List[Record]:
    """Load scene-level records from one main JSON play file."""
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {path}\n"
            "Make sure the JSON files are placed in data/processed/."
        )
    with path.open("r", encoding="utf-8") as f:
        obj = json.load(f)
    return _extract_scenes(obj)


def load_all_plays() -> List[Record]:
    """
    Load scene-level records from all three compulsory plays (via main JSON files).
    Each record is one scene with nested utterances.
    """
    all_records: List[Record] = []
    for play_key, path in PLAY_FILES.items():
        scenes = load_json_scenes(path)
        for s in scenes:
            s.setdefault("play_key", play_key)
        all_records.extend(scenes)
        print(f"  Loaded {len(scenes):>3} scenes  ←  {play_key}")
    print(f"  Total: {len(all_records)} scenes across 3 plays\n")
    return all_records


# ---------------------------------------------------------------------------
# Strategy 2 — load from pre-built scene_chunks JSONL (recommended for RAG)
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> List[Record]:
    """Load every line of a JSONL file as a list of dicts."""
    if not path.exists():
        raise FileNotFoundError(
            f"JSONL file not found: {path}\n"
            "Make sure the *_scene_chunks.jsonl files are placed in data/processed/."
        )
    records = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def load_scene_chunks() -> List[Record]:
    """
    Load pre-built scene-level chunks from JSONL files.

    Each record has:
        scene_id, play, act, scene, location,
        scene_summary, keywords, text

    This is the recommended source for RAG retrieval.
    """
    all_chunks: List[Record] = []
    for play_key, path in SCENE_CHUNK_FILES.items():
        records = load_jsonl(path)
        for r in records:
            r.setdefault("play_key", play_key)
        all_chunks.extend(records)
        print(f"  Loaded {len(records):>3} scene chunks  ←  {play_key}")
    print(f"  Total: {len(all_chunks)} scene chunks across 3 plays\n")
    return all_chunks


def load_utterances() -> List[Record]:
    """
    Load utterance-level records from JSONL files.
    Useful for fine-grained retrieval or custom chunking experiments.
    """
    all_utterances: List[Record] = []
    for play_key, path in UTTERANCE_FILES.items():
        records = load_jsonl(path)
        for r in records:
            r.setdefault("play_key", play_key)
        all_utterances.extend(records)
        print(f"  Loaded {len(records):>4} utterances  ←  {play_key}")
    print(f"  Total: {len(all_utterances)} utterances across 3 plays\n")
    return all_utterances


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== Strategy 1: load from main JSON ===")
    scenes = load_all_plays()
    print("First scene keys:", list(scenes[0].keys()))

    print("\n=== Strategy 2: load scene chunks from JSONL ===")
    chunks = load_scene_chunks()
    print("First chunk keys:", list(chunks[0].keys()))
    print("Sample scene_summary:", chunks[0].get("scene_summary", ""))