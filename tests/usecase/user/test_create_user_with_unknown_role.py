import pytest

from domain.exceptions import DomainException
from infrastructure.inmemory.uow.user import InMemoryUserUnitOfWork
from usecase.user.utils.dto import UserCreateDTO
from usecase.user.create_user.implementation import PostgresCreateUserUseCase


@pytest.mark.asyncio
async def test_create_user_with_unknown_role():
    uow = InMemoryUserUnitOfWork()
    usecase = PostgresCreateUserUseCase(uow)

    dto = UserCreateDTO(
        email="test@mail.com",
        password="password",
        role="unknown"
    )

    with pytest.raises(DomainException):
        await usecase.execute(dto)