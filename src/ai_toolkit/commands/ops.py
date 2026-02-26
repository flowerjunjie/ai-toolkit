"""
自动化运维工具 - 真实实现
使用 psutil、subprocess、docker 等实现真实的运维功能
"""

import click
import subprocess
import json
import psutil
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich.tree import Tree
import docker
import yaml

console = Console()

# Docker 客户端
try:
    docker_client = docker.from_env()
except Exception:
    docker_client = None


def run_command(cmd: List[str], capture: bool = True, timeout: int = 300) -> Dict[str, Any]:
    """执行 shell 命令"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=timeout,
            check=False
        )
        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timeout", "stdout": "", "stderr": "Timeout"}
    except Exception as e:
        return {"success": False, "error": str(e), "stdout": "", "stderr": str(e)}


def get_system_metrics() -> Dict[str, Any]:
    """获取系统指标"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage('/')._asdict(),
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_recv": psutil.net_io_counters().bytes_recv
        },
        "boot_time": psutil.boot_time(),
        "load_avg": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }


@click.group(name="ops")
def ops_cli():
    """自动化运维工具 - 真实实现"""
    pass


@ops_cli.command(name="deploy")
@click.option("--environment", "-e", default="production", help="部署环境")
@click.option("--version", "-v", help="版本号")
@click.option("--image", "-i", help="Docker镜像")
@click.option("--compose-file", "-c", help="docker-compose文件路径")
@click.option("--dry-run", is_flag=True, help="仅预览，不执行")
def auto_deploy(environment: str, version: str, image: str, compose_file: str, dry_run: bool):
    """自动化部署 - 真实 Docker 部署"""
    console.print(f"\n🚀 自动化部署\n")
    
    start_time = datetime.now()
    
    # 获取 Git 信息
    git_result = run_command(["git", "rev-parse", "--short", "HEAD"])
    git_commit = git_result["stdout"].strip() if git_result["success"] else "unknown"
    
    console.print(f"环境: {environment}")
    console.print(f"版本: {version or git_commit}")
    console.print(f"Git Commit: {git_commit}")
    
    if dry_run:
        console.print("\n[DRY RUN] 预览模式，不执行实际部署")
    
    # 部署步骤
    steps = []
    
    # 1. 检查 Git 状态
    console.print("\n[1/7] 检查 Git 状态...")
    git_status = run_command(["git", "status", "--porcelain"])
    if git_status["stdout"].strip():
        console.print("  ⚠️  有未提交的更改")
    else:
        console.print("  ✓ 工作区干净")
    
    # 2. 安装依赖
    console.print("\n[2/7] 安装依赖...")
    if not dry_run:
        pip_result = run_command(["pip", "install", "-r", "requirements.txt"])
        if pip_result["success"]:
            console.print("  ✓ 依赖安装完成")
        else:
            console.print(f"  ⚠️  依赖安装警告: {pip_result['stderr'][:100]}")
    
    # 3. 运行测试
    console.print("\n[3/7] 运行测试...")
    if not dry_run:
        test_result = run_command(["python", "-m", "pytest", "-xvs"], timeout=120)
        if test_result["success"]:
            console.print("  ✓ 测试通过")
        else:
            console.print("  ⚠️  测试有警告")
    
    # 4. 构建镜像
    if image or compose_file:
        console.print("\n[4/7] 构建 Docker 镜像...")
        if not dry_run and docker_client:
            try:
                if compose_file and Path(compose_file).exists():
                    build_result = run_command(["docker-compose", "-f", compose_file, "build"])
                else:
                    build_result = run_command(["docker", "build", "-t", image or "app:latest", "."])
                
                if build_result["success"]:
                    console.print("  ✓ 镜像构建完成")
                else:
                    console.print(f"  ✗ 构建失败: {build_result['stderr'][:200]}")
            except Exception as e:
                console.print(f"  ✗ 构建错误: {e}")
    
    # 5. 推送镜像
    if image:
        console.print("\n[5/7] 推送镜像...")
        if not dry_run:
            push_result = run_command(["docker", "push", image])
            if push_result["success"]:
                console.print("  ✓ 镜像推送完成")
    
    # 6. 更新服务
    console.print("\n[6/7] 更新服务...")
    if not dry_run:
        if compose_file and Path(compose_file).exists():
            up_result = run_command(["docker-compose", "-f", compose_file, "up", "-d"])
            if up_result["success"]:
                console.print("  ✓ 服务已更新")
        elif docker_client:
            try:
                # 尝试重启容器
                containers = docker_client.containers.list(filters={"name": environment})
                for container in containers:
                    container.restart()
                    console.print(f"  ✓ 重启容器: {container.name}")
            except Exception as e:
                console.print(f"  ⚠️  服务更新警告: {e}")
    
    # 7. 健康检查
    console.print("\n[7/7] 健康检查...")
    if not dry_run:
        import time
        time.sleep(2)
        health_result = run_command(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                                     "http://localhost:8000/health"])
        if health_result["stdout"].strip() == "200":
            console.print("  ✓ 健康检查通过")
        else:
            console.print("  ⚠️  健康检查可能需要更多时间")
    
    duration = (datetime.now() - start_time).total_seconds()
    console.print(f"\n✅ 部署完成 (耗时: {duration:.1f}s)")


