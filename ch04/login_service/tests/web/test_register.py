import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRegister:
    """用户注册接口测试"""

    def test_register_success(self):
        """测试注册成功"""
        # 使用随机用户名避免冲突
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
        username = f"duplicate_user_{uuid.uuid4().hex[:8]}"
        
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
        import uuid
        response = client.post("/register", json={
            "username": f"test_{uuid.uuid4().hex[:8]}"
        })
        
        assert response.status_code == 422
