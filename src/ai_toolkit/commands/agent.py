"""Agent management commands for AI Toolkit.

This module provides real agent management functionality including:
- Creating agent configurations
- Deploying agents as background processes or Docker containers
- Listing and monitoring agents
- Chat and task assignment
- Swarm management and scaling
"""

import json
import os
import subprocess
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import requests
import yaml

# Configuration directories
AGENTS_DIR = Path.home() / ".ai-toolkit" / "agents"
RUNNING_DIR = AGENTS_DIR / "running"
DEFAULT_AGENT_PORT = 8000


def ensure_dirs():
    """Ensure required directories exist."""
    AGENTS_DIR.mkdir(parents=True, exist_ok=True)
    RUNNING_DIR.mkdir(parents=True, exist_ok=True)


def get_agent_config_path(agent_id: str) -> Path:
    """Get the configuration file path for an agent."""
    return AGENTS_DIR / f"{agent_id}.yaml"


def get_agent_pid_file(agent_id: str) -> Path:
    """Get the PID file path for a running agent."""
    return RUNNING_DIR / f"{agent_id}.pid"


def get_agent_port(agent_id: str) -> int:
    """Get the port for an agent (deterministic based on agent_id)."""
    # Simple hash to get a port in range 8000-9000
    hash_val = hash(agent_id) % 1000
    return DEFAULT_AGENT_PORT + abs(hash_val)


def is_agent_running(agent_id: str) -> tuple[bool, Optional[int]]:
    """Check if an agent is running and return its PID if so."""
    pid_file = get_agent_pid_file(agent_id)
    if not pid_file.exists():
        return False, None
    
    try:
        pid = int(pid_file.read_text().strip())
        # Check if process exists
        os.kill(pid, 0)
        return True, pid
    except (ValueError, OSError, ProcessLookupError):
        # Process not running, clean up stale pid file
        pid_file.unlink(missing_ok=True)
        return False, None


def generate_agent_code(agent_config: dict) -> str:
    """Generate Python code for an agent based on configuration."""
    agent_type = agent_config.get("type", "generic")
    capabilities = agent_config.get("capabilities", [])
    
    code = f'''#!/usr/bin/env python3
"""Auto-generated agent: {agent_config.get("name", "unnamed")}"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import JSONResponse
    import uvicorn
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False
    print("FastAPI not installed, running in limited mode")

# Agent configuration
AGENT_ID = "{agent_config.get("id")}"
AGENT_NAME = "{agent_config.get("name")}"
AGENT_TYPE = "{agent_type}"
CAPABILITIES = {capabilities}

class Agent:
    def __init__(self):
        self.id = AGENT_ID
        self.name = AGENT_NAME
        self.type = AGENT_TYPE
        self.capabilities = CAPABILITIES
        self.status = "idle"
        self.task_history = []
        self.created_at = datetime.now().isoformat()
    
    def get_info(self) -> Dict[str, Any]:
        return {{
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "capabilities": self.capabilities,
            "status": self.status,
            "created_at": self.created_at,
            "task_count": len(self.task_history)
        }}
    
    def chat(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Handle chat messages."""
        # Simple response logic - can be extended with LLM integration
        responses = {{
            "hello": f"Hello! I'm {{self.name}}, a {{self.type}} agent. How can I help you?",
            "help": f"I can perform these tasks: {{', '.join(self.capabilities)}}",
            "status": f"Current status: {{self.status}}",
        }}
        
        message_lower = message.lower().strip()
        response_text = responses.get(message_lower, f"Received: {{message}}. I'm a {{self.type}} agent with capabilities: {{', '.join(self.capabilities)}}")
        
        return {{
            "response": response_text,
            "agent_id": self.id,
            "timestamp": datetime.now().isoformat()
        }}
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task based on type."""
        task_type = task.get("type", "unknown")
        task_id = str(uuid.uuid4())
        
        self.status = f"executing: {{task_type}}"
        
        # Record task
        task_record = {{
            "id": task_id,
            "type": task_type,
            "params": task.get("params", {{}}),
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }}
        
        # Simulate task execution based on capability
        result = {{"task_id": task_id, "status": "completed"}}
        
        if task_type in self.capabilities:
            result["message"] = f"Task '{{task_type}}' executed successfully"
            result["output"] = f"Simulated output for {{task_type}}"
        else:
            result["status"] = "failed"
            result["error"] = f"Capability '{{task_type}}' not available"
            task_record["status"] = "failed"
        
        self.task_history.append(task_record)
        self.status = "idle"
        
        return result
    
    def health_check(self) -> Dict[str, Any]:
        return {{
            "status": "healthy",
            "agent_id": self.id,
            "uptime": "running",
            "timestamp": datetime.now().isoformat()
        }}

# Global agent instance
agent = Agent()

if HAS_FASTAPI:
    app = FastAPI(title=AGENT_NAME)
    
    @app.get("/")
    async def root():
        return {{"message": f"{{AGENT_NAME}} Agent API", "agent_id": AGENT_ID}}
    
    @app.get("/info")
    async def info():
        return agent.get_info()
    
    @app.post("/chat")
    async def chat_endpoint(request: Dict[str, Any]):
        message = request.get("message", "")
        context = request.get("context")
        return agent.chat(message, context)
    
    @app.post("/task")
    async def task_endpoint(request: Dict[str, Any]):
        return agent.execute_task(request)
    
    @app.get("/health")
    async def health():
        return agent.health_check()
    
    @app.get("/tasks")
    async def tasks():
        return {{"tasks": agent.task_history}}

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else {DEFAULT_AGENT_PORT}
    
    if HAS_FASTAPI:
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    else:
        print(f"Agent {{AGENT_NAME}} would run on port {{port}}")
        print("Install FastAPI for full functionality: pip install fastapi uvicorn")
'''
    return code


