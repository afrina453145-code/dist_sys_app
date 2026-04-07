@echo off
:: This script registers the services using the local nssm.exe
cd /d "%~dp0"

echo [1/2] Installing DST_Backend Service...
.\nssm.exe install DST_Backend "%~dp0dst-backend.bat"
.\nssm.exe set DST_Backend AppDirectory "%~dp0..\backend"
.\nssm.exe set DST_Backend Description "Campus Ride Backend FastAPI"

echo [2/2] Installing DST_Frontend Service...
.\nssm.exe install DST_Frontend "%~dp0dst-frontend.bat"
.\nssm.exe set DST_Frontend AppDirectory "%~dp0..\frontend"
.\nssm.exe set DST_Frontend Description "Campus Ride Next.js Frontend"

echo Starting services...
.\nssm.exe start DST_Backend
.\nssm.exe start DST_Frontend

echo Done! Check services.msc to verify.
pause
