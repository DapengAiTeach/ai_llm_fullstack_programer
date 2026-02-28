"""
用户请求响应模型单元测试
"""
import pytest
from pydantic import ValidationError
from schema.user import (
    UserRequest,
    UserRegisterRequest,
    UserLoginRequest,
    UserRegisterResponse,
    UserLoginResponse,
    UserActivateRequest,
    UserActivateResponse,
    UserUpdateRequest,
    UserChangePasswordRequest
)


class TestUserRequest:
    """测试用户请求基础模型（UserRequest）"""

    def test_valid_request(self):
        """测试有效的请求"""
        request = UserRequest(username="testuser", password="password123")
        assert request.username == "testuser"
        assert request.password == "password123"

    def test_username_trim_whitespace(self):
        """测试用户名去除首尾空格"""
        request = UserRequest(username="  testuser  ", password="password123")
        assert request.username == "testuser"

    def test_empty_username(self):
        """测试用户名为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="", password="password123")
        assert "用户名不能为空" in str(exc_info.value)

    def test_whitespace_only_username(self):
        """测试用户名为空白字符"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="   ", password="password123")
        assert "用户名不能为空" in str(exc_info.value)

    def test_short_username(self):
        """测试用户名太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="ab", password="password123")
        assert "用户名长度不能少于3个字符" in str(exc_info.value)

    def test_long_username(self):
        """测试用户名太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="a" * 21, password="password123")
        assert "用户名长度不能超过20个字符" in str(exc_info.value)

    def test_empty_password(self):
        """测试密码为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="testuser", password="")
        assert "密码不能为空" in str(exc_info.value)

    def test_short_password(self):
        """测试密码太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="testuser", password="12345")
        assert "密码长度不能少于6个字符" in str(exc_info.value)

    def test_long_password(self):
        """测试密码太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserRequest(username="testuser", password="a" * 51)
        assert "密码长度不能超过50个字符" in str(exc_info.value)

    def test_username_boundary_min(self):
        """测试用户名边界值 - 最小长度(3个字符)"""
        request = UserRequest(username="abc", password="password123")
        assert request.username == "abc"

    def test_username_boundary_max(self):
        """测试用户名边界值 - 最大长度(20个字符)"""
        request = UserRequest(username="a" * 20, password="password123")
        assert request.username == "a" * 20

    def test_password_boundary_min(self):
        """测试密码边界值 - 最小长度(6个字符)"""
        request = UserRequest(username="testuser", password="123456")
        assert request.password == "123456"

    def test_password_boundary_max(self):
        """测试密码边界值 - 最大长度(50个字符)"""
        request = UserRequest(username="testuser", password="a" * 50)
        assert request.password == "a" * 50


class TestUserRegisterRequest:
    """测试用户注册请求模型（继承自 UserRequest）"""

    def test_register_request_inherits_validation(self):
        """测试注册请求继承验证规则"""
        # 有效的注册请求
        request = UserRegisterRequest(username="newuser", password="password123")
        assert request.username == "newuser"
        assert request.password == "password123"

    def test_register_request_validation_error(self):
        """测试注册请求验证错误"""
        with pytest.raises(ValidationError):
            UserRegisterRequest(username="ab", password="123")  # 太短


class TestUserLoginRequest:
    """测试用户登录请求模型（继承自 UserRequest）"""

    def test_login_request_inherits_validation(self):
        """测试登录请求继承验证规则"""
        # 有效的登录请求
        request = UserLoginRequest(username="existinguser", password="password123")
        assert request.username == "existinguser"
        assert request.password == "password123"

    def test_login_request_validation_error(self):
        """测试登录请求验证错误"""
        with pytest.raises(ValidationError):
            UserLoginRequest(username="", password="password123")  # 用户名为空


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


class TestUserLoginResponse:
    """测试用户登录响应模型"""

    def test_valid_login_response(self):
        """测试有效的登录响应"""
        response = UserLoginResponse(
            message="登录成功",
            username="testuser",
            nickname="测试用户"
        )
        assert response.message == "登录成功"
        assert response.username == "testuser"
        assert response.nickname == "测试用户"

    def test_login_response_with_default_nickname(self):
        """测试使用用户名作为默认昵称的登录响应"""
        response = UserLoginResponse(
            message="登录成功",
            username="testuser",
            nickname="testuser"
        )
        assert response.nickname == "testuser"


class TestUserActivateRequest:
    """测试用户激活请求模型"""

    def test_valid_activate_request(self):
        """测试有效的激活请求"""
        request = UserActivateRequest(username="testuser", key="activation_key_123")
        assert request.username == "testuser"
        assert request.key == "activation_key_123"


class TestUserActivateResponse:
    """测试用户激活响应模型"""

    def test_valid_activate_response(self):
        """测试有效的激活响应"""
        response = UserActivateResponse(
            message="激活成功",
            username="testuser",
            active=True
        )
        assert response.message == "激活成功"
        assert response.username == "testuser"
        assert response.active is True

    def test_activate_response_not_activated(self):
        """测试未激活状态的响应"""
        response = UserActivateResponse(
            message="激活失败",
            username="testuser",
            active=False
        )
        assert response.active is False


class TestUserUpdateRequest:
    """测试用户信息更新请求模型"""

    def test_valid_update_nickname(self):
        """测试有效的昵称更新"""
        request = UserUpdateRequest(nickname="新昵称")
        assert request.nickname == "新昵称"

    def test_valid_update_avatar(self):
        """测试有效的头像更新"""
        request = UserUpdateRequest(avatar="https://example.com/avatar.jpg")
        assert request.avatar == "https://example.com/avatar.jpg"

    def test_valid_update_both(self):
        """测试同时更新昵称和头像"""
        request = UserUpdateRequest(
            nickname="新昵称",
            avatar="https://example.com/avatar.jpg"
        )
        assert request.nickname == "新昵称"
        assert request.avatar == "https://example.com/avatar.jpg"

    def test_empty_update(self):
        """测试空更新（可选字段）"""
        request = UserUpdateRequest()
        assert request.nickname is None
        assert request.avatar is None

    def test_nickname_trim_whitespace(self):
        """测试昵称去除首尾空格"""
        request = UserUpdateRequest(nickname="  新昵称  ")
        assert request.nickname == "新昵称"

    def test_nickname_too_long(self):
        """测试昵称太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdateRequest(nickname="a" * 51)
        assert "昵称长度不能超过50个字符" in str(exc_info.value)