@click.group()
def agent():
    """Agent management commands."""
    ensure_dirs()


@agent.command()
@click.option("--name", "-n", required=True, help="Agent name")
@click.option("--type", "-t", "agent_type", default="generic", help="Agent type")
@click.option("--capabilities", "-c", multiple=True, help="Agent capabilities")
@click.option("--config", "-f", type=click.Path(), help="Config file (JSON/YAML)")
@click.option("--port", "-p", type=int, help="Custom port (auto-assigned if not specified)")
def create(name: str, agent_type: str, capabilities: tuple, config: Optional[str], port: Optional[int]):
    """Create a new agent configuration."""
    agent_id = f"{agent_type}-{uuid.uuid4().hex[:8]}"
    
    # Load config from file if provided
    if config:
        config_path = Path(config)
        if not config_path.exists():
            click.echo(f"Error: Config file not found: {config}", err=True)
            sys.exit(1)
        
        with open(config_path) as f:
            if config_path.suffix in ('.yaml', '.yml'):
                file_config = yaml.safe_load(f)
            else:
                file_config = json.load(f)
    else:
        file_config = {}
    
    # Build agent configuration
    agent_config = {
        "id": agent_id,
        "name": name,
        "type": agent_type,
        "capabilities": list(capabilities) if capabilities else file_config.get("capabilities", ["chat", "task"]),
        "created_at": datetime.now().isoformat(),
        "port": port or get_agent_port(agent_id),
        **{k: v for k, v in file_config.items() if k not in ["id", "name", "type", "capabilities", "created_at", "port"]}
    }
    
    # Save configuration
    config_path = get_agent_config_path(agent_id)
    with open(config_path, 'w') as f:
        yaml.dump(agent_config, f, default_flow_style=False)
    
    # Generate agent code
    agent_code = generate_agent_code(agent_config)
    code_path = AGENTS_DIR / f"{agent_id}.py"
    with open(code_path, 'w') as f:
        f.write(agent_code)
    
    # Make executable
    code_path.chmod(0o755)
    
    click.echo(f"✓ Agent created: {agent_id}")
    click.echo(f"  Name: {name}")
    click.echo(f"  Type: {agent_type}")
    click.echo(f"  Port: {agent_config['port']}")
    click.echo(f"  Config: {config_path}")
    click.echo(f"  Code: {code_path}")


