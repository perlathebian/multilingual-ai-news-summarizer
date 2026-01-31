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

## Quick Demo Output

Want to see it in action without running the code? Here's what happens:

<details>
<summary>Click to see demo output</summary>

**First Run (Cache Miss - Full Processing):**

```
======================================================================
MULTILINGUAL AI NEWS SUMMARIZER - DEMO
======================================================================

This demo shows the complete workflow:
URL -> Scrape -> Detect Language -> Translate -> Summarize -> Cache

With caching for instant repeated requests!

Database initialized: c:\Users\BC\Desktop\multilingual-ai-news-summarizer\articles.db

======================================================================
DEMO 1/2
======================================================================
URL: https://www.mtv.com.lb/en/news/International/1628197/gold-ga...

Step 1: Scraping article...
Fetching: https://www.mtv.com.lb/en/news/International/1628197/gold-gains-as-traders-bet-delayed-u-s--data-will-strengthen-rate-cut-outlook
Successfully extracted from MTV Lebanon
   Title: Gold gains as traders bet delayed U.S. data will strengthen ...
   Text length: 1,823 characters
   Date: 12 Nov 202511:52 AM
Article scraped in 7.47s
   Title: Gold gains as traders bet delayed U.S. data will strengthen ...
   Source: MTV Lebanon
   Text length: 1,823 characters

Step 2: Processing through AI pipeline...
   (Checking cache first...)

======================================================================
CACHE-AWARE PROCESSING
======================================================================
URL: https://www.mtv.com.lb/en/news/International/1628197/gold-ga...

Checking cache...
Cache miss: https://www.mtv.com.lb/en/news/International/16281...
Cache Miss - Article not in cache

──────────────────────────────────────────────────────────────────────
Processing through AI pipeline...
──────────────────────────────────────────────────────────────────────

======================================================================
PROCESSING ARTICLE THROUGH AI PIPELINE
======================================================================

Article: Gold gains as traders bet delayed U.S. data will strengthen ...
   Source: MTV Lebanon
   URL: https://www.mtv.com.lb/en/news/International/16281...

──────────────────────────────────────────────────────────────────────
STEP 1: Language Detection
──────────────────────────────────────────────────────────────────────
Detected language: English (en)

──────────────────────────────────────────────────────────────────────
STEP 2: Translation
──────────────────────────────────────────────────────────────────────

──────────────────────────────────────────────────────────────────────
STEP 3: Summarization
──────────────────────────────────────────────────────────────────────
Loading summarization model (first time only, ~10 min)...
   Model: facebook/bart-large-cnn
C:\Users\BC\Desktop\multilingual-ai-news-summarizer\venv\Lib\site-packages\huggingface_hub\file_download.py:942: FutureWarning: `resume_download` is deprecated and will be removed in version 1.0.0. Downloads always resume when possible. If you want to force a new download, use `force_download=True`.
  warnings.warn(
Model loaded in 8.8 seconds
Generating summary...
   Input length: 1823 characters
Summary generated (276 characters)

======================================================================
PROCESSING COMPLETE
======================================================================
Original language: English
Summary generated: 276 characters
Total processing time: 23.5s
======================================================================

──────────────────────────────────────────────────────────────────────
Saving to cache...
──────────────────────────────────────────────────────────────────────
Database initialized: c:\Users\BC\Desktop\multilingual-ai-news-summarizer\articles.db
Article saved to cache: Gold gains as traders bet delayed U.S. data will s...
Result cached for future requests
======================================================================

──────────────────────────────────────────────────────────────────────
FINAL RESULT
──────────────────────────────────────────────────────────────────────

Gold gains as traders bet delayed U.S. data will strengthen rate cut outlook
Language: English
12 Nov 202511:52 AM

SUMMARY:
Spot gold was up 0.1% at $4,118.58 per ounce, having earlier hit its highest since October 23. Gold, traditionally considered a safe haven, also tends to benefit in low-interest rate environments. Markets see a 64% chance of a rate cut in December, CME's FedWatch Tool showed.

Processing time: 23.50s
Processed and cached for future requests

======================================================================
DEMO 2/2
======================================================================
URL: https://beirut-today.com/ar/2022/10/19/ar-can-gas-extraction...

Step 1: Scraping article...
Fetching: https://beirut-today.com/ar/2022/10/19/ar-can-gas-extraction-save-lebanon-from-its-financial-collapse/
Successfully extracted from Beirut Today
   Title: الغاز بأفضل السيناريوهات ليس كافيًا لحل الأزمة المالية: الإص...
   Text length: 6,145 characters
   Date: أكتوبر 19, 2022
Article scraped in 5.11s
   Title: الغاز بأفضل السيناريوهات ليس كافيًا لحل الأزمة المالية: الإص...
   Source: Beirut Today
   Text length: 6,145 characters

Step 2: Processing through AI pipeline...
   (Checking cache first...)

======================================================================
CACHE-AWARE PROCESSING
======================================================================
URL: https://beirut-today.com/ar/2022/10/19/ar-can-gas-extraction...

Checking cache...
Cache miss: https://beirut-today.com/ar/2022/10/19/ar-can-gas-...
Cache Miss - Article not in cache

──────────────────────────────────────────────────────────────────────
Processing through AI pipeline...
──────────────────────────────────────────────────────────────────────

======================================================================
PROCESSING ARTICLE THROUGH AI PIPELINE
======================================================================

Article: الغاز بأفضل السيناريوهات ليس كافيًا لحل الأزمة المالية: الإص...
   Source: Beirut Today
   URL: https://beirut-today.com/ar/2022/10/19/ar-can-gas-...

──────────────────────────────────────────────────────────────────────
STEP 1: Language Detection
──────────────────────────────────────────────────────────────────────
Detected language: Arabic (ar)

──────────────────────────────────────────────────────────────────────
STEP 2: Translation
──────────────────────────────────────────────────────────────────────
Loading Arabic_to_English model (first time only, ~5 min)...
   Model: Helsinki-NLP/opus-mt-ar-en
C:\Users\BC\Desktop\multilingual-ai-news-summarizer\venv\Lib\site-packages\transformers\models\marian\tokenization_marian.py:197: UserWarning: Recommended: pip install sacremoses.
  warnings.warn("Recommended: pip install sacremoses.")
Model loaded in 3.6 seconds
Translating Arabic to English...
Translation complete (5411 chars)

──────────────────────────────────────────────────────────────────────
STEP 3: Summarization
──────────────────────────────────────────────────────────────────────
Generating summary...
   Input length: 5411 characters
   Text is long, using first 4000 characters
Summary generated (315 characters)

======================================================================
PROCESSING COMPLETE
======================================================================
Original language: Arabic
Summary generated: 315 characters
Total processing time: 86.3s
======================================================================

──────────────────────────────────────────────────────────────────────
Saving to cache...
──────────────────────────────────────────────────────────────────────
Database initialized: c:\Users\BC\Desktop\multilingual-ai-news-summarizer\articles.db
Article saved to cache: الغاز بأفضل السيناريوهات ليس كافيًا لحل الأزمة الم...
Result cached for future requests
======================================================================

──────────────────────────────────────────────────────────────────────
FINAL RESULT
──────────────────────────────────────────────────────────────────────

الغاز بأفضل السيناريوهات ليس كافيًا لحل الأزمة المالية: الإصلاح أولًا
Language: Arabic
أكتوبر 19, 2022

SUMMARY:
Lebanon has not entered the oil-state club as politicians try to inspire Lebanon. Politicians sell illusions to hopeful Lebanese to resolve their crises. Total's gas exploration in Block 9, where Qana's border field is located. The promised oil and gas wealth, if properly anticipated, will not fill a huge deficit.

Processing time: 86.41s
Processed and cached for future requests

======================================================================
CACHE STATISTICS
======================================================================

Total cached articles: 8
Languages: ar, en
Sources: Beirut Today, MTV Lebanon

======================================================================
CACHE STATISTICS
======================================================================

Total cached articles: 8
Languages: ar, en
Sources: Beirut Today, MTV Lebanon

Sources: Beirut Today, MTV Lebanon

======================================================================
DEMO COMPLETE
======================================================================
```

