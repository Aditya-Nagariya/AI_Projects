@echo off
setlocal enabledelayedexpansion

:: Get the current folder path
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

echo [Z-Image Portable] Checking environment...

:: Define venv path
set "VENV_DIR=%BASE_DIR%venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [Z-Image Portable] Environment not found. Creating new venv...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Python not found in PATH. Please install Python.
        pause
        exit /b
    )
    
    echo [Z-Image Portable] Installing core requirements...
    call "%VENV_DIR%\Scripts\activate.bat"
    python -m pip install --upgrade pip
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
    pip install -r requirements.txt
    
    echo [Z-Image Portable] Installing Z-Image dependencies...
    pip install transformers loguru accelerate huggingface_hub
    
    echo [Z-Image Portable] Initialization complete.
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

echo [Z-Image Portable] Launching ComfyUI on http://127.0.0.1:8189 ...
python main.py --listen 127.0.0.1 --port 8189

pause