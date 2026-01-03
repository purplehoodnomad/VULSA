from abc import ABC, abstractmethod

from usecase.link.utils.dto import LinkDTO, LinkCreateDTO


class AbstractCreateLinkUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: LinkCreateDTO
    ) -> LinkDTO:
        raise NotImplementedError