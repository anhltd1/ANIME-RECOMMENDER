# Data — CSV sources and processed dataset

This document is the **source of truth** for anime CSV layout, how **`processed_data.csv`** is built, how the **OpenAI embeddings + FAISS** index under **`faiss_db/`** is produced, and how to regenerate artifacts. **Update this file** whenever `data/*.csv`, column meanings, **`src/process_data.py`** / **`DataLoader`**, or **`src/vector_store.py`** behavior changes.

## Files in `data/`

| File | Role |
|------|------|
| **`anime_with_synopsis.csv`** | Raw export-style table: **`MAL_ID`**, **`Name`**, **`Score`**, **`Genres`**, **`sypnopsis`** (column name matches the source file spelling). |
| **`processed_data.csv`** | Derived file for downstream use (embeddings, RAG, or recommendations). Built only from **`Name`**, **`Genres`**, **`sypnopsis`**, plus a generated **`combined_column`**. |

Do not hand-edit **`processed_data.csv`** for structural changes; change **`DataLoader`** logic in **`src/process_data.py`** (or pass different **`input_csv`** / **`output_csv`**) and regenerate.

## Regeneration

From the repository root:

```bash
python src/process_data.py
```

Requires **`pandas`** (see `requirements.txt`). The CLI uses **`DEFAULT_INPUT_CSV`** and **`DEFAULT_OUTPUT_CSV`** from **`src/process_data.py`**; programmatically:

```python
from src.process_data import DataLoader, DEFAULT_INPUT_CSV, DEFAULT_OUTPUT_CSV

DataLoader(DEFAULT_INPUT_CSV, DEFAULT_OUTPUT_CSV).process()
```

## Processing rules (`DataLoader` in `src/process_data.py`)

1. **Input columns read:** `Name`, `Genres`, `sypnopsis` (only these are loaded from the raw CSV).
2. **Row filter:** Any row where **`Name`**, **`Genres`**, or **`sypnopsis`** is missing (`NaN`) or becomes empty after **strip** is **dropped**. Rows must have all three fields non-empty.
3. **`combined_column`:** Built as a single text field:

   ```text
   Title {Name} 

    Genres: {Genres} 

    Overview: {sypnopsis}
   ```

   Literal newlines match ` \n\n ` segments in code (spaces around line breaks as implemented in **`DataLoader`**).

## Output schema (`processed_data.csv`)

| Column | Description |
|--------|-------------|
| `Name` | Anime title. |
| `Genres` | Comma-separated genre list as in the source. |
| `sypnopsis` | Synopsis text (column name preserved from source CSV). |
| `combined_column` | Concatenated block for LLM / embedding input. |

No index column is written; row order follows the filtered input order.

## Vector index — OpenAI embeddings + FAISS (`src/vector_store.py`)

**`VectorStoreBuilder`** reads a CSV (typically **`data/processed_data.csv`**), uses **`combined_column`** as **page content**, attaches other columns as **metadata**, splits with **`RecursiveCharacterTextSplitter`** (**`chunk_size=1000`**, **`chunk_overlap=0`**), embeds chunks with **`langchain_openai.OpenAIEmbeddings`** (**`OPENAI_EMBEDDING_MODEL`**, default **`text-embedding-3-small`**), builds **`langchain_community.vectorstores.FAISS`**, and calls **`save_local`** under **`faiss_db/`** (**`index.faiss`** + **`index.pkl`**).

Embeddings are **remote (OpenAI)** — no **sentence-transformers** / **torch** for vectors. The **vector store** is **FAISS** on disk so each run can **`load_local`** and skip re-embedding all chunks.

| Setting | Value |
|---------|--------|
| Persist directory | **`faiss_db/`** at repo root (`index.faiss`, `index.pkl`) |
| Embeddings | OpenAI API — **`OPENAI_EMBEDDING_MODEL`** in **`.env`** (see **`config/config.py`**) |
| Chunking | size **1000**, overlap **0** |
| Default text column | **`combined_column`** |
| Requirements | **`OPENAI_API_KEY`** for build, load, and query embedding; keep **`OPENAI_EMBEDDING_MODEL`** consistent with the built index. |

Remove legacy dirs if unused: **`chroma_db/`**, old **`vector_store/`**. To force a full rebuild, delete **`faiss_db/`** and run **`VectorStoreBuilder`** or **`AnimeRecommenderPipeline`** again.

Example (from repo root, with **`.env`** configured):

```python
from pathlib import Path

from src.vector_store import VectorStoreBuilder

csv_path = Path("data/processed_data.csv")
builder = VectorStoreBuilder(csv_path)
vs = builder.build()  # returns FAISS; use vs.as_retriever() in the pipeline
```

Prefer **`AnimeRecommenderPipeline`** (see below) so the index is reused when **`faiss_db/index.faiss`** and **`index.pkl`** already exist.

## Application pipeline (`pipeline/pipeline.py`)

**`AnimeRecommenderPipeline`** is a **singleton**. First instantiation passes **`csv_path`** (typically **`data/processed_data.csv`**).

| Behavior | When |
|----------|------|
| **Reuse index** | **`faiss_db/index.faiss`** and **`faiss_db/index.pkl`** exist — **`FAISS.load_local`** with **`OpenAIEmbeddings`**; **does not** re-chunk or re-embed stored documents. |
| **Build index** | No FAISS snapshot — **`VectorStoreBuilder`** chunks **`csv_path`**, embeds via OpenAI, **`save_local`** to **`faiss_db/`**. |

Public surface: **`vector_store`**, **`retriever`**, **`recommender`**, **`get_recommendation(query)`**. Further **`AnimeRecommenderPipeline(...)`** calls return the **same instance** (constructor **`csv_path`** ignored after first init).

```python
from pathlib import Path

from pipeline import AnimeRecommenderPipeline

pipe = AnimeRecommenderPipeline(Path("data/processed_data.csv"))
answer = pipe.get_recommendation("Anime like Cowboy Bebop")
```

## Row counts (regenerate to refresh)

After changes to the raw CSV or script, rerun **`python src/process_data.py`** and update this subsection. Example from a full run with no dropped rows: **269** data rows in both **`anime_with_synopsis.csv`** and **`processed_data.csv`** (header excluded).

---

*Maintenance:* Any agent or contributor who changes processing logic, vector index settings, or datasets must update **`docs/data.md`**, **`docs/task.md`** (if scope/status changes), and **`README.md`** / **`docs/architecture.md`** cross-links if paths or commands change.
