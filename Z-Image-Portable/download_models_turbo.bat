@echo off
setlocal enabledelayedexpansion

set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

set "VENV_PYTHON=%BASE_DIR%venv\Scripts\python.exe"
set "HF_XET_HIGH_PERFORMANCE=1"

echo ============================================
echo  Z-Image Turbo Model Downloader
echo ============================================
echo.

:: Check venv
if not exist "%VENV_PYTHON%" (
    echo [ERROR] Venv not found. Run run_portable.bat first.
    pause
    exit /b 1
)

echo [1/3] Downloading diffusion model (z_image_turbo_bf16.safetensors ~12.3GB)...
echo       This is the biggest file, please be patient.
if exist "models\diffusion_models\z_image_turbo_bf16.safetensors" (
    echo       Already exists, skipping.
) else (
    "%VENV_PYTHON%" -c "import os; os.environ['HF_XET_HIGH_PERFORMANCE']='1'; from huggingface_hub import hf_hub_download; hf_hub_download('Comfy-Org/z_image_turbo', 'split_files/diffusion_models/z_image_turbo_bf16.safetensors', local_dir='models')"
    if errorlevel 1 (
        echo [ERROR] Failed to download diffusion model.
        pause
        exit /b 1
    )
    :: Move from split_files path to correct location
    if exist "models\split_files\diffusion_models\z_image_turbo_bf16.safetensors" (
        move "models\split_files\diffusion_models\z_image_turbo_bf16.safetensors" "models\diffusion_models\z_image_turbo_bf16.safetensors"
    )
)
echo.

echo [2/3] Downloading text encoder (qwen_3_4b.safetensors ~7.6GB)...
if exist "models\text_encoders\qwen_3_4b.safetensors" (
    echo       Already exists, skipping.
) else (
    "%VENV_PYTHON%" -c "import os; os.environ['HF_XET_HIGH_PERFORMANCE']='1'; from huggingface_hub import hf_hub_download; hf_hub_download('Comfy-Org/z_image_turbo', 'split_files/text_encoders/qwen_3_4b.safetensors', local_dir='models')"
    if errorlevel 1 (
        echo [ERROR] Failed to download text encoder.
        pause
        exit /b 1
    )
    if exist "models\split_files\text_encoders\qwen_3_4b.safetensors" (
        move "models\split_files\text_encoders\qwen_3_4b.safetensors" "models\text_encoders\qwen_3_4b.safetensors"
    )
)
echo.

echo [3/3] Checking VAE (ae.safetensors)...
if exist "models\vae\ae.safetensors" (
    echo       Already exists, skipping.
) else (
    "%VENV_PYTHON%" -c "import os; os.environ['HF_XET_HIGH_PERFORMANCE']='1'; from huggingface_hub import hf_hub_download; hf_hub_download('Comfy-Org/z_image_turbo', 'split_files/vae/ae.safetensors', local_dir='models')"
    if errorlevel 1 (
        echo [ERROR] Failed to download VAE.
        pause
        exit /b 1
    )
    if exist "models\split_files\vae\ae.safetensors" (
        move "models\split_files\vae\ae.safetensors" "models\vae\ae.safetensors"
    )
)

echo.
echo ============================================
echo  All models downloaded successfully!
echo ============================================
echo.
echo You can now run: run_portable.bat
pause
