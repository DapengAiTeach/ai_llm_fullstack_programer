"""
用户模型模块 - 使用 SQLModel
"""
from datetime import datetime
from typing import Optional
import secrets
import hashlib
from sqlmodel import SQLModel, Field


def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    return hashlib.sha256(password.encode()).hexdigest()


def generate_key() -> str:
    """生成随机的激活密钥"""
    return secrets.token_urlsafe(32)


class User(SQLModel, table=True):
    """
    用户模型类
    
    对应数据库表 user
    """
    __tablename__ = "user"
    
    # 主键：用户名
    username: str = Field(primary_key=True, description="用户名")
    
    # 密码（存储为哈希值）
    password: str = Field(description="密码哈希值")
    
    # 是否激活
    active: bool = Field(default=False, description="是否激活")
    
    # 用于激活用户的密钥
    key: str = Field(default_factory=generate_key, description="激活密钥")
    
    # 上次登录时间
    login_time: Optional[datetime] = Field(default=None, description="上次登录时间")
    
    # 添加时间
    add_time: datetime = Field(default_factory=datetime.now, description="添加时间")
    
    # 修改时间
    update_time: datetime = Field(default_factory=datetime.now, description="修改时间")
    
    # 昵称，默认为用户名
    nickname: str = Field(default=None, description="昵称")
    
    # 头像地址
    avatar: str = Field(default="", description="头像地址")
    
    def __init__(self, **data):
        # 如果没有提供 nickname，默认为 username
        if "nickname" not in data or data.get("nickname") is None:
            data["nickname"] = data.get("username", "")
        super().__init__(**data)
    
    def verify_password(self, password: str) -> bool:
        """验证密码是否正确"""
        return self.password == hash_password(password)
    
    def set_password(self, password: str):
        """设置密码（自动哈希）"""
        self.password = hash_password(password)
    
    def activate(self, key: str) -> bool:
        """
        激活用户
        
        Args:
            key: 激活密钥
            
        Returns:
            bool: 激活成功返回True，密钥错误返回False
        """
        if self.key == key:
            self.active = True
            self.update_time = datetime.now()
            return True
        return False
    
    def update_login_time(self):
        """更新登录时间"""
        self.login_time = datetime.now()
    
    def update_info(
        self,
        nickname: Optional[str] = None,
        avatar: Optional[str] = None,
        password: Optional[str] = None
    ):
        """更新用户信息"""
        if nickname is not None:
            self.nickname = nickname
        if avatar is not None:
            self.avatar = avatar
        if password is not None:
            self.set_password(password)
        self.update_time = datetime.now()
    
    def to_dict(self) -> dict:
        """将用户对象转换为字典（不包含敏感信息）"""
        return {
            "username": self.username,
            "active": self.active,
            "login_time": self.login_time.isoformat() if self.login_time else None,
            "add_time": self.add_time.isoformat() if self.add_time else None,
            "update_time": self.update_time.isoformat() if self.update_time else None,
            "nickname": self.nickname,
            "avatar": self.avatar
        }
    
    def to_dict_with_key(self) -> dict:
        """将用户对象转换为字典（包含激活密钥，用于注册后返回）"""
        return {
            "username": self.username,
            "active": self.active,
            "key": self.key,
            "login_time": self.login_time.isoformat() if self.login_time else None,
            "add_time": self.add_time.isoformat() if self.add_time else None,
            "update_time": self.update_time.isoformat() if self.update_time else None,
            "nickname": self.nickname,
            "avatar": self.avatar
        }
    
    def __repr__(self) -> str:
        return f"<User username={self.username} active={self.active}>"


class UserCreate(SQLModel):
    """创建用户的请求模型（不包含敏感字段）"""
    username: str
    password: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None


class UserPublic(SQLModel):
    """公开的响应模型（不包含敏感信息）"""
    username: str
    active: bool
    login_time: Optional[datetime] = None
    add_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    nickname: str
    avatar: str
