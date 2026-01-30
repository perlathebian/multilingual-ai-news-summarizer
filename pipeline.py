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
        # Arabic → English
        if source_language == 'ar':
            if _translator_ar is None:
                print(f"Loading Arabic_to_English model (first time only, ~5 min)...")
                print(f"   Model: {TRANSLATION_MODELS['ar']}")
                start_time = time.time()
                _translator_ar = pipeline("translation", model=TRANSLATION_MODELS['ar'])
                elapsed = time.time() - start_time
                print(f"Model loaded in {elapsed:.1f} seconds")
            
            print("Translating Arabic → English...")
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
        
        # French → English
        elif source_language == 'fr':
            if _translator_fr is None:
                print(f"Loading French→English model (first time only, ~5 min)...")
                print(f"   Model: {TRANSLATION_MODELS['fr']}")
                start_time = time.time()
                _translator_fr = pipeline("translation", model=TRANSLATION_MODELS['fr'])
                elapsed = time.time() - start_time
                print(f"Model loaded in {elapsed:.1f} seconds")
            
            print("Translating French → English...")
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
    Generate a concise summary of English text.
    
    Args:
        text (str): English text to summarize
        max_length (int): Maximum summary length in words
        min_length (int): Minimum summary length in words
        
    Returns:
        str: Generated summary
    """
    # TODO: will implement in step 7
    pass


def process_article(article_data):
    """
    Complete AI pipeline: detect language → translate → summarize.
    
    Args:
        article_data (dict): Article with 'title' and 'text' keys
        
    Returns:
        dict: Processed article with summary and metadata
    """
    # TODO: will implement in step 9
    pass


# ============================================================================
# TESTING
# ============================================================================

def test_pipeline():
    """
    Test language detection and translation.
    """
    print("="*70)
    print("STEP 4: TRANSLATION PIPELINE TEST")
    print("="*70)
    
    # Test samples with translations
    test_samples = [
        {
            'language': 'English',
            'code': 'en',
            'text': 'This is a test article about news in Lebanon. The economy is recovering from the crisis.'
        },
        {
            'language': 'Arabic',
            'code': 'ar',
            'text': 'هذا مقال تجريبي عن الأخبار في لبنان. الاقتصاد يتعافى من الأزمة المالية.'
        },
        {
            'language': 'French',
            'code': 'fr',
            'text': 'Ceci est un article de test sur les nouvelles au Liban. L\'économie se rétablit de la crise.'
        }
    ]
    
    print("\nTesting language detection + translation:\n")
    
    for sample in test_samples:
        print(f"{'─'*70}")
        print(f"Testing: {sample['language']}")
        print(f"Original text: {sample['text'][:60]}...")
        print()
        
        # Detect language
        detected = detect_language(sample['text'])
        
        if detected:
            # Translate to English
            translated = translate_to_english(sample['text'], detected)
            print(f"\nTranslated text: {translated[:100]}...")
            print(f"   Length: {len(translated)} characters")
        else:
            print("Detection failed, skipping translation")
        
        print()
    
    print("="*70)
    print("Translation pipeline test complete!")
    print("="*70)

if __name__ == "__main__":
    test_pipeline()