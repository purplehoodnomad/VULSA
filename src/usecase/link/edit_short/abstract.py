from abc import ABC, abstractmethod

from usecase.link.utils.dto import LinkDTO, LinkUpdateDTO


class AbstractEditShortLinkUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: LinkUpdateDTO) -> LinkDTO:
        """Changes short link to parameters given."""
        raise NotImplementedError