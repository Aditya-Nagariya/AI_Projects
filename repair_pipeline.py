import os
import subprocess
import sys
import shutil

def run_command(command, desc):
    print(f"\n🚀 {desc}...")
    try:
        subprocess.check_call(command, shell=True)
        print(f"✅ {desc} Successful.")
    except subprocess.CalledProcessError as e:
        print(f"❌ {desc} Failed. Error: {e}")

def fix_folder_name():
    base_path = os.path.abspath("custom_nodes")
    disabled_path = os.path.join(base_path, "ComfyUI-MuseTalk.disabled")
    active_path = os.path.join(base_path, "ComfyUI-MuseTalk")
    
    if os.path.exists(disabled_path):
        print(f"\n🔄 Re-enabling MuseTalk...")
        try:
            os.rename(disabled_path, active_path)
            print("✅ MuseTalk folder enabled.")
        except Exception as e:
            print(f"❌ Could not rename folder: {e}")
    elif os.path.exists(active_path):
        print("✅ MuseTalk folder is already active.")
    else:
        print("⚠️ MuseTalk folder not found. Make sure you installed it.")

def main():
    print("=== 🛠️ NEURAL TWIN PIPELINE REPAIR TOOL 🛠️ ===")
    
    # 1. Fix Folder Name
    fix_folder_name()

    # 2. Downgrade Numpy (The Critical Fix)
    # MuseTalk/OpenMIM requires numpy 1.x, but environment has 2.x
    print("\n📦 Fixing Numpy Compatibility (Downgrading to 1.x)...")
    run_command(f'"{sys.executable}" -m pip uninstall -y numpy', "Uninstalling incompatible Numpy")
    run_command(f'"{sys.executable}" -m pip install "numpy<2.0"', "Installing Numpy 1.26.x")

    # 3. Reinstall affected binaries to link with new numpy
    print("\n🔄 Re-linking Binary Dependencies...")
    run_command(f'"{sys.executable}" -m pip install --force-reinstall --no-deps xtcocotools', "Reinstalling xtcocotools")
    run_command(f'"{sys.executable}" -m pip install --force-reinstall --no-deps mmcv>=2.0.1', "Reinstalling mmcv")

    print("\n" + "="*50)
    print("✨ REPAIR COMPLETE")
    print("You can now launch ComfyUI.")
    print("Command: python main.py --listen --use-pytorch-cross-attention")
    print("="*50)

if __name__ == "__main__":
    main()
