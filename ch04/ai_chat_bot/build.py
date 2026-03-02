#!/usr/bin/env python3
"""
PyQt6 简洁打包脚本

用法:
    python build.py              # 默认打包（目录模式，推荐）
    python build.py --onefile    # 单文件模式
    python build.py --clean      # 清理后打包
    python build.py --console    # 显示控制台窗口（调试用）
"""

import os
import sys
import shutil
import subprocess

# ==================== 配置区域（按需修改）====================
APP_NAME = "VideoStatsTool"           # 应用名称
MAIN_SCRIPT = "main.py"               # 入口文件
ICON_FILE = ""                        # 图标路径，如 "assets/icon.ico"
ONEFILE = False                       # True=单文件, False=目录（推荐）
CONSOLE = False                       # True=显示控制台, False=仅窗口（调试用）
# ==========================================================


def clean():
    """清理构建目录"""
    for d in ["build", "dist", "__pycache__"]:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"[清理] {d}")
    for f in os.listdir("."):
        if f.endswith(".spec"):
            os.remove(f)
            print(f"[清理] {f}")


def build():
    """执行打包"""
    print(f"开始打包: {APP_NAME}\n")
    
    # 安装 pyinstaller（如未安装）
    try:
        subprocess.run(["pyinstaller", "--version"], capture_output=True, check=True)
    except:
        print("[安装] PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # 构建命令
    cmd = [
        "pyinstaller",
        MAIN_SCRIPT,
        "--name", APP_NAME,
        "--noconfirm",
        "--clean",
        "--onedir" if not ONEFILE else "--onefile",
        "--console" if CONSOLE else "--windowed",
    ]
    
    # 图标
    if ICON_FILE and os.path.exists(ICON_FILE):
        cmd.extend(["--icon", ICON_FILE])
    
    # 隐藏导入 - 包含所有项目模块
    hidden_imports = [
        # PyQt6
        "PyQt6.sip",
        "PyQt6.QtCore",
        "PyQt6.QtGui",
        "PyQt6.QtWidgets",
        # 第三方库
        "cv2",
        "loguru",
        # 项目模块（关键！）
        "config",
        "config.constants",
        "config.loguru",
        "entity",
        "entity.video_info",
        "services",
        "services.video_service",
        "ui",
        "ui.main_window",
        "utils",
        "utils.format",
        "utils.resource",
    ]
    
    for imp in hidden_imports:
        cmd.extend(["--hidden-import", imp])
    
    # 收集所有子模块（确保所有包都被包含）
    collect_modules = ["config", "entity", "services", "ui", "utils"]
    for mod in collect_modules:
        cmd.extend(["--collect-submodules", mod])
    
    # 包含项目目录
    sep = ";" if sys.platform == "win32" else ":"
    for d in ["config", "entity", "services", "ui", "utils"]:
        if os.path.exists(d):
            cmd.extend(["--add-data", f"{d}{sep}{d}"])
    
    # 排除无用模块（减小体积）
    for exc in ["pytest", "unittest", "tkinter", "matplotlib", "scipy", "pandas"]:
        cmd.extend(["--exclude-module", exc])
    
    # 执行
    print(f"[执行] {' '.join(cmd)}\n")
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        exe_path = os.path.join("dist", f"{APP_NAME}.exe" if ONEFILE else f"{APP_NAME}/{APP_NAME}.exe")
        print(f"\n✅ 打包成功: {os.path.abspath(exe_path)}")
        if os.path.exists(exe_path):
            print(f"📦 大小: {os.path.getsize(exe_path)/1024/1024:.1f} MB")
        return True
    else:
        print("\n❌ 打包失败")
        return False


def main():
    global ONEFILE, CONSOLE
    
    # 解析参数
    for arg in sys.argv[1:]:
        if arg == "--clean":
            clean()
        elif arg == "--onefile":
            ONEFILE = True
        elif arg == "--console":
            CONSOLE = True
    
    print(f"[模式] {'单文件' if ONEFILE else '目录'} | {'控制台' if CONSOLE else '窗口'}\n")
    
    sys.exit(0 if build() else 1)


if __name__ == "__main__":
    main()
