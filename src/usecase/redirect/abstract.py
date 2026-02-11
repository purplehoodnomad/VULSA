from abc import ABC, abstractmethod

from usecase.link.utils.dto import SimpleLinkDTO
from usecase.redirect.utils.dto import ClickMetadataDTO


class AbstractLinkRedirectUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        short: str,
        metadata: ClickMetadataDTO
    ) -> SimpleLinkDTO:
        raise NotImplementedError