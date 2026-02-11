from typing import Optional
from redis.asyncio import Redis, from_url


class RedisClient:
    def __init__(self):
        self._client: Optional[Redis] = None


    def init(self, url: str) -> None:
        if self._client is None:
            self._client = from_url(url, decode_responses=True)


    def _ensure(self) -> Redis:
        if self._client is None:
            raise RuntimeError("RedisClient is not initialized")
        return self._client


    async def close(self) -> None:
        if self._client is not None:
            await self._client.close()
            await self._client.connection_pool.disconnect()
            self._client = None


    @property
    def client(self) -> Redis:
        return self._ensure()