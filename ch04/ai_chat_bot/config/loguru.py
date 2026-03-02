import os
import sys
from pathlib import Path
from loguru import logger

# 获取应用根目录（开发环境和打包环境通用）
def get_app_dir():
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的环境
        return os.path.dirname(sys.executable)
    else:
        # 开发环境
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 确保日志目录存在
log_dir = os.path.join(get_app_dir(), "logs")
os.makedirs(log_dir, exist_ok=True)

# 移除默认的 stderr 处理器
logger.remove()

# 添加控制台输出（带颜色，仅 INFO 及以上级别）
# 在打包后可能无控制台，需要检查 sys.stdout
if sys.stdout is not None:
    log_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                  "<level>{level: <8}</level> | "
                  "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                  "<level>{message}</level>")
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )

# 添加文件输出（JSON 格式，用于日志分析系统）
log_file = os.path.join(log_dir, "log.json")
logger.add(
    log_file,
    serialize=True,  # 输出为 JSON 格式
    rotation="1 day",
    retention="30 days",
    compression="gz",
    encoding="utf-8",
    enqueue=True  # 线程安全队列，支持多进程/异步
)
