from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class LinkId:
    value: UUID

    @staticmethod
    def generate() -> "LinkId":
        return LinkId(uuid4())

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID

    @staticmethod
    def generate() -> "UserId":
        return UserId(uuid4())

    def __str__(self) -> str:
        return str(self.value)