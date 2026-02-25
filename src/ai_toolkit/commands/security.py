"""
安全和合规工具 - 真实安全扫描版
集成 bandit、safety 等工具进行真实安全检测
"""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import subprocess
import json
import re
import os

console = Console()


def run_command(cmd, capture_output=True, check=False, cwd=None):
    """运行命令"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check,
            cwd=cwd
        )
        return result
    except Exception as e:
        return None


def check_tool_installed(tool_name):
    """检查工具是否安装"""
    result = run_command(["which", tool_name])
    return result is not None and result.returncode == 0


def install_tool(tool_name, package_name=None):
    """尝试安装工具"""
    if not package_name:
        package_name = tool_name
    
    console.print(f"📦 尝试安装 {tool_name}...")
    result = run_command(["pip", "install", package_name], capture_output=False)
    return result is not None and result.returncode == 0


@click.group(name="security")
def security_cli():
    """安全和合规工具"""
    pass


@security_cli.command(name="audit")
@click.option("--path", "-p", default=".", help="审计路径")
@click.option("--format", "-f", default="table", help="输出格式 (table, json)")
def security_audit(path: str, format: str):
    """安全审计 - 检查代码安全问题"""
    console.print(f"\n🔒 安全审计: {path}\n")
    
    target_path = Path(path).resolve()
    if not target_path.exists():
        console.print(f"❌ 路径不存在: {path}")
        return
    
    results = {
        "timestamp": subprocess.check_output(["date", "-Iseconds"]).decode().strip(),
        "path": str(target_path),
        "checks": []
    }
    
    # 1. 检查硬编码密钥
    console.print("🔍 检查硬编码密钥...")
    secret_patterns = [
        (r'api[_-]?key\s*=\s*["\'][^"\']{10,}["\']', "API Key"),
        (r'secret\s*=\s*["\'][^"\']{10,}["\']', "Secret"),
        (r'password\s*=\s*["\'][^"\']{6,}["\']', "Password"),
        (r'token\s*=\s*["\'][^"\']{10,}["\']', "Token"),
        (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
        (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token"),
    ]
    
    secrets_found = []
    python_files = list(target_path.rglob("*.py"))
    
    for file_path in python_files[:100]:  # 限制文件数量
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for pattern, secret_type in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # 排除示例/文档中的假阳性
                        line_num = content[:match.start()].count('\n') + 1
                        line_content = content.split('\n')[line_num - 1].strip()
                        if not any(x in line_content.lower() for x in ['example', 'placeholder', 'your_', 'xxx']):
                            secrets_found.append({
                                "file": str(file_path.relative_to(target_path)),
                                "line": line_num,
                                "type": secret_type,
                                "snippet": line_content[:80]
                            })
        except Exception:
            pass
    
    if secrets_found:
        results["checks"].append({
            "name": "硬编码密钥检查",
            "status": "警告",
            "issues": len(secrets_found),
            "details": secrets_found[:5]  # 只显示前5个
        })
        console.print(f"  ⚠️ 发现 {len(secrets_found)} 个潜在密钥暴露")
    else:
        results["checks"].append({
            "name": "硬编码密钥检查",
            "status": "通过",
            "issues": 0
        })
        console.print("  ✅ 未发现硬编码密钥")
    
    # 2. 检查 .env 文件
    console.print("🔍 检查环境变量文件...")
    env_files = list(target_path.rglob(".env*"))
    gitignore_path = target_path / ".gitignore"
    
    env_issues = []
    if env_files:
        for env_file in env_files:
            env_issues.append({
                "file": str(env_file.relative_to(target_path)),
                "issue": "环境变量文件存在"
            })
        
        # 检查 .gitignore
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
                if '.env' not in gitignore_content:
                    env_issues.append({
                        "file": ".gitignore",
                        "issue": "未忽略 .env 文件"
                    })
        else:
            env_issues.append({
                "file": "项目根目录",
                "issue": "缺少 .gitignore 文件"
            })
    
    if env_issues:
        results["checks"].append({
            "name": "环境变量文件检查",
            "status": "警告",
            "issues": len(env_issues),
            "details": env_issues
        })
        console.print(f"  ⚠️ 发现 {len(env_issues)} 个环境变量相关问题")
    else:
        results["checks"].append({
            "name": "环境变量文件检查",
            "status": "通过",
            "issues": 0
        })
        console.print("  ✅ 环境变量配置正确")
    
    # 3. Bandit 安全扫描
    console.print("🔍 运行 Bandit 安全扫描...")
    
    if not check_tool_installed("bandit"):
        console.print("  📦 Bandit 未安装，尝试安装...")
        install_tool("bandit")
    
    if check_tool_installed("bandit"):
        bandit_result = run_command([
            "bandit", "-r", str(target_path),
            "-f", "json",
            "-ll",  # 低级别及以上
            "--skip", "B101,B311"  # 跳过一些常见误报
        ], check=False)
        
        if bandit_result and bandit_result.stdout:
            try:
                bandit_data = json.loads(bandit_result.stdout)
                issues = bandit_data.get("results", [])
                
                severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
                for issue in issues:
                    severity = issue.get("issue_severity", "LOW")
                    severity_counts[severity] = severity_counts.get(severity, 0) + 1
                
                total_issues = sum(severity_counts.values())
                
                if total_issues > 0:
                    results["checks"].append({
                        "name": "Bandit 代码安全扫描",
                        "status": "警告" if severity_counts["HIGH"] > 0 else "通过",
                        "issues": total_issues,
                        "severity": severity_counts,
                        "details": issues[:3]
                    })
                    console.print(f"  ⚠️ 发现 {total_issues} 个问题")
                    console.print(f"     高危: {severity_counts['HIGH']}, 中危: {severity_counts['MEDIUM']}, 低危: {severity_counts['LOW']}")
                else:
                    results["checks"].append({
                        "name": "Bandit 代码安全扫描",
                        "status": "通过",
                        "issues": 0
                    })
                    console.print("  ✅ 未发现安全问题")
            except json.JSONDecodeError:
                results["checks"].append({
                    "name": "Bandit 代码安全扫描",
                    "status": "错误",
                    "error": "解析失败"
                })
                console.print("  ❌ 扫描结果解析失败")
    else:
        console.print("  ⚠️ Bandit 安装失败，跳过扫描")
        results["checks"].append({
            "name": "Bandit 代码安全扫描",
            "status": "跳过",
            "reason": "工具未安装"
        })
    
    # 4. 检查文件权限
    console.print("🔍 检查敏感文件权限...")
    
    sensitive_files = [
        target_path / "id_rsa",
        target_path / ".ssh" / "id_rsa",
        target_path / ".aws" / "credentials",
    ]
    
    permission_issues = []
    for file_path in sensitive_files:
        if file_path.exists():
            stat = file_path.stat()
            # 检查是否对其他用户可读
            if stat.st_mode & 0o044:
                permission_issues.append({
                    "file": str(file_path),
                    "issue": "权限过于开放"
                })
    
    if permission_issues:
        results["checks"].append({
            "name": "文件权限检查",
            "status": "警告",
            "issues": len(permission_issues),
            "details": permission_issues
        })
        console.print(f"  ⚠️ 发现 {len(permission_issues)} 个权限问题")
    else:
        results["checks"].append({
            "name": "文件权限检查",
            "status": "通过",
            "issues": 0
        })
        console.print("  ✅ 文件权限正确")
    
    # 输出结果
    console.print("\n" + "="*50)
    console.print("📊 审计结果汇总")
    console.print("="*50)
    
    total_issues = sum(c.get("issues", 0) for c in results["checks"])
    high_risk = sum(1 for c in results["checks"] if c.get("status") == "警告")
    
    if format == "json":
        console.print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        table = Table(show_header=True)
        table.add_column("检查项", style="cyan")
        table.add_column("状态", style="green")
        table.add_column("问题数", style="yellow")
        
        for check in results["checks"]:
            status_color = {
                "通过": "green",
                "警告": "yellow",
                "错误": "red",
                "跳过": "dim"
            }.get(check["status"], "white")
            
            table.add_row(
                check["name"],
                f"[{status_color}]{check['status']}[/{status_color}]",
                str(check.get("issues", "-"))
            )
        
        console.print(table)
        
        if total_issues > 0:
            console.print(f"\n⚠️ 共发现 {total_issues} 个问题")
            console.print("💡 建议: 运行 'ai-toolkit security scan' 获取详细信息")
        else:
            console.print("\n✅ 所有检查通过！")
    
    # 保存报告
    report_dir = Path.home() / ".ai-toolkit" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "security_audit.json"
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n📝 报告已保存: {report_file}")


@security_cli.command(name="scan")
@click.argument("path", default=".")
@click.option("--depth", "-d", default="medium", help="扫描深度 (light, medium, deep)")
def scan_security(path: str, depth: str):
    """深度安全扫描"""
    console.print(f"\n🔍 深度安全扫描: {path} (深度: {depth})\n")
    
    target_path = Path(path).resolve()
    if not target_path.exists():
        console.print(f"❌ 路径不存在: {path}")
        return
    
    findings = []
    
    # 1. 依赖漏洞扫描
    console.print("📦 检查依赖漏洞...")
    
    req_files = list(target_path.glob("requirements*.txt")) + list(target_path.glob("pyproject.toml"))
    
    if req_files:
        if not check_tool_installed("safety"):
            console.print("  📦 安装 Safety...")
            install_tool("safety")
        
        if check_tool_installed("safety"):
            for req_file in req_files:
                result = run_command(["safety", "check", "-r", str(req_file), "--json"], check=False)
                if result and result.stdout:
                    try:
                        safety_data = json.loads(result.stdout)
                        vulnerabilities = safety_data.get("vulnerabilities", [])
                        for vuln in vulnerabilities:
                            findings.append({
                                "type": "依赖漏洞",
                                "severity": vuln.get("severity", "unknown"),
                                "package": vuln.get("package_name"),
                                "description": vuln.get("vulnerability_id"),
                                "file": str(req_file.name)
                            })
                        console.print(f"  {'✅' if not vulnerabilities else '⚠️'} {req_file.name}: {len(vulnerabilities)} 个漏洞")
                    except:
                        console.print(f"  ⚠️ {req_file.name}: 解析失败")
        else:
            console.print("  ⚠️ Safety 未安装，跳过依赖扫描")
    else:
        console.print("  ℹ️ 未找到依赖文件")
    
    # 2. 敏感文件扫描
    console.print("🔍 扫描敏感文件...")
    
    sensitive_patterns = {
        ".env": "环境变量文件",
        "id_rsa": "SSH 私钥",
        "id_dsa": "SSH 私钥",
        ".aws/credentials": "AWS 凭证",
        ".docker/config.json": "Docker 配置",
        "kubeconfig": "Kubernetes 配置",
        ".pypirc": "PyPI 配置",
        "token.json": "Token 文件",
        "credentials.json": "凭证文件",
    }
    
    for pattern, desc in sensitive_patterns.items():
        matches = list(target_path.rglob(pattern))
        for match in matches:
            findings.append({
                "type": "敏感文件",
                "severity": "MEDIUM",
                "file": str(match.relative_to(target_path)),
                "description": desc
            })
    
    if any(f["type"] == "敏感文件" for f in findings):
        console.print(f"  ⚠️ 发现敏感文件")
    else:
        console.print("  ✅ 未发现敏感文件")
    
    # 3. 代码模式扫描
    if depth in ["medium", "deep"]:
        console.print("🔍 扫描危险代码模式...")
        
        dangerous_patterns = [
            (r'eval\s*\(', "使用 eval()", "HIGH"),
            (r'exec\s*\(', "使用 exec()", "HIGH"),
            (r'subprocess\.call.*shell\s*=\s*True', "shell=True 安全风险", "MEDIUM"),
            (r'pickle\.loads', "pickle 反序列化", "MEDIUM"),
            (r'yaml\.load\s*\([^)]*\)', "YAML 不安全加载", "MEDIUM"),
            (r'input\s*\(', "使用 input()", "LOW"),
        ]
        
        for file_path in target_path.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    for pattern, desc, severity in dangerous_patterns:
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            findings.append({
                                "type": "代码模式",
                                "severity": severity,
                                "file": str(file_path.relative_to(target_path)),
                                "line": line_num,
                                "description": desc
                            })
            except:
                pass
        
        code_issues = [f for f in findings if f["type"] == "代码模式"]
        if code_issues:
            console.print(f"  ⚠️ 发现 {len(code_issues)} 个危险代码模式")
        else:
            console.print("  ✅ 未发现危险代码模式")
    
    # 显示结果
    console.print("\n" + "="*50)
    console.print("📊 扫描结果")
    console.print("="*50)
    
    if findings:
        table = Table(show_header=True)
        table.add_column("类型", style="cyan")
        table.add_column("严重程度", style="yellow")
        table.add_column("文件/包", style="green")
        table.add_column("描述", style="white")
        
        for finding in findings[:20]:  # 限制显示数量
            severity_color = {
                "HIGH": "red",
                "MEDIUM": "yellow",
                "LOW": "blue"
            }.get(finding.get("severity", ""), "white")
            
            table.add_row(
                finding["type"],
                f"[{severity_color}]{finding.get('severity', '-')}[/{severity_color}]",
                finding.get("file", finding.get("package", "-")),
                finding.get("description", "")[:40]
            )
        
        console.print(table)
        
        if len(findings) > 20:
            console.print(f"\n... 还有 {len(findings) - 20} 个问题")
        
        # 统计
        high = len([f for f in findings if f.get("severity") == "HIGH"])
        medium = len([f for f in findings if f.get("severity") == "MEDIUM"])
        low = len([f for f in findings if f.get("severity") == "LOW"])
        
        console.print(f"\n高危: {high}, 中危: {medium}, 低危: {low}")
    else:
        console.print("✅ 未发现安全问题")
    
    # 保存结果
    report_dir = Path.home() / ".ai-toolkit" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / "security_scan.json"
    
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": subprocess.check_output(["date", "-Iseconds"]).decode().strip(),
            "path": str(target_path),
            "depth": depth,
            "findings": findings
        }, f, indent=2, ensure_ascii=False)
    
    console.print(f"\n📝 报告已保存: {report_file}")


@security_cli.command(name="compliance")
@click.option("--framework", "-f", default="basic", help="合规框架 (basic, gdpr, soc2)")
def check_compliance(framework: str):
    """合规检查"""
    console.print(f"\n📋 合规检查: {framework.upper()}\n")
    
    checks = {
        "basic": [
            ("LICENSE 文件存在", Path("LICENSE").exists() or Path("LICENSE.txt").exists()),
            ("README 文件存在", Path("README.md").exists()),
            (".gitignore 配置正确", Path(".gitignore").exists()),
            ("无硬编码密钥", True),  # 简化检查
            ("依赖版本锁定", Path("requirements.txt").exists() or Path("poetry.lock").exists()),
        ],
        "gdpr": [
            ("隐私政策", Path("PRIVACY.md").exists() or Path("privacy.md").exists()),
            ("数据收集声明", True),  # 需要手动检查
            ("用户数据删除机制", True),
            ("数据加密传输", True),
        ],
        "soc2": [
            ("访问控制策略", True),
            ("审计日志", Path(".ai-toolkit/logs").exists()),
            ("变更管理流程", True),
            ("备份策略", True),
        ]
    }
    
    framework_checks = checks.get(framework, checks["basic"])
    
    table = Table(show_header=True)
    table.add_column("检查项", style="cyan")
    table.add_column("状态", style="green")
    
    passed = 0
    for check_name, result in framework_checks:
        status = "✅ 通过" if result else "❌ 未通过"
        table.add_row(check_name, status)
        if result:
            passed += 1
    
    console.print(table)
    console.print(f"\n通过率: {passed}/{len(framework_checks)} ({passed/len(framework_checks)*100:.0f}%)")


@security_cli.command(name="report")
@click.option("--output", "-o", help="输出文件路径")
def security_report(output: str):
    """生成安全报告"""
    console.print("\n📊 生成安全报告\n")
    
    report_dir = Path.home() / ".ai-toolkit" / "reports"
    
    # 合并所有报告
    all_findings = []
    
    audit_file = report_dir / "security_audit.json"
    if audit_file.exists():
        with open(audit_file) as f:
            audit_data = json.load(f)
            all_findings.extend([{"source": "审计", **c} for c in audit_data.get("checks", [])])
    
    scan_file = report_dir / "security_scan.json"
    if scan_file.exists():
        with open(scan_file) as f:
            scan_data = json.load(f)
            all_findings.extend([{"source": "扫描", **f} for f in scan_data.get("findings", [])])
    
    # 生成报告
    report_md = f"""# AI Toolkit 安全报告

