"""
Database layer for caching processed articles.

Uses SQLite for persistent storage of scraped and AI-processed articles.
Prevents redundant API calls and provides instant retrieval of cached content.
"""

import sqlite3
from datetime import datetime
import os

# Database configuration
DB_NAME = 'articles.db'
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)


def get_connection():
    """
    Get database connection.
    
    Returns:
        sqlite3.Connection: Database connection object
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn


def init_db():
    """
    Initialize database and create articles table if it doesn't exist.
    
    Creates the database file and articles table with proper schema.
    Safe to call multiple times - won't recreate if already exists.
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create articles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            original_language TEXT NOT NULL,
            original_text TEXT NOT NULL,
            english_text TEXT,
            summary TEXT NOT NULL,
            date_published TEXT,
            date_processed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processing_time TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"Database initialized: {DB_PATH}")


def save_article(article_data):
    """
    Save processed article to database.
    
    Args:
        article_data (dict): Processed article from pipeline.process_article()
                            Must contain: url, source, title, original_language,
                            original_text, english_text, summary
    
    Returns:
        bool: True if saved successfully, False if error or duplicate
    """
    # Validate required fields
    required_fields = ['url', 'source', 'title', 'original_language', 
                      'original_text', 'summary']
    
    for field in required_fields:
        if field not in article_data or not article_data[field]:
            print(f"Missing required field: {field}")
            return False
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO articles (
                url, source, title, original_language, original_text,
                english_text, summary, date_published, processing_time
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article_data['url'],
            article_data['source'],
            article_data['title'],
            article_data['original_language'],
            article_data['original_text'],
            article_data.get('english_text'),  # May be None
            article_data['summary'],
            article_data.get('date', 'N/A'),
            article_data.get('processing_time', 'N/A')
        ))
        
        conn.commit()
        conn.close()
        
        print(f"Article saved to cache: {article_data['title'][:50]}...")
        return True
        
    except sqlite3.IntegrityError:
        # URL already exists in database
        print(f"Article already in cache: {article_data['url'][:50]}...")
        return False
    except Exception as e:
        print(f"Error saving to database: {e}")
        return False


def get_cached_article(url):
    """
    Retrieve cached article by URL.
    
    Args:
        url (str): Article URL
        
    Returns:
        dict: Article data if found, None if not in cache
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM articles WHERE url = ?
        ''', (url,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            # Convert Row object to dict
            article = {
                'id': row['id'],
                'url': row['url'],
                'source': row['source'],
                'title': row['title'],
                'original_language': row['original_language'],
                'original_text': row['original_text'],
                'english_text': row['english_text'],
                'summary': row['summary'],
                'date': row['date_published'],
                'date_processed': row['date_processed'],
                'processing_time': row['processing_time']
            }
            print(f"Cache hit: {article['title'][:50]}...")
            return article
        else:
            print(f"Cache miss: {url[:50]}...")
            return None
            
    except Exception as e:
        print(f"Error retrieving from cache: {e}")
        return None


def article_exists(url):
    """
    Check if article URL exists in cache.
    
    Args:
        url (str): Article URL to check
        
    Returns:
        bool: True if URL in cache, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM articles WHERE url = ?
        ''', (url,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
        
    except Exception as e:
        print(f"Error checking cache: {e}")
        return False


def get_all_articles(limit=None):
    """
    Get all cached articles, ordered by most recently processed.
    
    Args:
        limit (int, optional): Maximum number of articles to return
        
    Returns:
        list: List of article dicts, or empty list if none found
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        if limit:
            cursor.execute('''
                SELECT * FROM articles 
                ORDER BY date_processed DESC 
                LIMIT ?
            ''', (limit,))
        else:
            cursor.execute('''
                SELECT * FROM articles 
                ORDER BY date_processed DESC
            ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts
        articles = []
        for row in rows:
            articles.append({
                'id': row['id'],
                'url': row['url'],
                'source': row['source'],
                'title': row['title'],
                'original_language': row['original_language'],
                'original_text': row['original_text'],
                'english_text': row['english_text'],
                'summary': row['summary'],
                'date': row['date_published'],
                'date_processed': row['date_processed'],
                'processing_time': row['processing_time']
            })
        
        return articles
        
    except Exception as e:
        print(f"Error getting articles: {e}")
        return []


