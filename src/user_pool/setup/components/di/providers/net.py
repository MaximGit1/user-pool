from dishka import Provider, Scope, provide
from dishka.integrations.fastapi import FastapiProvider
from grpc.aio import Channel, insecure_channel

from user_pool.application.common.repositories.auth.sso_clients import (
    AuthSSOClient,
    UserSSOClient,
)
from user_pool.delivery.http.secure import ContextResolver
from user_pool.infrastructure.grpc.clients.auth import AuthGRPCClient
from user_pool.infrastructure.grpc.clients.users import UsersGRPCClient
from user_pool.setup.config import AuthGRPCClientConfig


def get_grpc_provider() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(AuthGRPCClient, provides=AuthSSOClient)
    provider.provide(UsersGRPCClient, provides=UserSSOClient)

    return provider


def get_context_resolver() -> Provider:
    provider = Provider(Scope.APP)

    provider.provide(ContextResolver)

    return provider


class GRPCChannelProvider(Provider):
    @provide(scope=Scope.APP)
    async def create_channel(self, config: AuthGRPCClientConfig) -> Channel:
        return insecure_channel(f"{config.host}:{config.port}")


def get_net_providers() -> list[Provider]:
    return [
        FastapiProvider(),
        GRPCChannelProvider(),
        get_grpc_provider(),
        get_context_resolver(),
    ]
