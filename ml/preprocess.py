"""
Text preprocessing utilities.

Requirements:
- Lowercase
- Remove URLs
- Remove punctuation & special characters
- Normalize whitespace
"""
import re

URL_REGEX = re.compile(
    r"(https?://\S+|www\.\S+)", re.IGNORECASE
)

def remove_urls(text: str) -> str:
    return URL_REGEX.sub(" ", text)

def remove_special_characters(text: str) -> str:
    # Keep letters, numbers and whitespace
    return re.sub(r"[^A-Za-z0-9\s]", " ", text)

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def preprocess_text(text: str) -> str:
    if not isinstance(text, str):
        text = str(text or "")
    text = text.lower()
    text = remove_urls(text)
    text = remove_special_characters(text)
    text = normalize_whitespace(text)
    return text