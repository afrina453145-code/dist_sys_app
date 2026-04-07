@echo off
TITLE Campus Ride - Backend Service
:: Using relative paths based on script location
set BASE_DIR=%~dp0..
cd /d "%BASE_DIR%\backend"

echo Starting Backend Server in %cd%...
call .venv\Scripts\activate
python server.py
