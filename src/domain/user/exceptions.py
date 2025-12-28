from uuid import UUID
from typing import Optional


class UserDoesNotExistException(Exception):
    def __init__(self, user_id: UUID | None = None) -> None:
        if user_id is not None:
            self.msg = f"User with id {user_id} does not exist"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.user_id = user_id


class UserWithEmailAlreadyExistsException(Exception):
    def __init__(self, email: Optional[str] = None) -> None:
        if email is not None:
            self.msg = f"User with email {email} already exists"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.email = email


class EmailDoesNotExistException(Exception):
    def __init__(self, email: Optional[str] = None) -> None:
        if email is not None:
            self.msg = f"User with email {email} does not exist"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.email = email


class PasswordMismatchException(Exception):
    def __init__(self, user_id: Optional[UUID] = None) -> None:
        if user_id is not None:
            self.msg = f"Invalid password for user with id {user_id}"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.user_id = user_id


class LinkOwnershipViolation(Exception):
    def __init__(self, *, short: str, user_id: UUID) -> None:
        if user_id is not None:
            self.msg = f"User {user_id} does not own {short}"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.user_id = user_id
        self.short = short