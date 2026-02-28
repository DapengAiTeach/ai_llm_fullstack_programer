from fastapi import APIRouter, HTTPException
from service.user_service import user_service
from core.exceptions import UserNotFoundError, InvalidActivationKeyError
from schema.user import UserActivateRequest, UserActivateResponse

router = APIRouter()


@router.post("/activate", response_model=UserActivateResponse)
def activate(request: UserActivateRequest):
    """激活用户账号"""
    try:
        result = user_service.activate(request.username, request.key)
        return UserActivateResponse(
            message="激活成功",
            username=result.username,
            active=result.active
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidActivationKeyError as e:
        raise HTTPException(status_code=400, detail=str(e))
