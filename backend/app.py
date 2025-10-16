# backend/app.py
from flask import Flask, request, jsonify
from processing import process_messages_from_list
import pandas as pd
from pathlib import Path
import json

app = Flask(__name__)

# Load sample file on startup for demo
DATA_FILE = Path(__file__).resolve().parent.parent / "sample_data" / "messages.csv"

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts JSON payload:
    { "messages": [ {"message_id": str/int, "sender": str, "text": str, "timestamp": str}, ... ] }
    OR if empty, will analyze sample_data/messages.csv
    """
    payload = request.json or {}
    messages = payload.get("messages")
    if messages is None:
        # load sample
        df = pd.read_csv(DATA_FILE, encoding='utf-8', parse_dates=['timestamp'], on_bad_lines='skip')
        messages = df.to_dict(orient="records")
    # process
    results = process_messages_from_list(messages)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
