from config.constants import FILE_SIZE_UNITS


def format_duration(duration_seconds: float) -> str:
    """
    格式化视频时长
    :param duration_seconds 时长，秒数
    :return 格式化之后的时间 08:08:08
    """
    total_seconds = int(duration_seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def format_size(size_bytes: int) -> str:
    """
    格式化文件大小
    :param size_bytes 文件大小，字节
    :return 格式化之后的文件大小 1.0 MB
    """
    size = size_bytes
    for unit in FILE_SIZE_UNITS:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"
