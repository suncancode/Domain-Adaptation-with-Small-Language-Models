"""
Configuration for the Shakespeare RAG system.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR     = PROJECT_ROOT / "data" / "processed"
INDEX_DIR    = PROJECT_ROOT / "data" / "index"
PROMPT_DIR   = PROJECT_ROOT / "prompts"
RESULTS_DIR  = PROJECT_ROOT / "results"

PLAY_FILES = {
    "hamlet":           DATA_DIR / "hamlet.json",
    "macbeth":          DATA_DIR / "macbeth.json",
    "romeo_and_juliet": DATA_DIR / "romeo_and_juliet.json",
}

DEFAULT_TOP_K = 3

# ---------------------------------------------------------------------------
# Embedding model
# Lightweight model that runs locally, no API key needed.
# ---------------------------------------------------------------------------
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------------------------------------------------------------
# LLM Backend
#
# "ollama"     — run a small model locally via Ollama (default, recommended)
#                No API key needed. Everyone on the team just needs to install
#                Ollama and run: ollama pull llama3.2
#
# "anthropic"  — use Claude API (requires ANTHROPIC_API_KEY env variable)
#                Useful for higher quality answers but needs a paid key.
#
# To switch:   change LLM_BACKEND below, or set env var:
#                set LLM_BACKEND=anthropic   (Windows cmd)
#                $env:LLM_BACKEND="anthropic" (PowerShell)
# ---------------------------------------------------------------------------
import os
LLM_BACKEND = os.environ.get("LLM_BACKEND", "ollama")   # "ollama" | "anthropic"

# Ollama settings
OLLAMA_MODEL   = "llama3.2"          # pull with: ollama pull llama3.2
OLLAMA_BASE_URL = "http://localhost:11434"

# Anthropic settings (only used when LLM_BACKEND="anthropic")
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"