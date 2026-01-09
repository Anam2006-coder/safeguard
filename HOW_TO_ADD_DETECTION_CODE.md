# 🔧 How to Add Your Advanced Detection Algorithms

This guide explains how to integrate your sophisticated scam detection and fake news detection code into the SafeGuard application.

## 📁 File Structure

```
safeguard_app/
├── app.py                          # Main Flask application
├── detection_modules/              # Your detection algorithms go here
│   ├── __init__.py                # Package initializer
│   ├── scam_detector.py           # Replace with your scam detection code
│   └── fake_news_detector.py      # Replace with your fake news detection code
├── templates/                      # HTML templates (already configured)
└── requirements.txt               # Add your dependencies here
```

## 🎯 Step 1: Replace Detection Modules

### For Scam Detection:

**Replace the content of `detection_modules/scam_detector.py`** with your code, but ensure your main function follows this signature:

```python
def detect_scam(content):
    """
    Your advanced scam detection function
    
    Args:
        content (str): Text content to analyze
        
    Returns:
        dict: Must return a dictionary with these keys:
        {
            'is_scam': bool,              # True if scam detected
            'scam_score': int,            # Risk score 0-100
            'detected_keywords': list,    # List of detected keywords
            'message': str,               # User-friendly message
            
            # Optional advanced fields:
            'risk_level': str,            # "LOW", "MEDIUM", "HIGH", "CRITICAL"
            'risk_factors': list,         # List of specific risk factors found
            'recommendations': list       # List of specific recommendations
        }
    """
    # Your advanced algorithm here
    pass
```

### For Fake News Detection:

**Replace the content of `detection_modules/fake_news_detector.py`** with your code:

```python
def detect_fake_news(content):
    """
    Your advanced fake news detection function
    
    Args:
        content (str): News content to analyze
        
    Returns:
        dict: Must return a dictionary with these keys:
        {
            'is_fake': bool,              # True if fake news detected
            'fake_score': int,            # Risk score 0-100
            'detected_indicators': list,  # List of detected indicators
            'message': str,               # User-friendly message
            
            # Optional advanced fields:
            'credibility_level': str,     # "RELIABLE", "QUESTIONABLE", "UNRELIABLE"
            'credibility_factors': list,  # List of credibility factors
            'recommendations': list       # List of specific recommendations
        }
    """
    # Your advanced algorithm here
    pass
```

## 🔧 Step 2: Add Dependencies

If your detection code requires additional libraries, add them to `requirements.txt`:

```txt
Flask==2.3.3
Werkzeug==2.3.7
# Add your dependencies below:
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
tensorflow==2.13.0
transformers==4.30.0
torch==2.0.1
nltk==3.8.1
spacy==3.6.0
```

## 🧠 Step 3: Integration Examples

### Example 1: Using Machine Learning Models

```python
# In scam_detector.py
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load your pre-trained model
model = joblib.load('path/to/your/scam_model.pkl')
vectorizer = joblib.load('path/to/your/vectorizer.pkl')

def detect_scam(content):
    # Vectorize the content
    features = vectorizer.transform([content])
    
    # Get prediction and probability
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    scam_score = int(probability[1] * 100)  # Probability of being scam
    
    return {
        'is_scam': prediction == 1,
        'scam_score': scam_score,
        'detected_keywords': extract_keywords(content),
        'message': f'ML Model confidence: {scam_score}%'
    }
```

### Example 2: Using Deep Learning (BERT/Transformers)

```python
# In fake_news_detector.py
from transformers import pipeline

# Load pre-trained model
classifier = pipeline("text-classification", 
                     model="your-model/fake-news-detector")

def detect_fake_news(content):
    # Get prediction from transformer model
    result = classifier(content)
    
    # Extract confidence score
    fake_confidence = result[0]['score'] if result[0]['label'] == 'FAKE' else 1 - result[0]['score']
    fake_score = int(fake_confidence * 100)
    
    return {
        'is_fake': fake_confidence > 0.5,
        'fake_score': fake_score,
        'detected_indicators': [],
        'message': f'AI Model confidence: {fake_score}%',
        'credibility_level': get_credibility_level(fake_score)
    }

def get_credibility_level(score):
    if score >= 80: return "HIGHLY UNRELIABLE"
    elif score >= 60: return "UNRELIABLE"
    elif score >= 40: return "QUESTIONABLE"
    else: return "RELIABLE"
```