class TestUserChangePasswordRequest:
    """测试用户修改密码请求模型"""

    def test_valid_change_password(self):
        """测试有效的修改密码请求"""
        request = UserChangePasswordRequest(
            old_password="old_password123",
            new_password="new_password123"
        )
        assert request.old_password == "old_password123"
        assert request.new_password == "new_password123"

    def test_empty_old_password(self):
        """测试旧密码为空"""
        with pytest.raises(ValidationError) as exc_info:
            UserChangePasswordRequest(old_password="", new_password="newpass")
        assert "旧密码不能为空" in str(exc_info.value)

    def test_short_new_password(self):
        """测试新密码太短"""
        with pytest.raises(ValidationError) as exc_info:
            UserChangePasswordRequest(old_password="oldpass", new_password="12345")
        assert "新密码长度不能少于6个字符" in str(exc_info.value)

    def test_long_new_password(self):
        """测试新密码太长"""
        with pytest.raises(ValidationError) as exc_info:
            UserChangePasswordRequest(old_password="oldpass", new_password="a" * 51)
        assert "新密码长度不能超过50个字符" in str(exc_info.value)

    def test_new_password_boundary_min(self):
        """测试新密码边界值 - 最小长度"""
        request = UserChangePasswordRequest(old_password="oldpass", new_password="123456")
        assert request.new_password == "123456"

    def test_new_password_boundary_max(self):
        """测试新密码边界值 - 最大长度"""
        request = UserChangePasswordRequest(old_password="oldpass", new_password="a" * 50)
        assert request.new_password == "a" * 50
