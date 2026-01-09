"""
Language detection and translation helper.

- Detect language using langdetect
- If detected language != 'en', attempt translation using free services
- Fallback gracefully if translation fails

Returns:
(detected_language, text_to_use, translation_performed_bool)
"""
from langdetect import detect, DetectorFactory, LangDetectException
DetectorFactory.seed = 0

import os
import requests
import json

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "unknown"
    except Exception:
        return "unknown"

def translate_text_google(text: str, target_language: str = "en"):
    # Try to import google translate client
    try:
        from google.cloud import translate_v2 as translate
    except Exception:
        # google package not available
        raise RuntimeError("google-cloud-translate not available")

    # Instantiate client - it will use GOOGLE_APPLICATION_CREDENTIALS env var if set
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result.get("translatedText", text)

def translate_text_free(text: str, source_lang: str, target_lang: str = "en"):
    """
    Use a free translation service (MyMemory API)
    """
    try:
        # MyMemory API - free translation service
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f"{source_lang}|{target_lang}"
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200:
                translated = data.get('responseData', {}).get('translatedText', '')
                if translated and translated.lower() != text.lower():
                    return translated
        
        # If MyMemory fails, try basic dictionary translations for common phrases
        return translate_basic_phrases(text, source_lang)
        
    except Exception as e:
        print(f"Translation error: {e}")
        return translate_basic_phrases(text, source_lang)

def translate_basic_phrases(text: str, source_lang: str):
    """
    Basic translation for common phrases and scam-related terms
    """
    text_lower = text.lower()
    
    # Common scam/spam phrases translations
    translations = {
        'fr': {
            'bonjour': 'hello',
            'salut': 'hi',
            'comment allez-vous': 'how are you',
            'rappel final': 'final reminder',
            'péage impayé': 'unpaid toll',
            'paiement': 'payment',
            'cliquez ici': 'click here',
            'urgent': 'urgent',
            'félicitations': 'congratulations',
            'vous avez gagné': 'you have won',
            'compte bloqué': 'account blocked',
            'vérifiez': 'verify',
            'le défaut de paiement': 'payment default',
            'entraînera des pénalités': 'will result in penalties',
            'supplémentaires': 'additional'
        },
        'es': {
            'hola': 'hello',
            'como estas': 'how are you',
            'recordatorio final': 'final reminder',
            'pago pendiente': 'pending payment',
            'haga clic aquí': 'click here',
            'urgente': 'urgent',
            'felicidades': 'congratulations',
            'has ganado': 'you have won',
            'cuenta bloqueada': 'account blocked',
            'verificar': 'verify'
        },
        'de': {
            'hallo': 'hello',
            'wie geht es dir': 'how are you',
            'letzte erinnerung': 'final reminder',
            'unbezahlte rechnung': 'unpaid bill',
            'klicken sie hier': 'click here',
            'dringend': 'urgent',
            'glückwunsch': 'congratulations',
            'sie haben gewonnen': 'you have won',
            'konto gesperrt': 'account blocked',
            'überprüfen': 'verify'
        },
        'it': {
            'ciao': 'hello',
            'come stai': 'how are you',
            'promemoria finale': 'final reminder',
            'pagamento in sospeso': 'pending payment',
            'clicca qui': 'click here',
            'urgente': 'urgent',
            'congratulazioni': 'congratulations',
            'hai vinto': 'you have won',
            'account bloccato': 'account blocked',
            'verificare': 'verify'
        }
    }
    
    if source_lang in translations:
        lang_dict = translations[source_lang]
        
        # Try to find and translate key phrases
        translated_text = text
        for phrase, translation in lang_dict.items():
            if phrase in text_lower:
                # Replace the phrase with translation, preserving case
                translated_text = translated_text.replace(phrase, translation)
                translated_text = translated_text.replace(phrase.title(), translation.title())
                translated_text = translated_text.replace(phrase.upper(), translation.upper())
        
        # If we made any translations, return the result
        if translated_text.lower() != text.lower():
            return f"[Partial Translation] {translated_text}"
    
    # Fallback: return with language indicator
    return f"[{source_lang.upper()} Text - Translation not available] {text}"

def detect_and_translate(text: str):
    detected = detect_language(text)
    if detected == "en":
        return detected, text, False
    
    # Attempt Google translation first
    try:
        translated = translate_text_google(text, target_language="en")
        if translated != text:
            return detected, translated, True
    except Exception:
        pass
    
    # Try free translation service
    try:
        translated = translate_text_free(text, detected, "en")
        if translated and translated != text:
            return detected, translated, True
    except Exception:
        pass
    
    # Final fallback
    return detected, f"[{detected.upper()} Text - No translation available] {text}", True