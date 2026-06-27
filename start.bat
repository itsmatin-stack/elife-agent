@echo off
title E LIFE Agent
color 0A
echo.
echo  ========================================
echo     E LIFE Agent v0.1.0
echo     Your AI-Powered Life
echo  ========================================
echo.
echo  [*] Server start ho raha hai...
echo  [*] Browser mein khul jayega automatically
echo  [*] Band karne ke liye ye window close karo
echo.

cd /d "%~dp0"

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python nahi mila! Python install karo.
    pause
    exit
)

:: Check .env
if not exist ".env" (
    echo  [WARNING] .env file nahi mili - copy kar raha hoon...
    copy ".env.example" ".env" >nul
    echo  [!] .env file mein GROQ_API_KEY daalo!
)

:: Start server in background aur browser kholo
start "" /B python -m uvicorn api.main:app --port 8000 --log-level warning

:: Wait for server
echo  [*] Server ready ho raha hai...
timeout /t 3 /nobreak >nul

:: Open browser
start "" "http://localhost:8000"

echo  [OK] E LIFE Agent chal raha hai!
echo  [OK] Browser mein: http://localhost:8000
echo.
echo  Band karne ke liye Ctrl+C dabaо ya ye window close karo.
echo.

:: Keep window open aur server alive
python -m uvicorn api.main:app --port 8000 --log-level warning
