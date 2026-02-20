"""
Language support module for PhytoSense application.
Provides multi-language support for the application.
"""

import streamlit as st
import json
import os
import requests
 


# Available languages
AVAILABLE_LANGUAGES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "mr": "मराठी (Marathi)",
}

# Default translations path
TRANSLATIONS_PATH = "translations"

translation_cache = {}


def initialize_language():
    """
    Initialize language support
    """
    # Create translations directory if it doesn't exist
    if not os.path.exists(TRANSLATIONS_PATH):
        os.makedirs(TRANSLATIONS_PATH, exist_ok=True)
    
    # For each language, create an empty translation file if it doesn't exist
    for lang_code in AVAILABLE_LANGUAGES:
        lang_file = os.path.join(TRANSLATIONS_PATH, f"{lang_code}.json")
        if not os.path.exists(lang_file):
            with open(lang_file, 'w') as f:
                json.dump({}, f)

def load_translations(lang_code):
    """
    Load translations for a specific language
    
    Args:
        lang_code: Language code
        
    Returns:
        dict: Translations dictionary
    """
    # Default to English if language code is not valid
    if lang_code not in AVAILABLE_LANGUAGES:
        lang_code = "en"
    
    # Try to load translations from file
    translations_file = os.path.join(TRANSLATIONS_PATH, f"{lang_code}.json")
    
    try:
        if os.path.exists(translations_file):
            with open(translations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    
    # Return empty dictionary if translations couldn't be loaded
    return {}

def translate_api(text, target_lang):

    MAX_CHARS = 450   # safe below 500

    cache_key = text.strip()

    # 1️⃣ RAM cache
    if cache_key in translation_cache:
        return translation_cache[cache_key]

    # 2️⃣ Disk cache
    stored_translations = load_translations(target_lang)
    if cache_key in stored_translations:
        translation_cache[cache_key] = stored_translations[cache_key]
        return stored_translations[cache_key]

    # 3️⃣ Chunk if text too long
    try:
        if len(text) > MAX_CHARS:
            chunks = [text[i:i+MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]
            translated_chunks = [translate_api(chunk, target_lang) for chunk in chunks]
            final_translation = " ".join(translated_chunks)

            translation_cache[cache_key] = final_translation
            add_translation(cache_key, final_translation, target_lang)

            return final_translation

        # 4️⃣ Normal API call
        url = "https://api.mymemory.translated.net/get"

        params = {
            "q": text,
            "langpair": f"en|{target_lang}"
        }

        response = requests.get(url, params=params, timeout=5)

        if response.status_code == 200:
            translated = response.json()["responseData"]["translatedText"]

            translation_cache[cache_key] = translated
            add_translation(cache_key, translated, target_lang)

            return translated

        return text

    except Exception:
        return text


def t(text, lang_code=None):

    if text is None:
        return ""

    if lang_code is None:
        lang_code = st.session_state.get("language", "en")

    if lang_code == "en":
        return text

    if isinstance(text, (int, float)):
        return text

    return translate_api(str(text), lang_code)


def show_language_selector(sidebar=True, key="language_selector"):
    """
    Display language selector
    
    Args:
        sidebar: Whether to show in sidebar (default True)
        key: Unique key for the widget
    """
    # Get current language from session state
    current_lang = st.session_state.get("language", "en")
    
    # Determine container
    container = st.sidebar if sidebar else st
    
    if sidebar:
        container.markdown("### 🌐 Language / भाषा")
    
    # Display language selector
    # Use a customized label or no label for cleaner look in header
    label = "Select Language" if sidebar else "🌐 Language"
    
    selected_lang = container.selectbox(
        label,
        options=list(AVAILABLE_LANGUAGES.keys()),
        format_func=lambda x: AVAILABLE_LANGUAGES[x],
        index=list(AVAILABLE_LANGUAGES.keys()).index(current_lang),
        key=key
    )
    
    # Update session state if language changed
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    # Display language information only in sidebar
    if sidebar and selected_lang != "en":
        container.info(f"Some content may still appear in English if translations are not available.")

def get_available_languages():
    """
    Get list of available languages
    
    Returns:
        dict: Available languages dictionary
    """
    return AVAILABLE_LANGUAGES

def add_translation(text, translation, lang_code):
    """
    Add a translation to the language file
    
    Args:
        text: Original text
        translation: Translated text
        lang_code: Language code
        
    Returns:
        bool: Success status
    """
    # Ignore English (source language)
    if lang_code == "en":
        return True
    
    # Load existing translations
    translations = load_translations(lang_code)
    
    # Add new translation
    translations[text] = translation
    
    # Save translations
    translations_file = os.path.join(TRANSLATIONS_PATH, f"{lang_code}.json")
    
    try:
        with open(translations_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

# Populate translations for common UI elements
def populate_default_translations():
    """
    Populate default translations for common UI elements
    """
    # Hindi translations
    hindi_translations = {
        "Login to PhytoSense": "फाइटोसेंस में लॉगिन करें",
        "Username": "उपयोगकर्ता नाम",
        "Password": "पासवर्ड",
        "Login": "लॉगिन करें",
        "Create Account": "अकाउंट बनाएं",
        "Welcome to PhytoSense": "फाइटोसेंस में आपका स्वागत है",
        "Plant Health Analysis": "पौधे का स्वास्थ्य विश्लेषण",
        "Soil Analysis": "मिट्टी का विश्लेषण",
        "Weather Alerts": "मौसम चेतावनी",
        "Resources": "संसाधन",
        "History": "इतिहास",
        "Dashboard": "डैशबोर्ड",
        "Logout": "लॉगआउट करें"
    }
    
    # Marathi translations
    marathi_translations = {
        "Login to PhytoSense": "फायटोसेन्समध्ये लॉगिन करा",
        "Username": "वापरकर्ता नाव",
        "Password": "पासवर्ड",
        "Login": "लॉगिन करा",
        "Create Account": "खाते तयार करा",
        "Welcome to PhytoSense": "फायटोसेन्समध्ये आपले स्वागत आहे",
        "Plant Health Analysis": "वनस्पती आरोग्य विश्लेषण",
        "Soil Analysis": "माती विश्लेषण",
        "Weather Alerts": "हवामान सूचना",
        "Resources": "संसाधने",
        "History": "इतिहास",
        "Dashboard": "डॅशबोर्ड",
        "Logout": "लॉगआउट करा"
    }
    
    # Save translations
    for lang_code, translations in [("hi", hindi_translations), ("mr", marathi_translations)]:
        for text, translation in translations.items():
            add_translation(text, translation, lang_code)
