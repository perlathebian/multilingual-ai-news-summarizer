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

### Data Collection

- **Python 3.11**: Core programming language
- **Requests**: HTTP requests to news websites
- **BeautifulSoup4**: Web scraping and HTML parsing

### AI/ML (Coming Soon)

- **HuggingFace Transformers**: Translation and summarization models
- **PyTorch**: Deep learning framework
- **LangDetect**: Language detection

### Application Layer (Coming Soon)

- **SQLite**: Caching processed articles
- **Streamlit**: Interactive web interface

## Current Features

### Web Scraping (Naharnet.com)

- Extracts article title from `<h1 itemprop="name">`
- Extracts article body from `<div itemprop="description">`
- Extracts publication date from `<abbr class="timeago">`
- Filters out short text (ads, captions, navigation)
- Respectful rate limiting (1-3 seconds delay between requests)
- 350-second timeout for slow servers
- Comprehensive error handling

## Use Case

Initially developed to address news accessibility in Lebanon's trilingual ecosystem, but designed to work for any multilingual news region.

## Installation

```bash
# Clone repository
git clone https://github.com/perlathebian/multilingual-ai-news-summarizer.git
cd multilingual-ai-news-summarizer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Test the Scraper

```bash
# Edit scraper.py and update the test_url with an actual article URL
python scraper.py
```

## Development Roadmap

- [x] Project structure and setup
- [x] Single-source web scraping
- [ ] Multi-source web scraping
- [ ] Language detection
- [ ] Arabic ↔ English translation
- [ ] French ↔ English translation
- [ ] AI-powered summarization
- [ ] SQLite caching layer
- [ ] Interactive Streamlit UI
- [ ] Cloud deployment

## Project Structure

```
multilingual-ai-news-summarizer/
├── scraper.py          # Web scraping logic
├── pipeline.py         # AI translation/summarization (coming soon)
├── db.py              # SQLite database functions (coming soon)
├── app.py             # Streamlit web app (coming soon)
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Author

Perla Thebian - [GitHub](https://github.com/perlathebian)

Built to demonstrate production-ready ML engineering skills.
