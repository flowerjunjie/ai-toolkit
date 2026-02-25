"""
批处理工具 - 真实实现版
支持真实的批量文件处理、批处理脚本执行、并行任务处理
"""

import click
import os
import subprocess
import shutil
import fnmatch
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree

console = Console()


@click.group(name="batch")
def batch_cli():
    """批处理工具 - 批量文件处理、脚本执行、并行任务"""
    pass


def run_command(cmd: List[str], cwd: Optional[str] = None) -> tuple:
    """运行shell命令"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


def get_files_by_pattern(directory: str, pattern: str, recursive: bool = True) -> List[Path]:
    """根据模式获取文件列表"""
    base_path = Path(directory)
    files = []
    
    if recursive:
        for path in base_path.rglob("*"):
            if path.is_file() and fnmatch.fnmatch(path.name, pattern):
                files.append(path)
    else:
        for path in base_path.glob(pattern):
            if path.is_file():
                files.append(path)
    
    return sorted(files)


@batch_cli.command(name="run")
@click.option("--script", "-s", required=True, help="要执行的脚本或命令")
@click.option("--input", "-i", help="输入目录")
@click.option("--pattern", "-p", default="*", help="文件匹配模式")
@click.option("--workers", "-w", default=4, help="并行工作数")
@click.option("--recursive/--no-recursive", default=True, help="递归处理子目录")
@click.option("--dry-run", is_flag=True, help="仅预览不执行")
def run_batch(script: str, input: Optional[str], pattern: str, workers: int, recursive: bool, dry_run: bool):
    """批量执行脚本处理文件"""
    console.print(f"\n⚡ 批量执行\n")
    
    # 获取文件列表
    if input:
        files = get_files_by_pattern(input, pattern, recursive)
        console.print(f"输入目录: {input}")
        console.print(f"匹配模式: {pattern}")
        console.print(f"找到文件: {len(files)}个")
    else:
        files = []
        console.print(f"脚本: {script}")
        console.print("模式: 直接执行脚本（无输入文件）")
    
    console.print(f"并行数: {workers}")
    console.print(f"Dry-run: {dry_run}")
    console.print("")
    
    if dry_run:
        console.print("[yellow]Dry-run模式，仅预览:[/yellow]\n")
        if files:
            for f in files[:10]:
                console.print(f"  将处理: {f}")
            if len(files) > 10:
                console.print(f"  ... 还有 {len(files) - 10} 个文件")
        else:
            console.print(f"  将执行: {script}")
        return
    
    # 执行处理
    results = {"success": 0, "failed": 0, "errors": []}
    
    if files:
        # 文件批处理模式
        def process_file(file_path: Path) -> tuple:
            try:
                # 替换脚本中的占位符
                cmd = script.format(file=str(file_path), filename=file_path.name, stem=file_path.stem)
                cmd_parts = cmd.split() if " " in cmd else [cmd]
                
                result = subprocess.run(
                    cmd_parts,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                return file_path, result.returncode == 0, result.stdout, result.stderr
            except Exception as e:
                return file_path, False, "", str(e)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"处理 {len(files)} 个文件...", total=len(files))
            
            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(process_file, f): f for f in files}
                
                for future in as_completed(futures):
                    file_path, success, stdout, stderr = future.result()
                    progress.update(task, advance=1)
                    
                    if success:
                        results["success"] += 1
                    else:
                        results["failed"] += 1
                        results["errors"].append((str(file_path), stderr[:100]))
    else:
        # 直接执行脚本模式
        console.print(f"执行: {script}")
        success, stdout, stderr = run_command(script.split())
        
        if success:
            results["success"] = 1
            console.print(f"[green]✓ 成功[/green]")
            if stdout:
                console.print(stdout[:500])
        else:
            results["failed"] = 1
            console.print(f"[red]✗ 失败: {stderr}[/red]")
    
    # 显示结果
    console.print(f"\n📊 执行结果:")
    console.print(f"  成功: {results['success']}")
    console.print(f"  失败: {results['failed']}")
    
    if results["errors"]:
        console.print("\n[red]错误详情:[/red]")
        for path, error in results["errors"][:5]:
            console.print(f"  {path}: {error}")


@batch_cli.command(name="rename")
@click.option("--pattern", "-p", required=True, help="匹配模式 (如: *.txt)")
@click.option("--replacement", "-r", required=True, help="替换模式 (如: new_{stem}.txt)")
@click.option("--directory", "-d", default=".", help="目标目录")
@click.option("--recursive/--no-recursive", default=False, help="递归处理")
@click.option("--dry-run", is_flag=True, help="仅预览")
def batch_rename(pattern: str, replacement: str, directory: str, recursive: bool, dry_run: bool):
    """批量重命名文件"""
    console.print(f"\n🔄 批量重命名\n")
    
    files = get_files_by_pattern(directory, pattern, recursive)
    
    console.print(f"目录: {directory}")
    console.print(f"匹配: {pattern}")
    console.print(f"找到: {len(files)}个文件")
    console.print(f"Dry-run: {dry_run}\n")
    
    if not files:
        console.print("[yellow]未找到匹配的文件[/yellow]")
        return
    
    # 预览重命名
    renames = []
    for file_path in files:
        # 支持的占位符: {stem}, {ext}, {name}, {parent}
        new_name = replacement.format(
            stem=file_path.stem,
            ext=file_path.suffix.lstrip("."),
            name=file_path.name,
            parent=file_path.parent.name
        )
        new_path = file_path.parent / new_name
        renames.append((file_path, new_path))
    
    # 显示预览
    table = Table(title="重命名预览")
    table.add_column("原文件名", style="cyan")
    table.add_column("新文件名", style="green")
    
    for old, new in renames[:20]:
        table.add_row(str(old.relative_to(directory)), str(new.relative_to(directory)))
    
    if len(renames) > 20:
        table.add_row("...", f"还有 {len(renames) - 20} 个文件")
    
    console.print(table)
    
    if dry_run:
        console.print("\n[yellow]Dry-run模式，未实际执行[/yellow]")
        return
    
    # 确认
    if not click.confirm("\n确认执行重命名?"):
        console.print("已取消")
        return
    
    # 执行重命名
    success_count = 0
    for old_path, new_path in renames:
        try:
            old_path.rename(new_path)
            success_count += 1
        except Exception as e:
            console.print(f"[red]✗ 失败 {old_path}: {e}[/red]")
    
    console.print(f"\n[green]✅ 成功重命名 {success_count}/{len(renames)} 个文件[/green]")


@batch_cli.command(name="copy")
@click.option("--source", "-s", required=True, help="源目录")
@click.option("--dest", "-d", required=True, help="目标目录")
@click.option("--pattern", "-p", default="*", help="文件匹配模式")
@click.option("--preserve/--no-preserve", default=True, help="保留文件属性")
@click.option("--dry-run", is_flag=True, help="仅预览")
def batch_copy(source: str, dest: str, pattern: str, preserve: bool, dry_run: bool):
    """批量复制文件"""
    console.print(f"\n📋 批量复制\n")
    
    source_path = Path(source)
    dest_path = Path(dest)
    
    if not source_path.exists():
        console.print(f"[red]源目录不存在: {source}[/red]")
        return
    
    files = get_files_by_pattern(source, pattern, recursive=True)
    
    console.print(f"源: {source}")
    console.print(f"目标: {dest}")
    console.print(f"匹配: {pattern}")
    console.print(f"文件数: {len(files)}")
    console.print(f"Dry-run: {dry_run}\n")
    
    if dry_run:
        for f in files[:10]:
            rel_path = f.relative_to(source_path)
            target = dest_path / rel_path
            console.print(f"  {rel_path} -> {target}")
        if len(files) > 10:
            console.print(f"  ... 还有 {len(files) - 10} 个文件")
        return
    
    # 执行复制
    copied = 0
    failed = 0
    
    with Progress(console=console) as progress:
        task = progress.add_task("复制中...", total=len(files))
        
        for file_path in files:
            try:
                rel_path = file_path.relative_to(source_path)
                target_path = dest_path / rel_path
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                if preserve:
                    shutil.copy2(file_path, target_path)
                else:
                    shutil.copy(file_path, target_path)
                
                copied += 1
            except Exception as e:
                failed += 1
                console.print(f"[red]✗ {file_path}: {e}[/red]")
            
            progress.update(task, advance=1)
    
    console.print(f"\n[green]✅ 复制完成: {copied} 成功, {failed} 失败[/green]")


@batch_cli.command(name="delete")
@click.option("--pattern", "-p", required=True, help="匹配模式")
@click.option("--directory", "-d", default=".", help="目标目录")
@click.option("--recursive/--no-recursive", default=False, help="递归处理")
@click.option("--dry-run", is_flag=True, help="仅预览")
@click.confirmation_option(prompt="确定要删除匹配的文件吗?")
def batch_delete(pattern: str, directory: str, recursive: bool, dry_run: bool):
    """批量删除文件"""
    console.print(f"\n🗑️ 批量删除\n")
    
    files = get_files_by_pattern(directory, pattern, recursive)
    
    console.print(f"目录: {directory}")
    console.print(f"匹配: {pattern}")
    console.print(f"找到: {len(files)}个文件")
    console.print(f"Dry-run: {dry_run}\n")
    
    if not files:
        console.print("[yellow]未找到匹配的文件[/yellow]")
        return
    
    # 显示将要删除的文件
    for f in files[:20]:
        console.print(f"  [red]删除: {f}[/red]")
    
    if len(files) > 20:
        console.print(f"  ... 还有 {len(files) - 20} 个文件")
    
    if dry_run:
        console.print("\n[yellow]Dry-run模式，未实际删除[/yellow]")
        return
    
    # 执行删除
    deleted = 0
    failed = 0
    
    for file_path in files:
        try:
            file_path.unlink()
            deleted += 1
        except Exception as e:
            failed += 1
            console.print(f"[red]✗ {file_path}: {e}[/red]")
    
    console.print(f"\n[green]✅ 删除完成: {deleted} 成功, {failed} 失败[/green]")


@batch_cli.command(name="convert")
@click.option("--input", "-i", required=True, help="输入目录")
@click.option("--output", "-o", required=True, help="输出目录")
@click.option("--from", "from_fmt", required=True, help="源格式 (如: jpg, png)")
@click.option("--to", "to_fmt", required=True, help="目标格式 (如: png, webp)")
@click.option("--workers", "-w", default=4, help="并行数")
@click.option("--quality", "-q", default=85, help="输出质量 (1-100)")
def batch_convert(input: str, output: str, from_fmt: str, to_fmt: str, workers: int, quality: int):
    """批量转换文件格式（图片、文档等）"""
    console.print(f"\n🔄 批量格式转换\n")
    
    input_path = Path(input)
    output_path = Path(output)
    
    if not input_path.exists():
        console.print(f"[red]输入目录不存在: {input}[/red]")
        return
    
    # 获取匹配文件
    pattern = f"*.{from_fmt}"
    files = get_files_by_pattern(input, pattern, recursive=True)
    
    console.print(f"输入: {input}")
    console.print(f"输出: {output}")
    console.print(f"转换: {from_fmt} -> {to_fmt}")
    console.print(f"文件数: {len(files)}")
    console.print(f"并行数: {workers}\n")
    
    if not files:
        console.print("[yellow]未找到匹配的文件[/yellow]")
        return
    
    # 检查转换工具
    if from_fmt in ["jpg", "jpeg", "png", "gif", "bmp", "webp"]:
        # 图片转换
        has_pil = False
        try:
            from PIL import Image
            has_pil = True
        except ImportError:
            pass
        
        if not has_pil:
            console.print("[yellow]警告: 未安装Pillow，尝试安装...[/yellow]")
            run_command(["pip", "install", "Pillow"])
            from PIL import Image
        
        def convert_image(file_path: Path) -> tuple:
            try:
                rel_path = file_path.relative_to(input_path)
                target_path = output_path / rel_path.with_suffix(f".{to_fmt}")
                target_path.parent.mkdir(parents=True, exist_ok=True)
                
                with Image.open(file_path) as img:
                    if img.mode in ('RGBA', 'P') and to_fmt in ['jpg', 'jpeg']:
                        img = img.convert('RGB')
                    
                    save_kwargs = {}
                    if to_fmt in ['jpg', 'jpeg']:
                        save_kwargs['quality'] = quality
                        save_kwargs['optimize'] = True
                    elif to_fmt == 'png':
                        save_kwargs['optimize'] = True
                    elif to_fmt == 'webp':
                        save_kwargs['quality'] = quality
                    
                    img.save(target_path, **save_kwargs)
                
                return file_path, True, ""
            except Exception as e:
                return file_path, False, str(e)
        
        convert_func = convert_image
    else:
        console.print(f"[yellow]暂不支持 {from_fmt} 格式的自动转换[/yellow]")
        console.print("支持的图片格式: jpg, png, gif, bmp, webp")
        return
    
    # 执行转换
    success_count = 0
    failed_count = 0
    
    with Progress(console=console) as progress:
        task = progress.add_task("转换中...", total=len(files))
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(convert_func, f): f for f in files}
            
            for future in as_completed(futures):
                file_path, success, error = future.result()
                progress.update(task, advance=1)
                
                if success:
                    success_count += 1
                else:
                    failed_count += 1
                    console.print(f"[red]✗ {file_path}: {error}[/red]")
    
    console.print(f"\n[green]✅ 转换完成: {success_count} 成功, {failed_count} 失败[/green]")


@batch_cli.command(name="find-dup")
@click.option("--directory", "-d", required=True, help="要扫描的目录")
@click.option("--recursive/--no-recursive", default=True, help="递归扫描")
@click.option("--delete", is_flag=True, help="删除重复文件")
def find_duplicates(directory: str, recursive: bool, delete: bool):
    """查找重复文件"""
    console.print(f"\n🔍 查找重复文件\n")
    
    import hashlib
    
    dir_path = Path(directory)
    if not dir_path.exists():
        console.print(f"[red]目录不存在: {directory}[/red]")
        return
    
    # 收集文件
    files = []
    if recursive:
        files = [f for f in dir_path.rglob("*") if f.is_file()]
    else:
        files = [f for f in dir_path.iterdir() if f.is_file()]
    
    console.print(f"扫描文件数: {len(files)}")
    
    # 计算文件哈希
    file_hashes = {}
    
    with Progress(console=console) as progress:
        task = progress.add_task("计算哈希...", total=len(files))
        
        for file_path in files:
            try:
                # 使用文件大小+前4KB+后4KB的哈希作为快速指纹
                stat = file_path.stat()
                size = stat.st_size
                
                if size == 0:
                    file_hash = "empty"
                else:
                    hasher = hashlib.md5()
                    hasher.update(str(size).encode())
                    
                    with open(file_path, 'rb') as f:
                        # 读取前4KB
                        hasher.update(f.read(4096))
                        # 读取后4KB
                        if size > 8192:
                            f.seek(-4096, 2)
                            hasher.update(f.read())
                    
                    file_hash = hasher.hexdigest()
                
                if file_hash not in file_hashes:
                    file_hashes[file_hash] = []
                file_hashes[file_hash].append(file_path)
                
            except Exception as e:
                console.print(f"[red]✗ {file_path}: {e}[/red]")
            
            progress.update(task, advance=1)
    
    # 找出重复
    duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}
    
    if not duplicates:
        console.print("\n[green]✅ 未发现重复文件[/green]")
        return
    
    # 显示结果
    total_dup_files = sum(len(files) - 1 for files in duplicates.values())
    console.print(f"\n[yellow]发现 {len(duplicates)} 组重复文件，共 {total_dup_files} 个重复[/yellow]\n")
    
    for file_hash, dup_files in duplicates.items():
        console.print(f"[cyan]哈希: {file_hash[:16]}...[/cyan]")
        for i, f in enumerate(dup_files):
            marker = "[green]✓ 保留[/green]" if i == 0 else "[red]✗ 重复[/red]"
            size = f.stat().st_size
            console.print(f"  {marker} {f} ({size // 1024}KB)")
        console.print("")
    
    if delete:
        deleted = 0
        saved_space = 0
        
        for dup_files in duplicates.values():
            for f in dup_files[1:]:  # 保留第一个
                try:
                    size = f.stat().st_size
                    f.unlink()
                    deleted += 1
                    saved_space += size
                except Exception as e:
                    console.print(f"[red]✗ 删除失败 {f}: {e}[/red]")
        
        console.print(f"\n[green]✅ 已删除 {deleted} 个重复文件，节省 {saved_space // 1024 // 1024}MB[/green]")


@batch_cli.command(name="stats")
@click.option("--directory", "-d", default=".", help="目标目录")
@click.option("--recursive/--no-recursive", default=True, help="递归统计")
def batch_stats(directory: str, recursive: bool):
    """批量统计文件信息"""
    console.print(f"\n📊 文件统计\n")
    
    dir_path = Path(directory)
    if not dir_path.exists():
        console.print(f"[red]目录不存在: {directory}[/red]")
        return
    
    # 收集文件
    files = []
    if recursive:
        files = [f for f in dir_path.rglob("*") if f.is_file()]
    else:
        files = [f for f in dir_path.iterdir() if f.is_file()]
    
    # 统计
    total_size = 0
    type_count = {}
    size_ranges = {
        "0-1KB": 0,
        "1KB-1MB": 0,
        "1MB-10MB": 0,
        "10MB-100MB": 0,
        "100MB+": 0
    }
    
    for f in files:
        try:
            stat = f.stat()
            size = stat.st_size
            total_size += size
            
            # 文件类型
            ext = f.suffix.lower() or "(无扩展名)"
            type_count[ext] = type_count.get(ext, 0) + 1
            
            # 大小范围
            if size < 1024:
                size_ranges["0-1KB"] += 1
            elif size < 1024 * 1024:
                size_ranges["1KB-1MB"] += 1
            elif size < 10 * 1024 * 1024:
                size_ranges["1MB-10MB"] += 1
            elif size < 100 * 1024 * 1024:
                size_ranges["10MB-100MB"] += 1
            else:
                size_ranges["100MB+"] += 1
                
        except Exception:
            pass
    
    # 显示结果
    console.print(f"目录: {directory}")
    console.print(f"总文件数: {len(files)}")
    console.print(f"总大小: {total_size // 1024 // 1024}MB ({total_size} bytes)\n")
    
    # 文件类型统计
    table = Table(title="文件类型分布")
    table.add_column("扩展名", style="cyan")
    table.add_column("数量", style="green", justify="right")
    table.add_column("占比", style="yellow")
    
    for ext, count in sorted(type_count.items(), key=lambda x: x[1], reverse=True)[:15]:
        pct = count / len(files) * 100 if files else 0
        table.add_row(ext, str(count), f"{pct:.1f}%")
    
    console.print(table)
    console.print("")
    
    # 大小分布
    table2 = Table(title="文件大小分布")
    table2.add_column("大小范围", style="cyan")
    table2.add_column("数量", style="green", justify="right")
    
    for range_name, count in size_ranges.items():
        if count > 0:
            table2.add_row(range_name, str(count))
    
    console.print(table2)


if __name__ == "__main__":
    batch_cli()
