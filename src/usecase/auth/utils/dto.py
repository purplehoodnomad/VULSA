from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.token.entity import Token


@dataclass(slots=True)
class LoginUserDTO:
    email: str
    password: str


@dataclass(slots=True)
class TokenDTO:
    user_id: UUID
    access_token: str
    refresh_token: str
    access_token_expires_at: datetime
    refresh_token_expires_at: datetime
    created_at: datetime


    @staticmethod
    def from_entity(entity: Token):
        return TokenDTO(
            user_id=entity.user_id.value,
            access_token=entity.access_token.value,
            refresh_token=entity.refresh_token.value,
            access_token_expires_at=entity.access_token_expires_at,
            refresh_token_expires_at=entity.refresh_token_expires_at,
            created_at=entity.created_at
        )