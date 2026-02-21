# CLI主文件更新 - 添加market和revenue命令

from ai_toolkit.commands.market import market_cli
from ai_toolkit.commands.revenue import revenue_cli

# 在main函数中添加
main.add_command(market_cli)
main.add_command(revenue_cli)
