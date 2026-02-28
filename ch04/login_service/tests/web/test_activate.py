"""
用户激活接口测试
"""
import uuid
import pytest
from fastapi.testclient import TestClient
from main import app
from service.user_service import UserService

client = TestClient(app)


class TestActivate:
    """用户激活接口测试"""

    def setup_method(self):
        """每个测试方法前清理数据库"""
        UserService.clear_all_users()

    def test_activate_success(self):
        """测试激活成功"""
        username = f"user_{uuid.uuid4().hex[:8]}"
        
        # 先注册
        response = client.post("/register", json={
            "username": username,
            "password": "password123"
        })
        assert response.status_code == 200
        key = response.json()["key"]
        
        # 激活
        response = client.post("/activate", json={
            "username": username,
            "key": key
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "激活成功"
        assert data["username"] == username
        assert data["active"] is True

    def test_activate_wrong_key(self):
        """测试错误激活密钥"""
        username = f"user_{uuid.uuid4().hex[:8]}"
        
        # 先注册
        client.post("/register", json={
            "username": username,
            "password": "password123"
        })
        
        # 使用错误密钥激活
        response = client.post("/activate", json={
            "username": username,
            "key": "wrong_key"
        })
        
        assert response.status_code == 400
        assert "激活密钥错误" in response.json()["detail"]

    def test_activate_user_not_exist(self):
        """测试激活不存在的用户"""
        response = client.post("/activate", json={
            "username": "nonexistent_user",
            "key": "some_key"
        })
        
        assert response.status_code == 404
        assert "用户不存在" in response.json()["detail"]

    def test_activate_missing_username(self):
        """测试缺少用户名"""
        response = client.post("/activate", json={
            "key": "some_key"
        })
        
        assert response.status_code == 422

    def test_activate_missing_key(self):
        """测试缺少密钥"""
        response = client.post("/activate", json={
            "username": "testuser"
        })
        
        assert response.status_code == 422

    def test_activate_then_login(self):
        """测试激活后可以登录"""
        username = f"user_{uuid.uuid4().hex[:8]}"
        
        # 注册
        response = client.post("/register", json={
            "username": username,
            "password": "password123"
        })
        key = response.json()["key"]
        
        # 未激活时无法登录
        response = client.post("/login", json={
            "username": username,
            "password": "password123"
        })
        assert response.status_code == 400
        assert "用户未激活" in response.json()["detail"]
        
        # 激活
        client.post("/activate", json={
            "username": username,
            "key": key
        })
        
        # 激活后可以登录
        response = client.post("/login", json={
            "username": username,
            "password": "password123"
        })
        assert response.status_code == 200
        assert response.json()["message"] == "登录成功"
