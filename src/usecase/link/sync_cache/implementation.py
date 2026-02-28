from infrastructure.uow.link import AbstractLinkUnitOfWork
from domain.link.cache import AbstractLinkCache

from .abstract import AbstractSyncCacheUseCase

from domain.value_objects.link import Short


class SyncCacheUseCase(AbstractSyncCacheUseCase):
	def __init__(
		self,
		uow: AbstractLinkUnitOfWork,
		cache: AbstractLinkCache
	):
		self.uow = uow
		self.cache = cache

	async def execute(self) -> None:
		deltas = await self.cache.gather_click_deltas()

		if deltas:
			async with self.uow as uow:
				await uow.link_repo.increment_redirects_bulk(deltas)

		# for short, delta in deltas.items():
		# 	async with self.uow as uow:
		# 		link = await uow.link_repo.get_by_short(Short(short))
		# 		link.consume_redirect(redirect_delta=delta)
		# 		await uow.link_repo.update(link)