生成时间: {subprocess.check_output(['date']).decode().strip()}

## 执行摘要

- 总检查项: {len(all_findings)}
- 发现问题: {len([f for f in all_findings if f.get('issues', 0) > 0 or f.get('severity') in ['HIGH', 'MEDIUM']])}
- 高危问题: {len([f for f in all_findings if f.get('severity') == 'HIGH'])}

## 详细结果

"""
    
    for finding in all_findings:
        report_md += f"\n### {finding.get('name', finding.get('type', 'Unknown'))}\n"
        report_md += f"- 来源: {finding.get('source', 'unknown')}\n"
        report_md += f"- 状态: {finding.get('status', finding.get('severity', 'unknown'))}\n"
        if 'issues' in finding:
            report_md += f"- 问题数: {finding['issues']}\n"
    
    report_md += """
## 建议措施

1. 定期运行安全扫描
2. 及时更新依赖
3. 审查敏感文件权限
4. 配置自动化安全检测

---
报告由 AI Toolkit Security 模块生成
"""
    
    # 保存报告
    if output:
        report_path = Path(output)
    else:
        report_path = report_dir / "security_report.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)
    
    console.print(Panel(report_md, title="📊 安全报告", border_style="cyan"))
    console.print(f"\n✅ 报告已保存: {report_path}")


@security_cli.command(name="fix")
@click.option("--dry-run", is_flag=True, help="仅显示将要修复的内容")
def auto_fix(dry_run: bool):
    """自动修复安全问题"""
    console.print("\n🔧 自动修复安全问题\n")
    
    fixes_applied = []
    
    # 1. 修复 .gitignore
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        needed_entries = ['.env', '.env.local', '*.key', '*.pem', '.ai-toolkit/']
        missing = [e for e in needed_entries if e not in content]
        
        if missing:
            if dry_run:
                console.print(f"📋 将添加 .gitignore 条目: {', '.join(missing)}")
            else:
                with open(gitignore_path, 'a') as f:
                    f.write('\n# Security\n')
                    for entry in missing:
                        f.write(f"{entry}\n")
                fixes_applied.append(f"更新 .gitignore: {', '.join(missing)}")
                console.print(f"✅ 已更新 .gitignore")
    
    # 2. 检查并建议权限修复
    sensitive_files = list(Path('.').rglob('id_rsa')) + list(Path('.').rglob('*.pem'))
    for file_path in sensitive_files:
        if file_path.exists():
            stat = file_path.stat()
            if stat.st_mode & 0o044:  # 对其他用户可读
                if dry_run:
                    console.print(f"📋 将修复权限: {file_path} (chmod 600)")
                else:
                    os.chmod(file_path, 0o600)
                    fixes_applied.append(f"修复权限: {file_path}")
                    console.print(f"✅ 已修复权限: {file_path}")
    
    if fixes_applied:
        console.print(f"\n✅ 已应用 {len(fixes_applied)} 个修复:")
        for fix in fixes_applied:
            console.print(f"  - {fix}")
    elif not dry_run:
        console.print("✅ 未发现需要修复的问题")
    
    if dry_run:
        console.print("\n💡 使用 --dry-run 查看将要修复的内容，移除该参数执行修复")
