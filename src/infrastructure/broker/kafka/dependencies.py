from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from infrastructure.broker.kafka.producer import KafkaProducer

from container import Container

from infrastructure.broker.kafka.client import KafkaClient


@inject
async def get_kafka_client(client: KafkaClient = Depends(Provide[Container.kafka_client])) -> KafkaClient:
    return client


async def get_producer(client: KafkaClient = Depends(get_kafka_client)) -> KafkaProducer:
    return await client.get_producer()