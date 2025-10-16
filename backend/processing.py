# backend/processing.py
from typing import List, Dict, Any
from nlp_model import SentimentAnalyzer, IntentClassifier
from scoring import compute_scores
from datetime import datetime
import re

sentiment = SentimentAnalyzer()
intenter = IntentClassifier()

def normalize_text(text: str) -> str:
    if text is None:
        return ""
    t = text.strip()
    # minimal cleaning
    t = re.sub(r'\s+', ' ', t)
    return t

def process_single_message(msg: Dict[str, Any]) -> Dict[str, Any]:
    text = normalize_text(msg.get("text",""))
    sender = msg.get("sender", "unknown")
    ts = msg.get("timestamp")
    # parse timestamp to ISO-like string if not already
    try:
        if ts and not isinstance(ts, str):
            ts = str(ts)
    except Exception:
        ts = None

    s = sentiment.analyze(text)
    intent = intenter.predict(text)

    return {
        "message_id": msg.get("message_id"),
        "sender": sender,
        "text": text,
        "timestamp": ts,
        "sentiment": s,          # dict with label & score
        "intent": intent         # single intent label
    }

def process_messages_from_list(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    processed = [process_single_message(m) for m in messages]
    # aggregate per user
    scores = compute_scores(processed)
    return {
        "processed_messages": processed,
        "scores": scores
    }
