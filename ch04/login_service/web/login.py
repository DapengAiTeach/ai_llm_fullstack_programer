from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# 获取内存数据库引用（从main导入）
from main import users_db

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(user: User):
    """用户登录"""
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    if users_db[user.username] != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    return {"message": "登录成功", "username": user.username}
