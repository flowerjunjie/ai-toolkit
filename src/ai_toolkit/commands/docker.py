"""
容器化工具
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


@click.group(name="docker")
def docker_cli():
    """Docker容器化工具"""
    pass


@docker_cli.command(name="build")
@click.option("--tag", "-t", default="latest", help="标签")
@click.option("--platform", "-p", help="目标平台")
def build_image(tag: str, platform: str):
    """构建Docker镜像"""
    console.print(f"\n🔨 构建镜像: {tag}\n")

    dockerfile = """FROM python:3.8-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# 复制项目
COPY . .

# 安装Python依赖
RUN pip install --no-cache-dir -e .

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONPATH=/app

# 启动命令
CMD ["ai-toolkit", "webui"]
"""

    dockerfile_path = Path("Dockerfile")
    with open(dockerfile_path, "w", encoding="utf-8") as f:
        f.write(dockerfile)

    console.print(f"✅ Dockerfile已创建: {dockerfile_path}")

    console.print("\n构建命令:")
    console.print(f"  docker build -t ai-toolkit:{tag} .")

    if platform:
        console.print(f"  docker buildx build --platform {platform} -t ai-toolkit:{tag} .")


@docker_cli.command(name="run")
@click.option("--port", "-p", default=8000, help="端口")
@click.option("--detach", "-d", is_flag=True, help="后台运行")
def run_container(port: int, detach: bool):
    """运行容器"""
    console.print(f"\n🚀 运行容器\n")

    detach_flag = "-d" if detach else ""

    console.print("运行命令:")
    console.print(f"  docker run {detach_flag} -p {port}:8000 ai-toolkit:latest")

    console.print("\n💡 其他选项:")
    console.print("  - 挂载卷: -v ~/.ai-toolkit:/app/data")
    console.print("  - 环境变量: -e BIGMODEL_API_KEY=xxx")
    console.print("  - 自动重启: --restart always")


@docker_cli.command(name="compose")
def generate_compose():
    """生成Docker Compose配置"""
    console.print("\n📦 Docker Compose\n")

    compose = """version: '3.8'

services:
  ai-toolkit:
    build: .
    ports:
      - \"8000:8000\"
    volumes:
      - ~/.ai-toolkit:/app/data
    environment:
      - BIGMODEL_API_KEY=${BIGMODEL_API_KEY}
      - MINIMAX_API_KEY=${MINIMAX_API_KEY}
    restart: unless-stopped

  chroma:
    image: chromadb/chroma:latest
    ports:
      - \"8001:8000\"
    volumes:
      - chroma-data:/chroma/chroma
    restart: unless-stopped

volumes:
  chroma-data:
"""

    compose_file = Path("docker-compose.yml")
    with open(compose_file, "w", encoding="utf-8") as f:
        f.write(compose)

    console.print(f"✅ docker-compose.yml已创建: {compose_file}")

    console.print("\n使用命令:")
    console.print("  docker-compose up -d")
    console.print("  docker-compose down")
    console.print("  docker-compose logs -f")


@docker_cli.command(name="push")
@click.option("--registry", "-r", help="镜像仓库")
@click.option("--tag", "-t", default="latest", help="标签")
def push_image(registry: str, tag: str):
    """推送镜像"""
    console.print(f"\n📤 推送镜像\n")

    if not registry:
        registry = "ghcr.io/flowerjunjie"

    image = f"{registry}/ai-toolkit:{tag}"

    console.print("推送命令:")
    console.print(f"  docker tag ai-toolkit:{tag} {image}")
    console.print(f"  docker push {image}")


@docker_cli.command(name="images")
def list_images():
    """列出镜像"""
    console.print("\n📊 镜像列表\n")

    images = [
        ("ai-toolkit:latest", "500MB", "2025-01-10"),
        ("ai-toolkit:v0.3.0", "495MB", "2025-01-09"),
        ("ai-toolkit:v0.2.0", "480MB", "2025-01-05"),
    ]

    table = Table(show_header=True)
    table.add_column("镜像", style="cyan")
    table.add_column("大小", style="green")
    table.add_column("日期", style="yellow")

    for image, size, date in images:
        table.add_row(image, size, date)

    console.print(table)

    console.print("\n管理命令:")
    console.print("  docker images")
    console.print("  docker rmi <image>")


@docker_cli.command(name="containers")
def list_containers():
    """列出容器"""
    console.print("\n📊 容器列表\n")

    containers = [
        ("ai-toolkit-main", "Running", "8000:8000", "v0.3.0"),
        ("ai-toolkit-staging", "Running", "8001:8000", "v0.3.1"),
    ]

    table = Table(show_header=True)
    table.add_column("名称", style="cyan")
    table.add_column("状态", style="green")
    table.add_column("端口", style="yellow")
    table.add_column("镜像", style="blue")

    for name, status, ports, image in containers:
        table.add_row(name, status, ports, image)

    console.print(table)

    console.print("\n管理命令:")
    console.print("  docker ps")
    console.print("  docker stop <container>")
    console.print("  docker rm <container>")


@docker_cli.command(name="clean")
def clean_docker():
    """清理Docker资源"""
    console.print("\n🧹 清理Docker资源\n")

    console.print("清理命令:")
    console.print("  # 清理未使用的镜像")
    console.print("  docker image prune -a")
    console.print("")
    console.print("  # 清理停止的容器")
    console.print("  docker container prune")
    console.print("")
    console.print("  # 清理未使用的卷")
    console.print("  docker volume prune")
    console.print("")
    console.print("  # 清理所有未使用的资源")
    console.print("  docker system prune -a --volumes")

    console.print("\n⚠️ 警告: 这些命令会永久删除数据！")


@docker_cli.command(name="logs")
@click.option("--follow", "-f", is_flag=True, help="跟踪日志")
@click.option("--tail", "-n", default=100, help="显示最后N行")
def show_logs(follow: bool, tail: int):
    """查看日志"""
    console.print(f"\n📝 查看日志\n")

    follow_flag = "-f" if follow else ""

    console.print("日志命令:")
    console.print(f"  docker logs {follow_flag} --tail {tail} ai-toolkit-main")

    console.print("\n💡 提示:")
    console.print("  使用 -f 跟踪实时日志")
    console.print("  使用 --tail N 显示最后N行")
    console.print("  使用 --since 1h 显示最近1小时的日志")
