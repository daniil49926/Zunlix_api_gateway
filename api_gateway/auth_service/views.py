from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from api_gateway.utils import reverse_proxy_route

auth_gateway = APIRouter()


@reverse_proxy_route(
    method=auth_gateway.get,
    path="/token",
)
async def read_token(_request: Request, _response: Response, _token: str):
    pass


@reverse_proxy_route(
    method=auth_gateway.post,
    path="/token",
)
async def login(
    _request: Request,
    _response: Response,
    _form_data: OAuth2PasswordRequestForm = Depends(),
):
    pass
