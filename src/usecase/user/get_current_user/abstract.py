from abc import ABC, abstractmethod

from domain.value_objects.token import TokenVO
from usecase.user.utils.dto import UserDTO


class AbstractGetCurrentUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        access_token: TokenVO
    ) -> UserDTO:
        raise NotImplementedError