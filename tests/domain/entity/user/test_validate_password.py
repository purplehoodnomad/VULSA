from domain.user.entity import User
from domain.value_objects.user import Email, HashedPassword
from domain.value_objects.role import RoleName


def test_user_validate_password():
    user = User.create(
        email=Email("test@mail.com"),
        hashed_password=HashedPassword(""),
        role=RoleName("user")
    )
    user.change_password("password")
    user.validate_password("password")
