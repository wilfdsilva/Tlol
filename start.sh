#!/usr/bin/env bash

# Start FastAPI backend in the background on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend on Render's assigned port
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
