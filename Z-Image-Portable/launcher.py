import os, sys, subprocess
os.chdir(r"C:\AI_Projects\Z-Image-Portable")
sys.exit(subprocess.call([
    r"C:\AI_Projects\Z-Image-Portable\venv\Scripts\python.exe",
    "main.py", "--listen", "127.0.0.1", "--port", "8189"
]))
