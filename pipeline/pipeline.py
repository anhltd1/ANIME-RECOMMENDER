"""Singleton pipeline: reuse persisted FAISS index when present, otherwise build from CSV."""

from __future__ import annotations

from pathlib import Path

from langchain_community.vectorstores import FAISS

from config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL, OPENAI_MODEL
from src.recommender import AnimeRecommender
from src.vector_store import (
    DEFAULT_FAISS_DIR,
    VectorStoreBuilder,
    openai_embeddings,
)


def _persist_dir_has_faiss_index(persist_dir: Path) -> bool:
    """True if ``FAISS.save_local`` output exists (skip re-chunk / re-embed documents)."""
    return (persist_dir / "index.faiss").is_file() and (persist_dir / "index.pkl").is_file()


class AnimeRecommenderPipeline:
    """
    Singleton: wires **FAISS** (``faiss_db/``) with **OpenAI embeddings** and **`AnimeRecommender`**.

    If **`faiss_db/index.faiss`** and **`index.pkl`** exist, loads **FAISS** (no document
    re-embedding). Otherwise **`VectorStoreBuilder`** chunks the CSV, embeds via OpenAI,
    and **``save_local``**s under **`faiss_db/`**.

    Query-time still calls the embeddings API for the user question only.
    """

    _instance: AnimeRecommenderPipeline | None = None

    def __new__(cls, csv_path: str | Path) -> AnimeRecommenderPipeline:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False  # noqa: SLF001
        return cls._instance

    def __init__(self, csv_path: str | Path) -> None:
        if getattr(self, "_initialized", False):
            return

        csv_path_resolved = Path(csv_path)
        embeddings = openai_embeddings(OPENAI_EMBEDDING_MODEL)

        persist_dir = DEFAULT_FAISS_DIR
        if _persist_dir_has_faiss_index(persist_dir):
            self.vector_store = FAISS.load_local(
                str(persist_dir),
                embeddings,
                allow_dangerous_deserialization=True,
            )
        else:
            self.vector_store = VectorStoreBuilder(
                csv_path_resolved,
                persist_dir=persist_dir,
                embedding_model=OPENAI_EMBEDDING_MODEL,
            ).build()

        self.csv_path = csv_path_resolved
        self.retriever = self.vector_store.as_retriever()
        self.recommender = AnimeRecommender(
            self.retriever,
            OPENAI_API_KEY,
            OPENAI_MODEL,
        )
        self._initialized = True

    def get_recommendation(self, query: str) -> str:
        return self.recommender.get_recommendation(query)


__all__ = ["AnimeRecommenderPipeline"]
