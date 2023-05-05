from fastapi import APIRouter

from src.endpoints import auth, user
from src.endpoints.language import router_init as language_router

router = APIRouter()
router.include_router(auth.router)
router.include_router(language_router.router)
router.include_router(user.router)
