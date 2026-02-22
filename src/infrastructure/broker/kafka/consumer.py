from aiokafka import AIOKafkaConsumer, TopicPartition

from infrastructure.broker.abstract.consumer import AbstractConsumer


class KafkaConsumer(AbstractConsumer):
    def __init__(self, *args, **kwargs):
        self._consumer = AIOKafkaConsumer(*args, **kwargs)
    
    async def start(self) -> None:
        await self._consumer.start()
    
    async def stop(self) -> None:
        await self._consumer.stop()
    
    async def getmany(self) -> dict[TopicPartition, list]:
        return await self._consumer.getmany()
    
    async def commit(self) -> None:
        await self._consumer.commit()