from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import Response

from api_gateway.response_serializers import Message404
from api_gateway.user_service.serializers import UserIn, UserOut
from api_gateway.utils import reverse_proxy_route

user_gateway = APIRouter()


@reverse_proxy_route(
    method=user_gateway.get,
    path="/users/{_uid}",
    response_model=UserOut,
    responses={404: {"model": Message404}},
)
async def get_user(_request: Request, _response: Response, _uid: int):
    pass


@reverse_proxy_route(method=user_gateway.post, path="/users", response_model=UserOut)
async def create_user(_request: Request, _response: Response, _user: UserIn):
    pass


@reverse_proxy_route(method=user_gateway.get, path="/me", response_model=UserOut)
async def get_me(_request: Request, _response: Response, _token: str):
    pass
