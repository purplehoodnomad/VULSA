from dataclasses import dataclass
from uuid import UUID
from enum import Enum

from fastapi import HTTPException, status


class ActorType(Enum):
    USER = "user"
    ANONYMOUS = "anonymous"
    UNAUTHORIZED = "unauthorized"


@dataclass(slots=True)
class Actor:
    id: UUID | str | None
    type: ActorType

    def is_anonymous(self) -> bool:
        return self.type == ActorType.ANONYMOUS
    
    def is_user(self) -> bool:
        return self.type == ActorType.USER
    
    def validate_user(self) -> None:
        if self.type != ActorType.USER:
            raise HTTPException(detail="Not authorized", status_code=status.HTTP_401_UNAUTHORIZED) 
    
    def validate_actor_authentication(self) -> None:
        if self.type == ActorType.UNAUTHORIZED:
            raise HTTPException(detail="Not authorized", status_code=status.HTTP_401_UNAUTHORIZED)