# Current task status

## Done

- [x] Repository layout agreed: `app/`, `config/`, `data/`, `docs/`, `logs/`, `utils/`, `src/` (see `docs/architecture.md`).  
- [x] Documentation created/updated: `docs/architecture.md`, `docs/claude.md`, `docs/rules.md`, `docs/task.md`.  
- [x] Package stubs with `__init__.py`: `app/`, `config/`, `utils/` (root).  
- [x] `data/` and `logs/` tracked via `.gitkeep`.  
- [x] Root `README.md`, `requirements.md`, and `Dockerfile` placeholder instructions.  
- [x] **`.gitignore`** added (`.env`, virtualenvs, `logs/*.md` / `*.log`, keep `logs/.gitkeep`).  
- [x] **`config/config.py`** — `load_dotenv`, `OPENAI_API_KEY`, `OPENAI_MODEL`, **`OPENAI_EMBEDDING_MODEL`** (default `text-embedding-3-small`), `HUGGINGFACE_API_KEY`; exported from `config/__init__.py`.  
- [x] **`.env` / `.env.example`** — OpenAI + HF keys; model name in env.  
- [x] **`requirements.txt`** — `langchain-openai==0.1.23` + `openai` (compatible with `langchain` 0.2.16; `langchain-openai` 0.2.x removed — needs LangChain 0.3+).  
- [x] **Data preprocessing** — **`DataLoader`** in **`src/process_data.py`** (**`input_csv`**, **`output_csv`**); defaults write **`data/processed_data.csv`** from **`data/anime_with_synopsis.csv`** (`Name`, `Genres`, `sypnopsis`, `combined_column`; rows with any empty/missing field dropped). Documented in **`docs/data.md`**; README and architecture cross-links updated.  
- [x] **Vector store** — **`src/vector_store.py`** defines **`VectorStoreBuilder`**: CSV → **`OpenAIEmbeddings`** (**`OPENAI_EMBEDDING_MODEL`**) + **FAISS** persisted under **`faiss_db/`** (`save_local`; **no** HuggingFace/torch for embeddings). Documented in **`docs/data.md`**, README, architecture, **`docs/rules.md`**, **`docs/claude.md`**.  
- [x] **`src/prompt_template.py`** — **`get_prompt_template()`** returns LangChain **`PromptTemplate`** with variables **`context`** and **`question`**; default copy in **`DEFAULT_TEMPLATE`** (override via argument or by editing the constant).  
- [x] **`src/recommender.py`** — **`AnimeRecommender`**: **`__init__(retriever, api_key, model_name)`**, **`get_recommendation(query)`** — retrieves context, formats prompt, calls **`ChatOpenAI`**.  
- [x] **`pipeline/pipeline.py`** — **`AnimeRecommenderPipeline`** singleton: **`csv_path`** on first init; if **`faiss_db/index.faiss`** + **`index.pkl`** exist, loads **FAISS** (no full re-embed of corpus); else **`VectorStoreBuilder`**. **`get_recommendation`**, **`vector_store`**, **`retriever`**, **`recommender`**. Documented in **`docs/data.md`**, README, architecture, **`docs/claude.md`**.  
- [x] **`app/app.py`** — Streamlit UI: query + **`get_pipeline().get_recommendation()`**; **`@st.cache_resource`** caches **`AnimeRecommenderPipeline`** once per Streamlit server process.  
- [x] **`Dockerfile`** + **`AnimeRecommender-k8s.yaml`** — Linux image (**`STREAMLIT_SERVER_*`**, **`0.0.0.0`**, **`headless`**); single-file Deployment + LoadBalancer Service (**8501**), local image **`imagePullPolicy: Never`**, README updated.

## In progress

- Nothing active.

## Next (suggested)

- Optional: **`src/backend/`** wrapper if you want HTTP-free services separate from Streamlit.  
- Polish **`app/app.py`** (history, sources, error UX) as needed.

*Last updated: Dockerfile + **`AnimeRecommender-k8s.yaml`** for GKE.*  
