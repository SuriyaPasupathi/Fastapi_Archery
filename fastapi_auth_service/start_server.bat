@echo off
echo Starting FastAPI Auth Service...
echo.
echo The server will run on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
cd /d "%~dp0"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
