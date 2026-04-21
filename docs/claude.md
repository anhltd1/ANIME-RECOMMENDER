# Agent context — Anime Recommender

Use this file as the **single snapshot** of what the repository is for and where things live. Update it when structure, stack, or phase changes.

## Project

- **Name:** Anime Recommender  
- **Goal:** Recommend anime from user input (text and/or structured preferences) via a Streamlit UI and Python backend; AI pieces may follow in `src/` under dedicated folders.

## Tech stack (planned / current)

- **Language:** Python 3.x  
- **UI:** Streamlit (`app/`)  
- **Backend & AI:** `src/` with at least `src/backend/` and a separate folder for AI logic (e.g. `src/llm/`, `src/rag/`) — names TBD when implemented.  
- **Data:** CSV under `data/`; raw **`anime_with_synopsis.csv`**, derived **`processed_data.csv`** via **`DataLoader`** in **`src/process_data.py`** (CLI: **`python src/process_data.py`**); **FAISS** under **`faiss_db/`** via **`VectorStoreBuilder`** (**OpenAIEmbeddings**, no HuggingFace/torch) — details in **`docs/data.md`**.  
- **Config:** `config/config.py` loads `.env` via `python-dotenv`; **`OPENAI_API_KEY`**, **`OPENAI_MODEL`**, **`OPENAI_EMBEDDING_MODEL`**, **`HUGGINGFACE_API_KEY`**.  
- **LLM:** OpenAI GPT through **`langchain-openai==0.1.23`** + **`openai`** (pinned with `langchain` 0.2.16; `langchain-openai` 0.2.x needs LangChain 0.3+).  
- **Logging:** `utils/common/` (`logger`, `CustomException`); log files under `logs/` as Markdown per `docs/rules.md`  
- **Packaging:** `setup.py`, `requirements.txt`  
- **Deploy:** `Dockerfile` (to be filled as deployment needs clarify)

## Repository map

| Path | Role |
|------|------|
| `app/` | Streamlit frontend — **`app/app.py`** (cached **`AnimeRecommenderPipeline`**) |
| `config/` | Configuration modules |
| `data/` | `anime_with_synopsis.csv`, `processed_data.csv` (regenerate with `python src/process_data.py`) |
| `docs/` | `architecture.md`, **`data.md`**, `claude.md`, `rules.md`, `task.md` |
| `logs/` | Runtime `.md` logs |
| `utils/` | Shared utilities (`common` has logger + CustomException) |
| `src/process_data.py` | `DataLoader(input_csv, output_csv).process()` — default `data/` paths |
| `src/vector_store.py` | `VectorStoreBuilder`: processed CSV → `faiss_db/` (FAISS + OpenAI embeddings) |
| `src/prompt_template.py` | `get_prompt_template()` — LangChain `PromptTemplate` with `context` and `question` |
| `src/recommender.py` | `AnimeRecommender(retriever, api_key, model_name)` — `get_recommendation(query)` |
| `pipeline/` | `AnimeRecommenderPipeline(csv_path)` — singleton; reuses `faiss_db/` when present |
| `src/` | Backend + AI modules |

## Conventions

- Every Python package directory contains `__init__.py`.  
- Read and update `docs/` at each meaningful step; **`docs/data.md`** must stay aligned with **`DataLoader`** / **`src/process_data.py`**, **`src/vector_store.py`**, and `data/` files.  
- Record new global rules in `docs/rules.md`.  
- Record current work in `docs/task.md`.  
- Do not commit real `.env` values.

## Current phase (see `task.md` for live status)

Central config: `config/config.py` exposes `settings` and **`OPENAI_MODEL`** / **`OPENAI_EMBEDDING_MODEL`** / keys. Backend/LLM code under `src/` when added should import from `config` and use **`OPENAI_MODEL`** for chat and **`OPENAI_EMBEDDING_MODEL`** for the vector index.
