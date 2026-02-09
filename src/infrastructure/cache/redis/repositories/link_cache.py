from datetime import datetime

from redis.asyncio import Redis

from domain.link.cache import AbstractLinkCache
from infrastructure.cache.entries.link import LinkCacheEntry
from infrastructure.cache.exceptions import CacheMiss

LUA_CHECK_AND_INCR = """
local hash_key = KEYS[1]
local counter_key = KEYS[2]
local now = tonumber(ARGV[1])

if redis.call("EXISTS", hash_key) == 0 then
  return {"MISS"}
end

local vals = redis.call("HMGET", hash_key, "is_active", "expires_at", "redirect_limit", "long")
local is_active = vals[1]
local expires_at = vals[2]
local redirect_limit = vals[3]
local long = vals[4]

if not is_active or is_active ~= "1" then
  return {"INACTIVE"}
end

if expires_at and expires_at ~= "" then
  local exp = tonumber(expires_at)
  if exp and exp < now then
    return {"EXPIRED"}
  end
end

local new_count = redis.call("INCR", counter_key)
if redirect_limit and redirect_limit ~= "" then
  local rl = tonumber(redirect_limit)
  if rl and new_count > rl then
    redis.call("DECR", counter_key)
    return {"LIMIT"}
  end
end

return {"OK", tostring(new_count), long}
"""

ТУТ ПРОДОЛЖИТЬ
class RedisLinkCache(AbstractLinkCache):
    def __init__(self, client: Redis):
        self._client = client

    def _hash_key(self, short: str) -> str:
        return f"link:{short}"

    def _counter_key(self, short: str) -> str:
        return f"link:{short}:counter"

    async def get_and_increment(self, short: str) -> LinkCacheEntry:
        hkey = self._hash_key(short)
        exists = await self._client.exists(hkey)
        if not exists:
            raise CacheMiss()

        vals = await self._client.hgetall(hkey)
        # === Getting values from dict ===
        long = vals.get("long")
        expires_at_raw = vals.get("expires_at")
        expires_at = int(expires_at_raw) if expires_at_raw else None
        redirect_limit_raw = vals.get("redirect_limit")
        redirect_limit = int(redirect_limit_raw) if redirect_limit_raw != "" else None

        counter_key = self._counter_key(short)
        times_used_raw = await self._client.get(counter_key)
        times_used = int(times_used_raw) if times_used_raw else 0

        res = await self._client.eval(
            LUA_CHECK_AND_INCR,
            numkeys=2,
            keys=[hkey, counter_key],
            args=[str(int(datetime.now().timestamp()))]
        )

        return LinkCacheEntry(
            short=short,
            long=long,
            expires_at=expires_at,
            redirect_limit=redirect_limit,
            times_used=times_used
        )    
    
    async def save(self, entry: LinkCacheEntry, ttl: int | None = None) -> None:
        ...