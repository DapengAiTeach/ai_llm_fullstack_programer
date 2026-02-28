import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestLogin:
    """用户登录接口测试"""

    def test_login_success(self):
        """测试登录成功"""
        import uuid
        username = f"login_user_{uuid.uuid4().hex[:8]}"
        password = "correct_password"
        
        # 先注册
        client.post("/register", json={
            "username": username,
            "password": password
        })
        
        # 再登录
        response = client.post("/login", json={
            "username": username,
            "password": password
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "登录成功"
        assert data["username"] == username

    def test_login_wrong_password(self):
        """测试密码错误"""
        import uuid
        username = f"login_user_{uuid.uuid4().hex[:8]}"
        password = "correct_password"
        
        # 先注册
        client.post("/register", json={
            "username": username,
            "password": password
        })
        
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
            "username": "non_existent_user_12345",
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
