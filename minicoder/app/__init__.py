"""MiniCoder Textual/TUI 入口模块。"""

from minicoder.app.factory import create_minicoder_app
from minicoder.app.tui import MiniCoderApp, MiniCoderTuiConfig

__all__ = ["MiniCoderApp", "MiniCoderTuiConfig", "create_minicoder_app"]
