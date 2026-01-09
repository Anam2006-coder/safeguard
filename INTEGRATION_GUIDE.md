# 📁 How to Add Your Two Detection Folders

This guide explains how to integrate your existing scam detection and fake news detection folders into the SafeGuard application.

## 🎯 Current Structure

```
safeguard_app/
├── app.py                          # Main Flask app (already configured)
├── detection_modules/              # Integration layer
│   ├── __init__.py
│   ├── scam_detector.py           # Wrapper for your scam folder
│   └── fake_news_detector.py      # Wrapper for your fake news folder
├── templates/                      # Web interface (ready)
└── requirements.txt               # Add your dependencies here
```

## 📂 Step 1: Add Your Folders

Copy your two detection folders into the SafeGuard directory:

```
safeguard_app/
├── app.py
├── detection_modules/
├── your_scam_detection_folder/     # ← Copy your scam detection folder here
│   ├── main.py                     # Your main scam detection file
│   ├── model.pkl                   # Your trained models
│   ├── utils.py                    # Your utility functions
│   └── ... (all your files)
├── your_fake_news_folder/          # ← Copy your fake news folder here
│   ├── main.py                     # Your main fake news file
│   ├── model.pkl                   # Your trained models
│   ├── preprocessing.py            # Your preprocessing code
│   └── ... (all your files)
└── templates/
```

## 🔧 Step 2: Create Wrapper Functions

Now I'll show you how to modify the wrapper files to call your existing code.

### For Scam Detection

Edit `detection_modules/scam_detector.py` to import and use your existing code:

```python
"""
Scam Detection Wrapper
This file imports and uses your existing scam detection folder
"""

import sys
import os

# Add your scam detection folder to Python path
scam_folder_path = os.path.join(os.path.dirname(__file__), '..', 'your_scam_detection_folder')
sys.path.append(scam_folder_path)

try:
    # Import your existing scam detection functions
    # Replace these imports with your actual file and function names
    from main import detect_scam_content  # Replace with your function name
    from utils import preprocess_text     # Replace with your utility functions
    # Add more imports as needed
    
    SCAM_MODULE_LOADED = True
except ImportError as e:
    print(f"Warning: Could not import scam detection module: {e}")
    SCAM_MODULE_LOADED = False

def detect_scam(content):
    """
    Wrapper function that calls your existing scam detection code
    
    Args:
        content (str): Text content to analyze
        
    Returns:
        dict: Standardized results for the web app
    """
    
    if not SCAM_MODULE_LOADED:
        return fallback_scam_detection(content)
    
    try:
        # Call your existing scam detection function
        # Replace this with your actual function call
        your_result = detect_scam_content(content)  # Replace with your function
        
        # Convert your result format to SafeGuard format
        # Modify this based on what your function returns
        
        if isinstance(your_result, dict):
            # If your function returns a dictionary
            scam_score = your_result.get('score', 0) * 100  # Convert to 0-100 scale
            is_scam = your_result.get('is_scam', False)
            keywords = your_result.get('keywords', [])
            
        elif isinstance(your_result, (int, float)):
            # If your function returns just a score
            scam_score = int(your_result * 100)  # Convert to 0-100 scale
            is_scam = scam_score > 50
            keywords = []
            
        elif isinstance(your_result, bool):
            # If your function returns just True/False
            is_scam = your_result
            scam_score = 80 if is_scam else 20
            keywords = []
            
        else:
            # Handle other return types
            is_scam = bool(your_result)
            scam_score = 80 if is_scam else 20
            keywords = []
        
        # Return standardized format for SafeGuard
        return {
            'is_scam': is_scam,
            'scam_score': min(max(scam_score, 0), 100),  # Ensure 0-100 range
            'detected_keywords': keywords[:10],  # Limit to 10 keywords
            'message': f'Scam probability: {scam_score}%',
            'risk_level': get_risk_level(scam_score),
            'recommendations': get_scam_recommendations(is_scam, scam_score)
        }
        
    except Exception as e:
        print(f"Error in scam detection: {e}")
        return fallback_scam_detection(content)

def get_risk_level(score):
    """Convert score to risk level"""
    if score >= 80: return "CRITICAL"
    elif score >= 60: return "HIGH"
    elif score >= 40: return "MEDIUM"
    else: return "LOW"

def get_scam_recommendations(is_scam, score):
    """Generate recommendations based on results"""
    if is_scam:
        return [
            "🚨 HIGH RISK: Do not respond to this message",
            "🚨 Do not click any links or download attachments",
            "🚨 Report as spam/scam immediately",
            "🚨 Do not provide any personal information"
        ]
    else:
        return [
            "✅ Content appears safe",
            "✅ Still verify sender if unknown",
            "✅ Be cautious with any requests for information"
        ]

def fallback_scam_detection(content):
    """Fallback detection if your module fails to load"""
    # Simple keyword-based detection as backup
    scam_keywords = ['urgent', 'winner', 'lottery', 'prize', 'click here']
    score = sum(10 for keyword in scam_keywords if keyword.lower() in content.lower())
    
    return {
        'is_scam': score > 20,
        'scam_score': min(score, 100),
        'detected_keywords': [kw for kw in scam_keywords if kw.lower() in content.lower()],
        'message': 'Using fallback detection',
        'risk_level': 'MEDIUM' if score > 20 else 'LOW',
        'recommendations': get_scam_recommendations(score > 20, score)
    }
```

