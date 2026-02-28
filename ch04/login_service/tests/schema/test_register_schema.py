"""
测试注册参数校验模块
"""
import pytest
from pydantic import ValidationError
from schema.register import UserRegisterRequest, UserRegisterResponse


class TestUserRegisterRequest:
    """测试用户注册请求模型"""

    def test_valid_register_request(self):
        """测试有效的注册请求"""
        user = UserRegisterRequest(username="testuser", password="password123")
        assert user.username == "testuser"
        assert user.password == "password123"

    def test_username_trim_whitespace(self):
        """测试用户名去除首尾空格"""
        user = UserRegisterRequest(username="  testuser  ", password="password123")
        assert user.username == "testuser"

    def test_empty_username(self):
        """测试用户名为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="", password="password123")
        assert "用户名不能为空" in str(exc_info.value)

    def test_whitespace_only_username(self):
        """测试用户名为空白字符"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="   ", password="password123")
        assert "用户名不能为空" in str(exc_info.value)

    def test_short_username(self):
        """测试用户名太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="ab", password="password123")
        assert "用户名长度不能少于3个字符" in str(exc_info.value)

    def test_long_username(self):
        """测试用户名太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="a" * 21, password="password123")
        assert "用户名长度不能超过20个字符" in str(exc_info.value)

    def test_empty_password(self):
        """测试密码为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="testuser", password="")
        assert "密码不能为空" in str(exc_info.value)

    def test_short_password(self):
        """测试密码太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="testuser", password="12345")
        assert "密码长度不能少于6个字符" in str(exc_info.value)

    def test_long_password(self):
        """测试密码太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserRegisterRequest(username="testuser", password="a" * 51)
        assert "密码长度不能超过50个字符" in str(exc_info.value)

    def test_username_boundary_min(self):
        """测试用户名边界值 - 最小长度(3个字符)"""
        user = UserRegisterRequest(username="abc", password="password123")
        assert user.username == "abc"

    def test_username_boundary_max(self):
        """测试用户名边界值 - 最大长度(20个字符)"""
        user = UserRegisterRequest(username="a" * 20, password="password123")
        assert user.username == "a" * 20

    def test_password_boundary_min(self):
        """测试密码边界值 - 最小长度(6个字符)"""
        user = UserRegisterRequest(username="testuser", password="123456")
        assert user.password == "123456"

    def test_password_boundary_max(self):
        """测试密码边界值 - 最大长度(50个字符)"""
        user = UserRegisterRequest(username="testuser", password="a" * 50)
        assert user.password == "a" * 50

    def test_username_with_special_characters(self):
        """测试用户名包含特殊字符"""
        user = UserRegisterRequest(username="user_123-abc", password="password123")
        assert user.username == "user_123-abc"

    def test_password_with_special_characters(self):
        """测试密码包含特殊字符"""
        user = UserRegisterRequest(username="testuser", password="pass!@#$%^&*()")
        assert user.password == "pass!@#$%^&*()"


class TestUserRegisterResponse:
    """测试用户注册响应模型"""

    def test_valid_register_response(self):
        """测试有效的注册响应"""
        response = UserRegisterResponse(
            message="注册成功",
            username="testuser",
            key="test_key_123",
            active=False
        )
        assert response.message == "注册成功"
        assert response.username == "testuser"
        assert response.key == "test_key_123"
        assert response.active is False

    def test_register_response_with_different_message(self):
        """测试不同消息的注册响应"""
        response = UserRegisterResponse(
            message="Welcome!",
            username="alice",
            key="activation_key_abc",
            active=True
        )
        assert response.message == "Welcome!"
        assert response.username == "alice"
        assert response.key == "activation_key_abc"
        assert response.active is True
