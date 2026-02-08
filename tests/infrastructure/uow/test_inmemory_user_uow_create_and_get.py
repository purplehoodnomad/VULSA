import pytest

from domain.user.entity import User
from domain.value_objects.user import Email, HashedPassword
from domain.value_objects.role import RoleName
from infrastructure.inmemory.uow.user import InMemoryUserUnitOfWork


@pytest.mark.asyncio
async def test_inmemory_user_uow_create_and_get():
    user = User.create(
        email=Email("test@mail.com"),
        hashed_password=HashedPassword(""),
        role=RoleName("user")
    )
    user.change_password("password")

    uow = InMemoryUserUnitOfWork()
    async with uow:
        await uow.user_repo.create(user)
        fetched = await uow.user_repo.get(user.user_id)

    assert fetched.email.value == "test@mail.com"
