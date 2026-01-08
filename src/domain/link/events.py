from dataclasses import dataclass
from datetime import datetime

from domain.value_objects.common import LinkId
from domain.value_objects.link import Short
from domain.value_objects.click import IP, UserAgent, URL


@dataclass(frozen=True, slots=True)
class LinkClickEvent:
    link_id: LinkId
    short: Short
    timestamp: datetime
    ip: IP
    user_agent: UserAgent
    referer: URL
    request_url: URL