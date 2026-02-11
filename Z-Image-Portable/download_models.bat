@echo off
setlocal enabledelayedexpansion

set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

set "VENV_DIR=%BASE_DIR%venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [ERROR] Please run 'run_portable.bat' first to initialize the environment.
    pause
    exit /b
)

call "%VENV_DIR%\Scripts\activate.bat"

echo [Z-Image Portable] Downloading models from Hugging Face...
echo This might take a while depending on your internet speed (approx 12GB total).

:: Create directories if they don't exist
mkdir "models\vae" 2>nul
mkdir "models	ext_encoders" 2>nul
mkdir "models\diffusion_models" 2>nul

:: Download VAE
if not exist "models\vae\ae.safetensors" (
    echo Downloading VAE (ae.safetensors)...
    huggingface-cli download Tongyi-MAI/Z-Image ae.safetensors --local-dir models\vae --local-dir-use-symlinks False
) else (
    echo VAE already exists.
)

:: Download Text Encoder
if not exist "models	ext_encoders\qwen_3_4b.safetensors" (
    echo Downloading Text Encoder (qwen_3_4b.safetensors)...
    huggingface-cli download Tongyi-MAI/Z-Image qwen_3_4b.safetensors --local-dir models	ext_encoders --local-dir-use-symlinks False
) else (
    echo Text Encoder already exists.
)

:: Download Diffusion Model (Base)
if not exist "models\diffusion_models\z_image_bf16.safetensors" (
    echo Downloading Diffusion Model (z_image_bf16.safetensors)...
    huggingface-cli download Tongyi-MAI/Z-Image z_image_bf16.safetensors --local-dir models\diffusion_models --local-dir-use-symlinks False
) else (
    echo Diffusion Model already exists.
)

echo.
echo [Z-Image Portable] All models downloaded successfully!
echo You can now run 'run_portable.bat' to start ComfyUI.
pause
