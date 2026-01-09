"""
Advanced Fake News Detection Module
Replace this with your sophisticated fake news detection algorithm
"""

import re
import string
from datetime import datetime
from collections import Counter

def detect_fake_news(content):
    """
    Advanced fake news detection function
    
    Args:
        content (str): News content to analyze
        
    Returns:
        dict: Detection results with credibility score and analysis
    """
    
    # Initialize analysis
    fake_score = 0
    detected_indicators = []
    credibility_factors = []
    
    # Sensational language indicators
    sensational_words = [
        'shocking', 'unbelievable', 'incredible', 'amazing', 'stunning',
        'mind-blowing', 'explosive', 'bombshell', 'devastating', 'outrageous',
        'miracle', 'breakthrough', 'revolutionary', 'insane', 'crazy',
        'unreal', 'jaw-dropping', 'epic', 'massive', 'huge revelation',
        'exclusive', 'leaked', 'exposed', 'secret', 'hidden truth',
        'conspiracy', 'cover-up', 'they don\'t want you to know',
        'mainstream media won\'t tell you', 'wake up', 'sheeple'
    ]
    
    # Clickbait patterns
    clickbait_patterns = [
        r"you won't believe",
        r"doctors hate",
        r"this will shock you",
        r"what happened next",
        r"the truth about",
        r"they don't want you to know",
        r"secret that",
        r"exposed",
        r"leaked",
        r"everything you know is wrong",
        r"this changes everything",
        r"nobody is talking about",
        r"mainstream media won't tell you",
        r"wake up",
        r"must see",
        r"gone viral",
        r"breaking:",
        r"urgent:",
        r"alert:",
        r"warning:"
    ]
    
    # Bias indicators
    bias_words = [
        'always', 'never', 'all', 'none', 'every', 'completely',
        'totally', 'absolutely', 'definitely', 'certainly', 'obviously',
        'clearly', 'undeniably', 'without a doubt', 'everyone knows'
    ]
    
    # Emotional manipulation words
    emotional_words = [
        'outraged', 'furious', 'disgusted', 'terrified', 'panicked',
        'devastated', 'heartbroken', 'enraged', 'horrified', 'scared',
        'angry', 'betrayed', 'shocked', 'appalled', 'stunned'
    ]
    
    # Scam-related keywords that should raise flags
    scam_keywords = [
        'money from bill gates', 'free iphone', 'free money', 'get rich quick',
        'make money fast', 'work from home', 'easy money', 'guaranteed income',
        'click here to win', 'you have won', 'congratulations winner',
        'limited time offer', 'act now', 'urgent response required'
    ]
    
    # Convert to lowercase for analysis
    content_lower = content.lower()
    
    # Check for scam keywords
    scam_count = sum(1 for keyword in scam_keywords if keyword in content_lower)
    if scam_count >= 2:
        fake_score += 40
        credibility_factors.append(f"Multiple scam-related keywords detected ({scam_count} instances)")
        detected_indicators.extend([kw for kw in scam_keywords if kw in content_lower])
    elif scam_count >= 1:
        fake_score += 20
        credibility_factors.append("Contains scam-related keywords")
        detected_indicators.extend([kw for kw in scam_keywords if kw in content_lower])
    
    # 1. Sensational Language Analysis
    sensational_count = 0
    for word in sensational_words:
        if word in content_lower:
            sensational_count += 1
            detected_indicators.append(word)
    
    if sensational_count >= 3:
        fake_score += 35
        credibility_factors.append(f"Excessive sensational language ({sensational_count} instances)")
    elif sensational_count >= 2:
        fake_score += 25
        credibility_factors.append(f"Multiple sensational words ({sensational_count} instances)")
    elif sensational_count >= 1:
        fake_score += 15
        credibility_factors.append("Contains sensational language")
    
    # 2. Clickbait Pattern Analysis
    clickbait_matches = 0
    for pattern in clickbait_patterns:
        if re.search(pattern, content_lower):
            clickbait_matches += 1
            detected_indicators.append(pattern.replace(r'\b', '').replace(r'.*', ''))
    
    if clickbait_matches >= 2:
        fake_score += 40
        credibility_factors.append("Multiple clickbait patterns detected")
    elif clickbait_matches >= 1:
        fake_score += 25
        credibility_factors.append("Clickbait pattern detected")
    
    # 3. Source and Attribution Analysis
    source_indicators = analyze_source_quality(content)
    fake_score += source_indicators['score']
    credibility_factors.extend(source_indicators['factors'])
    
    # 4. Bias Language Analysis
    bias_count = sum(1 for word in bias_words if word in content_lower)
    if bias_count >= 5:
        fake_score += 25
        credibility_factors.append(f"Excessive absolute language ({bias_count} instances)")
    elif bias_count >= 3:
        fake_score += 15
        credibility_factors.append("Contains biased language")
    elif bias_count >= 1:
        fake_score += 8
        credibility_factors.append("Some absolute language detected")
    
    # 5. Emotional Manipulation Analysis
    emotional_count = sum(1 for word in emotional_words if word in content_lower)
    if emotional_count >= 3:
        fake_score += 30
        credibility_factors.append("High emotional manipulation")
    elif emotional_count >= 1:
        fake_score += 15
        credibility_factors.append("Contains emotional manipulation")
    
    # 6. Factual Claims Analysis
    fact_analysis = analyze_factual_claims(content)
    fake_score += fact_analysis['score']
    credibility_factors.extend(fact_analysis['factors'])
    
    # 7. Writing Quality Analysis
    quality_analysis = analyze_writing_quality(content)
    fake_score += quality_analysis['score']
    credibility_factors.extend(quality_analysis['factors'])
    
    # 8. Urgency and Time Pressure
    urgency_analysis = analyze_urgency(content)
    fake_score += urgency_analysis['score']
    credibility_factors.extend(urgency_analysis['factors'])
    
    # Determine credibility - more aggressive scoring
    is_fake = fake_score >= 20  # Even lower threshold for fake detection
    
    # Credibility classification
    if fake_score >= 50:
        credibility_level = "HIGHLY UNRELIABLE"
        message = "This content shows STRONG indicators of fake news or misinformation"
    elif fake_score >= 35:
        credibility_level = "UNRELIABLE"
        message = "This content has MULTIPLE red flags suggesting fake news"
    elif fake_score >= 20:
        credibility_level = "QUESTIONABLE"
        message = "This content has QUESTIONABLE credibility - verify before trusting"
    elif fake_score >= 10:
        credibility_level = "MOSTLY RELIABLE"
        message = "This content appears mostly reliable with minor concerns"
    else:
        credibility_level = "RELIABLE"
        message = "This content appears credible with good journalistic standards"
    
    # Generate recommendations
    recommendations = generate_news_recommendations(fake_score, credibility_factors)
    
    return {
        'is_fake': is_fake,
        'fake_score': min(fake_score, 100),
        'credibility_level': credibility_level,
        'detected_indicators': detected_indicators[:10],  # Limit to top 10
        'credibility_factors': credibility_factors,
        'recommendations': recommendations,
        'message': message
    }


