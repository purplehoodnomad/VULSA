import asyncio
import signal
from aiokafka import AIOKafkaConsumer

from container import Container
from settings import settings
from infrastructure.broker.topics import Topic
from workers.dependencies import get_resolve_clicks_usecase, WorkerResources


async def handle_message(container: Container, consumer: AIOKafkaConsumer):
    session_manager = container.session_manager()
    session_manager.init(settings.database.get_url())

    try:
        async with session_manager.session() as session:
            resources = WorkerResources(session=session, consumer=consumer)

            usecase = await get_resolve_clicks_usecase(resources)
            await usecase.execute()
    finally:
        await session_manager.close()



async def main():
    container = Container.get_wired_container()

    kafka = container.kafka_client()
    kafka.init(settings.kafka.bootstrap_servers)

    consumer = await kafka.get_consumer(
        Topic.LINK_CLICKED,
        group_id="resolve_clicks_group",
        auto_offset_reset="latest",
    )

    print("Kafka resolve_clicks worker started")

    try:
        await handle_message(container, consumer)

    finally:
        await kafka.close()


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