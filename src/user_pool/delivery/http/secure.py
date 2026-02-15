from fastapi.security import HTTPBearer
from starlette.responses import Response

from user_pool.application.common.data.dtos.auth import AuthContext
from user_pool.application.common.data.dtos.net import HeaderData, CookieData
from user_pool.delivery.http.response_data_editor import attach_header, set_cookie
from user_pool.setup.config import TokenConfig

bearer_scheme = HTTPBearer(auto_error=False)
"""Draws handle protection in Swagger"""


class ContextResolver:
    def __init__(self, config: TokenConfig) -> None:
        self._refresh_key = config.refresh_cookie_key
        self._access_key = config.access_header_key
        self._refresh_max_age = config.refresh_max_age

    def resolve_context(self, response: Response, contex: AuthContext) -> None:
        if contex.new_access:
            attach_header(response, HeaderData(key=self._access_key, value=contex.new_access))

        if contex.new_refresh:
            set_cookie(response, CookieData(
                key=self._refresh_key,
                value=contex.new_refresh,
                max_age=self._refresh_max_age,
            ))
