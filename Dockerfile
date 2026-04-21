# Anime Recommender — Streamlit on Linux (GKE / Cloud Run style)
# Build:  docker build -t anime-recommender:latest .
# Run:    docker run --rm -p 8501:8501 -e OPENAI_API_KEY=... anime-recommender:latest

FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

COPY requirements.txt setup.py ./
COPY app ./app
COPY config ./config
COPY pipeline ./pipeline
COPY src ./src
COPY utils ./utils
COPY data ./data
COPY faiss_db ./faiss_db

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -e .

EXPOSE 8501

# Bind all interfaces for containers; headless for server deployments (no browser auto-open).
CMD ["streamlit", "run", "app/app.py", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.port=8501"]
