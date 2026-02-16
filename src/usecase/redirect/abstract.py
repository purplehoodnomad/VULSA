from abc import ABC, abstractmethod

from usecase.link.utils.dto import SimpleLinkDTO


class AbstractLinkRedirectUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        short: str,
    ) -> SimpleLinkDTO:
        raise NotImplementedError