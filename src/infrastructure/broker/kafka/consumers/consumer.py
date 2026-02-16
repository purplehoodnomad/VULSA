# from kafka import KafkaConsumer

# from infrastructure.broker.kafka.serializers import deserialize
# from usecase.link.resolve_clicks.implementation import ResolveClicksUseCase


# class LinkClickConsumer:
#     def __init__(self, client: KafkaConsumer, usecase: ResolveClicksUseCase):
#         self._client = client
#         self._usecase = usecase

#     async def start(self):
#         async for msg in self._client:
#             payload = deserialize(msg.value)
#             await self._usecase.execute(payload)
