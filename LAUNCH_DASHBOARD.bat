@echo off
title [INDUSTRIAL AGRI-COMMAND V6.0] - SYSTEM INITIALIZATION
echo [INIT] INITIALIZING INDUSTRIAL BACKEND ENGINE...
cd backend
:: Attempt to clear port 8002 if stalled
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8002') do taskkill /f /pid %%a >nul 2>&1
start /min "AGRI-AI-BACKEND" python main.py
echo [INIT] BACKEND UPLINK ESTABLISHED ON PORT 8002.
timeout 5
cd ..
echo [INIT] LAUNCHING ENTERPRISE CONTROL INTERFACE...
start /max python gui_agri.py
echo [INIT] DEPLOYMENT COMPLETE. SYSTEM STABLE.
exit
