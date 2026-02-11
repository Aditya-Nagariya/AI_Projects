# PROJECT REBOOT: Full-Performance Avatar Synthesis
## Last Updated: 2026-01-29 16:45
## Status: ✅ InfiniteTalk FP8 Downloaded → 🎉 MultiTalk Audio Proj Fix Applied

---

## 🎯 MISSION

Replace MuseTalk lip-sync with a **generative simulation stack** producing broadcast-quality full-body avatar performances. The system doesn't warp pixels—it *hallucinates reality* frame-by-frame.

### Stack Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                    PROJECT REBOOT PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│  Layer 4: INFINITALK (MultiTalk)     ← Lip Sync (Sparse-Frame)  │
│  Layer 3: FANTASY PORTRAIT           ← Identity Lock (DiT)      │
│  Layer 2: PUSAV2 / Motion Driver     ← Kinetic Choreography     │
│  Layer 1: WAN2.1 14B                 ← Physics Engine (Core)    │
├─────────────────────────────────────────────────────────────────┤
│  Hardware: RTX 5090 32GB VRAM        ← Zero-Offload Strategy    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 VRAM BUDGET (RTX 5090 32GB)

| Component | Model | Est. VRAM | Precision | Status |
|-----------|-------|-----------|-----------|--------|
| **Motion Engine** | Wan2.1 I2V 14B | ~14.5 GB | FP8 Scaled | ⚠️ Need FP8 |
| **Text Encoder** | UMT5-XXL | ~4.8 GB | BF16 | ✅ Have (10.6GB) |
| **CLIP Vision** | ViT-H | ~1.2 GB | FP16 | ✅ Have |
| **Identity Control** | Fantasy Portrait | ~2.5 GB | BF16 | ⚠️ Need model |
| **Lip Sync** | Infinitalk | ~1.5 GB | FP16 | ⚠️ Need model |
| **ControlNet** | Wan Fun Control | ~2.0 GB | FP16 | ⚠️ Need model |
| **Wav2Vec2** | TencentGameMate | ~0.4 GB | FP16 | ⚠️ Need model |
| **VAE** | Wan2.1 VAE | ~0.5 GB | FP32 | ✅ Have |
| **Latent Buffer** | 720p/81 frames | ~4.0 GB | FP32 | Runtime |
| **Overhead** | PyTorch context | ~2.0 GB | N/A | Runtime |
| **TOTAL** | | **~31.4 GB** | | **97% util** |

---

## ✅ INFRASTRUCTURE AUDIT (2026-01-28)

### Node Packages Found
| Component | Path | Status |
|-----------|------|--------|
| **WanVideoWrapper** | `custom_nodes/ComfyUI-WanVideoWrapper/` | ✅ Installed |
| ├─ Wan2.1 Loader | `nodes_model_loading.py` | ✅ Ready |
| ├─ Wan2.1 Sampler | `nodes_sampler.py` | ✅ Ready |
| ├─ Fantasy Portrait | `fantasyportrait/` | ✅ Ready |
| ├─ MultiTalk/Infinitalk | `multitalk/` | ✅ Ready |
| └─ ControlNet | `controlnet/` | ✅ Ready |

### Model Inventory (Verified from Example Workflows)
| Model | Expected File | Expected Path | Status |
|-------|---------------|---------------|--------|
| Wan2.1 14B FP8 | `Wan2_1-I2V-14B-720p_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models/WanVideo/fp8_scaled_kj/I2V/` | ✅ Present |
| Fantasy Portrait | `Wan2_1_FantasyPortrait_fp16.safetensors` | `diffusion_models/WanVideo/FantasyPortrait/` | ✅ Present |
| Infinitalk FP8 | `Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors` | `diffusion_models/WanVideo/fp8_scaled_kj/InfiniteTalk/` | ✅ Downloaded |
| Infinitalk GGUF | `Wan2_1-InfiniteTalk_Single_Q8.gguf` | `diffusion_models/WanVideo/InfiniteTalk/` | ✅ Present (not compatible with FP8 main) |
| Wav2Vec2 | `wav2vec2-chinese-base_fp16.safetensors` | `wav2vec2/` | ✅ Present |
| Pusa LoRA | `Wan21_PusaV1_LoRA_14B_rank512_bf16.safetensors` | `diffusion_models/WanVideo/Pusa/` | ✅ Present |
| UMT5-XXL | `umt5-xxl-enc-bf16.safetensors` | `text_encoders/` | ✅ Present |
| CLIP-ViT-H | `clip_vision_h.safetensors` | `clip_vision/` | ✅ Present |
| Wan2.1 VAE | `Wan2_1_VAE_bf16.safetensors` | `vae/` | ✅ Present |

