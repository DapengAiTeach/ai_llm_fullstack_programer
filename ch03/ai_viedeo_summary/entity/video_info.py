import os
import cv2
from config.constants import FILE_SIZE_UNITS


class VideoInfo:
    """视频信息"""

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.size = os.path.getsize(filepath)
        self.duration = self._get_duration()

    def _get_duration(self) -> float:
        """获取视频时长(秒)"""
        try:
            cap = cv2.VideoCapture(self.filepath)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            cap.release()
            if fps > 0 and frame_count > 0:
                return frame_count / fps
            return 0
        except Exception as e:
            print(e)
            return 0

    @property
    def size_str(self) -> str:
        """格式化文件大小"""
        size = self.size
        for unit in FILE_SIZE_UNITS:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"

    @property
    def duration_str(self) -> str:
        """格式化视频时长"""
        total_seconds = int(self.duration)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
