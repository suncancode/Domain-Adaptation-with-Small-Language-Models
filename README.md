# Shakespeare-Aware RAG System
## CSCI433/933 Assignment 2 — Domain Adaptation with Small Language Models

A Retrieval-Augmented Generation (RAG) system that enables beginners to ask
questions about Shakespeare's *Hamlet*, *Macbeth*, and *Romeo and Juliet*.
The system retrieves relevant scene passages and generates beginner-friendly
answers using a local language model (Ollama) or the Claude API.

---

## Repository Structure

```
project-root/
│
├── data/
│   ├── processed/                  ← Shakespeare source data (commit these)
│   │   ├── hamlet.json
│   │   ├── macbeth.json
│   │   ├── romeo_and_juliet.json
│   │   ├── hamlet_scene_chunks.jsonl
│   │   ├── hamlet_utterances.jsonl
│   │   ├── macbeth_scene_chunks.jsonl
│   │   ├── macbeth_utterances.jsonl
│   │   ├── romeo_and_juliet_scene_chunks.jsonl
│   │   └── romeo_and_juliet_utterances.jsonl
│   │
│   └── index/                      ← Generated indexes (DO NOT commit)
│       ├── scene/
│       │   ├── embeddings.npy
│       │   └── chunks.json
│       └── utterance/
│           ├── embeddings.npy
│           └── chunks.json
│
├── src/
│   ├── config.py           ← Paths, model names, LLM backend setting
│   ├── data_loader.py      ← Load JSON / JSONL data files
│   ├── chunking.py         ← Convert records into retrieval chunks
│   ├── retrieval.py        ← Embed chunks, save/load index, cosine search
│   ├── llm.py              ← Unified LLM interface (Ollama / Anthropic)
│   ├── build_index.py      ← One-time script to build both indexes
│   ├── rag_chatbot.py      ← Full RAG pipeline + interactive chat
│   ├── baseline.py         ← Baseline system (no retrieval)
│   └── evaluate.py         ← Run evaluation and save CSV
│
├── prompts/
│   └── system_prompt.txt   ← Instructions given to the LLM
│
├── results/
│   ├── instructor_questions.json   ← 5 questions provided by instructor
│   ├── group_questions.json        ← 10 questions designed by group
│   └── evaluation_results.csv      ← Generated (DO NOT commit)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## File Descriptions

### `src/config.py`
Central configuration. Edit this file to change:
- `LLM_BACKEND`: `"ollama"` (default, local) or `"anthropic"` (Claude API)
- `OLLAMA_MODEL`: which Ollama model to use (default `"llama3.2"`)
- `EMBEDDING_MODEL_NAME`: sentence-transformers model for embeddings

### `src/data_loader.py`
Loads Shakespeare data from disk. Two strategies:
- `load_scene_chunks()` — loads from `*_scene_chunks.jsonl` (73 records total)
- `load_utterances()` — loads from `*_utterances.jsonl` (3613 records total)

### `src/chunking.py`
Converts raw records into retrieval-ready chunks. Key design decision:
enriched text = `scene_summary` (modern English) + `keywords` + original text.
This bridges the vocabulary gap between plain-English user queries and
Shakespearean language.

Two strategies:
- `create_scene_chunks()` — one chunk per scene (73 chunks)
- `create_utterance_chunks()` — one chunk per speaker turn (2690 chunks)

### `src/retrieval.py`
Handles embedding and similarity search.
- Embeds chunks using `sentence-transformers/all-MiniLM-L6-v2`
- Saves index to `data/index/<strategy>/` so re-embedding is not needed
- Retrieves top-k chunks using cosine similarity

### `src/llm.py`
Unified interface for language model generation. Supports:
- **Ollama** (default): calls local model at `http://localhost:11434`
- **Anthropic**: calls Claude API (requires `ANTHROPIC_API_KEY`)

### `src/build_index.py`
One-time setup script. Builds and saves both indexes:
- `data/index/scene/` — 73 scene-level chunks
- `data/index/utterance/` — 2690 utterance-level chunks

### `src/rag_chatbot.py`
Main RAG pipeline. For each user question:
1. Retrieves top-3 relevant scenes from index
2. Builds a prompt combining context + question
3. Generates answer via LLM
4. Detects stylised generation requests automatically

### `src/baseline.py`
Baseline system for comparison. Calls the same LLM with the same question
but **without** any retrieved context. Used to measure how much RAG helps.

### `src/evaluate.py`
Runs both systems (baseline + RAG) on all evaluation questions and saves
results to `results/evaluation_results.csv` for manual scoring.

