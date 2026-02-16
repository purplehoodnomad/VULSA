from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from container import Container

from infrastructure.broker.kafka.client import KafkaClient
from infrastructure.broker.topics import Topic


@inject
async def get_producer(client: KafkaClient = Depends(Provide[Container.kafka_client])) -> AIOKafkaProducer:
    return await client.get_producer()

@inject
async def get_consumer(
    topic: Topic,
    client: KafkaClient = Depends(Provide[Container.kafka_client])
) -> AIOKafkaConsumer:
    return await client.get_consumer(topic, auto_offset_reset="earliest")