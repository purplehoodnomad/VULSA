from uuid import UUID

class SuffixDoesNotExist(Exception):
    def __init__(self, suffix: str | None = None) -> None:
        super().__init__(f"Link with short_url={suffix} does not exist")
        
        self.short_url: str | None = suffix

class LinkDoesNotExist(Exception):
    def __init__(self, link_id: UUID | None = None) -> None:
        super().__init__(f"Link with link_id={link_id} does not exist")
        
        self.link_id: UUID | None = link_id