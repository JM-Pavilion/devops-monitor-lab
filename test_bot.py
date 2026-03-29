#test_bot.py
import pytest
from bot import TARGETS # 从你的主程序里导入监控目标

def test_targets_url_format():
    """检查所有的监控网址是否以 http 开头，且没有奇怪的结尾点"""
    for name, url in TARGETS.items():
        # 1.检查是否以 http 或 https 开头
        assert url.startswith("http"), f"错误： {name} 的网址格式不对！"

        # 2.检查末尾是否有多余的点（防止前天的错误再次发生）
        assert not url.endswith("."), f"错误： {name} 的网址末尾不应该有点！"

def test_targets_not_empty():
    """检查监控列表是不是空的"""
    assert len(TARGETS) > 0,"错误： 监控列表不能为空！"