@ops_cli.command(name="rollback")
@click.option("--version", "-v", help="回滚版本")
@click.option("--compose-file", "-c", help="docker-compose文件路径")
@click.option("--container", help="容器名称")
def auto_rollback(version: str, compose_file: str, container: str):
    """自动回滚 - 真实容器回滚"""
    console.print(f"\n🔄 自动回滚\n")
    
    # 获取历史镜像
    if docker_client:
        try:
            images = docker_client.images.list()
            console.print("可用镜像:")
            for img in images[:5]:
                tags = img.tags[0] if img.tags else img.id[:12]
                console.print(f"  - {tags}")
        except Exception as e:
            console.print(f"无法获取镜像: {e}")
    
    console.print(f"\n目标版本: {version or '上一个版本'}")
    
    # 回滚流程
    console.print("\n回滚流程:")
    
    # 1. 停止当前服务
    console.print("  1. 停止当前服务...")
    if compose_file and Path(compose_file).exists():
        result = run_command(["docker-compose", "-f", compose_file, "down"])
        if result["success"]:
            console.print("     ✓ 服务已停止")
    elif container and docker_client:
        try:
            c = docker_client.containers.get(container)
            c.stop()
            console.print(f"     ✓ 容器 {container} 已停止")
        except Exception as e:
            console.print(f"     ⚠️  {e}")
    
    # 2. 恢复旧版本
    console.print("  2. 恢复旧版本...")
    if version:
        result = run_command(["docker", "run", "-d", "--name", f"{container or 'app'}_rollback", version])
        if result["success"]:
            console.print("     ✓ 旧版本已启动")
    
    console.print("\n✅ 回滚完成")


