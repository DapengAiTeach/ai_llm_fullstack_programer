from fastapi import APIRouter, HTTPException
from service.user_service import user_service
from core.exceptions import UserAlreadyExistsError
from schema.user import UserRegisterRequest, UserRegisterResponse

router = APIRouter()


@router.post("/register", response_model=UserRegisterResponse)
def register(user: UserRegisterRequest):
    """用户注册"""
    try:
        result = user_service.register(user.username, user.password)
        return UserRegisterResponse(
            message="注册成功",
            username=result.username,
            key=result.key,
            active=result.active
        )
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
