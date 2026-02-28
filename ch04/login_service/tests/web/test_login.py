import uuid
import pytest
from fastapi.testclient import TestClient
from main import app
from core import db

client = TestClient(app)


class TestLogin:
    """用户登录接口测试"""

    def setup_method(self):
        """每个测试方法前清理数据库"""
        db.clear_db()

    def test_login_success(self):
        """测试登录成功（已激活用户）"""
        username = f"login_user_{uuid.uuid4().hex[:8]}"
        password = "correct_password"
        
        # 先注册
        response1 = client.post("/register", json={
            "username": username,
            "password": password
        })
        assert response1.status_code == 200
        
        # 获取激活密钥并激活用户
        key = response1.json()["key"]
        db.activate_user(username, key)
        
        # 再登录
        response = client.post("/login", json={
            "username": username,
            "password": password
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "登录成功"
        assert data["username"] == username
        assert data["nickname"] == username  # 默认昵称为用户名

    def test_login_not_activated(self):
        """测试未激活用户无法登录"""
        username = f"login_user_{uuid.uuid4().hex[:8]}"
        password = "correct_password"
        
        # 先注册（未激活）
        client.post("/register", json={
            "username": username,
            "password": password
        })
        
        # 尝试登录（未激活）
        response = client.post("/login", json={
            "username": username,
            "password": password
        })
        
        assert response.status_code == 400
        assert "用户未激活" in response.json()["detail"]

    def test_login_wrong_password(self):
        """测试密码错误"""
        username = f"login_user_{uuid.uuid4().hex[:8]}"
        password = "correct_password"
        
        # 先注册并激活
        response1 = client.post("/register", json={
            "username": username,
            "password": password
        })
        key = response1.json()["key"]
        db.activate_user(username, key)
        
        # 用错误密码登录
        response = client.post("/login", json={
            "username": username,
            "password": "wrong_password"
        })
        
        assert response.status_code == 400
        assert response.json()["detail"] == "用户名或密码错误"

    def test_login_user_not_exist(self):
        """测试用户不存在"""
        response = client.post("/login", json={
            "username": "non_exist_user",
            "password": "any_password"
        })
        
        assert response.status_code == 400
        assert response.json()["detail"] == "用户名或密码错误"

    def test_login_missing_username(self):
        """测试缺少用户名参数"""
        response = client.post("/login", json={
            "password": "password123"
        })
        
        assert response.status_code == 422

    def test_login_missing_password(self):
        """测试缺少密码参数"""
        response = client.post("/login", json={
            "username": "test_user"
        })
        
        assert response.status_code == 422
