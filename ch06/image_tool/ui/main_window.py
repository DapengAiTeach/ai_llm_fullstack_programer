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
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # ===== 上方：图片预览区域 =====
        preview_group = QGroupBox("图片预览")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(10, 15, 10, 10)

        # 图片预览容器（带尺寸信息叠加）
        self.image_container = QWidget()
        self.image_container.setStyleSheet("background-color: #f5f5f5; border: 1px solid #ddd; border-radius: 4px;")
        image_container_layout = QVBoxLayout(self.image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel()
        self.image_label.setMinimumHeight(350)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setText("未选择图片")
        self.image_label.setStyleSheet("border: none; background: transparent;")
        image_container_layout.addWidget(self.image_label)
        
        preview_layout.addWidget(self.image_container)
        main_layout.addWidget(preview_group, stretch=3)

        # ===== 下方：控制面板区域 =====
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        control_layout.setSpacing(10)
        control_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(control_widget, stretch=1)

        # 使用水平布局放置设置项
        settings_layout = QHBoxLayout()
        control_layout.addLayout(settings_layout)

        # ===== 图片选择区域 =====
        file_group = QGroupBox("图片选择")
        file_layout = QHBoxLayout(file_group)
        file_layout.setSpacing(8)

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText("请选择要处理的图片...")
        self.file_input.setReadOnly(True)
        file_layout.addWidget(self.file_input)

        self.browse_btn = QPushButton("浏览...")
        self.browse_btn.setFixedWidth(80)
        self.browse_btn.clicked.connect(self.browse_image)
        file_layout.addWidget(self.browse_btn)

        settings_layout.addWidget(file_group, stretch=2)

        # ===== 尺寸设置区域 =====
        size_group = QGroupBox("尺寸设置")
        size_layout = QHBoxLayout(size_group)
        size_layout.setSpacing(15)

        # 预设选择
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("预设:"))
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("自定义")
        for preset_name in SIZE_PRESETS.keys():
            self.preset_combo.addItem(preset_name)
        self.preset_combo.currentTextChanged.connect(self.on_preset_changed)
        self.preset_combo.setFixedWidth(100)
        preset_layout.addWidget(self.preset_combo)
        size_layout.addLayout(preset_layout)

        # 宽度设置
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("宽度:"))
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 10000)
        self.width_spin.setValue(DEFAULT_IMAGE_WIDTH)
        self.width_spin.setSuffix(" px")
        self.width_spin.setFixedWidth(120)
        width_layout.addWidget(self.width_spin)
        size_layout.addLayout(width_layout)

        # 高度设置
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("高度:"))
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 10000)
        self.height_spin.setValue(DEFAULT_IMAGE_HEIGHT)
        self.height_spin.setSuffix(" px")
        self.height_spin.setFixedWidth(120)
        height_layout.addWidget(self.height_spin)
        size_layout.addLayout(height_layout)

        settings_layout.addWidget(size_group, stretch=3)

        # ===== 操作按钮区域 =====
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        control_layout.addLayout(button_layout)

        # 尺寸信息显示（底部居中）
        self.image_info_label = QLabel("")
        self.image_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_info_label.setStyleSheet("color: #666; font-size: 13px;")
        button_layout.addWidget(self.image_info_label)

        button_layout.addStretch()

        self.preview_btn = QPushButton("预览")
        self.preview_btn.setFixedWidth(100)
        self.preview_btn.clicked.connect(self.preview_image)
        self.preview_btn.setEnabled(False)
        button_layout.addWidget(self.preview_btn)

        self.save_btn = QPushButton("保存图片")
        self.save_btn.setFixedWidth(100)
        self.save_btn.clicked.connect(self.save_image)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)

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

        # 创建工作线程
        self.worker_thread = ImageResizeWorker(
            self.current_image_path,
            width,
            height,
            preview_only=True
        )
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

        # 创建工作线程
        self.worker_thread = ImageResizeWorker(
            self.current_image_path,
            width,
            height,
            output_path=file_path,
            preview_only=False
        )
        self.worker_thread.finished_signal.connect(self.handle_save_finished)
        self.worker_thread.start()

    def handle_preview_finished(self, success, message):
        """预览完成处理"""
        self.preview_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        if not success:
            QMessageBox.critical(self, "错误", f"处理失败: {message}")

    def handle_save_finished(self, success, message):
        """保存完成处理"""
        self.preview_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "完成", f"图片已成功保存到:\n{message}")
        else:
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
