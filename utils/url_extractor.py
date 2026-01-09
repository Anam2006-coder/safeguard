"""
URL extractor using regex. Extracts http(s) and www. links.
"""
import re

URL_REGEX = re.compile(
    r"(https?://[^\s]+|www\.[^\s]+)",
    re.IGNORECASE
)

def extract_urls(text: str):
    if not text:
        return []
    urls = URL_REGEX.findall(text)
    # Normalize results
    urls = [u.strip(".,;:()[]<>\"'") for u in urls]
    return list(dict.fromkeys(urls))  # de-duplicate preserving order