import os
from typing import List, Optional, Callable

from openai import OpenAI
from PyQt6.QtCore import QObject, pyqtSignal, QThread

from entity.chat_message import ChatMessage, MessageRole
from config.loguru import logger


class ChatWorker(QThread):
    """聊天工作线程 - 处理流式API请求"""
    
    # 信号：收到新内容块
    content_received = pyqtSignal(str)
    # 信号：流式传输完成
    stream_finished = pyqtSignal()
    # 信号：发生错误
    error_occurred = pyqtSignal(str)
    
    def __init__(self, client: OpenAI, model: str, messages: List[dict]):
        super().__init__()
        self.client = client
        self.model = model
        self.messages = messages
        self._is_running = True
    
    def run(self):
        """执行流式请求"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True
            )
            
            for chunk in stream:
                if not self._is_running:
                    break
                    
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    self.content_received.emit(content)
            
            if self._is_running:
                self.stream_finished.emit()
                
        except Exception as e:
            logger.error(f"流式请求错误: {e}")
            self.error_occurred.emit(str(e))
    
    def stop(self):
        """停止线程"""
        self._is_running = False
        self.wait(1000)


class ChatService(QObject):
    """聊天服务 - 管理OpenAI API通信"""
    
    # 信号：收到新内容
    content_received = pyqtSignal(str)
    # 信号：回复完成
    response_completed = pyqtSignal()
    # 信号：发生错误
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.client: Optional[OpenAI] = None
        self.model: str = ""
        self.messages: List[ChatMessage] = []
        self._worker: Optional[ChatWorker] = None
        self._load_config()
    
    def _load_config(self):
        """从环境变量加载配置"""
        from dotenv import load_dotenv
        load_dotenv(".env")
        
        base_url = os.getenv("OPENAI_BASE_URL")
        api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("MODEL", "gpt-3.5-turbo")
        
        if base_url and api_key:
            self.client = OpenAI(
                base_url=base_url,
                api_key=api_key
            )
            logger.info(f"ChatService初始化完成，模型: {self.model}")
        else:
            logger.warning("未找到OpenAI配置，请在.env文件中设置")
    
    def is_configured(self) -> bool:
        """检查是否已配置"""
        return self.client is not None
    
    def set_system_prompt(self, prompt: str):
        """设置系统提示词"""
        # 移除旧的系统消息
        self.messages = [m for m in self.messages if m.role != MessageRole.SYSTEM]
        # 添加新的系统消息
        self.messages.insert(0, ChatMessage.create_system_message(prompt))
    
    def send_message(self, content: str) -> ChatMessage:
        """
        发送消息并启动流式接收
        返回：助手的消息对象（初始为空，内容会通过信号逐步填充）
        """
        if not self.client:
            raise RuntimeError("ChatService未配置，请检查.env文件")
        
        # 添加用户消息
        user_message = ChatMessage.create_user_message(content)
        self.messages.append(user_message)
        
        # 创建助手消息（流式接收）
        assistant_message = ChatMessage.create_assistant_message("")
        
        # 启动工作线程
        self._start_stream(assistant_message)
        
        return assistant_message
    
    def _start_stream(self, assistant_message: ChatMessage):
        """启动流式请求"""
        # 停止之前的工作线程
        if self._worker and self._worker.isRunning():
            self._worker.stop()
        
        # 准备消息列表（排除正在流式传输的消息）
        api_messages = [m.to_dict() for m in self.messages if not m.is_streaming]
        
        # 创建并启动工作线程
        self._worker = ChatWorker(self.client, self.model, api_messages)
        self._worker.content_received.connect(self._on_content_received)
        self._worker.stream_finished.connect(self._on_stream_finished)
        self._worker.error_occurred.connect(self._on_error)
        self._worker.start()
        
        self._current_assistant_message = assistant_message
    
    def _on_content_received(self, content: str):
        """处理收到的内容块"""
        self._current_assistant_message.content += content
        self.content_received.emit(content)
    
    def _on_stream_finished(self):
        """处理流式传输完成"""
        self._current_assistant_message.is_streaming = False
        self.messages.append(self._current_assistant_message)
        self.response_completed.emit()
    
    def _on_error(self, error_msg: str):
        """处理错误"""
        self.error_occurred.emit(error_msg)
    
    def clear_history(self):
        """清空对话历史（保留系统消息）"""
        system_messages = [m for m in self.messages if m.role == MessageRole.SYSTEM]
        self.messages = system_messages
    
    def stop_generation(self):
        """停止生成"""
        if self._worker and self._worker.isRunning():
            self._worker.stop()
            self._current_assistant_message.is_streaming = False
