import os
import sys
from loguru import logger
from .common import get_app_dir

# 确保日志目录存在
log_dir = os.path.join(get_app_dir(), "logs")
log_file_suffix = ".jsonl"  # .jsonl/.log
os.makedirs(log_dir, exist_ok=True)

# 添加控制台日志输出,带颜色,仅 INFO 及以上级别
# 在打包后可能没有控制台,需要检查 sys.stdout 是否为 None
if sys.stdout is not None:
    log_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                  "<level>{level: <8}</level> | "
                  "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                  "<level>{message}</level>")
    logger.add(sys.stdout, format=log_format, level="INFO", colorize=True)

# 添加生产环境的日志文件配置
if log_file_suffix == ".jsonl":
    log_file = os.path.join(log_dir, "app.jsonl")
    logger.add(
        log_file,
        serialize=True,  # 启用 JSON 格式
        rotation="1 day",  # 按天轮转
        retention="30 days",  # 保留 30 天
        compression="gz",  # 压缩
        encoding="utf-8",  # 编码
        enqueue=True,  # 启用多线程
    )
elif log_file_suffix == ".log":
    text_log_file = os.path.join(log_dir, "app.log")
    logger.add(
        text_log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="1 day",
        retention="30 days",
        compression="gz",
        encoding="utf-8",
        enqueue=True,
    )