def analyze_source_quality(content):
    """Analyze source attribution and quality indicators"""
    score = 0
    factors = []
    
    # Check for source attribution
    source_patterns = [
        r'according to',
        r'sources say',
        r'reported by',
        r'study shows',
        r'research indicates'
    ]
    
    has_sources = any(re.search(pattern, content.lower()) for pattern in source_patterns)
    
    if not has_sources and len(content) > 200:
        score += 15
        factors.append("Lacks proper source attribution")
    
    # Check for vague sources
    vague_sources = [
        'anonymous sources', 'sources close to', 'insiders say',
        'experts believe', 'many people say'
    ]
    
    vague_count = sum(1 for source in vague_sources if source in content.lower())
    if vague_count >= 2:
        score += 20
        factors.append("Multiple vague source references")
    elif vague_count >= 1:
        score += 10
        factors.append("Contains vague source references")
    
    return {'score': score, 'factors': factors}


def analyze_factual_claims(content):
    """Analyze the nature of factual claims made"""
    score = 0
    factors = []
    
    # Look for extraordinary claims
    extraordinary_patterns = [
        r'\d+% of (people|doctors|experts)',
        r'scientists discovered',
        r'breakthrough study',
        r'miracle cure',
        r'secret government'
    ]
    
    extraordinary_count = sum(1 for pattern in extraordinary_patterns 
                            if re.search(pattern, content.lower()))
    
    if extraordinary_count >= 2:
        score += 25
        factors.append("Multiple extraordinary claims")
    elif extraordinary_count >= 1:
        score += 12
        factors.append("Contains extraordinary claims")
    
    # Check for specific numbers without context
    number_pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b'
    numbers = re.findall(number_pattern, content)
    
    if len(numbers) >= 5:
        score += 15
        factors.append("Heavy use of statistics without context")
    
    return {'score': score, 'factors': factors}


