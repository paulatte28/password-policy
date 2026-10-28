@echo off
title PasswordPolicy Checker Launcher
echo ==========================================================
echo Starting PasswordPolicy Checker (Project #23 - IT23/L)
echo Author: Kristine Paula S. Coretico
echo ==========================================================
if exist ".venv\Scripts\python.exe" (
    start cmd /k "title PasswordPolicy Backend && .\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8000"
) else (
    start cmd /k "title PasswordPolicy Backend && py -m uvicorn backend.main:app --reload --port 8000"
)
start cmd /k "title PasswordPolicy Frontend && cd frontend && npm run dev"
echo Backend running on:  http://localhost:8000
echo Frontend running on: http://localhost:5173
echo.
