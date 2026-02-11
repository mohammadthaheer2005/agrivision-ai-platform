@echo off
title AGRI-COMMAND UNIFIED MASTER LAUNCHER
echo [1/3] CLEANING SYSTEM...
:: Kill existing processes on ports 8002, 8501, 8502
powershell -Command "Get-NetTCPConnection -LocalPort 8002, 8501, 8502 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }"

echo [2/3] STARTING BACKEND...
cd backend
start /min "AGRI-BACKEND" python main.py
timeout 5
cd ..

echo [3/3] STARTING FRONTEND...
start /min "AGRI-STREAMLIT" streamlit run streamlit_app.py --server.port 8501
echo ====================================================
echo SYSTEM READY
echo Backend: http://localhost:8002
echo Frontend: http://localhost:8501
echo ====================================================
pause
