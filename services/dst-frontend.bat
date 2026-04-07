@echo off
TITLE Campus Ride - Frontend Service
:: Using relative paths based on script location
set BASE_DIR=%~dp0..
cd /d "%BASE_DIR%\frontend"

echo Starting Frontend Development Server in %cd%...
pnpm dev
