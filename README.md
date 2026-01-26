# Multilingual AI News Summarizer

AI-powered news summarizer that breaks language barriers by providing summaries in Arabic, English, and French.

## Problem

In multilingual regions, news sources publish in different languages, creating accessibility barriers. Not everyone can access important information in their preferred language.

## Solution

An intelligent web application that:

1. Scrapes news from multiple sources
2. Automatically detects the article's language
3. Translates content as needed
4. Generates concise AI summaries
5. Delivers results in the user's preferred language

**Supported Languages**: Arabic • English • French

## Tech Stack

- **Python 3.9+**: Core programming language
- **BeautifulSoup4**: Web scraping and HTML parsing
- **Requests**: HTTP requests to news websites
- **HuggingFace Transformers**: State-of-the-art translation and summarization models
- **SQLite**: Efficient caching of processed articles
- **Streamlit**: Interactive web application interface

## Use Case

Initially developed to address news accessibility in Lebanon's trilingual ecosystem, but designed to work for any multilingual news region.

## Project Status

**In Development** - Building as part of ML engineering portfolio

## Installation

```bash
# Clone repository
git clone https://github.com/perlathebian/multilingual-ai-news-summarizer.git
cd multilingual-ai-news-summarizer

# Install dependencies
pip install -r requirements.txt

# Run application (coming soon)
streamlit run app.py
```

## Features Roadmap

- [x] Project structure and setup
- [ ] Multi-source web scraping
- [ ] Language detection
- [ ] Arabic ↔ English translation
- [ ] French ↔ English translation
- [ ] AI-powered summarization
- [ ] SQLite caching layer
- [ ] Interactive Streamlit UI
- [ ] Cloud deployment
