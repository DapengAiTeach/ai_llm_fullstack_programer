import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QFileDialog, QMessageBox,
    QSpinBox, QGroupBox, QSplitter,
    QComboBox,
)
from PyQt6.QtGui import QPixmap
from services import ImageResizeWorker
from config import logger, SUPPORTED_IMAGE_EXTENSIONS, DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT, SIZE_PRESETS


class MainWindow(QMainWindow):
    """图像尺寸修改工具主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("图像尺寸修改工具")
        self.setMinimumSize(800, 600)
        self.worker_thread = None
        self.current_image_path = None
        self.preview_image_path = None
        self.is_showing_preview = False
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

        splitter.setSizes([300, 500])

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

        # 预设选择
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("预设:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("自定义")
        for preset_name in SIZE_PRESETS.keys():
            self.preset_combo.addItem(preset_name)
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addStretch()
        size_layout.addLayout(preset_layout)

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

        # ===== 右侧：图片预览区域（单张图片）=====
        preview_group = QGroupBox("图片预览")
        preview_layout = QVBoxLayout(preview_group)

        # 图片预览标签
        self.image_label = QLabel()
        self.image_label.setMinimumHeight(400)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        self.image_label.setText("未选择图片")
        preview_layout.addWidget(self.image_label)

        # 图片尺寸信息
        self.image_info_label = QLabel("")
        self.image_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.image_info_label)

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
            self.preview_image_path = None
            self.is_showing_preview = False
            self.file_input.setText(file_path)
            self.preview_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            logger.info(f"选择的图片: {file_path}")
            
            # 显示原始图片
            self.display_image(file_path, is_preview=False)

    def display_image(self, image_path, is_preview=False):
        """显示图片"""
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        # 缩放以适应标签大小，保持比例
        label_size = self.image_label.size()
        scaled_pixmap = pixmap.scaled(
            label_size.width() - 20,
            label_size.height() - 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(scaled_pixmap)

        # 更新尺寸信息
        if is_preview:
            self.image_info_label.setText(f"调整后尺寸: {pixmap.width()} x {pixmap.height()}")
        else:
            self.image_info_label.setText(f"原始尺寸: {pixmap.width()} x {pixmap.height()}")
            # 自动设置目标尺寸为原始尺寸
            self.width_spin.setValue(pixmap.width())
            self.height_spin.setValue(pixmap.height())

        self.log_label.setText(f"图片: {Path(image_path).name}")

    def on_preset_changed(self, preset_name):
        """尺寸预设选择改变"""
        if preset_name in SIZE_PRESETS:
            width, height = SIZE_PRESETS[preset_name]
            self.width_spin.setValue(width)
            self.height_spin.setValue(height)

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
        self.worker_thread.preview_signal.connect(self.on_preview_ready)
        self.worker_thread.finished_signal.connect(self.handle_preview_finished)
        self.worker_thread.start()

    def on_preview_ready(self, image_path):
        """预览图片生成完成"""
        self.preview_image_path = image_path
        self.display_image(image_path, is_preview=True)

    def save_image(self):
        """保存调整后的图片"""
        if not self.current_image_path:
            QMessageBox.warning(self, "错误", "请先选择图片")
            return

        # 选择保存路径
        width = self.width_spin.value()
        height = self.height_spin.value()
        default_name = f"{Path(self.current_image_path).stem}_{width}_{height}{Path(self.current_image_path).suffix}"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存图片",
            str(Path(self.current_image_path).parent / default_name),
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
        if self.is_showing_preview and self.preview_image_path:
            self.display_image(self.preview_image_path, is_preview=True)
        elif self.current_image_path:
            self.display_image(self.current_image_path, is_preview=False)

    def closeEvent(self, event):
        """优雅关闭窗口"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.stop()
            logger.info("已关闭处理线程")
        event.accept()
