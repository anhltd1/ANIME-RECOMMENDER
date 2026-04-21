"""LangChain prompt templates for retrieval / QA (``context`` + ``question``)."""

from __future__ import annotations

from langchain_core.prompts import PromptTemplate

INPUT_VARIABLES = ("context", "question")

# Replace this string when you finalize the prompt; it must contain ``{context}`` and ``{question}``.
DEFAULT_TEMPLATE = """You are an expert anime recommender. Your job is to help users find the perfect anime based on their preferences.

Using the following context, provide a detailed and engaging response to the user's question.

For each question, suggest exactly three anime titles. For each recommendation, include:
1. The anime title.
2. A concise plot summary (2-3 sentences).
3. A clear explanation of why this anime matches the user's preferences.

Present your recommendations in a numbered list format for easy reading.

If you don't know the answer, respond honestly by saying you don't know — do not fabricate any information.

Context:
{context}

User's question:
{question}

Your well-structured response:
"""


def get_prompt_template(template: str | None = None) -> PromptTemplate:
    """
    Return a LangChain ``PromptTemplate`` with input variables ``context`` and ``question``.

    Parameters
    ----------
    template :
        Optional template string. If omitted, ``DEFAULT_TEMPLATE`` is used.
        Custom templates must include ``{context}`` and ``{question}`` placeholders.
    """
    text = DEFAULT_TEMPLATE if template is None else template
    return PromptTemplate(template=text, input_variables=list(INPUT_VARIABLES))


__all__ = ["DEFAULT_TEMPLATE", "INPUT_VARIABLES", "get_prompt_template"]
