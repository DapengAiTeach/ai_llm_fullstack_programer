import os
import sys
import shutil
import subprocess

# 配置
APP_NAME = "AdRemoverTool"
MAIN_SCRIPT = "main.py"
ICON_FILE = ""

# 清理构建目录
for d in ["build", "dist", "__pycache__"]:
    if os.path.exists(d):
        shutil.rmtree(d)
        print(f"已清理目录: {d}")
print("已清理所有构建目录，开始打包...")

# 构建命令
cmd = [
    "pyinstaller",
    MAIN_SCRIPT,
    "--name", APP_NAME,
    "--noconfirm",
    "--clean",
    "--onedir",
    "--windowed",
]

# 图标
if ICON_FILE and os.path.exists(ICON_FILE):
    cmd.extend(["--icon", ICON_FILE])

# 隐藏导入，包含所有项目模块
hidden_imports = [
    # PyQt6
    "PyQt6.sip",
    "PyQt6.QtCore",
    "PyQt6.QtGui",
    "PyQt6.QtWidgets",
    # 第三方库
    "loguru",
    # 项目模块
    "config",
    "config.common",
    "config.constants",
    "config.loguru",
    "services",
    "services.ad_remover_worker",
    "ui",
    "ui.main_window",
]
for imp in hidden_imports:
    cmd.extend(["--hidden-import", imp])

# 收集所有子模块
collect_modules = ["config", "services", "ui"]
for mod in collect_modules:
    cmd.extend(["--collect-submodules", mod])

# 包含项目目录
sep = ";" if sys.platform == "win32" else ":"
for d in ["config", "services", "ui"]:
    if os.path.exists(d):
        cmd.extend(["--add-data", f"{d}{sep}{d}"])

# 执行命令
print("执行命令：", " ".join(cmd))
result = subprocess.run(cmd)
if result.returncode == 0:
    print(f"打包完成：dist/{APP_NAME}")
    print(f"运行方式：dist/{APP_NAME}/{APP_NAME}.exe")
else:
    print("打包失败")
sys.exit(result.returncode)