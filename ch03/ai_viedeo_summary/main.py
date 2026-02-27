import sys
import os
import cv2

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QFileDialog, QGroupBox, QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt


class VideoInfo:
    """视频信息类"""
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.size = os.path.getsize(filepath)
        self.duration = self._get_duration()
    
    def _get_duration(self) -> float:
        """获取视频时长（秒）"""
        try:
            cap = cv2.VideoCapture(self.filepath)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            cap.release()
            if fps > 0 and frame_count > 0:
                return frame_count / fps
            return 0
        except Exception:
            return 0
    
    @property
    def size_str(self) -> str:
        """格式化文件大小"""
        size = self.size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    
    @property
    def duration_str(self) -> str:
        """格式化时长"""
        total_seconds = int(self.duration)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


class VideoStatsTool(QMainWindow):
    """视频统计工具主窗口"""
    
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'}
    
    def __init__(self):
        super().__init__()
        self.current_dir = ""
        self.video_list = []
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("视频统计工具")
        self.setGeometry(100, 100, 800, 600)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # ===== 顶部区域：目录选择 =====
        top_layout = QHBoxLayout()
        
        self.dir_label = QLabel("未选择目录")
        self.dir_label.setStyleSheet("color: gray;")
        top_layout.addWidget(self.dir_label)
        top_layout.addStretch()
        
        self.select_btn = QPushButton("选择目录")
        self.select_btn.clicked.connect(self.select_directory)
        top_layout.addWidget(self.select_btn)
        
        self.refresh_btn = QPushButton("刷新")
        self.refresh_btn.clicked.connect(self.refresh_directory)
        top_layout.addWidget(self.refresh_btn)
        
        main_layout.addLayout(top_layout)
        
        # ===== 统计信息区域 =====
        stats_group = QGroupBox("统计信息")
        stats_layout = QHBoxLayout(stats_group)
        
        self.stats_label = QLabel("视频数量: 0  |  总时长: 00:00:00  |  总大小: 0 MB")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        
        main_layout.addWidget(stats_group)
        
        # ===== 表格区域 =====
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["序号", "文件名", "时长", "大小"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 60)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        
        main_layout.addWidget(self.table)
        
        # ===== 底部区域 =====
        bottom_layout = QHBoxLayout()
        
        self.status_label = QLabel("就绪")
        bottom_layout.addWidget(self.status_label)
        bottom_layout.addStretch()
        
        self.export_btn = QPushButton("导出列表")
        self.export_btn.clicked.connect(self.export_list)
        bottom_layout.addWidget(self.export_btn)
        
        main_layout.addLayout(bottom_layout)
    
    def select_directory(self):
        """选择目录"""
        dir_path = QFileDialog.getExistingDirectory(self, "选择视频目录")
        if dir_path:
            self.current_dir = dir_path
            self.dir_label.setText(dir_path)
            self.dir_label.setStyleSheet("color: black;")
            self.scan_videos()
    
    def refresh_directory(self):
        """刷新当前目录"""
        if self.current_dir and os.path.exists(self.current_dir):
            self.scan_videos()
        else:
            self.status_label.setText("请先选择目录")
    
    def scan_videos(self):
        """扫描目录中的视频文件"""
        self.status_label.setText("正在扫描...")
        self.video_list = []
        
        try:
            # 遍历目录获取视频文件
            for filename in os.listdir(self.current_dir):
                filepath = os.path.join(self.current_dir, filename)
                if os.path.isfile(filepath):
                    ext = os.path.splitext(filename)[1].lower()
                    if ext in self.VIDEO_EXTENSIONS:
                        try:
                            video_info = VideoInfo(filepath)
                            self.video_list.append(video_info)
                        except Exception as e:
                            print(f"读取视频失败 {filepath}: {e}")
            
            # 按文件名排序
            self.video_list.sort(key=lambda x: x.filename.lower())
            
            # 更新界面
            self.update_table()
            self.update_stats()
            self.status_label.setText(f"扫描完成，共找到 {len(self.video_list)} 个视频")
            
        except Exception as e:
            self.status_label.setText(f"扫描出错: {e}")
    
    def update_table(self):
        """更新表格显示"""
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
        count = len(self.video_list)
        total_duration = sum(v.duration for v in self.video_list)
        total_size = sum(v.size for v in self.video_list)
        
        # 格式化总时长
        total_seconds = int(total_duration)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # 格式化总大小
        size = total_size
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                size_str = f"{size:.2f} {unit}"
                break
            size /= 1024
        else:
            size_str = f"{size:.2f} PB"
        
        self.stats_label.setText(f"视频数量: {count}  |  总时长: {duration_str}  |  总大小: {size_str}")
    
    def export_list(self):
        """导出列表到文件"""
        if not self.video_list:
            QMessageBox.information(self, "提示", "没有可导出的数据")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "导出列表", "视频列表.txt", "文本文件 (*.txt);;CSV文件 (*.csv)"
        )
        
        if not filepath:
            return
        
        try:
            ext = os.path.splitext(filepath)[1].lower()
            
            if ext == '.csv':
                # CSV 格式
                import csv
                with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                    writer = csv.writer(f)
                    writer.writerow(['序号', '文件名', '时长', '大小'])
                    for i, video in enumerate(self.video_list, 1):
                        writer.writerow([i, video.filename, video.duration_str, video.size_str])
            else:
                # 文本格式
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write("视频文件列表\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(f"目录: {self.current_dir}\n")
                    f.write(f"视频数量: {len(self.video_list)}\n")
                    
                    # 计算统计信息
                    total_duration = sum(v.duration for v in self.video_list)
                    total_size = sum(v.size for v in self.video_list)
                    
                    total_seconds = int(total_duration)
                    hours = total_seconds // 3600
                    minutes = (total_seconds % 3600) // 60
                    seconds = total_seconds % 60
                    f.write(f"总时长: {hours:02d}:{minutes:02d}:{seconds:02d}\n")
                    
                    size = total_size
                    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
                        if size < 1024:
                            f.write(f"总大小: {size:.2f} {unit}\n")
                            break
                        size /= 1024
                    
                    f.write("\n" + "=" * 80 + "\n\n")
                    f.write(f"{'序号':<6}{'文件名':<40}{'时长':<12}{'大小':<15}\n")
                    f.write("-" * 80 + "\n")
                    
                    for i, video in enumerate(self.video_list, 1):
                        filename = video.filename[:38] if len(video.filename) > 38 else video.filename
                        f.write(f"{i:<6}{filename:<40}{video.duration_str:<12}{video.size_str:<15}\n")
            
            self.status_label.setText(f"已导出到: {filepath}")
            QMessageBox.information(self, "成功", "列表导出成功！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导出失败: {e}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = VideoStatsTool()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
