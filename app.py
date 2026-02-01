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

# Helper Fyunction 
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

# Page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="Multilingual AI News Summarizer",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    
    # Options in two columns
    opt_col1, opt_col2 = st.columns(2)
    
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
    
    # Summarize button
    summarize_button = st.button(
        "🚀 Summarize Article",
        type="primary",
        use_container_width=True
    )
    
    # Show what was entered (for testing)
    if url:
        st.caption(f"URL entered: {url[:50]}...")

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
            with st.spinner("🔍 Scraping article..."):
                scrape_start = time.time()
                article = get_article(url)
                scrape_time = time.time() - scrape_start
            
            if not article:
                st.error("❌ Failed to scrape article. Please check the URL and try again.")
            else:
                st.success(f"✅ Article scraped in {format_time(scrape_time)}")
                
                # Step 2: Process through AI pipeline with cache
                with st.spinner("🤖 Processing through AI pipeline..."):
                    process_start = time.time()
                    # Convert user's desired word count to tokens (internal detail)
                    summary_tokens = words_to_tokens(summary_words)

                    # DEBUG: Print to see values
                    st.write(f"DEBUG: Requested words: {summary_words}")
                    st.write(f"DEBUG: Converted to tokens: {summary_tokens}")

                    result = process_article_with_cache(
                        article, 
                        force_refresh=force_refresh,
                        summary_max_length=summary_tokens 
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
                        st.markdown("#### 📝 Summary")
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
            st.error(f"❌ An error occurred: {str(e)}")
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
