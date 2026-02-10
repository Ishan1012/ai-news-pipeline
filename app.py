import streamlit as st
from scraper import scrape_articles, fetch_article_text, classify_domain
from cleaner import clean_text
from llm_processor import process_article
from db import save_article, fetch_articles_paginated, count_articles
from config import SCRAPE_SOURCES

st.set_page_config(
    page_title="AI News Pipeline",
    layout="wide"
)

st.title("📰 AI News Summarization Pipeline")
st.caption("Scrape → Summarize → Classify → Store → Read")

if "pipeline_ran" not in st.session_state:
    st.session_state.pipeline_ran = False

if "sources" not in st.session_state:
    st.session_state.sources = list(SCRAPE_SOURCES)

if "page" not in st.session_state:
    st.session_state.page = 0

st.sidebar.header("Controls")

run_button = st.sidebar.button("Re-run Pipeline")

st.sidebar.markdown("### Sources")
for src in st.session_state.sources:
    st.sidebar.write(src)

st.sidebar.markdown("---")
st.sidebar.markdown("### Add Custom Source")

new_source = st.sidebar.text_input(
    "Enter news URL",
    placeholder="https://example.com/news"
)

add_source_btn = st.sidebar.button("➕ Add Source")

if add_source_btn and new_source:
    if new_source not in st.session_state.sources:
        st.session_state.sources.append(new_source)
        st.session_state.pipeline_ran = False
        st.rerun()
    else:
        st.warning("Source already exists.")

def run_pipeline(sources):
    st.info("Pipeline running...")
    progress = st.progress(0)

    total_sources = len(sources)
    processed = 0

    for source in sources:
        st.subheader(f"Source: {source}")

        articles = scrape_articles(source)[:10]

        if not articles:
            processed += 1
            progress.progress(processed / total_sources)
            continue

        for art in articles:
            with st.spinner("Processing article..."):
                title = clean_text(art["title"])
                text = fetch_article_text(art["url"])

                if not text or len(text) < 300:
                    continue

                domain = classify_domain(text)
                summary = process_article(text)
                summary = summary if "Summary unavailable" not in summary else text[:500] + "..."

                save_article({
                    "title": title,
                    "url": art["url"],
                    "domain": domain,
                    "summary": summary
                })

                with st.expander(title):
                    st.markdown(f"**URL:** {art['url']}")
                    st.markdown(f"**Domain:** `{domain}`")
                    st.markdown("### Summary")
                    st.write(summary)

        processed += 1
        progress.progress(processed / total_sources)

    st.success("✅ Pipeline completed!")
    st.session_state.pipeline_ran = True

if not st.session_state.pipeline_ran:
    run_pipeline(st.session_state.sources)

if run_button:
    st.session_state.pipeline_ran = False
    st.rerun()

st.markdown("---")
st.header("📚 Stored Articles")

PAGE_SIZE = 10
total_articles = count_articles()
start = st.session_state.page * PAGE_SIZE

articles = fetch_articles_paginated(skip=start, limit=PAGE_SIZE)

if not articles:
    st.info("No articles stored yet.")
else:
    for art in articles:
        with st.expander(art["title"]):
            st.markdown(f"**URL:** {art['url']}")
            st.markdown(f"**Domain:** `{art['domain']}`")
            st.markdown("### Summary")
            st.write(art["summary"])

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.page > 0:
        if st.button("⬅ Previous"):
            st.session_state.page -= 1
            st.rerun()

with col3:
    if start + PAGE_SIZE < total_articles:
        if st.button("Read More ➡"):
            st.session_state.page += 1
            st.rerun()

st.caption(
    f"Showing {start + 1}–{min(start + PAGE_SIZE, total_articles)} "
    f"of {total_articles} articles"
)
