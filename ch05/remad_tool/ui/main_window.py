import sys
from pathlib import Path
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QPlainTextEdit, QProgressBar,
    QFileDialog, QMessageBox,
)
from services import AdRemoverWorker
from config import logger, DEFAULT_AD_PATTERNS


class MainWindow(QMainWindow):
    """去广告工具主窗口"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("去广告工具")
        self.setMinimumSize(700, 500)
        self.worker_thread = None
        self.ad_patterns = DEFAULT_AD_PATTERNS
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        ######################中央部件开始######################
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        ######################中央部件结束######################

        ######################顶部目录选择开始######################
        dir_layout = QHBoxLayout()
        main_layout.addLayout(dir_layout)

        dir_label = QLabel("目标目录:")
        dir_layout.addWidget(dir_label)

        self.dir_input = QLineEdit()
        self.dir_input.setPlaceholderText("请选择要处理的目录...")
        dir_layout.addWidget(self.dir_input, 1)

        self.browse_btn = QPushButton("浏览")
        self.browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.browse_btn)
        ######################顶部目录选择结束######################

        ######################广告词模式选择区域开始######################
        patterns_label = QLabel("广告词匹配规则:")
        main_layout.addWidget(patterns_label)

        self.patterns_text = QPlainTextEdit()
        self.patterns_text.setPlainText("\n".join(self.ad_patterns))
        self.patterns_text.setMaximumHeight(120)
        main_layout.addWidget(self.patterns_text)
        ######################广告词模式选择区域结束######################

        ######################操作按钮区域开始######################
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        button_layout.addStretch()

        self.remove_btn = QPushButton("移除广告")
        self.remove_btn.clicked.connect(self.remove_advertisements)
        button_layout.addWidget(self.remove_btn)

        self.clear_btn = QPushButton("清空日志")
        self.clear_btn.clicked.connect(self.clear_log)
        button_layout.addWidget(self.clear_btn)

        button_layout.addStretch()
        ######################操作按钮区域结束######################

        ######################进度条区域开始######################
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        ######################进度条区域结束######################

        ######################日志显示区域开始######################
        log_label = QLabel("处理日志:")
        main_layout.addWidget(log_label)

        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text, 1)
        ######################日志显示区域结束######################

        ######################状态栏区域开始######################
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(self.status_label)
        ######################状态栏区域结束######################

    def browse_directory(self):
        """浏览目录"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "选择要处理的目录",
            "",
            QFileDialog.Option.ShowDirsOnly,
        )
        if directory:
            self.dir_input.setText(directory)
            logger.info(f"选择的目录: {directory}")

    def remove_advertisements(self):
        """移除广告"""
        # 获取用户选择的目录
        directory = self.dir_input.text().strip()
        if not directory:
            QMessageBox.warning(self, "错误", "请选择要处理的目录")
            return
        if not Path(directory).exists():
            QMessageBox.warning(self, "错误", "指定的目录不存在")
            return

        # 更新广告词模式
        patterns_text = self.patterns_text.toPlainText().strip()
        if patterns_text:
            self.ad_patterns = [p.strip() for p in patterns_text.split("\n") if p.strip()]
        else:
            self.ad_patterns = DEFAULT_AD_PATTERNS

        # 开始处理目录
        self.remove_btn.setEnabled(False)
        self.browse_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.status_label.setText("处理中...")
        self.log_text.appendPlainText(f"开始处理目录: {directory}")
        self.log_text.appendPlainText(f"广告词匹配规则数量: {len(self.ad_patterns)}")
        self.log_text.appendPlainText("-" * 30)
        logger.info(f"开始处理目录: {directory}")

        # 创建并启动工作线程
        self.worker_thread = AdRemoverWorker(directory, self.ad_patterns)
        self.worker_thread.log_signal.connect(self.append_log)
        self.worker_thread.progress_signal.connect(self.update_progress)
        self.worker_thread.finished_signal.connect(self.handle_finished)
        self.worker_thread.start()

    def clear_log(self):
        """清空日志"""
        self.log_text.clear()
        self.status_label.setText("日志已清空")
        logger.info("已清空日志")

    def append_log(self, log):
        """追加日志"""
        self.log_text.appendPlainText(log)

    def update_progress(self, progress):
        """更新进度"""
        self.progress_bar.setValue(progress)

    def handle_finished(self, total_items, renamed_count):
        """处理完成"""
        self.remove_btn.setEnabled(True)
        self.browse_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        self.status_label.setText(f"处理完成：{total_items} 项目, {renamed_count} 重命名")
        self.log_text.appendPlainText("-" * 30)
        self.log_text.appendPlainText(f"处理完成, 共处理 {total_items} 个项目, 重命名了 {renamed_count} 个项目")
        logger.info(f"处理完成, 共处理 {total_items} 个项目, 重命名了 {renamed_count} 个项目")
        QMessageBox.information(self, "完成", f"处理完成, 共处理 {total_items} 个项目, 重命名了 {renamed_count} 个项目")

    def closeEvent(self, event):
        """优雅关闭窗口"""
        if self.worker_thread and self.worker_thread.isRunning():
            self.worker_thread.terminate()
            self.worker_thread.wait()
            logger.info("已关闭处理线程")
        event.accept()
