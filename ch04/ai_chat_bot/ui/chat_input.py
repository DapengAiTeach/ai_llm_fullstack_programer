from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeyEvent


class ChatInput(QWidget):
    """聊天输入组件 - 包含输入框和发送按钮"""
    
    # 信号：发送消息
    message_sent = pyqtSignal(str)
    # 信号：停止生成
    stop_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_generating = False
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # 输入框区域
        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)
        
        # 多行文本输入框
        self.input_edit = QTextEdit()
        self.input_edit.setPlaceholderText("输入消息... (按 Enter 发送，Shift+Enter 换行)")
        self.input_edit.setMaximumHeight(100)
        self.input_edit.setStyleSheet("""
            QTextEdit {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                background-color: #FFFFFF;
            }
            QTextEdit:focus {
                border: 2px solid #4A90D9;
            }
        """)
        input_layout.addWidget(self.input_edit, stretch=1)
        
        # 按钮区域
        button_layout = QVBoxLayout()
        button_layout.setSpacing(5)
        
        # 发送按钮
        self.send_btn = QPushButton("发送")
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A90D9;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357ABD;
            }
            QPushButton:pressed {
                background-color: #2E6DA4;
            }
            QPushButton:disabled {
                background-color: #CCCCCC;
                color: #666666;
            }
        """)
        self.send_btn.setFixedHeight(40)
        self.send_btn.clicked.connect(self.on_send_clicked)
        button_layout.addWidget(self.send_btn)
        
        # 停止按钮（初始隐藏）
        self.stop_btn = QPushButton("停止")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:pressed {
                background-color: #BD2130;
            }
        """)
        self.stop_btn.setFixedHeight(40)
        self.stop_btn.clicked.connect(self.on_stop_clicked)
        self.stop_btn.hide()
        button_layout.addWidget(self.stop_btn)
        
        input_layout.addLayout(button_layout)
        layout.addLayout(input_layout)
        
        # 提示标签
        self.hint_label = QLabel("按 Enter 发送，Shift+Enter 换行")
        self.hint_label.setStyleSheet("""
            QLabel {
                color: #888888;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.hint_label)
    
    def keyPressEvent(self, event: QKeyEvent):
        """处理键盘事件"""
        # 检查是否是输入框的焦点
        if self.input_edit.hasFocus():
            # Enter 发送，Shift+Enter 换行
            if event.key() == Qt.Key.Key_Return and not event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                self.on_send_clicked()
                return
        super().keyPressEvent(event)
    
    def on_send_clicked(self):
        """发送按钮点击"""
        text = self.input_edit.toPlainText().strip()
        if text and not self.is_generating:
            self.input_edit.clear()
            self.message_sent.emit(text)
    
    def on_stop_clicked(self):
        """停止按钮点击"""
        self.stop_requested.emit()
        self.set_generating_state(False)
    
    def set_generating_state(self, is_generating: bool):
        """设置生成状态"""
        self.is_generating = is_generating
        
        if is_generating:
            self.send_btn.hide()
            self.stop_btn.show()
            self.input_edit.setEnabled(False)
            self.hint_label.setText("AI 正在回复中...")
        else:
            self.stop_btn.hide()
            self.send_btn.show()
            self.input_edit.setEnabled(True)
            self.input_edit.setFocus()
            self.hint_label.setText("按 Enter 发送，Shift+Enter 换行")
    
    def get_input_text(self) -> str:
        """获取输入文本"""
        return self.input_edit.toPlainText().strip()
    
    def clear_input(self):
        """清空输入"""
        self.input_edit.clear()
