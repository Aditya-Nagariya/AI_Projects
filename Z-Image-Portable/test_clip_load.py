"""Quick test of the CLIPLoader to see if qwen_3_4b loads properly."""
import sys
sys.path.insert(0, r"C:\AI_Projects\Z-Image-Portable")

import comfy.options
comfy.options.args_parsing = False

import comfy.sd
import comfy.utils
import folder_paths

clip_path = folder_paths.get_full_path("text_encoders", "qwen_3_4b.safetensors")
print(f"Clip path: {clip_path}")
if clip_path is None:
    print("ERROR: qwen_3_4b.safetensors not found in text_encoders paths!")
    print(f"Search paths: {folder_paths.get_folder_paths('text_encoders')}")
    sys.exit(1)

print("Loading clip data...")
try:
    sd, metadata = comfy.utils.load_torch_file(clip_path, safe_load=True, return_metadata=True)
    print(f"Keys loaded: {len(sd)} keys")
    # Check a few keys for QWEN3 detection
    keys_to_check = [
        "model.layers.0.post_attention_layernorm.weight",
        "model.layers.0.self_attn.q_norm.weight",
    ]
    for k in keys_to_check:
        if k in sd:
            print(f"  Found: {k} shape={sd[k].shape}")
        else:
            print(f"  Missing: {k}")
    
    # Try detecting
    te_model = comfy.sd.detect_te_model(sd)
    print(f"Detected TE model: {te_model}")
    
except Exception as e:
    print(f"ERROR loading: {e}")
    import traceback
    traceback.print_exc()
