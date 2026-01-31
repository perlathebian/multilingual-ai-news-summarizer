"""
Cache Performance Demonstration

This script demonstrates the performance improvement from database caching.
Shows before/after comparisons and cache statistics.

Usage:
    python cache_demo.py
"""

from scraper import get_article
from pipeline import process_article_with_cache
import db
import time


def format_time(seconds):
    """Format time in seconds or milliseconds for better readability."""
    if seconds < 0.01:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.2f}s"


def demo_cache_performance():
    """
    Demonstrate cache performance with real articles.
    Shows timing for cache miss vs cache hit.
    """
    print("="*70)
    print("CACHE PERFORMANCE DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows the performance impact of database caching")
    print("when processing news articles through the AI pipeline.\n")
    
    # Initialize database
    db.init_db()
    
    # Test URLs 
    test_urls = [
        {
            'name': 'Beirut Today Article',
            'url': 'https://beirut-today.com/ar/2023/03/01/ar-sustainable-development-goals-chat-gpt/'
        },
        {
            'name': 'MTV Lebanon Article',
            'url': 'https://www.mtv.com.lb/en/news/International/1629710/bitcoin-slides-below--90-000-as-traders-grow-cautious'
        },
    ]
    
    print("Testing with 2 articles from different sources...\n")
    
    results = []
    
    for i, article_info in enumerate(test_urls, 1):
        print("="*70)
        print(f"ARTICLE {i}: {article_info['name']}")
        print("="*70)
        print(f"URL: {article_info['url'][:60]}...\n")
        
        # ====================================================================
        # FIRST REQUEST: Cache Miss or Cache Hit?
        # ====================================================================
        
        print("─"*70)
        print("FIRST REQUEST")
        print("─"*70)
        
        # Scrape article
        print("Scraping article...")
        scrape_start = time.time()
        article = get_article(article_info['url'])
        scrape_time = time.time() - scrape_start
        
        if not article:
            print("Scraping failed, skipping...\n")
            continue
        
        print(f"Scraped in {format_time(scrape_time)}")
        print(f"   Title: {article['title'][:50]}...\n")
        
        # Process with cache
        print("Processing with cache check...")
        process_start = time.time()
        result1 = process_article_with_cache(article, summary_max_length=100)
        process_time1 = time.time() - process_start
        
        if not result1:
            print("Processing failed, skipping...\n")
            continue
        
        # Check if it was a cache hit or miss
        # Cache hits are typically 0.01-0.05s, cache misses are 40-90s
        status1 = "Cache HIT" if process_time1 < 5 else "Cache MISS"

        print(f"\nFirst request: {format_time(process_time1)} [{status1}]")
        
        # ====================================================================
        # SECOND REQUEST: Should be Cache Hit
        # ====================================================================
        
        print(f"\n{'─'*70}")
        print("SECOND REQUEST (Same Article)")
        print("─"*70)
        print("Processing same article again...\n")
        
        process_start = time.time()
        result2 = process_article_with_cache(article, summary_max_length=100)
        process_time2 = time.time() - process_start

        if result2:
            print(f"\nSecond request: {format_time(process_time2)} [Cache HIT]")
        else:
            print(f"\nSecond request failed")
        
        # ====================================================================
        # COMPARISON
        # ====================================================================
        
        print(f"\n{'─'*70}")
        print("PERFORMANCE COMPARISON")
        print("─"*70)
        
        if process_time1 >= 1:  # Was a cache miss
            speedup = process_time1 / process_time2 if process_time2 > 0 else 0
            time_saved = process_time1 - process_time2
            
            print(f"\n1st Request (Cache Miss): {format_time(process_time1):>12}")
            print(f"2nd Request (Cache Hit):  {format_time(process_time2):>12}")
            print(f"\nSpeedup: {speedup:,.0f}x faster")
            print(f"Time saved: {format_time(time_saved)}")
        else:  # Both were cache hits
            print(f"\nBoth requests were cache hits (article already processed)")
            print(f"1st Request: {format_time(process_time1)}")
            print(f"2nd Request: {format_time(process_time2)}")
        
        results.append({
            'name': article_info['name'],
            'url': article_info['url'],
            'first_time': process_time1,
            'second_time': process_time2,
            'scrape_time': scrape_time
        })
        
        print()
    
    # ========================================================================
    # OVERALL STATISTICS
    # ========================================================================
    
    print("="*70)
    print("OVERALL CACHE STATISTICS")
    print("="*70)
    
    stats = db.get_cache_stats()
    
    print(f"\nTotal articles in cache: {stats['total_articles']}")
    
    if stats['by_language']:
        print(f"\nBy language:")
        for lang, count in stats['by_language'].items():
            lang_names = {'ar': 'Arabic', 'en': 'English', 'fr': 'French'}
            print(f"   • {lang_names.get(lang, lang)}: {count}")
    
    if stats['by_source']:
        print(f"\nBy source:")
        for source, count in stats['by_source'].items():
            print(f"   • {source}: {count}")
    
    # Calculate total time saved
    total_saved = sum(r['first_time'] - r['second_time'] 
                     for r in results 
                     if r['first_time'] >= 1)
    
    if total_saved > 0:
        print(f"\nTotal time saved across {len(results)} articles: {format_time(total_saved)}")
    
    print("\n" + "="*70)
    print("KEY TAKEAWAYS")
    print("="*70)
    print("""
 First request (Cache Miss):
   • Scrapes article from website (~1-3s)
   • Processes through AI pipeline (~40-80s on CPU)
   • Saves result to database
   • Total: ~50-90 seconds

 Subsequent requests (Cache Hit):
   • Retrieves from database (~0.01-0.05s)
   • No scraping needed
   • No AI processing needed
   • Total: ~10-50 milliseconds

 Performance Improvement: 2,000-10,000x faster!

 Why This Matters:
   • Better user experience (instant results)
   • Reduced server load (no redundant AI calls)
   • Lower costs (if using paid AI APIs)
   • Professional optimization practice
""")
    print("="*70 + "\n")


