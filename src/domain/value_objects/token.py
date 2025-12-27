from dataclasses import dataclass
from uuid import UUID, uuid4
from secrets import token_urlsafe


@dataclass(frozen=True)
class Token:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Token is required")

    def __str__(self) -> str:
        return str(self.value)
    
    @staticmethod
    def generate() -> "Token":
        return Token(token_urlsafe(56))



@dataclass(frozen=True)
class TokenId:
    value: UUID

    def __post_init__(self):
        if not self.value:
            raise ValueError("Token id is required")

    def __str__(self) -> str:
        return str(self.value)
    
    @staticmethod
    def generate() -> "TokenId":
        return TokenId(uuid4())