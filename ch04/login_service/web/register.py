from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core import db

router = APIRouter()


class User(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(user: User):
    """用户注册"""
    if not db.create_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    return {"message": "注册成功", "username": user.username}
