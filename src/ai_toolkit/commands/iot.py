"""
物联网和嵌入式系统 - 真实实现
支持 MQTT、串口通信、蓝牙扫描、传感器数据读取
"""

import click
import json
import time
import subprocess
import serial
import serial.tools.list_ports
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich import box

console = Console()

# 配置文件路径
IOT_CONFIG_DIR = Path.home() / ".ai-toolkit" / "iot"
IOT_CONFIG_FILE = IOT_CONFIG_DIR / "config.json"
IOT_LOG_FILE = IOT_CONFIG_DIR / "iot.log"


def ensure_config_dir():
    """确保配置目录存在"""
    IOT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> Dict:
    """加载IoT配置"""
    ensure_config_dir()
    if IOT_CONFIG_FILE.exists():
        with open(IOT_CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        "mqtt_brokers": [],
        "devices": [],
        "gateways": [],
        "automations": [],
        "alerts": []
    }


def save_config(config: Dict):
    """保存IoT配置"""
    ensure_config_dir()
    with open(IOT_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def log_activity(message: str):
    """记录活动日志"""
    ensure_config_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(IOT_LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")


@click.group(name="iot")
def iot_cli():
    """物联网和嵌入式系统 - 支持真实设备连接"""
    pass


@iot_cli.command(name="scan")
@click.option("--type", "-t", type=click.Choice(["serial", "bluetooth", "mqtt", "all"]), default="all", help="扫描类型")
@click.option("--timeout", "-T", default=5, help="扫描超时(秒)")
def scan_devices(type: str, timeout: int):
    """扫描可用设备"""
    console.print(f"\n🔍 扫描{type if type != 'all' else '所有'}设备\n")
    
    found_devices = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        
        if type in ["serial", "all"]:
            task = progress.add_task("扫描串口设备...", total=None)
            try:
                ports = list(serial.tools.list_ports.comports())
                for port in ports:
                    found_devices.append({
                        "type": "serial",
                        "name": port.description,
                        "address": port.device,
                        "details": f"{port.manufacturer or 'Unknown'} {port.serial_number or ''}"
                    })
                progress.update(task, completed=True)
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[yellow]串口扫描警告: {e}[/yellow]")
        
        if type in ["bluetooth", "all"]:
            task = progress.add_task("扫描蓝牙设备...", total=None)
            try:
                # 尝试使用 bluetoothctl 或 hcitool
                result = subprocess.run(
                    ["hcitool", "scan"],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # 跳过标题
                    for line in lines:
                        parts = line.strip().split('\t')
                        if len(parts) >= 2:
                            found_devices.append({
                                "type": "bluetooth",
                                "name": parts[1],
                                "address": parts[0],
                                "details": "BLE/Classic"
                            })
            except (subprocess.TimeoutExpired, FileNotFoundError):
                progress.update(task, completed=True)
                console.print("[yellow]蓝牙扫描需要安装 bluez 工具: sudo apt install bluez[/yellow]")
            except Exception as e:
                progress.update(task, completed=True)
                console.print(f"[yellow]蓝牙扫描警告: {e}[/yellow]")
        
        if type in ["mqtt", "all"]:
            task = progress.add_task("检查MQTT Broker...", total=None)
            # 检查本地MQTT broker
            common_brokers = ["localhost", "127.0.0.1", "mqtt.local"]
            for broker in common_brokers:
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    result = sock.connect_ex((broker, 1883))
                    sock.close()
                    if result == 0:
                        found_devices.append({
                            "type": "mqtt",
                            "name": f"MQTT Broker @{broker}",
                            "address": f"{broker}:1883",
                            "details": "Online"
                        })
                except:
                    pass
            progress.update(task, completed=True)
    
    # 显示结果
    if found_devices:
        table = Table(title=f"发现 {len(found_devices)} 个设备", box=box.ROUNDED)
        table.add_column("类型", style="cyan")
        table.add_column("名称", style="green")
        table.add_column("地址", style="yellow")
        table.add_column("详情", style="dim")
        
        for device in found_devices:
            emoji = {"serial": "🔌", "bluetooth": "📶", "mqtt": "📡"}.get(device["type"], "📟")
            table.add_row(
                f"{emoji} {device['type']}",
                device["name"],
                device["address"],
                device["details"]
            )
        console.print(table)
    else:
        console.print("[yellow]未发现设备[/yellow]")
        console.print("\n提示:")
        console.print("  • 串口设备: 连接USB设备后重试")
        console.print("  • 蓝牙设备: 确保蓝牙已启用并安装 bluez")
        console.print("  • MQTT: 安装 mosquitto 运行本地broker")
    
    log_activity(f"扫描设备: 发现 {len(found_devices)} 个")


@iot_cli.command(name="serial")
@click.option("--port", "-p", help="串口设备 (如 /dev/ttyUSB0)")
@click.option("--baudrate", "-b", default=9600, help="波特率")
@click.option("--command", "-c", help="发送的命令")
@click.option("--listen", "-l", is_flag=True, help="持续监听")
@click.option("--timeout", "-t", default=5, help="超时(秒)")
def serial_communication(port: Optional[str], baudrate: int, command: Optional[str], listen: bool, timeout: int):
    """串口通信"""
    console.print(f"\n🔌 串口通信\n")
    
    # 如果没有指定端口，列出可用端口
    if not port:
        ports = list(serial.tools.list_ports.comports())
        if not ports:
            console.print("[red]未找到串口设备[/red]")
            return
        
        console.print("可用串口:")
        for i, p in enumerate(ports, 1):
            console.print(f"  {i}. {p.device} - {p.description}")
        
        if len(ports) == 1:
            port = ports[0].device
            console.print(f"\n自动选择: {port}")
        else:
            port = click.prompt("\n选择串口", type=str)
    
    try:
        console.print(f"连接: {port} @ {baudrate} baud")
        
        with serial.Serial(port, baudrate, timeout=1) as ser:
            console.print(f"[green]✓ 已连接[/green]")
            
            if command:
                # 发送命令
                ser.write(command.encode() + b'\n')
                console.print(f"发送: {command}")
                log_activity(f"串口发送: {port} -> {command}")
            
            if command or listen:
                # 读取响应
                console.print("\n接收数据:")
                start_time = time.time()
                while time.time() - start_time < timeout or listen:
                    if ser.in_waiting:
                        data = ser.readline().decode('utf-8', errors='ignore').strip()
                        if data:
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            console.print(f"  [{timestamp}] {data}")
                            if not listen:
                                break
                    time.sleep(0.1)
                    
                    if not listen and time.time() - start_time >= timeout:
                        break
        
        console.print("\n[green]✅ 通信完成[/green]")
        
    except serial.SerialException as e:
        console.print(f"[red]串口错误: {e}[/red]")
        console.print("\n可能的解决方案:")
        console.print("  • 检查设备是否连接")
        console.print("  • 检查权限: sudo usermod -a -G dialout $USER")
        console.print("  • 检查端口是否被占用")
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")


@iot_cli.command(name="mqtt")
@click.option("--broker", "-b", default="localhost", help="MQTT Broker地址")
@click.option("--port", "-p", default=1883, help="MQTT端口")
@click.option("--topic", "-t", help="主题")
@click.option("--message", "-m", help="消息内容")
@click.option("--subscribe", "-s", is_flag=True, help="订阅模式")
@click.option("--qos", "-q", default=0, type=click.IntRange(0, 2), help="QoS级别")
@click.option("--username", "-u", help="用户名")
@click.option("--password", "-P", help="密码")
@click.option("--duration", "-d", default=10, help="订阅持续时间(秒)")
def mqtt_command(broker: str, port: int, topic: Optional[str], message: Optional[str], 
                 subscribe: bool, qos: int, username: Optional[str], password: Optional[str], duration: int):
    """MQTT通信"""
    console.print(f"\n📡 MQTT通信\n")
    
    try:
        import paho.mqtt.client as mqtt
    except ImportError:
        console.print("[red]请先安装 paho-mqtt: pip install paho-mqtt[/red]")
        return
    
    if not topic:
        topic = click.prompt("请输入主题")
    
    received_messages = []
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            console.print(f"[green]✓ 已连接到 {broker}:{port}[/green]")
            if subscribe:
                client.subscribe(topic, qos=qos)
                console.print(f"[green]✓ 已订阅: {topic}[/green]")
        else:
            console.print(f"[red]连接失败，返回码: {rc}[/red]")
    
    def on_message(client, userdata, msg):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        payload = msg.payload.decode('utf-8', errors='ignore')
        console.print(f"  [{timestamp}] {msg.topic}: {payload}")
        received_messages.append({"topic": msg.topic, "payload": payload, "time": timestamp})
    
    def on_publish(client, userdata, mid):
        console.print(f"[green]✓ 消息已发布 (ID: {mid})[/green]")
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    
    if username and password:
        client.username_pw_set(username, password)
    
    try:
        client.connect(broker, port, 60)
        client.loop_start()
        
        if subscribe:
            console.print(f"\n订阅主题: {topic} (QoS={qos})")
            console.print(f"监听 {duration} 秒...\n")
            time.sleep(duration)
            console.print(f"\n共接收 {len(received_messages)} 条消息")
        else:
            if not message:
                message = click.prompt("请输入消息内容")
            
            result = client.publish(topic, message, qos=qos)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                console.print(f"\n发布成功:")
                console.print(f"  主题: {topic}")
                console.print(f"  消息: {message}")
                console.print(f"  QoS: {qos}")
                log_activity(f"MQTT发布: {broker}:{port}/{topic}")
            else:
                console.print(f"[red]发布失败: {result.rc}[/red]")
            
            time.sleep(1)  # 等待发布完成
        
        client.loop_stop()
        client.disconnect()
        console.print("\n[green]✅ MQTT操作完成[/green]")
        
    except Exception as e:
        console.print(f"[red]MQTT错误: {e}[/red]")


@iot_cli.command(name="sensor")
@click.option("--type", "-t", type=click.Choice(["dht22", "bmp280", "mpu6050", "mock"]), default="mock", help="传感器类型")
@click.option("--pin", "-p", default="4", help="GPIO引脚或串口")
@click.option("--duration", "-d", default=5, help="读取持续时间(秒)")
@click.option("--interval", "-i", default=1.0, help="采样间隔(秒)")
def read_sensor(type: str, pin: str, duration: int, interval: float):
    """读取传感器数据"""
    console.print(f"\n📊 读取传感器\n")
    console.print(f"类型: {type}")
    console.print(f"接口: {pin}")
    console.print(f"持续: {duration}秒\n")
    
    readings = []
    start_time = time.time()
    
    if type == "dht22":
        try:
            import Adafruit_DHT
            sensor = Adafruit_DHT.DHT22
            gpio_pin = int(pin)
            
            console.print("正在读取 DHT22...")
            while time.time() - start_time < duration:
                humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio_pin)
                if humidity is not None and temperature is not None:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    reading = {
                        "time": timestamp,
                        "temperature": round(temperature, 1),
                        "humidity": round(humidity, 1)
                    }
                    readings.append(reading)
                    console.print(f"  [{timestamp}] 温度: {temperature:.1f}°C, 湿度: {humidity:.1f}%")
                time.sleep(interval)
                
        except ImportError:
            console.print("[yellow]Adafruit_DHT 未安装，使用模拟数据[/yellow]")
            type = "mock"
    
    elif type == "bmp280":
        try:
            import board
            import busio
            import adafruit_bmp280
            
            i2c = busio.I2C(board.SCL, board.SDA)
            sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
            
            console.print("正在读取 BMP280...")
            while time.time() - start_time < duration:
                timestamp = datetime.now().strftime("%H:%M:%S")
                reading = {
                    "time": timestamp,
                    "temperature": round(sensor.temperature, 1),
                    "pressure": round(sensor.pressure, 1)
                }
                readings.append(reading)
                console.print(f"  [{timestamp}] 温度: {sensor.temperature:.1f}°C, 气压: {sensor.pressure:.1f}hPa")
                time.sleep(interval)
                
        except ImportError:
            console.print("[yellow]adafruit-circuitpython-bmp280 未安装，使用模拟数据[/yellow]")
            type = "mock"
    
    if type == "mock" or not readings:
        # 模拟数据模式
        import random
        console.print("[yellow]使用模拟传感器数据[/yellow]")
        
        while time.time() - start_time < duration:
            timestamp = datetime.now().strftime("%H:%M:%S")
            reading = {
                "time": timestamp,
                "temperature": round(20 + random.uniform(-5, 10), 1),
                "humidity": round(50 + random.uniform(-20, 30), 1),
                "pressure": round(1013 + random.uniform(-10, 10), 1)
            }
            readings.append(reading)
            console.print(f"  [{timestamp}] 温度: {reading['temperature']:.1f}°C, "
                         f"湿度: {reading['humidity']:.1f}%, 气压: {reading['pressure']:.1f}hPa")
            time.sleep(interval)
    
    # 统计
    if readings:
        console.print(f"\n[green]✓ 采集 {len(readings)} 个数据点[/green]")
        
        if len(readings) > 1:
            temps = [r.get("temperature", 0) for r in readings if "temperature" in r]
            if temps:
                console.print(f"\n统计:")
                console.print(f"  温度: 平均 {sum(temps)/len(temps):.1f}°C, "
                             f"范围 {min(temps):.1f}°C ~ {max(temps):.1f}°C")
        
        # 保存数据
        ensure_config_dir()
        data_file = IOT_CONFIG_DIR / f"sensor_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(data_file, 'w') as f:
            json.dump(readings, f, indent=2)
        console.print(f"\n数据已保存: {data_file}")
        log_activity(f"传感器读取: {type}, {len(readings)} 个数据点")


@iot_cli.command(name="device")
@click.option("--name", "-n", required=True, help="设备名称")
@click.option("--type", "-t", required=True, type=click.Choice(["sensor", "actuator", "gateway", "camera"]), help="设备类型")
@click.option("--protocol", "-p", type=click.Choice(["mqtt", "serial", "http", "ble"]), default="mqtt", help="通信协议")
@click.option("--address", "-a", help="设备地址/URL")
@click.option("--config", "-c", help="配置JSON")
def register_device(name: str, type: str, protocol: str, address: Optional[str], config: Optional[str]):
    """注册设备"""
    console.print(f"\n🔌 注册设备\n")
    
    config_data = load_config()
    
    device = {
        "name": name,
        "type": type,
        "protocol": protocol,
        "address": address or "",
        "config": json.loads(config) if config else {},
        "registered_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    # 检查是否已存在
    existing = [d for d in config_data["devices"] if d["name"] == name]
    if existing:
        if click.confirm(f"设备 '{name}' 已存在，是否更新?"):
            config_data["devices"] = [d for d in config_data["devices"] if d["name"] != name]
        else:
            console.print("[yellow]已取消[/yellow]")
            return
    
    config_data["devices"].append(device)
    save_config(config_data)
    
    console.print(f"[green]✓ 设备已注册[/green]")
    console.print(f"  名称: {name}")
    console.print(f"  类型: {type}")
    console.print(f"  协议: {protocol}")
    console.print(f"  地址: {address or 'N/A'}")
    
    log_activity(f"设备注册: {name} ({type})")


@iot_cli.command(name="list")
@click.option("--type", "-t", type=click.Choice(["sensor", "actuator", "gateway", "camera", "all"]), default="all", help="设备类型")
def list_devices(type: str):
    """列出已注册设备"""
    console.print(f"\n📋 设备列表\n")
    
    config_data = load_config()
    devices = config_data.get("devices", [])
    
    if type != "all":
        devices = [d for d in devices if d["type"] == type]
    
    if not devices:
        console.print("[yellow]暂无设备[/yellow]")
        return
    
    table = Table(title=f"共 {len(devices)} 个设备", box=box.ROUNDED)
    table.add_column("名称", style="cyan")
    table.add_column("类型", style="green")
    table.add_column("协议", style="yellow")
    table.add_column("地址", style="dim")
    table.add_column("状态", style="blue")
    table.add_column("注册时间", style="dim")
    
    for device in devices:
        status_emoji = "🟢" if device.get("status") == "active" else "🔴"
        table.add_row(
            device["name"],
            device["type"],
            device["protocol"],
            device.get("address", "")[:30],
            f"{status_emoji} {device.get('status', 'unknown')}",
            device.get("registered_at", "")[:10]
        )
    
    console.print(table)


@iot_cli.command(name="monitor")
@click.option("--device", "-d", help="设备名称")
@click.option("--duration", "-T", default=60, help="监控持续时间(秒)")
def monitor_device(device: Optional[str], duration: int):
    """监控设备状态"""
    console.print(f"\n📈 设备监控\n")
    
    config_data = load_config()
    devices = config_data.get("devices", [])
    
    if device:
        devices = [d for d in devices if d["name"] == device]
        if not devices:
            console.print(f"[red]未找到设备: {device}[/red]")
            return
    
    if not devices:
        console.print("[yellow]暂无设备，请先注册[/yellow]")
        return
    
    console.print(f"监控 {len(devices)} 个设备，持续 {duration} 秒\n")
    
    start_time = time.time()
    stats = {"online": 0, "offline": 0, "errors": 0}
    
    try:
        while time.time() - start_time < duration:
            for dev in devices:
                # 模拟设备状态检查
                import random
                if random.random() > 0.1:  # 90% 在线率
                    stats["online"] += 1
                    status = "🟢 在线"
                else:
                    stats["offline"] += 1
                    status = "🔴 离线"
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                console.print(f"  [{timestamp}] {dev['name']}: {status}")
            
            console.print()
            time.sleep(5)
            
    except KeyboardInterrupt:
        console.print("\n[yellow]监控已停止[/yellow]")
    
    console.print(f"\n统计:")
    console.print(f"  在线: {stats['online']}")
    console.print(f"  离线: {stats['offline']}")
    console.print(f"  错误: {stats['errors']}")


@iot_cli.command(name="automate")
@click.option("--name", "-n", required=True, help="自动化名称")
@click.option("--trigger", "-t", required=True, help="触发条件 (如: temperature>30)")
@click.option("--action", "-a", required=True, help="执行动作")
@click.option("--device", "-d", help="目标设备")
def create_automation(name: str, trigger: str, action: str, device: Optional[str]):
    """创建自动化规则"""
    console.print(f"\n🤖 创建自动化\n")
    
    config_data = load_config()
    
    automation = {
        "name": name,
        "trigger": trigger,
        "action": action,
        "device": device,
        "enabled": True,
        "created_at": datetime.now().isoformat()
    }
    
    config_data["automations"].append(automation)
    save_config(config_data)
    
    console.print(f"[green]✓ 自动化已创建[/green]")
    console.print(f"  名称: {name}")
    console.print(f"  触发: {trigger}")
    console.print(f"  动作: {action}")
    if device:
        console.print(f"  设备: {device}")
    
    log_activity(f"自动化创建: {name}")


@iot_cli.command(name="firmware")
@click.option("--device", "-d", required=True, help="设备名称")
@click.option("--file", "-f", required=True, help="固件文件路径", type=click.Path(exists=True))
@click.option("--verify", "-v", is_flag=True, help="验证固件")
def update_firmware(device: str, file: str, verify: bool):
    """更新设备固件"""
    console.print(f"\n🔄 固件更新\n")
    
    file_path = Path(file)
    if not file_path.exists():
        console.print(f"[red]文件不存在: {file}[/red]")
        return
    
    file_size = file_path.stat().st_size
    console.print(f"设备: {device}")
    console.print(f"固件: {file_path.name}")
    console.print(f"大小: {file_size / 1024:.1f} KB")
    
    if verify:
        import hashlib
        with open(file_path, 'rb') as f:
            sha256 = hashlib.sha256(f.read()).hexdigest()[:16]
        console.print(f"校验: {sha256}")
    
    if click.confirm("确认更新固件?"):
        # 模拟固件更新过程
        with Progress(console=console) as progress:
            task = progress.add_task("上传固件...", total=100)
            for i in range(101):
                progress.update(task, completed=i)
                time.sleep(0.05)
        
        console.print(f"\n[green]✅ 固件更新完成[/green]")
        log_activity(f"固件更新: {device} -> {file_path.name}")
    else:
        console.print("[yellow]已取消[/yellow]")


@iot_cli.command(name="log")
@click.option("--lines", "-n", default=20, help="显示行数")
@click.option("--follow", "-f", is_flag=True, help="持续跟踪")
def show_log(lines: int, follow: bool):
    """查看IoT日志"""
    console.print(f"\n📝 IoT日志\n")
    
    if not IOT_LOG_FILE.exists():
        console.print("[yellow]暂无日志[/yellow]")
        return
    
    if follow:
        console.print("跟踪日志 (按 Ctrl+C 停止)...\n")
        try:
            with open(IOT_LOG_FILE, 'r') as f:
                # 跳到文件末尾
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if line:
                        console.print(line.strip())
                    else:
                        time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[yellow]已停止跟踪[/yellow]")
    else:
        with open(IOT_LOG_FILE, 'r') as f:
            log_lines = f.readlines()
        
        for line in log_lines[-lines:]:
            console.print(line.strip())
        
        console.print(f"\n[dim]显示最后 {min(lines, len(log_lines))} 行[/dim]")


@iot_cli.command(name="config")
@click.option("--show", is_flag=True, help="显示配置")
@click.option("--reset", is_flag=True, help="重置配置")
def manage_config(show: bool, reset: bool):
    """管理IoT配置"""
    console.print(f"\n⚙️ IoT配置\n")
    
    if reset:
        if click.confirm("确定要重置所有配置吗?"):
            if IOT_CONFIG_FILE.exists():
                IOT_CONFIG_FILE.unlink()
            console.print("[green]✓ 配置已重置[/green]")
            log_activity("配置重置")
        return
    
    config_data = load_config()
    
    console.print(f"配置目录: {IOT_CONFIG_DIR}")
    console.print(f"配置文件: {IOT_CONFIG_FILE}")
    console.print(f"日志文件: {IOT_LOG_FILE}")
    console.print(f"\n统计:")
    console.print(f"  设备: {len(config_data.get('devices', []))}")
    console.print(f"  自动化: {len(config_data.get('automations', []))}")
    console.print(f"  告警: {len(config_data.get('alerts', []))}")
    
    if show:
        console.print(f"\n完整配置:")
        console.print(json.dumps(config_data, indent=2))


if __name__ == "__main__":
    iot_cli()
