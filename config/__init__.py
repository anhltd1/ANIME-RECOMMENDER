"""Configuration loaders and settings objects.

Read defaults from files in this package and secrets from the root ``.env`` (never commit
real keys). Expose a single place for the rest of the app to read paths, model names, and
feature flags.
"""

from config.config import (
    HUGGINGFACE_API_KEY,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
    OPENAI_MODEL,
    Settings,
    settings,
)

__all__ = [
    "HUGGINGFACE_API_KEY",
    "OPENAI_API_KEY",
    "OPENAI_EMBEDDING_MODEL",
    "OPENAI_MODEL",
    "Settings",
    "settings",
]
