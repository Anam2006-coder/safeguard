"""
Calculate risk score and reasons for classification
"""

def compute_risk_score_and_reasons(prediction_result, urls_check, original_text):
    """
    Compute overall risk score (0-100) and reasons based on verdict
    
    FIXED LOGIC:
    - Safe verdict → Low risk (0-30%) - Higher confidence = LOWER risk
    - Spam verdict → Moderate risk (40-70%)
    - Scam verdict → High risk (70-100%) - Higher confidence = HIGHER risk
    """
    
    # Get model prediction
    predicted_label = prediction_result.get("predicted_label", 0)
    confidence = prediction_result.get("confidence", 0.5)
    
    label_names = {0: "Safe", 1: "Spam", 2: "Scam"}
    label_name = label_names.get(predicted_label, "Unknown")
    
    reasons = []
    
    # ====== CORRECTED BASE RISK SCORE CALCULATION ======
    if predicted_label == 0:  # SAFE
        # For Safe messages: Higher confidence = LOWER risk
        # Formula: (1 - confidence) * 30 gives us 0-30% risk range
        base_risk = (1.0 - confidence) * 30
        reasons.append(f"Message classified as Safe with {confidence:.2f} confidence")
    elif predicted_label == 1:  # SPAM
        # For Spam messages: Moderate risk 40-70%
        base_risk = 40 + (confidence * 30)
        reasons.append(f"Message classified as Spam with {confidence:.2f} confidence")
    else:  # SCAM (2)
        # For Scam messages: Higher confidence = HIGHER risk (70-100%)
        base_risk = 70 + (confidence * 30)
        reasons.append(f"Message classified as Scam with {confidence:.2f} confidence")
    
    risk_score = base_risk
    
    # ====== URL SAFETY CHECK ======
    unsafe_flagged = False
    if urls_check and urls_check.get("checked") and urls_check.get("api_key_present"):
        matches = urls_check.get("matches", {})
        for url, info in matches.items():
            if info.get("unsafe"):
                unsafe_flagged = True
                risk_score += 25  # Add risk for unsafe URLs
                reasons.append(f"Malicious URL detected: {url}")
        if not unsafe_flagged and matches:
            reasons.append("All URLs checked and found safe")
    elif not urls_check.get("api_key_present", True):
        reasons.append("URL safety check skipped (API key not configured)")
    elif not urls_check.get("checked", True):
        if urls_check.get("error"):
            reasons.append(f"URL safety check failed: {urls_check.get('error')}")
        else:
            reasons.append("No URLs found to check")

    # ====== FRAUD KEYWORDS CHECK ======
    fraud_keywords = [
        "urgent", "verify", "blocked", "pay", "click", "limited", "otp", "account", 
        "immediately", "bank", "password", "wire", "transfer", "verify now", 
        "update your", "suspended", "claim", "congratulations", "winner"
    ]
    
    text_lower = original_text.lower()
    found_keywords = [kw for kw in fraud_keywords if kw in text_lower]
    
    if found_keywords:
        risk_score += 20  # Add risk for fraud keywords
        keywords_str = ", ".join(found_keywords[:5])
        reasons.append(f"Suspicious keywords detected: {keywords_str}")
    else:
        # Only add this reason for Safe messages to explain low risk
        if predicted_label == 0:
            reasons.append("No suspicious keywords or urgency indicators found")

    # ====== ADDITIONAL CONTEXT REASONS ======
    if predicted_label == 0 and confidence >= 0.7:
        reasons.append("Message contains legitimate communication patterns")
    elif predicted_label == 1 and confidence >= 0.7:
        reasons.append("Message shows typical spam/marketing characteristics")
    elif predicted_label == 2 and confidence >= 0.7:
        reasons.append("Message exhibits strong fraud indicators")
    
    # ====== FINAL CAPS ======
    risk_score = max(0, min(100, risk_score))  # Ensure 0-100
    
    return int(round(risk_score)), reasons