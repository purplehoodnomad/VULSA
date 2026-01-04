from dataclasses import dataclass
from uuid import UUID, uuid4

from domain.exceptions import InvalidValue


@dataclass(frozen=True, slots=True)
class LinkId:
    value: UUID

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Link id is required")

    @staticmethod
    def generate() -> "LinkId":
        return LinkId(uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("User id is required")

    @staticmethod
    def generate() -> "UserId":
        return UserId(uuid4())

    def __str__(self) -> str:
        return str(self.value)