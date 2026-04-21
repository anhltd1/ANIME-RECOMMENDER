# Dependencies policy

- **Source of truth:** `requirements.txt` lists packages for `pip` / `setup.py` (`install_requires`).
- **Pinning:** Core stack is pinned; `openai` is constrained to v1.x.
- **LangChain trio:** `langchain` / `langchain-community` **0.2.16** pin `langchain-core` below **0.3**. **`langchain-openai` 0.2.x** requires `langchain-core` **0.3.27+**, so those versions conflict. This repo uses **`langchain-openai==0.1.23`**, which resolves with **0.2.16** and still supports **`ChatOpenAI`** and **`gpt-4o-mini`**. To adopt **`langchain-openai` 0.2+**, upgrade **`langchain`**, **`langchain-community`**, and **`langchain-openai`** together on the **0.3.x** LangChain line.
- **Comments:** Lines starting with `#` in `requirements.txt` are allowed for notes.
- **Vector index:** Embeddings use the **OpenAI API** (`OPENAI_EMBEDDING_MODEL`, default **`text-embedding-3-small`**). Storage is **FAISS** (**`faiss-cpu`**) under **`faiss_db/`** (`save_local` / `load_local`). **No** HuggingFace **sentence-transformers** / local embedding models (avoids torch-related DLL issues); **no** chromadb.

## Stack roles

| Package | Role |
|---------|------|
| `streamlit` | Web UI (`app/`) |
| `pandas` | CSV / tabular data in `data/`; preprocessing in `process_data.py` — see **`docs/data.md`** |
| `python-dotenv` | Load `.env` via `config/config.py` |
| `langchain`, `langchain-community` | Orchestration, **`FAISS`** vector store (`langchain_community.vectorstores`) |
| `langchain-openai` (0.1.23), `openai` | **GPT** via LangChain `ChatOpenAI` + **`OpenAIEmbeddings`** for the vector index (`OPENAI_MODEL`, `OPENAI_EMBEDDING_MODEL`) |
| `faiss-cpu` | **FAISS** index on disk under **`faiss_db/`** (`index.faiss`, `index.pkl`) |

## Environment variables

See root `.env.example`: **`OPENAI_API_KEY`**, **`OPENAI_MODEL`**, **`OPENAI_EMBEDDING_MODEL`**, **`HUGGINGFACE_API_KEY`** (optional; not used by the vector index path).
