@echo off
setlocal enabledelayedexpansion

:: Navigation
set "BASE_DIR=%~dp0"
cd /d "%BASE_DIR%"

echo [RTX 5090 Fixer] Starting local environment repair...

:: 1. Activate venv
if exist "venv\Scripts\activate.bat" (
    echo [Local Fixer] Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No venv found.
    pause
    exit /b
)

:: Fix for LLVM ERROR: Symbol not found: __svml_cosf16_ha
set MKL_THREADING_LAYER=GNU
set KMP_DUPLICATE_LIB_OK=TRUE
set TF_ENABLE_ONEDNN_OPTS=0

:: 2. Install Intel MKL components into venv
echo [Local Fixer] Installing Intel MKL components...
pip install mkl mkl-include intel-openmp

:: 3. Re-install MMCV for MuseTalk
echo [Local Fixer] Repairing MMCV / MMPose...
pip uninstall -y mmcv mmcv-full mmengine
pip install -U openmim
mim install mmengine
:: Force install mmcv (using the compatible version for modern torch)
pip install mmcv>=2.1.0 -f https://download.openmmlab.com/mmcv/dist/cu121/torch2.4/index.html

:: 4. Patch webrtcvad (if not already patched)
python -c "import webrtcvad; import os; path = webrtcvad.__file__.replace('__init__.py', 'webrtcvad.py') if '__init__.py' in webrtcvad.__file__ else webrtcvad.__file__; f=open(path, 'r'); c=f.read(); f.close(); f=open(path, 'w'); f.write(c.replace('register_finder(pkgutil.ImpImporter', '# register_finder(pkgutil.ImpImporter')); f.close()" 2>nul

echo.
echo [Local Fixer] Launching ComfyUI with RTX 5090 workarounds...
python main.py --listen 127.0.0.1 --port 8188

pause