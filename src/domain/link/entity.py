from typing import Optional
from datetime import datetime, timezone

from domain.link.events import LinkClickEvent
from domain.exceptions import InvalidValue
from domain.link.exceptions import ShortLinkInactive, ShortLinkExpired, ShortLinkRedirectLimitReached

from domain.value_objects.common import (
    LinkId,
    UserId
)
from domain.value_objects.link import (
    Long,
    Short,
    RedirectLimit
)
from domain.value_objects.click import ClickMetadata


class Link:
    """Link entity"""
    def __init__(
        self,
        *,
        link_id: LinkId,
        user_id: UserId,
        long: Long,
        short: Short,
        created_at: datetime,
        times_used: int,
        is_active: bool,
        redirect_limit: RedirectLimit = RedirectLimit(None),
        expires_at: Optional[datetime] = None,
    ):
        self._link_id = link_id
        self._user_id = user_id
        self._long = long
        self._short = short
        self._redirect_limit = redirect_limit
        self._expires_at = expires_at
        self._created_at = created_at
        self._times_used = times_used
        self._is_active = is_active

        self._events: list[LinkClickEvent] = []

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Link):
            return self.link_id == obj.link_id
        return False
    
    @property
    def link_id(self) -> LinkId:
        return self._link_id
    
    @property
    def user_id(self) -> UserId:
        return self._user_id
    
    @property
    def long(self) -> Long:
        return self._long
    
    @property
    def short(self) -> Short:
        return self._short
    
    @property
    def redirect_limit(self) -> RedirectLimit:
        return self._redirect_limit
    
    @property
    def expires_at(self) -> datetime | None:
        return self._expires_at
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def times_used(self) -> int:
        return self._times_used
    
    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def events(self) -> list:
        return self._events
    
    @staticmethod
    def create(*,
        user_id: UserId,
        long: Long,
        short: Optional[Short],
        redirect_limit: RedirectLimit = RedirectLimit(None),
        expires_at: Optional[datetime] = None,
    ) -> "Link":
        """Creates Link entity"""
        link_id = LinkId.generate()
        if short is None:
            short = Short.generate()

        return Link(
            link_id=link_id,
            user_id=user_id,
            long=long,
            short=short,
            redirect_limit=redirect_limit,
            expires_at=expires_at,
            created_at=datetime.now(timezone.utc),
            times_used=0,
            is_active=True
    )


    def pull_events(self) -> list[LinkClickEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
    

    def consume_redirect(self, metadata: ClickMetadata) -> None:
        if self.expires_at is not None and self.expires_at < datetime.now(timezone.utc):
            raise ShortLinkExpired()
        if self.redirect_limit.value is not None and self.redirect_limit.value <= self.times_used:
            raise ShortLinkRedirectLimitReached()
        if not self.is_active:
            raise ShortLinkInactive()
        
        self._times_used += 1
        self._events.append(
            LinkClickEvent(
                link_id=self.link_id,
                short=self.short,
                timestamp=datetime.now(timezone.utc),
                ip=metadata.ip,
                user_agent=metadata.user_agent,
                referer=metadata.referer,
                request_url=metadata.request_url
            )
        )

    
    def change_long(self, long: Long) -> None:
        self._long = long
    
    def change_short(self, short: Short) -> None:
        self._short = short
    
    def change_expiration_date(self, new_date: datetime) -> None:
        if new_date < datetime.now(timezone.utc):
            raise InvalidValue("Expiration date can't be set to past")
        self._expires_at = new_date
    
    def change_redirect_limit(self, redirect_limit: RedirectLimit) -> None:
        if redirect_limit.value is not None and redirect_limit.value < self._times_used:
            raise InvalidValue("Redirect limit can't be less than total redirect count")
        self._redirect_limit = redirect_limit
    
    def activate(self) -> None:
        self._is_active = True
    
    def deactivate(self) -> None:
        self._is_active = False