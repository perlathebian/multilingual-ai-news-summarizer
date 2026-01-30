# Multilingual AI News Summarizer

AI-powered news summarizer that breaks language barriers by providing intelligent summaries in multiple languages.

## Problem

In multilingual regions, news sources publish in different languages, creating accessibility barriers. Not everyone can access important information in their preferred language.

## Solution

An intelligent system that:

1. **Scrapes** news from multiple Lebanese sources
2. **Detects** the article's language automatically (Arabic/English/French)
3. **Translates** content to English if needed
4. **Generates** AI-powered concise summaries
5. **Delivers** accessible summaries regardless of original language

## Features

### Multi-Source Web Scraping

**Supported Sources:**

- **Naharnet** (naharnet.com) - Lebanese news
- **MTV Lebanon** (mtv.com.lb) - Lebanese broadcaster
- **Beirut Today** (beirut-today.com) - Lebanese culture & news

**Capabilities:**

- Site-specific HTML parsing with automatic source detection
- Extracts title, full text, and publication dates
- Rate limiting and error handling
- DRY architecture with shared helper functions

### AI-Powered Language Processing

**Automatic Language Detection:**

- Identifies Arabic, English, and French text
- Statistical detection using langdetect library

**Neural Machine Translation:**

- Arabic -> English (Helsinki-NLP/opus-mt-ar-en)
- French -> English (Helsinki-NLP/opus-mt-fr-en)
- Handles long text with intelligent chunking

**AI Summarization:**

- BART model (facebook/bart-large-cnn) for English summarization
- Generates concise summaries preserving key information
- Configurable summary length

**Complete Pipeline:**

```
News URL -> Scrape -> Detect Language -> Translate (if needed) -> Summarize -> Output
```

## Tech Stack

### Data Collection

- **Python 3.11**: Core programming language
- **Requests**: HTTP client for web scraping
- **BeautifulSoup4**: HTML parsing and extraction

### AI/ML

- **HuggingFace Transformers**: State-of-the-art NLP models
- **PyTorch**: Deep learning framework
- **LangDetect**: Statistical language identification
- **SentencePiece**: Neural text tokenization

### Coming Soon

- **SQLite**: Caching layer for processed articles
- **Streamlit**: Interactive web interface

## Installation

```bash
# Clone repository
git clone https://github.com/perlathebian/multilingual-ai-news-summarizer.git
cd multilingual-ai-news-summarizer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** First run will download AI models (~2-3GB). This takes 10-20 minutes but only happens once.

## Usage

### Quick Demo

```bash
python demo.py
```

### Scrape a Specific Article

```python
from scraper import get_article

# Scrape an article
article = get_article(url)
print(article['title'])
print(article['text'])
```

### Process Through AI Pipeline

```python
from scraper import get_article
from pipeline import process_article

# Get article
article = get_article(url)

# Process through AI pipeline
result = process_article(article)

# Access results
print(f"Original Language: {result['original_language']}")
print(f"Summary: {result['summary']}")
```

### Language Detection

```python
from pipeline import detect_language

language = detect_language("هذا نص عربي")  # Returns 'ar'
language = detect_language("This is English")  # Returns 'en'
```

### Translation

```python
from pipeline import translate_to_english

# Translate Arabic
english = translate_to_english("مرحبا", 'ar')

# Translate French
english = translate_to_english("Bonjour", 'fr')
```

## Project Structure

```
multilingual-ai-news-summarizer/
├── scraper.py          # Multi-source web scraping (3 Lebanese sources)
├── pipeline.py         # AI pipeline (detection, translation, summarization)
├── demo.py             # Demo script showing complete workflow
├── test_sites.py       # Site compatibility testing
├── db.py               # Database caching (not yet done)
├── app.py              # Streamlit UI (not yet done)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Development Roadmap

- [x] Project structure and setup
- [x] Site compatibility testing
- [x] Multi-source web scraping (3 sources)
- [x] Language detection (Arabic/English/French)
- [x] Neural machine translation (Arabic/French to English)
- [x] AI-powered summarization (BART model)
- [x] Complete end-to-end pipeline
- [ ] SQLite caching layer
- [ ] Interactive Streamlit UI
- [ ] Cloud deployment
- [ ] Polish and optimization

## Models Used

| Task               | Model                      | Size   |
| ------------------ | -------------------------- | ------ |
| Arabic Translation | Helsinki-NLP/opus-mt-ar-en | ~300MB |
| French Translation | Helsinki-NLP/opus-mt-fr-en | ~300MB |
| Summarization      | facebook/bart-large-cnn    | ~1.6GB |

All models cached locally after first download.

## Performance

- **Language Detection**: <1s
- **Translation**: 1-3s per article
- **Summarization**: 1-2s per article
- **Total Pipeline**: 10-30s per article (after models cached)

## Use Case

Initially developed to address news accessibility in Lebanon's trilingual ecosystem (Arabic/English/French), but designed to work for any multilingual news region.

## Author

[Perla Thebian] - [GitHub](https://github.com/perlathebian)
