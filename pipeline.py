"""
AI Pipeline for multilingual news processing.

Features:
- Language detection (Arabic, English, French)
- Translation (Arabic/French → English)
- Text summarization (English → concise summary)

Tools & Models:
- langdetect library: Statistical language identification
- Helsinki-NLP/opus-mt-ar-en: Arabic → English translation
- Helsinki-NLP/opus-mt-fr-en: French → English translation
- facebook/bart-large-cnn: English text summarization
"""

import time
from langdetect import detect, DetectorFactory
from transformers import pipeline

# Set seed for consistent language detection results
DetectorFactory.seed = 0


# ============================================================================
# CONFIGURATION
# ============================================================================

# Supported languages
SUPPORTED_LANGUAGES = {
    'ar': 'Arabic',
    'en': 'English',
    'fr': 'French'
}

# Translation model names
TRANSLATION_MODELS = {
    'ar': 'Helsinki-NLP/opus-mt-ar-en',  # Arabic → English
    'fr': 'Helsinki-NLP/opus-mt-fr-en',  # French → English
}

# Summarization model
SUMMARIZATION_MODEL = 'facebook/bart-large-cnn'


# ====================================================================================
# MODEL CACHE (loaded on first use so we dont have to load every call and waste time)
# ====================================================================================

# Global variables to cache loaded models (avoid reloading)
_translator_ar = None
_translator_fr = None
_summarizer = None


def detect_language(text):
    """
    Detect the language of input text.
    
    Args:
        text (str): Text to analyze (at least 20 characters recommended)
        
    Returns:
        str: Language code ('ar', 'en', 'fr') or None if detection fails
    """
    if not text or len(text) < 10:
        print("Text too short for language detection!!")
        return None
    
    try:
        # Use first 500 chars for faster detection
        sample = text[:500]
        detected = detect(sample)
        
        # Only return if it's a supported language
        if detected in SUPPORTED_LANGUAGES:
            lang_name = SUPPORTED_LANGUAGES[detected]
            print(f"Detected language: {lang_name} ({detected})")
            return detected
        else:
            print(f"Detected unsupported language: {detected}")
            return None
            
    except Exception as e:
        print(f"Language detection error: {e}")
        return None


def translate_to_english(text, source_language):
    """
    Translate text from Arabic/French to English using HuggingFace models.
    
    Args:
        text (str): Text to translate
        source_language (str): Source language code ('ar', 'en', or 'fr')
        
    Returns:
        str: Translated English text, or original text if already English/error
    """
    global _translator_ar, _translator_fr
    
    # If already English, return as-is
    if source_language == 'en':
        print("Text already in English, no translation needed")
        return text
    
    # Validate supported languages
    if source_language not in ['ar', 'fr']:
        print(f"Unsupported source language: {source_language}")
        return text
    
    try:
        # Arabic -> English
        if source_language == 'ar':
            if _translator_ar is None:
                print(f"Loading Arabic_to_English model (first time only, ~5 min)...")
                print(f"   Model: {TRANSLATION_MODELS['ar']}")
                start_time = time.time()
                _translator_ar = pipeline("translation", model=TRANSLATION_MODELS['ar'])
                elapsed = time.time() - start_time
                print(f"Model loaded in {elapsed:.1f} seconds")
            
            print("Translating Arabic to English...")
            # Translate in chunks if text is long (model has max length)
            if len(text) > 500:
                # Split into chunks and translate
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                translated_chunks = []
                for chunk in chunks:
                    result = _translator_ar(chunk, max_length=512)
                    translated_chunks.append(result[0]['translation_text'])
                translated = ' '.join(translated_chunks)
            else:
                result = _translator_ar(text, max_length=512)
                translated = result[0]['translation_text']
            
            print(f"Translation complete ({len(translated)} chars)")
            return translated
        
        # French -> English
        elif source_language == 'fr':
            if _translator_fr is None:
                print(f"Loading French_to_English model (first time only, ~5 min)...")
                print(f"   Model: {TRANSLATION_MODELS['fr']}")
                start_time = time.time()
                _translator_fr = pipeline("translation", model=TRANSLATION_MODELS['fr'])
                elapsed = time.time() - start_time
                print(f"Model loaded in {elapsed:.1f} seconds")
            
            print("Translating French to English...")
            # Translate in chunks if text is long
            if len(text) > 500:
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                translated_chunks = []
                for chunk in chunks:
                    result = _translator_fr(chunk, max_length=512)
                    translated_chunks.append(result[0]['translation_text'])
                translated = ' '.join(translated_chunks)
            else:
                result = _translator_fr(text, max_length=512)
                translated = result[0]['translation_text']
            
            print(f"Translation complete ({len(translated)} chars)")
            return translated
            
    except Exception as e:
        print(f"Translation error: {e}")
        print(f"   Returning original text")
        return text