---

## 📥 MODEL ACQUISITION PLAN (VERIFIED FROM EXAMPLE WORKFLOWS)

### Phase 1A: Core Diffusion Model (FP8)
```powershell
# Wan2.1 I2V 14B FP8 (~14GB) - REQUIRED
# Source: Kijai/WanVideo_comfy_fp8_scaled
New-Item -ItemType Directory -Path "C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo\fp8_scaled_kj\I2V" -Force
huggingface-cli download Kijai/WanVideo_comfy_fp8_scaled I2V/Wan2_1-I2V-14B-720p_fp8_e4m3fn_scaled_KJ.safetensors --local-dir C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo\fp8_scaled_kj
```

### Phase 1B: Fantasy Portrait Model
```powershell
# Fantasy Portrait FP16 (~2.5GB) - REQUIRED
New-Item -ItemType Directory -Path "C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo\FantasyPortrait" -Force
huggingface-cli download Kijai/WanVideo_comfy FantasyPortrait/Wan2_1_FantasyPortrait_fp16.safetensors --local-dir C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo
```

### Phase 1C: Infinitalk Model
```powershell
# Infinitalk GGUF Q8 (~1.5GB) - REQUIRED
# Note: Can use FP8 or GGUF, GGUF more memory efficient
New-Item -ItemType Directory -Path "C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo\InfiniteTalk" -Force
huggingface-cli download Kijai/WanVideo_comfy_GGUF InfiniteTalk/Wan2_1-InfiniteTalk_Single_Q8.gguf --local-dir C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo
```

### Phase 1D: Wav2Vec2 (Audio Encoder)
```powershell
# Wav2Vec2 Chinese Base FP16 (~0.4GB) - REQUIRED
New-Item -ItemType Directory -Path "C:\AI_Projects\ComfyUI\models\wav2vec2" -Force
huggingface-cli download Kijai/wav2vec2_safetensors wav2vec2-chinese-base_fp16.safetensors --local-dir C:\AI_Projects\ComfyUI\models\wav2vec2
```

### Phase 1E: Pusa LoRA (Motion Control)
```powershell
# PusaV1 LoRA for motion direction (~1.5GB) - OPTIONAL
New-Item -ItemType Directory -Path "C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo\Pusa" -Force
huggingface-cli download Kijai/WanVideo_comfy Pusa/Wan21_PusaV1_LoRA_14B_rank512_bf16.safetensors --local-dir C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo
```

### Phase 1F: Lightx2v (Speed Optimization) - OPTIONAL
```powershell
# Lightx2v distillation LoRA for faster inference
New-Item -ItemType Directory -Path "C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo\Lightx2v" -Force
huggingface-cli download Kijai/WanVideo_comfy Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors --local-dir C:\AI_Projects\ComfyUI\models\diffusion_models\WanVideo
```

### Phase 1G: VAE (If Missing)
```powershell
# Wan2.1 VAE BF16 (~470MB) - Check if already present
huggingface-cli download Kijai/WanVideo_comfy wanvideo/Wan2_1_VAE_bf16.safetensors --local-dir C:\AI_Projects\ComfyUI\models\vae
```

---

## 🔧 IMPLEMENTATION PHASES

### Phase 0: Infrastructure Audit ✅ COMPLETE
- [x] Inventory node packages
- [x] Inventory model files
- [x] Map VRAM budget
- [x] Identify missing components

### Phase 1: Model Acquisition ✅ COMPLETE
- [x] Download Wan2.1 14B FP8
- [x] Download Fantasy Portrait model
- [x] Download Infinitalk FP8 model
- [x] Download Wav2Vec2
- [x] Download Pusa LoRA
- [x] Verify all models load

### Phase 2: Basic Wan2.1 Pipeline ✅ COMPLETE
- [x] Create minimal I2V workflow
- [x] Test 720p @ 81 frames
- [x] Verify VRAM stays under 32GB
- [x] Benchmark generation speed

### Phase 3: TTS Voice Cloning ✅ COMPLETE
- [x] ChatterBox TTS integration
- [x] UnifiedTTSTextNode working
- [x] Voice cloning from reference audio

