from uuid import UUID

class ShortLinkDoesNotExist(Exception):
    def __init__(self, short: str | None = None) -> None:
        super().__init__(f"Link with short={short} does not exist")
        
        self.short_url: str | None = short

class LinkDoesNotExist(Exception):
    def __init__(self, url_id: UUID | None = None) -> None:
        super().__init__(f"Link with url_id={url_id} does not exist")
        
        self.url_id: UUID | None = url_id

class ShortLinkAlreadyExists(Exception):
    def __init__(self, short: str) -> None:
        super().__init__(f"Link with short={short} already exists")

        self.short_url: str = short