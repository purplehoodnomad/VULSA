from datetime import datetime

from redis.asyncio import Redis

from domain.link.cache import AbstractLinkCache
from infrastructure.cache.entries.link import LinkCacheEntry
from infrastructure.cache.exceptions import CacheMiss

from domain.link.exceptions import ShortLinkRedirectLimitReached, ShortLinkExpired


LUA_GET_AND_INCREMENT = """
-- KEYS[1] = hash key
-- KEYS[2] = counter key
-- KEYS[3] = delta key

if redis.call("EXISTS", KEYS[1]) == 0 then
	return "CACHE_MISS"
end

local data = redis.call("HGETALL", KEYS[1])

local redirect_limit = nil
local expires_at = nil

-- parsing limits
for i = 1, #data, 2 do
	if data[i] == "redirect_limit" then
		redirect_limit = tonumber(data[i + 1])
	elseif data[i] == "expires_at" then
		expires_at = tonumber(data[i + 1])
	end
end

-- validating expiration date
if expires_at ~= nil then
	local now = tonumber(redis.call("TIME")[1])
	if now >= expires_at then
		return "SHORT_LINK_EXPIRED"
	end
end

-- validating redirect limit
local times_used_current = tonumber(redis.call("GET", KEYS[2])) or 0

if redirect_limit ~= nil and times_used_current >= redirect_limit then
	return "SHORT_LINK_REDIRECT_LIMIT_REACHED"
end

local times_used = redis.call("INCR", KEYS[2]) -- click count
redis.call("INCR", KEYS[3]) -- delta

-- restore TTL if lost
local ttl = redis.call("TTL", KEYS[3])
if ttl < 0 then
    local hash_ttl = redis.call("TTL", KEYS[1])
    if hash_ttl > 0 then
        redis.call("EXPIRE", KEYS[3], hash_ttl)
    end
end

return {data, times_used}
"""

LUA_GATHER_DELTAS = """
local cursor = "0"
local result = {}

repeat
    local scan_result = redis.call(
        "SCAN",
        cursor,
        "MATCH",
        "link:*:delta",
        "COUNT",
        10000
    )

    cursor = scan_result[1]
    local keys = scan_result[2]

    for _, delta_key in ipairs(keys) do
        local delta = tonumber(redis.call("GET", delta_key))

        if delta ~= nil and delta > 0 then
            local short = string.match(delta_key, "^link:(.+):delta$")

            if short then
                table.insert(result, short)
                table.insert(result, delta)
                redis.call("SET", delta_key, 0, "KEEPTTL")
            end
        end
    end

until cursor == "0"

return result
"""

class RedisLinkCache(AbstractLinkCache):
	DEFAULT_TTL = 24 * 60 * 60 # 1 day

	def __init__(self, client: Redis):
		self._client = client
		self._script_get_and_increment = self._client.register_script(LUA_GET_AND_INCREMENT)
		self._script_gather_deltas = self._client.register_script(LUA_GATHER_DELTAS)

	def _hash_key(self, short: str) -> str:
		return f"link:{short}"

	def _counter_key(self, short: str) -> str:
		return f"link:{short}:counter"
	
	def _delta_key(self, short: str) -> str:
		return f"link:{short}:delta"

	def _parse_link_hash(
		self,
		vals: dict[str, str],
		*,
		times_used: int,
		short: str,
	) -> LinkCacheEntry:
		long: str = vals["long"]
		expires_at_raw = vals.get("expires_at")
		expires_at = int(expires_at_raw) if expires_at_raw else None

		redirect_limit_raw = vals.get("redirect_limit")
		redirect_limit = int(redirect_limit_raw) if redirect_limit_raw is not None else None

		return LinkCacheEntry(
			short=short,
			long=long,
			expires_at=expires_at,
			redirect_limit=redirect_limit,
			times_used=times_used,
		)
	

	async def get(self, short: str) -> LinkCacheEntry:
		"""Returns raw LinkCacheEntry"""
		hkey = self._hash_key(short)
		vals = await self._client.hgetall(hkey) # type: ignore
		if not vals:
			raise CacheMiss()

		counter_key = self._counter_key(short)
		times_used_raw = await self._client.get(counter_key)
		times_used = int(times_used_raw) if times_used_raw else 0

		print(self._client.hgetall)
		return self._parse_link_hash(
			vals=vals,
			times_used=times_used,
			short=short,
		)


	async def get_and_increment(self, short: str) -> LinkCacheEntry:
		hash_key = self._hash_key(short)
		counter_key = self._counter_key(short)
		delta_key = self._delta_key(short)

		res = await self._script_get_and_increment(keys=[hash_key, counter_key, delta_key]) # type: ignore

		if isinstance(res, str):
			match res:
				case "CACHE_MISS":
					raise CacheMiss()
				case "SHORT_LINK_REDIRECT_LIMIT_REACHED":
					raise ShortLinkRedirectLimitReached()
				case "SHORT_LINK_EXPIRED":
					raise ShortLinkExpired()
				case _:
					raise Exception(res)

		raw_vals, times_used = res
		vals = dict(zip(raw_vals[::2], raw_vals[1::2]))

		return self._parse_link_hash(
			vals=vals,
			times_used=int(times_used),
			short=short,
		)


	async def save(self, entry: LinkCacheEntry, custom_ttl: int | None = None) -> None:
		now = int(datetime.now().timestamp())

		hash_key = self._hash_key(entry.short)
		counter_key = self._counter_key(entry.short)
		delta_key = self._delta_key(entry.short)

		data: dict[str, str] = {"long": entry.long}

		if entry.expires_at is not None:
			data["expires_at"] = str(entry.expires_at)

		if entry.redirect_limit is not None:
			data["redirect_limit"] = str(entry.redirect_limit)

		pipe = self._client.pipeline()


		pipe.hset(hash_key, mapping=data)
		pipe.set(counter_key, entry.times_used)
		pipe.set(delta_key, 0)

		ttl = custom_ttl if custom_ttl is not None else self.DEFAULT_TTL
		if entry.expires_at is not None:
			delta = entry.expires_at - now
			ttl = min(ttl, delta) if delta > 0 else 1
		
		pipe.expire(hash_key, ttl)
		pipe.expire(counter_key, ttl)
		pipe.expire(delta_key, ttl)

		await pipe.execute()

	
	async def remove(self, short: str) -> None:
		hash_key = self._hash_key(short)
		counter_key = self._counter_key(short)
		delta_key = self._delta_key(short)

		await self._client.delete(hash_key, counter_key, delta_key)
	

	async def gather_click_deltas(self) -> dict[str, int]:
		raw = await self._script_gather_deltas()
		if not raw:
			return {}
		
		return {short: int(delta) for short, delta in zip(raw[::2], raw[1::2])}