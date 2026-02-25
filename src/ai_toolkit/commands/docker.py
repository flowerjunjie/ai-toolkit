"""
容器化工具 - 真实 Docker 集成版
真实调用 docker 命令执行容器操作
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess
import json
import shutil

console = Console()


def check_docker():
    """检查 Docker 是否安装"""
    return shutil.which("docker") is not None


def run_docker_command(args, capture_output=True, check=True):
    """运行 Docker 命令"""
    if not check_docker():
        console.print("❌ Docker 未安装或未在 PATH 中")
        return None
    
    cmd = ["docker"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        console.print(f"❌ Docker 命令失败: {e.stderr}")
        return None
    except Exception as e:
        console.print(f"❌ 错误: {e}")
        return None


@click.group(name="docker")
def docker_cli():
    """Docker容器化工具"""
    pass


@docker_cli.command(name="build")
@click.option("--tag", "-t", default="ai-toolkit:latest", help="镜像标签")
@click.option("--platform", "-p", help="目标平台 (如 linux/amd64)")
@click.option("--no-cache", is_flag=True, help="不使用缓存")
@click.option("--push", is_flag=True, help="构建后推送")
def build_image(tag: str, platform: str, no_cache: bool, push: bool):
    """构建Docker镜像"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print(f"\n🔨 构建镜像: {tag}\n")
    
    # 检查 Dockerfile 是否存在
    dockerfile_path = Path("Dockerfile")
    if not dockerfile_path.exists():
        console.print("📄 未找到 Dockerfile，创建默认配置...")
        dockerfile_content = """FROM python:3.9-slim

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
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(dockerfile_content)
        console.print(f"✅ Dockerfile已创建: {dockerfile_path}")
    
    # 构建命令
    cmd = ["build", "-t", tag, "."]
    
    if no_cache:
        cmd.append("--no-cache")
    
    if platform:
        cmd.extend(["--platform", platform])
    
    console.print(f"执行: docker {' '.join(cmd)}\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        progress.add_task("正在构建镜像...", total=None)
        result = run_docker_command(cmd, capture_output=False, check=False)
    
    if result and result.returncode == 0:
        console.print(f"\n✅ 镜像构建成功: {tag}")
        
        # 显示镜像信息
        result_info = run_docker_command(["images", tag, "--format", "json"])
        if result_info and result_info.stdout:
            console.print("\n📊 镜像信息:")
            console.print(result_info.stdout)
        
        if push:
            console.print(f"\n📤 推送镜像: {tag}")
            push_result = run_docker_command(["push", tag], capture_output=False, check=False)
            if push_result and push_result.returncode == 0:
                console.print(f"✅ 推送成功")
    else:
        console.print("\n❌ 镜像构建失败")


@docker_cli.command(name="run")
@click.option("--image", "-i", default="ai-toolkit:latest", help="镜像名称")
@click.option("--port", "-p", default=8000, help="主机端口")
@click.option("--container-port", default=8000, help="容器端口")
@click.option("--name", "-n", help="容器名称")
@click.option("--detach", "-d", is_flag=True, help="后台运行")
@click.option("--volume", "-v", multiple=True, help="挂载卷 (格式: 主机路径:容器路径)")
@click.option("--env", "-e", multiple=True, help="环境变量 (格式: KEY=VALUE)")
@click.option("--rm", is_flag=True, help="停止后自动删除容器")
def run_container(image: str, port: int, container_port: int, name: str, 
                  detach: bool, volume: tuple, env: tuple, rm: bool):
    """运行容器"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print(f"\n🚀 运行容器: {image}\n")
    
    cmd = ["run"]
    
    if detach:
        cmd.append("-d")
    
    if rm:
        cmd.append("--rm")
    
    if name:
        cmd.extend(["--name", name])
    
    cmd.extend(["-p", f"{port}:{container_port}"])
    
    for vol in volume:
        cmd.extend(["-v", vol])
    
    for e in env:
        cmd.extend(["-e", e])
    
    cmd.append(image)
    
    console.print(f"执行: docker {' '.join(cmd)}\n")
    
    result = run_docker_command(cmd, capture_output=False, check=False)
    
    if result and result.returncode == 0:
        console.print("\n✅ 容器启动成功")
        if detach:
            console.print(f"\n💡 查看日志: docker logs {name or '<container_id>'}")
            console.print(f"💡 停止容器: docker stop {name or '<container_id>'}")
    else:
        console.print("\n❌ 容器启动失败")


@docker_cli.command(name="compose")
@click.option("--up", is_flag=True, help="启动服务")
@click.option("--down", is_flag=True, help="停止服务")
@click.option("--build", is_flag=True, help="重新构建")
@click.option("--logs", is_flag=True, help="查看日志")
def compose_command(up: bool, down: bool, build: bool, logs: bool):
    """Docker Compose 管理"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    compose_file = Path("docker-compose.yml")
    
    if not compose_file.exists():
        console.print("📄 创建 docker-compose.yml...")
        compose_content = """version: '3.8'

