#!/usr/bin/env python3
"""
Flask Web Application + API for Scam Detection
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import os
import traceback

from ml.predict import ScamPredictor
from google_ai.translate import detect_and_translate
from utils.url_extractor import extract_urls
from google_ai.safe_browsing import check_urls_safe_browsing
from utils.risk_score import compute_risk_score_and_reasons
from detection_modules.fake_news_detector import detect_fake_news
from detection_modules.scam_detector import detect_scam

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'safeguard-secret-key-2024'

# Initialize predictor
try:
    predictor = ScamPredictor(
        model_path=os.path.join("models", "scam_model.pkl"),
        vectorizer_path=os.path.join("models", "vectorizer.pkl")
    )
except FileNotFoundError as e:
    print(f"ERROR: {str(e)}")
    print("Please run: python -m ml.train_model")
    exit(1)


# ============ WEB UI ROUTES ============

@app.route('/')
def index():
    """Redirect to login page"""
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (in production, use proper authentication)
        if username and password:
            session['user'] = username
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    """Home page with analyzer"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    # Check if user is logged in
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/fake_news_detection')
def fake_news_detection():
    """Fake news detection page"""
    return render_template('fake_news_detection.html')


@app.route('/scam_detection')
def scam_detection():
    """Scam detection page"""
    return render_template('scam_detection.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze message - Web form"""
    try:
        message = request.form.get('message', '').strip()

        if not message:
            return redirect(url_for('home'))

        if len(message) < 5:
            return redirect(url_for('home'))

        # Extract URLs
        urls = extract_urls(message)

        # Detect language & translate
        detected_language, translated_text, translation_performed = detect_and_translate(message)

        # Predict
        prediction_result = predictor.predict(translated_text)

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

        # Get confidence
        confidence = prediction_result.get("confidence", 0)

        result = {
            "verdict": verdict,
            "risk_score": int(risk_score),
            "confidence": round(float(confidence), 4),
            "reasons": reasons,
            "detected_language": detected_language,
            "message": message,
            "translated_text": translated_text if (translation_performed and translated_text != message) else None,
            "translation_available": translation_performed
        }

        return render_template('analyze.html', result=result)

    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return redirect(url_for('home'))


# ============ API ROUTES ============

@app.route('/api/detect-scam', methods=['POST'])
def api_detect_scam():
    """API endpoint - returns JSON for programmatic access"""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400

        message = data["message"].strip()

        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400

        if len(message) < 5:
            return jsonify({"error": "Message too short"}), 400

        # Extract URLs
        urls = extract_urls(message)

        # Detect language & translate
        detected_language, translated_text, translation_performed = detect_and_translate(message)

        # Predict
        prediction_result = predictor.predict(translated_text)

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

        # Get confidence
        confidence = prediction_result.get("confidence", 0)

        result = {
            "verdict": verdict,
            "risk_score": int(risk_score),
            "confidence": round(float(confidence), 4),
            "reasons": reasons,
            "detected_language": detected_language,
            "message": message,
            "translated_text": translated_text if (translation_performed and translated_text != message) else None,
            "translation_available": translation_performed
        }
        
        print(f"DEBUG API: translation_performed={translation_performed}, translated_text={translated_text}")
        print(f"DEBUG API: Final result keys: {list(result.keys())}")

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500


@app.route('/analyze-scam', methods=['POST'])
def analyze_scam():
    """Web endpoint for scam detection"""
    try:
        data = request.get_json()
        if not data or "content" not in data:
            return jsonify({"error": "Missing 'content' in request body"}), 400

        content = data["content"].strip()
        if not content:
            return jsonify({"error": "Content cannot be empty"}), 400

        result = detect_scam(content)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500


@app.route('/analyze-news', methods=['POST'])
def analyze_news():
    """Web endpoint for fake news detection"""
    try:
        data = request.get_json()
        if not data or "content" not in data:
            return jsonify({"error": "Missing 'content' in request body"}), 400

        content = data["content"].strip()
        if not content:
            return jsonify({"error": "Content cannot be empty"}), 400

        result = detect_fake_news(content)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500


@app.route('/api/fake-news', methods=['POST'])
def api_fake_news():
    """API endpoint for fake news detection"""
    try:
        data = request.get_json()
        if not data or "content" not in data:
            return jsonify({"error": "Missing 'content' in request body"}), 400

        content = data["content"].strip()
        if not content:
            return jsonify({"error": "Content cannot be empty"}), 400

        result = detect_fake_news(content)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "detail": str(e)}), 500


@app.route('/api/docs')
def api_docs():
    """API Documentation page"""
    return render_template('api_docs.html')


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "SafeGuard"}), 200


if __name__ == '__main__': 
    print("\n" + "="*60)
    print("Shield SafeGuard - Scam Detection System")
    print("="*60)
    
    # Get port from environment variable (for Render) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    print(f"\nWeb UI:    http://0.0.0.0:{port}")
    print(f"API:     http://0.0.0.0:{port}/api/detect-scam (POST)")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)