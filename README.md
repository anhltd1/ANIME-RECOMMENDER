# Anime Recommender

Recommend anime titles from user input using a **Streamlit** UI, a Python **backend** under `src/`, and **CSV** data in `data/`. The default LLM is **OpenAI GPT** (**`gpt-4o-mini`**) via `langchain-openai` and the `openai` SDK; configure **`OPENAI_API_KEY`**, optional **`OPENAI_MODEL`**, and **`OPENAI_EMBEDDING_MODEL`** (vector index) in `.env`.

## Tech stack

- **Python 3** — application language  
- **Streamlit** — frontend (`app/`)  
- **OpenAI GPT** — `langchain-openai`, `openai` (model from `OPENAI_MODEL`, default `gpt-4o-mini`)  
- **Packaging** — `setup.py`, `requirements.txt`  
- **Configuration** — `config/config.py` loads `.env` (`OPENAI_*`, `HUGGINGFACE_API_KEY`)  
- **Data** — CSV files in `data/`; optional **FAISS** index under **`faiss_db/`** with **`OpenAIEmbeddings`** (no HuggingFace/torch for embeddings)  
- **Docker / K8s** — root **`Dockerfile`** (Streamlit **`0.0.0.0`** + **`headless`**); **`AnimeRecommender-k8s.yaml`** (Deployment + LoadBalancer Service)

## Documentation

| Doc | Contents |
|-----|----------|
| **`docs/architecture.md`** | Repository structure and target pipeline. |
| **`docs/data.md`** | CSV schemas, **`DataLoader`** / preprocessing, **FAISS + OpenAI embeddings / `VectorStoreBuilder`** — **update when data, preprocessing, or vector index behavior changes.** |
| **`docs/rules.md`** | Project conventions; includes keeping **`docs/data.md`** in sync. |
| **`docs/task.md`** | Done / in progress / next steps. |
| **`docs/claude.md`** | Short agent snapshot of stack and layout. |

## Setup

1. Create a virtual environment (recommended):

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install the package in editable mode:

   ```bash
   pip install -e .
   ```

3. Copy `.env.example` to `.env` and set **`OPENAI_API_KEY`**. Optional: **`OPENAI_MODEL`** (chat), **`OPENAI_EMBEDDING_MODEL`** (vector index; default **`text-embedding-3-small`**), **`HUGGINGFACE_API_KEY`** if needed elsewhere.

4. Run the UI from the repo root (after **`pip install -e .`**):

   ```bash
   streamlit run app/app.py
   ```

   The **`AnimeRecommenderPipeline`** is cached with **`st.cache_resource`** so the vector index loads once per server process.

## Data preprocessing

Raw anime metadata: **`data/anime_with_synopsis.csv`**. To build the cleaned file **`data/processed_data.csv`** ( **`Name`**, **`Genres`**, **`sypnopsis`**, **`combined_column`** ) with empty-field rows removed:

```bash
python src/process_data.py
```

Details: **`docs/data.md`**. From code: `DataLoader(input_csv, output_csv).process()`.

### Vector store (FAISS + OpenAI embeddings)

Build / refresh the persisted **FAISS** index under **`faiss_db/`** from **`data/processed_data.csv`** (chunking **1000** / **0**). Document embeddings use the OpenAI API (**`OPENAI_EMBEDDING_MODEL`**); index is **`save_local`**’d for reuse.

```python
from pathlib import Path
from src.vector_store import VectorStoreBuilder

VectorStoreBuilder(Path("data/processed_data.csv")).build()
```

See **`docs/data.md`** for defaults and constructor options.

### Orchestration (`pipeline/`)

**`AnimeRecommenderPipeline`** (singleton): pass **`csv_path`** on first use. If **`faiss_db/`** already has **`index.faiss`** and **`index.pkl`**, **FAISS** is loaded and the CSV is **not** chunked again; otherwise the pipeline builds and saves the index. See **`docs/data.md`**.

## Project layout (short)

| Path | Role |
|------|------|
| `app/` | Streamlit UI — **`app/app.py`** (`streamlit run app/app.py`) |
| `config/` | Settings loaders |
| `data/` | CSV datasets (`anime_with_synopsis.csv`, **`processed_data.csv`**) |
| `src/process_data.py` | **`DataLoader`** — **`input_csv`** → **`output_csv`** (CLI uses `data/` defaults) |
| `src/vector_store.py` | **`VectorStoreBuilder`** — CSV → **FAISS** under **`faiss_db/`** (OpenAI embeddings) |
| `src/recommender.py` | **`AnimeRecommender`** — retriever + OpenAI **`get_recommendation(query)`** |
| `pipeline/` | **`AnimeRecommenderPipeline`** — singleton (reuses **`faiss_db/`**) |
| `faiss_db/` | Persisted FAISS index (**`index.faiss`**, **`index.pkl`**; generated) |
| `docs/` | Architecture, **data schema**, rules, agent context, tasks |
| `logs/` | Runtime Markdown logs |
| `utils/` | Shared utilities (logging, exceptions) |
| `src/` | Backend and AI code (modular subpackages) |
| `Dockerfile` | Container image — **`streamlit run app/app.py`** with **`--server.address=0.0.0.0`** and **`--server.headless=true`** |
| `AnimeRecommender-k8s.yaml` | Kubernetes **Deployment** + **Service** (port **8501**) |

## Docker & Kubernetes

```bash
docker build -t anime-recommender:latest .
docker run --rm -p 8501:8501 \
  -e OPENAI_API_KEY=your-key \
  -e OPENAI_MODEL=gpt-4o-mini \
  -e OPENAI_EMBEDDING_MODEL=text-embedding-3-small \
  anime-recommender:latest
```

Ensure **`data/processed_data.csv`** and **`faiss_db/`** exist in the build context (run preprocessing / index build locally before `docker build` if needed).

On **GKE**, push the image to Artifact Registry, change **`image:`** and **`imagePullPolicy:`** in **`AnimeRecommender-k8s.yaml`**, create the **`anime-recommender-secrets`** Secret (see comments in the YAML), then:

```bash
kubectl apply -f AnimeRecommender-k8s.yaml
```

## License / author

See `setup.py` for package metadata.
