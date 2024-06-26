import logging

from fastapi import APIRouter, status, HTTPException
from fastapi import Request
from backend.entity.user import User
from fastapi import Security
from backend.utils.auth import get_current_user
from backend.gateway.user_gw import UserGw
from backend.entity.responses import UserInfoResponse, user_responses

router = APIRouter()


@router.get("/get_info", summary="get user info",
            response_model=UserInfoResponse, responses={**user_responses})
async def get_user_info(
        request: Request,
        user: User = Security(get_current_user)
) -> UserInfoResponse:
    user_gw = UserGw(request.app.state.db)
    try:
        user = await user_gw.get_user_by_username(user.username)
    except Exception as e:
        logging.error(f"error in getting user info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return UserInfoResponse(success=True, user=user)
