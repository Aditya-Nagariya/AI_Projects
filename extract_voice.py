import os
import sys
import shutil
import subprocess
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# --- CONFIGURATION ---
TARGET_URL = "https://www.youtube.com/watch?v=OpUGl4gBHAU" # The URL you provided
OUTPUT_BASE = "varun_maya_voice"

def get_executable_path(name):
    """Finds the executable in the VENV or System PATH"""
    # 1. Check inside the current Python Environment (venv/Scripts)
    venv_path = os.path.join(sys.prefix, 'Scripts', name + '.exe')
    if os.path.exists(venv_path):
        return venv_path
    
    # 2. Check global path
    global_path = shutil.which(name)
    if global_path:
        return global_path
        
    return None

def check_system_requirements():
    print("🔍 Checking system requirements...")
    
    # Check FFmpeg
    if not shutil.which("ffmpeg"):
        print("❌ CRITICAL ERROR: FFmpeg not found in system PATH.")
        print("   Please run: winget install \"FFmpeg (Essentials Build)\" in a new terminal.")
        sys.exit(1)
        
    # Check Audio Separator
    exe = get_executable_path("audio-separator")
    if not exe:
        print("❌ CRITICAL ERROR: 'audio-separator' not found.")
        print("   Please run: pip install audio-separator")
        sys.exit(1)
        
    print(f"✅ Found Audio Separator: {exe}")
    print("✅ Found FFmpeg")
    return exe

def download_audio(url, output_base):
    print(f"\n⬇️ Downloading audio from: {url}")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_base}.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return f"{output_base}.wav"

def separate_vocals(input_wav, separator_exe):
    print(f"\n🧼 Cleaning audio (AI Vocal Isolation - CPU Mode)...")
    print("   (This may take a few minutes on CPU...)")
    
    # We use the full path to the executable we found earlier
    cmd = [
        separator_exe,
        input_wav,
        "--model_filename", "Kim_Vocal_2.onnx",
        "--output_dir", ".",
        "--output_format", "wav",
        "--normalization", "0.9"
    ]
    print(f"   Executing: {' '.join(cmd)}")
    
    # Force CPU mode by hiding GPU from CUDA/PyTorch/ONNX (fixes RTX 5090 compatibility)
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = "-1"  # Hide all GPUs
    env["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    env["ONNXRUNTIME_EXECUTION_PROVIDERS"] = "CPUExecutionProvider"
    
    subprocess.run(cmd, check=True, env=env)
    
    # Primary expected output name
    expected_output = f"{os.path.splitext(input_wav)[0]}_(Vocals)_Kim_Vocal_2.wav"
    
    # Fallback: check for any vocal file if naming convention varies
    if not os.path.exists(expected_output):
        import glob
        vocal_files = glob.glob("*Vocals*.wav") + glob.glob("*vocals*.wav")
        if vocal_files:
            expected_output = vocal_files[0]
            print(f"   Found vocal file: {expected_output}")
    
    return expected_output

def trim_audio(file_path, duration_sec=15):
    print(f"\n✂️ Trimming to best {duration_sec} seconds...")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Could not find separated file: {file_path}")

    audio = AudioSegment.from_wav(file_path)
    
    # Start 30s in to avoid intro music
    start_time = 30 * 1000 
    end_time = start_time + (duration_sec * 1000)
    
    if len(audio) < end_time:
        start_time = 0
        end_time = min(len(audio), duration_sec * 1000)
        
    chunk = audio[start_time:end_time]
    
    final_name = "final_voice_clone.wav"
    chunk.export(final_name, format="wav")
    print(f"✅ Voice Clone Ready: {final_name}")
    return final_name

if __name__ == "__main__":
    # 1. Verification
    separator_exe = check_system_requirements()

    # 2. Pipeline
    try:
        raw_audio = download_audio(TARGET_URL, "temp_raw_audio")
        clean_vocab_path = separate_vocals(raw_audio, separator_exe)
        final_file = trim_audio(clean_vocab_path)
        
        # Cleanup
        if os.path.exists("temp_raw_audio.wav"): os.remove("temp_raw_audio.wav")
        
        print(f"\n🎉 DONE! Upload this file to CosyVoice: {os.path.abspath(final_file)}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")