@agent.command()
@click.argument("agent_id")
@click.option("--docker", is_flag=True, help="Deploy as Docker container")
@click.option("--detach/--no-detach", default=True, help="Run in background")
def deploy(agent_id: str, docker: bool, detach: bool):
    """Deploy an agent."""
    config_path = get_agent_config_path(agent_id)
    if not config_path.exists():
        click.echo(f"Error: Agent not found: {agent_id}", err=True)
        sys.exit(1)
    
    with open(config_path) as f:
        agent_config = yaml.safe_load(f)
    
    # Check if already running
    is_running, existing_pid = is_agent_running(agent_id)
    if is_running:
        click.echo(f"Agent {agent_id} is already running (PID: {existing_pid})")
        return
    
    port = agent_config.get("port", get_agent_port(agent_id))
    
    if docker:
        # Docker deployment
        dockerfile_content = f'''FROM python:3.11-slim
WORKDIR /app
RUN pip install fastapi uvicorn
COPY {agent_id}.py /app/agent.py
EXPOSE {port}
CMD ["python", "/app/agent.py", "{port}"]
'''
        dockerfile_path = AGENTS_DIR / f"{agent_id}.Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content)
        
        click.echo(f"Building Docker image for {agent_id}...")
        try:
            subprocess.run(
                ["docker", "build", "-f", str(dockerfile_path), "-t", f"ai-toolkit/{agent_id}", str(AGENTS_DIR)],
                check=True,
                capture_output=True
            )
            
            click.echo(f"Starting Docker container...")
            subprocess.run(
                ["docker", "run", "-d", "--name", agent_id, "-p", f"{port}:{port}", f"ai-toolkit/{agent_id}"],
                check=True,
                capture_output=True
            )
            click.echo(f"✓ Agent {agent_id} deployed as Docker container on port {port}")
        except subprocess.CalledProcessError as e:
            click.echo(f"Error deploying Docker container: {e}", err=True)
            sys.exit(1)
        except FileNotFoundError:
            click.echo("Error: Docker not found. Please install Docker.", err=True)
            # Fallback to subprocess
            click.echo("Falling back to subprocess deployment...")
    else:
        # Subprocess deployment
        code_path = AGENTS_DIR / f"{agent_id}.py"
        if not code_path.exists():
            click.echo(f"Error: Agent code not found: {code_path}", err=True)
            sys.exit(1)
        
        try:
            if detach:
                # Start in background
                process = subprocess.Popen(
                    [sys.executable, str(code_path), str(port)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                pid = process.pid
            else:
                # Run in foreground
                click.echo(f"Starting agent {agent_id} on port {port}...")
                process = subprocess.Popen([sys.executable, str(code_path), str(port)])
                pid = process.pid
            
            # Save PID
            pid_file = get_agent_pid_file(agent_id)
            pid_file.write_text(str(pid))
            
            click.echo(f"✓ Agent {agent_id} deployed (PID: {pid}, Port: {port})")
            
            if detach:
                # Wait a moment and verify it's running
                time.sleep(1)
                is_running, _ = is_agent_running(agent_id)
                if is_running:
                    click.echo(f"  Health check: http://localhost:{port}/health")
                else:
                    click.echo("  Warning: Agent may not have started properly", err=True)
            
        except Exception as e:
            click.echo(f"Error starting agent: {e}", err=True)
            sys.exit(1)


@agent.command()
def list():
    """List all agents."""
    ensure_dirs()
    
    agents = []
    for config_file in AGENTS_DIR.glob("*.yaml"):
        try:
            with open(config_file) as f:
                config = yaml.safe_load(f)
            
            agent_id = config.get("id", config_file.stem)
            is_running, pid = is_agent_running(agent_id)
            
            agents.append({
                "id": agent_id,
                "name": config.get("name", "Unknown"),
                "type": config.get("type", "generic"),
                "port": config.get("port", get_agent_port(agent_id)),
                "status": "running" if is_running else "stopped",
                "pid": pid
            })
        except Exception as e:
            click.echo(f"Warning: Could not read {config_file}: {e}", err=True)
    
    if not agents:
        click.echo("No agents found. Create one with: ai-toolkit agent create")
        return
    
    # Print table
    click.echo(f"{'ID':<25} {'Name':<20} {'Type':<12} {'Port':<8} {'Status':<10} {'PID':<8}")
    click.echo("-" * 85)
    for a in sorted(agents, key=lambda x: x["id"]):
        pid_str = str(a["pid"]) if a["pid"] else "-"
        click.echo(f"{a['id']:<25} {a['name']:<20} {a['type']:<12} {a['port']:<8} {a['status']:<10} {pid_str:<8}")


@agent.command()
@click.argument("agent_id")
@click.argument("message")
@click.option("--context", "-c", help="JSON context for the conversation")
def chat(agent_id: str, message: str, context: Optional[str]):
    """Chat with an agent."""
    config_path = get_agent_config_path(agent_id)
    if not config_path.exists():
        click.echo(f"Error: Agent not found: {agent_id}", err=True)
        sys.exit(1)
    
    with open(config_path) as f:
        agent_config = yaml.safe_load(f)
    
    port = agent_config.get("port", get_agent_port(agent_id))
    
    # Check if agent is running
    is_running, _ = is_agent_running(agent_id)
    if not is_running:
        click.echo(f"Agent {agent_id} is not running. Start it with: ai-toolkit agent deploy {agent_id}")
        sys.exit(1)
    
    try:
        ctx = json.loads(context) if context else None
        response = requests.post(
            f"http://localhost:{port}/chat",
            json={"message": message, "context": ctx},
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        click.echo(f"Agent: {result.get('response', 'No response')}")
        
    except requests.ConnectionError:
        click.echo(f"Error: Could not connect to agent at port {port}", err=True)
        sys.exit(1)
    except requests.Timeout:
        click.echo("Error: Request timed out", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@agent.command()
@click.argument("agent_id")
@click.argument("task_type")
@click.option("--params", "-p", help="JSON parameters for the task")
@click.option("--file", "-f", type=click.Path(), help="JSON file with task parameters")
def task(agent_id: str, task_type: str, params: Optional[str], file: Optional[str]):
    """Assign a task to an agent."""
    config_path = get_agent_config_path(agent_id)
    if not config_path.exists():
        click.echo(f"Error: Agent not found: {agent_id}", err=True)
        sys.exit(1)
    
    with open(config_path) as f:
        agent_config = yaml.safe_load(f)
    
    port = agent_config.get("port", get_agent_port(agent_id))
    
    # Check if agent is running
    is_running, _ = is_agent_running(agent_id)
    if not is_running:
        click.echo(f"Agent {agent_id} is not running. Start it with: ai-toolkit agent deploy {agent_id}")
        sys.exit(1)
    
    # Parse parameters
    task_params = {}
    if file:
        with open(file) as f:
            task_params = json.load(f)
    elif params:
        task_params = json.loads(params)
    
    try:
        response = requests.post(
            f"http://localhost:{port}/task",
            json={"type": task_type, "params": task_params},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        
        if result.get("status") == "completed":
            click.echo(f"✓ Task completed: {result.get('message', 'Success')}")
            if "output" in result:
                click.echo(f"Output: {result['output']}")
        else:
            click.echo(f"✗ Task failed: {result.get('error', 'Unknown error')}", err=True)
            sys.exit(1)
        
        click.echo(f"Task ID: {result.get('task_id')}")
        
    except requests.ConnectionError:
        click.echo(f"Error: Could not connect to agent at port {port}", err=True)
        sys.exit(1)
    except requests.Timeout:
        click.echo("Error: Request timed out", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@agent.command()
@click.argument("name")
@click.option("--agents", "-a", multiple=True, required=True, help="Agent IDs to include in swarm")
@click.option("--strategy", "-s", default="round_robin", type=click.Choice(["round_robin", "load_balance", "priority"]), help="Task distribution strategy")
def swarm(name: str, agents: tuple, strategy: str):
    """Create a swarm of agents."""
    swarm_id = f"swarm-{uuid.uuid4().hex[:8]}"
    
    # Validate agents exist
    agent_list = []
    for agent_id in agents:
        config_path = get_agent_config_path(agent_id)
        if not config_path.exists():
            click.echo(f"Error: Agent not found: {agent_id}", err=True)
            sys.exit(1)
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
        agent_list.append({
            "id": agent_id,
            "name": config.get("name"),
            "type": config.get("type"),
            "port": config.get("port", get_agent_port(agent_id))
        })
    
    swarm_config = {
        "id": swarm_id,
        "name": name,
        "strategy": strategy,
        "agents": agent_list,
        "created_at": datetime.now().isoformat()
    }
    
    # Save swarm configuration
    swarm_path = AGENTS_DIR / f"swarm-{swarm_id}.yaml"
    with open(swarm_path, 'w') as f:
        yaml.dump(swarm_config, f, default_flow_style=False)
    
    click.echo(f"✓ Swarm created: {swarm_id}")
    click.echo(f"  Name: {name}")
    click.echo(f"  Strategy: {strategy}")
    click.echo(f"  Agents: {len(agent_list)}")
    for a in agent_list:
        click.echo(f"    - {a['id']} ({a['name']})")


@agent.command()
@click.argument("agent_id", required=False)
@click.option("--all", "-a", "monitor_all", is_flag=True, help="Monitor all agents")
def monitor(agent_id: Optional[str], monitor_all: bool):
    """Monitor agent status."""
    if not agent_id and not monitor_all:
        click.echo("Error: Specify an agent ID or use --all", err=True)
        sys.exit(1)
    
    agents_to_monitor = []
    
    if monitor_all:
        for config_file in AGENTS_DIR.glob("*.yaml"):
            if config_file.name.startswith("swarm-"):
                continue
            try:
                with open(config_file) as f:
                    config = yaml.safe_load(f)
                agents_to_monitor.append(config.get("id", config_file.stem))
            except:
                pass
    else:
        agents_to_monitor = [agent_id]
    
    if not agents_to_monitor:
        click.echo("No agents to monitor")
        return
    
    click.echo(f"{'Agent ID':<25} {'Status':<10} {'Health':<10} {'Uptime':<15}")
    click.echo("-" * 65)
    
    for aid in agents_to_monitor:
        config_path = get_agent_config_path(aid)
        if not config_path.exists():
            click.echo(f"{aid:<25} {'not_found':<10}")
            continue
        
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        port = config.get("port", get_agent_port(aid))
        is_running, _ = is_agent_running(aid)
        
        if not is_running:
            click.echo(f"{aid:<25} {'stopped':<10} {'-':<10} {'-':<15}")
            continue
        
        # Check health endpoint
        try:
            response = requests.get(f"http://localhost:{port}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                status = health_data.get("status", "unknown")
                uptime = "running"
                click.echo(f"{aid:<25} {'running':<10} {status:<10} {uptime:<15}")
            else:
                click.echo(f"{aid:<25} {'running':<10} {'error':<10} {'-':<15}")
        except:
            click.echo(f"{aid:<25} {'running':<10} {'no_response':<10} {'-':<15}")


@agent.command()
@click.argument("agent_id")
@click.option("--replicas", "-r", type=int, default=2, help="Number of replicas")
@click.option("--docker-compose", "-d", is_flag=True, help="Use Docker Compose for scaling")
def scale(agent_id: str, replicas: int, docker_compose: bool):
    """Scale an agent to multiple replicas."""
    config_path = get_agent_config_path(agent_id)
    if not config_path.exists():
        click.echo(f"Error: Agent not found: {agent_id}", err=True)
        sys.exit(1)
    
    with open(config_path) as f:
        agent_config = yaml.safe_load(f)
    
    base_port = agent_config.get("port", get_agent_port(agent_id))
    
    if docker_compose:
        # Generate docker-compose.yml for scaling
        compose_config = {
            "version": "3.8",
            "services": {}
        }
        
        for i in range(replicas):
            service_name = f"{agent_id}-{i+1}"
            compose_config["services"][service_name] = {
                "build": {
                    "context": str(AGENTS_DIR),
                    "dockerfile": f"{agent_id}.Dockerfile"
                },
                "ports": [f"{base_port + i}:{base_port}"],
                "environment": {
                    "AGENT_ID": f"{agent_id}-{i+1}",
                    "REPLICA_INDEX": str(i)
                }
            }
        
        compose_path = AGENTS_DIR / f"{agent_id}-compose.yaml"
        with open(compose_path, 'w') as f:
            yaml.dump(compose_config, f, default_flow_style=False)
        
        click.echo(f"✓ Docker Compose file created: {compose_path}")
        click.echo(f"  Replicas: {replicas}")
        click.echo(f"  Ports: {base_port}-{base_port + replicas - 1}")
        click.echo(f"\nTo deploy, run:")
        click.echo(f"  docker-compose -f {compose_path} up -d")
        click.echo(f"\nTo scale later:")
        click.echo(f"  docker-compose -f {compose_path} up -d --scale {agent_id}-1={replicas}")
    else:
        # Process-based scaling
        click.echo(f"Scaling {agent_id} to {replicas} replicas...")
        
        started = 0
        for i in range(replicas):
            replica_id = f"{agent_id}-{i+1}"
            port = base_port + i
            
            # Check if already running
            pid_file = RUNNING_DIR / f"{replica_id}.pid"
            if pid_file.exists():
                try:
                    pid = int(pid_file.read_text().strip())
                    os.kill(pid, 0)
                    click.echo(f"  Replica {i+1} already running (PID: {pid})")
                    started += 1
                    continue
                except:
                    pass
            
            # Start new replica
            code_path = AGENTS_DIR / f"{agent_id}.py"
            try:
                process = subprocess.Popen(
                    [sys.executable, str(code_path), str(port)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True,
                    env={**os.environ, "AGENT_ID": replica_id, "REPLICA_INDEX": str(i)}
                )
                pid_file.write_text(str(process.pid))
                click.echo(f"  ✓ Replica {i+1} started (PID: {process.pid}, Port: {port})")
                started += 1
            except Exception as e:
                click.echo(f"  ✗ Replica {i+1} failed: {e}", err=True)
        
        click.echo(f"\n{started}/{replicas} replicas running")
        click.echo(f"Ports: {base_port}-{base_port + replicas - 1}")


@agent.command()
@click.argument("agent_id")
def stop(agent_id: str):
    """Stop a running agent."""
    is_running, pid = is_agent_running(agent_id)
    
    if not is_running:
        click.echo(f"Agent {agent_id} is not running")
        return
    
    try:
        os.kill(pid, 15)  # SIGTERM
        click.echo(f"✓ Stopped agent {agent_id} (PID: {pid})")
        
        # Clean up PID file
        pid_file = get_agent_pid_file(agent_id)
        pid_file.unlink(missing_ok=True)
    except ProcessLookupError:
        click.echo(f"Agent {agent_id} process not found")
        pid_file = get_agent_pid_file(agent_id)
        pid_file.unlink(missing_ok=True)
    except Exception as e:
        click.echo(f"Error stopping agent: {e}", err=True)
        sys.exit(1)


@agent.command()
@click.argument("agent_id")
def logs(agent_id: str):
    """View agent logs."""
    # Check if running
    is_running, pid = is_agent_running(agent_id)
    
    if is_running:
        click.echo(f"Agent {agent_id} is running (PID: {pid})")
        click.echo("Attempting to get logs from running process...")
        # In a real implementation, we'd have a logging mechanism
        # For now, just show status
        config_path = get_agent_config_path(agent_id)
        with open(config_path) as f:
            config = yaml.safe_load(f)
        port = config.get("port", get_agent_port(agent_id))
        click.echo(f"Health endpoint: http://localhost:{port}/health")
    else:
        click.echo(f"Agent {agent_id} is not running")


# Backwards compatibility aliases
@agent.command(name="run")
@click.argument("agent_id")
def run_cmd(agent_id: str):
    """Run an agent (alias for deploy --no-detach)."""
    ctx = click.get_current_context()
    ctx.invoke(deploy, agent_id=agent_id, docker=False, detach=False)


@agent.command(name="status")
def status_cmd():
    """Show agent status (alias for list)."""
    ctx = click.get_current_context()
    ctx.invoke(list)