### Example 3: Combining Multiple Approaches

```python
def detect_scam(content):
    # Combine rule-based + ML + deep learning
    
    # 1. Rule-based analysis
    rule_score = rule_based_analysis(content)
    
    # 2. ML model prediction
    ml_score = ml_model_prediction(content)
    
    # 3. Deep learning analysis
    dl_score = deep_learning_analysis(content)
    
    # Weighted combination
    final_score = int(0.3 * rule_score + 0.4 * ml_score + 0.3 * dl_score)
    
    return {
        'is_scam': final_score > 50,
        'scam_score': final_score,
        'detected_keywords': get_all_keywords(content),
        'risk_factors': get_risk_factors(content),
        'recommendations': get_recommendations(final_score),
        'message': f'Combined analysis score: {final_score}%'
    }
```

## 📊 Step 4: Adding Model Files

If you have pre-trained models, create a `models/` directory:

```
safeguard_app/
├── models/
│   ├── scam_model.pkl
│   ├── fake_news_model.pkl
│   ├── vectorizer.pkl
│   └── bert_model/
└── detection_modules/
    ├── scam_detector.py
    └── fake_news_detector.py
```

Load models in your detection functions:

```python
import os
import joblib

# Get the path to models directory
models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
model_path = os.path.join(models_dir, 'scam_model.pkl')

# Load model
model = joblib.load(model_path)
```

## 🧪 Step 5: Testing Your Integration

1. **Test individual modules:**
```bash
cd safeguard_app/detection_modules
python scam_detector.py
python fake_news_detector.py
```

2. **Test full application:**
```bash
cd safeguard_app
python app.py
```

3. **Test with sample data:**
   - Navigate to `http://localhost:5000`
   - Login with any credentials
   - Test both detection modules with sample content

## 🔍 Step 6: Advanced Features

### Adding Configuration

Create `config.py` for model settings:

```python
# config.py
class Config:
    SCAM_MODEL_PATH = 'models/scam_model.pkl'
    FAKE_NEWS_MODEL_PATH = 'models/fake_news_model.pkl'
    CONFIDENCE_THRESHOLD = 0.7
    MAX_TEXT_LENGTH = 10000
```

### Adding Logging

```python
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_scam(content):
    logger.info(f"Analyzing content of length: {len(content)}")
    # Your detection code
    logger.info(f"Detection complete. Score: {score}")
```

### Adding Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def detect_scam_cached(content_hash):
    # Your detection logic here
    pass

def detect_scam(content):
    # Create hash of content for caching
    content_hash = hashlib.md5(content.encode()).hexdigest()
    return detect_scam_cached(content_hash)
```

## 🚀 Step 7: Deployment Ready

Once your algorithms are integrated:

1. **Update requirements.txt** with all dependencies
2. **Test thoroughly** with various inputs
3. **Optimize performance** for real-time analysis
4. **Add error handling** for edge cases
5. **Document your algorithms** in the code

## 💡 Tips for Success

1. **Keep the function signatures** - The web app expects specific return formats
2. **Handle errors gracefully** - Add try-catch blocks around your ML code
3. **Optimize for speed** - Users expect quick results
4. **Test edge cases** - Empty content, very long content, special characters
5. **Add progress indicators** - For long-running analyses

## 🔧 Troubleshooting

**If your modules don't load:**
- Check the import statements in `app.py`
- Ensure all dependencies are installed
- Check file paths and permissions

**If detection fails:**
- The app will fall back to basic detection
- Check the console for error messages
- Test your functions independently first

Your advanced detection algorithms are now ready to be integrated into the SafeGuard application! 🛡️