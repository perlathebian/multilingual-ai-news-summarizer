"""
Web scraper for extracting news articles from news sources.
"""

import requests
from bs4 import BeautifulSoup
import time

# User-Agent to identify myself to the website
HEADERS = {
    'User-Agent': 'MultilinguaNewsAI/1.0 (Educational; +https://github.com/perlathebian/multilingual-ai-news-summarizer)'
}

# HELPER FUNCTIONS
def _fetch_and_parse(url):
    """
    Fetch webpage and parse with BeautifulSoup.
    
    Args:
        url (str): URL to fetch
        
    Returns:
        BeautifulSoup: Parsed HTML soup object
        None: If fetch fails
        
    Raises:
        All exceptions are caught and None is returned
    """
    try:
        time.sleep(3)  # Rate limiting - respectful
        
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=100)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
        
    except requests.exceptions.Timeout:
        print(f"Timeout: Server took too long to respond")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return None

def _extract_paragraphs(container, min_length=50):
    """
    Extract and filter paragraphs from a container element.
    
    Args:
        container: BeautifulSoup element containing paragraphs
        min_length (int): Minimum paragraph length to include (filters ads/captions)
        
    Returns:
        str: Joined paragraph text
    """
    if not container:
        return None
    
    paragraphs = container.find_all('p')
    
    text_parts = []
    for p in paragraphs:
        text = p.get_text(strip=True)
        if len(text) > min_length:
            text_parts.append(text)
    
    return '\n\n'.join(text_parts) if text_parts else None

def _validate_and_report(article_data, source_name):
    """
    Validate extracted data and print status report.
    
    Args:
        article_data (dict): Article data with title, text, date
        source_name (str): Name of news source for reporting
        
    Returns:
        dict: article_data if valid, None if invalid
    """
    if article_data['title'] and article_data['text']:
        print(f"Successfully extracted from {source_name}")
        print(f"   Title: {article_data['title'][:60]}...")
        print(f"   Text length: {len(article_data['text']):,} characters")
        if article_data['date']:
            print(f"   Date: {article_data['date']}")
        return article_data
    else:
        print(f"Failed to extract from {source_name}")
        print(f"   Title found: {bool(article_data['title'])}")
        print(f"   Text found: {bool(article_data['text'])}")
        return None

# SITE-SPECIFIC SCRAPER FUNCTIONS
def scrape_naharnet(url):
    """
    Extract article from Naharnet.com
    
    HTML Structure:
    - Title: <h1 itemprop="name">
    - Body: <div itemprop="description">
    - Date: <abbr class="timeago">
    """
    soup = _fetch_and_parse(url)
    if not soup:
        return None
    
    article_data = {
        'url': url,
        'source': 'Naharnet',
        'title': None,
        'text': None,
        'date': None
    }
    
    # Extract title
    title = soup.find('h1', itemprop='name')
    if not title:
        title = soup.find('h1')
    if title:
        article_data['title'] = title.get_text(strip=True)
    
    # Extract article body
    article_body = soup.find('div', itemprop='description')
    article_data['text'] = _extract_paragraphs(article_body)
    
    # Extract date
    date = soup.find('abbr', class_='timeago')
    if date:
        article_data['date'] = date.get_text(strip=True)
    
    return _validate_and_report(article_data, 'Naharnet')

def scrape_mtv(url):
    """
    Extract article from MTV Lebanon (mtv.com.lb)
    
    HTML Structure:
    - Title: <div class="section-header-text">
    - Body: <div class="articles-report">
    - Date: <div class="articles-header-date">
    """
    soup = _fetch_and_parse(url)
    if not soup:
        return None
    
    article_data = {
        'url': url,
        'source': 'MTV Lebanon',
        'title': None,
        'text': None,
        'date': None
    }
    
    # Extract title
    title = soup.find('div', class_='section-header-text')
    if not title:
        title = soup.find('div', id='title') 
    if title:
        article_data['title'] = title.get_text(strip=True)
    
    # Extract article body - MTV has different structure, use raw text extraction
    article_body = soup.find('div', class_='articles-report')
    if article_body:
        # Get text with line breaks, then split and filter
        raw_text = article_body.get_text(separator="\n", strip=True)
        paragraphs = [line.strip() for line in raw_text.split("\n") if line.strip()]
        
        text_parts = [text for text in paragraphs if len(text) > 50]
        article_data['text'] = '\n\n'.join(text_parts) if text_parts else None
    
    # Extract date
    date = soup.find('div', class_='articles-header-date')
    if date:
        article_data['date'] = date.get_text(strip=True)
    
    return _validate_and_report(article_data, 'MTV Lebanon')


