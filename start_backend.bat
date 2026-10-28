@echo off
title PasswordPolicy Checker - FastAPI Backend
echo Starting FastAPI Backend on http://localhost:8000 using .venv...
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -m uvicorn backend.main:app --reload --port 8000
) else (
    py -m uvicorn backend.main:app --reload --port 8000
)
pause
