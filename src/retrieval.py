"""
Embedding and retrieval utilities for the Shakespeare RAG system.

Each chunking strategy has its own saved index directory so they never
overwrite each other:

    data/index/
        scene/
            embeddings.npy
            chunks.json
        utterance/
            embeddings.npy
            chunks.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

Chunk = Dict[str, Any]

BASE_INDEX_DIR = Path(__file__).resolve().parents[1] / "data" / "index"


def _index_paths(strategy: str) -> Tuple[Path, Path]:
    folder = BASE_INDEX_DIR / strategy
    return folder / "embeddings.npy", folder / "chunks.json"


class EmbeddingRetriever:
    """
    Embedding-based retriever with per-strategy index persistence.

    Args:
        embedding_model_name: HuggingFace model name
        strategy: "scene" or "utterance"
    """

    def __init__(self, embedding_model_name: str, strategy: str = "scene"):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise ImportError(
                "sentence-transformers is required.\n"
                "Install with: pip install sentence-transformers"
            ) from exc

        self.strategy = strategy
        self.embeddings_path, self.chunks_path = _index_paths(strategy)

        print(f"Loading embedding model: {embedding_model_name}")
        self.model = SentenceTransformer(embedding_model_name)
        self.chunks: List[Chunk] = []
        self.embeddings = None

    def build_index(self, chunks: List[Chunk], save: bool = True) -> None:
        if not chunks:
            raise ValueError("No chunks supplied to build_index().")
        print(f"Embedding {len(chunks)} chunks [{self.strategy}]...")
        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]
        self.embeddings = np.asarray(
            self.model.encode(texts, show_progress_bar=True), dtype=np.float32
        )
        print(f"Embedding shape: {self.embeddings.shape}")
        if save:
            self.save_index()

    def save_index(self) -> None:
        if self.embeddings is None or not self.chunks:
            raise RuntimeError("Nothing to save. Run build_index() first.")
        self.embeddings_path.parent.mkdir(parents=True, exist_ok=True)
        np.save(self.embeddings_path, self.embeddings)
        slim_chunks = [
            {k: v for k, v in c.items() if k != "metadata"}
            for c in self.chunks
        ]
        with self.chunks_path.open("w", encoding="utf-8") as f:
            json.dump(slim_chunks, f, ensure_ascii=False)
        print(f"Index saved [{self.strategy}]: {self.embeddings_path.parent}")

    def load_index(self) -> bool:
        if not self.embeddings_path.exists() or not self.chunks_path.exists():
            return False
        self.embeddings = np.load(self.embeddings_path)
        with self.chunks_path.open("r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        print(f"Index loaded [{self.strategy}]: {len(self.chunks)} chunks, shape {self.embeddings.shape}")
        return True

    def index_exists(self) -> bool:
        return self.embeddings_path.exists() and self.chunks_path.exists()

    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[Chunk, float]]:
        if self.embeddings is None:
            raise RuntimeError("Index is empty. Call build_index() or load_index() first.")
        query_vec = np.asarray(self.model.encode([query]), dtype=np.float32)
        scores = cosine_similarity(query_vec, self.embeddings)[0]
        top_indices = np.argsort(scores)[::-1][:top_k]
        return [(self.chunks[i], float(scores[i])) for i in top_indices]