### Phase 4: Identity Lock (Fantasy Portrait) ✅ COMPLETE
- [x] Wire face detector
- [x] Configure masked attention
- [x] Test identity preservation
- [x] FantasyPortraitFaceDetector working (81 frames)

### Phase 5: Lip Sync (InfiniteTalk/MultiTalk) ⬅️ CURRENT
- [x] Load Wav2Vec2
- [x] MultiTalkWav2VecEmbeds processing audio
- [x] Fixed 'multitalk_audio_proj' missing error
- [x] Added MultiTalkModelLoader to workflow
- [ ] Test full audio-driven lip sync generation
- [ ] Tune audio_scale/audio_cfg_scale

### Phase 6: Full Integration
- [ ] Create master workflow
- [ ] Test end-to-end
- [ ] Quality tuning

---

## 💡 KEY COMMANDS

### Start ComfyUI (High VRAM)
```powershell
cd C:\AI_Projects\ComfyUI
.\venv\Scripts\Activate.ps1
python main.py --highvram --preview-method auto
```

### HuggingFace Download
```powershell
pip install huggingface_hub
huggingface-cli download <repo> <file> --local-dir <path>
```

### Monitor VRAM
```powershell
nvidia-smi --query-gpu=memory.used,memory.total --format=csv -l 2
```

---

## ⚠️ CRITICAL PARAMETERS

### Wan2.1 14B Sampling
```yaml
Resolution: 1280x720 or 720x1280
Frames: 81-120 (5-7 seconds)
Steps: 35-50
CFG: 6.5
Sampler: euler / dpmpp_2m
Scheduler: simple / karras
```

### Fantasy Portrait
```yaml
Identity_Weight: 1.0
Expression_Weight: 0.8
Mask: Head bounding box only
```

### Infinitalk
```yaml
Audio_CFG: 3.5-4.5
Sliding_Window: 24 frames, 4 overlap
Crop: Jaw + upper neck
```

### ControlNet Decay
```yaml
Steps 0-20%: 1.0 (layout)
Steps 20-50%: 0.7
Steps 50-100%: 0.4 (texture)
```

---

## 📁 KEY PATHS

| Purpose | Path |
|---------|------|
| Task State | `.agent/task.md` |
| WanWrapper | `custom_nodes/ComfyUI-WanVideoWrapper/` |
| Diffusion Models | `models/diffusion_models/` |
| ControlNets | `models/controlnet/` |
| Text Encoders | `models/text_encoders/` |
| CLIP Vision | `models/clip_vision/` |
| Wav2Vec2 | `models/wav2vec2/` (TO CREATE) |
| Example Workflows | `custom_nodes/ComfyUI-WanVideoWrapper/example_workflows/` |

---

## 🚨 CONSTRAINTS

1. **RTX 5090 sm_120**: PTX JIT only - ~10-15% slower than native
2. **FP8 Required**: BF16 14B (61GB) won't fit - must use FP8 (~14GB)
3. **PyTorch 2.5.1**: Frozen until cu130 for native Blackwell
4. **No --lowvram**: Defeats zero-offload strategy

---

## 📝 SESSION LOG

### 2026-01-29 16:45 - MultiTalk Audio Proj Fix ✅

**Error Encountered:**
```
AttributeError: 'WanModel' object has no attribute 'multitalk_audio_proj'
```
- Node: `WanVideoSampler` (Node ID 50)
- Root Cause: MultiTalk audio embeddings passed to sampler but WanModel not patched

**Root Cause Analysis:**
- Workflow used `MultiTalkWav2VecEmbeds` to create lip-sync embeddings ✅
- Embeddings passed to `WanVideoSampler` ✅
- BUT `WanVideoModelLoader` was missing `multitalk_model` input ❌
- The `multitalk_audio_proj` layer only gets patched when `MultiTalkModelLoader` connected

**Solution:**
1. Downloaded InfiniteTalk FP8 models (compatible with FP8 main model):
   ```powershell
   hf download Kijai/WanVideo_comfy_fp8_scaled --include "InfiniteTalk/*" --local-dir "models/diffusion_models/WanVideo/fp8_scaled_kj"
   ```
   - `Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors` (2.71GB)
   - `Wan2_1-InfiniteTalk-Multi_fp8_e4m3fn_scaled_KJ.safetensors` (2.71GB)

