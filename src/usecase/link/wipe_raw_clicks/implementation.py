import logging

from .abstract import AbstractWipeRawClicksUseCase
from infrastructure.uow.link import AbstractLinkUnitOfWork


logger = logging.getLogger(__name__)


class WipeRawClicksUseCase(AbstractWipeRawClicksUseCase):
    def __init__(
        self,
        uow: AbstractLinkUnitOfWork
    ):
        self.uow = uow

    async def execute(self) -> None:
        try:
            async with self.uow as uow:
                await uow.click_repo.truncate_raw()
        except Exception as e:
            logger.exception(e)
