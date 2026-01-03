from abc import ABC, abstractmethod

from usecase.auth.utils.dto import LoginUserDTO, TokenDTO


class AbstractLoginUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        dto: LoginUserDTO
    ) -> TokenDTO:
        raise NotImplementedError