"""
Quick script to test which Lebanese news sites allow scraping
(before building site-specific scrapers)
"""

import requests
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
    'Referer': 'https://www.google.com/',
    'X-Purpose': 'Educational portfolio project - github.com/perlathebian/multilingual-ai-news-summarizer'
}

def test_site(site_name, url):
    """
    Testing if a site allows scraping.
    
    Returns:
        dict: Status, response code, content length, and accessibility
    """
    print(f"\n{'='*60}")
    print(f"Testing: {site_name}")
    print(f"URL: {url}")
    print('='*60)
    
    try:
        time.sleep(3)  # Respectful
        
        response = requests.get(url, headers=HEADERS, timeout=50)
        
        result = {
            'site': site_name,
            'url': url,
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'content_length': len(response.text),
            'error': None
        }
        
        if response.status_code == 200:
            print(f"SUCCESS")
            print(f"   Status: {response.status_code}")
            print(f"   Content length: {len(response.text):,} characters")
            print(f"   This site is scrapable!")
        elif response.status_code == 403:
            print(f"BLOCKED (403 Forbidden)")
            print(f"   This site has anti-bot protection")
            result['error'] = '403 Forbidden'
        elif response.status_code == 404:
            print(f"NOT FOUND (404)")
            print(f"   Check if URL is correct")
            result['error'] = '404 Not Found'
        else:
            print(f"Unexpected status: {response.status_code}")
            result['error'] = f'Status {response.status_code}'
        
        return result
        
    except requests.exceptions.Timeout:
        print(f"TIMEOUT")
        print(f"   Server took too long to respond")
        return {
            'site': site_name,
            'url': url,
            'success': False,
            'error': 'Timeout'
        }
    except requests.exceptions.RequestException as e:
        print(f"ERROR: {e}")
        return {
            'site': site_name,
            'url': url,
            'success': False,
            'error': str(e)
        }


def main():
    """Tests all candidate Lebanese news sites."""
    
    print("\n" + "="*60)
    print("LEBANESE NEWS SITES COMPATIBILITY TEST")
    print("="*60)
    print("\nTesting which sites allow automated scraping...")
    print("This will take about 1-2 minutes.\n")
    
    # Test sites 
    test_urls = [
        ("Naharnet", "https://www.naharnet.com/stories/en/317898-across-forgotten-walls-of-hong-kong-island-a-flock-of-bird-murals-rises"),
        ("MTV Lebanon", "https://www.mtv.com.lb/en/news/International/1628094/uk-court-jails-chinese-bitcoin-fraudster-for-over-11-years"),
        ("NNA", "https://www.nna-leb.gov.lb/en/news/151689/aub-attracts-top-medical-talent-from-harvard-medical-school-and-md-anderson-cancer-center-to-its-medical-center"),
        ("Beirut Today", "https://beirut-today.com/2025/08/06/climate-issues-are-no-longer-ignorable-in-crisis-ridden-lebanon/"),
    ]
    
    results = []
    for site_name, url in test_urls:
        if "PASTE" in url:
            print(f"\nSkipping {site_name} - No URL provided")
            continue
        result = test_site(site_name, url)
        results.append(result)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    working_sites = [r for r in results if r.get('success')]
    blocked_sites = [r for r in results if r.get('error') == '403 Forbidden']
    other_errors = [r for r in results if not r.get('success') and r.get('error') != '403 Forbidden']
    
    print(f"\nWorking sites ({len(working_sites)}):")
    for r in working_sites:
        print(f"   {r['site']}")
    
    if blocked_sites:
        print(f"\nBlocked sites ({len(blocked_sites)}):")
        for r in blocked_sites:
            print(f"   {r['site']} (403 Forbidden)")
    
    if other_errors:
        print(f"\nOther errors ({len(other_errors)}):")
        for r in other_errors:
            print(f"   {r['site']}: {r['error']}")
    
    print(f"\n{'='*60}")
    print(f"Recommendation: Use the {len(working_sites)} working sites for scraper")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()