#!/usr/bin/env bash
cd "/home/rasmus/Desktop/sejrliste systemet"
exec "./venv/bin/streamlit" run web_app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless true