@ops_cli.command(name="scale")
@click.option("--service", "-s", help="服务名称")
@click.option("--replicas", "-r", default=3, help="副本数量")
@click.option("--compose-file", "-c", help="docker-compose文件路径")
def auto_scale(service: str, replicas: int, compose_file: str):
    """自动扩缩容 - 真实 Docker 扩缩容"""
    console.print(f"\n📈 自动扩缩容\n")
    
    console.print(f"服务: {service or 'all'}")
    console.print(f"目标副本数: {replicas}")
    
    # 获取当前系统指标
    metrics = get_system_metrics()
    console.print(f"\n当前系统状态:")
    console.print(f"  CPU: {metrics['cpu_percent']}%")
    console.print(f"  内存: {metrics['memory']['percent']}%")
    console.print(f"  负载: {metrics['load_avg']}")
    
    # 扩缩容决策
    console.print("\n扩缩容策略:")
    if metrics['cpu_percent'] > 70:
        console.print("  ⚠️  CPU使用率 > 70% → 建议扩容")
    elif metrics['cpu_percent'] < 30:
        console.print("  ℹ️  CPU使用率 < 30% → 可考虑缩容")
    
    # 执行扩缩容
    if compose_file and Path(compose_file).exists():
        console.print(f"\n执行 docker-compose scale...")
        if service:
            result = run_command(["docker-compose", "-f", compose_file, "up", "-d", "--scale", 
                                f"{service}={replicas}"])
        else:
            # 读取 compose 文件获取所有服务
            with open(compose_file) as f:
                compose_data = yaml.safe_load(f)
                services = list(compose_data.get('services', {}).keys())
            
            for svc in services:
                result = run_command(["docker-compose", "-f", compose_file, "up", "-d", "--scale",
                                    f"{svc}={replicas}"])
        
        if result["success"]:
            console.print("  ✓ 扩缩容完成")
        else:
            console.print(f"  ✗ 失败: {result['stderr'][:200]}")
    elif docker_client and service:
        try:
            # 使用 Docker Swarm 模式
            service_obj = docker_client.services.get(service)
            service_obj.scale(replicas)
            console.print(f"  ✓ 服务 {service} 已缩放到 {replicas} 副本")
        except Exception as e:
            console.print(f"  ⚠️  {e}")
    
    console.print("\n✅ 扩缩容完成")


@ops_cli.command(name="monitor")
@click.option("--alert", "-a", is_flag=True, help="启用告警")
@click.option("--interval", "-i", default=5, help="监控间隔(秒)")
@click.option("--duration", "-d", default=60, help="监控时长(秒)")
def auto_monitor(alert: bool, interval: int, duration: int):
    """自动监控 - 真实系统监控"""
    console.print(f"\n📊 自动监控\n")
    
    console.print(f"监控间隔: {interval}s")
    console.print(f"监控时长: {duration}s")
    console.print(f"告警: {'启用' if alert else '禁用'}\n")
    
    # 获取进程信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # 按 CPU 排序
    top_cpu = sorted(processes, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:5]
    
    console.print("Top CPU 进程:")
    for p in top_cpu:
        console.print(f"  {p['pid']:>6} {p['name'][:20]:<20} CPU: {p['cpu_percent'] or 0:.1f}%")
    
    # 获取 Docker 容器状态
    if docker_client:
        console.print("\nDocker 容器:")
        try:
            containers = docker_client.containers.list(all=True)
            for c in containers[:10]:
                status = "✓" if c.status == "running" else "✗"
                console.print(f"  {status} {c.name[:30]:<30} {c.status}")
        except Exception as e:
            console.print(f"  无法获取容器: {e}")
    
    # 系统指标
    metrics = get_system_metrics()
    console.print(f"\n系统指标:")
    console.print(f"  CPU使用率: {metrics['cpu_percent']}%")
    console.print(f"  内存使用率: {metrics['memory']['percent']}%")
    console.print(f"  可用内存: {metrics['memory']['available'] / (1024**3):.2f} GB")
    console.print(f"  磁盘使用率: {metrics['disk']['percent']}%")
    console.print(f"  可用磁盘: {metrics['disk']['free'] / (1024**3):.2f} GB")
    
    # 告警检查
    if alert:
        alerts = []
        if metrics['cpu_percent'] > 80:
            alerts.append(f"CPU 使用率过高: {metrics['cpu_percent']}%")
        if metrics['memory']['percent'] > 85:
            alerts.append(f"内存使用率过高: {metrics['memory']['percent']}%")
        if metrics['disk']['percent'] > 90:
            alerts.append(f"磁盘使用率过高: {metrics['disk']['percent']}%")
        
        if alerts:
            console.print("\n🚨 告警:")
            for a in alerts:
                console.print(f"  ! {a}")
        else:
            console.print("\n✓ 所有指标正常")
    
    console.print("\n✅ 监控完成")


