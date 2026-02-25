# comfyui_cpu_docker

在 WSL（Ubuntu 22.04）中，使用 Docker Compose 以 CPU 模式部署 ComfyUI，并通过 GitHub Actions 自动构建镜像推送到 GHCR。

## 环境要求

- Windows 11 + WSL2 + Ubuntu 22.04
- Docker Desktop（已启用 WSL2 集成）
- 无需 NVIDIA 显卡，纯 CPU 运行

## 镜像

镜像由 GitHub Actions 自动构建并推送到 GHCR：

```
ghcr.io/dreamhoney-j/comfyui_cpu_docker:main
```

## 快速开始

### 1. 克隆本仓库

```bash
git clone https://github.com/DreamHoney-J/comfyui_cpu_docker.git
cd comfyui_cpu_docker
```

### 2. 创建数据目录

```bash
mkdir -p data/models data/output data/input
```

### 3. 启动服务

```bash
docker compose up -d
```

Docker 会自动从 GHCR 拉取镜像并启动容器。

### 4. 访问 ComfyUI

浏览器打开：

```
http://localhost:8188
```

局域网其他设备访问（替换为你的 WSL IP）：

```
http://<WSL_IP>:8188
```

## 目录结构

```
comfyui_cpu_docker/
├── Dockerfile                        # 镜像构建文件
├── docker-compose.yml                # 本地启动配置
├── .github/
│   └── workflows/
│       └── docker-image.yml         # GitHub Actions 自动构建
└── data/                            # 持久化数据（运行后自动生成）
    ├── models/                      # 模型文件
    ├── output/                      # 生成图片输出
    └── input/                       # 输入图片
```

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

## GitHub Actions 自动构建

每次推送到 `main` 分支或打 `v*.*.*` tag，会自动触发构建并推送镜像到 GHCR。

也可在仓库 Actions 页面手动触发：[Actions](https://github.com/DreamHoney-J/comfyui_cpu_docker/actions)
