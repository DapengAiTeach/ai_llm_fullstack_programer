from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from service.user_service import user_service
from core.exceptions import UserNotFoundError, InvalidActivationKeyError

router = APIRouter()


class ActivateRequest(BaseModel):
    """激活请求模型"""
    username: str = Field(..., description="用户名")
    key: str = Field(..., description="激活密钥")


class ActivateResponse(BaseModel):
    """激活响应模型"""
    message: str = Field(..., description="响应消息")
    username: str = Field(..., description="用户名")
    active: bool = Field(..., description="激活状态")


@router.post("/activate", response_model=ActivateResponse)
def activate(request: ActivateRequest):
    """激活用户账号"""
    try:
        result = user_service.activate(request.username, request.key)
        return ActivateResponse(
            message="激活成功",
            username=result.username,
            active=result.active
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidActivationKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
