from fastapi import APIRouter, HTTPException
from core import db
from schema.login import UserLoginRequest, UserLoginResponse

router = APIRouter()


@router.post("/login", response_model=UserLoginResponse)
def login(user: UserLoginRequest):
    """用户登录"""
    if not db.verify_user(user.username, user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    return UserLoginResponse(message="登录成功", username=user.username)
