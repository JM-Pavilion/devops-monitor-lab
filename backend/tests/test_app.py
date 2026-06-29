# tests/test_app.py
import sys
import os

# 让 pytest 能找到 backend/monitor/app.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from monitor.app import TARGETS


def test_targets_url_format():
    """所有监控目标的 URL 必须以 http 开头，且不以点结尾"""
    for name, url in TARGETS.items():
        assert url.startswith("http"), f"错误：{name} 的网址格式不对！"
        assert not url.endswith("."), f"错误：{name} 的网址末尾不应该有点！"


def test_targets_not_empty():
    """监控列表不能为空"""
    assert len(TARGETS) > 0, "错误：监控列表不能为空！"
