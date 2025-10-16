# Shadow Work — Revealing the Hidden Effort in Teams

*AI-powered analytics to make invisible teamwork visible.*

## 📖 Overview

**Shadow Work** is an AI system designed to uncover *invisible contributions* in team environments — such as reminders, emotional support, and coordination — that often go unrecognized in traditional productivity metrics.  

By analyzing communication data using **Natural Language Processing (NLP)** and **sentiment analysis**, Shadow Work identifies and visualizes hidden efforts to promote fair recognition, healthier collaboration, and improved group dynamics.

---

## 🎯 Problem Statement

In group projects and workplaces, many valuable contributions remain unseen — organizing meetings, resolving conflicts, offering motivation, and maintaining morale.  
Traditional metrics track only tangible outputs, leaving “shadow work” invisible.

---

## 💡 Objective

To build an **AI-driven system** that:
- Detects hidden labor types (reminders, coordination, emotional support).
- Quantifies them using NLP and sentiment metrics.
- Visualizes insights via an interactive dashboard.
- Encourages fair recognition and improved teamwork.

---

## 🧩 System Architecture

``` mermaid

graph LR
   A[Chat Logs / Emails / Transcripts] --> B[Text Preprocessing]
   B --> C[NLP + Sentiment Analysis (DistilBERT)]
   C --> D[Intent Classification (Rule-based / ML Model)]
   D --> E[Shadow Work Scoring Engine]
   E --> F[Visualization Dashboard (Streamlit)]
```

### Quick start (local)

1. Create a Python venv
2. Install dependencies
3. Start the backend (Flask)
4. Backend will run by default at http://127.0.0.1:5000.
5. In another terminal, start the dashboard

Terminal - 1

   ```bash
      python -m venv venv
      venv\Scripts\activate
      pip install -r requirements.txt
      cd shadow-work/backend
      python app.py
   ```

Terminal - 2

   ```bash
      python -m venv venv
      venv\Scripts\activate
      cd shadow-work/dashboard
      streamlit run dashboard.py
   ```

Streamlit UI usually opens at http://localhost:8501.





