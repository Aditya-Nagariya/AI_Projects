import os

target_file = r"custom_nodes\ComfyUI_NTCosyVoice\cosyvoice\cli\cosyvoice.py"

def force_fp32():
    print(f"🔧 Patching {target_file} to disable FP16...")
    
    if not os.path.exists(target_file):
        print("❌ File not found. Check path.")
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Force the init to default to False for fp16
    # We look for the definition line
    new_content = content.replace("fp16=True):", "fp16=False):")
    
    # 2. Hard code the initialization call just in case
    new_content = new_content.replace(
        "self.model = CosyVoiceModel(configs['llm'], configs['flow'], configs['hift'], fp16)",
        "self.model = CosyVoiceModel(configs['llm'], configs['flow'], configs['hift'], False) # Forced FP32"
    )

    if content != new_content:
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ Success: Forced FP32 mode. This prevents the 5090 crash.")
    else:
        print("⚠️ File was already patched or pattern not found.")

if __name__ == "__main__":
    force_fp32()