def demo_cache_management():
    """
    Demonstrate cache management features.
    """
    print("="*70)
    print("CACHE MANAGEMENT DEMONSTRATION")
    print("="*70)
    
    # Get all cached articles
    print("\n1. Viewing all cached articles:")
    print("─"*70)
    
    articles = db.get_all_articles(limit=5)
    
    if articles:
        for i, article in enumerate(articles, 1):
            print(f"\n{i}. {article['title'][:60]}...")
            print(f"   Source: {article['source']}")
            print(f"   Language: {article['original_language']}")
            print(f"   Cached: {article['date_processed'][:19]}")
            print(f"   Summary: {article['summary'][:80]}...")
    else:
        print("\nNo articles in cache yet. Run the performance demo first.")
    
    # Show cache stats
    print(f"\n{'─'*70}")
    print("2. Cache statistics:")
    print("─"*70)
    
    stats = db.get_cache_stats()
    print(f"\nTotal articles: {stats['total_articles']}")
    print(f"Languages: {', '.join(stats['by_language'].keys()) if stats['by_language'] else 'None'}")
    print(f"Sources: {', '.join(stats['by_source'].keys()) if stats['by_source'] else 'None'}")
    
    # Database file info
    print(f"\n{'─'*70}")
    print("3. Database file information:")
    print("─"*70)
    
    import os
    if os.path.exists('articles.db'):
        size = os.path.getsize('articles.db')
        size_kb = size / 1024
        print(f"\nDatabase file: articles.db")
        print(f"Size: {size_kb:.2f} KB ({size:,} bytes)")
        print(f"Location: {os.path.abspath('articles.db')}")
    else:
        print("\nDatabase file not found. Run performance demo first.")
    
    print("\n" + "="*70)
    print("CACHE MANAGEMENT OPTIONS")
    print("="*70)
    print("""
Available operations:

1. View cached articles:
   from db import get_all_articles
   articles = get_all_articles()

2. Get cache statistics:
   from db import get_cache_stats
   stats = get_cache_stats()

3. Check if article is cached:
   from db import article_exists
   exists = article_exists(url)

4. Clear entire cache:
   from db import clear_cache
   clear_cache()  # Warning: Cannot be undone!

5. Retrieve specific article:
   from db import get_cached_article
   article = get_cached_article(url)
""")
    print("="*70 + "\n")


def main():
    """
    Main demo function - runs all demonstrations.
    """
    print("\n" + "="*70)
    print("MULTILINGUAL NEWS SUMMARIZER - CACHE DEMONSTRATION")
    print("="*70)
    print("\nThis demo shows:")
    print("  1. Cache performance (before/after comparison)")
    print("  2. Cache management (viewing, statistics)")
    print("\n" + "="*70 + "\n")
    
    # Demo 1: Performance
    demo_cache_performance()
    
    input("\nPress Enter to continue to cache management demo...")
    print()
    
    # Demo 2: Management
    demo_cache_management()
    
    print("Demo complete!!!!\n")


if __name__ == "__main__":
    main()