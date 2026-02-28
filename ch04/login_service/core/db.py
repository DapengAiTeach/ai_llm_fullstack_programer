"""
内存数据库模块 - 使用 SQLModel
提供用户数据的内存存储功能
"""
from typing import Optional
from model.user import User, hash_password

# 内存存储用户信息
_users_db: dict[str, User] = {}


def get_db() -> dict[str, User]:
    """获取数据库实例"""
    return _users_db


def user_exists(username: str) -> bool:
    """检查用户是否存在"""
    return username in _users_db


def create_user(username: str, password: str) -> User | None:
    """
    创建新用户
    
    Args:
        username: 用户名
        password: 密码
    
    Returns:
        User: 创建成功返回 User 对象，用户已存在返回 None
    """
    if username in _users_db:
        return None
    user = User(username=username, password=hash_password(password))
    _users_db[username] = user
    return user


def verify_user(username: str, password: str) -> bool:
    """
    验证用户密码
    
    Args:
        username: 用户名
        password: 密码
    
    Returns:
        bool: 验证成功返回 True，否则返回 False
    """
    if username not in _users_db:
        return False
    return _users_db[username].verify_password(password)


def get_user(username: str) -> User | None:
    """
    获取用户信息
    
    Args:
        username: 用户名
    
    Returns:
        User: 用户对象，用户不存在返回 None
    """
    return _users_db.get(username)


def delete_user(username: str) -> bool:
    """
    删除用户
    
    Args:
        username: 用户名
    
    Returns:
        bool: 删除成功返回 True，用户不存在返回 False
    """
    if username not in _users_db:
        return False
    del _users_db[username]
    return True


def clear_db():
    """清空数据库（仅用于测试）"""
    _users_db.clear()


def update_login_time(username: str) -> bool:
    """
    更新用户登录时间
    
    Args:
        username: 用户名
        
    Returns:
        bool: 更新成功返回 True，用户不存在返回 False
    """
    if username not in _users_db:
        return False
    _users_db[username].update_login_time()
    return True


def activate_user(username: str, key: str) -> bool:
    """
    激活用户
    
    Args:
        username: 用户名
        key: 激活密钥
        
    Returns:
        bool: 激活成功返回 True，否则返回 False
    """
    if username not in _users_db:
        return False
    return _users_db[username].activate(key)
