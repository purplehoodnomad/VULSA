from dataclasses import dataclass

from domain.value_objects.click import ClickMetadata, IP, UserAgent, URL


@dataclass(slots=True)
class ClickMetadataDTO:
    ip: str | None
    user_agent: str | None
    referer: str | None
    request_url: str | None

    def to_vo_container(self) -> ClickMetadata:
        return ClickMetadata(
            ip=IP(self.ip),
            user_agent=UserAgent(self.user_agent),
            referer=URL(self.referer),
            request_url=URL(self.request_url)
        )