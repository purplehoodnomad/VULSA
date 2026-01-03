from abc import ABC, abstractmethod
from uuid import UUID

from usecase.link.utils.dto import LinkDTO, LinkUpdateDTO


class AbstractEditShortLinkUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        *,
        user_id: UUID,
        short: str,
        dto: LinkUpdateDTO
    ) -> LinkDTO:
        """Changes short link to parameters given.
        
        Args:
            user_id: UUID of user trying to edit link
            short: Current short link
            dto: New link data
        """
        raise NotImplementedError