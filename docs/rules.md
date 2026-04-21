# Project rules

All contributors and agents must follow these rules. **Add new rules here** when conventions change; do not rely only on chat history.

## Documentation

1. **Read `docs/`** before changing behavior or structure.  
2. **Update** `architecture.md`, `claude.md`, `rules.md`, and `task.md` when you change structure, stack, or team agreements.  
3. **`docs/data.md`** — Whenever you change **`data/*.csv`**, **`src/process_data.py`** / **`DataLoader`**, **`src/vector_store.py`**, **`pipeline/pipeline.py`** / **`AnimeRecommenderPipeline`**, or preprocessing / vector-index rules (columns, filters, `combined_column`, **`faiss_db/`** paths, **`OPENAI_EMBEDDING_MODEL`**, chunking), update **`docs/data.md`** in the **same step**, and adjust **`README.md`** / **`docs/architecture.md`** if commands or paths change.  
4. Keep **`task.md`** accurate: it describes what is **in progress** and what is **done**.

## Code organization

1. **`src/`** holds all backend and AI code, split into **individual modules**.  
2. **`src/`** must include at least:  
   - `src/backend/` — API-free services, orchestration, data access.  
   - One additional package for AI behavior (name by purpose, e.g. `llm/`, `rag/`), split by logical units.  
3. **Every folder that is a Python package** must contain `__init__.py`. Asset-only directories (`data/`, `docs/`, `logs/`) are **not** Python packages and do not need `__init__.py`.  
4. **`app/`** is Streamlit-only; avoid embedding domain logic that belongs in `src/`.  
5. **`utils/`** is for cross-cutting helpers used across the project.  
6. **`config/`** centralizes settings; **secrets** live in **`.env`** (never commit real keys).

## Logging (`logs/`)

1. Log files are **Markdown** (`.md`) under `logs/`.  
2. Each log **entry** should be readable on its own and mirror **CustomException-style context** where applicable:  
   - Timestamp (UTC or local, state which in the file header once).  
   - Level (INFO, WARNING, ERROR).  
   - Message.  
   - If wrapping an error: original error repr, **filename**, **line number** (same spirit as `utils.common.custom_exception.CustomException`).  
3. Example line pattern (adjust headings as needed):

   ```markdown
   ## 2026-04-19T12:00:00Z | ERROR
   **Message:** Failed to load anime index  
   **Error:** `FileNotFoundError('...')`  
   **Location:** `path/to/module.py` line 42
   ```

## Collaboration

1. Keep prompts and replies **short** unless detail is required.  
2. Follow the **user’s prompt** strictly; avoid scope creep.  
3. Prefer **small, focused changes** over large refactors unless asked.

## Git and secrets

1. Do not commit `.env` or API keys.  
2. Document required environment **variable names** in `docs/` or `config/` examples without real values.

## Environment variables (`.env`)

Load via `config/config.py` (do not scatter `load_dotenv` calls):

| Variable | Purpose |
|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT chat completions **and** embedding API calls for the vector index. |
| `OPENAI_MODEL` | Chat model id (default **`gpt-4o-mini`**). |
| `OPENAI_EMBEDDING_MODEL` | Embeddings model id for **FAISS** / **`faiss_db/`** (default **`text-embedding-3-small`**). Must stay consistent when reusing **`index.faiss`** / **`index.pkl`**. |
| `HUGGINGFACE_API_KEY` | Optional; reserved for future HF tooling (not used by the current vector index). |
