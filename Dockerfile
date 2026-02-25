FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
 && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -U pip setuptools wheel

RUN python -m pip install --index-url https://download.pytorch.org/whl/cpu \
    torch torchvision torchaudio

# 从 ComfyUI 仓库直接下载 requirements.txt 安装依赖
# 构建时无需完整 clone ComfyUI，运行时通过 volume 挂载
RUN curl -fsSL https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/requirements.txt \
    -o /tmp/requirements.txt \
 && python -m pip install -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

RUN python -m pip install -U "numpy==1.26.4" "scipy==1.11.4"

RUN python -m pip install requests pillow

EXPOSE 8188

WORKDIR /app/ComfyUI

CMD ["python", "main.py", "--cpu", "--listen", "0.0.0.0", "--port", "8188"]
