import os
import sys
import shutil
import subprocess
from yt_dlp import YoutubeDL
from pydub import AudioSegment

# --- CONFIGURATION ---
TARGET_URL = "https://www.youtube.com/watch?v=OpUGl4gBHAU" 
OUTPUT_BASE = "varun_maya_voice"

def get_executable_path(name):
    """Finds the executable in the VENV or System PATH"""
    venv_path = os.path.join(sys.prefix, 'Scripts', name + '.exe')
    if os.path.exists(venv_path):
        return venv_path
    global_path = shutil.which(name)
    if global_path:
        return global_path
    return None

def check_system_requirements():
    print("🔍 Checking 5090 readiness...")
    
    if not shutil.which("ffmpeg"):
        print("❌ CRITICAL ERROR: FFmpeg not found.")
        sys.exit(1)
        
    exe = get_executable_path("audio-separator")
    if not exe:
        print("❌ CRITICAL ERROR: 'audio-separator' not found.")
        sys.exit(1)
        
    print(f"✅ Found Audio Separator: {exe}")
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
    print(f"\n🚀 IGNITING RTX 5090 for Audio Separation...")
    
    cmd = [
        separator_exe,
        input_wav,
        "--model_filename", "Kim_Vocal_2.onnx",
        "--output_dir", ".",
        "--output_format", "wav",
        "--normalization", "0.9",
        "--use_autocast", # Optimization for 5090/4090 cards
    ]
    
    # We let it run natively. If the nightly build works, this flies.
    subprocess.run(cmd, check=True)
    
    expected_output = f"{os.path.splitext(input_wav)[0]}_(Vocals)_Kim_Vocal_2.wav"
    return expected_output

def trim_audio(file_path, duration_sec=15):
    print(f"\n✂️ Trimming to best {duration_sec} seconds...")
    if not os.path.exists(file_path):
        # Fallback check
        folder = os.path.dirname(file_path) or "."
        candidates = [f for f in os.listdir(folder) if "(Vocals)" in f and f.endswith(".wav")]
        if candidates:
            file_path = os.path.join(folder, candidates[0])
        else:
            raise FileNotFoundError(f"Could not find separated file: {file_path}")

    audio = AudioSegment.from_wav(file_path)
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
    separator_exe = check_system_requirements()

    try:
        if not os.path.exists("temp_raw_audio.wav"):
            raw_audio = download_audio(TARGET_URL, "temp_raw_audio")
        else:
            print("✅ Using existing temp_raw_audio.wav")
            raw_audio = "temp_raw_audio.wav"

        clean_vocab_path = separate_vocals(raw_audio, separator_exe)
        final_file = trim_audio(clean_vocab_path)
        
        print(f"\n🎉 DONE! Upload this file to CosyVoice: {os.path.abspath(final_file)}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")