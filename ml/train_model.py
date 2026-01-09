# """
# Train TF-IDF + Logistic Regression model from data/scam_dataset.csv
# CSV must have columns: text,label
# Labels: 0 = Safe, 1 = Spam, 2 = Scam
# Saves:  models/vectorizer.pkl and models/scam_model.pkl
# Run:  python -m ml.train_model
# """
# import os
# import joblib
# import pandas as pd
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report, accuracy_score

# from ml.preprocess import preprocess_text

# def get_model_path():
#     return os.path.join("models", "scam_model.pkl")

# def get_vectorizer_path():
#     return os.path.join("models", "vectorizer.pkl")

# def get_data_path():
#     return os.path.join("data", "scam_dataset.csv")

# def load_dataset(path=None):
#     if path is None:
#         path = get_data_path()
#     if not os.path.exists(path):
#         raise FileNotFoundError(f"Dataset not found at {path}")
#     df = pd.read_csv(path)
#     if "text" not in df.columns or "label" not in df.columns:
#         raise ValueError("CSV must contain 'text' and 'label' columns")
#     return df

# def train():
#     print("Loading dataset...")
#     df = load_dataset()
    
#     print("Preprocessing text...")
#     df["text_clean"] = df["text"].astype(str).apply(preprocess_text)
#     X = df["text_clean"]. tolist()
#     y = df["label"].astype(int).tolist()

#     print(f"Total samples: {len(X)}")
#     print(f"Classes: {set(y)}")

#     min_test_samples = 3 * len(set(y))
#     total_samples = len(X)
    
#     if total_samples < min_test_samples * 2:
#         test_size = max(0.1, min_test_samples / total_samples)
#         use_stratify = False
#         print(f"Small dataset detected ({total_samples} samples). Not using stratified split.")
#     else:
#         test_size = 0.15
#         use_stratify = True

#     stratify_arg = y if use_stratify else None
    
#     print("Splitting data...")
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y, test_size=test_size, random_state=42, stratify=stratify_arg
#     )

#     print("Vectorizing text with TF-IDF...")
#     vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=20000)
#     X_train_tfidf = vectorizer.fit_transform(X_train)
#     X_test_tfidf = vectorizer.transform(X_test)

#     print("Training Logistic Regression model...")
#     clf = LogisticRegression(solver="lbfgs", max_iter=1000, random_state=42)
#     clf.fit(X_train_tfidf, y_train)

#     print("Evaluating model...")
#     preds = clf.predict(X_test_tfidf)
#     acc = accuracy_score(y_test, preds)
#     print(f"Validation Accuracy: {acc}")
#     print("Classification report:")
#     print(classification_report(y_test, preds))

#     print("Saving artifacts...")
#     os.makedirs("models", exist_ok=True)
    
#     vectorizer_path = get_vectorizer_path()
#     model_path = get_model_path()
    
#     joblib.dump(vectorizer, vectorizer_path)
#     print(f"Saved vectorizer to:  {vectorizer_path}")
    
#     joblib.dump(clf, model_path)
#     print(f"Saved model to: {model_path}")
    
#     print("Training complete!")

# if __name__ == "__main__":
#     train()


"""
Train TF-IDF + Logistic Regression model from data/scam_dataset.csv
CSV must have columns: text,label
Labels: 0 = Safe, 1 = Spam, 2 = Scam
Saves:   models/vectorizer.pkl and models/scam_model.pkl
Run:  python -m ml.train_model
"""
import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from ml.preprocess import preprocess_text

def get_model_path():
    return os.path.join("models", "scam_model.pkl")

def get_vectorizer_path():
    return os.path.join("models", "vectorizer.pkl")

def get_data_path():
    return os.path.join("data", "scam_dataset.csv")

def load_dataset(path=None):
    if path is None:
        path = get_data_path()
    if not os.path.exists(path):
        raise FileNotFoundError(f"Dataset not found at {path}")
    df = pd.read_csv(path)
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("CSV must contain 'text' and 'label' columns")
    return df

def train():
    print("Loading dataset...")
    df = load_dataset()
    
    print("Preprocessing text...")
    df["text_clean"] = df["text"].astype(str).apply(preprocess_text)
    X = df["text_clean"]. tolist()
    y = df["label"].astype(int).tolist()

    print(f"Total samples: {len(X)}")
    print(f"Classes distribution: {dict((label, y.count(label)) for label in set(y))}")

    min_test_samples = 3 * len(set(y))
    total_samples = len(X)
    
    if total_samples < min_test_samples * 2:
        test_size = max(0.1, min_test_samples / total_samples)
        use_stratify = False
        print(f"Small dataset detected ({total_samples} samples). Not using stratified split.")
    else:
        test_size = 0.2
        use_stratify = True

    stratify_arg = y if use_stratify else None
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=stratify_arg
    )

    print("Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=5000,
        min_df=2,
        max_df=0.8,
        sublinear_tf=True
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    print("Training Logistic Regression model...")
    clf = LogisticRegression(
        solver="saga",
        max_iter=2000,
        random_state=42,
        C=1.0,
        class_weight="balanced"
    )
    clf.fit(X_train_tfidf, y_train)

    print("\nEvaluating model...")
    preds = clf.predict(X_test_tfidf)
    probs = clf.predict_proba(X_test_tfidf)
    acc = accuracy_score(y_test, preds)
    
    print(f"Validation Accuracy: {acc:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, preds, target_names=["Safe", "Spam", "Scam"]))
    
    avg_confidence = probs. max(axis=1).mean()
    print(f"\nAverage Model Confidence:  {avg_confidence:.4f} ({avg_confidence*100:.2f}%)")

    print("\nSaving artifacts...")
    os.makedirs("models", exist_ok=True)
    
    vectorizer_path = get_vectorizer_path()
    model_path = get_model_path()
    
    joblib.dump(vectorizer, vectorizer_path)
    print(f"Saved vectorizer to:  {vectorizer_path}")
    
    joblib.dump(clf, model_path)
    print(f"Saved model to:  {model_path}")
    
    print("\nTraining complete!")

if __name__ == "__main__":  
    train()