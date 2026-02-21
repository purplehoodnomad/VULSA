import asyncio
import signal
from aiokafka import AIOKafkaConsumer

from container import Container
from settings import settings
from infrastructure.broker.topics import Topic
from infrastructure.clickhouse.client import ClickHouseClient
from workers.dependencies import get_resolve_clicks_usecase, WorkerResources


async def worker_loop(
    stop_event: asyncio.Event,
    container: Container,
    consumer: AIOKafkaConsumer,
    clickhouse: ClickHouseClient
):
    session_manager = container.session_manager()
    session_manager.init(settings.database.get_url())

    try:
        while not stop_event.is_set():
            async with session_manager.session() as session:
                resources = WorkerResources(session=session, consumer=consumer, clickhouse=clickhouse)

                usecase = await get_resolve_clicks_usecase(resources)
                await usecase.execute()
            await asyncio.sleep(2)
    finally:
        await session_manager.close()



async def main():
    container = Container.get_wired_container()

    kafka = container.kafka_client()
    kafka.init(settings.kafka.get_url())

    consumer = await kafka.get_consumer(
        Topic.LINK_CLICKED,
        group_id="resolve_clicks_group",
        auto_offset_reset="latest",
    )
    clickhouse = container.clickhouse_client()
    clickhouse.init(settings.clickhouse.get_url())

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)
    
    print("Resolve Clicks worker started")
    await worker_loop(stop_event, container, consumer, clickhouse)

    await kafka.close()
    clickhouse.close()
    print("Resolve Clicks worker stopped")


def run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    task = loop.create_task(main())

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, task.cancel)

    try:
        loop.run_until_complete(task)
    finally:
        loop.close()


if __name__ == "__main__":
    run()