### For Fake News Detection

Edit `detection_modules/fake_news_detector.py`:

```python
"""
Fake News Detection Wrapper
This file imports and uses your existing fake news detection folder
"""

import sys
import os

# Add your fake news folder to Python path
news_folder_path = os.path.join(os.path.dirname(__file__), '..', 'your_fake_news_folder')
sys.path.append(news_folder_path)

try:
    # Import your existing fake news detection functions
    # Replace these imports with your actual file and function names
    from main import classify_news        # Replace with your function name
    from preprocessing import clean_text  # Replace with your preprocessing
    # Add more imports as needed
    
    NEWS_MODULE_LOADED = True
except ImportError as e:
    print(f"Warning: Could not import fake news module: {e}")
    NEWS_MODULE_LOADED = False

def detect_fake_news(content):
    """
    Wrapper function that calls your existing fake news detection code
    
    Args:
        content (str): News content to analyze
        
    Returns:
        dict: Standardized results for the web app
    """
    
    if not NEWS_MODULE_LOADED:
        return fallback_news_detection(content)
    
    try:
        # Preprocess content if needed (use your preprocessing)
        # processed_content = clean_text(content)  # Replace with your function
        
        # Call your existing fake news detection function
        # Replace this with your actual function call
        your_result = classify_news(content)  # Replace with your function
        
        # Convert your result format to SafeGuard format
        # Modify this based on what your function returns
        
        if isinstance(your_result, dict):
            # If your function returns a dictionary
            fake_score = your_result.get('fake_probability', 0) * 100
            is_fake = your_result.get('is_fake', False)
            confidence = your_result.get('confidence', 0.5)
            
        elif isinstance(your_result, (int, float)):
            # If your function returns just a score (0-1 or 0-100)
            if your_result <= 1.0:
                fake_score = int(your_result * 100)  # Convert 0-1 to 0-100
            else:
                fake_score = int(your_result)  # Already 0-100
            is_fake = fake_score > 50
            
        elif isinstance(your_result, bool):
            # If your function returns just True/False
            is_fake = your_result
            fake_score = 80 if is_fake else 20
            
        else:
            # Handle other return types
            is_fake = bool(your_result)
            fake_score = 80 if is_fake else 20
        
        # Return standardized format for SafeGuard
        return {
            'is_fake': is_fake,
            'fake_score': min(max(fake_score, 0), 100),  # Ensure 0-100 range
            'detected_indicators': extract_indicators(content),
            'message': f'Fake news probability: {fake_score}%',
            'credibility_level': get_credibility_level(fake_score),
            'recommendations': get_news_recommendations(is_fake, fake_score)
        }
        
    except Exception as e:
        print(f"Error in fake news detection: {e}")
        return fallback_news_detection(content)

def extract_indicators(content):
    """Extract indicators from content (customize based on your analysis)"""
    indicators = []
    sensational_words = ['shocking', 'unbelievable', 'breaking', 'exposed']
    
    for word in sensational_words:
        if word.lower() in content.lower():
            indicators.append(word)
    
    return indicators[:10]  # Limit to 10

def get_credibility_level(score):
    """Convert score to credibility level"""
    if score >= 80: return "HIGHLY UNRELIABLE"
    elif score >= 60: return "UNRELIABLE"
    elif score >= 40: return "QUESTIONABLE"
    elif score >= 20: return "MOSTLY RELIABLE"
    else: return "RELIABLE"

def get_news_recommendations(is_fake, score):
    """Generate recommendations based on results"""
    if is_fake:
        return [
            "🚨 HIGH RISK: Verify with multiple reliable sources",
            "🚨 Check fact-checking websites",
            "🚨 Look for original source documentation",
            "🚨 Be cautious about sharing this content"
        ]
    else:
        return [
            "✅ Content appears credible",
            "✅ Still cross-reference with other sources",
            "✅ Check publication date and author credentials"
        ]

def fallback_news_detection(content):
    """Fallback detection if your module fails to load"""
    # Simple indicator-based detection as backup
    fake_indicators = ['breaking', 'shocking', 'unbelievable', 'secret']
    score = sum(15 for indicator in fake_indicators if indicator.lower() in content.lower())
    
    return {
        'is_fake': score > 30,
        'fake_score': min(score, 100),
        'detected_indicators': [ind for ind in fake_indicators if ind.lower() in content.lower()],
        'message': 'Using fallback detection',
        'credibility_level': get_credibility_level(score),
        'recommendations': get_news_recommendations(score > 30, score)
    }
```

