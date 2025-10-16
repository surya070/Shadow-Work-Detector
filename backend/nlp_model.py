# backend/nlp_model.py
from transformers import pipeline
from typing import Dict
import os
import re

class SentimentAnalyzer:
    """
    Uses transformers sentiment pipeline (can be swapped to a distil or fine-tuned model).
    Output: {"label": "POSITIVE"/"NEGATIVE", "score": float}
    """
    def __init__(self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"):
        # initialize pipeline (downloads model on first run)
        self.pipe = pipeline("sentiment-analysis", model=model_name, device=-1)  # CPU default

    def analyze(self, text: str) -> Dict:
        if not text:
            return {"label": "NEUTRAL", "score": 0.0}
        out = self.pipe(text[:512])[0]
        # normalize
        label = out.get("label")
        score = float(out.get("score", 0.0))
        # convert label to a more nuanced one for our app
        if label == "POSITIVE":
            return {"label": "positive", "score": score}
        elif label == "NEGATIVE":
            return {"label": "negative", "score": score}
        else:
            return {"label": label.lower(), "score": score}

class IntentClassifier:
    """
    Prototype intent classifier.
    Returns one of: reminder, encouragement, coordination, task-update, neutral
    Replace with a trained classifier later.
    """
    def __init__(self):
        # You can load a saved sklearn/torch model here if you have one
        self.simple_rules = [
            ("reminder", [r"\bremind\b", r"\breminder\b", r"\bdon't forget\b", r"\bsubmit\b", r"\bdeadline\b"]),
            ("encouragement", [r"\bwell done\b", r"\bappreciate\b", r"\bthank(s| you)\b", r"\bdon't worry\b", r"\bproud of\b", r"\bkeep it up\b"]),
            ("coordination", [r"\bschedule\b", r"\bsync\b", r"\bmeeting\b", r"\bassign\b", r"\bdistribut(e|ion)\b", r"\bconnect\b"]),
            ("task-update", [r"\bupdated\b", r"\bcheck the updated\b", r"\buploaded\b", r"\bsubmitted\b", r"\bfix(ed)?\b"]),
        ]

    def predict(self, text: str) -> str:
        t = text.lower()
        # rule-based matching
        for label, patterns in self.simple_rules:
            for pat in patterns:
                if re.search(pat, t):
                    return label
        # emoticon/emoji-based encouragement detection
        if any(x in t for x in ["💪", "😊", "👍", "🙏", "🙂"]):
            return "encouragement"
        # "I will handle" or "I'll handle" => coordination/support
        if re.search(r"\b(i will handle|i'll handle|i can handle|i will take)\b", t):
            return "coordination"
        return "neutral"
