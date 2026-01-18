from dishka import Provider, Scope

from user_pool.domain.ports.password_hasher import PasswordHasher
from user_pool.domain.ports.user_id_generator import UserIDGenerator
from user_pool.infrastructure.adapters.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)
from user_pool.infrastructure.adapters.uuid7_user_id_generator import (
    UUID7UserIDGenerator,
)


def port_provider() -> Provider:
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
