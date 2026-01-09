"""
Prediction utilities: load model/vectorizer and run predictions.

Provides:
- ScamPredictor class with predict(text) method which returns:
  {
    "predicted_label": int,
    "confidence": float,
    "probabilities": [float]
  }

If model files are missing, predict will raise FileNotFoundError with clear message.
"""
import os
import joblib
import numpy as np

from ml.preprocess import preprocess_text

class ScamPredictor:
    def __init__(self, model_path="models/scam_model.pkl", vectorizer_path="models/vectorizer.pkl"):
        self.model_path = model_path
        self.vectorizer_path = vectorizer_path
        self.model = None
        self.vectorizer = None
        self._load()

    def _load(self):
        if not os.path.exists(self.model_path) or not os.path.exists(self.vectorizer_path):
            # Do not crash silently; provide helpful message
            raise FileNotFoundError(
                "Model or vectorizer not found. Please run training: python -m ml.train_model\n"
                f"Expected model: {self.model_path}\nExpected vectorizer: {self.vectorizer_path}"
            )
        self.vectorizer = joblib.load(self.vectorizer_path)
        self.model = joblib.load(self.model_path)

    def predict(self, text: str) -> dict:
        if self.model is None or self.vectorizer is None:
            self._load()
        clean = preprocess_text(text)
        X = self.vectorizer.transform([clean])
        probs = self.model.predict_proba(X)[0]
        pred_label = int(np.argmax(probs))
        confidence = float(probs[pred_label])
        return {
            "predicted_label": pred_label,
            "confidence": confidence,
            "probabilities": probs.tolist()
        }