from dataclasses import dataclass
from uuid import UUID, uuid4
import validators

from domain.exceptions import InvalidValue


@dataclass(frozen=True)
class ClickStampId:
    value: UUID
    
    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Visited Link Stamp id is required")

    @staticmethod
    def generate() -> "ClickStampId":
        return ClickStampId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
    

@dataclass(frozen=True)
class IP:
    value: str | None

    def __post_init__(self):
        if self.value is not None and not validators.ipv4(self.value):
            raise InvalidValue("Visited Link Stamp id is required")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class UserAgent:
    value: str | None

    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class URL:
    value: str | None

    def __str__(self) -> str:
        return str(self.value)
    

@dataclass(frozen=True)
class ClickMetadata:
    ip: IP
    user_agent: UserAgent
    referer: URL
    request_url: URL

    def __str__(self) -> str:
        return str(f"ip={self.ip}, user_agent={self.user_agent}, referer={self.referer}, request_url={self.request_url}")