def analyze_writing_quality(content):
    """Analyze writing quality indicators"""
    score = 0
    factors = []
    
    # Check for excessive punctuation
    if re.search(r'[!?]{2,}', content):
        score += 10
        factors.append("Excessive punctuation usage")
    
    # Check for all caps sections
    caps_sections = re.findall(r'\b[A-Z]{4,}\b', content)
    if len(caps_sections) >= 3:
        score += 15
        factors.append("Excessive capitalization")
    
    # Check sentence length variation (poor quality often has very short or very long sentences)
    sentences = re.split(r'[.!?]+', content)
    if sentences:
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        if avg_length < 5 or avg_length > 40:
            score += 10
            factors.append("Poor sentence structure")
    
    return {'score': score, 'factors': factors}


def analyze_urgency(content):
    """Analyze urgency and time pressure indicators"""
    score = 0
    factors = []
    
    urgency_words = [
        'breaking', 'urgent', 'immediate', 'emergency', 'crisis',
        'must read', 'act now', 'before it\'s too late'
    ]
    
    urgency_count = sum(1 for word in urgency_words if word in content.lower())
    
    if urgency_count >= 3:
        score += 20
        factors.append("Excessive urgency language")
    elif urgency_count >= 1:
        score += 8
        factors.append("Contains urgency indicators")
    
    return {'score': score, 'factors': factors}


def generate_news_recommendations(score, factors):
    """Generate specific recommendations based on credibility analysis"""
    recommendations = []
    
    if score >= 50:
        recommendations.extend([
            "🚨 CRITICAL: Do NOT share this content",
            "🚨 HIGH RISK: Verify with multiple reliable sources immediately",
            "🚨 Check fact-checking websites (Snopes, FactCheck.org, PolitiFact)",
            "🚨 Look for original source documentation and citations",
            "🚨 This appears to be misinformation or propaganda"
        ])
    elif score >= 35:
        recommendations.extend([
            "⚠️ WARNING: High probability of fake news",
            "⚠️ Do not trust without verification",
            "⚠️ Cross-reference with reputable news sources",
            "⚠️ Check the publication's credibility and bias",
            "⚠️ Verify all claims independently"
        ])
    elif score >= 20:
        recommendations.extend([
            "⚠️ QUESTIONABLE: Cross-reference with other sources",
            "⚠️ Check the publication's reputation and track record",
            "⚠️ Look for author credentials and expertise",
            "⚠️ Verify any statistics or claims made",
            "⚠️ Be cautious about sharing without verification"
        ])
    elif score >= 10:
        recommendations.extend([
            "✅ Appears mostly credible but verify important details",
            "✅ Check publication date for relevance",
            "✅ Look for supporting evidence from other sources",
            "✅ Minor concerns detected - use critical thinking"
        ])
    else:
        recommendations.extend([
            "✅ Content appears credible with good standards",
            "✅ Shows proper journalistic practices",
            "✅ Still verify critical claims independently",
            "✅ Check publication date for current relevance"
        ])
    
    # Add specific recommendations based on detected factors
    if any("source" in factor.lower() for factor in factors):
        recommendations.append("🔍 Research and verify the original sources cited")
    
    if any("emotional" in factor.lower() for factor in factors):
        recommendations.append("🧠 Be aware of emotional manipulation tactics being used")
    
    if any("clickbait" in factor.lower() for factor in factors):
        recommendations.append("📰 Look beyond sensational headlines to actual content")
        
    if any("bias" in factor.lower() for factor in factors):
        recommendations.append("⚖️ Check for balanced reporting from multiple perspectives")
    
    return recommendations


# Example usage and testing
if __name__ == "__main__":
    # Test cases
    test_fake = """
    SHOCKING! Doctors HATE this one simple trick that COMPLETELY eliminates cancer!
    You won't believe what this anonymous insider revealed about the secret government
    cover-up! This breakthrough study shows 99% of people don't know this amazing fact!
    BREAKING: Must read before it's too late!
    """
    
    test_real = """
    According to a study published in the Journal of Medical Research, researchers
    at Stanford University have identified a potential new treatment approach for
    certain types of cancer. The peer-reviewed study, conducted over 3 years with
    500 participants, showed promising preliminary results that warrant further investigation.
    """
    
    print("=== FAKE NEWS TEST ===")
    result1 = detect_fake_news(test_fake)
    print(f"Score: {result1['fake_score']}")
    print(f"Credibility: {result1['credibility_level']}")
    print(f"Message: {result1['message']}")
    
    print("\n=== REAL NEWS TEST ===")
    result2 = detect_fake_news(test_real)
    print(f"Score: {result2['fake_score']}")
    print(f"Credibility: {result2['credibility_level']}")
    print(f"Message: {result2['message']}")