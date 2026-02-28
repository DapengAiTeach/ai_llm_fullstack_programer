"""
用户业务逻辑服务模块
处理用户注册、登录、激活等核心业务逻辑
"""
from typing import Optional
from model.user import User
from core import db
from core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidPasswordError,
    UserNotActivatedError,
    InvalidActivationKeyError
)


class UserService:
    """用户服务类"""

    @staticmethod
    def register(username: str, password: str) -> User:
        """
        用户注册
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            User: 新创建的用户对象
            
        Raises:
            UserAlreadyExistsError: 用户已存在
        """
        if db.user_exists(username):
            raise UserAlreadyExistsError("用户名已存在")
        
        user = db.create_user(username, password)
        if user is None:
            raise UserAlreadyExistsError("用户名已存在")
        
        return user

    @staticmethod
    def login(username: str, password: str) -> User:
        """
        用户登录
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            User: 登录成功的用户对象
            
        Raises:
            UserNotFoundError: 用户不存在
            InvalidPasswordError: 密码错误
            UserNotActivatedError: 用户未激活
        """
        user = db.get_user(username)
        if user is None:
            raise UserNotFoundError("用户名或密码错误")
        
        if not user.verify_password(password):
            raise InvalidPasswordError("用户名或密码错误")
        
        if not user.active:
            raise UserNotActivatedError("用户未激活，请先激活账号")
        
        # 更新登录时间
        user.update_login_time()
        
        return user

    @staticmethod
    def activate(username: str, key: str) -> User:
        """
        激活用户
        
        Args:
            username: 用户名
            key: 激活密钥
            
        Returns:
            User: 激活后的用户对象
            
        Raises:
            UserNotFoundError: 用户不存在
            InvalidActivationKeyError: 激活密钥错误
        """
        user = db.get_user(username)
        if user is None:
            raise UserNotFoundError("用户不存在")
        
        if not user.activate(key):
            raise InvalidActivationKeyError("激活密钥错误")
        
        return user

    @staticmethod
    def get_user_info(username: str) -> Optional[dict]:
        """
        获取用户信息
        
        Args:
            username: 用户名
            
        Returns:
            dict: 用户信息字典，用户不存在返回 None
        """
        user = db.get_user(username)
        if user is None:
            return None
        return user.to_dict()

    @staticmethod
    def update_user_info(
        username: str,
        nickname: Optional[str] = None,
        avatar: Optional[str] = None
    ) -> User:
        """
        更新用户信息
        
        Args:
            username: 用户名
            nickname: 新昵称
            avatar: 新头像地址
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            UserNotFoundError: 用户不存在
        """
        user = db.get_user(username)
        if user is None:
            raise UserNotFoundError("用户不存在")
        
        user.update_info(nickname=nickname, avatar=avatar)
        return user

    @staticmethod
    def change_password(username: str, old_password: str, new_password: str) -> User:
        """
        修改密码
        
        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            UserNotFoundError: 用户不存在
            InvalidPasswordError: 旧密码错误
        """
        user = db.get_user(username)
        if user is None:
            raise UserNotFoundError("用户不存在")
        
        if not user.verify_password(old_password):
            raise InvalidPasswordError("原密码错误")
        
        user.update_info(password=new_password)
        return user

    @staticmethod
    def delete_user(username: str) -> bool:
        """
        删除用户
        
        Args:
            username: 用户名
            
        Returns:
            bool: 删除成功返回 True，用户不存在返回 False
        """
        return db.delete_user(username)


# 创建服务实例
user_service = UserService()
