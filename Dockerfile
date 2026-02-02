FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install torch with CUDA 12.4 support (adjust as needed for HF Space hardware)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create non-root user for security (and HF compatibility)
RUN useradd -m -u 1000 user
RUN chown -R user:user /app
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Expose the HF Space port
EXPOSE 7860

# Command to run ComfyUI on port 7860 and listen on all interfaces
CMD ["python", "main.py", "--listen", "0.0.0.0", "--port", "7860"]
