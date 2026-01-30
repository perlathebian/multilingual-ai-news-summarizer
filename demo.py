"""
Demo script showing complete URL-to-Summary workflow.

This demonstrates the multilingual news summarizer in action:
1. Scrapes article from URL
2. Detects language (Arabic/English/French)
3. Translates to English if needed
4. Generates AI summary

Usage:
    python demo.py
"""

from scraper import get_article
from pipeline import process_article, SUPPORTED_LANGUAGES


def demo():
    """
    Demonstrate complete pipeline with sample URLs.
    """
    print("="*70)
    print("MULTILINGUAL AI NEWS SUMMARIZER - DEMO")
    print("="*70)
    print("\nThis demo shows the complete workflow:")
    print("URL -> Scrape -> Detect Language -> Translate -> Summarize\n")
    
    # Sample URLs 
    demo_urls = [
        "https://www.naharnet.com/stories/en/317898-across-forgotten-walls-of-hong-kong-island-a-flock-of-bird-murals-rises",
        "https://www.mtv.com.lb/en/news/International/1628094/uk-court-jails-chinese-bitcoin-fraudster-for-over-11-years",
        "https://beirut-today.com/ar/2023/06/02/ar-corruption-health-sector-coronavirus-lebanon/"
    ]
    
    for i, url in enumerate(demo_urls, 1):
        print(f"\n{'='*70}")
        print(f"DEMO {i}/{len(demo_urls)}")
        print('='*70)
        print(f"URL: {url[:60]}...\n")
        
        # 1) Scrape
        print("Step 1: Scraping article...")
        article = get_article(url)
        
        if not article:
            print("Scraping failed, skipping to next article\n")
            continue
        
        print(f"Article scraped")
        print(f"   Title: {article['title'][:60]}...")
        print(f"   Source: {article.get('source', 'N/A')}")
        
        # 2) Process through AI pipeline
        print("\nStep 2: Processing through AI pipeline...")
        result = process_article(article, summary_max_length=100)
        
        if result:
            print(f"\n{'─'*70}")
            print("FINAL RESULT")
            print('─'*70)
            print(f"\n{result['title']}")
            print(f"Language: {SUPPORTED_LANGUAGES[result['original_language']]}")
            print(f"{result['date']}")
            print(f"\nSUMMARY:")
            print(f"{result['summary']}")
            print(f"\nProcessing time: {result['processing_time']}")
        else:
            print("Processing failed")
    
    print(f"\n{'='*70}")
    print("DEMO COMPLETE")
    print('='*70)
    print("\nTo use with your own URLs:")
    print("  1. Edit demo.py and replace demo_urls with your article URLs")
    print("  2. Run: python demo.py")
    print("\nSupported sources: Naharnet, MTV Lebanon, Beirut Today")
    print("Supported languages: Arabic, English, French")
    print('='*70 + "\n")


if __name__ == "__main__":
    demo()