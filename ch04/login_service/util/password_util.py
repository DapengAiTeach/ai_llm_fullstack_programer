"""
密码工具模块
提供密码哈希和验证功能
"""
import hashlib
import secrets
import string


def hash_password(password: str) -> str:
    """
    对密码进行 SHA256 哈希处理
    
    Args:
        password: 原始密码
        
    Returns:
        str: 哈希后的密码
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    验证密码是否匹配
    
    Args:
        password: 原始密码
        hashed_password: 哈希后的密码
        
    Returns:
        bool: 匹配返回 True，否则返回 False
    """
    return hash_password(password) == hashed_password


def generate_random_password(length: int = 12) -> str:
    """
    生成随机密码
    
    Args:
        length: 密码长度，默认 12
        
    Returns:
        str: 随机密码
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_activation_key(length: int = 32) -> str:
    """
    生成随机的激活密钥
    
    Args:
        length: 密钥长度，默认 32
        
    Returns:
        str: 激活密钥
    """
    return secrets.token_urlsafe(length)
