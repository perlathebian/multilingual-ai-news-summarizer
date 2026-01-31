"""
Demo script showing complete URL-to-Summary workflow with caching.

This demonstrates the multilingual news summarizer in action:
1. Scrapes article from URL
2. Detects language (Arabic/English/French)
3. Translates to English if needed
4. Generates AI summary
5. Uses database caching for instant repeated requests

Usage:
    python demo.py
"""

from scraper import get_article
from pipeline import process_article_with_cache, SUPPORTED_LANGUAGES
import db
import time


def format_time(seconds):
    """Format time for better readability."""
    if seconds < 0.01:
        return f"{seconds*1000:.2f}ms"
    elif seconds < 1:
        return f"{seconds*1000:.0f}ms"
    else:
        return f"{seconds:.2f}s"


def demo():
    """
    Demonstrate complete pipeline with sample URLs and caching.
    """
    print("="*70)
    print("MULTILINGUAL AI NEWS SUMMARIZER - DEMO")
    print("="*70)
    print("\nThis demo shows the complete workflow:")
    print("URL -> Scrape -> Detect Language -> Translate -> Summarize -> Cache")
    print("\nWith caching for instant repeated requests!\n")
    
    # Initialize database
    db.init_db()
    
    # Sample URLs 
    demo_urls = [
        "https://www.mtv.com.lb/en/news/International/1628197/gold-gains-as-traders-bet-delayed-u-s--data-will-strengthen-rate-cut-outlook",
        "https://beirut-today.com/ar/2022/10/19/ar-can-gas-extraction-save-lebanon-from-its-financial-collapse/"
    ]
    
    for i, url in enumerate(demo_urls, 1):
        print(f"\n{'='*70}")
        print(f"DEMO {i}/{len(demo_urls)}")
        print('='*70)
        print(f"URL: {url[:60]}...\n")
        
        # Step 1: Scrape
        print("Step 1: Scraping article...")
        scrape_start = time.time()
        article = get_article(url)
        scrape_time = time.time() - scrape_start
        
        if not article:
            print("Scraping failed, skipping to next article\n")
            continue
        
        print(f"Article scraped in {format_time(scrape_time)}")
        print(f"   Title: {article['title'][:60]}...")
        print(f"   Source: {article.get('source', 'N/A')}")
        print(f"   Text length: {len(article['text']):,} characters")
        
        # Step 2: Process through AI pipeline with caching
        print(f"\nStep 2: Processing through AI pipeline...")
        print("   (Checking cache first...)")

        # Check if article is already cached BEFORE processing
        was_cached_before = db.article_exists(article['url'])

        process_start = time.time()
        result = process_article_with_cache(article, summary_max_length=100)
        process_time = time.time() - process_start

        if result:
            # Determine cache status
            # If article existed before processing, this was a cache hit
            was_cached = was_cached_before
            
            # Display results
            print(f"\n{'─'*70}")
            print("FINAL RESULT")
            print('─'*70)
            print(f"\n{result['title']}")
            print(f"Language: {SUPPORTED_LANGUAGES[result['original_language']]}")
            print(f"{result['date']}")
            print(f"\nSUMMARY:")
            print(f"{result['summary']}")
            print(f"\nProcessing time: {format_time(process_time)}")
            
            if was_cached:
                print(f"Retrieved from cache instantly!!")
            else:
                print(f"Processed and cached for future requests")
        else:
            print("Processing failed")
    
    # Show cache statistics
    print(f"\n{'='*70}")
    print("CACHE STATISTICS")
    print('='*70)
    
    stats = db.get_cache_stats()
    print(f"\nTotal cached articles: {stats['total_articles']}")
    
    if stats['by_language']:
        print(f"Languages: {', '.join(stats['by_language'].keys())}")
    
    if stats['by_source']:
        print(f"Sources: {', '.join(stats['by_source'].keys())}")
    
    print(f"\n{'='*70}")
    print("DEMO COMPLETE")
    print('='*70)


if __name__ == "__main__":
    demo()