## 📋 Step 3: Update Requirements

Add your dependencies to `requirements.txt`:

```txt
Flask==2.3.3
Werkzeug==2.3.7

# Add your specific dependencies here:
# numpy==1.24.3
# pandas==2.0.3
# scikit-learn==1.3.0
# tensorflow==2.13.0
# torch==2.0.1
# transformers==4.30.0
# nltk==3.8.1
# spacy==3.6.0
# joblib==1.3.0
# pickle5==0.0.12
```

## 🧪 Step 4: Test Integration

1. **Copy your folders** into the safeguard_app directory
2. **Update the wrapper files** with your actual function names
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Test the integration**: `python test_detection.py`
5. **Run the app**: `python app.py`

## 📝 Step 5: Customization Examples

### If your scam detection function looks like this:
```python
# In your_scam_detection_folder/main.py
def analyze_scam(text):
    # Your code here
    return {'probability': 0.85, 'is_scam': True, 'features': [...]}
```

### Update the wrapper like this:
```python
# In detection_modules/scam_detector.py
from main import analyze_scam  # Import your function

def detect_scam(content):
    result = analyze_scam(content)  # Call your function
    
    return {
        'is_scam': result['is_scam'],
        'scam_score': int(result['probability'] * 100),
        'detected_keywords': result.get('features', []),
        'message': f"Scam probability: {result['probability']:.2%}"
    }
```

## 🔧 Common Integration Patterns

### Pattern 1: Your function returns a probability (0-1)
```python
your_result = your_function(content)  # Returns 0.75
scam_score = int(your_result * 100)   # Convert to 75
is_scam = your_result > 0.5           # True if > 50%
```

### Pattern 2: Your function returns a class label
```python
your_result = your_function(content)  # Returns "SCAM" or "SAFE"
is_scam = your_result == "SCAM"
scam_score = 80 if is_scam else 20
```

### Pattern 3: Your function returns multiple values
```python
prediction, confidence, features = your_function(content)
is_scam = prediction == 1
scam_score = int(confidence * 100)
detected_keywords = features
```

## 🚀 Ready to Integrate!

1. Copy your two folders into `safeguard_app/`
2. Update the wrapper files with your actual function names
3. Add your dependencies to requirements.txt
4. Test and run!

Your advanced detection algorithms will now power the SafeGuard web application! 🛡️