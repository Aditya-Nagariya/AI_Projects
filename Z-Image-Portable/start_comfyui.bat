@echo off
cd /d "C:\AI_Projects\Z-Image-Portable"
call "venv\Scripts\activate.bat"
python main.py --listen 127.0.0.1 --port 8189
pause
