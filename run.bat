@echo off
title Competitive Intelligence Agent Launcher
echo ====================================================================
echo   COMPETITIVE INTELLIGENCE RESEARCH AGENT - STARTUP SCRIPT
echo ====================================================================
echo.

echo [1/3] Installing Python backend dependencies...
python -m pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo [WARNING] Failed to install some Python packages. Ensure Python is in your PATH.
)
echo.

echo [2/3] Starting FastAPI Backend server...
start "Agent Backend (FastAPI)" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"
echo Backend launch command sent.
echo.

echo [3/3] Starting React Frontend dev server...
cd frontend
start "Agent Frontend (Vite)" cmd /k "npm run dev"
echo Frontend launch command sent.
cd ..
echo.

echo ====================================================================
echo   SERVICES LAUNCHED SUCCESSFULLY
echo ====================================================================
echo.
echo   - Frontend: http://localhost:5173
echo   - Backend API: http://127.0.0.1:8000
echo.
echo   Close the popped terminal windows to stop the servers.
echo ====================================================================
pause
