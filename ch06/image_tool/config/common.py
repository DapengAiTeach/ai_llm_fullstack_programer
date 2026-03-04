import sys
import os

def get_app_dir():
    """
    获取当前app的目录
    """
    if getattr(sys, 'frozen', False):
        # Pyinstaller 打包后的环境
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
