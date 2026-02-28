"""
用户注册相关的数据验证模块

注意：此文件保留以兼容现有代码，新的代码应直接从 schema.user 导入
"""
from schema.user import (
    UserRequest,
    UserRegisterRequest,
    UserRegisterResponse
)

# 导出供外部使用
__all__ = ["UserRequest", "UserRegisterRequest", "UserRegisterResponse"]
