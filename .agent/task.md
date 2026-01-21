# ComfyUI + MuseTalk Project - PAUSED STATE
## Last Updated: 2026-01-21
## Status: ⏸️ PAUSED - Resumable

---

## 🎯 RESUME CHECKLIST (Start Here When Returning)

1. **Activate ComfyUI environment:**
   ```powershell
   cd C:\AI_Projects\ComfyUI
   .\venv\Scripts\Activate.ps1
   ```

2. **Start ComfyUI:**
   ```powershell
   python main.py
   ```

3. **Verify MuseTalk loads** - Should see in console:
   ```
   9.7 seconds: C:\AI_Projects\ComfyUI\custom_nodes\ComfyUI-MuseTalk
   ```

4. **Open browser:** http://127.0.0.1:8188

5. **Load workflow:** `neural_twin_v38_advanced.json` (or latest version)

---

## 📊 Environment Overview

| Environment | Location | Python | PyTorch | CUDA | Status |
|-------------|----------|--------|---------|------|--------|
| **ComfyUI venv** | `C:\AI_Projects\ComfyUI\venv` | 3.11.9 | 2.5.1+cu124 | 12.4 | ✅ Working |
| **env_cuda** | Conda env | 3.12 | 2.3.1+cu121 | 12.1 | ✅ Fixed |

**Hardware:** NVIDIA GeForce RTX 5090 (sm_120 Blackwell, 32GB VRAM)
- Uses PTX forward compatibility (no native sm_120 kernels yet)
- Expect warning: "sm_120 is not compatible" - **THIS IS COSMETIC, IT WORKS**

---

## ✅ COMPLETED WORK

### 1. MuseTalk Import Fix (2026-01-16)
**Problem:** `ImportError: DLL load failed while importing _ext` from mmcv

**Root Cause:** mmcv was compiled for PyTorch 2.6.0, user had upgraded to 2.9.1

**Solution Applied:**
1. Downgraded to PyTorch 2.5.1+cu124 (2.9.1 had C++ `'std': ambiguous symbol` error)
2. Rebuilt mmcv 2.1.0 from source:
   ```powershell
   cd C:\Users\Admin\AppData\Local\Temp\mmcv_build
   pip install -e . -v
   ```
3. Rebuilt xtcocotools for NumPy 2.x:
   ```powershell
   pip install git+https://github.com/jin-s13/xtcocoapi.git
   ```
4. Patched whisper to load to CPU first (RTX 5090 GPU init issue)

**Files Modified:**
| File | Change |
|------|--------|
| `musetalk/models/unet.py` | `weights_only=False` |
| `musetalk/utils/face_detection/detection/sfd/sfd_detector.py` | `weights_only=False` |
| `musetalk/utils/face_parsing/__init__.py` | `weights_only=False` |
| `musetalk/utils/face_parsing/resnet.py` | `weights_only=False` |
| `musetalk/utils/preprocessing.py` | `weights_only=False` |
| `musetalk/whisper/whisper/__init__.py` | `device = "cpu"` for RTX 5090 |

**Git:** Commit `a567a5b9` pushed to `https://github.com/Aditya-Nagariya/AI_Projects.git`

### 2. env_cuda Recovery (2026-01-21)
**Problem:** `OSError: [WinError 127] c10_cuda.dll` - PyTorch broken

**Root Cause:** Mixed versions from prior experiments:
- torch: 2.3.1 (stable)
- torchaudio: 2.6.0.dev20250430+cu128 (nightly) ← MISMATCH

**Solution Applied:**
```powershell
conda activate env_cuda
pip uninstall torch torchvision torchaudio -y
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

---

## ❌ KNOWN ISSUES / WHAT WENT WRONG

### Issue 1: RTX 5090 Compatibility Warnings
- **Status:** Expected behavior, not a bug
- **Message:** `NVIDIA GeForce RTX 5090 with CUDA capability sm_120 is not compatible`
- **Impact:** None - works via PTX JIT compilation
- **Fix:** Wait for PyTorch cu130+ release

### Issue 2: mmcv Requires Rebuild on PyTorch Upgrade
- **Lesson:** If you upgrade PyTorch, you MUST rebuild mmcv from source
- **Command:** 
  ```powershell
  cd C:\Users\Admin\AppData\Local\Temp\mmcv_build
  pip install -e . -v --no-build-isolation
  ```

### Issue 3: Neural Twin Workflow Blocked (Prior Issue)
- **Status:** NOT ADDRESSED THIS SESSION
- **Problem:** v37 workflow failed - KSampler incompatible with LTXBaseModel
- **Error:** `missing attention_mask`
- **Attempted:** v38 with LTXVScheduler + SamplerCustomAdvanced
- **Files:** `neural_twin_v38_advanced.json`

---

## 📁 KEY FILE LOCATIONS

| Purpose | Path |
|---------|------|
| ComfyUI Root | `C:\AI_Projects\ComfyUI` |
| Virtual Env | `C:\AI_Projects\ComfyUI\venv` |
| MuseTalk Node | `C:\AI_Projects\ComfyUI\custom_nodes\ComfyUI-MuseTalk` |
| mmcv Source | `C:\Users\Admin\AppData\Local\Temp\mmcv_build` |
| Task State | `C:\AI_Projects\ComfyUI\.agent\task.md` |
| Git Remote | `https://github.com/Aditya-Nagariya/AI_Projects.git` |

### Workflow Files
- `neural_twin_v38_advanced.json` - Latest LTX workflow attempt
- `neural_twin_v37_fixed.json` - Failed (KSampler issue)

