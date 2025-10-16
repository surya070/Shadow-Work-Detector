# dashboard/dashboard.py
import streamlit as st
import pandas as pd
import requests
import altair as alt
from pathlib import Path
import time

st.set_page_config(page_title="Shadow Work Dashboard", layout="wide")

BACKEND_URL = "http://127.0.0.1:5000"

st.title("Shadow Work — Revealing Hidden Contributions")
st.markdown("Upload team messages or use the sample dataset to analyze invisible work.")

uploaded = st.file_uploader("Upload CSV (columns: message_id,sender,text,timestamp)", type=["csv"])
use_sample = st.button("Use sample data")

if uploaded is not None:
    df = pd.read_csv(uploaded)
    messages = df.to_dict(orient="records")
    st.write("Preview:", df.head())
    if st.button("Analyze uploaded data"):
        with st.spinner("Sending to backend..."):
            r = requests.post(f"{BACKEND_URL}/analyze", json={"messages": messages})
            r.raise_for_status()
            resp = r.json()
            st.session_state["last_result"] = resp
elif use_sample:
    # call backend without payload
    with st.spinner("Analyzing sample data..."):
        r = requests.post(f"{BACKEND_URL}/analyze", json={})
        r.raise_for_status()
        resp = r.json()
        st.session_state["last_result"] = resp
else:
    st.info("Upload a file or press 'Use sample data' to begin.")

if "last_result" in st.session_state:
    res = st.session_state["last_result"]
    per_user = res["scores"]["per_user"]
    leaderboard = res["scores"]["leaderboard"]
    processed = pd.DataFrame(res["processed_messages"])

    st.subheader("Leaderboard")
    lb_df = pd.DataFrame(leaderboard)
    st.table(lb_df[["user", "score", "messages"]])

    st.subheader("Per-user breakdown")
    # show each user's counts and scores
    cols = st.columns(3)
    for i, (user, info) in enumerate(per_user.items()):
        with cols[i % 3]:
            st.metric(label=user, value=f"{info['score']} / 100", delta=f"{info['messages']} msgs")
            st.write("Intent counts:", info["counts"])
            st.write("Intent score:", info["intent_score"])
            st.write("Sentiment score:", info["sentiment_score"])

    st.subheader("Message timeline and intents")
    if not processed.empty:
        processed['timestamp'] = pd.to_datetime(processed['timestamp'])
        processed = processed.sort_values('timestamp')
        chart = alt.Chart(processed).mark_circle(size=60).encode(
            x='timestamp:T',
            y=alt.Y('sender:N', sort=alt.EncodingSortField(field="sender", order="descending")),
            color='intent:N',
            tooltip=['sender', 'text', 'intent', 'sentiment']
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

    st.subheader("Raw processed messages")
    st.dataframe(processed[["timestamp","sender","text","intent","sentiment"]])

