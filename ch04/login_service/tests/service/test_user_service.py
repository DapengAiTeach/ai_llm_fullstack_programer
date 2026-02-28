"""
用户服务业务逻辑单元测试
"""
import pytest
from service.user_service import UserService, user_service
from core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidPasswordError,
    UserNotActivatedError,
    InvalidActivationKeyError
)


@pytest.fixture
def service():
    """创建服务实例并清理数据库"""
    UserService.clear_all_users()
    yield UserService()
    UserService.clear_all_users()


class TestUserServiceRegister:
    """测试用户注册功能"""

    def test_register_success(self, service):
        """测试注册成功"""
        user = service.register("testuser", "password123")
        
        assert user.username == "testuser"
        assert user.active is False  # 新用户默认未激活
        assert user.key is not None  # 自动生成激活密钥
        assert user.nickname == "testuser"  # 默认昵称为用户名

    def test_register_duplicate_user(self, service):
        """测试重复注册"""
        service.register("testuser", "password123")
        
        with pytest.raises(UserAlreadyExistsError) as exc_info:
            service.register("testuser", "another_password")
        
        assert "用户名已存在" in str(exc_info.value)


class TestUserServiceLogin:
    """测试用户登录功能"""

    def test_login_success(self, service):
        """测试已激活用户登录成功"""
        # 注册用户
        user = service.register("testuser", "password123")
        # 激活用户
        service.activate("testuser", user.key)
        # 登录
        logged_in_user = service.login("testuser", "password123")
        
        assert logged_in_user.username == "testuser"
        assert logged_in_user.login_time is not None  # 登录时间已更新

    def test_login_not_activated(self, service):
        """测试未激活用户无法登录"""
        service.register("testuser", "password123")
        
        with pytest.raises(UserNotActivatedError) as exc_info:
            service.login("testuser", "password123")
        
        assert "用户未激活" in str(exc_info.value)

    def test_login_wrong_password(self, service):
        """测试密码错误"""
        user = service.register("testuser", "password123")
        service.activate("testuser", user.key)
        
        with pytest.raises(InvalidPasswordError) as exc_info:
            service.login("testuser", "wrong_password")
        
        assert "用户名或密码错误" in str(exc_info.value)

    def test_login_user_not_exist(self, service):
        """测试用户不存在"""
        with pytest.raises(UserNotFoundError) as exc_info:
            service.login("nonexistent", "password123")
        
        assert "用户名或密码错误" in str(exc_info.value)


class TestUserServiceActivate:
    """测试用户激活功能"""

    def test_activate_success(self, service):
        """测试激活成功"""
        user = service.register("testuser", "password123")
        assert user.active is False
        
        activated_user = service.activate("testuser", user.key)
        
        assert activated_user.active is True

    def test_activate_wrong_key(self, service):
        """测试错误激活密钥"""
        service.register("testuser", "password123")
        
        with pytest.raises(InvalidActivationKeyError) as exc_info:
            service.activate("testuser", "wrong_key")
        
        assert "激活密钥错误" in str(exc_info.value)

    def test_activate_user_not_exist(self, service):
        """测试激活不存在的用户"""
        with pytest.raises(UserNotFoundError) as exc_info:
            service.activate("nonexistent", "some_key")
        
        assert "用户不存在" in str(exc_info.value)


class TestUserServiceGetUserInfo:
    """测试获取用户信息功能"""

    def test_get_user_info_success(self, service):
        """测试获取用户信息成功"""
        service.register("testuser", "password123")
        
        info = service.get_user_info("testuser")
        
        assert info is not None
        assert info["username"] == "testuser"
        assert info["active"] is False
        assert "password" not in info  # 不应包含密码
        assert "key" not in info  # 不应包含密钥

    def test_get_user_info_not_exist(self, service):
        """测试获取不存在的用户信息"""
        info = service.get_user_info("nonexistent")
        
        assert info is None


class TestUserServiceUpdateUserInfo:
    """测试更新用户信息功能"""

    def test_update_nickname(self, service):
        """测试更新昵称"""
        service.register("testuser", "password123")
        
        updated_user = service.update_user_info("testuser", nickname="新昵称")
        
        assert updated_user.nickname == "新昵称"

    def test_update_avatar(self, service):
        """测试更新头像"""
        service.register("testuser", "password123")
        
        updated_user = service.update_user_info("testuser", avatar="https://example.com/avatar.jpg")
        
        assert updated_user.avatar == "https://example.com/avatar.jpg"

    def test_update_user_not_exist(self, service):
        """测试更新不存在的用户"""
        with pytest.raises(UserNotFoundError) as exc_info:
            service.update_user_info("nonexistent", nickname="新昵称")
        
        assert "用户不存在" in str(exc_info.value)


class TestUserServiceChangePassword:
    """测试修改密码功能"""

    def test_change_password_success(self, service):
        """测试修改密码成功"""
        user = service.register("testuser", "old_password")
        service.activate("testuser", user.key)
        
        # 修改密码
        service.change_password("testuser", "old_password", "new_password")
        
        # 使用新密码登录
        logged_in_user = service.login("testuser", "new_password")
        assert logged_in_user.username == "testuser"

    def test_change_password_wrong_old_password(self, service):
        """测试原密码错误"""
        service.register("testuser", "password123")
        
        with pytest.raises(InvalidPasswordError) as exc_info:
            service.change_password("testuser", "wrong_old", "new_password")
        
        assert "原密码错误" in str(exc_info.value)

    def test_change_password_user_not_exist(self, service):
        """测试修改不存在用户的密码"""
        with pytest.raises(UserNotFoundError) as exc_info:
            service.change_password("nonexistent", "old", "new")
        
        assert "用户不存在" in str(exc_info.value)


class TestUserServiceDeleteUser:
    """测试删除用户功能"""

    def test_delete_user_success(self, service):
        """测试删除用户成功"""
        service.register("testuser", "password123")
        
        result = service.delete_user("testuser")
        
        assert result is True
        # 验证用户已被删除
        info = service.get_user_info("testuser")
        assert info is None

    def test_delete_user_not_exist(self, service):
        """测试删除不存在的用户"""
        result = service.delete_user("nonexistent")
        
        assert result is False
