from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core import db

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(user: User):
    """用户登录"""
    if not db.verify_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    return {"message": "登录成功", "username": user.username}
