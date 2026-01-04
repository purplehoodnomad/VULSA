from dataclasses import dataclass
from uuid import UUID, uuid4
from secrets import token_urlsafe

from domain.exceptions import InvalidValue


@dataclass(frozen=True)
class TokenVO:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Token is required")

    def __str__(self) -> str:
        return str(self.value)
    
    @staticmethod
    def generate() -> "TokenVO":
        return TokenVO(token_urlsafe(56))


@dataclass(frozen=True)
class TokenId:
    value: UUID

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Token id is required")

    def __str__(self) -> str:
        return str(self.value)
    
    @staticmethod
    def generate() -> "TokenId":
        return TokenId(uuid4())