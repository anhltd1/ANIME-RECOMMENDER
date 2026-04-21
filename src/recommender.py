"""High-level retrieval-augmented anime recommender."""

from __future__ import annotations

from langchain_core.messages import HumanMessage
from langchain_core.retrievers import BaseRetriever
from langchain_openai import ChatOpenAI

from src.prompt_template import get_prompt_template


class AnimeRecommender:
    """
    Pipeline-friendly wrapper: a LangChain **retriever**, the shared prompt template
    (``context`` / ``question``), and **OpenAI** chat completion.

    Construct with injected dependencies; call ``get_recommendation`` per user query.
    """

    def __init__(self, retriever: BaseRetriever, api_key: str, model_name: str) -> None:
        self._retriever = retriever
        self._prompt = get_prompt_template()
        self._llm = ChatOpenAI(openai_api_key=api_key, model=model_name)

    def get_recommendation(self, query: str) -> str:
        docs = self._retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        prompt_text = self._prompt.format(context=context, question=query)
        response = self._llm.invoke([HumanMessage(content=prompt_text)])
        content = getattr(response, "content", None)
        if content is None:
            return str(response)
        if isinstance(content, str):
            return content
        return "".join(str(part) for part in content)


__all__ = ["AnimeRecommender"]
