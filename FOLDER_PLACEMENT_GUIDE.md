# 📁 Exact Folder Placement Guide

## 🎯 Where to Put Your Two Folders

Copy your existing detection folders directly into the `safeguard_app` directory:

```
safeguard_app/                          # Main application folder
├── app.py                              # Flask app (already exists)
├── detection_modules/                  # Wrapper layer (already exists)
│   ├── scam_detector.py               # Will call your scam folder
│   └── fake_news_detector.py          # Will call your fake news folder
├── templates/                          # Web interface (already exists)
├── requirements.txt                    # Add your dependencies here
│
├── [YOUR_SCAM_FOLDER_NAME]/           # ← COPY YOUR SCAM FOLDER HERE
│   ├── main.py                        # Your scam detection files
│   ├── model.pkl                      # Your trained models
│   ├── utils.py                       # Your utility functions
│   ├── data/                          # Your data files
│   └── ... (all your scam files)
│
└── [YOUR_FAKE_NEWS_FOLDER_NAME]/      # ← COPY YOUR FAKE NEWS FOLDER HERE
    ├── main.py                        # Your fake news files
    ├── model.pkl                      # Your trained models
    ├── preprocessing.py               # Your preprocessing code
    ├── data/                          # Your data files
    └── ... (all your fake news files)
```

## 📋 Step-by-Step Instructions

### Step 1: Copy Your Folders
1. Navigate to your `safeguard_app` folder
2. Copy your scam detection folder into `safeguard_app/`
3. Copy your fake news detection folder into `safeguard_app/`

### Step 2: Note Your Folder Names
Write down the exact names of your folders:
- Scam detection folder name: `_________________`
- Fake news detection folder name: `_________________`

### Step 3: Find Your Main Functions
Look inside your folders and note:
- **Scam detection**: Which file has the main detection function? `_________________`
- **Scam detection**: What is the function name? `_________________`
- **Fake news detection**: Which file has the main detection function? `_________________`
- **Fake news detection**: What is the function name? `_________________`

## 🔧 Quick Integration Template

Once you know your folder and function names, update the wrapper files:

### Update `detection_modules/scam_detector.py`:

```python
import sys
import os

# Replace 'YOUR_SCAM_FOLDER_NAME' with your actual folder name
scam_folder_path = os.path.join(os.path.dirname(__file__), '..', 'YOUR_SCAM_FOLDER_NAME')
sys.path.append(scam_folder_path)

try:
    # Replace 'main_file' and 'your_function_name' with your actual names
    from main_file import your_function_name
    SCAM_MODULE_LOADED = True
except ImportError as e:
    print(f"Could not import scam module: {e}")
    SCAM_MODULE_LOADED = False

def detect_scam(content):
    if not SCAM_MODULE_LOADED:
        return {'is_scam': False, 'scam_score': 0, 'message': 'Module not loaded'}
    
    try:
        # Replace 'your_function_name' with your actual function
        result = your_function_name(content)
        
        # Convert your result to SafeGuard format
        # Modify this based on what your function returns
        return {
            'is_scam': bool(result),  # Adjust based on your return type
            'scam_score': 50,         # Adjust based on your return type
            'detected_keywords': [],
            'message': 'Scam analysis complete'
        }
    except Exception as e:
        return {'is_scam': False, 'scam_score': 0, 'message': f'Error: {e}'}
```

### Update `detection_modules/fake_news_detector.py`:

```python
import sys
import os

# Replace 'YOUR_FAKE_NEWS_FOLDER_NAME' with your actual folder name
news_folder_path = os.path.join(os.path.dirname(__file__), '..', 'YOUR_FAKE_NEWS_FOLDER_NAME')
sys.path.append(news_folder_path)

try:
    # Replace 'main_file' and 'your_function_name' with your actual names
    from main_file import your_function_name
    NEWS_MODULE_LOADED = True
except ImportError as e:
    print(f"Could not import news module: {e}")
    NEWS_MODULE_LOADED = False

def detect_fake_news(content):
    if not NEWS_MODULE_LOADED:
        return {'is_fake': False, 'fake_score': 0, 'message': 'Module not loaded'}
    
    try:
        # Replace 'your_function_name' with your actual function
        result = your_function_name(content)
        
        # Convert your result to SafeGuard format
        # Modify this based on what your function returns
        return {
            'is_fake': bool(result),  # Adjust based on your return type
            'fake_score': 50,         # Adjust based on your return type
            'detected_indicators': [],
            'message': 'News analysis complete'
        }
    except Exception as e:
        return {'is_fake': False, 'fake_score': 0, 'message': f'Error: {e}'}
```

## 🧪 Test Your Integration

After copying your folders and updating the wrapper files:

1. **Install dependencies**:
   ```bash
   cd safeguard_app
   pip install -r requirements.txt
   ```

2. **Test the integration**:
   ```bash
   python test_detection.py
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open in browser**: `http://localhost:5000`

## 📞 Need Help?

If you get errors, check:
1. ✅ Folder names are correct in the wrapper files
2. ✅ Function names are correct in the import statements
3. ✅ All dependencies are installed
4. ✅ Your original code works independently

## 🎯 Example with Real Names

If your folders are named:
- `scam_detection_ml` (with function `detect_scam_ml` in `classifier.py`)
- `fake_news_bert` (with function `classify_news` in `model.py`)

Update like this:

```python
# In scam_detector.py
scam_folder_path = os.path.join(os.path.dirname(__file__), '..', 'scam_detection_ml')
from classifier import detect_scam_ml

def detect_scam(content):
    result = detect_scam_ml(content)
    # Convert result format...
```

```python
# In fake_news_detector.py  
news_folder_path = os.path.join(os.path.dirname(__file__), '..', 'fake_news_bert')
from model import classify_news

def detect_fake_news(content):
    result = classify_news(content)
    # Convert result format...
```

Your folders are now integrated into SafeGuard! 🛡️