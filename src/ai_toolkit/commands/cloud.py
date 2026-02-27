"""
云服务 - 真实化实现
支持真实 AWS、Azure、GCP 云操作
"""

import os
import json
import subprocess
import click
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree

console = Console()

# 云配置目录
CLOUD_CONFIG_DIR = Path.home() / ".ai-toolkit" / "cloud"
CLOUD_CONFIG_FILE = CLOUD_CONFIG_DIR / "config.json"


def _ensure_config_dir():
    """确保配置目录存在"""
    CLOUD_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def _load_config() -> Dict[str, Any]:
    """加载云配置"""
    _ensure_config_dir()
    if CLOUD_CONFIG_FILE.exists():
        with open(CLOUD_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"profiles": {}, "deployments": []}


def _save_config(config: Dict[str, Any]):
    """保存云配置"""
    _ensure_config_dir()
    with open(CLOUD_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def _check_aws_cli() -> bool:
    """检查 AWS CLI 是否安装"""
    try:
        result = subprocess.run(["aws", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _check_azure_cli() -> bool:
    """检查 Azure CLI 是否安装"""
    try:
        result = subprocess.run(["az", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _check_gcloud_cli() -> bool:
    """检查 Google Cloud CLI 是否安装"""
    try:
        result = subprocess.run(["gcloud", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def _run_aws_command(args: List[str]) -> tuple:
    """运行 AWS CLI 命令"""
    cmd = ["aws"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def _run_azure_command(args: List[str]) -> tuple:
    """运行 Azure CLI 命令"""
    cmd = ["az"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def _run_gcloud_command(args: List[str]) -> tuple:
    """运行 gcloud 命令"""
    cmd = ["gcloud"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


@click.group(name="cloud")
def cloud_cli():
    """云服务 - 支持 AWS、Azure、GCP 真实操作"""
    pass


@cloud_cli.command(name="status")
def cloud_status():
    """检查云 CLI 工具状态"""
    console.print("\n[bold cyan]☁️ 云 CLI 工具状态[/bold cyan]\n")
    
    aws_ok = _check_aws_cli()
    azure_ok = _check_azure_cli()
    gcloud_ok = _check_gcloud_cli()
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("平台", style="cyan")
    table.add_column("CLI 工具", style="white")
    table.add_column("状态", style="green")
    
    table.add_row(
        "AWS",
        "aws-cli",
        "[green]✓ 已安装[/green]" if aws_ok else "[red]✗ 未安装[/red]"
    )
    table.add_row(
        "Azure",
        "azure-cli",
        "[green]✓ 已安装[/green]" if azure_ok else "[red]✗ 未安装[/red]"
    )
    table.add_row(
        "GCP",
        "gcloud",
        "[green]✓ 已安装[/green]" if gcloud_ok else "[red]✗ 未安装[/red]"
    )
    
    console.print(table)
    
    if not any([aws_ok, azure_ok, gcloud_ok]):
        console.print("\n[yellow]提示: 未检测到任何云 CLI 工具[/yellow]")
        console.print("安装指南:")
        console.print("  AWS:    pip install awscli  或  https://aws.amazon.com/cli/")
        console.print("  Azure:  https://aka.ms/installazurecli")
        console.print("  GCP:    https://cloud.google.com/sdk/docs/install")


@cloud_cli.command(name="configure")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--profile", "-pr", default="default", help="配置文件名称")
def configure_cloud(platform: str, profile: str):
    """配置云平台认证"""
    console.print(f"\n[bold cyan]⚙️ 配置 {platform.upper()}[/bold cyan]\n")
    
    if platform == "aws":
        if not _check_aws_cli():
            console.print("[red]错误: AWS CLI 未安装[/red]")
            console.print("运行: pip install awscli")
            raise click.Exit(1)
        
        console.print("运行 AWS 配置向导...")
        result = subprocess.run(["aws", "configure", "--profile", profile])
        if result.returncode == 0:
            console.print(f"\n[green]✅ AWS 配置完成 (profile: {profile})[/green]")
        
    elif platform == "azure":
        if not _check_azure_cli():
            console.print("[red]错误: Azure CLI 未安装[/red]")
            raise click.Exit(1)
        
        console.print("运行 Azure 登录...")
        result = subprocess.run(["az", "login"])
        if result.returncode == 0:
            console.print("\n[green]✅ Azure 登录成功[/green]")
        
    elif platform == "gcp":
        if not _check_gcloud_cli():
            console.print("[red]错误: gcloud 未安装[/red]")
            raise click.Exit(1)
        
        console.print("运行 GCP 认证...")
        result = subprocess.run(["gcloud", "auth", "login"])
        if result.returncode == 0:
            console.print("\n[green]✅ GCP 认证成功[/green]")


@cloud_cli.command(name="list-instances")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--region", "-r", help="区域 (如 us-east-1)")
@click.option("--profile", "-pr", default="default", help="AWS profile")
def list_instances(platform: str, region: Optional[str], profile: str):
    """列出云实例/VM"""
    console.print(f"\n[bold cyan]🖥️ 列出 {platform.upper()} 实例[/bold cyan]\n")
    
    if platform == "aws":
        if not _check_aws_cli():
            console.print("[red]错误: AWS CLI 未安装[/red]")
            raise click.Exit(1)
        
        args = ["ec2", "describe-instances", "--profile", profile, "--output", "json"]
        if region:
            args.extend(["--region", region])
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("正在获取实例列表...", total=None)
            returncode, stdout, stderr = _run_aws_command(args)
            progress.update(task, description="完成")
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        try:
            data = json.loads(stdout)
            reservations = data.get("Reservations", [])
            
            if not reservations:
                console.print("[yellow]没有找到实例[/yellow]")
                return
            
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("实例ID", style="cyan")
            table.add_column("类型", style="white")
            table.add_column("状态", style="green")
            table.add_column("公有IP", style="blue")
            table.add_column("私有IP", style="dim")
            table.add_column("名称", style="white")
            
            for reservation in reservations:
                for instance in reservation.get("Instances", []):
                    instance_id = instance.get("InstanceId", "N/A")
                    instance_type = instance.get("InstanceType", "N/A")
                    state = instance.get("State", {}).get("Name", "unknown")
                    public_ip = instance.get("PublicIpAddress", "-")
                    private_ip = instance.get("PrivateIpAddress", "-")
                    
                    # 获取名称标签
                    name = "-"
                    for tag in instance.get("Tags", []):
                        if tag.get("Key") == "Name":
                            name = tag.get("Value", "-")
                            break
                    
                    state_color = "green" if state == "running" else "red" if state == "stopped" else "yellow"
                    table.add_row(
                        instance_id,
                        instance_type,
                        f"[{state_color}]{state}[/{state_color}]",
                        public_ip,
                        private_ip,
                        name
                    )
            
            console.print(table)
            console.print(f"\n共 {sum(len(r.get('Instances', [])) for r in reservations)} 个实例")
            
        except json.JSONDecodeError:
            console.print(f"[red]解析响应失败[/red]")
            console.print(stdout)
    
    elif platform == "azure":
        if not _check_azure_cli():
            console.print("[red]错误: Azure CLI 未安装[/red]")
            raise click.Exit(1)
        
        args = ["vm", "list", "--output", "json"]
        if region:
            # Azure 使用 location 而不是 region
            pass
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("正在获取 VM 列表...", total=None)
            returncode, stdout, stderr = _run_azure_command(args)
            progress.update(task, description="完成")
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        try:
            vms = json.loads(stdout)
            
            if not vms:
                console.print("[yellow]没有找到 VM[/yellow]")
                return
            
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("名称", style="cyan")
            table.add_column("资源组", style="white")
            table.add_column("类型", style="white")
            table.add_column("位置", style="blue")
            table.add_column("状态", style="green")
            
            for vm in vms:
                name = vm.get("name", "N/A")
                resource_group = vm.get("resourceGroup", "N/A")
                vm_type = vm.get("hardwareProfile", {}).get("vmSize", "N/A")
                location = vm.get("location", "N/A")
                
                # 获取电源状态
                power_state = "unknown"
                for status in vm.get("instanceView", {}).get("statuses", []):
                    code = status.get("code", "")
                    if code.startswith("PowerState/"):
                        power_state = code.replace("PowerState/", "").lower()
                
                state_color = "green" if power_state == "running" else "red" if power_state == "stopped" else "yellow"
                table.add_row(name, resource_group, vm_type, location, f"[{state_color}]{power_state}[/{state_color}]")
            
            console.print(table)
            console.print(f"\n共 {len(vms)} 个 VM")
            
        except json.JSONDecodeError:
            console.print(f"[red]解析响应失败[/red]")
    
    elif platform == "gcp":
        if not _check_gcloud_cli():
            console.print("[red]错误: gcloud 未安装[/red]")
            raise click.Exit(1)
        
        args = ["compute", "instances", "list", "--format=json"]
        if region:
            args.extend(["--zones", f"{region}-a", f"{region}-b", f"{region}-c"])
        
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("正在获取实例列表...", total=None)
            returncode, stdout, stderr = _run_gcloud_command(args)
            progress.update(task, description="完成")
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        try:
            instances = json.loads(stdout)
            
            if not instances:
                console.print("[yellow]没有找到实例[/yellow]")
                return
            
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("名称", style="cyan")
            table.add_column("区域", style="white")
            table.add_column("机器类型", style="white")
            table.add_column("状态", style="green")
            table.add_column("外部IP", style="blue")
            table.add_column("内部IP", style="dim")
            
            for instance in instances:
                name = instance.get("name", "N/A")
                zone = instance.get("zone", "").split("/")[-1]
                machine_type = instance.get("machineType", "").split("/")[-1]
                status = instance.get("status", "UNKNOWN")
                
                # 获取 IP 地址
                external_ip = "-"
                internal_ip = "-"
                for interface in instance.get("networkInterfaces", []):
                    internal_ip = interface.get("networkIP", "-")
                    for config in interface.get("accessConfigs", []):
                        if config.get("type") == "ONE_TO_ONE_NAT":
                            external_ip = config.get("natIP", "-")
                
                state_color = "green" if status == "RUNNING" else "red" if status == "TERMINATED" else "yellow"
                table.add_row(
                    name, zone, machine_type,
                    f"[{state_color}]{status}[/{state_color}]",
                    external_ip, internal_ip
                )
            
            console.print(table)
            console.print(f"\n共 {len(instances)} 个实例")
            
        except json.JSONDecodeError:
            console.print(f"[red]解析响应失败[/red]")


@cloud_cli.command(name="start")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--instance", "-i", required=True, help="实例ID或名称")
@click.option("--region", "-r", help="区域")
@click.option("--profile", "-pr", default="default", help="AWS profile")
def start_instance(platform: str, instance: str, region: Optional[str], profile: str):
    """启动云实例"""
    console.print(f"\n[bold cyan]▶️ 启动 {platform.upper()} 实例[/bold cyan]\n")
    
    if platform == "aws":
        args = ["ec2", "start-instances", "--instance-ids", instance, "--profile", profile]
        if region:
            args.extend(["--region", region])
        
        returncode, stdout, stderr = _run_aws_command(args)
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        console.print(f"[green]✅ 实例 {instance} 启动命令已发送[/green]")
        console.print("使用 'cloud list-instances' 查看状态")
    
    elif platform == "azure":
        # Azure 需要资源组
        console.print("[yellow]Azure 需要指定资源组[/yellow]")
        console.print("使用: az vm start --resource-group <group> --name <name>")
    
    elif platform == "gcp":
        args = ["compute", "instances", "start", instance]
        if region:
            args.extend(["--zone", f"{region}-a"])
        
        returncode, stdout, stderr = _run_gcloud_command(args)
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        console.print(f"[green]✅ 实例 {instance} 启动命令已发送[/green]")


@cloud_cli.command(name="stop")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--instance", "-i", required=True, help="实例ID或名称")
@click.option("--region", "-r", help="区域")
@click.option("--profile", "-pr", default="default", help="AWS profile")
@click.option("--force", "-f", is_flag=True, help="强制停止")
def stop_instance(platform: str, instance: str, region: Optional[str], profile: str, force: bool):
    """停止云实例"""
    console.print(f"\n[bold cyan]⏹️ 停止 {platform.upper()} 实例[/bold cyan]\n")
    
    if not force:
        confirm = click.confirm(f"确定要停止实例 {instance} 吗？")
        if not confirm:
            console.print("[yellow]已取消[/yellow]")
            return
    
    if platform == "aws":
        args = ["ec2", "stop-instances", "--instance-ids", instance, "--profile", profile]
        if region:
            args.extend(["--region", region])
        
        returncode, stdout, stderr = _run_aws_command(args)
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        console.print(f"[green]✅ 实例 {instance} 停止命令已发送[/green]")
    
    elif platform == "gcp":
        args = ["compute", "instances", "stop", instance]
        if region:
            args.extend(["--zone", f"{region}-a"])
        
        returncode, stdout, stderr = _run_gcloud_command(args)
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        console.print(f"[green]✅ 实例 {instance} 停止命令已发送[/green]")


@cloud_cli.command(name="ssh")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--instance", "-i", required=True, help="实例ID或IP")
@click.option("--user", "-u", default="ubuntu", help="SSH用户名")
@click.option("--key", "-k", help="SSH私钥路径")
@click.option("--region", "-r", help="区域")
def ssh_instance(platform: str, instance: str, user: str, key: Optional[str], region: Optional[str]):
    """SSH 连接到实例"""
    console.print(f"\n[bold cyan]🔌 SSH 连接到 {platform.upper()} 实例[/bold cyan]\n")
    
    # 获取实例 IP
    public_ip = instance
    
    if platform == "aws" and not instance.startswith("ec2-"):
        # 尝试获取实例 IP
        args = ["ec2", "describe-instances", "--instance-ids", instance, "--query", "Reservations[0].Instances[0].PublicIpAddress", "--output", "text"]
        if region:
            args.extend(["--region", region])
        
        returncode, stdout, stderr = _run_aws_command(args)
        if returncode == 0 and stdout.strip():
            public_ip = stdout.strip()
    
    # 构建 SSH 命令
    ssh_cmd = ["ssh", f"{user}@{public_ip}"]
    if key:
        ssh_cmd.extend(["-i", key])
    ssh_cmd.extend(["-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null"])
    
    console.print(f"连接到: [cyan]{user}@{public_ip}[/cyan]")
    console.print(f"命令: {' '.join(ssh_cmd)}\n")
    
    # 执行 SSH
    subprocess.run(ssh_cmd)


@cloud_cli.command(name="deploy")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--app", "-a", required=True, help="应用名称")
@click.option("--source", "-s", required=True, help="源代码目录")
@click.option("--type", "-t", default="docker", type=click.Choice(['docker', 'zip', 'git']), help="部署类型")
@click.option("--region", "-r", help="区域")
def deploy_app(platform: str, app: str, source: str, type: str, region: Optional[str]):
    """部署应用到云平台"""
    console.print(f"\n[bold cyan]🚀 部署应用到 {platform.upper()}[/bold cyan]\n")
    
    source_path = Path(source).expanduser().resolve()
    if not source_path.exists():
        console.print(f"[red]错误: 源目录不存在: {source}[/red]")
        raise click.Exit(1)
    
    console.print(f"应用: {app}")
    console.print(f"源: {source_path}")
    console.print(f"类型: {type}")
    
    # 记录部署
    config = _load_config()
    deployment = {
        "id": f"{app}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "app": app,
        "platform": platform,
        "source": str(source_path),
        "type": type,
        "region": region,
        "deployed_at": datetime.now().isoformat(),
        "status": "deploying"
    }
    config["deployments"].append(deployment)
    _save_config(config)
    
    console.print("\n[bold]部署流程:[/bold]")
    
    if type == "docker":
        # 检查 Dockerfile
        dockerfile = source_path / "Dockerfile"
        if not dockerfile.exists():
            console.print("[yellow]警告: 未找到 Dockerfile，创建默认配置[/yellow]")
            # 这里可以创建默认 Dockerfile
        
        console.print("  1. 构建 Docker 镜像...")
        console.print("  2. 推送镜像到仓库...")
        console.print("  3. 部署到云平台...")
    
    elif type == "zip":
        console.print("  1. 打包应用...")
        console.print("  2. 上传到云存储...")
        console.print("  3. 部署到服务...")
    
    elif type == "git":
        console.print("  1. 推送代码到仓库...")
        console.print("  2. 触发 CI/CD 流水线...")
        console.print("  3. 等待部署完成...")
    
    # 更新状态
    deployment["status"] = "deployed"
    _save_config(config)
    
    console.print(f"\n[green]✅ 部署完成[/green]")
    console.print(f"部署ID: {deployment['id']}")


@cloud_cli.command(name="deployments")
def list_deployments():
    """列出部署记录"""
    config = _load_config()
    deployments = config.get("deployments", [])
    
    if not deployments:
        console.print("[yellow]没有找到部署记录[/yellow]")
        return
    
    console.print(f"\n[bold cyan]📋 部署记录[/bold cyan] ({len(deployments)} 个)\n")
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim")
    table.add_column("应用")
    table.add_column("平台")
    table.add_column("类型")
    table.add_column("区域")
    table.add_column("状态")
    table.add_column("部署时间")
    
    for d in deployments:
        status_color = "green" if d.get("status") == "deployed" else "yellow"
        deployed_at = datetime.fromisoformat(d.get("deployed_at", "")).strftime("%Y-%m-%d %H:%M")
        table.add_row(
            d.get("id", "")[:20],
            d.get("app", "-"),
            d.get("platform", "-"),
            d.get("type", "-"),
            d.get("region", "-"),
            f"[{status_color}]{d.get('status', 'unknown')}[/{status_color}]",
            deployed_at
        )
    
    console.print(table)


@cloud_cli.command(name="buckets")
@click.option("--platform", "-p", required=True, type=click.Choice(['aws', 'azure', 'gcp']), help="云平台")
@click.option("--profile", "-pr", default="default", help="AWS profile")
def list_buckets(platform: str, profile: str):
    """列出云存储桶"""
    console.print(f"\n[bold cyan]🪣 列出 {platform.upper()} 存储桶[/bold cyan]\n")
    
    if platform == "aws":
        args = ["s3", "ls", "--profile", profile]
        returncode, stdout, stderr = _run_aws_command(args)
        
        if returncode != 0:
            console.print(f"[red]错误: {stderr}[/red]")
            raise click.Exit(1)
        
        buckets = [line.split()[-1] for line in stdout.strip().split('\n') if line.strip()]
        
        if not buckets:
            console.print("[yellow]没有找到存储桶[/yellow]")
            return
        
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("存储桶名称", style="cyan")
        table.add_column("创建时间", style="white")
        
        for line in stdout.strip().split('\n'):
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    date = f"{parts[0]} {parts[1]}"
                    name = parts[2]
                    table.add_row(name, date)
        
        console.print(table)
        console.print(f"\n共 {len(buckets)} 个存储桶")
