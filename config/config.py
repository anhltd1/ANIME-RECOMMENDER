"""Load project configuration and API keys from the root ``.env`` file.

Import ``settings`` or the module-level constants from anywhere in the app or ``src``::

    from config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_EMBEDDING_MODEL, settings
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    """Values read once at import time from environment variables."""

    openai_api_key: str
    openai_model: str
    openai_embedding_model: str
    huggingface_api_key: str

    @classmethod
    def load(cls) -> Settings:
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip() or "gpt-4o-mini",
            openai_embedding_model=(
                os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small").strip()
                or "text-embedding-3-small"
            ),
            huggingface_api_key=os.getenv("HUGGINGFACE_API_KEY", "").strip(),
        )


settings = Settings.load()

OPENAI_API_KEY = settings.openai_api_key
OPENAI_MODEL = settings.openai_model
OPENAI_EMBEDDING_MODEL = settings.openai_embedding_model
HUGGINGFACE_API_KEY = settings.huggingface_api_key
