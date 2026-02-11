"""Full test of CLIPLoader with z_image text encoder."""
import sys, os
sys.path.insert(0, r"C:\AI_Projects\Z-Image-Portable")
os.chdir(r"C:\AI_Projects\Z-Image-Portable")

import comfy.options
comfy.options.args_parsing = False

import comfy.sd
import folder_paths

print("Loading CLIP with lumina2 type (as workflow does)...")
clip_path = folder_paths.get_full_path("text_encoders", "qwen_3_4b.safetensors")
print(f"Path: {clip_path}")

try:
    clip = comfy.sd.load_clip(
        ckpt_paths=[clip_path],
        embedding_directory=folder_paths.get_folder_paths("embeddings"),
        clip_type=comfy.sd.CLIPType.LUMINA2,
        model_options={}
    )
    print(f"SUCCESS! clip = {clip}")
    print(f"clip type: {type(clip)}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
