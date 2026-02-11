import requests
r = requests.head(
    "https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors",
    allow_redirects=True,
    timeout=30,
)
print(f"Status: {r.status_code}")
cl = r.headers.get("content-length", "0")
print(f"Size: {int(cl)/1024**3:.2f} GB")
print(f"URL: {r.url[:100]}")