services:
  ai-toolkit:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ~/.ai-toolkit:/app/data
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

volumes:
  redis-data:
"""
        with open(compose_file, "w", encoding="utf-8") as f:
            f.write(compose_content)
        console.print(f"✅ docker-compose.yml 已创建")
    
    if up:
        console.print("\n🚀 启动服务...")
        cmd = ["compose", "up", "-d"]
        if build:
            cmd.append("--build")
        result = run_docker_command(cmd, capture_output=False, check=False)
        if result and result.returncode == 0:
            console.print("✅ 服务已启动")
            console.print("\n💡 查看状态: docker compose ps")
            console.print("💡 查看日志: docker compose logs -f")
    
    elif down:
        console.print("\n🛑 停止服务...")
        result = run_docker_command(["compose", "down"], capture_output=False, check=False)
        if result and result.returncode == 0:
            console.print("✅ 服务已停止")
    
    elif logs:
        console.print("\n📝 查看日志...")
        run_docker_command(["compose", "logs", "-f"], capture_output=False, check=False)
    
    else:
        console.print("\n📦 Docker Compose 配置")
        console.print(f"配置文件: {compose_file.absolute()}")
        console.print("\n可用命令:")
        console.print("  ai-toolkit docker compose --up       # 启动服务")
        console.print("  ai-toolkit docker compose --down     # 停止服务")
        console.print("  ai-toolkit docker compose --up --build  # 重新构建并启动")
        console.print("  ai-toolkit docker compose --logs     # 查看日志")


@docker_cli.command(name="images")
@click.option("--filter", "-f", help="过滤条件")
def list_images(filter: str):
    """列出镜像"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print("\n📊 镜像列表\n")
    
    cmd = ["images", "--format", "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"]
    
    if filter:
        cmd.extend(["--filter", f"reference={filter}"])
    
    result = run_docker_command(cmd, check=False)
    
    if result and result.stdout:
        console.print(result.stdout)
    else:
        # 备用表格显示
        cmd_json = ["images", "--format", "json"]
        result = run_docker_command(cmd_json, check=False)
        
        if result and result.stdout:
            images = []
            for line in result.stdout.strip().split('\n'):
                try:
                    images.append(json.loads(line))
                except:
                    pass
            
            table = Table(show_header=True)
            table.add_column("仓库", style="cyan")
            table.add_column("标签", style="green")
            table.add_column("大小", style="yellow")
            table.add_column("创建时间", style="blue")
            
            for img in images[:20]:  # 限制显示数量
                table.add_row(
                    img.get("Repository", "<none>"),
                    img.get("Tag", "<none>"),
                    img.get("Size", "unknown"),
                    img.get("CreatedAt", "unknown")
                )
            
            console.print(table)


@docker_cli.command(name="containers")
@click.option("--all", "-a", is_flag=True, help="显示所有容器")
def list_containers(all: bool):
    """列出容器"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print("\n📊 容器列表\n")
    
    cmd = ["ps"]
    if all:
        cmd.append("-a")
    
    cmd.extend(["--format", "json"])
    
    result = run_docker_command(cmd, check=False)
    
    if result and result.stdout:
        containers = []
        for line in result.stdout.strip().split('\n'):
            try:
                containers.append(json.loads(line))
            except:
                pass
        
        if containers:
            table = Table(show_header=True)
            table.add_column("容器ID", style="cyan", max_width=12)
            table.add_column("名称", style="green")
            table.add_column("镜像", style="yellow")
            table.add_column("状态", style="blue")
            table.add_column("端口", style="magenta")
            
            for c in containers:
                table.add_row(
                    c.get("ID", "")[:12],
                    c.get("Names", ""),
                    c.get("Image", ""),
                    c.get("State", ""),
                    c.get("Ports", "")
                )
            
            console.print(table)
        else:
            console.print("暂无运行中的容器")
    
    console.print("\n💡 管理命令:")
    console.print("  docker stop <container>   # 停止容器")
    console.print("  docker start <container>  # 启动容器")
    console.print("  docker rm <container>     # 删除容器")


@docker_cli.command(name="clean")
@click.option("--force", "-f", is_flag=True, help="强制清理，无需确认")
@click.option("--images", is_flag=True, help="清理未使用的镜像")
@click.option("--containers", is_flag=True, help="清理停止的容器")
@click.option("--volumes", is_flag=True, help="清理未使用的卷")
@click.option("--all", is_flag=True, help="清理所有未使用的资源")
def clean_docker(force: bool, images: bool, containers: bool, volumes: bool, all: bool):
    """清理Docker资源"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print("\n🧹 清理Docker资源\n")
    
    if not any([images, containers, volumes, all]):
        console.print("请指定要清理的资源类型:")
        console.print("  --images      清理未使用的镜像")
        console.print("  --containers  清理停止的容器")
        console.print("  --volumes     清理未使用的卷")
        console.print("  --all         清理所有未使用的资源")
        return
    
    if all:
        if not force:
            console.print("⚠️ 警告: 这将删除所有未使用的 Docker 资源！")
            console.print("使用 --force 跳过确认")
            return
        
        console.print("🧹 清理所有未使用的资源...")
        result = run_docker_command(["system", "prune", "-a", "--volumes", "-f"], 
                                    capture_output=False, check=False)
        if result and result.returncode == 0:
            console.print("✅ 清理完成")
    else:
        if images:
            console.print("🧹 清理未使用的镜像...")
            run_docker_command(["image", "prune", "-f"], capture_output=False, check=False)
        
        if containers:
            console.print("🧹 清理停止的容器...")
            run_docker_command(["container", "prune", "-f"], capture_output=False, check=False)
        
        if volumes:
            console.print("🧹 清理未使用的卷...")
            run_docker_command(["volume", "prune", "-f"], capture_output=False, check=False)
        
        console.print("\n✅ 清理完成")