def summarize_text(text, max_length=150, min_length=50):
    """
    Generate a concise summary of English text using BART model.
    
    Args:
        text (str): English text to summarize (should be at least 200 chars)
        max_length (int): Maximum summary length in tokens (~words)
        min_length (int): Minimum summary length in tokens
        
    Returns:
        str: Generated summary, or original text if too short/error
    """
    global _summarizer
    
    # Don't summarize very short text
    if len(text) < 200:
        print("Text too short for summarization (< 200 chars)")
        return text
    
    try:
        # Load model on first use (cached after that)
        if _summarizer is None:
            print(f"Loading summarization model (first time only, ~10 min)...")
            print(f"   Model: {SUMMARIZATION_MODEL}")
            start_time = time.time()
            _summarizer = pipeline("summarization", model=SUMMARIZATION_MODEL)
            elapsed = time.time() - start_time
            print(f"Model loaded in {elapsed:.1f} seconds")
        
        print(f"Generating summary...")
        print(f"   Input length: {len(text)} characters")
        
        # Bart has a max input length of ~1024 tokens (~4000 chars)
        # If text is longer, truncate it
        if len(text) > 4000:
            print(f"   Text is long, using first 4000 characters")
            text = text[:4000]
        
        # Generate summary
        result = _summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        summary = result[0]['summary_text']
        
        print(f"Summary generated ({len(summary)} characters)")
        return summary
        
    except Exception as e:
        print(f"Summarization error: {e}")
        print(f"   Returning original text")
        return text


def process_article(article_data, output_language='en', summary_max_length=150):
    """
    Complete AI pipeline: detect language -> translate -> summarize.
    
    This is the master function that processes a scraped article through
    the complete AI workflow.
    
    Args:
        article_data (dict): Article from scraper with 'title', 'text', 'url' keys
        output_language (str): Desired output language ('en', 'ar', 'fr')
                               Currently only 'en' supported
        summary_max_length (int): Maximum summary length in tokens
        
    Returns:
        dict: Processed article with original data + AI enhancements:
              {
                  'url': original URL,
                  'source': news source,
                  'title': original title,
                  'original_language': detected language,
                  'original_text': original article text,
                  'english_text': translated text (if not English),
                  'summary': AI-generated summary,
                  'processing_time': time taken to process
              }
              Returns None if processing fails
    """
    print("\n" + "="*70)
    print("PROCESSING ARTICLE THROUGH AI PIPELINE")
    print("="*70)
    
    start_time = time.time()
    
    # Validate input
    if not article_data or 'text' not in article_data:
        print("Invalid article data")
        return None
    
    # Initialize result
    result = {
        'url': article_data.get('url', 'N/A'),
        'source': article_data.get('source', 'Unknown'),
        'title': article_data.get('title', 'Untitled'),
        'date': article_data.get('date', 'N/A'),
        'original_language': None,
        'original_text': article_data['text'],
        'english_text': None,
        'summary': None,
        'processing_time': None
    }
    
    print(f"\nArticle: {result['title'][:60]}...")
    print(f"   Source: {result['source']}")
    print(f"   URL: {result['url'][:50]}...")
    
    # Step 1: Detect language
    print(f"\n{'─'*70}")
    print("STEP 1: Language Detection")
    print('─'*70)
    language = detect_language(article_data['text'])
    
    if not language:
        print("Language detection failed")
        return None
    
    result['original_language'] = language
    
    # Step 2: Translate to English (if needed)
    print(f"\n{'─'*70}")
    print("STEP 2: Translation")
    print('─'*70)
    
    if language == 'en':
        english_text = article_data['text']
        result['english_text'] = english_text
    else:
        english_text = translate_to_english(article_data['text'], language)
        result['english_text'] = english_text
    
    # Step 3: Summarize
    print(f"\n{'─'*70}")
    print("STEP 3: Summarization")
    print('─'*70)
    summary = summarize_text(english_text, max_length=summary_max_length)
    result['summary'] = summary
    
    # Calculate processing time
    elapsed = time.time() - start_time
    result['processing_time'] = f"{elapsed:.1f}s"
    
    # Final output
    print(f"\n{'='*70}")
    print("PROCESSING COMPLETE")
    print('='*70)
    print(f"Original language: {SUPPORTED_LANGUAGES[language]}")
    print(f"Summary generated: {len(summary)} characters")
    print(f"Total processing time: {result['processing_time']}")
    print('='*70)
    
    return result


