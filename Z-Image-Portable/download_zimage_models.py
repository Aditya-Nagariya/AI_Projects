"""Download Z-Image Turbo models for ComfyUI from Comfy-Org repo."""
import os
import sys

# Enable high-performance Xet downloads
os.environ["HF_XET_HIGH_PERFORMANCE"] = "1"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

from huggingface_hub import hf_hub_download

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

downloads = [
    {
        "repo": "Comfy-Org/z_image_turbo",
        "filename": "split_files/diffusion_models/z_image_turbo_bf16.safetensors",
        "dest_dir": os.path.join(MODELS_DIR, "diffusion_models"),
        "dest_name": "z_image_turbo_bf16.safetensors",
    },
    {
        "repo": "Comfy-Org/z_image_turbo",
        "filename": "split_files/text_encoders/qwen_3_4b.safetensors",
        "dest_dir": os.path.join(MODELS_DIR, "text_encoders"),
        "dest_name": "qwen_3_4b.safetensors",
    },
    {
        "repo": "Comfy-Org/z_image_turbo",
        "filename": "split_files/vae/ae.safetensors",
        "dest_dir": os.path.join(MODELS_DIR, "vae"),
        "dest_name": "ae.safetensors",
    },
]

for dl in downloads:
    dest_path = os.path.join(dl["dest_dir"], dl["dest_name"])
    if os.path.isfile(dest_path):
        size_gb = os.path.getsize(dest_path) / (1024**3)
        print(f"[SKIP] {dl['dest_name']} already exists ({size_gb:.2f} GB)")
        continue

    print(f"[DOWNLOADING] {dl['dest_name']} -> {dl['dest_dir']}")
    try:
        downloaded = hf_hub_download(
            repo_id=dl["repo"],
            filename=dl["filename"],
            local_dir=MODELS_DIR,
        )
        # hf_hub_download saves to models/split_files/..., move to final location
        if os.path.isfile(downloaded) and downloaded != dest_path:
            os.makedirs(dl["dest_dir"], exist_ok=True)
            if not os.path.isfile(dest_path):
                import shutil
                shutil.move(downloaded, dest_path)
                print(f"[MOVED] -> {dest_path}")
            else:
                print(f"[OK] Already at {dest_path}")
        else:
            print(f"[OK] {downloaded}")
    except Exception as e:
        print(f"[ERROR] {dl['dest_name']}: {e}")
        sys.exit(1)

print("\n[DONE] All models ready!")
