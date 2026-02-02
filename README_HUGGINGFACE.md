---
title: Multilingual AI News Summarizer
emoji: 🌍
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.29.0"
app_file: app.py
pinned: false
license: mit
---

# 🌍 Multilingual AI News Summarizer

Transform news articles from Arabic, English, or French into concise summaries in any of these languages using state-of-the-art AI.

## Features

- **Multi-Source Scraping**: Extracts articles from Lebanese news sources (Naharnet, MTV Lebanon, Beirut Today)
- **Automatic Language Detection**: Identifies Arabic, English, or French text
- **Neural Translation**: Translates between all three languages using Helsinki-NLP models
- **AI Summarization**: Generates intelligent summaries using Facebook's BART model
- **Multi-Language Output**: Get summaries in your preferred language (Arabic/English/French)
- **Smart Caching**: Instant retrieval for previously processed articles
- **Beautiful UI**: Modern, responsive interface with real-time feedback

## How It Works

1. **Paste URL**: Enter a news article URL from supported sources
2. **Choose Options**: Select summary length (30-200 words) and output language
3. **Process**: AI detects language, translates if needed, and generates summary
4. **Download**: Get your summary as a text file

## Use Case

Breaking language barriers in Lebanon's trilingual news ecosystem (Arabic/English/French). Perfect for:

- Multilingual readers who want news in their preferred language
- Quick scanning of multiple sources
- Language learners
- Researchers analyzing multilingual content

## Technology

**AI Models:**

- **Translation**: Helsinki-NLP OPUS models (Arabic to/from English, French to/from English)
- **Summarization**: Facebook BART-large-CNN
- **Detection**: LangDetect statistical analysis

**Backend:**

- Python 3.11
- HuggingFace Transformers
- Beautiful Soup (web scraping)
- SQLite (caching)

**Frontend:**

- Streamlit
- Custom CSS styling

## Performance

- **First request**: 30-90 seconds (full AI processing + caching)
- **Cached request**: <1 second (instant retrieval)
- **Translation**: 5-10 seconds per language pair
- **Speedup**: 50-500x faster for cached articles

## Limitations

- Only works with supported news sources (Naharnet, MTV Lebanon, Beirut Today)
- Processing time depends on article length and chosen options
- Translation quality varies by language pair and content type
- First load may be slow (models need to initialize)

## Links

- [GitHub Repository](https://github.com/perlathebian/multilingual-ai-news-summarizer)
- [Documentation](https://github.com/perlathebian/multilingual-ai-news-summarizer#readme)

## Developer

Built as a portfolio project demonstrating full-stack ML engineering skills.

**Skills Demonstrated:**

- Web scraping and data extraction
- Natural Language Processing (NLP)
- Neural machine translation
- AI model integration and optimization
- Database design and caching strategies
- Full-stack web development
- Production deployment
