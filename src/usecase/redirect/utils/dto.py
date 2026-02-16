from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class ClickMetadataDTO:
    short: str
    timestamp: datetime
    ip: str | None
    user_agent: str | None
    referer: str | None
    request_url: str | None