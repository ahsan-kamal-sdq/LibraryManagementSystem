from fastapi import Depends, Request, status

from src.dependencies import get_current_user, redis_conn
from src.endpoints.auth.auth_utils import get_jwt_exp
from src.endpoints.auth.router_init import router
from src.responses import custom_response
from src.schemas.token import TokenSchema


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    refresh_token: TokenSchema, request: Request, user: dict = Depends(get_current_user)
) -> dict:
    """
    Logs out the authenticated user by storing the token in the redis blacklist
    """
    token = request.headers.get("authorization").split()[1]
    redis_conn.setex(f"bl_{token}", get_jwt_exp(token), token)
    # For refresh token using the same expire time since expire time in refresh token is 5 days.
    redis_conn.setex(
        f"bl_{refresh_token.refresh_token}",
        get_jwt_exp(token),
        refresh_token.refresh_token,
    )
    return custom_response(
        status_code=status.HTTP_200_OK, details="Logout successful.", data=None
    )
