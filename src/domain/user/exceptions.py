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
