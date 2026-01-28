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

def get_article(url):
    """
    Fetch and extract article content from a given URL.
    
    Args:
        url (str): The URL of the news article
        
    Returns:
        dict: Dictionary containing title, text, and date (if available)
              Returns None if extraction fails
    """
    try:
        # Add delay to be respectful to the server
        time.sleep(3)
        
        # Fetch the webpage
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise error for bad status codes
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract article data
        article_data = {
            'url': url,
            'title': None,
            'text': None,
            'date': None
        }
        
        # Try to find title (common patterns)
        title = None
        title = soup.find('h1')
        if not title:
            title = soup.find('h1', class_='article-title')
        if not title:
            title = soup.find(class_='article-title')
        
        if title:
            article_data['title'] = title.get_text(strip=True)
        
        # Try to find article body (common patterns)
        article_body = None
        
        # Try common article body class names
        article_body = soup.find('div', class_='article-body')
        if not article_body:
            article_body = soup.find('div', class_='article-content')
        if not article_body:
            article_body = soup.find('article')
        if not article_body:
            article_body = soup.find('div', class_='entry-content')
        
        # If we found the body, extract all paragraphs
        if article_body:
            paragraphs = article_body.find_all('p')
            text = ' '.join([p.get_text(strip=True) for p in paragraphs])
            article_data['text'] = text
        
        # Try to find publication date (optional)
        date = soup.find('time')
        if not date:
            date = soup.find(class_='date')
        if not date:
            date = soup.find(class_='published')
        
        if date:
            article_data['date'] = date.get_text(strip=True)
        
        # Validate we got essential data
        if article_data['title'] and article_data['text']:
            print(f"Successfully extracted: {article_data['title'][:50]}...")
            return article_data
        else:
            print("Failed to extract article content")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def clean_text(text):
    """
    Clean extracted text by removing extra whitespace and unwanted characters.
    
    Args:
        text (str): Raw text from article
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # TODO
    # Remove common unwanted patterns 
    
    return text


def test_scraper():
    """
    Test function to verify scraper works with a sample article.
    """
    # Test URL
    test_url = "https://www.naharnet.com/stories/en/317898-across-forgotten-walls-of-hong-kong-island-a-flock-of-bird-murals-rises"
    
    print("="*60)
    print("TESTING SCRAPER")
    print("="*60)
    print(f"\nTest URL: {test_url}")
    print("-"*60)
    
    article = get_article(test_url)
    
    if article:
        print("\n" + "="*60)
        print("EXTRACTION RESULTS")
        print("="*60)
        print(f"\nTitle: {article['title']}")
        print(f"\nDate: {article['date']}")
        print(f"\nText Preview (first 300 chars):")
        print(article['text'][:300] + "...")
        print(f"\nFull text length: {len(article['text'])} characters")
        print("\n" + "="*60)
    else:
        print("\nScraping failed. Check the URL and HTML structure.")


if __name__ == "__main__":
    test_scraper()