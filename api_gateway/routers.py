from fastapi import APIRouter

from api_gateway.auth_service.views import auth_gateway
from api_gateway.user_service.views import user_gateway

gateway = APIRouter()


gateway.include_router(user_gateway, prefix="/user", tags=["user"])
gateway.include_router(auth_gateway, prefix="/auth", tags=["auth"])
