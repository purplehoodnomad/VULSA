from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1 import routers as api_v1
from redirect import routers as redirect
from container import Container

from domain.exceptions import DomainException
from api.v1.exceptions import domain_exception_handler


container = Container()
container.wire(
    modules=[
        "infrastructure.sqlalchemy.session",
        "api.v1.link.dependencies",
        "api.v1.user.dependencies",
        "api.v1.auth.dependencies",
        "redirect.dependencies"
    ]
) 


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager = container.session_manager()

    sessionmanager.init("postgresql+asyncpg://user:password@localhost:5433/backend_course")
    # sessionmanager.init("postgresql+asyncpg://user:password@db:5432/backend_course")

    async with sessionmanager.connect() as connection:
        # await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection) 

    try:
        yield

    finally:
        await sessionmanager.close()
    

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(redirect.router)
app.include_router(api_v1.router)
