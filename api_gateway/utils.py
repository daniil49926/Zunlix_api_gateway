from functools import wraps

import json
import aiohttp
import asyncio
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from starlette.datastructures import FormData
from typing import Optional, Any

from api_gateway.settings import settings

services = {
    "user": settings.USER_SERVICE,
    "auth": settings.AUTH_SERVICE,
}


async def request(
    session: aiohttp.ClientSession,
    _request: Request
):
    service = services[_request.scope["path"].split("/")[1]]
    _full_url = f"{service['host']}:{service['port']}/" + "/".join(_request.scope["path"].split("/")[2:])

    if _request.method == "GET":
        async with session.get(_full_url) as response:
            return await response.json()
    elif _request.method == "POST":
        _form = None
        _body = None
        try:
            if getattr(_request, "_form"):
                _form = await _request.form()
                _form = remake_form_data(_form)
        except AttributeError:
            pass
        try:
            if getattr(_request, "_body"):
                _body = await _request.body()
        except AttributeError:
            pass
        if _form:
            async with session.post(
                    _full_url,
                    data=_form,
                    cookies=_request.cookies,
            ) as response:
                return await response.json()
        elif _body:
            async with session.post(
                    _full_url,
                    json=json.loads(_body.decode("utf-8")),
                    cookies=_request.cookies,
            ) as response:
                return await response.json()


async def task(
    _request: Request
):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            request(
                session=session,
                _request=_request
            )
        )


def reverse_proxy_route(
    method,
    path: str,
    status_code: Optional[int] = status.HTTP_200_OK,
    response_model: Optional[Any] = None,
    responses: Optional[Any] = None,
):
    app_method = method(
        path=path,
        status_code=status_code,
        response_model=response_model,
        responses=responses,
    )

    def wrapped(endpoint_coroutine):
        @app_method
        @wraps(endpoint_coroutine)
        async def decorator(_request: Request, _response: Response, **kwargs):
            response_from_service = await task(
                _request
            )
            return JSONResponse(
                status_code=status_code,
                content=response_from_service
            )

    return wrapped


def remake_form_data(form: FormData) -> aiohttp.FormData:
    fd = aiohttp.FormData()
    for i_key in form:
        fd.add_field(name=i_key, value=form[i_key])
    return fd
