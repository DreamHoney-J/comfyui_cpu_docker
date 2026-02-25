# comfyui_cpu_docker

使用 Docker Compose 以 CPU 模式部署 ComfyUI。提供两种部署方式：Fork 自行构建镜像，或直接使用本项目已构建的镜像。

## 环境要求

- Docker 及 Docker Compose（推荐 Docker Desktop 或 Linux 原生安装）
- 无需 NVIDIA 显卡，纯 CPU 运行

---

## 方式一：Fork 本项目，自行构建镜像

适合需要自定义 Dockerfile、修改构建流程或维护私有镜像的用户。

### 1. Fork 本仓库

打开 [https://github.com/DreamHoney-J/comfyui_cpu_docker](https://github.com/DreamHoney-J/comfyui_cpu_docker)，点击右上角 **Fork**。

### 2. 触发 GitHub Actions 构建镜像

Fork 完成后，进入你 Fork 的仓库，打开 **Actions** 页面：

- 首次 Fork 需要手动启用 Actions（GitHub 会提示 "I understand my workflows, go ahead and enable them"）
- 启用后，点击左侧 `build-and-push-comfyui-cpu` workflow，点击 **Run workflow** 手动触发
- 也可以直接推送代码到 `main` 分支，会自动触发构建

等待构建完成（约 5-10 分钟）。

### 3. 获取镜像地址

构建成功后，镜像会推送到你的 GHCR（GitHub Container Registry）。地址格式为：

```
ghcr.io/<你的GitHub用户名>/comfyui_cpu_docker:main
```

可在仓库的 **Packages** 页面查看。

### 4. 下载 docker-compose.yml 到本地

```bash
mkdir comfyui_cpu_docker && cd comfyui_cpu_docker
curl -O https://raw.githubusercontent.com/<你的GitHub用户名>/comfyui_cpu_docker/main/docker-compose.yml
```

### 5. 修改 docker-compose.yml 中的镜像地址

用编辑器打开 `docker-compose.yml`，将 `image` 字段改为你自己的镜像地址：

```yaml
services:
  comfyui:
    image: ghcr.io/<你的GitHub用户名>/comfyui_cpu_docker:main
    # ... 其余配置保持不变
```

### 6. 启动服务

```bash
mkdir -p data/models data/output data/input
docker compose up -d
```

浏览器打开 `http://localhost:8188` 即可访问 ComfyUI。

---

## 方式二：直接使用本项目已构建的镜像（推荐）

适合快速体验、不需要修改构建流程的用户。

### 1. 下载 docker-compose.yml

```bash
mkdir comfyui_cpu_docker && cd comfyui_cpu_docker
curl -O https://raw.githubusercontent.com/DreamHoney-J/comfyui_cpu_docker/main/docker-compose.yml
```

### 2. 创建数据目录

```bash
mkdir -p data/models data/output data/input
```

### 3. 启动服务

```bash
docker compose up -d
```

Docker 会自动从 GHCR 拉取本项目预构建的镜像 `ghcr.io/dreamhoney-j/comfyui_cpu_docker:main` 并启动容器。

### 4. 访问 ComfyUI

浏览器打开：

```
http://localhost:8188
```

局域网其他设备访问（替换为实际 IP）：

```
http://<你的IP>:8188
```

---

## 常用命令

```bash
# 启动
docker compose up -d

# 查看日志
docker compose logs -f

# 停止
docker compose down

# 更新镜像后重启
docker compose pull && docker compose up -d
```

## 模型存放

将模型文件放入 `data/models/` 目录下对应子目录，与 ComfyUI 标准目录结构一致：

```
data/models/
├── checkpoints/
├── loras/
├── vae/
└── ...
```

## 内置自定义节点：Grok2API Image Generator

镜像中预装了 `simple_grok2api.py` 自定义节点，位于容器内 `ComfyUI/custom_nodes/` 目录。

该节点通过 OpenAI 兼容的图像生成 API（如 Grok2API）在 ComfyUI 工作流中直接调用文生图服务，无需本地模型即可生成图片。

### 节点参数

| 参数 | 说明 |
|------|------|
| `api_base` | API 服务地址（如 `https://api.example.com`） |
| `api_key` | API 密钥 |
| `prompt` | 图像描述提示词（支持外部输入连接） |
| `model` | 模型名称，默认 `grok-imagine-1.0` |
| `n` | 生成数量（1-10） |
| `size` | 图片尺寸，支持 `1024x1024`、`1792x1024`、`1024x1792`、`1280x720`、`720x1280` |
| `response_format` | 响应格式，支持 `b64_json`、`base64`、`url` |

节点输出标准 ComfyUI `IMAGE` 类型，可直接连接预览或保存节点。

### SillyTavern 生图工作流

项目提供了 `comfyui_grok2api.json`，可直接导入 SillyTavern 作为 ComfyUI 生图工作流使用。

使用方法：

1. 在 SillyTavern 中进入 **图像生成** 设置，选择 ComfyUI 作为后端
2. 导入 `comfyui_grok2api.json` 工作流文件
3. 将工作流中的 `api_base` 和 `api_key` 替换为你自己的 API 地址和密钥

该工作流调用 `SimpleGrok2APIGen` 节点生成图片，并通过 `SaveImage` 节点保存结果。SillyTavern 会自动将提示词填入 `%prompt%` 占位符。

## 项目结构

```
comfyui_cpu_docker/
├── Dockerfile                        # 镜像构建文件（GitHub Actions 使用）
├── docker-compose.yml                # 本地部署配置
├── simple_grok2api.py                # Grok2API 自定义节点（构建时复制到容器内）
├── comfyui_grok2api.json             # SillyTavern 生图工作流配置
├── .github/
│   └── workflows/
│       └── docker-image.yml         # GitHub Actions 自动构建
└── data/                            # 持久化数据（运行后生成）
    ├── models/                      # 模型文件
    ├── output/                      # 生成图片输出
    └── input/                       # 输入图片
```