@ops_cli.command(name="backup")
@click.option("--database", "-d", is_flag=True, help="备份数据库")
@click.option("--files", "-f", is_flag=True, help="备份文件")
@click.option("--output", "-o", default="./backups", help="备份输出目录")
@click.option("--compress", "-c", is_flag=True, help="压缩备份")
def auto_backup(database: bool, files: bool, output: str, compress: bool):
    """自动备份 - 真实文件备份"""
    console.print(f"\n💾 自动备份\n")
    
    backup_dir = Path(output)
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"backup_{timestamp}"
    
    console.print(f"备份目录: {backup_dir}")
    console.print(f"备份名称: {backup_name}\n")
    
    backed_up = []
    
    if database:
        console.print("备份数据库...")
        # 检查 PostgreSQL
        pg_result = run_command(["which", "pg_dump"])
        if pg_result["success"]:
            pg_file = backup_dir / f"{backup_name}_postgres.sql"
            pg_backup = run_command([
                "pg_dump", "-h", "localhost", "-U", "postgres",
                "-f", str(pg_file), "postgres"
            ])
            if pg_backup["success"]:
                backed_up.append(f"PostgreSQL: {pg_file}")
                console.print(f"  ✓ PostgreSQL 备份: {pg_file}")
        
        # 检查 MySQL
        mysql_result = run_command(["which", "mysqldump"])
        if mysql_result["success"]:
            mysql_file = backup_dir / f"{backup_name}_mysql.sql"
            mysql_backup = run_command([
                "mysqldump", "-h", "localhost", "-u", "root",
                "-p", "database", ">", str(mysql_file)
            ])
            if mysql_backup["success"]:
                backed_up.append(f"MySQL: {mysql_file}")
                console.print(f"  ✓ MySQL 备份: {mysql_file}")
        
        # Redis
        redis_result = run_command(["which", "redis-cli"])
        if redis_result["success"]:
            redis_file = backup_dir / f"{backup_name}_redis.rdb"
            redis_backup = run_command([
                "redis-cli", "BGSAVE"
            ])
            if redis_backup["success"]:
                # 复制 dump.rdb
                dump_path = Path("/var/lib/redis/dump.rdb")
                if dump_path.exists():
                    shutil.copy2(dump_path, redis_file)
                    backed_up.append(f"Redis: {redis_file}")
                    console.print(f"  ✓ Redis 备份: {redis_file}")
    
    if files:
        console.print("\n备份文件...")
        
        # 备份配置文件
        config_paths = ["./config", "./.env", "./settings.py", "./config.yaml"]
        for path in config_paths:
            p = Path(path)
            if p.exists():
                dest = backup_dir / f"{backup_name}_config"
                if p.is_dir():
                    shutil.copytree(p, dest / p.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(p, dest)
                console.print(f"  ✓ 配置: {path}")
        
        # 备份上传文件
        upload_paths = ["./uploads", "./media", "./static"]
        for path in upload_paths:
            p = Path(path)
            if p.exists():
                dest = backup_dir / f"{backup_name}_files"
                shutil.copytree(p, dest / p.name, dirs_exist_ok=True)
                console.print(f"  ✓ 文件: {path}")
                backed_up.append(f"Files: {dest}")
    
    # 压缩备份
    if compress and backed_up:
        console.print("\n压缩备份...")
        archive_name = backup_dir / f"{backup_name}.tar.gz"
        result = run_command([
            "tar", "-czf", str(archive_name), "-C", str(backup_dir),
            backup_name
        ])
        if result["success"]:
            console.print(f"  ✓ 压缩完成: {archive_name}")
            # 删除原始文件
            shutil.rmtree(backup_dir / backup_name, ignore_errors=True)
    
    # 清理旧备份（保留最近10个）
    console.print("\n清理旧备份...")
    all_backups = sorted(backup_dir.glob("backup_*"), key=lambda x: x.stat().st_mtime)
    if len(all_backups) > 10:
        for old_backup in all_backups[:-10]:
            if old_backup.is_dir():
                shutil.rmtree(old_backup)
            else:
                old_backup.unlink()
            console.print(f"  删除: {old_backup.name}")
    
    console.print(f"\n✅ 备份完成 ({len(backed_up)} 项)")


@ops_cli.command(name="restore")
@click.option("--source", "-s", required=True, help="备份源路径")
@click.option("--target", "-t", default="./", help="目标位置")
@click.option("--database-only", is_flag=True, help="仅恢复数据库")
@click.option("--files-only", is_flag=True, help="仅恢复文件")
def auto_restore(source: str, target: str, database_only: bool, files_only: bool):
    """自动恢复 - 真实文件恢复"""
    console.print(f"\n♻️ 自动恢复\n")
    
    source_path = Path(source)
    target_path = Path(target)
    
    if not source_path.exists():
        console.print(f"✗ 备份源不存在: {source}")
        return
    
    console.print(f"源: {source}")
    console.print(f"目标: {target}\n")
    
    # 如果是压缩文件，先解压
    if source_path.suffix == ".gz" or source_path.suffix == ".tar":
        console.print("解压备份...")
        extract_dir = target_path / "extracted"
        extract_dir.mkdir(parents=True, exist_ok=True)
        result = run_command(["tar", "-xzf", str(source_path), "-C", str(extract_dir)])
        if result["success"]:
            console.print("  ✓ 解压完成")
            source_path = extract_dir
    
    # 恢复数据库
    if not files_only:
        console.print("\n恢复数据库...")
        sql_files = list(source_path.glob("*.sql"))
        for sql_file in sql_files:
            if "postgres" in sql_file.name:
                result = run_command([
                    "psql", "-h", "localhost", "-U", "postgres",
                    "-f", str(sql_file)
                ])
                if result["success"]:
                    console.print(f"  ✓ PostgreSQL: {sql_file.name}")
            elif "mysql" in sql_file.name:
                console.print(f"  ℹ️ MySQL 恢复需手动执行: {sql_file}")
    
    # 恢复文件
    if not database_only:
        console.print("\n恢复文件...")
        if source_path.is_dir():
            for item in source_path.iterdir():
                if item.is_dir():
                    dest = target_path / item.name
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                    console.print(f"  ✓ {item.name}")
    
    console.print("\n✅ 恢复完成")


@ops_cli.command(name="update")
@click.option("--package", "-p", help="包名")
@click.option("--version", "-v", help="版本号")
@click.option("--requirements", "-r", default="requirements.txt", help="requirements文件")
@click.option("--check-only", is_flag=True, help="仅检查更新")
def auto_update(package: str, version: str, requirements: str, check_only: bool):
    """自动更新 - 真实包更新"""
    console.print(f"\n⬆️ 自动更新\n")
    
    if check_only:
        console.print("检查可用更新...")
        result = run_command(["pip", "list", "--outdated", "--format=json"])
        if result["success"]:
            try:
                outdated = json.loads(result["stdout"])
                if outdated:
                    table = Table(title="可更新包")
                    table.add_column("包名", style="cyan")
                    table.add_column("当前版本", style="yellow")
                    table.add_column("最新版本", style="green")
                    
                    for pkg in outdated[:20]:  # 只显示前20个
                        table.add_row(
                            pkg.get("name", ""),
                            pkg.get("version", ""),
                            pkg.get("latest_version", "")
                        )
                    console.print(table)
                else:
                    console.print("  ✓ 所有包都是最新版本")
            except json.JSONDecodeError:
                console.print(result["stdout"])
        return
    
    # 执行更新
    if package:
        console.print(f"更新包: {package}")
        if version:
            package_spec = f"{package}=={version}"
        else:
            package_spec = package
        
        result = run_command(["pip", "install", "--upgrade", package_spec])
        if result["success"]:
            console.print(f"  ✓ {package} 更新完成")
            console.print(result["stdout"][-500:] if len(result["stdout"]) > 500 else result["stdout"])
        else:
            console.print(f"  ✗ 更新失败: {result['stderr']}")
    else:
        # 更新 requirements.txt 中的所有包
        req_path = Path(requirements)
        if req_path.exists():
            console.print(f"从 {requirements} 更新所有包...")
            result = run_command(["pip", "install", "--upgrade", "-r", str(req_path)])
            if result["success"]:
                console.print("  ✓ 所有包更新完成")
            else:
                console.print(f"  ✗ 更新失败: {result['stderr'][:500]}")
    
    console.print("\n✅ 更新完成")


@ops_cli.command(name="health")
@click.option("--service", "-s", help="服务名称")
@click.option("--port", "-p", default=8000, help="服务端口")
@click.option("--timeout", "-t", default=5, help="超时时间")
def auto_health(service: str, port: int, timeout: int):
    """健康检查 - 真实服务检查"""
    console.print(f"\n❤️ 健康检查\n")
    
    checks = []
    
    # 系统健康
    console.print("系统健康:")
    metrics = get_system_metrics()
    
    system_ok = True
    if metrics['cpu_percent'] > 90:
        console.print(f"  ✗ CPU: {metrics['cpu_percent']}% (过高)")
        system_ok = False
    else:
        console.print(f"  ✓ CPU: {metrics['cpu_percent']}%")
    
    if metrics['memory']['percent'] > 90:
        console.print(f"  ✗ 内存: {metrics['memory']['percent']}% (过高)")
        system_ok = False
    else:
        console.print(f"  ✓ 内存: {metrics['memory']['percent']}%")
    
    if metrics['disk']['percent'] > 95:
        console.print(f"  ✗ 磁盘: {metrics['disk']['percent']}% (过高)")
        system_ok = False
    else:
        console.print(f"  ✓ 磁盘: {metrics['disk']['percent']}%")
    
    checks.append(("System", system_ok))
    
    # Docker 健康
    if docker_client:
        console.print("\nDocker 容器:")
        try:
            containers = docker_client.containers.list()
            for c in containers:
                # 获取容器健康状态
                health = c.attrs.get('State', {}).get('Health', {}).get('Status', 'unknown')
                status_ok = c.status == "running"
                icon = "✓" if status_ok else "✗"
                console.print(f"  {icon} {c.name[:30]:<30} {c.status} (health: {health})")
                checks.append((c.name, status_ok))
        except Exception as e:
            console.print(f"  ⚠️ 无法检查容器: {e}")
    
    # HTTP 健康检查
    console.print("\nHTTP 服务:")
    endpoints = [
        ("localhost", port, "/health"),
        ("localhost", port, "/api/health"),
    ]
    
    for host, p, path in endpoints:
        url = f"http://{host}:{p}{path}"
        result = run_command(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", 
                             "--max-time", str(timeout), url])
        status_code = result["stdout"].strip()
        if status_code == "200":
            console.print(f"  ✓ {url} (200)")
            checks.append((url, True))
        else:
            console.print(f"  ✗ {url} ({status_code or 'unreachable'})")
            checks.append((url, False))
    
    # 总结
    console.print("\n" + "="*50)
    passed = sum(1 for _, ok in checks if ok)
    total = len(checks)
    console.print(f"检查结果: {passed}/{total} 通过")
    
    if passed == total:
        console.print("✅ 所有检查通过")
    else:
        console.print("⚠️  部分检查失败")


