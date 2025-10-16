# Shadow Work — Revealing the Hidden Effort in Teams

Prototype that analyzes team communications and surfaces "shadow work" contributions
(reminders, emotional support, coordination).

## Quick start (local)

1. Create a Python venv:

2. Install dependencies:

3. Start the backend (Flask):

4. Backend will run by default at http://127.0.0.1:5000.

5. In another terminal, start the dashboard

   ```bash
      python -m venv venv
      venv\Scripts\activate
      pip install -r requirements.txt
      cd shadow-work/backend
      python app.py
      cd ..
      cd shadow-work/dashboard
      streamlit run dashboard.py

Streamlit UI usually opens at http://localhost:8501.

