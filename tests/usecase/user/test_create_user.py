import pytest
from datetime import datetime

from infrastructure.inmemory.uow.user import InMemoryUserUnitOfWork
from usecase.user.utils.dto import UserCreateDTO
from usecase.user.create_user.implementation import PostgresCreateUserUseCase


@pytest.mark.asyncio
async def test_create_user_usecase():
    user_dto = UserCreateDTO(
        email="test@mail.com",
        password="password",
        role="user"
    )

    uow = InMemoryUserUnitOfWork()
    usecase = PostgresCreateUserUseCase(uow)
    user = await usecase.execute(user_dto)
    
    assert user.email == "test@mail.com"
    assert user.role == "user"
    assert user.user_id is not None
    assert user.created_at < datetime.now()