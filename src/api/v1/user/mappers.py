from .schemas import UserSchema
from usecase.user.utils.dto import UserDTO

def dto_to_schema(dto: UserDTO) -> UserSchema:
    return UserSchema(
        user_id=dto.user_id,
        email=dto.email,
        status=dto.status,
        created_at=dto.created_at
    )