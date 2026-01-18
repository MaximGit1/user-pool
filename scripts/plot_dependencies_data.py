import dishka.plotter
from dishka import AsyncContainer

from user_pool.setup.components.di.main import container_factory
from user_pool.setup.config import Config, create_config


def make_plot_data_container(config: Config) -> AsyncContainer:
    return container_factory(config)


def generate_dependency_graph_d2(container: AsyncContainer) -> str:
    return dishka.plotter.render_mermaid(container)


async def main() -> None:
    config = create_config()

    async with make_plot_data_container(config)() as container:
        print(generate_dependency_graph_d2(container))
        await container.close()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
