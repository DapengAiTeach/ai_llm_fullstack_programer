import sys
from loguru import logger

# 移除默认的 stderr 处理器（可选）
logger.remove()

# 添加控制台输出（带颜色，仅 INFO 及以上级别）
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
logger.add(
    "logs/log.json",
    serialize=True,  # 输出为 JSON 格式
    rotation="1 day",
    retention="30 days",
    compression="gz",
    encoding="utf-8",
    enqueue=True  # 线程安全队列，支持多进程/异步
)
