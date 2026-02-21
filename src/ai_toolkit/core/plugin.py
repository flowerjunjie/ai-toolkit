"""
插件系统
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import importlib.util
import sys
import json


class Plugin:
    """插件基类"""

    name: str = "Unnamed Plugin"
    version: str = "1.0.0"
    description: str = ""
    author: str = ""

    def __init__(self):
        """初始化插件"""
        self.enabled = True

    def on_load(self):
        """插件加载时调用"""
        pass

    def on_unload(self):
        """插件卸载时调用"""
        pass

    def on_command(self, command: str, *args, **kwargs):
        """
        命令处理

        Args:
            command: 命令名称
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            命令执行结果
        """
        pass


class PluginManager:
    """插件管理器"""

    def __init__(self):
        """初始化插件管理器"""
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_dirs: List[Path] = []

        # 默认插件目录
        self.add_plugin_dir(Path.home() / ".ai-toolkit" / "plugins")

    def add_plugin_dir(self, directory: Path):
        """
        添加插件目录

        Args:
            directory: 插件目录
        """
        if directory not in self.plugin_dirs:
            self.plugin_dirs.append(directory)

    def load_plugins(self):
        """加载所有插件"""
        for plugin_dir in self.plugin_dirs:
            if not plugin_dir.exists():
                continue

            for plugin_file in plugin_dir.glob("*.py"):
                if plugin_file.name.startswith("_"):
                    continue

                self.load_plugin(plugin_file)

    def load_plugin(self, plugin_file: Path):
        """
        加载单个插件

        Args:
            plugin_file: 插件文件路径
        """
        try:
            # 动态导入
            spec = importlib.util.spec_from_file_location(
                plugin_file.stem,
                plugin_file
            )
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_file.stem] = module
            spec.loader.exec_module(module)

            # 查找Plugin类
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Plugin)
                    and attr != Plugin
                ):
                    # 实例化插件
                    plugin_instance = attr()

                    # 注册插件
                    self.plugins[plugin_instance.name] = plugin_instance

                    # 调用加载回调
                    plugin_instance.on_load()

        except Exception as e:
            print(f"加载插件失败 {plugin_file}: {e}")

    def unload_plugin(self, name: str):
        """
        卸载插件

        Args:
            name: 插件名称
        """
        if name in self.plugins:
            plugin = self.plugins[name]
            plugin.on_unload()
            del self.plugins[name]

    def get_plugin(self, name: str) -> Optional[Plugin]:
        """
        获取插件

        Args:
            name: 插件名称

        Returns:
            插件实例
        """
        return self.plugins.get(name)

    def list_plugins(self) -> List[Dict[str, Any]]:
        """
        列出所有插件

        Returns:
            插件列表
        """
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "author": plugin.author,
                "enabled": plugin.enabled,
            }
            for plugin in self.plugins.values()
        ]

    def execute_command(self, command: str, *args, **kwargs):
        """
        执行插件命令

        Args:
            command: 命令
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            执行结果
        """
        results = []

        for plugin in self.plugins.values():
            if plugin.enabled:
                try:
                    result = plugin.on_command(command, *args, **kwargs)
                    if result is not None:
                        results.append({
                            "plugin": plugin.name,
                            "result": result,
                        })
                except Exception as e:
                    results.append({
                        "plugin": plugin.name,
                        "error": str(e),
                    })

        return results


# 全局插件管理器
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """获取全局插件管理器"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
        _plugin_manager.load_plugins()
    return _plugin_manager
