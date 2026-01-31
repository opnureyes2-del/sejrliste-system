#!/bin/bash
# Start Victory List Web App (English - Mobile Support)
cd "/home/rasmus/Desktop/sejrliste systemet"
source venv/bin/activate
streamlit run web_app_en.py --server.port 8502 --server.address 0.0.0.0
