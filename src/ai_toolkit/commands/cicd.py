"""
CI/CD工具 - 真实实现版
集成真实CI/CD功能：GitHub Actions、GitLab CI、Jenkinsfile生成和验证
"""

import click
import os
import subprocess
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.progress import Progress

console = Console()


@click.group(name="cicd")
def cicd_cli():
    """CI/CD工具 - 支持GitHub Actions、GitLab CI、Jenkins"""
    pass


def run_command(cmd: List[str], cwd: Optional[str] = None) -> tuple:
    """运行shell命令并返回结果"""
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


@cicd_cli.command(name="init")
@click.option("--platform", "-p", type=click.Choice(["github", "gitlab", "jenkins"]), default="github", help="CI/CD平台")
@click.option("--language", "-l", default="python", help="项目语言")
@click.option("--output", "-o", help="输出文件路径")
def init_pipeline(platform: str, language: str, output: Optional[str]):
    """初始化CI/CD配置文件"""
    console.print(f"\n🔧 初始化 {platform} CI/CD 配置\n")
    
    templates = {
        "github": {
            "python": """name: Python CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v5
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint with flake8
      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
    
    - name: Test with pytest
      run: pytest --cov=. --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
""",
            "node": """name: Node.js CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run tests
      run: npm test
    
    - name: Build
      run: npm run build
"""
        },
        "gitlab": {
            "python": """stages:
  - test
  - build
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

test:
  stage: test
  image: python:3.11
  before_script:
    - python -m venv venv
    - source venv/bin/activate
    - pip install -r requirements.txt
    - pip install pytest pytest-cov flake8
  script:
    - flake8 . --count --select=E9,F63,F7,F82
    - pytest --cov=. --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t $CI_PROJECT_NAME:$CI_COMMIT_SHA .
  only:
    - main
""",
            "node": """stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: node:20
  cache:
    paths:
      - node_modules/
  before_script:
    - npm ci
  script:
    - npm run lint
    - npm test
  coverage: '/All files[^|]*\|[^|]*\s+(\d+\.?\d*)/'

build:
  stage: build
  image: node:20
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
  only:
    - main
"""
        },
        "jenkins": {
            "python": """pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.11'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest pytest-cov flake8'
            }
        }
        
        stage('Lint') {
            steps {
                sh 'flake8 . --count --select=E9,F63,F7,F82'
            }
        }
        
        stage('Test') {
            steps {
                sh 'pytest --cov=. --cov-report=xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                    cobertura coberturaReportFile: 'coverage.xml'
                }
            }
        }
        
        stage('Build') {
            when {
                branch 'main'
            }
            steps {
                sh 'docker build -t myapp:${BUILD_NUMBER} .'
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}""",
            "node": """pipeline {
    agent any
    
    tools {
        nodejs 'Node 20'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }
        
        stage('Lint') {
            steps {
                sh 'npm run lint'
            }
        }
        
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
    }
    
    post {
        always {
            junit 'test-results.xml'
            cleanWs()
        }
    }
}"""
        }
    }
    
    # 确定输出路径
    if not output:
        if platform == "github":
            output = ".github/workflows/ci.yml"
        elif platform == "gitlab":
            output = ".gitlab-ci.yml"
        else:
            output = "Jenkinsfile"
    
    output_path = Path(output)
    
    # 创建目录
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 获取模板
    template = templates.get(platform, {}).get(language, templates["github"]["python"])
    
    # 写入文件
    output_path.write_text(template)
    
    console.print(f"✅ 已创建: {output}")
    console.print(f"   平台: {platform}")
    console.print(f"   语言: {language}")
    console.print(f"\n📝 文件内容预览:")
    console.print(Panel(template[:500] + "..." if len(template) > 500 else template, title=output))