def scrape_beirut_today(url):
    """
    Extract article from Beirut Today (beirut-today.com)
    
    HTML Structure:
    - Title: <h1 class="title">
    - Body: <div class="entry-content">
    - Date: <time class="entry-date">
    """
    soup = _fetch_and_parse(url)
    if not soup:
        return None
    
    article_data = {
        'url': url,
        'source': 'Beirut Today',
        'title': None,
        'text': None,
        'date': None
    }
    
    # Extract title
    title = soup.find('h1', class_='title')
    if not title:
        title = soup.find('div', id='title')
    if title:
        article_data['title'] = title.get_text(strip=True)
    
    # Extract article body
    article_body = soup.find('div', class_='entry-content')
    article_data['text'] = _extract_paragraphs(article_body)
    
    # Extract date
    date = soup.find('time', class_='entry-date')
    if date:
        article_data['date'] = date.get_text(strip=True)
    
    return _validate_and_report(article_data, 'Beirut Today')

def get_article(url):
    """
    Smart dispatcher - routes URL to appropriate site-specific scraper.
    
    Args:
        url (str): Article URL
        
    Returns:
        dict: Article data (title, text, date, url, source) or None if failed
    """
    if 'naharnet.com' in url:
        return scrape_naharnet(url)
    elif 'mtv.com.lb' in url:
        return scrape_mtv(url)
    elif 'beirut-today.com' in url:
        return scrape_beirut_today(url)
    else:
        print(f"Unsupported site: {url}")
        print(f"   Supported sites: Naharnet, MTV Lebanon, Beirut Today")
        return None

def clean_text(text):
    """
    Clean extracted text by removing extra whitespace and unwanted patterns.
    
    Args:
        text (str): Raw text from article
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove common navigation/social media text
    unwanted_phrases = [
        'Share on Facebook',
        'Tweet this',
        'Share on Twitter',
        'Share on LinkedIn',
        'Email this',
        'Print this',
        'Read more',
        'Click here',
        'Advertisement',
        'Subscribe now',
        'Sign up for',
    ]
    
    for phrase in unwanted_phrases:
        text = text.replace(phrase, '')
    
    # Clean up any double spaces created by removals
    text = ' '.join(text.split())
    
    return text


def test_scraper():
    """
    Test function to verify all scrapers work correctly.
    """
    print("\n" + "="*70)
    print("MULTI-SOURCE SCRAPER TEST")
    print("="*70)
    
    # Test URLs for each source
    test_urls = [
        ("Naharnet", "https://www.naharnet.com/stories/en/317898-across-forgotten-walls-of-hong-kong-island-a-flock-of-bird-murals-rises"),
        ("MTV Lebanon", "https://www.mtv.com.lb/en/news/International/1628094/uk-court-jails-chinese-bitcoin-fraudster-for-over-11-years"),
        ("Beirut Today", "https://beirut-today.com/2025/08/06/climate-issues-are-no-longer-ignorable-in-crisis-ridden-lebanon/"),
    ]
    
    results = []
    for source_name, url in test_urls:
        print(f"\n{'─'*70}")
        print(f"Testing: {source_name}")
        print(f"{'─'*70}")
        
        article = get_article(url)
        results.append((source_name, article is not None))
        
        if article:
            print(f"\nRESULTS:")
            print(f"   Title: {article['title']}")
            print(f"   Date: {article['date']}")
            print(f"   Text preview: {article['text'][:150]}...")
        
        print()  
    
    print("="*70)
    print("TEST SUMMARY")
    print("="*70)
    successful = sum(1 for _, success in results if success)
    print(f"Passed: {successful}/{len(results)}")
    for source, success in results:
        status = "Success" if success else "Fail"
        print(f"   {status} {source}")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_scraper()