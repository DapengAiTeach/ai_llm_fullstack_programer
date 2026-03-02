from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class MessageRole(Enum):
    """消息角色"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    """聊天消息实体"""
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    is_streaming: bool = False
    
    def to_dict(self) -> dict:
        """转换为API格式"""
        return {
            "role": self.role.value,
            "content": self.content
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "ChatMessage":
        """从字典创建"""
        return cls(
            role=MessageRole(data.get("role", "user")),
            content=data.get("content", "")
        )
    
    @classmethod
    def create_user_message(cls, content: str) -> "ChatMessage":
        """创建用户消息"""
        return cls(role=MessageRole.USER, content=content)
    
    @classmethod
    def create_assistant_message(cls, content: str = "") -> "ChatMessage":
        """创建助手消息"""
        return cls(role=MessageRole.ASSISTANT, content=content, is_streaming=True)
    
    @classmethod
    def create_system_message(cls, content: str) -> "ChatMessage":
        """创建系统消息"""
        return cls(role=MessageRole.SYSTEM, content=content)
