from starlette.responses import Response

from user_pool.application.common.data.dtos.net import CookieData, HeaderData


def set_cookie(response: Response, cookie: CookieData) -> None:
    response.set_cookie(
        key=cookie.key,
        value=cookie.value,
        max_age=cookie.max_age,
        samesite=cookie.same_site,
        secure=cookie.secure,
        httponly=cookie.httponly,
    )

def delete_cookie(response: Response, cookie_key: str) -> None:
    response.delete_cookie(cookie_key)

def attach_header(response: Response, header: HeaderData) -> None:
    response.headers[header.key] = header.value
