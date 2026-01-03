from abc import ABC, abstractmethod

from usecase.link.utils.dto import LinkDTO, LinkFilterDto


class AbstractGetLinksListUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: LinkFilterDto) -> list[LinkDTO]:
        raise NotImplementedError