#!/bin/bash
cd "$(dirname "$0")"
python3 -m streamlit run ml_dashboard.py --server.port 8501
