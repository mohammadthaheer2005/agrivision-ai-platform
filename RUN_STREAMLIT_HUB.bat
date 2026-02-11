@echo off
title [V23.0 GLOBAL MASTER HUB] - LOCAL TEST LAUNCHER
echo [INIT] INSTALLING INDUSTRIAL DEPENDENCIES...
pip install -r requirements.txt
echo [INIT] LAUNCHING STREAMLIT CLOUD SIMULATOR...
streamlit run streamlit_app.py
pause
