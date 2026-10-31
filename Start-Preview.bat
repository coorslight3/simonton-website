@echo off
rem Double-click (Windows) to preview the website at http://localhost:8123
cd /d "%~dp0"
start "" http://localhost:8123
python serve.py 8123