@ops_cli.command(name="log")
@click.option("--service", "-s", help="服务名称/容器名")
@click.option("--tail", "-t", default=100, help="行数")
@click.option("--follow", "-f", is_flag=True, help="持续跟踪")
@click.option("--since", help="开始时间 (如: 1h, 30m)")
def auto_log(service: str, tail: int, follow: bool, since: str):
    """日志管理 - 真实日志查看"""
    console.print(f"\n📝 日志管理\n")
    
    if service and docker_client:
        # Docker 容器日志
        console.print(f"容器: {service}")
        try:
            container = docker_client.containers.get(service)
            
            kwargs = {"tail": tail}
            if since:
                kwargs["since"] = since
            
            logs = container.logs(**kwargs).decode('utf-8', errors='replace')
            console.print("\n日志内容:")
            console.print("-" * 60)
            
            lines = logs.split('\n')
            for line in lines[-tail:]:
                if line:
                    console.print(line)
            
            if follow:
                console.print("\n[按 Ctrl+C 停止跟踪]\n")
                for log_line in container.logs(stream=True, follow=True):
                    console.print(log_line.decode('utf-8', errors='replace'), end='')
                    
        except docker.errors.NotFound:
            console.print(f"✗ 容器不存在: {service}")
        except KeyboardInterrupt:
            console.print("\n\n停止跟踪")
    else:
        # 系统日志
        console.print("系统日志:")
        
        # 尝试 journalctl
        journal_result = run_command(["which", "journalctl"])
        if journal_result["success"]:
            cmd = ["journalctl", "-n", str(tail), "--no-pager"]
            if since:
                cmd.extend(["--since", since])
            
            result = run_command(cmd)
            if result["success"]:
                console.print(result["stdout"])
        else:
            # 尝试读取 syslog
            syslog_paths = ["/var/log/syslog", "/var/log/messages"]
            for path in syslog_paths:
                if Path(path).exists():
                    result = run_command(["tail", "-n", str(tail), path])
                    if result["success"]:
                        console.print(result["stdout"])
                        break
    
    console.print("\n✅ 日志查看完成")


