#!/bin/bash
# Start Sejrliste Web App (Mobil Support)
cd "/home/rasmus/Desktop/sejrliste systemet"
source venv/bin/activate
streamlit run web_app.py --server.port 8501 --server.address 0.0.0.0
