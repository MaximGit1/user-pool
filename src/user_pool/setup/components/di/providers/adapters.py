from dishka import Provider, Scope

from user_pool.application.common.repositories.auth.identity_provider import (
    IdentityProvider,
)
from user_pool.application.common.repositories.auth.tokenManager import (
    TokenManager,
)
from user_pool.application.common.repositories.auth.tokenTransportManager import (
    HttpTokenTransportManager,
)
from user_pool.domain.ports.password_hasher import PasswordHasher
from user_pool.domain.ports.user_id_generator import UserIDGenerator
from user_pool.infrastructure.adapters.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from user_pool.infrastructure.adapters.http_cookie_header_token_transport import (
    HttpCookieHeaderTokenTransportManager,
)
from user_pool.infrastructure.adapters.jwt_identity_provider import (
    JWTIdentityProvider,
)
from user_pool.infrastructure.adapters.jwt_token_manager import JWTTokenManager
from user_pool.infrastructure.adapters.uuid7_user_id_generator import (
    UUID7UserIDGenerator,
)


def ports_provider() -> Provider:
    provider = Provider()

    provider.provide(
        BcryptPasswordHasher,
        scope=Scope.APP,
        provides=PasswordHasher,
    )

    provider.provide(
        UUID7UserIDGenerator,
        scope=Scope.APP,
        provides=UserIDGenerator,
    )

    return provider


def repositories_provider() -> Provider:
    provider = Provider()

    provider.provide(
        JWTTokenManager,
        scope=Scope.APP,
        provides=TokenManager,
    )

    provider.provide(
        HttpCookieHeaderTokenTransportManager,
        scope=Scope.REQUEST,
        provides=HttpTokenTransportManager,
    )

    provider.provide(
        JWTIdentityProvider,
        scope=Scope.REQUEST,
        provides=IdentityProvider,
    )

    return provider
