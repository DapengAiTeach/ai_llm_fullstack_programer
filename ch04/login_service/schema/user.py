"""
用户相关的数据验证模块
包含请求和响应模型
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class UserRequest(BaseModel):
    """用户请求基础模型（用于注册和登录）"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """验证用户名"""
        v = v.strip()
        if not v:
            raise ValueError("用户名不能为空")
        if len(v) < 3:
            raise ValueError("用户名长度不能少于3个字符")
        if len(v) > 20:
            raise ValueError("用户名长度不能超过20个字符")
        return v
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """验证密码"""
        if not v:
            raise ValueError("密码不能为空")
        if len(v) < 6:
            raise ValueError("密码长度不能少于6个字符")
        if len(v) > 50:
            raise ValueError("密码长度不能超过50个字符")
        return v


class UserRegisterRequest(UserRequest):
    """用户注册请求模型
    
    继承自 UserRequest，包含相同的用户名和密码验证规则
    """
    pass


class UserLoginRequest(UserRequest):
    """用户登录请求模型
    
    继承自 UserRequest，包含相同的用户名和密码验证规则
    """
    pass


class UserRegisterResponse(BaseModel):
    """用户注册响应模型"""
    message: str = Field(..., description="响应消息")
    username: str = Field(..., description="用户名")
    key: str = Field(..., description="激活密钥")
    active: bool = Field(..., description="是否已激活")


class UserLoginResponse(BaseModel):
    """用户登录响应模型"""
    message: str = Field(..., description="响应消息")
    username: str = Field(..., description="用户名")
    nickname: str = Field(..., description="昵称")


class UserActivateRequest(BaseModel):
    """用户激活请求模型"""
    username: str = Field(..., description="用户名")
    key: str = Field(..., description="激活密钥")


class UserActivateResponse(BaseModel):
    """用户激活响应模型"""
    message: str = Field(..., description="响应消息")
    username: str = Field(..., description="用户名")
    active: bool = Field(..., description="激活状态")


class UserInfoResponse(BaseModel):
    """用户信息响应模型"""
    username: str = Field(..., description="用户名")
    active: bool = Field(..., description="是否激活")
    login_time: Optional[str] = Field(None, description="上次登录时间")
    add_time: Optional[str] = Field(None, description="添加时间")
    update_time: Optional[str] = Field(None, description="修改时间")
    nickname: str = Field(..., description="昵称")
    avatar: str = Field(..., description="头像地址")


class UserUpdateRequest(BaseModel):
    """用户信息更新请求模型"""
    nickname: Optional[str] = Field(None, description="新昵称")
    avatar: Optional[str] = Field(None, description="新头像地址")
    
    @field_validator("nickname")
    @classmethod
    def validate_nickname(cls, v: Optional[str]) -> Optional[str]:
        """验证昵称"""
        if v is None:
            return v
        v = v.strip()
        if v and len(v) > 50:
            raise ValueError("昵称长度不能超过50个字符")
        return v


class UserChangePasswordRequest(BaseModel):
    """用户修改密码请求模型"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., description="新密码")
    
    @field_validator("old_password")
    @classmethod
    def validate_old_password(cls, v: str) -> str:
        """验证旧密码"""
        if not v:
            raise ValueError("旧密码不能为空")
        return v
    
    @field_validator("new_password")
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        """验证新密码"""
        if not v:
            raise ValueError("新密码不能为空")
        if len(v) < 6:
            raise ValueError("新密码长度不能少于6个字符")
        if len(v) > 50:
            raise ValueError("新密码长度不能超过50个字符")
        return v
