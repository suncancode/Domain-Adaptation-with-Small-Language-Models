"""
Unified LLM interface supporting two backends:

  1. Ollama  (default) — local model, no API key needed
     Install: https://ollama.com/download
     Then run: ollama pull llama3.2

  2. Anthropic Claude  — hosted API, higher quality
     Requires: pip install anthropic
     Requires: ANTHROPIC_API_KEY environment variable

Backend is controlled by LLM_BACKEND in config.py, or by setting
the environment variable LLM_BACKEND=ollama / LLM_BACKEND=anthropic.

Usage:
    from llm import generate

    answer = generate(system_prompt="You are...", user_prompt="Question...")
"""

from __future__ import annotations

import os
from config import (
    LLM_BACKEND,
    OLLAMA_MODEL,
    OLLAMA_BASE_URL,
    ANTHROPIC_MODEL,
)


# ---------------------------------------------------------------------------
# Ollama backend
# ---------------------------------------------------------------------------

def _generate_ollama(system_prompt: str, user_prompt: str) -> str:
    """
    Call a locally running Ollama model.

    Requires Ollama to be running: https://ollama.com/download
    Requires the model to be pulled: ollama pull llama3.2
    """
    try:
        import requests
    except ImportError:
        raise ImportError("requests is required: pip install requests")

    url = f"{OLLAMA_BASE_URL}/api/chat"

    payload = {
        "model": OLLAMA_MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        return (
            "[ERROR] Cannot connect to Ollama.\n"
            "Make sure Ollama is running:\n"
            "  1. Download from https://ollama.com/download\n"
            "  2. Install and start Ollama\n"
            f"  3. Run: ollama pull {OLLAMA_MODEL}\n"
            "  4. Try again."
        )
    except requests.exceptions.Timeout:
        return "[ERROR] Ollama request timed out. The model may still be loading — try again."
    except Exception as e:
        return f"[ERROR] Ollama error: {e}"


# ---------------------------------------------------------------------------
# Anthropic backend
# ---------------------------------------------------------------------------

def _generate_anthropic(system_prompt: str, user_prompt: str) -> str:
    """
    Call the Claude API via the Anthropic SDK.

    Requires: pip install anthropic
    Requires: ANTHROPIC_API_KEY environment variable set.
    """
    try:
        import anthropic
    except ImportError:
        raise ImportError("anthropic is required: pip install anthropic")

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return (
            "[ERROR] ANTHROPIC_API_KEY not set.\n"
            "PowerShell:  $env:ANTHROPIC_API_KEY = 'sk-ant-...'\n"
            "cmd.exe:     set ANTHROPIC_API_KEY=sk-ant-...\n"
            "Or create a .env file with: ANTHROPIC_API_KEY=sk-ant-..."
        )

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


# ---------------------------------------------------------------------------
# Public interface — call this everywhere
# ---------------------------------------------------------------------------

def generate(system_prompt: str, user_prompt: str) -> str:
    """
    Generate a response using the configured LLM backend.

    Backend is set by LLM_BACKEND in config.py:
        "ollama"     — local Ollama model (default)
        "anthropic"  — Claude API

    Args:
        system_prompt: instructions for the model
        user_prompt:   the actual question / context

    Returns:
        Generated text string.
    """
    backend = LLM_BACKEND.strip().lower()

    if backend == "anthropic":
        return _generate_anthropic(system_prompt, user_prompt)
    elif backend == "ollama":
        return _generate_ollama(system_prompt, user_prompt)
    else:
        return (
            f"[ERROR] Unknown LLM_BACKEND: '{backend}'\n"
            "Valid options: 'ollama' or 'anthropic'\n"
            "Check config.py or set the LLM_BACKEND environment variable."
        )


def get_backend_info() -> str:
    """Return a human-readable string describing the active backend."""
    backend = LLM_BACKEND.strip().lower()
    if backend == "ollama":
        return f"Ollama (local) — model: {OLLAMA_MODEL}"
    elif backend == "anthropic":
        return f"Anthropic Claude — model: {ANTHROPIC_MODEL}"
    return f"Unknown backend: {backend}"
