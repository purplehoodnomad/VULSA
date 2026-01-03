from abc import ABC, abstractmethod

from usecase.auth.utils.dto import TokenDTO


class AbstractRefreshAccessTokenUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        access_token: str
    ) -> TokenDTO:
        raise NotImplementedError