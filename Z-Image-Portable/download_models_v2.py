"""Download Z-Image Turbo models, bypassing Xet storage issues."""
import os
import sys
import time
import requests
from tqdm import tqdm

MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

downloads = [
    {
        "url": "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors",
        "dest": os.path.join(MODELS_DIR, "diffusion_models", "z_image_turbo_bf16.safetensors"),
        "name": "Diffusion Model (~11.5 GB)",
    },
    {
        "url": "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors",
        "dest": os.path.join(MODELS_DIR, "text_encoders", "qwen_3_4b.safetensors"),
        "name": "Text Encoder (~7.6 GB)",
    },
    {
        "url": "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors",
        "dest": os.path.join(MODELS_DIR, "vae", "ae.safetensors"),
        "name": "VAE (~0.3 GB)",
    },
]

def download_with_retry(url, dest, name, max_retries=10, chunk_mb=8):
    """Download large file with resume support and automatic retry."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".downloading"
    chunk_size = chunk_mb * 1024 * 1024

    # Get total size
    for attempt in range(3):
        try:
            head = requests.head(url, allow_redirects=True, timeout=30)
            total_size = int(head.headers.get("content-length", 0))
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2)

    if total_size == 0:
        print(f"  [ERROR] Could not determine file size")
        return False

    # Check if already complete
    if os.path.isfile(dest):
        existing = os.path.getsize(dest)
        if existing >= total_size:
            print(f"  [SKIP] Already downloaded ({existing/1024**3:.2f} GB)")
            return True

    # Resume from partial download
    downloaded = 0
    if os.path.isfile(tmp):
        downloaded = os.path.getsize(tmp)
        if downloaded >= total_size:
            os.rename(tmp, dest)
            print(f"  [OK] Download complete")
            return True

    print(f"  Total: {total_size/1024**3:.2f} GB")
    if downloaded > 0:
        print(f"  Resuming from: {downloaded/1024**3:.2f} GB ({downloaded*100//total_size}%)")

    retries = 0
    pbar = tqdm(total=total_size, initial=downloaded, unit="B", unit_scale=True, desc=f"  {name}")

    while downloaded < total_size and retries < max_retries:
        try:
            headers = {"Range": f"bytes={downloaded}-"} if downloaded > 0 else {}
            resp = requests.get(url, headers=headers, stream=True, timeout=60)

            if resp.status_code == 416:
                break  # Complete

            resp.raise_for_status()
            mode = "ab" if downloaded > 0 else "wb"

            with open(tmp, mode) as f:
                for chunk in resp.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        pbar.update(len(chunk))

            if downloaded >= total_size:
                break

        except (requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout,
                requests.exceptions.ChunkedEncodingError) as e:
            retries += 1
            wait = min(retries * 5, 30)
            pbar.write(f"\n  Connection lost. Retry {retries}/{max_retries} in {wait}s...")
            time.sleep(wait)
            # Re-check actual file size for resume
            if os.path.isfile(tmp):
                downloaded = os.path.getsize(tmp)

    pbar.close()

    if downloaded >= total_size:
        if os.path.isfile(dest):
            os.remove(dest)
        os.rename(tmp, dest)
        print(f"  [OK] Saved to {dest}")
        return True
    else:
        print(f"  [ERROR] Download incomplete ({downloaded}/{total_size})")
        return False

if __name__ == "__main__":
    print("=" * 55)
    print(" Z-Image Turbo Model Downloader (Direct HTTP + Retry)")
    print("=" * 55)

    for i, dl in enumerate(downloads, 1):
        print(f"\n[{i}/{len(downloads)}] {dl['name']}")
        try:
            ok = download_with_retry(dl["url"], dl["dest"], dl["name"])
            if not ok:
                print("\nFailed. Run again to resume.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n  Interrupted. Run again to resume from where you left off.")
            sys.exit(1)
        except Exception as e:
            print(f"  [ERROR] {e}")
            sys.exit(1)

    print("\n" + "=" * 55)
    print(" All models ready! Run: .\\run_portable.bat")
    print("=" * 55)
