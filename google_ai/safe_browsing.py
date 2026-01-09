"""
Google Safe Browsing v4 API checker.

- Reads SAFE_BROWSING_API_KEY from env
- If missing, returns a safe-skipped structure
- If present, sends URLs to Safe Browsing API and returns matches info

Response format:
{
  "checked": True/False,
  "api_key_present": True/False,
  "matches": {
     "<url>": {"unsafe": True/False, "threat_types": [...]} ...
  },
  "error": "..." optional
}
"""
import os
import requests
import json

SAFE_BROWSING_URL = "https://safebrowsing.googleapis.com/v4/threatMatches:find"

def check_urls_safe_browsing(urls):
    if not urls:
        return {"checked": True, "api_key_present": False, "matches": {}}
    api_key = os.environ.get("SAFE_BROWSING_API_KEY")
    if not api_key:
        # Gracefully skip URL checking
        return {"checked": False, "api_key_present": False, "matches": {}}

    body = {
        "client": {
            "clientId": "scam_detection_system",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": u} for u in urls]
        }
    }
    params = {"key": api_key}
    try:
        resp = requests.post(SAFE_BROWSING_URL, params=params, json=body, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        matches_raw = data.get("matches", [])
        matches = {u: {"unsafe": False, "threat_types": []} for u in urls}
        # matches_raw contains entries with 'threat' field having 'url' and 'threatType'
        for m in matches_raw:
            threat = m.get("threat", {})
            url = threat.get("url")
            ttype = m.get("threatType") or m.get("threatTypes") or []
            # mark as unsafe
            if url in matches:
                matches[url]["unsafe"] = True
                # threatType may be a single string
                if isinstance(ttype, str):
                    matches[url]["threat_types"].append(ttype)
                elif isinstance(ttype, list):
                    matches[url]["threat_types"].extend(ttype)
                else:
                    # fallback
                    matches[url]["threat_types"].append(str(m.get("threatType", "")))
        return {"checked": True, "api_key_present": True, "matches": matches}
    except Exception as e:
        return {"checked": False, "api_key_present": True, "matches": {}, "error": str(e)}