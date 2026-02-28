from fastapi import APIRouter, HTTPException
from service.user_service import user_service
from core.exceptions import (
    UserNotFoundError,
    InvalidPasswordError,
    UserNotActivatedError
)
from schema.login import UserLoginRequest, UserLoginResponse

router = APIRouter()


@router.post("/login", response_model=UserLoginResponse)
def login(user: UserLoginRequest):
    """用户登录"""
    try:
        result = user_service.login(user.username, user.password)
        return UserLoginResponse(
            message="登录成功",
            username=result.username,
            nickname=result.nickname
        )
    except (UserNotFoundError, InvalidPasswordError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except UserNotActivatedError as e:
        raise HTTPException(status_code=400, detail=str(e))
