from fastapi import APIRouter
from fastapi.responses import Response
from fastapi.requests import Request

from api_gateway.utils import reverse_proxy_route

user_gateway = APIRouter()


@reverse_proxy_route(
    method=user_gateway.get,
    path="/users/{_uid}"
)
async def get_user(
    _request: Request,
    _response: Response,
    _uid: int
):
    pass