---

## Installation

### Step 1 — Clone the repository

```bash
git clone <repo-url>
cd <project-folder>
```

### Step 2 — Install Python dependencies

```bash
pip install sentence-transformers scikit-learn numpy requests
```

Optional (only if using Anthropic backend):
```bash
pip install anthropic
```

### Step 3 — Install Ollama (local LLM)

1. Download from **https://ollama.com/download** and install
2. Pull the language model (~2GB, one-time download):

```bash
ollama pull llama3.2
```

3. Verify Ollama is running:

```bash
ollama list
# Should show: llama3.2:latest
```

### Step 4 — Verify data files

Make sure all 9 data files are in `data/processed/`:

```
hamlet.json
macbeth.json
romeo_and_juliet.json
hamlet_scene_chunks.jsonl
hamlet_utterances.jsonl
macbeth_scene_chunks.jsonl
macbeth_utterances.jsonl
romeo_and_juliet_scene_chunks.jsonl
romeo_and_juliet_utterances.jsonl
```

---

## Running the System

### Step 1 — Build the index (run once)

Embeds all chunks and saves indexes to `data/index/`.
Must be run before using the chatbot or evaluation.

```bash
python src/build_index.py
```

Expected output:
```
Building SCENE-LEVEL index
  Loaded 73 scene chunks across 3 plays
  Embedding shape: (73, 384)
  Index saved [scene]: data/index/scene/

Building UTTERANCE-LEVEL index
  Loaded 2690 utterance chunks across 3 plays
  Embedding shape: (2690, 384)
  Index saved [utterance]: data/index/utterance/
```

To build only one strategy:
```bash
python src/build_index.py --scene       # scene only (~10 seconds)
python src/build_index.py --utterance   # utterance only (~1 minute)
```

---

### Step 2 — Run the chatbot

Interactive question-answering with retrieved evidence.

```bash
python src/rag_chatbot.py
```

Example session:
```
Question: Why does Macbeth kill Duncan?

--- Retrieved Evidence ---
Rank 1 | Score: 0.7292
[Macbeth | Act 2, Scene 2]
Scene summary: Macbeth murders Duncan...

--- Generated Answer ---
Macbeth kills Duncan because...
```

To get a Shakespearean-style response, include style keywords in your question:
```
Question: Write a short Shakespearean-style speech from Hamlet about revenge
```

---

### Step 3 — Run evaluation

Runs all 15 questions through both systems and saves results to CSV.

```bash
# Preview questions without making LLM calls
python src/evaluate.py --dry-run

# Run full evaluation (~20 LLM calls, takes a few minutes)
python src/evaluate.py
```

Output: `results/evaluation_results.csv`

Open the CSV and fill in scores (1–5) for each row:

| Column | Meaning | Applies to |
|--------|---------|-----------|
| `correctness_score` | Factually accurate? | Both systems |
| `grounding_score` | Cites retrieved passages? | RAG only |
| `retrieval_relevance_score` | Retrieved chunks relevant? | RAG only |
| `usefulness_score` | Helpful for a beginner? | Both systems |
| `style_quality_score` | Sounds Shakespearean? | Stylised questions only |

---

### Step 4 — Test baseline only

```bash
python src/baseline.py --question "Who is Hamlet?"
```

---

## Switching LLM Backend

### Option A — Ollama (default, no API key needed)
```python
# In src/config.py
LLM_BACKEND = "ollama"
OLLAMA_MODEL = "llama3.2"
```

### Option B — Anthropic Claude API
```python
# In src/config.py
LLM_BACKEND = "anthropic"
```

Then set your API key before running:
```bash
# PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Command Prompt
set ANTHROPIC_API_KEY=sk-ant-...

# Mac / Linux
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Chunking Strategies

This system implements two chunking strategies for comparison:

| Strategy | Chunks | Best for |
|----------|--------|---------|
| Scene-level (default) | 73 | Contextual questions about motivation and theme |
| Utterance-level | 2690 | Specific quote retrieval, higher similarity scores |

The scene-level strategy is used as default because it provides richer context
for the LLM to generate complete answers.

---

## Dataset

Source texts from Project Gutenberg:
- Hamlet: https://www.gutenberg.org/cache/epub/1787/pg1787.txt
- Macbeth: https://www.gutenberg.org/cache/epub/1795/pg1795.txt
- Romeo and Juliet: https://www.gutenberg.org/cache/epub/1777/pg1777.txt

The structured dataset (JSON/JSONL) was provided by the course instructor
and includes scene summaries and keywords as teaching aids.
