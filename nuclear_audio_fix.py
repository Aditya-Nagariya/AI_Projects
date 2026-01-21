import os

# Define paths
base_path = r"custom_nodes\ComfyUI_NTCosyVoice\cosyvoice"
model_file = os.path.join(base_path, "cli", "model.py")
flow_file = os.path.join(base_path, "flow", "flow.py")

def apply_fix():
    print("🚀 Starting Nuclear Audio Fix...")

    # --- FIX 1: MODEL.PY (Disable FP16 & Force CPU Context) ---
    if os.path.exists(model_file):
        print(f"🔧 Fixing {model_file}...")
        with open(model_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        # Ensure nullcontext is available
        if not any("from contextlib import nullcontext" in line for line in lines):
            new_lines.append("from contextlib import nullcontext\n")

        for line in lines:
            # 1. Force NullContext (CPU Mode)
            if "torch.cuda.stream(torch.cuda.Stream(self.device))" in line:
                # Keep indentation, replace assignment
                indent = line.split("self")[0]
                var_name = line.strip().split("=")[0].strip()
                new_lines.append(f"{indent}{var_name} = nullcontext()\n")
                continue

            # 2. Kill .half() calls safely (Replace with 'pass' to preserve indentation)
            if ".half()" in line and not line.strip().startswith("#"):
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.append(f"{indent}pass # Removed FP16 for 5090 compatibility: {line.strip()}\n")
                continue

            new_lines.append(line)

        with open(model_file, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("   ✅ model.py fixed.")
    else:
        print(f"   ❌ Could not find {model_file}")

    # --- FIX 2: FLOW.PY (Fix Data Type for CPU) ---
    if os.path.exists(flow_file):
        print(f"🔧 Fixing {flow_file}...")
        with open(flow_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Force .long() casting for embedding layer
        old_code = "token = self.input_embedding(torch.clamp(token, min=0))"
        new_code = "token = self.input_embedding(torch.clamp(token, min=0).long())"
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            with open(flow_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print("   ✅ flow.py fixed (Added .long() cast).")
        elif ".long())" in content:
             print("   ✅ flow.py already patched.")
        else:
            print("   ⚠️ Could not match pattern in flow.py (Check line ~123 manually)")
    else:
        print(f"   ❌ Could not find {flow_file}")

    print("\n✨ FIX COMPLETE. Restart ComfyUI now.")

if __name__ == "__main__":
    apply_fix()