def get_cache_stats():
    """
    Get statistics about cached articles.
    
    Returns:
        dict: Cache statistics (total_articles, languages, sources)
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Total count
        cursor.execute('SELECT COUNT(*) FROM articles')
        total = cursor.fetchone()[0]
        
        # By language
        cursor.execute('''
            SELECT original_language, COUNT(*) 
            FROM articles 
            GROUP BY original_language
        ''')
        languages = {row[0]: row[1] for row in cursor.fetchall()}
        
        # By source
        cursor.execute('''
            SELECT source, COUNT(*) 
            FROM articles 
            GROUP BY source
        ''')
        sources = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total_articles': total,
            'by_language': languages,
            'by_source': sources
        }
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        return {'total_articles': 0, 'by_language': {}, 'by_source': {}}


def clear_cache():
    """
    Delete ALL cached articles from database.
    Use with caution - this cannot be undone!
    
    Returns:
        int: Number of articles deleted
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get count before deleting
        cursor.execute('SELECT COUNT(*) FROM articles')
        count = cursor.fetchone()[0]
        
        # Delete all
        cursor.execute('DELETE FROM articles')
        
        conn.commit()
        conn.close()
        
        print(f"Cache cleared: {count} articles deleted")
        return count
        
    except Exception as e:
        print(f"Error clearing cache: {e}")
        return 0


# ============================================================================
# TESTING FUNCTIONS
# ============================================================================

def test_database():
    """
    Test database functions with REAL scraped articles.
    """
    print("="*70)
    print("STEP 3: DATABASE TEST WITH REAL ARTICLES")
    print("="*70)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_db()
    
    # Import scraper and pipeline
    from scraper import get_article
    from pipeline import process_article
    
    # Test URLs 
    test_urls = [
        "https://www.naharnet.com/stories/en/317898-across-forgotten-walls-of-hong-kong-island-a-flock-of-bird-murals-rises",
        "https://www.mtv.com.lb/en/news/International/1628094/uk-court-jails-chinese-bitcoin-fraudster-for-over-11-years",
        "https://beirut-today.com/ar/2023/05/09/ar-beware-of-drinking-water-beirut/"
    ]
    
    print(f"\n2. Testing with {len(test_urls)} real articles...")
    print("="*70)
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{'─'*70}")
        print(f"Article {i}/{len(test_urls)}")
        print('─'*70)
        print(f"URL: {url[:60]}...")
        
        # Check if already cached
        if article_exists(url):
            print("Article already in cache, retrieving...")
            cached = get_cached_article(url)
            print(f"   Title: {cached['title'][:50]}...")
            print(f"   Summary: {cached['summary'][:100]}...")
        else:
            print("Article not cached, processing...")
            
            # Scrape article
            article = get_article(url)
            if not article:
                print("Scraping failed")
                continue
            
            # Process through AI pipeline
            result = process_article(article, summary_max_length=100)
            if not result:
                print("Processing failed")
                continue
            
            # Save to database
            saved = save_article(result)
            if saved:
                print(f"Article processed and cached")
                print(f"   Title: {result['title'][:50]}...")
                print(f"   Summary: {result['summary'][:100]}...")
    
    # Show cache statistics
    print(f"\n{'='*70}")
    print("CACHE STATISTICS")
    print('='*70)
    stats = get_cache_stats()
    print(f"Total articles in cache: {stats['total_articles']}")
    print(f"By language: {stats['by_language']}")
    print(f"By source: {stats['by_source']}")
    
    # List all cached articles
    print(f"\n{'='*70}")
    print("ALL CACHED ARTICLES")
    print('='*70)
    all_articles = get_all_articles()
    for i, article in enumerate(all_articles, 1):
        print(f"{i}. {article['title'][:50]}...")
        print(f"   Source: {article['source']} | Language: {article['original_language']} | Processed: {article['date_processed'][:19]}")
    
    # Test retrieval speed
    print(f"\n{'='*70}")
    print("CACHE SPEED TEST")
    print('='*70)
    if test_urls:
        test_url = test_urls[0]
        print(f"Retrieving cached article from: {test_url[:50]}...")
        
        import time
        start = time.time()
        cached = get_cached_article(test_url)
        elapsed = (time.time() - start) * 1000  # Convert to milliseconds
        
        if cached:
            print(f"Retrieved in {elapsed:.2f}ms")
            print(f"   Compare to: 2000-5000ms for full AI processing")
            print(f"   Speed improvement: {(2500/elapsed):.0f}x faster!")
    
    print(f"\n{'='*70}")
    print("DATABASE TEST COMPLETE")
    print('='*70)
    print("\nDatabase location: articles.db")
    print("To clear cache: from db import clear_cache; clear_cache()")
    print('='*70 + "\n")


if __name__ == "__main__":
    test_database()