# ============================================================================
# TESTING
# ============================================================================

def test_pipeline():
    """
    Test complete pipeline with multiple real articles from different sources.
    """
    print("="*70)
    print("STEP 10: MULTI-SOURCE PIPELINE TEST")
    print("="*70)
    
    # Import scraper
    from scraper import get_article
    
    # Test articles from different sources
    # Replace with your actual article URLs
    test_articles = [
        {
            'name': 'Naharnet (English)',
            'url': 'https://www.naharnet.com/stories/en/317898-across-forgotten-walls-of-hong-kong-island-a-flock-of-bird-murals-rises'
        },
        {
            'name': 'MTV Lebanon (English)',
            'url': 'https://www.mtv.com.lb/en/news/International/1628094/uk-court-jails-chinese-bitcoin-fraudster-for-over-11-years'
        },
        {
            'name': 'Beirut Today (Arabic)',
            'url': 'https://beirut-today.com/ar/2023/06/02/ar-corruption-health-sector-coronavirus-lebanon/'
        },
    ]
    
    print(f"\nTesting pipeline with {len(test_articles)} articles from different sources...")
    print(f"This will take ~40-120 seconds (models already cached)\n")
    
    results = []
    
    for i, test_article in enumerate(test_articles, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(test_articles)}: {test_article['name']}")
        print('='*70)
        
        # Scrape article
        article = get_article(test_article['url'])
        
        if not article:
            print(f"Scraping failed for {test_article['name']}")
            results.append({
                'name': test_article['name'],
                'success': False
            })
            continue
        
        # Process through pipeline
        result = process_article(article, summary_max_length=100)
        
        if result:
            results.append({
                'name': test_article['name'],
                'success': True,
                'language': SUPPORTED_LANGUAGES[result['original_language']],
                'summary_length': len(result['summary']),
                'processing_time': result['processing_time']
            })
            
            # Show brief result
            print(f"\nSUCCESS")
            print(f"   Language: {SUPPORTED_LANGUAGES[result['original_language']]}")
            print(f"   Summary: {result['summary'][:100]}...")
        else:
            results.append({
                'name': test_article['name'],
                'success': False
            })
            print(f"Processing failed")
    
    # Summary report
    print(f"\n{'='*70}")
    print("FINAL SUMMARY REPORT")
    print('='*70)
    
    successful = [r for r in results if r.get('success')]
    failed = [r for r in results if not r.get('success')]
    
    print(f"\nSuccessful: {len(successful)}/{len(results)}")
    for r in successful:
        print(f"   {r['name']}")
        print(f"     Language: {r['language']}, Time: {r['processing_time']}")
    
    if failed:
        print(f"\nFailed: {len(failed)}/{len(results)}")
        for r in failed:
            print(f"   {r['name']}")
    
    print(f"\n{'='*70}")
    print("Multi-source pipeline test complete!")
    print('='*70)

if __name__ == "__main__":
    test_pipeline()