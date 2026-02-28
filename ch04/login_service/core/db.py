"""
内存数据库模块
提供用户数据的内存存储功能
"""

# 内存存储用户信息
_users_db = {}


def get_db():
    """获取数据库实例"""
    return _users_db


def user_exists(username: str) -> bool:
    """检查用户是否存在"""
    return username in _users_db


def create_user(username: str, password: str) -> bool:
    """
    创建新用户
    
    Args:
        username: 用户名
        password: 密码
    
    Returns:
        bool: 创建成功返回 True，用户已存在返回 False
    """
    if username in _users_db:
        return False
    _users_db[username] = password
    return True


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
    return _users_db[username] == password


def get_user(username: str) -> dict | None:
    """
    获取用户信息
    
    Args:
        username: 用户名
    
    Returns:
        dict: 用户信息字典，用户不存在返回 None
    """
    if username not in _users_db:
        return None
    return {
        "username": username,
        "password": _users_db[username]
    }


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