@cicd_cli.command(name="validate")
@click.option("--file", "-f", help="配置文件路径")
@click.option("--platform", "-p", type=click.Choice(["github", "gitlab", "jenkins"]), help="CI/CD平台")
def validate_config(file: Optional[str], platform: Optional[str]):
    """验证CI/CD配置文件"""
    console.print("\n✅ 验证CI/CD配置\n")
    
    # 自动检测平台和文件
    if not file:
        for path, plat in [
            (".github/workflows/ci.yml", "github"),
            (".github/workflows/main.yml", "github"),
            (".gitlab-ci.yml", "gitlab"),
            ("Jenkinsfile", "jenkins")
        ]:
            if Path(path).exists():
                file = path
                platform = plat
                break
    
    if not file or not Path(file).exists():
        console.print("[red]❌ 未找到CI/CD配置文件[/red]")
        console.print("\n请指定文件路径或使用 --platform 选项")
        return
    
    file_path = Path(file)
    content = file_path.read_text()
    
    console.print(f"文件: {file}")
    console.print(f"平台: {platform or 'auto-detect'}")
    console.print("")
    
    errors = []
    warnings = []
    
    if platform == "github" or file_path.suffix == ".yml":
        # 验证YAML语法
        try:
            yaml.safe_load(content)
            console.print("[green]✓ YAML语法正确[/green]")
        except yaml.YAMLError as e:
            errors.append(f"YAML语法错误: {e}")
        
        # GitHub Actions特定验证
        if "github" in str(file_path).lower():
            if "on:" not in content and "'on':" not in content:
                errors.append("缺少触发器配置 (on:)")
            if "jobs:" not in content:
                errors.append("缺少jobs配置")
            if "runs-on:" not in content and "runs-on :" not in content:
                warnings.append("建议指定runs-on")
                
    elif platform == "gitlab" or "gitlab" in file.lower():
        try:
            yaml.safe_load(content)
            console.print("[green]✓ YAML语法正确[/green]")
        except yaml.YAMLError as e:
            errors.append(f"YAML语法错误: {e}")
        
        if "stages:" not in content:
            warnings.append("未定义stages，将使用默认阶段")
            
    elif platform == "jenkins" or "jenkins" in file.lower():
        if "pipeline {" not in content:
            errors.append("不是有效的Declarative Pipeline语法")
        if "stages {" not in content:
            errors.append("缺少stages块")
        if "agent" not in content:
            warnings.append("建议指定agent")
    
    # 显示结果
    if errors:
        console.print("\n[red]❌ 错误:[/red]")
        for error in errors:
            console.print(f"  • {error}")
    
    if warnings:
        console.print("\n[yellow]⚠️ 警告:[/yellow]")
        for warning in warnings:
            console.print(f"  • {warning}")
    
    if not errors and not warnings:
        console.print("[green]✅ 配置验证通过！[/green]")
    elif not errors:
        console.print("\n[yellow]⚠️ 配置可用，但存在警告[/yellow]")
    else:
        console.print("\n[red]❌ 配置存在错误，请修复后再使用[/red]")


