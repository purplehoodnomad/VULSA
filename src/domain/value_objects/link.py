from dataclasses import dataclass
import secrets, string
import validators
from re import fullmatch
from secrets import token_urlsafe
from uuid import UUID, uuid4
from typing import Optional
from datetime import datetime, timezone
import random

from domain.value_objects.common import LinkId
from domain.exceptions import InvalidValue


@dataclass(frozen=True)
class Long:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Link URL is required")
        
        if not validators.url(self.value):
            raise InvalidValue(f"Invalid URL: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Short:
    value: str

    MIN_SHORT_LINK_LENGTH = 2
    MAX_SHORT_LINK_LENGTH = 32

    @classmethod
    def generate(cls, length: int = 9) -> "Short":
        """
        Generates short link suffix of max available size by default.
        """
        size = cls.MAX_SHORT_LINK_LENGTH if length > cls.MAX_SHORT_LINK_LENGTH or length < cls.MIN_SHORT_LINK_LENGTH or length <= 0 else length
        return Short(''.join(secrets.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(size)))

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Suffix for short link is required")
        
        if not fullmatch(r'^[A-Za-z0-9]+$', self.value):
            raise InvalidValue(f"Invalid short link: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class RedirectLimit:
    value: int | None

    def __post_init__(self):
        if self.value is not None and self.value <= 0:
            raise InvalidValue(f"Redirect limit must be positive integer: {self.value}")
    
    def __str__(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class AnonymousEditKey:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Edit key is required")

    def __str__(self) -> str:
        return str(self.value)
    
    @staticmethod
    def generate() -> "AnonymousEditKey":
        return AnonymousEditKey(token_urlsafe(56))

# === Click Event VO ===

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


@dataclass(frozen=True, slots=True)
class ClickStamp:
    id: ClickStampId
    link_id: LinkId
    short: Short
    timestamp: datetime
    ip: Optional[str]
    user_agent: Optional[str]
    referer: Optional[str]
    request_url: Optional[str]
    geo: Optional[str]
    platform: Optional[str]
    client: Optional[str]

    def __post_init__(self):
        if self.ip is not None and not validators.ipv4(self.ip):
            raise InvalidValue(f"Visited Link Stamp ip is not valid: {self.ip}")
        
    def __eq__(self, value: object) -> bool:
        return isinstance(value, ClickStamp) and value.id == self.id


    @staticmethod
    def create(
        link_id: LinkId,
        short: Short,
        timestamp: datetime,
        ip: Optional[str],
        user_agent: Optional[str],
        referer: Optional[str],
        request_url: Optional[str] 
    ) -> "ClickStamp":
        return ClickStamp(
            id=ClickStampId.generate(),
            link_id=link_id,
            short=short,
            timestamp=timestamp,
            ip=ip,
            user_agent=user_agent,
            referer=referer,
            request_url=request_url,
            geo=random.choice(("ru", "de", "kz", "us", "sex", "fr", "ar")),
            platform=random.choice(("android", "windows", "macos", "ios")),
            client=random.choice(("firefox", "chrome", "opera"))
        )