2. Updated `varun_mayya_avatar_v7.json`:
   - Added `MultiTalkModelLoader` (node 61)
   - Loads: `WanVideo\\fp8_scaled_kj\\InfiniteTalk\\Wan2_1-InfiniteTalk-Single_fp8_e4m3fn_scaled_KJ.safetensors`
   - Connected to `WanVideoModelLoader` via `multitalk_model` input (link 71)

**Key Learning:**
- GGUF InfiniteTalk (Q8) **cannot** be mixed with FP8 Scaled main model
- Must use FP8 InfiniteTalk with FP8 main model, or GGUF with GGUF
- `MultiTalkModelLoader` outputs `MULTITALKMODEL` → patches WanModel with audio projection

**Workflow Pipeline (varun_mayya_avatar_v7.json):**
```
Stage 1: Voice Cloning
  LoadAudio → ChatterBoxEngine → UnifiedTTSTextNode → AUDIO

Stage 2: Motion Extraction  
  VHS_LoadVideo → FantasyPortraitFaceDetector → PORTRAIT_EMBEDS

Stage 3: Lip Sync
  Wav2VecModelLoader → MultiTalkWav2VecEmbeds → MULTITALK_EMBEDS

Stage 4: Video Synthesis
  MultiTalkModelLoader ─────┐
                            ↓ (multitalk_model)
  WanVideoModelLoader ──────→ WanVideoSampler
  LoadWanVideoT5TextEncoder ─↗ (text_embeds)
  WanVideoImageToVideoEncode ↗ (image_embeds via FantasyPortraitEmbedsToWan)
```

**Files Modified:**
- `varun_mayya_avatar_v7.json` - Added MultiTalkModelLoader + connection

---

### 2026-01-29 15:57 - WanVideoImageToVideoEncode Fix

**Error:** `WanVideoImageToVideoEncode.process() got an unexpected keyword argument 'image'`
- Root Cause: Input should be `start_image` not `image`
- Fixed node 46 inputs and removed invalid num_frames link

---

### 2026-01-29 - TTS UnifiedTTSTextNode Fix

**Error:** Widget validation errors - values in wrong positions
- Root Cause: Hidden `control_after_generate` widget auto-added after seed
- Fix: Added `"fixed"` value after seed in widgets_values array
- TTS now generates audio successfully (3.375s audio, ChatterBox)

---

### 2026-01-29 - LTX-2 Gemma Tokenizer Fix

**Issue Encountered:**
```
FileNotFoundError: No files matching pattern 'tokenizer.model' found under C:\AI_Projects\ComfyUI\models
```
- Node: `LTXVGemmaCLIPModelLoader` (Node ID 33)
- Root Cause: Had `gemma_3_12B_it_fp4_mixed.safetensors` but missing tokenizer files

**Resolution Steps:**
1. ❌ Initial download attempts failed - 403 Forbidden (gated repo)
2. ✅ HuggingFace login: `huggingface-cli login` → Token "ComfyUi" saved
3. ✅ Accepted Google's Gemma license terms on website
4. ✅ Download initiated successfully

**Download Command:**
```powershell
.\venv\Scripts\Activate.ps1; hf download google/gemma-3-12b-it-qat-q4_0-unquantized --local-dir C:\AI_Projects\ComfyUI\models\text_encoders\gemma-3-12b-it-qat-q4_0-unquantized
```

**Download Status (as of session):**
- ✅ `tokenizer.model` (4.69MB) - **CRITICAL FILE DOWNLOADED**
- ✅ `tokenizer.json` (33.4MB)
- ✅ `config.json`, `chat_template.json`, `preprocessor_config.json`
- ⏳ `model-00001-of-00005.safetensors` (~5GB)
- ⏳ `model-00002-of-00005.safetensors` (~5GB)
- ⏳ `model-00003-of-00005.safetensors` (~5GB)
- ⏳ `model-00004-of-00005.safetensors` (~5GB)
- ⏳ `model-00005-of-00005.safetensors` (~4.6GB)
- **Total:** ~25GB, ETA ~30-50 minutes

**Next Steps:**
1. Wait for Gemma download to complete
2. Restart ComfyUI: `python main.py --highvram`
3. Test LTX-2 workflow to confirm error resolved
4. Continue Project Reboot model downloads