@cicd_cli.command(name="run-local")
@click.option("--file", "-f", help="配置文件路径")
@click.option("--job", "-j", help="指定运行的job")
@click.option("--dry-run", is_flag=True, help="仅预览不执行")
def run_local(file: Optional[str], job: Optional[str], dry_run: bool):
    """本地模拟运行CI/CD流程"""
    console.print("\n🚀 本地运行CI/CD流程\n")
    
    # 检测配置文件
    if not file:
        for path in [".github/workflows/ci.yml", ".gitlab-ci.yml", "Jenkinsfile"]:
            if Path(path).exists():
                file = path
                break
    
    if not file or not Path(file).exists():
        console.print("[red]❌ 未找到CI/CD配置文件[/red]")
        return
    
    console.print(f"配置文件: {file}")
    console.print(f" dry-run: {dry_run}")
    console.print("")
    
    # 解析配置
    content = Path(file).read_text()
    
    if ".github" in file:
        # 简化的GitHub Actions本地运行
        try:
            config = yaml.safe_load(content)
            jobs = config.get("jobs", {})
            
            if job and job not in jobs:
                console.print(f"[red]Job '{job}' 不存在[/red]")
                return
            
            jobs_to_run = {job: jobs[job]} if job else jobs
            
            for job_name, job_config in jobs_to_run.items():
                console.print(f"\n[bold cyan]Job: {job_name}[/bold cyan]")
                
                steps = job_config.get("steps", [])
                for i, step in enumerate(steps, 1):
                    name = step.get("name", f"Step {i}")
                    console.print(f"\n  Step {i}: {name}")
                    
                    if "run" in step:
                        cmd = step["run"]
                        console.print(f"  Command: {cmd[:60]}..." if len(cmd) > 60 else f"  Command: {cmd}")
                        
                        if not dry_run:
                            success, stdout, stderr = run_command(cmd.split())
                            if success:
                                console.print(f"  [green]✓ 成功[/green]")
                            else:
                                console.print(f"  [red]✗ 失败: {stderr[:100]}[/red]")
                    elif "uses" in step:
                        console.print(f"  Action: {step['uses']}")
                        console.print(f"  [yellow]⚠ 跳过Action步骤（本地不支持）[/yellow]")
                        
        except yaml.YAMLError as e:
            console.print(f"[red]YAML解析错误: {e}[/red]")


@cicd_cli.command(name="status")
@click.option("--repo", "-r", help="仓库路径", default=".")
def pipeline_status(repo: str):
    """查看CI/CD状态（需要git和对应平台CLI）"""
    console.print("\n📊 CI/CD 状态\n")
    
    repo_path = Path(repo)
    if not (repo_path / ".git").exists():
        console.print("[red]❌ 不是git仓库[/red]")
        return
    
    # 检查配置文件
    configs = []
    if (repo_path / ".github/workflows").exists():
        workflows = list((repo_path / ".github/workflows").glob("*.yml"))
        configs.extend([f"GitHub Actions: {w.name}" for w in workflows])
    
    if (repo_path / ".gitlab-ci.yml").exists():
        configs.append("GitLab CI: .gitlab-ci.yml")
    
    if (repo_path / "Jenkinsfile").exists():
        configs.append("Jenkins: Jenkinsfile")
    
    if configs:
        console.print("[green]✓ 发现CI/CD配置:[/green]")
        for config in configs:
            console.print(f"  • {config}")
    else:
        console.print("[yellow]⚠ 未发现CI/CD配置文件[/yellow]")
    
    # 检查最近的git提交
    success, stdout, _ = run_command(
        ["git", "log", "--oneline", "-5"],
        cwd=str(repo_path)
    )
    if success:
        console.print("\n最近提交:")
        for line in stdout.strip().split("\n"):
            console.print(f"  {line}")
    
    # 检查git状态
    success, stdout, _ = run_command(
        ["git", "status", "--short"],
        cwd=str(repo_path)
    )
    if success and stdout.strip():
        console.print("\n[yellow]⚠ 有未提交的更改:[/yellow]")
        console.print(stdout)


