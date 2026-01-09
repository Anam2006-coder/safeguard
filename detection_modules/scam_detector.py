"""
Advanced Scam Detection Module
Replace this with your sophisticated scam detection algorithm
"""

import re
import string
from collections import Counter

def detect_scam(content):
    """
    Advanced scam detection function
    
    Args:
        content (str): Text content to analyze
        
    Returns:
        dict: Detection results with score, keywords, and recommendations
    """
    
    # Initialize analysis
    scam_score = 0
    detected_keywords = []
    risk_factors = []
    
    # Advanced scam indicators
    high_risk_keywords = [
        'urgent', 'winner', 'lottery', 'prize', 'congratulations',
        'inheritance', 'prince', 'bank transfer', 'wire transfer',
        'western union', 'moneygram', 'bitcoin', 'cryptocurrency',
        'tax refund', 'irs', 'government', 'legal action',
        'suspended account', 'verify account', 'click here',
        'limited time', 'act now', 'expires today'
    ]
    
    medium_risk_keywords = [
        'free money', 'easy money', 'work from home', 'make money fast',
        'no experience required', 'guaranteed', 'risk free',
        'investment opportunity', 'double your money'
    ]
    
    # URL and link patterns (suspicious)
    suspicious_patterns = [
        r'bit\.ly',
        r'tinyurl',
        r'[a-z0-9]{10,}\.com',  # Random domain names
        r'click.*here',
        r'verify.*account',
        r'\$\d+',  # Money amounts
        r'\d{4}-\d{4}-\d{4}-\d{4}',  # Credit card patterns
    ]
    
    # Convert to lowercase for analysis
    content_lower = content.lower()
    
    # 1. Keyword Analysis
    for keyword in high_risk_keywords:
        if keyword in content_lower:
            scam_score += 15
            detected_keywords.append(keyword)
            risk_factors.append(f"High-risk keyword: '{keyword}'")
    
    for keyword in medium_risk_keywords:
        if keyword in content_lower:
            scam_score += 8
            detected_keywords.append(keyword)
            risk_factors.append(f"Medium-risk keyword: '{keyword}'")
    
    # 2. Pattern Analysis
    for pattern in suspicious_patterns:
        matches = re.findall(pattern, content_lower)
        if matches:
            scam_score += 12
            risk_factors.append(f"Suspicious pattern detected: {pattern}")
    
    # 3. Urgency Analysis
    urgency_words = ['urgent', 'immediately', 'asap', 'expires', 'limited time', 'act now']
    urgency_count = sum(1 for word in urgency_words if word in content_lower)
    if urgency_count >= 2:
        scam_score += 20
        risk_factors.append("Multiple urgency indicators")
    
    # 4. Grammar and Spelling Analysis
    spelling_errors = analyze_spelling_quality(content)
    if spelling_errors > 3:
        scam_score += 10
        risk_factors.append(f"Poor spelling/grammar ({spelling_errors} errors)")
    
    # 5. Excessive Capitalization
    caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
    if caps_ratio > 0.3:
        scam_score += 15
        risk_factors.append("Excessive capitalization")
    
    # 6. Personal Information Requests
    personal_info_patterns = [
        r'social security', r'ssn', r'credit card', r'bank account',
        r'routing number', r'password', r'pin number'
    ]
    
    for pattern in personal_info_patterns:
        if re.search(pattern, content_lower):
            scam_score += 25
            risk_factors.append("Requests personal/financial information")
            break
    
    # Determine risk level
    is_scam = scam_score > 30
    
    # Risk level classification
    if scam_score >= 70:
        risk_level = "CRITICAL"
        message = "CRITICAL: High probability scam detected!"
    elif scam_score >= 40:
        risk_level = "HIGH"
        message = "HIGH RISK: Likely scam detected!"
    elif scam_score >= 20:
        risk_level = "MEDIUM"
        message = "MEDIUM RISK: Suspicious content detected"
    else:
        risk_level = "LOW"
        message = "LOW RISK: Content appears safe"
    
    # Generate recommendations
    recommendations = generate_scam_recommendations(scam_score, risk_factors)
    
    return {
        'is_scam': is_scam,
        'scam_score': min(scam_score, 100),
        'risk_level': risk_level,
        'detected_keywords': detected_keywords[:10],  # Limit to top 10
        'risk_factors': risk_factors,
        'recommendations': recommendations,
        'message': message
    }


def analyze_spelling_quality(text):
    """Basic spelling/grammar quality analysis"""
    # Simple heuristics for poor quality text
    errors = 0
    
    # Check for repeated characters (like "hellooo")
    if re.search(r'(.)\1{2,}', text):
        errors += 1
    
    # Check for missing spaces after punctuation
    if re.search(r'[.!?][a-zA-Z]', text):
        errors += 1
    
    # Check for excessive punctuation
    if re.search(r'[!?]{2,}', text):
        errors += 1
    
    # Check for common misspellings
    common_errors = ['recieve', 'seperate', 'occured', 'definately', 'goverment']
    for error in common_errors:
        if error in text.lower():
            errors += 1
    
    return errors


def generate_scam_recommendations(score, risk_factors):
    """Generate specific recommendations based on detected risks"""
    recommendations = []
    
    if score >= 50:
        recommendations.extend([
            "🚨 DO NOT respond to this message",
            "🚨 DO NOT click any links",
            "🚨 DO NOT provide personal information",
            "🚨 Report as spam/scam immediately"
        ])
    elif score >= 30:
        recommendations.extend([
            "⚠️ Verify sender through official channels",
            "⚠️ Do not click links or download attachments",
            "⚠️ Be cautious of any requests for information"
        ])
    else:
        recommendations.extend([
            "✅ Content appears safe",
            "✅ Still verify sender if unknown",
            "✅ Use caution with any financial requests"
        ])
    
    # Add specific recommendations based on risk factors
    if any("personal" in factor.lower() for factor in risk_factors):
        recommendations.append("🔒 Never share personal/financial info via email")
    
    if any("urgency" in factor.lower() for factor in risk_factors):
        recommendations.append("⏰ Legitimate organizations don't create false urgency")
    
    return recommendations


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_scam = """
    URGENT! Congratulations! You have won $1,000,000 in the international lottery!
    To claim your prize, please send your bank account details and social security number.
    This offer expires in 24 hours! Act now!
    """
    
    test_safe = """
    Hi John, hope you're doing well. Just wanted to follow up on our meeting
    scheduled for next week. Please let me know if you need to reschedule.
    Best regards, Sarah
    """
    
    print("=== SCAM TEST ===")
    result1 = detect_scam(test_scam)
    print(f"Score: {result1['scam_score']}")
    print(f"Risk Level: {result1['risk_level']}")
    print(f"Message: {result1['message']}")
    
    print("\n=== SAFE TEST ===")
    result2 = detect_scam(test_safe)
    print(f"Score: {result2['scam_score']}")
    print(f"Risk Level: {result2['risk_level']}")
    print(f"Message: {result2['message']}")