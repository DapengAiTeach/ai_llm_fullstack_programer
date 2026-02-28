"""
用户注册相关的数据验证模块
"""
from pydantic import BaseModel, Field, field_validator


class UserRegisterRequest(BaseModel):
    """用户注册请求模型"""
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


class UserRegisterResponse(BaseModel):
    """用户注册响应模型"""
    message: str = Field(..., description="响应消息")
    username: str = Field(..., description="用户名")
