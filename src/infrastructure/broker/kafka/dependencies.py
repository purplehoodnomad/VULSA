from fastapi import Depends
from dependency_injector.wiring import inject, Provide

from infrastructure.broker.kafka.producer import KafkaProducer

from container import Container

from infrastructure.broker.kafka.client import KafkaClient


@inject
async def get_kafka_client(client: KafkaClient = Depends(Provide[Container.kafka_client])) -> KafkaClient:
    return client

@inject
async def get_kafka_producer(producer: KafkaProducer = Depends(Provide[Container.kafka_producer])) -> KafkaProducer:
    return producer