### Model Files
- `models/checkpoints/ltx-video-2b-v0.9.safetensors`
- `models/text_encoders/umt5-xxl-enc-bf16.safetensors`
- `models/diffusers/TMElyralab/MuseTalk/` - MuseTalk models

---

## 🔮 PENDING WORK (When Resuming)

1. **Test MuseTalk end-to-end** - Load a MuseTalk workflow and generate lip-sync video
2. **Fix Neural Twin v38** - Debug LTX-Video sampling pipeline
3. **Upgrade PyTorch** - When cu130 releases, upgrade for native RTX 5090 support
4. **Clean up deprecated eggs** in env_cuda (filterpy, basicsr, etc.)

---

## 💡 KEY COMMANDS REFERENCE

### Start ComfyUI
```powershell
cd C:\AI_Projects\ComfyUI
.\venv\Scripts\Activate.ps1
python main.py
```

### Test PyTorch (venv)
```powershell
.\venv\Scripts\Activate.ps1
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

### Test PyTorch (env_cuda)
```powershell
conda activate env_cuda
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

### Rebuild mmcv (if needed)
```powershell
cd C:\Users\Admin\AppData\Local\Temp\mmcv_build
.\C:\AI_Projects\ComfyUI\venv\Scripts\Activate.ps1
pip install -e . -v --no-build-isolation
```

---

## 📝 SESSION LOG

| Date | Action | Result |
|------|--------|--------|
| 2026-01-16 | Rebuilt mmcv for PyTorch 2.5.1 | ✅ Success |
| 2026-01-16 | Rebuilt xtcocotools | ✅ Success |
| 2026-01-16 | Patched whisper CPU loading | ✅ Success |
| 2026-01-16 | MuseTalk loads in ComfyUI | ✅ 7.1s → 9.7s |
| 2026-01-16 | Pushed to GitHub | ✅ Commit a567a5b9 |
| 2026-01-21 | Fixed env_cuda PyTorch | ✅ 2.3.1+cu121 |
| 2026-01-21 | Updated task.md | ✅ This file |

---

## 📦 PACKAGE SNAPSHOTS (For Rollback)

Exact package versions saved for reproducibility:
- `.agent/venv_packages_2026-01-21.txt` - ComfyUI venv (Python 3.11.9)
- `.agent/env_cuda_packages_2026-01-21.txt` - env_cuda (Python 3.12)

**To restore venv if broken:**
```powershell
cd C:\AI_Projects\ComfyUI
python -m venv venv_backup  # Create fresh venv
.\venv_backup\Scripts\Activate.ps1
pip install -r .agent\venv_packages_2026-01-21.txt
```

---

## 🚨 TROUBLESHOOTING GUIDE

### Problem: MuseTalk fails to import
**Symptom:** `ImportError: DLL load failed while importing _ext`
**Cause:** mmcv compiled for wrong PyTorch version
**Fix:**
```powershell
cd C:\Users\Admin\AppData\Local\Temp\mmcv_build
.\C:\AI_Projects\ComfyUI\venv\Scripts\Activate.ps1
pip uninstall mmcv -y
pip install -e . -v --no-build-isolation
```

### Problem: whisper GPU error on startup
**Symptom:** CUDA error during MuseTalk import
**Cause:** RTX 5090 sm_120 kernels not in PyTorch
**Fix:** Already patched in `musetalk/whisper/whisper/__init__.py` - check `device = "cpu"`

### Problem: NumPy ABI mismatch
**Symptom:** `numpy.dtype size changed, may indicate binary incompatibility`
**Fix:**
```powershell
pip install git+https://github.com/jin-s13/xtcocoapi.git --force-reinstall
```

### Problem: PyTorch version mismatch in env_cuda
**Symptom:** `OSError: [WinError 127] c10_cuda.dll`
**Fix:**
```powershell
conda activate env_cuda
pip uninstall torch torchvision torchaudio -y
pip install torch==2.3.1 torchvision==0.18.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu121
```

### Problem: ComfyUI won't start
**Symptom:** Python errors on `python main.py`
**Debug:**
```powershell
.\venv\Scripts\Activate.ps1
python -c "import torch; print(torch.__version__)"
python -c "from mmcv.ops import MultiScaleDeformableAttention; print('mmcv OK')"
python -c "from musetalk.utils.preprocessing import get_landmark_and_bbox; print('MuseTalk OK')"
```

---

## ⚠️ THINGS THAT WILL BREAK (Avoid These)

1. **DO NOT upgrade PyTorch** without rebuilding mmcv
2. **DO NOT mix pip install sources** (PyPI vs pytorch.org wheel URLs)
3. **DO NOT install nightly PyTorch** in production envs
4. **DO NOT delete** `C:\Users\Admin\AppData\Local\Temp\mmcv_build` - needed for rebuilds

---

## 🔗 EXTERNAL DEPENDENCIES

| Dependency | Source | Notes |
|------------|--------|-------|
| mmcv | Local build | `C:\Users\Admin\AppData\Local\Temp\mmcv_build` |
| xtcocotools | GitHub | `pip install git+https://github.com/jin-s13/xtcocoapi.git` |
| PyTorch cu124 | pytorch.org | `--index-url https://download.pytorch.org/whl/cu124` |
| PyTorch cu121 | pytorch.org | `--index-url https://download.pytorch.org/whl/cu121` |

---

**END OF STATE SNAPSHOT - Ready to resume from here**
