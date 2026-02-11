"""Queue the Z-Image workflow via the ComfyUI API."""
import json
import urllib.request

workflow = {
  "1": {
    "class_type": "UNETLoader",
    "inputs": {
      "unet_name": "z_image_turbo_bf16.safetensors",
      "weight_dtype": "default"
    }
  },
  "2": {
    "class_type": "CLIPLoader",
    "inputs": {
      "clip_name": "qwen_3_4b.safetensors",
      "type": "stable_diffusion"
    }
  },
  "3": {
    "class_type": "VAELoader",
    "inputs": {
      "vae_name": "ae.safetensors"
    }
  },
  "4": {
    "class_type": "StylePromptEncoder //ZImagePowerNodes",
    "inputs": {
      "category": "photo",
      "style": "None",
      "text": "A futuristic cyberpunk city with neon lights and flying cars, high detail, 8k",
      "clip": ["2", 0]
    }
  },
  "5": {
    "class_type": "EmptyZImageLatentImage //ZImagePowerNodes",
    "inputs": {
      "landscape": False,
      "ratio": "1:1  (square)",
      "size": "medium (recommended)",
      "batch_size": 1
    }
  },
  "6": {
    "class_type": "ZSamplerTurbo //ZImagePowerNodes",
    "inputs": {
      "model": ["1", 0],
      "positive": ["4", 0],
      "latent_input": ["5", 0],
      "seed": 42,
      "steps": 9,
      "denoise": 1
    }
  },
  "7": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": ["6", 0],
      "vae": ["3", 0]
    }
  },
  "8": {
    "class_type": "SaveImage",
    "inputs": {
      "images": ["7", 0],
      "filename_prefix": "Z-Image-Output"
    }
  }
}

payload = json.dumps({"prompt": workflow}).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8189/prompt",
    data=payload,
    headers={"Content-Type": "application/json"},
)

try:
    resp = urllib.request.urlopen(req, timeout=10)
    print(f"Queued! Response: {resp.read().decode()}")
except Exception as e:
    print(f"Error: {e}")
