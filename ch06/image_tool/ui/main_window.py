import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QFileDialog, QMessageBox,
    QSpinBox, QGroupBox, QSplitter,
)
from PyQt6.QtGui import QPixmap
from services import ImageResizeWorker
from config import logger, SUPPORTED_IMAGE_EXTENSIONS, DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT


class MainWindow(QMainWindow):
    """图像尺寸修改工具主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("图像尺寸修改工具")
        self.setMinimumSize(900, 600)
        self.worker_thread = None
        self.current_image_path = None
        self.preview_image_path = None
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 使用分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # 左侧控制面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(15)
        splitter.addWidget(left_panel)

        # 右侧预览面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        splitter.addWidget(right_panel)

        splitter.setSizes([350, 550])

        # ===== 左侧：图片选择区域 =====
        file_group = QGroupBox("图片选择")
        file_layout = QHBoxLayout(file_group)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("请选择要处理的图片...")
        self.file_input.setReadOnly(True)
        file_layout.addWidget(self.file_input)

        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.clicked.connect(self.browse_image)
        file_layout.addWidget(self.browse_btn)

        left_layout.addWidget(file_group)

        # ===== 左侧：尺寸设置区域 =====
        size_group = QGroupBox("尺寸设置")
        size_layout = QVBoxLayout(size_group)

        # 宽度设置
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("宽度:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(DEFAULT_IMAGE_WIDTH)
        self.width_spin.setSuffix(" px")
        width_layout.addWidget(self.width_spin)
        width_layout.addStretch()
        size_layout.addLayout(width_layout)

        # 高度设置
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("高度:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(DEFAULT_IMAGE_HEIGHT)
        self.height_spin.setSuffix(" px")
        height_layout.addWidget(self.height_spin)
        height_layout.addStretch()
        size_layout.addLayout(height_layout)

        left_layout.addWidget(size_group)

        # ===== 左侧：操作按钮区域 =====
        button_layout = QHBoxLayout()

        self.preview_btn = QPushButton("预览")
        self.preview_btn.clicked.connect(self.preview_image)
        self.preview_btn.setEnabled(False)
        button_layout.addWidget(self.preview_btn)

        self.save_btn = QPushButton("保存图片")
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

        left_layout.addLayout(button_layout)

        # ===== 左侧：日志区域 =====
        log_group = QGroupBox("处理日志")
        log_layout = QVBoxLayout(log_group)

        self.log_label = QLabel("就绪")
        log_layout.addWidget(self.log_label)

        left_layout.addWidget(log_group)
        left_layout.addStretch()

        # ===== 右侧：图片预览区域 =====
        preview_group = QGroupBox("图片预览")
        preview_layout = QVBoxLayout(preview_group)

        # 原始图片标签
        original_label = QLabel("原始图片:")
        preview_layout.addWidget(original_label)

        self.original_image_label = QLabel()
        self.original_image_label.setMinimumHeight(200)
        self.original_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.original_image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.original_image_label.setText("未选择图片")
        preview_layout.addWidget(self.original_image_label)

        # 处理后的图片标签
        resized_label = QLabel("调整后预览:")
        preview_layout.addWidget(resized_label)

        self.resized_image_label = QLabel()
        self.resized_image_label.setMinimumHeight(200)
        self.resized_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resized_image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.resized_image_label.setText("点击预览按钮查看效果")
        preview_layout.addWidget(self.resized_image_label)

        right_layout.addWidget(preview_group)

    def browse_image(self):
        """浏览并选择图片"""
        file_filter = "图片文件 (" + " ".join([f"*{ext}" for ext in SUPPORTED_IMAGE_EXTENSIONS]) + ")"
        
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片",
            "",
            file_filter
        )
        
        if file_path:
            self.current_image_path = file_path
            self.file_input.setText(file_path)
            self.preview_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            self.log_label.setText(f"已选择图片: {Path(file_path).name}")
            logger.info(f"选择的图片: {file_path}")
            
            # 显示原始图片
            self.display_original_image(file_path)

    def display_original_image(self, image_path):
        """显示原始图片"""
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            # 缩放以适应标签大小，保持比例
            scaled_pixmap = pixmap.scaled(
                self.original_image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.original_image_label.setPixmap(scaled_pixmap)
            
            # 显示尺寸信息
            self.log_label.setText(f"原始尺寸: {pixmap.width()} x {pixmap.height()}")

    def preview_image(self):
        """预览调整后的图片"""
        if not self.current_image_path:
            QMessageBox.warning(self, "错误", "请先选择图片")
            return

        width = self.width_spin.value()
        height = self.height_spin.value()

        self.preview_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.log_label.setText("正在处理...")

        # 创建工作线程
        self.worker_thread = ImageResizeWorker(
            self.current_image_path,
            width,
            height,
            preview_only=True
        )
        self.worker_thread.log_signal.connect(self.update_log)
        self.worker_thread.preview_signal.connect(self.display_preview_image)
        self.worker_thread.finished_signal.connect(self.handle_preview_finished)
        self.worker_thread.start()

    def display_preview_image(self, image_path):
        """显示预览图片"""
        self.preview_image_path = image_path
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.resized_image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.resized_image_label.setPixmap(scaled_pixmap)

    def save_image(self):
        """保存调整后的图片"""
        if not self.current_image_path:
            QMessageBox.warning(self, "错误", "请先选择图片")
            return

        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            str(Path(self.current_image_path).parent / f"{Path(self.current_image_path).stem}_resized{Path(self.current_image_path).suffix}"),
            "图片文件 (" + " ".join([f"*{ext}" for ext in SUPPORTED_IMAGE_EXTENSIONS]) + ")"
        )

        if not file_path:
            return

        width = self.width_spin.value()
        height = self.height_spin.value()

        self.preview_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.log_label.setText("正在保存...")

        # 创建工作线程
        self.worker_thread = ImageResizeWorker(
            self.current_image_path,
            width,
            height,
            output_path=file_path,
            preview_only=False
        )
        self.worker_thread.log_signal.connect(self.update_log)
        self.worker_thread.finished_signal.connect(self.handle_save_finished)
        self.worker_thread.start()

    def update_log(self, message):
        """更新日志"""
        self.log_label.setText(message)

    def handle_preview_finished(self, success, message):
        """预览完成处理"""
        self.preview_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        if success:
            self.log_label.setText("预览生成完成")
        else:
            self.log_label.setText(f"处理失败: {message}")
            QMessageBox.critical(self, "错误", f"处理失败: {message}")

    def handle_save_finished(self, success, message):
        """保存完成处理"""
        self.preview_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        if success:
            self.log_label.setText(f"图片已保存: {message}")
            QMessageBox.information(self, "完成", f"图片已成功保存到:\n{message}")
        else:
            self.log_label.setText(f"保存失败: {message}")
            QMessageBox.critical(self, "错误", f"保存失败: {message}")

    def resizeEvent(self, event):
        """窗口大小改变时重新缩放图片"""
        super().resizeEvent(event)
        if self.current_image_path:
            self.display_original_image(self.current_image_path)
        if self.preview_image_path:
            self.display_preview_image(self.preview_image_path)

    def closeEvent(self, event):
        """优雅关闭窗口"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            logger.info("已关闭处理线程")
        event.accept()
