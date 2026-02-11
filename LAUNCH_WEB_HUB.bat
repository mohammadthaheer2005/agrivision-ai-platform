@echo off
title [INDUSTRIAL WEB HUB V21.0] - DEPLOYMENT SUITE
echo [INIT] INITIALIZING INDUSTRIAL BACKEND ENGINE...
cd backend
start /min "AGRI-AI-BACKEND" python main.py
echo [INIT] BACKEND UPLINK ESTABLISHED ON PORT 8002.
timeout 3
cd ..
echo [INIT] LAUNCHING INDUSTRIAL WEB FRONTEND...
cd frontend
start /min "AGRI-AI-WEB" npm run dev
echo [INIT] WEB DEPLOYMENT SUCCESSFUL.
echo Access the Hub at: http://localhost:5173
pause
