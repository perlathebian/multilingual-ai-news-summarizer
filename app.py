"""
Streamlit Web Application for Multilingual AI News Summarizer

This web interface allows users to:
- Input news article URLs
- Get AI-generated summaries
- View cache statistics
- Manage cached articles

Run with: streamlit run app.py
"""

import streamlit as st

from scraper import get_article
from pipeline import process_article_with_cache, SUPPORTED_LANGUAGES
import db
import time

# Initialize database
db.init_db()

# Helper Fyunctions
def format_time(seconds):
    """Format time for display."""
    if seconds < 0.01:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.2f}s"
    
def words_to_tokens(words):
    """
    Convert desired word count to approximate token count.
    
    Rule of thumb: 1 word ≈ 1.33 tokens (or 1 token ≈ 0.75 words)
    
    Args:
        words (int): Desired number of words
        
    Returns:
        int: Approximate number of tokens
    """
    return int(words * 1.33)    

# ============================================================================
# CUSTOM STYLING
# ============================================================================

def apply_custom_styling():
    """Apply clean, professional CSS styling to the app."""
    st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Main app - Clean white background */
    .stApp {
        background-color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main content area - Very subtle background */
    .main {
        background-color: #fafbfc;
    }
    
    /* Content blocks */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        background-color: transparent;
    }
    
    /* Sidebar - Light and modern */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e1e4e8;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: #24292e !important;
    }
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: #24292e !important;
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem !important;
        padding-bottom: 1rem !important;
        border-bottom: 2px solid #e1e4e8 !important;
    }
    
    /* Sidebar radio buttons */
    [data-testid="stSidebar"] .row-widget.stRadio > div {
        background-color: transparent;
        padding: 0.5rem;
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] .row-widget.stRadio > div > label:hover {
        background-color: #f6f8fa;
    }
    
    /* Sidebar links */
    [data-testid="stSidebar"] a {
        color: #0366d6 !important;
        text-decoration: none;
    }
    
    [data-testid="stSidebar"] a:hover {
        color: #0256c7 !important;
        text-decoration: underline;
    }
    
    /* Page titles */
    .main h1 {
        color: #24292e;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0;
        border-bottom: none !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Subheaders */
    .main h2 {
        color: #24292e;
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: none;
    }
    
    .main h3 {
        color: #586069;
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 1.5rem;
        border-bottom: none;
    }
    
    .main h4 {
        color: #586069;
        font-weight: 500;
        font-size: 1.25rem;
        border-bottom: none;
    }
    
    /* Markdown text after title */
    .main h1 + .stMarkdown {
        margin-top: 0.5rem;
        margin-bottom: 2rem;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #e1e4e8;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-color: #d1d5da;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 600;
        color: #586069;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        padding: 0.625rem 1.5rem;
        transition: all 0.2s ease;
        border: none;
        font-size: 0.975rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Primary button */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    /* Secondary button */
    .stButton > button[kind="secondary"] {
        background-color: #ffffff;
        color: #24292e;
        border: 1.5px solid #d1d5da;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: #f6f8fa;
        border-color: #959da5;
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        border: 1px solid;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }
    
    /* Info */
    [data-baseweb="notification"][kind="info"] {
        background-color: #f0f7ff;
        border-color: #c8e1ff;
        color: #0349b4;
    }
    
    /* Success */
    [data-baseweb="notification"][kind="success"] {
        background-color: #f0fdf4;
        border-color: #86efac;
        color: #166534;
    }
    
    /* Warning */
    [data-baseweb="notification"][kind="warning"] {
        background-color: #fffbeb;
        border-color: #fde68a;
        color: #92400e;
    }
    
    /* Error */
    [data-baseweb="notification"][kind="error"] {
        background-color: #fef2f2;
        border-color: #fecaca;
        color: #991b1b;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1.5px solid #d1d5da;
        padding: 0.625rem 0.875rem;
        transition: all 0.2s ease;
        font-size: 0.975rem;
        background-color: #ffffff;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        outline: none;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background-color: #6366f1;
    }
    
    /* Checkbox */
    .stCheckbox {
        color: #24292e;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        font-weight: 600;
        color: #24292e;
        padding: 1rem 1.25rem;
        transition: all 0.2s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f6f8fa;
        border-color: #d1d5da;
    }
    
    .streamlit-expanderContent {
        border: 1px solid #e1e4e8;
        border-top: none;
        border-radius: 0 0 8px 8px;
        background-color: #ffffff;
        padding: 1rem;
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e1e4e8;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
    }
    
    /* Tables */
    table {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #e1e4e8;
        background-color: #ffffff;
    }
    
    thead tr {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    }
    
    th {
        color: white !important;
        font-weight: 600;
        padding: 0.875rem 1rem;
        text-align: left;
        border: none;
    }
    
    td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e1e4e8;
        color: #24292e;
    }
    
    tbody tr {
        background-color: #ffffff;
        transition: background-color 0.15s ease;
    }
    
    tbody tr:hover {
        background-color: #f6f8fa;
    }
    
    tbody tr:last-child td {
        border-bottom: none;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #6366f1 !important;
    }
    
    /* Captions */
    .caption, [data-testid="stCaptionContainer"] {
        color: #586069;
        font-size: 0.875rem;
    }
    
    /* Links */
    a {
        color: #0366d6;
        text-decoration: none;
    }
    
    a:hover {
        color: #0256c7;
        text-decoration: underline;
    }
    
    /* Code */
    code {
        background-color: #f6f8fa;
        color: #e83e8c;
        padding: 0.2rem 0.4rem;
        border-radius: 3px;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
        border: 1px solid #e1e4e8;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f6f8fa;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #d1d5da;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #959da5;
    }
    
    /* Remove any stray borders */
    .main h1::after,
    .main h1::before {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="Multilingual AI News Summarizer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()

# Get cache stats for sidebar
cache_stats = db.get_cache_stats()

with st.sidebar:
    st.title("Navigation")
    
    # Page selection
    page = st.radio(
        "Choose a page:",
        ["Summarizer", "Cache Explorer", "About"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Quick stats in sidebar
    st.subheader("📈 Quick Stats")
    st.metric("Cached Articles", cache_stats['total_articles'])
    
    if cache_stats['by_language']:
        st.caption("**By Language:**")
        for lang, count in cache_stats['by_language'].items():
            lang_names = {'ar': 'Arabic', 'en': 'English', 'fr': 'French'}
            st.caption(f"• {lang_names.get(lang, lang)}: {count}")
    
    st.divider()
    
    # Links
    st.caption("**Resources:**")
    st.caption("📖 [GitHub Repo](https://github.com/perlathebian/multilingual-ai-news-summarizer)")
    st.caption("🤖 [HuggingFace Models](https://huggingface.co/)")

# PAGE ROUTER

if page == "Summarizer":
    # ========================================================================
    # SUMMARIZER PAGE 
    # ========================================================================
    
    # Header Section
    st.title("🌍 Multilingual AI News Summarizer")

    # Subtitle
    st.markdown("""
        Transform news articles from **Arabic**, **English**, or **French** into concise English summaries using AI.
    """)

    # Feature highlights
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Languages", "3", help="Arabic, English, French")

    with col2:
        st.metric("News Sources", "3", help="Naharnet, MTV Lebanon, Beirut Today")

    with col3:
        st.metric("AI Models", "3", help="Translation + Summarization")

    with col4:
        st.metric("Cache Speedup", "2,000x", help="Instant retrieval for cached articles")

    st.divider()

    # Main content Section

    # Create two columns: left for input, right for info
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📝 Article Summarizer")
    
        # URL input
        url = st.text_input(
            "Enter Article URL:",
            placeholder="https://www.source.com/stories/en/12345...",
            help="Paste a URL from Naharnet, MTV Lebanon, or Beirut Today"
        )
    
    # Options in three columns
    opt_col1, opt_col2, opt_col3 = st.columns(3)

    with opt_col1:
        # Force refresh checkbox
        force_refresh = st.checkbox(
            "Force Refresh",
            help="Bypass cache and reprocess article"
        )

    with opt_col2:
        # Summary length slider - in WORDS (user-friendly)
        summary_words = st.slider(
            "Summary Length (words)",
            min_value=30,
            max_value=200,
            value=100,
            step=10,
            help="Desired number of words in summary. Actual length may vary slightly as the AI completes sentences naturally."
        )

    with opt_col3:
        # Output language selector
        output_language = st.selectbox(
            "Summary Language",
            options=['en', 'ar', 'fr'],
            format_func=lambda x: {'en': 'EN English', 'ar': 'AR Arabic', 'fr': 'FR French'}[x],
            help="Choose the language for the final summary"
        )
    
        # Summarize button
        summarize_button = st.button(
            "🚀 Summarize Article",
            type="primary",
            use_container_width=True
        )

    with right_col:
        st.subheader("How It Works")
    
        st.markdown("""
            **Process:**
            1. 🔗 Paste article URL
            2. 🔍 Auto-detect language
            3. 🔄 Translate if needed
            4. 🤖 Generate AI summary
            5. 💾 Cache for instant reuse
    
            **Supported Sources:**
            - Naharnet (naharnet.com)
            - MTV Lebanon (mtv.com.lb)
            - Beirut Today (beirut-today.com)
        """)

    st.divider()

    # Results Section 

    st.subheader("📄 Summary Results")

    # Process article when button is clicked
    if summarize_button:
        if not url:
            st.error("Please enter a URL first!")
        else:
            # Check if URL is from supported source
            supported_domains = ['naharnet.com', 'mtv.com.lb', 'beirut-today.com']
            if not any(domain in url for domain in supported_domains):
                st.warning(f"URL may not be from a supported source. Supported: {', '.join(supported_domains)}")
        
            try:
                # Step 1: Scrape article
                with st.spinner("🔍 Scraping article from source..."):
                    scrape_start = time.time()
                    article = get_article(url)
                    scrape_time = time.time() - scrape_start

                if not article:
                    st.error("❌ Failed to scrape article.")
                    st.info("💡 **Troubleshooting Tips:**\n- Verify the URL is correct\n- Check if the article still exists\n- Try a different article from the same source")
                    st.stop()  # Stop execution here
                else:
                    # Success with details
                    st.success(f"✅ Article scraped successfully in {format_time(scrape_time)}")
    
                    # Show article preview
                    with st.expander("📄 Article Preview"):
                        st.write(f"**Title:** {article['title']}")
                        st.write(f"**Source:** {article.get('source', 'Unknown')}")
                        st.write(f"**Text length:** {len(article['text']):,} characters")
                
                    # Step 2: Process through AI pipeline with cache
                    # Check cache status first
                    is_cached = db.article_exists(url)

                    if is_cached and not force_refresh:
                        st.info("💾 Article found in cache - retrieving instantly...")
                    elif force_refresh:
                        st.info("🔄 Force refresh enabled - reprocessing article...")
                    else:
                        st.info("🤖 Article not cached - processing through AI pipeline (may take 40-90 seconds)...")

                    with st.spinner("🤖 Processing through AI pipeline..."):
                        process_start = time.time()
                        # Convert user's desired word count to tokens (internal detail)
                        summary_tokens = words_to_tokens(summary_words)

                        result = process_article_with_cache(
                            article, 
                            force_refresh=force_refresh,
                            summary_max_length=summary_tokens,
                            output_language=output_language 
                        )
                        process_time = time.time() - process_start
                
                    if not result:
                        st.error("❌ Failed to process article. Please try again.")
                    else:
                        # Determine if cached
                        was_cached = process_time < 1
                    
                        # Display results in a nice container
                        st.success("✅ Processing complete!")
                    
                        # Results container
                        with st.container():
                            # Title
                            st.markdown(f"### 📰 {result['title']}")
                        
                            # Metadata row
                            meta_col1, meta_col2, meta_col3, meta_col4 = st.columns(4)
                        
                            with meta_col1:
                                st.metric(
                                    "Source", 
                                    result['source'],
                                    help="News source"
                                )
                        
                            with meta_col2:
                                language_name = SUPPORTED_LANGUAGES.get(result['original_language'], 'Unknown')
                                st.metric(
                                    "Language", 
                                    language_name,
                                    help="Detected language"
                                )
                        
                            with meta_col3:
                                st.metric(
                                    "Date", 
                                    result.get('date', 'N/A'),
                                    help="Publication date"
                                )
                        
                            with meta_col4:
                                st.metric(
                                    "Processing Time",
                                    format_time(process_time),
                                    delta="Cached" if was_cached else "Fresh",
                                    delta_color="off"
                                )
                        
                            st.divider()
                        
                            # Summary section
                            summary_lang = result.get('summary_language', 'en')
                            lang_flag = {'en': 'EN', 'ar': 'AR', 'fr': 'FR'}.get(summary_lang, '🌍')
                            lang_name = SUPPORTED_LANGUAGES.get(summary_lang, 'Unknown')

                            st.markdown(f"#### 📝 Summary ({lang_flag} {lang_name})")
                            st.write(result['summary'])

                            # Word count - show requested vs actual
                            actual_words = len(result['summary'].split())
                            st.caption(f"📊 Requested: {summary_words} words | Actual: ~{actual_words} words")

                            # Cache status indicator
                            if was_cached:
                                st.info("✨ This result was retrieved from cache (instant retrieval!)")
                            else:
                                st.info("🔄 This article has been processed and cached for future requests.")

                            # Download button
                            summary_text = f"""
                                Title: {result['title']}
                                Source: {result['source']}
                                Language: {language_name}
                                Date: {result.get('date', 'N/A')}
                                URL: {result['url']}

                                Summary:
                                    {result['summary']}

                                ---
                                Generated by Multilingual AI News Summarizer
                                Processing Time: {format_time(process_time)}
                                Cache Status: {'Cached' if was_cached else 'Fresh'}
                            """
                            st.download_button(
                                label="📥 Download Summary",
                                data=summary_text,
                                file_name=f"summary_{result['source'].replace(' ', '_')}.txt",
                                mime="text/plain"
                            )
        
            except Exception as e:
                st.error("❌ An error occurred while processing the article.")
    
                # Show different messages based on error type
                error_msg = str(e).lower()
    
                if "connection" in error_msg or "timeout" in error_msg:
                    st.warning("🌐 Network issue detected. Please check your internet connection and try again.")
                elif "403" in error_msg or "forbidden" in error_msg:
                    st.warning("🚫 Access denied by the website. The site may be blocking automated requests.")
                elif "404" in error_msg or "not found" in error_msg:
                    st.warning("🔍 Article not found. Please check if the URL is correct and the article still exists.")
                else:
                    st.warning("💡 Try refreshing the page or using a different article URL.")
    
                # Show technical details in expander (for debugging)
                with st.expander("🔧 Technical Details (for debugging)"):
                    st.exception(e)

    else:
        # Show placeholder when no processing
        st.info("👆 Enter a URL above and click 'Summarize Article' to get started!")

    st.divider()

    # Footer Section

    # Statistics footer
    footer_col1, footer_col2, footer_col3 = st.columns(3)

    with footer_col1:
        st.caption("🚀 Powered by HuggingFace Transformers")

    with footer_col2:
        st.caption("💾 SQLite Database Caching")

    with footer_col3:
        st.caption("🐍 Built with Python & Streamlit")

elif page == "Cache Explorer":
    # ========================================================================
    # CACHE EXPLORER PAGE 
    # ========================================================================
    
    st.title("📊 Cache Explorer")
    st.markdown("View and manage cached articles")
    
    st.divider()
    
    # STEP 12: Statistics Dashboard
    st.subheader("📈 Cache Statistics")
    
    stats = db.get_cache_stats()
    
    # Metrics row
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric(
            "Total Articles",
            stats['total_articles'],
            help="Number of articles in cache"
        )
    
    with stat_col2:
        if stats['by_language']:
            most_common_lang = max(stats['by_language'], key=stats['by_language'].get)
            lang_names = {'ar': 'Arabic', 'en': 'English', 'fr': 'French'}
            st.metric(
                "Most Common Language",
                lang_names.get(most_common_lang, most_common_lang),
                delta=f"{stats['by_language'][most_common_lang]} articles"
            )
        else:
            st.metric("Most Common Language", "N/A")
    
    with stat_col3:
        if stats['by_source']:
            most_common_source = max(stats['by_source'], key=stats['by_source'].get)
            st.metric(
                "Most Common Source",
                most_common_source,
                delta=f"{stats['by_source'][most_common_source]} articles"
            )
        else:
            st.metric("Most Common Source", "N/A")
    
    # Detailed breakdown
    detail_col1, detail_col2 = st.columns(2)
    
    with detail_col1:
        st.markdown("**By Language:**")
        if stats['by_language']:
            lang_names = {'ar': 'Arabic', 'en': 'English', 'fr': 'French'}
            for lang, count in stats['by_language'].items():
                st.write(f"• {lang_names.get(lang, lang)}: **{count}** articles")
        else:
            st.info("No articles cached yet")
    
    with detail_col2:
        st.markdown("**By Source:**")
        if stats['by_source']:
            for source, count in stats['by_source'].items():
                st.write(f"• {source}: **{count}** articles")
        else:
            st.info("No articles cached yet")
    
    st.divider()
    
    # STEP 13: Cached Articles List
    st.subheader("📚 Cached Articles")
    
    articles = db.get_all_articles()
    
    if articles:
        st.info(f"Showing {len(articles)} cached article(s)")
        
        # Display each article in an expander
        for i, article in enumerate(articles, 1):
            # Truncate title for expander label
            title_short = article['title'][:60] + "..." if len(article['title']) > 60 else article['title']
            
            with st.expander(f"{i}. {title_short}"):
                # Article details
                art_col1, art_col2 = st.columns([2, 1])
                
                with art_col1:
                    st.markdown(f"**Title:** {article['title']}")
                    st.markdown(f"**URL:** [{article['url'][:50]}...]({article['url']})")
                
                with art_col2:
                    lang_names = {'ar': 'Arabic', 'en': 'English', 'fr': 'French'}
                    st.markdown(f"**Source:** {article['source']}")
                    st.markdown(f"**Language:** {lang_names.get(article['original_language'], 'Unknown')}")
                    st.markdown(f"**Date:** {article.get('date', 'N/A')}")
                    st.markdown(f"**Cached:** {article['date_processed'][:19]}")
                
                st.divider()
                
                # Summary
                st.markdown("**Summary:**")
                st.write(article['summary'])
                
                # Download this cached summary
                summary_text = f"""
                    Title: {article['title']}
                    Source: {article['source']}
                    Language: {lang_names.get(article['original_language'], 'Unknown')}
                    Date: {article.get('date', 'N/A')}
                    URL: {article['url']}
                    Cached: {article['date_processed']}

                    Summary:
                    {article['summary']}

                    ---
                    Retrieved from cache
                """
                st.download_button(
                    label="📥 Download",
                    data=summary_text,
                    file_name=f"cached_{article['source'].replace(' ', '_')}_{i}.txt",
                    mime="text/plain",
                    key=f"download_{i}"  # Unique key for each button
                )
    else:
        st.warning("No articles in cache yet. Process some articles in the Summarizer page!")
    
    st.divider()
    
    # STEP 14: Clear Cache Button
    st.subheader("🗑️ Cache Management")
    
    if stats['total_articles'] > 0:
        st.warning(f"⚠️ You have **{stats['total_articles']}** article(s) in cache.")
        
        # Confirmation checkbox
        confirm = st.checkbox("I understand this will delete all cached articles permanently")
        
        # Clear button (disabled unless confirmed)
        if st.button(
            "🗑️ Clear Entire Cache",
            type="secondary",
            disabled=not confirm,
            use_container_width=True
        ):
            deleted_count = db.clear_cache()
            st.success(f"✅ Cache cleared! Deleted {deleted_count} article(s).")
            st.rerun()  # Refresh page to update stats
    else:
        st.info("Cache is already empty!")


elif page == "About":
    # ========================================================================
    # ABOUT PAGE
    # ========================================================================
    
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    ### 🌍 Multilingual AI News Summarizer
    
    An intelligent web application that breaks language barriers by transforming news articles 
    from Arabic, English, or French into concise English summaries using state-of-the-art AI models.
    """)
    
    st.divider()
    
    # How It Works Section
    st.subheader("🔧 How It Works")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        **Complete Processing Pipeline:**
        
        1. **Web Scraping** 📰
           - Extracts article content from Lebanese news sources
           - Retrieves title, text, publication date
           - Site-specific parsing for reliability
        
        2. **Language Detection** 🔍
           - Automatic identification of Arabic, English, or French
           - Statistical detection using langdetect library
           - Handles mixed-language content
        
        3. **Neural Machine Translation** 🔄
           - Arabic → English (Helsinki-NLP model)
           - French → English (Helsinki-NLP model)
           - Preserves context and meaning
        """)
    
    with col2:
        st.markdown("""
        **AI Processing:**
        
        4. **AI Summarization** 🤖
           - BART model (Facebook AI)
           - Generates concise, coherent summaries
           - Preserves key information
           - Adjustable summary length
        
        5. **Database Caching** 💾
           - SQLite persistent storage
           - Instant retrieval for processed articles
           - Prevents redundant AI processing
           - 1,000-10,000x speedup
        """)
    
    st.divider()
    
    # Performance Metrics Section
    st.subheader("⚡ Performance Metrics")
    
    perf_col1, perf_col2, perf_col3 = st.columns(3)
    
    with perf_col1:
        st.metric(
            "Cache Hit Speed",
            "10-50ms",
            delta="vs 40-90s uncached",
            help="Time to retrieve cached articles"
        )
    
    with perf_col2:
        st.metric(
            "Speed Improvement",
            "2,000-5,000x",
            delta="Typical speedup",
            help="Cache vs full AI processing"
        )
    
    with perf_col3:
        st.metric(
            "AI Models",
            "3 Models",
            delta="2.2GB total",
            help="Translation + Summarization"
        )
    
    st.markdown("""
    **Processing Times (CPU):**
    
    | Operation | First Request | Cached Request | Improvement |
    |-----------|---------------|----------------|-------------|
    | Scraping | 1-3s | N/A | - |
    | Language Detection | 0.5s | N/A | - |
    | Translation | 1-3s | N/A | - |
    | Summarization | 40-80s | N/A | - |
    | **Total (Cache Miss)** | **50-90s** | - | - |
    | **Total (Cache Hit)** | - | **0.01-0.05s** | **1,000-10,000x** |
    """)
    
    st.divider()
    
    # Technology Stack Section
    st.subheader("🛠️ Technology Stack")
    
    tech_col1, tech_col2 = st.columns(2)
    
    with tech_col1:
        st.markdown("""
        **Backend:**
        - **Python 3.11** - Core language
        - **Beautiful Soup** - Web scraping
        - **HuggingFace Transformers** - AI models
        - **PyTorch** - Deep learning framework
        - **SQLite** - Database caching
        - **LangDetect** - Language identification
        """)
    
    with tech_col2:
        st.markdown("""
        **AI Models:**
        - **Helsinki-NLP/opus-mt-ar-en** (~300MB)
          - Arabic → English translation
        - **Helsinki-NLP/opus-mt-fr-en** (~300MB)
          - French → English translation
        - **facebook/bart-large-cnn** (~1.6GB)
          - English text summarization
        """)
    
    st.markdown("""
    **Frontend:**
    - **Streamlit** - Interactive web interface
    - **Python** - All UI logic in Python (no HTML/CSS/JS needed!)
    """)
    
    st.divider()
    
    # Use Case Section
    st.subheader("🎯 Use Case")
    
    st.markdown("""
    Initially developed to address news accessibility in **Lebanon's trilingual ecosystem** 
    (Arabic/English/French), but designed to work for any multilingual news region.
    
    **Problem Solved:**
    - Language barriers prevent people from accessing important news
    - Not everyone can read articles in Arabic, English, or French
    - Translation services are slow and inaccurate
    - Manual summarization is time-consuming
    
    **Solution Provided:**
    - Automatic language detection and translation
    - AI-powered accurate summaries
    - Fast processing with caching
    - Accessible web interface
    """)
    
    st.divider()
    
    # Supported Sources Section
    st.subheader("📰 Supported News Sources")
    
    source_col1, source_col2, source_col3 = st.columns(3)
    
    with source_col1:
        st.markdown("""
        **Naharnet**
        - naharnet.com
        - Lebanese news
        - English content
        """)
    
    with source_col2:
        st.markdown("""
        **MTV Lebanon**
        - mtv.com.lb
        - Lebanese broadcaster
        - Multi-language
        """)
    
    with source_col3:
        st.markdown("""
        **Beirut Today**
        - beirut-today.com
        - Culture & news
        - Arabic/English
        """)
    
    st.divider()
    
    # Developer Info Section
    st.subheader("👨‍💻 Developer Information")
    
    st.markdown("""
    **Built by:** Perla Thebian
    
    **Purpose:** Portfolio project demonstrating full-stack ML engineering skills
    
    **Part of:** 8-week ML Engineer employability plan
    
    **Skills Demonstrated:**
    - Web scraping and data extraction
    - Natural Language Processing (NLP)
    - Neural machine translation
    - AI model integration
    - Database design and caching strategies
    - Full-stack web development
    - Performance optimization
    - Production-ready code practices
    """)
    
    st.divider()
    
    # Links Section
    st.subheader("🔗 Links & Resources")
    
    link_col1, link_col2 = st.columns(2)
    
    with link_col1:
        st.markdown("""
        **Project:**
        - 📖 [GitHub Repository](https://github.com/perlathebian/multilingual-ai-news-summarizer)
        - 📄 [Documentation](https://github.com/perlathebian/multilingual-ai-news-summarizer#readme)
        """)
    
    with link_col2:
        st.markdown("""
        **Technologies:**
        - 🤗 [HuggingFace Models](https://huggingface.co/)
        - 🎨 [Streamlit Docs](https://docs.streamlit.io/)
        - 🐍 [Python](https://www.python.org/)
        """)
    
    st.divider()
    
    # Footer
    st.info("""
    **License:** MIT License - Educational portfolio project
    
    **Acknowledgments:** News sources used for educational scraping purposes. 
    HuggingFace for pre-trained models. Helsinki-NLP for translation models. Meta AI for BART.
    """)
