"""Download Z-Image Turbo models via direct HTTP (bypassing broken Xet storage)."""
import os
import sys
import requests
from tqdm import tqdm

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

# Direct resolve URLs bypass Xet and use plain HTTP
BASE_URL = "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main"

downloads = [
    {
        "url": f"{BASE_URL}/split_files/diffusion_models/z_image_turbo_bf16.safetensors",
        "dest": os.path.join(MODELS_DIR, "diffusion_models", "z_image_turbo_bf16.safetensors"),
        "name": "Diffusion Model (z_image_turbo_bf16.safetensors)",
    },
    {
        "url": f"{BASE_URL}/split_files/text_encoders/qwen_3_4b.safetensors",
        "dest": os.path.join(MODELS_DIR, "text_encoders", "qwen_3_4b.safetensors"),
        "name": "Text Encoder (qwen_3_4b.safetensors)",
    },
    {
        "url": f"{BASE_URL}/split_files/vae/ae.safetensors",
        "dest": os.path.join(MODELS_DIR, "vae", "ae.safetensors"),
        "name": "VAE (ae.safetensors)",
    },
]

def download_file(url, dest, name):
    """Download with resume support and progress bar."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    # Check existing partial download
    existing_size = 0
    if os.path.isfile(dest):
        existing_size = os.path.getsize(dest)
    
    # Check total size with HEAD request
    head = requests.head(url, allow_redirects=True, timeout=30)
    total_size = int(head.headers.get("content-length", 0))
    
    if existing_size >= total_size and total_size > 0:
        print(f"  [SKIP] Already complete ({existing_size / 1024**3:.2f} GB)")
        return True
    
    # Resume download
    headers = {}
    if existing_size > 0:
        headers["Range"] = f"bytes={existing_size}-"
        print(f"  Resuming from {existing_size / 1024**3:.2f} GB...")
    
    print(f"  Total size: {total_size / 1024**3:.2f} GB")
    
    response = requests.get(url, headers=headers, stream=True, timeout=60)
    
    if response.status_code == 416:  # Range not satisfiable = already complete
        print(f"  [SKIP] Already complete")
        return True
    
    response.raise_for_status()
    
    mode = "ab" if existing_size > 0 else "wb"
    chunk_size = 1024 * 1024 * 10  # 10MB chunks
    
    with open(dest, mode) as f:
        with tqdm(
            total=total_size,
            initial=existing_size,
            unit="B",
            unit_scale=True,
            desc=f"  {name}",
        ) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
    
    print(f"  [OK] Downloaded to {dest}")
    return True

print("=" * 50)
print("Z-Image Turbo Model Downloader (Direct HTTP)")
print("=" * 50)

for i, dl in enumerate(downloads, 1):
    print(f"\n[{i}/{len(downloads)}] {dl['name']}")
    try:
        download_file(dl["url"], dl["dest"], dl["name"])
    except KeyboardInterrupt:
        print("\n\nDownload interrupted. Run again to resume.")
        sys.exit(1)
    except Exception as e:
        print(f"  [ERROR] {e}")
        sys.exit(1)

print("\n" + "=" * 50)
print("All models downloaded successfully!")
print("=" * 50)
print("\nRun: .\\run_portable.bat")
