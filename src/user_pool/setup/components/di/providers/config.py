from dishka import Provider, Scope, from_context, provide

from user_pool.setup.config import (
    ASGIConfig,
    CacheConfig,
    Config,
    DBConfig,
    LoggingConfig, TokenConfig, AuthGRPCClientConfig,
)


class ConfigProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_postgres_config(self, config: Config) -> DBConfig:
        return config.db

    @provide(scope=Scope.APP)
    def get_asgi_config(self, config: Config) -> ASGIConfig:
        return config.asgi

    @provide(scope=Scope.APP)
    def get_logging_config(self, config: Config) -> LoggingConfig:
        return config.logging

    @provide(scope=Scope.APP)
    def get_cache_config(self, config: Config) -> CacheConfig:
        return config.cache

    @provide(scope=Scope.APP)
    def get_tokens_config(self, config: Config) -> TokenConfig:
        return config.tokens

    @provide(scope=Scope.APP)
    def get_grpc_client_config(self, config: Config) -> AuthGRPCClientConfig:
        return config.auth_grpc_client