import uuid
import pytest
from fastapi.testclient import TestClient
from main import app
from core import db

client = TestClient(app)


class TestRegister:
    """用户注册接口测试"""

    def setup_method(self):
        """每个测试方法前清理数据库"""
        db.clear_db()

    def test_register_success(self):
        """测试注册成功"""
        username = f"test_user_{uuid.uuid4().hex[:8]}"
        
        response = client.post("/register", json={
            "username": username,
            "password": "test_password_123"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "注册成功"
        assert data["username"] == username

    def test_register_duplicate_username(self):
        """测试重复用户名注册失败"""
        username = f"dup_{uuid.uuid4().hex[:8]}"
        
        # 第一次注册
        response1 = client.post("/register", json={
            "username": username,
            "password": "password123"
        })
        assert response1.status_code == 200
        
        # 第二次注册（重复用户名）
        response2 = client.post("/register", json={
            "username": username,
            "password": "different_password"
        })
        
        assert response2.status_code == 400
        assert response2.json()["detail"] == "用户名已存在"

    def test_register_missing_username(self):
        """测试缺少用户名参数"""
        response = client.post("/register", json={
            "password": "password123"
        })
        
        assert response.status_code == 422

    def test_register_missing_password(self):
        """测试缺少密码参数"""
        response = client.post("/register", json={
            "username": f"test_{uuid.uuid4().hex[:8]}"
        })
        
        assert response.status_code == 422

    def test_register_empty_username(self):
        """测试用户名为空"""
        response = client.post("/register", json={
            "username": "",
            "password": "password123"
        })
        
        assert response.status_code == 422

    def test_register_short_username(self):
        """测试用户名太短"""
        response = client.post("/register", json={
            "username": "ab",
            "password": "password123"
        })
        
        assert response.status_code == 422

    def test_register_short_password(self):
        """测试密码太短"""
        response = client.post("/register", json={
            "username": f"user_{uuid.uuid4().hex[:8]}",
            "password": "12345"
        })
        
        assert response.status_code == 422

    def test_register_whitespace_username(self):
        """测试用户名为空白字符"""
        response = client.post("/register", json={
            "username": "   ",
            "password": "password123"
        })
        
        assert response.status_code == 422