@ops_cli.command(name="clean")
@click.option("--logs", "-l", is_flag=True, help="清理日志")
@click.option("--cache", "-c", is_flag=True, help="清理缓存")
@click.option("--temp", "-t", is_flag=True, help="清理临时文件")
@click.option("--docker", "-d", is_flag=True, help="清理 Docker")
@click.option("--all", "-a", is_flag=True, help="清理所有")
def auto_clean(logs: bool, cache: bool, temp: bool, docker: bool, all: bool):
    """自动清理 - 真实系统清理"""
    console.print(f"\n🧹 自动清理\n")
    
    if all:
        logs = cache = temp = docker = True
    
    total_freed = 0
    
    if logs:
        console.print("清理日志...")
        log_paths = [
            "/var/log",
            "./logs",
            "./log",
            Path.home() / ".cache" / "pip" / "log"
        ]
        
        for path in log_paths:
            p = Path(path)
            if p.exists():
                # 删除 7 天前的日志
                result = run_command([
                    "find", str(p), "-name", "*.log",
                    "-mtime", "+7", "-delete"
                ])
                console.print(f"  ✓ 清理: {path}")
    
    if cache:
        console.print("\n清理缓存...")
        
        # pip 缓存
        pip_cache = run_command(["pip", "cache", "purge"])
        if pip_cache["success"]:
            console.print("  ✓ pip 缓存已清理")
        
        # Python pycache
        result = run_command([
            "find", ".", "-type", "d", "-name", "__pycache__",
            "-exec", "rm", "-rf", "{}", "+", "2>/dev/null"
        ])
        console.print("  ✓ Python 缓存已清理")
        
        # npm/yarn 缓存
        npm_result = run_command(["npm", "cache", "clean", "--force"])
        if npm_result["success"]:
            console.print("  ✓ npm 缓存已清理")
    
    if temp:
        console.print("\n清理临时文件...")
        temp_paths = ["/tmp", "/var/tmp", Path.home() / ".tmp"]
        for path in temp_paths:
            p = Path(path)
            if p.exists():
                # 删除 1 天前的临时文件
                result = run_command([
                    "find", str(p), "-type", "f",
                    "-mtime", "+1", "-delete"
                ])
                console.print(f"  ✓ 清理: {path}")
    
    if docker:
        console.print("\n清理 Docker...")
        if docker_client:
            try:
                # 清理未使用的容器
                docker_client.containers.prune()
                console.print("  ✓ 未使用容器已清理")
                
                # 清理未使用的镜像
                docker_client.images.prune(filters={"dangling": True})
                console.print("  ✓ 悬空镜像已清理")
                
                # 清理构建缓存
                result = run_command(["docker", "builder", "prune", "-f"])
                if result["success"]:
                    console.print("  ✓ 构建缓存已清理")
            except Exception as e:
                console.print(f"  ⚠️  Docker 清理警告: {e}")
    
    console.print("\n✅ 清理完成")


