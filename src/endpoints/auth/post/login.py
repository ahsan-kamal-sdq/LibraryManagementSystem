from fastapi import Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.dependencies import get_db, get_token_exception
from src.endpoints.auth.auth_utils import authenticate_user  # isort skip
from src.endpoints.auth.auth_utils import create_access_token  # isort skip
from src.endpoints.auth.router_init import router


@router.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> dict[str, str | bool]:
    """
    Logs in a user using username and password and returns the access token and a boolean indicating whether the user is a librarian
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise get_token_exception()
    token = create_access_token(user.username, user.id)
    return {"token": token, "is_librarian": user.is_librarian}