@cicd_cli.command(name="generate")
@click.option("--type", "-t", type=click.Choice(["docker", "python", "node", "go"]), default="python", help="项目类型")
@click.option("--platform", "-p", type=click.Choice(["github", "gitlab", "jenkins"]), default="github", help="CI/CD平台")
@click.option("--deploy", "-d", is_flag=True, help="包含部署阶段")
def generate_pipeline(type: str, platform: str, deploy: bool):
    """生成完整的CI/CD流水线"""
    console.print(f"\n🔧 生成 {platform} {type} 流水线\n")
    
    # Docker构建步骤
    docker_steps = """
    - name: Build Docker image
      run: docker build -t myapp:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
""" if deploy else ""
    
    # 部署步骤
    deploy_steps = """
    - name: Deploy to production
      run: |
        # 配置kubectl
        echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig
        
        # 更新部署
        kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
        kubectl rollout status deployment/myapp
""" if deploy else ""
    
    templates = {
        ("github", "python"): f"""name: Python CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.11'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: Cache pip packages
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov black flake8
    
    - name: Lint with flake8
      run: flake8 . --count --exit-zero --max-complexity=10
    
    - name: Format check with black
      run: black --check .
    
    - name: Test with pytest
      run: pytest --cov=. --cov-report=xml --cov-report=html
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false

  build:{docker_steps}
  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    {deploy_steps}
""",
        ("github", "node"): f"""name: Node.js CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '20'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint
    
    - name: Run tests
      run: npm test -- --coverage
    
    - name: Build
      run: npm run build

  build:{docker_steps}
  deploy:
    needs: [test, build]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    {deploy_steps}
"""
    }
    
    template = templates.get((platform, type), templates[("github", "python")])
    
    console.print("[green]✅ 生成的流水线配置:[/green]\n")
    console.print(Panel(template, title=f"{platform} - {type}"))
    
    # 保存建议
    output_file = ".github/workflows/ci.yml" if platform == "github" else ".gitlab-ci.yml" if platform == "gitlab" else "Jenkinsfile"
    console.print(f"\n💡 建议保存到: {output_file}")
    console.print(f"   使用: ai-toolkit cicd init --platform {platform} --language {type}")


@cicd_cli.command(name="lint")
@click.option("--file", "-f", help="配置文件路径")
@click.option("--fix", is_flag=True, help="自动修复问题")
def lint_pipeline(file: Optional[str], fix: bool):
    """检查CI/CD配置最佳实践"""
    console.print("\n🔍 CI/CD 最佳实践检查\n")
    
    if not file:
        for path in [".github/workflows/ci.yml", ".gitlab-ci.yml", "Jenkinsfile"]:
            if Path(path).exists():
                file = path
                break
    
    if not file or not Path(file).exists():
        console.print("[red]❌ 未找到配置文件[/red]")
        return
    
    content = Path(file).read_text()
    issues = []
    
    # 通用检查
    if "password" in content.lower() or "secret" in content.lower():
        if "secrets." not in content and "${{" not in content:
            issues.append(("error", "检测到硬编码的敏感信息，请使用secrets"))
    
    if "latest" in content and "docker" in content.lower():
        issues.append(("warning", "使用'latest'标签可能导致不可重现的构建"))
    
    # GitHub Actions特定检查
    if ".github" in file:
        if "actions/checkout@v2" in content or "actions/checkout@v3" in content:
            issues.append(("warning", "建议使用 actions/checkout@v4"))
        
        if "cache:" not in content and ("pip" in content or "npm" in content):
            issues.append(("suggestion", "建议添加依赖缓存以加速构建"))
        
        if "timeout-minutes:" not in content:
            issues.append(("suggestion", "建议设置timeout-minutes防止作业挂起"))
    
    # 显示结果
    errors = [i for i in issues if i[0] == "error"]
    warnings = [i for i in issues if i[0] == "warning"]
    suggestions = [i for i in issues if i[0] == "suggestion"]
    
    if errors:
        console.print("[red]❌ 错误:[/red]")
        for _, msg in errors:
            console.print(f"  • {msg}")
    
    if warnings:
        console.print("\n[yellow]⚠️ 警告:[/yellow]")
        for _, msg in warnings:
            console.print(f"  • {msg}")
    
    if suggestions:
        console.print("\n[blue]💡 建议:[/blue]")
        for _, msg in suggestions:
            console.print(f"  • {msg}")
    
    if not issues:
        console.print("[green]✅ 配置符合最佳实践！[/green]")
    
    if fix and warnings:
        console.print("\n[yellow]⚠️ 自动修复尚未实现，请手动修改[/yellow]")


if __name__ == "__main__":
    cicd_cli()
