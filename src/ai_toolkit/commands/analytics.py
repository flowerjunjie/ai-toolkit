
"""
数据分析 - 真实集成版
真实使用Pandas处理数据
"""

import click
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import warnings

console = Console()

# 尝试导入可选依赖
pd = None
matplotlib = None
plt = None
BytesIO = None
base64 = None

try:
    import pandas as pd
except ImportError:
    warnings.warn("pandas未安装，analytics功能将不可用", ImportWarning)

try:
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
    from io import BytesIO
    import base64
except ImportError:
    warnings.warn("matplotlib未安装，绘图功能将不可用", ImportWarning)


@click.group(name="analytics")
def analytics_cli():
    """数据分析"""
    pass


def check_pandas():
    """检查pandas是否已安装"""
    if pd is None:
        console.print("\n❌ 错误: pandas未安装")
        console.print("请运行: pip install pandas matplotlib")
        return False
    return True


@analytics_cli.command(name="describe")
@click.option("--file", "-f", help="数据文件路径")
def describe_data(file):
    """描述性分析"""
    if not check_pandas():
        return

    console.print(f"\n📊 描述性分析\n")

    if not file:
        console.print("❌ 请提供数据文件路径")
        return

    console.print(f"文件: {file}")

    file_path = Path(file)
    if not file_path.exists():
        console.print(f"\n❌ 文件不存在: {file}")
        return

    try:
        console.print("\n加载数据...")

        # 读取数据
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        elif file_path.suffix == '.json':
            df = pd.read_json(file_path)
        else:
            console.print(f"\n❌ 不支持的文件格式: {file_path.suffix}")
            return

        console.print(f"\n✅ 数据加载成功！")
        console.print(f"行数: {len(df)}")
        console.print(f"列数: {len(df.columns)}")

        console.print(f"\n📋 数据描述:")
        console.print(df.describe())

        console.print(f"\n📊 前5行数据:")
        console.print(df.head())

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@analytics_cli.command(name="visualize")
@click.option("--file", "-f", help="数据文件路径")
@click.option("--column", "-c", help="要可视化的列")
@click.option("--type", "-t", default="histogram", help="图表类型 (histogram/scatter/line)")
def visualize_data(file, column, type):
    """数据可视化"""
    if not check_pandas():
        return

    if matplotlib is None or plt is None:
        console.print("\n❌ 错误: matplotlib未安装")
        console.print("请运行: pip install matplotlib")
        return

    console.print(f"\n📈 数据可视化\n")

    if not file or not column:
        console.print("❌ 请提供数据文件路径和要可视化的列")
        return

    console.print(f"文件: {file}")
    console.print(f"列: {column}")
    console.print(f"类型: {type}")

    file_path = Path(file)
    if not file_path.exists():
        console.print(f"\n❌ 文件不存在: {file}")
        return

    try:
        console.print("\n加载数据...")

        # 读取数据
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        if column not in df.columns:
            console.print(f"\n❌ 列不存在: {column}")
            return

        console.print(f"\n生成图表...")

        plt.figure(figsize=(10, 6))

        if type == 'histogram':
            df[column].hist(bins=30)
            plt.title(f'{column} - 直方图')
        elif type == 'scatter':
            plt.scatter(range(len(df)), df[column])
            plt.title(f'{column} - 散点图')
        elif type == 'line':
            plt.plot(df[column])
            plt.title(f'{column} - 折线图')
        else:
            console.print(f"\n❌ 不支持的图表类型: {type}")
            return

        plt.xlabel('索引')
        plt.ylabel(column)
        plt.tight_layout()

        # 保存图表
        output_file = f"{file_path.stem}_{column}_{type}.png"
        plt.savefig(output_file)
        console.print(f"\n✅ 图表已保存: {output_file}")

        plt.close()

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@analytics_cli.command(name="correlation")
@click.option("--file", "-f", help="数据文件路径")
def correlation_analysis(file):
    """相关性分析"""
    if not check_pandas():
        return

    console.print(f"\n🔗 相关性分析\n")

    if not file:
        console.print("❌ 请提供数据文件路径")
        return

    console.print(f"文件: {file}")

    file_path = Path(file)
    if not file_path.exists():
        console.print(f"\n❌ 文件不存在: {file}")
        return

    try:
        console.print("\n加载数据...")

        # 读取数据
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        console.print(f"\n📊 相关性矩阵:")
        corr_matrix = df.select_dtypes(include=['number']).corr()
        console.print(corr_matrix)

        console.print(f"\n✅ 相关性分析完成！")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@analytics_cli.command(name="report")
@click.option("--file", "-f", help="数据文件路径")
@click.option("--output", "-o", help="输出报告文件")
def generate_report(file, output):
    """生成分析报告"""
    if not check_pandas():
        return

    console.print(f"\n📋 生成分析报告\n")

    if not file:
        console.print("❌ 请提供数据文件路径")
        return

    console.print(f"文件: {file}")

    if output:
        console.print(f"输出: {output}")

    file_path = Path(file)
    if not file_path.exists():
        console.print(f"\n❌ 文件不存在: {file}")
        return

    try:
        console.print("\n加载数据...")

        # 读取数据
        if file_path.suffix == '.csv':
            df = pd.read_csv(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)

        console.print(f"\n✅ 数据加载成功！")
        console.print(f"行数: {len(df)}")
        console.print(f"列数: {len(df.columns)}")

        console.print(f"\n📊 数据概览:")
        console.print(df.info())

        console.print(f"\n📋 数据描述:")
        console.print(df.describe())

        console.print(f"\n✅ 报告生成完成！")

        # 保存报告
        if output:
            report_content = f"""
# 数据分析报告

## 文件信息
- 文件: {file}
- 行数: {len(df)}
- 列数: {len(df.columns)}

## 数据描述
{df.describe().to_string()}
            """
            with open(output, 'w', encoding='utf-8') as f:
                f.write(report_content)
            console.print(f"\n✅ 报告已保存: {output}")

    except Exception as e:
        console.print(f"\n❌ 错误: {e}")


@analytics_cli.command(name="help")
def analytics_help():
    """帮助信息"""
    console.print(f"\n📖 数据分析帮助\n")

    console.print("快速开始:")
    console.print("  1. 安装依赖:")
    console.print("     pip install pandas matplotlib openpyxl")
    console.print("")
    console.print("  2. 描述性分析:")
    console.print("     ai-toolkit analytics describe --file data.csv")
    console.print("")
    console.print("  3. 数据可视化:")
    console.print("     ai-toolkit analytics visualize --file data.csv --column age")
    console.print("")
    console.print("  4. 相关性分析:")
    console.print("     ai-toolkit analytics correlation --file data.csv")
    console.print("")
    console.print("  5. 生成报告:")
    console.print("     ai-toolkit analytics report --file data.csv --output report.md")

    console.print("\n✅ 帮助信息显示完成")
