from uuid import UUID

class UserDoesNotExist(Exception):
    def __init__(self, user_id: UUID | None = None) -> None:
        super().__init__(f"User with id {user_id} does not exist")
        
        self.user_id: UUID | None = user_id

class UserAlreadyExists(Exception):
    pass