**Workflow Created:** `neural_twin_v42_infinitetalk.json`
- Uses Wan2.1 I2V 14B FP8 + InfiniteTalk for lip-sync
- Pipeline: Image → CLIP Vision → Wav2Vec Audio → WanVideo Sampler → Video
- Models verified present:
  - ✅ `Wan2_1-I2V-14B-720p_fp8_e4m3fn_scaled_KJ.safetensors`
  - ✅ `Wan2_1-InfiniteTalk_Single_Q8.gguf`
  - ✅ `wav2vec2-chinese-base_fp16.safetensors`
  - ✅ `clip_vision_h.safetensors`
  - ✅ `umt5-xxl-enc-bf16.safetensors`
  - ✅ `Wan2_1_VAE_bf16.safetensors`

**LTX-2 Gemma Error (12:30):**
```
RuntimeError: mat1 and mat2 shapes cannot be multiplied (1024x62208 and 188160x3840)
```
- **Root Cause:** `LTXVGemmaCLIPModelLoader` pointing to wrong model
- **Fix:** Change `gemma_path` to `gemma-3-12b-it-qat-q4_0-unquantized\model-00001-of-00005.safetensors`
- The node was loading CLIP-ViT-H instead of Gemma because the selected file didn't have `tokenizer.model` nearby

**LTX-2 OOM Error (12:30):**
```
torch.OutOfMemoryError: Allocation on device
```
- **Root Cause:** LTX-2 19B (20.5GB) + Gemma 12B (10-12GB) > 32GB VRAM
- **Fix:** Restart ComfyUI WITHOUT `--highvram` flag: `python main.py`
- This allows model offloading to CPU RAM when VRAM is full
- Alternative: Use T5 encoder instead of Gemma (~5GB), or use LTX-2B instead of 19B

**LTX-2 Node Error (13:00):**
```
TypeError: LTXVImgToVideo.execute() got an unexpected keyword argument 'model'
```
- **Root Cause:** Wrong workflow design - core `LTXVImgToVideo` doesn't accept MODEL input
- **Fix:** Use the official LTX-2 workflow from ComfyUI-LTXVideo:
  - Copied `LTX-2_I2V_Full_wLora.json` to `LTX2_I2V_official.json`
  - Load this in ComfyUI, it uses the correct specialized sampler subgraph

---

### 2026-01-28 - Project Reboot Initialization

**Actions Completed:**
- ✅ Full infrastructure audit of ComfyUI workspace
- ✅ Discovered ComfyUI-WanVideoWrapper already contains Fantasy Portrait & MultiTalk nodes
- ✅ Identified all required models from example workflows
- ✅ Created `download_reboot_models.ps1` script for automated downloads
- ✅ Rewrote `.agent/task.md` with complete Project Reboot architecture
- ✅ Mapped VRAM budget (31.4GB / 32GB = 97% utilization)

**Models Identified (from Example Workflows):**
| Model | Source | Size |
|-------|--------|------|
| Wan2.1 I2V 14B FP8 | `Kijai/WanVideo_comfy_fp8_scaled` | ~14GB |
| Fantasy Portrait FP16 | `Kijai/WanVideo_comfy` | ~2.5GB |
| Infinitalk GGUF Q8 | `Kijai/WanVideo_comfy_GGUF` | ~1.5GB |
| Wav2Vec2 FP16 | `Kijai/wav2vec2_safetensors` | ~0.4GB |
| Pusa LoRA | `Kijai/WanVideo_comfy` | ~1.5GB |

**Download Script Created:** `download_reboot_models.ps1`

---

## 📜 ARCHIVED: MuseTalk Pipeline

Previous Neural Twin pipeline preserved:
- Workflows: `neural_twin_v28` → `v41_complete.json`
- MuseTalk: `custom_nodes/ComfyUI-MuseTalk/`
- mmcv build: `C:\Users\Admin\AppData\Local\Temp\mmcv_build`

---

## 📝 SESSION LOG

| Date | Action | Result |
|------|--------|--------|
| 2026-01-28 | Project Reboot initiated | 🚀 |
| 2026-01-28 | Infrastructure audit | ✅ Nodes ready |
| 2026-01-28 | Model inventory | ⚠️ 5 models missing |

---

**NEXT ACTION**: Load `varun_mayya_avatar_v7.json` in ComfyUI and test full avatar generation pipeline with audio lip-sync.

**Active Workflow:** `varun_mayya_avatar_v7.json`
- ✅ ChatterBox TTS voice cloning
- ✅ FantasyPortrait face detection (81 frames)
- ✅ Wav2Vec2 audio embeddings
- ✅ MultiTalkModelLoader patches WanModel
- 🧪 Ready for full generation test

**END OF PROJECT REBOOT STATE**
