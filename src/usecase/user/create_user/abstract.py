from abc import ABC, abstractmethod

from usecase.user.utils.dto import UserDTO, UserCreateDTO


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: UserCreateDTO
    ) -> UserDTO:
        raise NotImplementedError