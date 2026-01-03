from abc import ABC, abstractmethod

from usecase.user.utils.dto import UserDeleteDTO


class AbstractDeleteUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: UserDeleteDTO
    ) -> None:
        raise NotImplementedError