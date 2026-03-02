import re
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit
)
from PyQt6.QtCore import Qt

from entity.chat_message import ChatMessage, MessageRole


class ChatBubble(QWidget):
    """聊天气泡组件 - 紧凑布局，占满宽度"""
    
    def __init__(self, message: ChatMessage, parent=None):
        super().__init__(parent)
        self.message = message
        self.init_ui()
    
    def init_ui(self):
        """初始化UI - 所有消息左对齐，占满宽度"""
        # 根据角色选择颜色
        if self.message.role == MessageRole.USER:
            bg_color = "#E3F2FD"  # 浅蓝
            text_color = "#1565C0"
            role_name = "我"
        elif self.message.role == MessageRole.ASSISTANT:
            bg_color = "#FFFFFF"  # 白色
            text_color = "#333333"
            role_name = "AI"
        else:
            bg_color = "#FFF3CD"  # 浅黄
            text_color = "#856404"
            role_name = "系统"
        
        # 主布局 - 紧凑
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 2, 8, 2)  # 极小边距
        main_layout.setSpacing(0)
        
        # 创建内容容器
        container = QWidget()
        container.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 6px;
                border: 1px solid #E0E0E0;
            }}
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 6, 8, 6)  # 紧凑内边距
        layout.setSpacing(2)  # 极小间距
        
        # 头部：角色名 + 操作按钮区域
        header = QHBoxLayout()
        header.setSpacing(0)
        header.setContentsMargins(0, 0, 0, 0)
        
        role_label = QLabel(role_name)
        role_label.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: 11px;
                font-weight: bold;
            }}
        """)
        header.addWidget(role_label)
        header.addStretch()
        layout.addLayout(header)
        
        # 内容区域
        self.content_edit = QTextEdit()
        self.content_edit.setReadOnly(True)
        self.content_edit.setFrameStyle(0)
        self.content_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.content_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # 转换并显示
        html_content = self._markdown_to_html(self.message.content)
        self.content_edit.setHtml(html_content)
        
        self.content_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: transparent;
                color: {text_color};
                border: none;
                font-size: 14px;
                line-height: 1.5;
                padding: 0px;
            }}
        """)
        
        layout.addWidget(self.content_edit)
        main_layout.addWidget(container)
        
        # 调整高度
        self._adjust_height()
    
    def _markdown_to_html(self, text: str) -> str:
        """Markdown 转 HTML"""
        if not text:
            return ""
        
        # 转义
        text = text.replace("&", "&")
        text = text.replace("<", "<")
        text = text.replace(">", ">")
        
        # 粗体
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        # 斜体
        text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
        # 行内代码
        text = re.sub(r'`(.+?)`', r'<code style="background:#f0f0f0;padding:1px 3px;border-radius:2px;font-family:monospace;font-size:12px;">\1</code>', text)
        # 代码块
        text = re.sub(r'```(\w*)\n(.*?)```', self._format_code_block, text, flags=re.DOTALL)
        
        # 标题
        text = re.sub(r'### (.+)', r'<div style="font-weight:bold;margin:6px 0 3px 0;">\1</div>', text)
        text = re.sub(r'## (.+)', r'<div style="font-weight:bold;font-size:15px;margin:8px 0 4px 0;">\1</div>', text)
        text = re.sub(r'# (.+)', r'<div style="font-weight:bold;font-size:16px;margin:10px 0 5px 0;">\1</div>', text)
        
        # 列表
        lines = text.split('\n')
        result_lines = []
        in_list = False
        
        for line in lines:
            if re.match(r'^[\s]*[-\*\+]\s+', line):
                if not in_list:
                    result_lines.append('<ul style="margin:3px 0;padding-left:18px;">')
                    in_list = True
                content = re.sub(r'^[\s]*[-\*\+]\s+', '', line)
                result_lines.append(f'<li style="margin:1px 0;">{content}</li>')
            else:
                if in_list:
                    result_lines.append('</ul>')
                    in_list = False
                result_lines.append(line)
        
        if in_list:
            result_lines.append('</ul>')
        
        text = '\n'.join(result_lines)
        text = text.replace('\n', '<br>')
        
        return f'<div style="line-height:1.5;">{text}</div>'
    
    def _format_code_block(self, match) -> str:
        """格式化代码块"""
        code = match.group(2)
        return f'<div style="background:#f5f5f5;border-radius:4px;padding:8px;margin:6px 0;overflow-x:auto;"><pre style="margin:0;font-family:monospace;font-size:12px;line-height:1.4;"><code>{code}</code></pre></div>'
    
    def _adjust_height(self):
        """根据内容调整高度"""
        doc = self.content_edit.document()
        doc.setTextWidth(self.content_edit.viewport().width())
        height = doc.size().height() + 3
        self.content_edit.setFixedHeight(int(max(height, 20)))
    
    def append_content(self, text: str):
        """追加内容"""
        self.message.content += text
        html_content = self._markdown_to_html(self.message.content)
        self.content_edit.setHtml(html_content)
        self._adjust_height()


class ChatMessageList(QWidget):
    """聊天消息列表"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.bubbles: list[ChatBubble] = []
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)  # 消息之间小间距
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    def add_message(self, message: ChatMessage) -> ChatBubble:
        """添加新消息"""
        bubble = ChatBubble(message)
        self.bubbles.append(bubble)
        self.main_layout.addWidget(bubble)
        return bubble
    
    def clear_messages(self):
        """清空所有消息"""
        for bubble in self.bubbles:
            bubble.deleteLater()
        self.bubbles.clear()
