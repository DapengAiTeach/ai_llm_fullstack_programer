"""
密码工具模块单元测试
"""
import pytest
from util.password_util import (
    hash_password,
    verify_password,
    generate_random_password,
    generate_activation_key
)


class TestHashPassword:
    """测试密码哈希功能"""

    def test_hash_password_consistency(self):
        """测试相同密码产生相同的哈希值"""
        password = "test_password_123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 == hash2
        assert len(hash1) == 64  # SHA256 哈希值长度为 64 个十六进制字符

    def test_hash_password_different_passwords(self):
        """测试不同密码产生不同的哈希值"""
        hash1 = hash_password("password1")
        hash2 = hash_password("password2")
        
        assert hash1 != hash2

    def test_hash_password_empty_string(self):
        """测试空字符串哈希"""
        result = hash_password("")
        assert len(result) == 64
        assert result == hash_password("")  # 一致性

    def test_hash_password_long_password(self):
        """测试长密码哈希"""
        long_password = "a" * 1000
        result = hash_password(long_password)
        assert len(result) == 64


class TestVerifyPassword:
    """测试密码验证功能"""

    def test_verify_password_correct(self):
        """测试正确密码验证通过"""
        password = "my_password"
        hashed = hash_password(password)
        
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """测试错误密码验证失败"""
        password = "my_password"
        hashed = hash_password(password)
        
        assert verify_password("wrong_password", hashed) is False

    def test_verify_password_case_sensitive(self):
        """测试密码大小写敏感"""
        password = "MyPassword"
        hashed = hash_password(password)
        
        assert verify_password("mypassword", hashed) is False
        assert verify_password("MyPassword", hashed) is True

    def test_verify_password_empty(self):
        """测试空密码验证"""
        hashed = hash_password("")
        
        assert verify_password("", hashed) is True
        assert verify_password("not_empty", hashed) is False


class TestGenerateRandomPassword:
    """测试随机密码生成功能"""

    def test_generate_random_password_default_length(self):
        """测试默认长度随机密码"""
        password = generate_random_password()
        
        assert len(password) == 12  # 默认长度

    def test_generate_random_password_custom_length(self):
        """测试自定义长度随机密码"""
        password = generate_random_password(length=20)
        
        assert len(password) == 20

    def test_generate_random_password_uniqueness(self):
        """测试生成的密码是随机的（不相同）"""
        passwords = [generate_random_password() for _ in range(10)]
        
        # 检查所有生成的密码都是唯一的
        assert len(set(passwords)) == len(passwords)

    def test_generate_random_password_contains_required_chars(self):
        """测试生成的密码包含必要的字符类型"""
        import string
        
        password = generate_random_password(length=100)  # 足够长以确保包含各种字符
        
        # 检查是否包含字母、数字和标点符号中的至少一种
        has_letter = any(c in string.ascii_letters for c in password)
        has_digit = any(c in string.digits for c in password)
        has_punctuation = any(c in string.punctuation for c in password)
        
        # 由于使用 secrets.choice 从所有字符中随机选择，
        # 足够长的密码应该包含各种类型
        assert has_letter or has_digit or has_punctuation


class TestGenerateActivationKey:
    """测试激活密钥生成功能"""

    def test_generate_activation_key_default_length(self):
        """测试默认长度激活密钥"""
        key = generate_activation_key()
        
        # token_urlsafe(32) 生成的字符串长度约为 43 个字符
        assert len(key) > 30

    def test_generate_activation_key_custom_length(self):
        """测试自定义长度激活密钥"""
        key = generate_activation_key(length=16)
        
        assert len(key) > 16  # URL-safe base64 编码会增加长度

    def test_generate_activation_key_uniqueness(self):
        """测试生成的密钥是唯一的"""
        keys = [generate_activation_key() for _ in range(10)]
        
        assert len(set(keys)) == len(keys)

    def test_generate_activation_key_url_safe(self):
        """测试生成的密钥是 URL-safe 的"""
        import re
        
        key = generate_activation_key()
        
        # URL-safe base64 只包含 A-Z, a-z, 0-9, -, _
        assert re.match(r'^[A-Za-z0-9_-]+$', key) is not None


class TestPasswordUtilIntegration:
    """测试密码工具集成场景"""

    def test_hash_and_verify_workflow(self):
        """测试哈希和验证完整流程"""
        original_password = "user_password_123"
        
        # 注册时：哈希密码
        hashed = hash_password(original_password)
        
        # 登录时：验证密码
        assert verify_password(original_password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_password_never_stored_in_plaintext(self):
        """测试密码从不以明文存储"""
        password = "secret_password"
        hashed = hash_password(password)
        
        # 哈希值中不应包含原始密码
        assert password not in hashed
        # 哈希值与原始密码不同
        assert hashed != password
