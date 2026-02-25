FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/Comfy-Org/ComfyUI.git /app/ComfyUI

WORKDIR /app/ComfyUI

RUN python -m pip install -U pip setuptools wheel

RUN python -m pip install --index-url https://download.pytorch.org/whl/cpu \
    torch torchvision torchaudio

RUN python -m pip install -r requirements.txt

RUN python -m pip install -U "numpy==1.26.4" "scipy==1.11.4"

EXPOSE 8188

VOLUME ["/app/ComfyUI/models", "/app/ComfyUI/output", "/app/ComfyUI/input"]

RUN python -m pip install requests pillow

COPY simple_grok2api.py /app/ComfyUI/custom_nodes/simple_grok2api.py

CMD ["python", "main.py", "--cpu", "--listen", "0.0.0.0", "--port", "8188"]
