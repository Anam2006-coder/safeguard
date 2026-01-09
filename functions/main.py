"""
Firebase Cloud Functions for SafeGuard API
"""
import os
import sys
import json
from flask import Flask, request, jsonify
from firebase_functions import https_fn, options

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ml.predict import ScamPredictor
    from google_ai.translate import detect_and_translate
    from utils.url_extractor import extract_urls
    from google_ai.safe_browsing import check_urls_safe_browsing
    from utils.risk_score import compute_risk_score_and_reasons
    from detection_modules.fake_news_detector import detect_fake_news
    from detection_modules.scam_detector import detect_scam
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports or error handling

# Initialize Flask app for Cloud Functions
app = Flask(__name__)

# Initialize predictor (will be loaded when first called)
predictor = None

def get_predictor():
    global predictor
    if predictor is None:
        try:
            predictor = ScamPredictor(
                model_path=os.path.join("..", "models", "scam_model.pkl"),
                vectorizer_path=os.path.join("..", "models", "vectorizer.pkl")
            )
        except Exception as e:
            print(f"Error loading predictor: {e}")
            return None
    return predictor

@https_fn.on_request(
    cors=options.CorsOptions(
        cors_origins=["*"],
        cors_methods=["GET", "POST", "OPTIONS"],
        cors_allow_headers=["Content-Type", "Authorization"]
    )
)
def api(req: https_fn.Request) -> https_fn.Response:
    """Main API endpoint for all SafeGuard functions"""
    
    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return https_fn.Response(
            status=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Max-Age': '3600'
            }
        )
    
    # Route requests based on path
    path = req.path.replace('/api/', '')
    
    if path == 'detect-scam' and req.method == 'POST':
        return detect_scam_api(req)
    elif path == 'analyze-news' and req.method == 'POST':
        return analyze_news_api(req)
    elif path == 'analyze-scam' and req.method == 'POST':
        return analyze_scam_api(req)
    elif path == 'health' and req.method == 'GET':
        return health_check(req)
    else:
        return https_fn.Response(
            json.dumps({"error": "Endpoint not found"}),
            status=404,
            headers={'Content-Type': 'application/json'}
        )

def detect_scam_api(req):
    """Scam detection API endpoint"""
    try:
        data = req.get_json()
        if not data or "message" not in data:
            return https_fn.Response(
                json.dumps({"error": "Missing 'message' in request body"}),
                status=400,
                headers={'Content-Type': 'application/json'}
            )

        message = data["message"].strip()
        if not message or len(message) < 5:
            return https_fn.Response(
                json.dumps({"error": "Message too short or empty"}),
                status=400,
                headers={'Content-Type': 'application/json'}
            )

        # Get predictor
        pred = get_predictor()
        if not pred:
            return https_fn.Response(
                json.dumps({"error": "ML model not available"}),
                status=500,
                headers={'Content-Type': 'application/json'}
            )

        # Extract URLs
        urls = extract_urls(message)

        # Detect language & translate
        detected_language, translated_text, translation_performed = detect_and_translate(message)

        # Predict
        prediction_result = pred.predict(translated_text)

        # Check URLs
        url_checks = check_urls_safe_browsing(urls)

        # Calculate risk score
        risk_score, reasons = compute_risk_score_and_reasons(
            prediction_result=prediction_result,
            urls_check=url_checks,
            original_text=message
        )

        # Map verdict
        label_map = {0: "Safe", 1: "Spam", 2: "Scam"}
        verdict = label_map.get(prediction_result["predicted_label"], "Unknown")

        result = {
            "verdict": verdict,
            "risk_score": int(risk_score),
            "confidence": round(float(prediction_result.get("confidence", 0)), 4),
            "reasons": reasons,
            "detected_language": detected_language,
            "message": message,
            "translated_text": translated_text if (translation_performed and translated_text != message) else None,
            "translation_available": translation_performed
        }

        return https_fn.Response(
            json.dumps(result),
            status=200,
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": "Internal server error", "detail": str(e)}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )

def analyze_news_api(req):
    """Fake news detection API endpoint"""
    try:
        data = req.get_json()
        if not data or "content" not in data:
            return https_fn.Response(
                json.dumps({"error": "Missing 'content' in request body"}),
                status=400,
                headers={'Content-Type': 'application/json'}
            )

        content = data["content"].strip()
        if not content:
            return https_fn.Response(
                json.dumps({"error": "Content cannot be empty"}),
                status=400,
                headers={'Content-Type': 'application/json'}
            )

        result = detect_fake_news(content)
        return https_fn.Response(
            json.dumps(result),
            status=200,
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": "Internal server error", "detail": str(e)}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )

def analyze_scam_api(req):
    """Scam analysis API endpoint"""
    try:
        data = req.get_json()
        if not data or "content" not in data:
            return https_fn.Response(
                json.dumps({"error": "Missing 'content' in request body"}),
                status=400,
                headers={'Content-Type': 'application/json'}
            )

        content = data["content"].strip()
        if not content:
            return https_fn.Response(
                json.dumps({"error": "Content cannot be empty"}),
                status=400,
                headers={'Content-Type': 'application/json'}
            )

        result = detect_scam(content)
        return https_fn.Response(
            json.dumps(result),
            status=200,
            headers={'Content-Type': 'application/json'}
        )

    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": "Internal server error", "detail": str(e)}),
            status=500,
            headers={'Content-Type': 'application/json'}
        )

def health_check(req):
    """Health check endpoint"""
    return https_fn.Response(
        json.dumps({"status": "ok", "service": "SafeGuard Firebase"}),
        status=200,
        headers={'Content-Type': 'application/json'}
    )