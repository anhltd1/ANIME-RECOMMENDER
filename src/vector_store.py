"""Build a persisted FAISS index from CSV using OpenAI embeddings (no HuggingFace/torch)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from config import OPENAI_API_KEY, OPENAI_EMBEDDING_MODEL

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FAISS_DIR = PROJECT_ROOT / "faiss_db"
DEFAULT_TEXT_COLUMN = "combined_column"
DEFAULT_CHUNK_SIZE = 1000
DEFAULT_CHUNK_OVERLAP = 0


def openai_embeddings(model: str | None = None) -> OpenAIEmbeddings:
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY is required to build or load the vector index "
            "(embeddings use the OpenAI API)."
        )
    return OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        model=model or OPENAI_EMBEDDING_MODEL,
    )


class VectorStoreBuilder:
    """
    Load a CSV, chunk text, embed chunks with **OpenAI**, and persist **FAISS** under
    ``faiss_db/`` via ``save_local`` (``index.faiss`` + ``index.pkl``).

    Embeddings are **not** local HuggingFace/torch (the usual DLL pain on Windows); the
    vector store is **FAISS** for efficient disk-backed reuse across runs.
    """

    def __init__(
        self,
        csv_path: str | Path,
        *,
        text_column: str = DEFAULT_TEXT_COLUMN,
        persist_dir: str | Path | None = None,
        embedding_model: str | None = None,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
    ) -> None:
        self.csv_path = Path(csv_path)
        self.text_column = text_column
        self.persist_dir = (
            Path(persist_dir) if persist_dir is not None else DEFAULT_FAISS_DIR
        )
        self.embedding_model = embedding_model or OPENAI_EMBEDDING_MODEL
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def build(self) -> FAISS:
        df = pd.read_csv(self.csv_path)
        if self.text_column not in df.columns:
            raise ValueError(
                f"CSV must contain column {self.text_column!r}; got {list(df.columns)}"
            )

        documents = self._rows_to_documents(df)
        if not documents:
            raise ValueError(f"No rows to index from {self.csv_path}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )
        splits = splitter.split_documents(documents)

        embeddings = openai_embeddings(self.embedding_model)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        store = FAISS.from_documents(documents=splits, embedding=embeddings)
        store.save_local(str(self.persist_dir))
        return store

    def _rows_to_documents(self, df: pd.DataFrame) -> list[Document]:
        meta_cols = [c for c in df.columns if c != self.text_column]
        docs: list[Document] = []
        for _, row in df.iterrows():
            raw = row[self.text_column]
            if pd.isna(raw):
                continue
            text = str(raw).strip()
            if not text:
                continue
            metadata: dict[str, Any] = {
                c: ("" if pd.isna(row[c]) else str(row[c])) for c in meta_cols
            }
            docs.append(Document(page_content=text, metadata=metadata))
        return docs


__all__ = ["DEFAULT_FAISS_DIR", "VectorStoreBuilder", "openai_embeddings"]
