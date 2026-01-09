# 🛡️ SafeGuard - AI-Powered Scam Detection System

SafeGuard is an advanced AI-powered system that detects scams, spam, and fake news using machine learning and Google's security APIs.

## 🌟 Features

- **🔍 Scam Detection** - Analyze messages for scam indicators
- **📰 Fake News Detection** - Verify news credibility with AI
- **🌐 Multi-language Support** - Automatic translation and analysis
- **🛡️ URL Safety Checking** - Google Safe Browsing integration
- **📊 Risk Scoring** - Comprehensive threat assessment
- **💻 Web Interface** - User-friendly dashboard

## 🚀 Live Demo

**🌐 Access SafeGuard:** [Coming Soon - Deploy to see URL]

## 🛠️ Technologies Used

### Google Technologies
- **Google Safe Browsing API** - URL threat detection
- **Google Cloud Translate API** - Multi-language support
- **Google Fonts** - Professional typography

### AI & Machine Learning
- **scikit-learn** - Machine learning models
- **pandas** - Data processing
- **numpy** - Numerical computations

### Web Framework
- **Flask** - Python web framework
- **Bootstrap** - Responsive UI
- **Font Awesome** - Icons

## 📁 Project Structure

```
SafeGuard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── ml/                  # Machine learning models
├── detection_modules/   # Scam & fake news detection
├── google_ai/          # Google API integrations
├── utils/              # Utility functions
├── models/             # Trained ML models
└── data/               # Training datasets
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager

### Local Development
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/safeguard-detector.git
cd safeguard-detector

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Environment Variables (Optional)
```bash
SAFE_BROWSING_API_KEY=your_google_safe_browsing_api_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_service_account.json
```

## 🌐 Deployment

### Deploy to Render.com (Free)
1. Fork this repository
2. Connect to Render.com
3. Deploy with these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`

### Deploy to Google Cloud
```bash
gcloud app deploy app.yaml
```

## 📊 API Endpoints

### Scam Detection
```bash
POST /api/detect-scam
Content-Type: application/json

{
  "message": "Your message to analyze"
}
```

### Fake News Detection
```bash
POST /api/analyze-news
Content-Type: application/json

{
  "content": "News content to verify"
}
```

## 🔒 Security Features

- **Real-time URL scanning** with Google Safe Browsing
- **ML-based content analysis** for scam detection
- **Multi-language threat detection**
- **Comprehensive risk scoring**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Safe Browsing API for URL security
- Google Cloud Translate for multi-language support
- scikit-learn community for ML tools
- Flask community for web framework

## 📞 Support

For support, email: [mohammedshameem636@gmail.com]

---

**⭐ Star this repository if SafeGuard helped protect you from scams!**
