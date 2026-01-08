from abc import ABC, abstractmethod

from usecase.link.utils.dto import LinkDTO
from usecase.redirect.utils.dto import ClickMetadataDTO


class AbstractLinkRedirectUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        short: str,
        metadata: ClickMetadataDTO
    ) -> LinkDTO:
        raise NotImplementedError