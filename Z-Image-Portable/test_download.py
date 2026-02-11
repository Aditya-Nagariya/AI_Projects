"""Quick test: can we actually stream bytes from the model URL?"""
import requests
import time

url = "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors"

print("Testing download speed (first 50MB)...")
start = time.time()
total = 0
try:
    resp = requests.get(url, stream=True, timeout=60)
    print(f"Status: {resp.status_code}")
    print(f"Redirect URL: {resp.url[:80]}...")
    for chunk in resp.iter_content(chunk_size=1024*1024):
        total += len(chunk)
        elapsed = time.time() - start
        speed = total / elapsed / 1024 / 1024
        print(f"\r  Downloaded: {total/1024/1024:.1f} MB  Speed: {speed:.1f} MB/s  Time: {elapsed:.0f}s", end="", flush=True)
        if total > 50 * 1024 * 1024:  # Stop after 50MB
            break
    print(f"\n\nTest OK! Average speed: {speed:.1f} MB/s")
    print("Full download would take roughly: {:.0f} minutes".format(11.5*1024 / speed / 60))
except Exception as e:
    print(f"\nError after {total/1024/1024:.1f} MB: {e}")
