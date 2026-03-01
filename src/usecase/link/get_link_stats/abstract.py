from abc import ABC, abstractmethod
from usecase.link.utils.dto import LinkStatsDTO
from usecase.common.actor import Actor


class AbstractGetLinkStatsUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        actor: Actor,
        short: str
    ) -> LinkStatsDTO:
        raise NotImplementedError()