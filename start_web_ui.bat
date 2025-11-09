@echo off
echo ====================================================================
echo  MEM-LLM Web UI Launcher
echo ====================================================================
echo.
echo Starting API Server...
cd "Memory LLM"
start "Mem-LLM API Server" python -m mem_llm.api_server

echo Waiting for API Server to start...
timeout /t 5 /nobreak > nul

echo.
echo Opening Web UI in browser...
start "" "web_ui\index.html"

echo.
echo ====================================================================
echo  Web UI is ready!
echo ====================================================================
echo.
echo In the Web UI:
echo   1. Enter User ID (e.g., user123)
echo   2. Select Backend (Ollama/LM Studio)
echo   3. Click "Connect"
echo   4. Start chatting!
echo.
echo To stop: Close the API Server window
echo.
pause

