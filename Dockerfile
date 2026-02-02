FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
# ffmpeg: required for video nodes (Wav2Lip, VideoHelperSuite)
# git: required for ComfyUI Manager and git-based nodes
# libgl1, libglib2.0-0: required for opencv (libgl1 replaces deprecated libgl1-mesa-glx)
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Torch with CUDA 12.4 support
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Copy root requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install dependencies for all custom nodes
# This script finds all requirements.txt files in custom_nodes and installs them
RUN for f in custom_nodes/*/requirements.txt; do \
        if [ -f "$f" ]; then \
            echo "Installing requirements for $f"; \
            pip install --no-cache-dir -r "$f"; \
        fi \
    done

# Create non-root user for security (and HF compatibility)
RUN useradd -m -u 1000 user
RUN chown -R user:user /app
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Expose the HF Space port
EXPOSE 7860

# Command to run ComfyUI
# --listen 0.0.0.0 enables access from outside the container
# --port 7860 matches the exposed port
CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "7860"]