"""资源路径工具 - 解决 PyInstaller 打包后的路径问题"""

import os
import sys


def resource_path(relative_path: str) -> str:
    """获取资源文件绝对路径（开发/打包环境通用）"""
    # PyInstaller 打包后的临时目录
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)
