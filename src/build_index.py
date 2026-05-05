"""
Build retrieval indexes for both chunking strategies.

Run this script ONCE (or after changing chunking logic).
Creates two separate index folders:
    data/index/scene/        ← 73 scene-level chunks
    data/index/utterance/    ← ~2690 utterance-level chunks

Usage:
    python src/build_index.py              # build both
    python src/build_index.py --scene      # scene only
    python src/build_index.py --utterance  # utterance only
"""

import sys
from config import DEFAULT_TOP_K, EMBEDDING_MODEL_NAME
from data_loader import load_scene_chunks, load_utterances
from chunking import create_chunks, format_chunk_for_display
from retrieval import EmbeddingRetriever


def build_scene_index() -> EmbeddingRetriever:
    print("\n" + "="*60)
    print("Building SCENE-LEVEL index")
    print("="*60)
    records  = load_scene_chunks()
    chunks   = create_chunks(records, strategy="scene")
    print(f"Created {len(chunks)} scene chunks")
    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME, strategy="scene")
    retriever.build_index(chunks, save=True)
    return retriever


def build_utterance_index() -> EmbeddingRetriever:
    print("\n" + "="*60)
    print("Building UTTERANCE-LEVEL index")
    print("="*60)
    records  = load_utterances()
    chunks   = create_chunks(records, strategy="utterance")
    print(f"Created {len(chunks)} utterance chunks")
    retriever = EmbeddingRetriever(EMBEDDING_MODEL_NAME, strategy="utterance")
    retriever.build_index(chunks, save=True)
    return retriever


def sanity_check(retriever: EmbeddingRetriever) -> None:
    print(f"\nSanity check [{retriever.strategy}]:")
    queries = [
        "Why does Macbeth kill Duncan?",
        "Who is Hamlet?",
        "What is the feud between Montagues and Capulets?",
    ]
    for query in queries:
        results = retriever.retrieve(query, top_k=DEFAULT_TOP_K)
        print(f"\n  Q: {query}")
        for rank, (chunk, score) in enumerate(results, 1):
            play    = chunk.get("play", "?")
            act     = chunk.get("act", "?")
            scene   = chunk.get("scene", "?")
            summary = chunk.get("scene_summary", "")[:60]
            speaker = chunk.get("speaker", "")
            info    = f"{play} Act {act} Sc {scene}"
            if speaker:
                info += f" [{speaker}]"
            print(f"  [{rank}] score={score:.4f} | {info} — {summary}")


def main() -> None:
    args = sys.argv[1:]
    build_scene     = "--utterance" not in args or "--scene" in args
    build_utterance = "--scene" not in args or "--utterance" in args

    if build_scene:
        r = build_scene_index()
        sanity_check(r)

    if build_utterance:
        r = build_utterance_index()
        sanity_check(r)

    print("\n" + "="*60)
    print("Done! Index structure:")
    print("  data/index/scene/      ← use for RAG (default)")
    print("  data/index/utterance/  ← use for comparison experiment")
    print("\nTo use a specific strategy in rag_chatbot.py:")
    print("  retriever = EmbeddingRetriever(model, strategy='scene')")
    print("  retriever = EmbeddingRetriever(model, strategy='utterance')")


if __name__ == "__main__":
    main()