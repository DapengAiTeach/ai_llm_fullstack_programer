import os
import copy
from entity.video_info import VideoInfo
from config.constants import VIDEO_EXTENSIONS
from config.loguru import logger
from utils.format import format_size, format_duration


class VideService:
    """
    视频处理业务逻辑类
    负责处理视频扫描，统计计算，导出等功能
    """

    def __init__(self):
        # 当前选中的目录
        self.current_dir = ""
        # 当前的视频列表
        self.video_list: list[VideoInfo] = []

    def set_directory(self, directory: str):
        """
        设置当前目录
        :param directory: 目录路径
        """
        self.current_dir = directory

    def scan_videos(self):
        """扫描目录下的视频"""
        # 判断扫描的目录是否存在
        if not self.current_dir or not os.path.exists(self.current_dir):
            return [], "目录不存在"

        logger.info(f"开始扫描目录 {self.current_dir} 下的视频")

        # 重置视频列表，防止重复
        self.video_list.clear()

        # 错误信息
        message = ""

        # 遍历目录获取视频文件
        for filename in os.listdir(self.current_dir):
            filepath = os.path.join(self.current_dir, filename)
            if os.path.isfile(filepath):
                ext = ""
                try:
                    ext = os.path.splitext(filename)[1].lower()
                except Exception as e:
                    message = "获取文件后缀失败"
                    logger.critical(e)
                if ext in VIDEO_EXTENSIONS:
                    try:
                        # 获取视频信息
                        vide_info = VideoInfo(filepath)
                        self.video_list.append(vide_info)
                    except Exception as e:
                        message = "获取视频信息失败"
                        logger.critical(e)
        # 按文件名排序
        self.video_list.sort(key=lambda x: x.filename.lower())
        logger.info(f"视频扫描并排序完成，共扫描到 {len(self.video_list)} 个视频文件")

        # 返回
        video_list = copy.deepcopy(self.video_list)
        return video_list, message

    def get_summary(self):
        """获取视频列表的统计信息"""
        # 数据统计
        count = len(self.video_list)
        total_duration = sum([video.duration for video in self.video_list])
        total_size = sum([video.size for video in self.video_list])

        # 格式化总时长
        total_duration_str = format_duration(int(total_duration))
        # 格式化总大小
        total_size_str = format_size(total_size)

        # 更新统计信息
        summary_str = f"视频数量：{count} | 总时长：{total_duration_str} | 总大小：{total_size_str}"

        # 返回
        return summary_str

    def export_txt(self, file_path):
        """导出列表为txt文件"""
        with open(file_path, "w", encoding="utf-8") as f:
            for i, video in enumerate(self.video_list):
                f.write(f"{video.filename}\n")
