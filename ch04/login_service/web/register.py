from fastapi import APIRouter, HTTPException
from core import db
from schema.register import UserRegisterRequest, UserRegisterResponse

router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
def register(user: UserRegisterRequest):
    """用户注册"""
    if not db.create_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    return UserRegisterResponse(message="注册成功", username=user.username)