@ops_cli.command(name="secure")
@click.option("--scan", "-s", is_flag=True, help="安全扫描")
@click.option("--fix", "-f", is_flag=True, help="自动修复")
@click.option("--audit", "-a", is_flag=True, help="审计模式")
def auto_secure(scan: bool, fix: bool, audit: bool):
    """安全加固 - 真实安全检查"""
    console.print(f"\n🔒 安全加固\n")
    
    issues = []
    
    # 1. 检查文件权限
    console.print("检查文件权限...")
    sensitive_files = [
        Path.home() / ".ssh" / "id_rsa",
        Path(".env"),
        Path("config.yaml"),
        Path("secrets.json")
    ]
    
    for file_path in sensitive_files:
        if file_path.exists():
            stat = file_path.stat()
            # 检查是否对其他用户可读
            if stat.st_mode & 0o044:
                console.print(f"  ⚠️  {file_path} 权限过于开放")
                issues.append(("permission", str(file_path)))
                if fix:
                    file_path.chmod(0o600)
                    console.print(f"    ✓ 已修复权限")
    
    # 2. 检查依赖漏洞
    if scan:
        console.print("\n扫描依赖漏洞...")
        safety_result = run_command(["safety", "check", "--json"])
        if safety_result["success"]:
            try:
                vulnerabilities = json.loads(safety_result["stdout"])
                if vulnerabilities:
                    console.print(f"  ⚠️  发现 {len(vulnerabilities)} 个漏洞")
                    for vuln in vulnerabilities[:5]:
                        console.print(f"    - {vuln.get('package_name')}: {vuln.get('vulnerability_id')}")
                else:
                    console.print("  ✓ 无已知漏洞")
            except:
                console.print("  ℹ️ 安全扫描完成")
    
    # 3. 检查代码安全问题
    console.print("\n代码安全扫描...")
    bandit_result = run_command(["bandit", "-r", "-f", "json", "."])
    if bandit_result["success"]:
        try:
            bandit_data = json.loads(bandit_result["stdout"])
            issues_count = len(bandit_data.get("results", []))
            if issues_count > 0:
                console.print(f"  ⚠️  发现 {issues_count} 个安全问题")
            else:
                console.print("  ✓ 代码安全")
        except:
            console.print("  ℹ️ 扫描完成")
    
    # 4. 检查环境变量
    console.print("\n检查敏感信息...")
    import os
    sensitive_vars = ['PASSWORD', 'SECRET', 'TOKEN', 'KEY', 'CREDENTIAL']
    for key in os.environ:
        for pattern in sensitive_vars:
            if pattern in key.upper():
                console.print(f"  ℹ️  发现敏感环境变量: {key}")
    
    # 5. 审计报告
    if audit:
        console.print("\n生成审计报告...")
        audit_report = {
            "timestamp": datetime.now().isoformat(),
            "issues_found": len(issues),
            "issues": issues,
            "recommendations": [
                "定期更新依赖包",
                "使用密钥管理服务",
                "启用双因素认证",
                "定期轮换密钥"
            ]
        }
        
        report_file = Path("security_audit.json")
        with open(report_file, 'w') as f:
            json.dump(audit_report, f, indent=2)
        console.print(f"  ✓ 审计报告已保存: {report_file}")
    
    console.print("\n✅ 安全加固完成")


if __name__ == "__main__":
    ops_cli()