import sys
import os
import cv2

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem, QFileDialog, QGroupBox,
    QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt

from config.constants import (
    VIDEO_EXTENSIONS, FILE_SIZE_UNITS,
)
from entity.video_info import VideoInfo
from utils.format import format_duration, format_size

class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        # 当前选中的目录
        self.current_dir = ""
        # 当前的视频列表
        self.video_list: list[VideoInfo] = []
        # 初始化UI界面
        self.init_ui()

    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("智能视频统计工具")
        self.setGeometry(100, 100, 800, 600)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        self.setLayout(main_layout)

        ####################顶部区域开始##########################
        # 顶部区域，放置选择目录按钮
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        # 目录标签
        self.dir_label = QLabel("未选择目录")
        self.dir_label.setStyleSheet("color: gray;")
        top_layout.addWidget(self.dir_label)
        top_layout.addStretch()

        # 选择按钮
        self.select_btn = QPushButton("选择目录")
        self.select_btn.clicked.connect(self.select_directory)
        top_layout.addWidget(self.select_btn)

        # 刷新按钮
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_directory)
        top_layout.addWidget(self.refresh_btn)
        ####################顶部区域结束##########################

        ####################统计信息区域开始##########################
        stats_group = QGroupBox("统计信息")
        stats_layout = QHBoxLayout(stats_group)
        main_layout.addWidget(stats_group)

        self.stats_label = QLabel("视频数量：0 | 总时长：00:00:00 | 总大小：0 MB")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        ####################统计信息区域结束##########################

        ####################表格区域开始##########################
        # 创建表格
        self.table = QTableWidget()
        main_layout.addWidget(self.table)

        # 设置表格
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["序号", "文件名", "时长", "大小"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)

        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 60)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 100)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 100)
        ####################表格区域结束##########################

        ####################底部区域开始##########################
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        self.status_label = QLabel("就绪")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()

        self.export_btn = QPushButton("导出")
        self.export_btn.clicked.connect(self.export_list)
        bottom_layout.addWidget(self.export_btn)
        ####################底部区域结束##########################

    def select_directory(self):
        """选择目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择视频目录")
        if dir_path:
            self.current_dir = dir_path
            self.dir_label.setText(dir_path)
            self.dir_label.setStyleSheet("color: black;")
            self.scan_videos()

    def refresh_directory(self):
        """刷新目录"""
        if self.current_dir and os.path.exists(self.current_dir):
            self.scan_videos()
        else:
            self.dir_label.setText("未选择目录")
            self.dir_label.setStyleSheet("color: gray;")

    def export_list(self):
        """导出列表"""
        # 检查列表是否为空
        if not self.video_list:
            QMessageBox.information(self, "提示", "列表为空")
            return

        # 选择文件保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出视频列表",
            "目录.txt",
            "文本文件 (*.txt);;CSV文件 (*.csv)"
        )
        if not file_path:
            return
        print("文件保存路径:", file_path)

        # 获取后缀
        ext = ""
        try:
            ext = os.path.splitext(file_path)[1].lower()
        except Exception as e:
            print(e)
            return

        # 文本格式
        if ext == ".txt":
            with open(file_path, "w", encoding="utf-8") as f:
                for i, video in enumerate(self.video_list):
                    f.write(f"{video.filename}\n")
            self.status_label.setText("导出成功")
            QMessageBox.information(self, "提示", "导出成功")
        else:
            QMessageBox.warning(self, "错误", "不支持的文件格式")

    def update_table(self):
        """更新表格"""
        self.table.setRowCount(len(self.video_list))
        for i, video in enumerate(self.video_list):
            # 序号
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            # 文件名
            self.table.setItem(i, 1, QTableWidgetItem(video.filename))
            # 时长
            self.table.setItem(i, 2, QTableWidgetItem(video.duration_str))
            # 大小
            self.table.setItem(i, 3, QTableWidgetItem(video.size_str))

            # 居中对齐
            for col in [0, 2, 3]:
                item = self.table.item(i, col)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_stats(self):
        """更新统计信息"""
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
        self.stats_label.setText(summary_str)

    def scan_videos(self):
        """扫描目录下的视频"""
        self.status_label.setText("正在扫描...")
        self.video_list = []

        # 遍历目录获取视频文件
        for filename in os.listdir(self.current_dir):
            filepath = os.path.join(self.current_dir, filename)
            if os.path.isfile(filepath):
                ext = ""
                try:
                    ext = os.path.splitext(filename)[1].lower()
                except Exception as e:
                    self.status_label.setText("获取文件后缀失败")
                    print(e)
                if ext in VIDEO_EXTENSIONS:
                    try:
                        # TODO: 获取视频信息
                        vide_info = VideoInfo(filepath)
                        self.video_list.append(vide_info)
                    except Exception as e:
                        self.status_label.setText("获取视频信息失败")
                        print(e)

        # 按文件名排序
        self.video_list.sort(key=lambda x: x.filename.lower())

        # 更新界面
        self.update_table()
        self.update_stats()
        self.status_label.setText("扫描完成")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
