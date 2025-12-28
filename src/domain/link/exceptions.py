from uuid import UUID
from typing import Optional


class ShortLinkAlreadyExistsException(Exception):
    def __init__(self, short: Optional[str] = None) -> None:
        if short is not None:
            self.msg = f"Short link {short} already exists"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.short = short

class ShortLinkDoesNotExistException(Exception):
    def __init__(self,
        *,
        short: Optional[str] = None,
        link_id: Optional[UUID] = None
    ) -> None:
        if short is not None:
            self.msg = f"Short link {short} does not exist"
        if link_id is not None:
            self.msg = f"Short link with id {link_id} does not exist"   
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.short = short
        self.link_id = link_id

class UnprocessableShortLinkException(Exception):
    def __init__(self, short: Optional[str] = None) -> None:
        if short is not None:
            self.msg = f"Short link {short} is expired"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.short = short