</details>

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

### Database Caching Layer

**Performance Optimization:**

- SQLite database for persistent article storage
- Automatic cache checking before AI processing
- Instant retrieval of previously processed articles
- 1,000-10,000x speedup for cached requests

**Cache Management:**

- Duplicate prevention via URL uniqueness
- Cache statistics and analytics
- CRUD operations (Create, Read, Delete)
- Persistent storage across sessions

**Processing Flow:**

```
Request → Check Cache → Found? Return (instant) : Process → Save → Return
```

**Performance Metrics:**

- First request (cache miss): 40-90 seconds (full AI processing)
- Repeat request (cache hit): 10-50 milliseconds (database retrieval)
- Typical speedup: 2,000-5,000x faster

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

### Data Storage

- **SQLite**: Persistent caching with CRUD operations

### Coming Soon

- **Streamlit**: Interactive web interface

## Database Schema

### Articles Table

| Column              | Type                | Description                               |
| ------------------- | ------------------- | ----------------------------------------- |
| `id`                | INTEGER PRIMARY KEY | Auto-increment ID                         |
| `url`               | TEXT UNIQUE         | Article URL (prevents duplicates)         |
| `source`            | TEXT                | News source (Naharnet, MTV, etc.)         |
| `title`             | TEXT                | Article title                             |
| `original_language` | TEXT                | Detected language (ar/en/fr)              |
| `original_text`     | TEXT                | Full article text                         |
| `english_text`      | TEXT                | Translated text (NULL if already English) |
| `summary`           | TEXT                | AI-generated summary                      |
| `date_published`    | TEXT                | Article publication date                  |
| `date_processed`    | TIMESTAMP           | When article was cached                   |
| `processing_time`   | TEXT                | Processing duration                       |

**Key Features:**

- `url` has UNIQUE constraint - prevents duplicate processing
- Automatic indexing on primary key and unique columns
- Stores both original and processed content
- Tracks processing metadata for analytics

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
├── scraper.py          # Multi-source web scraping
├── pipeline.py         # AI pipeline with caching integration
├── db.py               # SQLite database layer (CRUD operations)
├── demo.py             # Quick demo script
├── cache_demo.py       # Cache performance demonstration
├── test_sites.py       # Site compatibility testing
├── app.py              # Streamlit UI (coming Day 5)
├── requirements.txt    # Python dependencies
├── articles.db         # SQLite database (auto-generated, not in git)
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
- [x] SQLite caching layer with CRUD operations
- [x] Cache performance demonstration
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
