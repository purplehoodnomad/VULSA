from contextlib import asynccontextmanager

from fastapi import FastAPI
import asyncpg

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

    pool = await asyncpg.create_pool(
        dsn="postgresql://user:password@localhost:5433/vulsa_db",
        min_size=1,
        max_size=10
    )
    app.state.db_pool = pool

    sessionmanager.init("postgresql+asyncpg://user:password@localhost:5433/vulsa_db")
    # sessionmanager.init("postgresql+asyncpg://user:password@db:5432/vulsa_db")

    try:
        yield

    finally:
        await pool.close()
        await sessionmanager.close()
    

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(redirect.router)
app.include_router(api_v1.router)
