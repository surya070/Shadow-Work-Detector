# backend/scoring.py
from typing import List, Dict, Any
from collections import defaultdict
import math

# scoring weights (tweakable)
INTENT_WEIGHTS = {
    "reminder": 2.0,
    "encouragement": 1.5,
    "coordination": 2.5,
    "task-update": 1.0,
    "neutral": 0.0
}
SENTIMENT_WEIGHTS = {
    "positive": 1.2,
    "negative": -0.5,
    "neutral": 0.0
}

def compute_scores(processed_messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Returns scores per sender, plus breakdown of counts by type.
    """
    users = defaultdict(lambda: {
        "counts": defaultdict(int),
        "intent_score": 0.0,
        "sentiment_score": 0.0,
        "messages": 0
    })

    for m in processed_messages:
        sender = m.get("sender", "unknown")
        intent = m.get("intent", "neutral")
        sentiment = m.get("sentiment", {"label": "neutral", "score": 0.0})
        users[sender]["messages"] += 1
        users[sender]["counts"][intent] += 1

        # intent contribution
        iw = INTENT_WEIGHTS.get(intent, 0.0)
        users[sender]["intent_score"] += iw

        # sentiment contribution (positive increases shadow-work-credit if supportive)
        sl = sentiment.get("label", "neutral")
        sscore = sentiment.get("score", 0.0)
        sw = SENTIMENT_WEIGHTS.get(sl, 0.0)
        # weight by confidence
        users[sender]["sentiment_score"] += sw * sscore

    # produce normalized shadow work score
    result = {}
    max_raw = 0.0
    raw_scores = {}
    for u, v in users.items():
        raw = v["intent_score"] + v["sentiment_score"]
        # small boost for participation frequency (log)
        freq_boost = math.log1p(v["messages"]) * 0.1
        raw = raw + freq_boost
        raw_scores[u] = raw
        if raw > max_raw:
            max_raw = raw

    # normalize to 0-100
    for u, raw in raw_scores.items():
        norm = (raw / max_raw * 100) if max_raw > 0 else 0.0
        result[u] = {
            "raw": raw,
            "score": round(norm, 2),
            "messages": users[u]["messages"],
            "counts": dict(users[u]["counts"]),
            "intent_score": round(users[u]["intent_score"], 2),
            "sentiment_score": round(users[u]["sentiment_score"], 2)
        }

    # also provide leaderboard sorted list
    leaderboard = sorted(
        [{"user": u, **result[u]} for u in result],
        key=lambda x: x["score"], reverse=True
    )

    return {"per_user": result, "leaderboard": leaderboard}