@docker_cli.command(name="logs")
@click.argument("container")
@click.option("--follow", "-f", is_flag=True, help="跟踪日志")
@click.option("--tail", "-n", default=100, help="显示最后N行")
@click.option("--since", help="显示自某时间以来的日志 (如 1h, 30m)")
def show_logs(container: str, follow: bool, tail: int, since: str):
    """查看容器日志"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print(f"\n📝 查看日志: {container}\n")
    
    cmd = ["logs"]
    
    if follow:
        cmd.append("-f")
    
    if tail:
        cmd.extend(["--tail", str(tail)])
    
    if since:
        cmd.extend(["--since", since])
    
    cmd.append(container)
    
    run_docker_command(cmd, capture_output=False, check=False)


@docker_cli.command(name="exec")
@click.argument("container")
@click.argument("command", default="/bin/sh")
@click.option("--interactive", "-i", is_flag=True, help="交互模式")
def exec_command(container: str, command: str, interactive: bool):
    """在运行中的容器内执行命令"""
    if not check_docker():
        console.print("❌ Docker 未安装")
        return
    
    console.print(f"\n🔧 在 {container} 中执行: {command}\n")
    
    cmd = ["exec"]
    
    if interactive:
        cmd.append("-it")
    
    cmd.extend([container, command])
    
    run_docker_command(cmd, capture_output=False, check=False)


@docker_cli.command(name="status")
def docker_status():
    """检查 Docker 状态"""
    console.print("\n🔍 Docker 状态\n")
    
    if not check_docker():
        console.print("❌ Docker 未安装或未在 PATH 中")
        console.print("\n安装指南:")
        console.print("  Ubuntu/Debian: sudo apt install docker.io")
        console.print("  macOS: https://docs.docker.com/desktop/install/mac/")
        console.print("  Windows: https://docs.docker.com/desktop/install/windows/")
        return
    
    console.print("✅ Docker CLI 已安装")
    
    # 检查 Docker 守护进程
    result = run_docker_command(["version", "--format", "json"], check=False)
    if result and result.returncode == 0:
        try:
            version_info = json.loads(result.stdout)
            server_version = version_info.get("Server", {}).get("Version", "unknown")
            client_version = version_info.get("Client", {}).get("Version", "unknown")
            console.print(f"✅ Docker 守护进程运行中")
            console.print(f"   客户端版本: {client_version}")
            console.print(f"   服务端版本: {server_version}")
        except:
            console.print("✅ Docker 守护进程运行中")
    else:
        console.print("❌ Docker 守护进程未运行")
        return
    
    # 显示资源使用情况
    console.print("\n📊 资源使用:")
    
    # 镜像数量
    result = run_docker_command(["images", "-q"], check=False)
    image_count = len(result.stdout.strip().split('\n')) if result and result.stdout else 0
    console.print(f"   镜像数量: {image_count}")
    
    # 容器数量
    result = run_docker_command(["ps", "-q"], check=False)
    running_count = len(result.stdout.strip().split('\n')) if result and result.stdout else 0
    result = run_docker_command(["ps", "-aq"], check=False)
    total_count = len(result.stdout.strip().split('\n')) if result and result.stdout else 0
    console.print(f"   运行容器: {running_count}")
    console.print(f"   总容器数: {total_count}")
    
    # 磁盘使用
    result = run_docker_command(["system", "df"], check=False)
    if result and result.stdout:
        console.print("\n💾 磁盘使用:")
        console.print(result.stdout)
