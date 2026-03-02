from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QMessageBox,
    QSplitter
)
from PyQt6.QtCore import Qt

from ui.chat_bubble import ChatBubble, ChatMessageList
from ui.chat_input import ChatInput
from services.chat_service import ChatService
from entity.chat_message import ChatMessage, MessageRole
from config.loguru import logger


class MainWindow(QMainWindow):
    """AI聊天主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化聊天服务
        self.chat_service = ChatService()
        
        # 当前正在流式显示的消息气泡
        self.current_bubble: ChatBubble = None
        
        # 初始化UI
        self.init_ui()
        
        # 连接信号
        self.connect_signals()
        
        # 检查配置
        self.check_configuration()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("AI 聊天助手")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(600, 400)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ==================== 顶部工具栏 ====================
        toolbar = QWidget()
        toolbar.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border-bottom: 1px solid #DDDDDD;
            }
        """)
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(15, 10, 15, 10)
        
        # 标题
        self.title_label = QLabel("AI 聊天助手")
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
        """)
        toolbar_layout.addWidget(self.title_label)
        
        toolbar_layout.addStretch()
        
        # 清空按钮
        self.clear_btn = QPushButton("清空对话")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #666666;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                color: #333333;
            }
        """)
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        toolbar_layout.addWidget(self.clear_btn)
        
        main_layout.addWidget(toolbar)
        
        # ==================== 消息列表区域 ====================
        # 滚动区域
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #F0F0F0;
            }
            QScrollBar:vertical {
                background-color: #F0F0F0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #CCCCCC;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #AAAAAA;
            }
        """)
        
        # 消息列表
        self.message_list = ChatMessageList()
        self.scroll_area.setWidget(self.message_list)
        
        main_layout.addWidget(self.scroll_area, stretch=1)
        
        # ==================== 输入区域 ====================
        self.chat_input = ChatInput()
        self.chat_input.setStyleSheet("""
            ChatInput {
                background-color: #FFFFFF;
                border-top: 1px solid #DDDDDD;
            }
        """)
        main_layout.addWidget(self.chat_input)
        
        # ==================== 状态栏 ====================
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 12px;
                padding: 5px 15px;
            }
        """)
        main_layout.addWidget(self.status_label)
    
    def connect_signals(self):
        """连接信号"""
        # 输入组件信号
        self.chat_input.message_sent.connect(self.on_message_sent)
        self.chat_input.stop_requested.connect(self.on_stop_requested)
        
        # 聊天服务信号
        self.chat_service.content_received.connect(self.on_content_received)
        self.chat_service.response_completed.connect(self.on_response_completed)
        self.chat_service.error_occurred.connect(self.on_error_occurred)
        
        # 工具栏按钮
        self.clear_btn.clicked.connect(self.on_clear_clicked)
    
    def check_configuration(self):
        """检查配置"""
        if not self.chat_service.is_configured():
            QMessageBox.warning(
                self,
                "配置警告",
                "未找到OpenAI配置，请在项目根目录创建 .env 文件并设置以下变量：\n\n"
                "OPENAI_BASE_URL=你的API地址\n"
                "OPENAI_API_KEY=你的API密钥\n"
                "MODEL=gpt-3.5-turbo"
            )
        else:
            # 设置系统提示词
            self.chat_service.set_system_prompt(
                "你是一个友好、专业的AI助手。请用简洁、清晰的语言回答用户的问题。"
            )
            # 添加欢迎消息
            self.add_system_message("欢迎使用 AI 聊天助手！")
    
    def on_message_sent(self, text: str):
        """用户发送消息"""
        try:
            # 添加用户消息到界面
            user_message = ChatMessage.create_user_message(text)
            self.message_list.add_message(user_message)
            self.scroll_to_bottom()
            
            # 设置输入为生成状态
            self.chat_input.set_generating_state(True)
            self.status_label.setText("AI 思考中...")
            
            # 发送消息并获取助手消息对象
            assistant_message = self.chat_service.send_message(text)
            
            # 在界面添加助手消息气泡（初始为空）
            self.current_bubble = self.message_list.add_message(assistant_message)
            self.scroll_to_bottom()
            
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            QMessageBox.critical(self, "错误", f"发送消息失败: {e}")
            self.chat_input.set_generating_state(False)
    
    def on_content_received(self, content: str):
        """收到流式内容"""
        if self.current_bubble:
            self.current_bubble.append_content(content)
            self.scroll_to_bottom()
    
    def on_response_completed(self):
        """响应完成"""
        self.chat_input.set_generating_state(False)
        self.status_label.setText("就绪")
        self.current_bubble = None
    
    def on_error_occurred(self, error_msg: str):
        """发生错误"""
        self.chat_input.set_generating_state(False)
        self.status_label.setText("错误")
        self.add_system_message(f"错误: {error_msg}")
        QMessageBox.critical(self, "错误", f"请求失败: {error_msg}")
    
    def on_stop_requested(self):
        """停止生成"""
        self.chat_service.stop_generation()
        self.status_label.setText("已停止")
    
    def on_clear_clicked(self):
        """清空对话"""
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有对话记录吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.message_list.clear_messages()
            self.chat_service.clear_history()
            self.add_system_message("对话已清空")
    
    def add_system_message(self, text: str):
        """添加系统消息"""
        message = ChatMessage.create_system_message(text)
        self.message_list.add_message(message)
        self.scroll_to_bottom()
    
    def scroll_to_bottom(self):
        """滚动到底部"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
