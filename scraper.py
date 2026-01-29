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
    Currently optimized for Naharnet.com structure.
    
    Args:
        url (str): The URL of the news article
        
    Returns:
        dict: Dictionary containing title, text, and date (if available)
              Returns None if extraction fails
    """
    try:
        # Rate limiting - be respectful to server
        time.sleep(1)
        
        # Fetch the webpage
        print(f"Fetching: {url}")
        response = requests.get(url, headers=HEADERS, timeout=50)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize article data
        article_data = {
            'url': url,
            'title': None,
            'text': None,
            'date': None
        }
        
        # NAHARNET-SPECIFIC: Extract title from <h1 itemprop="name">
        title = soup.find('h1', itemprop='name')
        if not title:
            title = soup.find('h1')  # Fallback to any h1
        
        if title:
            article_data['title'] = title.get_text(strip=True)
        
        # NAHARNET-SPECIFIC: Extract article body from <div itemprop="description">
        article_body = soup.find('div', itemprop='description')
        
        if article_body:
            paragraphs = article_body.find_all('p')
            
            # Filter out short paragraphs (captions/ads)
            text_parts = []
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 50:
                    text_parts.append(text)
            
            article_data['text'] = ' '.join(text_parts)
        
        # NAHARNET-SPECIFIC: Extract date from <abbr class="timeago">
        date = soup.find('abbr', class_='timeago')
        if date:
            article_data['date'] = date.get_text(strip=True)
        
        # Validate we got essential data
        if article_data['title'] and article_data['text']:
            print(f"Successfully extracted: {article_data['title'][:60]}...")
            print(f"   Text length: {len(article_data['text'])} characters")
            if article_data['date']:
                print(f"   Date: {article_data['date']}")
            return article_data
        else:
            print("Failed to extract article content")
            print(f"   Title found: {bool(article_data['title'])}")
            print(f"   Text found: {bool(article_data['text'])}")
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