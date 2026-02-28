from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 获取内存数据库引用（从main导入）
from main import users_db

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(user: User):
    """用户注册"""
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    users_db[user.username] = user.password
    return {"message": "注册成功", "username": user.username}
