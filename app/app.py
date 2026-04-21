"""Streamlit UI: query in, recommendation out (pipeline loaded once via ``st.cache_resource``)."""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from pipeline import AnimeRecommenderPipeline

_REPO_ROOT = Path(__file__).resolve().parent.parent
_DEFAULT_CSV = _REPO_ROOT / "data" / "processed_data.csv"


@st.cache_resource(show_spinner="Loading recommender…")
def get_pipeline() -> AnimeRecommenderPipeline:
    """Build once per Streamlit server process; reused across reruns and sessions."""
    return AnimeRecommenderPipeline(_DEFAULT_CSV)


def main() -> None:
    st.set_page_config(page_title="Anime Recommender", layout="centered")

    st.title("Anime recommender")
    st.caption("Powered by retrieval + GPT. The pipeline is cached after first load.")

    query = st.text_area(
        "What are you in the mood for?",
        placeholder="e.g. dark sci-fi like Cowboy Bebop with jazz and bounty hunters",
        height=120,
    )

    if st.button("Get recommendation", type="primary"):
        q = (query or "").strip()
        if not q:
            st.warning("Enter a query first.")
            return
        try:
            with st.spinner("Generating answer…"):
                answer = get_pipeline().get_recommendation(q)
            st.markdown("### Response")
            st.markdown(answer)
        except Exception as e:
            st.error(str(e))


if __name__ == "__main__":
    main()
