"""
核心业务异常模块
定义系统中使用的所有业务异常类
"""


class ServiceException(Exception):
    """服务层异常基类"""
    pass


class UserException(ServiceException):
    """用户相关异常基类"""
    pass


class UserAlreadyExistsError(UserException):
    """用户已存在异常"""
    pass


class UserNotFoundError(UserException):
    """用户不存在异常"""
    pass


class InvalidPasswordError(UserException):
    """密码错误异常"""
    pass


class UserNotActivatedError(UserException):
    """用户未激活异常"""
    pass


class InvalidActivationKeyError(UserException):
    """激活密钥错误异常"""
    pass
