from redis.asyncio import Redis

from domain.link.cache import AbstractLinkCache
from infrastructure.cache.entries.link import LinkCacheEntry
from infrastructure.cache.exceptions import CacheMiss

from domain.link.exceptions import ShortLinkRedirectLimitReached, ShortLinkExpired


LUA_GET_AND_INCREMENT = """
-- KEYS[1] = hash key
-- KEYS[2] = counter key

if redis.call("EXISTS", KEYS[1]) == 0 then
	return {err = "CACHE_MISS"}
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
		return {err = "SHORT_LINK_EXPIRED"}
	end
end

-- validating redirect limit
local times_used_current = redis.call("GET", KEYS[2])

if redirect_limit ~= nil and times_used >= redirect_limit then
	return {err = "SHORT_LINK_REDIRECT_LIMIT_REACHED"}
end

local times_used = redis.call("INCR", KEYS[2])

return {data, times_used}
"""


class RedisLinkCache(AbstractLinkCache):
	def __init__(self, client: Redis):
		self._client = client
		self._script_get_and_increment = self._client.register_script(LUA_GET_AND_INCREMENT)

	def _hash_key(self, short: str) -> str:
		return f"link:{short}"

	def _counter_key(self, short: str) -> str:
		return f"link:{short}:counter"

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
		vals = await self._client.hgetall(hkey)
		if not vals:
			raise CacheMiss()

		counter_key = self._counter_key(short)
		times_used_raw = await self._client.get(counter_key)
		times_used = int(times_used_raw) if times_used_raw else 0

		return self._parse_link_hash(
			vals=vals,
			times_used=times_used,
			short=short,
		)


	async def get_and_increment(self, short: str) -> LinkCacheEntry:
		hkey = self._hash_key(short)
		counter_key = self._counter_key(short)

		res = await self._script_get_and_increment(keys=[hkey, counter_key])

		if isinstance(res, dict) and "err" in res:
			match res["err"]:
				case "CACHE_MISS":
					raise CacheMiss()
				case "SHORT_LINK_REDIRECT_LIMIT_REACHED":
					raise ShortLinkRedirectLimitReached()
				case "SHORT_LINK_EXPIRED":
					raise ShortLinkExpired()

		raw_vals, times_used = res
		vals = dict(zip(raw_vals[::2], raw_vals[1::2]))

		return self._parse_link_hash(
			vals=vals,
			times_used=int(times_used),
			short=short,
		)

	
	async def save(self, entry: LinkCacheEntry, ttl: int | None = None) -> None:
		...