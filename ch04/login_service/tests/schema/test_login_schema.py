"""
测试登录参数校验模块
"""
import pytest
from pydantic import ValidationError
from schema.login import UserLoginRequest


class TestUserLoginRequest:
    """测试用户登录请求模型"""

    def test_valid_login_request(self):
        """测试有效的登录请求"""
        user = UserLoginRequest(username="testuser", password="password123")
        assert user.username == "testuser"
        assert user.password == "password123"

    def test_username_trim_whitespace(self):
        """测试用户名去除首尾空格"""
        user = UserLoginRequest(username="  testuser  ", password="password123")
        assert user.username == "testuser"

    def test_empty_username(self):
        """测试用户名为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="", password="password123")
        assert "用户名不能为空" in str(exc_info.value)

    def test_whitespace_only_username(self):
        """测试用户名为空白字符"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="   ", password="password123")
        assert "用户名不能为空" in str(exc_info.value)

    def test_short_username(self):
        """测试用户名太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="ab", password="password123")
        assert "用户名长度不能少于3个字符" in str(exc_info.value)

    def test_long_username(self):
        """测试用户名太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="a" * 21, password="password123")
        assert "用户名长度不能超过20个字符" in str(exc_info.value)

    def test_empty_password(self):
        """测试密码为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="testuser", password="")
        assert "密码不能为空" in str(exc_info.value)

    def test_short_password(self):
        """测试密码太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="testuser", password="12345")
        assert "密码长度不能少于6个字符" in str(exc_info.value)

    def test_long_password(self):
        """测试密码太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserLoginRequest(username="testuser", password="a" * 51)
        assert "密码长度不能超过50个字符" in str(exc_info.value)

    def test_username_boundary_min(self):
        """测试用户名边界值 - 最小长度"""
        user = UserLoginRequest(username="abc", password="password123")
        assert user.username == "abc"

    def test_username_boundary_max(self):
        """测试用户名边界值 - 最大长度"""
        user = UserLoginRequest(username="a" * 20, password="password123")
        assert user.username == "a" * 20

    def test_password_boundary_min(self):
        """测试密码边界值 - 最小长度"""
        user = UserLoginRequest(username="testuser", password="123456")
        assert user.password == "123456"

    def test_password_boundary_max(self):
        """测试密码边界值 - 最大长度"""
        user = UserLoginRequest(username="testuser", password="a" * 50)
        assert user.password == "a" * 50
