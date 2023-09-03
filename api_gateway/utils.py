from functools import wraps

import aiohttp
import asyncio
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from typing import Optional, Any

from api_gateway.settings import settings

services = {
    "user": settings.USER_SERVICE,
}


async def request(
    session: aiohttp.ClientSession,
    method: str,
    url: str,
    **kwargs
):
    temp_dict: dict = {}
    if method == "GET":
        async with session.get(url) as response:
            return await response.json()
    elif method == "POST":
        for key_f_args in kwargs:
            for i_fields in kwargs[key_f_args].model_fields_set:
                temp_dict[i_fields] = getattr(kwargs[key_f_args], i_fields)

        async with session.post(url, json=temp_dict) as response:
            return await response.json()


async def task(
    method: str,
    url: str,
    **kwargs
):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            request(
                session=session,
                method=method,
                url=url,
                **kwargs
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
            service = services[_request.scope["path"].split("/")[1]]
            service_address = f"{service['host']}:{service['port']}"
            _on_service_endpoint = "/".join(_request.scope["path"].split("/")[2:])
            response_from_service = await task(
                method=_request.scope["method"].upper(),
                url=f"{service_address}/{_on_service_endpoint}",
                **kwargs
            )
            return JSONResponse(
                status_code=status_code,
                content=response_from_service
            )

    return wrapped
