from datetime import datetime

from domain.value_objects.common import LinkId
from domain.value_objects.link import Short
from domain.value_objects.click import ClickStampId, IP, UserAgent, URL


class ClickStamp:
    """Visited Link Metadata entity"""
    
    def __init__(
        self,
        *,
        id: ClickStampId,
        link_id: LinkId,
        short: Short,
        timestamp: datetime,
        ip: IP,
        user_agent: UserAgent,
        referer: URL,
        request_url: URL
    ):
        self._id = id
        self._link_id = link_id
        self._short = short
        self._timestamp = timestamp
        self._ip = ip
        self._user_agent = user_agent
        self._referer = referer
        self._request_url = request_url


    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, ClickStamp):
            return self.id == obj.id
        return False
    
    @property
    def id(self) -> ClickStampId:
        return self._id
    
    @property
    def link_id(self) -> LinkId:
        return self._link_id
    
    @property
    def short(self) -> Short:
        return self._short
    
    @property
    def timestamp(self) -> datetime:
        return self._timestamp
    
    @property
    def ip(self) -> IP:
        return self._ip

    @property
    def user_agent(self) -> UserAgent:
        return self._user_agent

    @property
    def referer(self) -> URL:
        return self._referer

    @property
    def request_url(self) -> URL:
        return self._request_url
    

    @staticmethod
    def create(*,
        link_id: LinkId,
        short: Short,
        timestamp: datetime,
        ip: IP,
        user_agent: UserAgent,
        referer: URL,
        request_url: URL
    ) -> "ClickStamp":
        return ClickStamp(
            id=ClickStampId.generate(),
            link_id=link_id,
            short=short,
            timestamp=timestamp,
            ip=ip,
            user_agent=user_agent,
            referer=referer,
            request_url=request_url
        )