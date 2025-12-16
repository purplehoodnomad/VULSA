from contextlib import asynccontextmanager

from fastapi import FastAPI

from config.config import DEV
from api.v1 import routers as api_v1
from container import Container

container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код до yield выполняется один раз на старте (инициализация ресурсов: БД, кэш, клиенты).
    sessionmanager = container.session_manager()

    if DEV:
        sessionmanager.init("postgresql+asyncpg://user:password@localhost:5433/backend_course")
    else:
        sessionmanager.init("postgresql+asyncpg://user:password@db:5432/backend_course")

    # --- startup: создаём таблицы один раз (идемпотентно) ---
    async with sessionmanager.connect() as connection:
        if DEV:
            await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)

        container.wire(
        modules=[
            "infrastructure.databases.postgresql.session",
            "api.v1.link.dependencies"
        ]
    )  

    try:
        yield

        # Код после yield выполняется при остановке (корректно закрываем соединения, пулы и т.д.).
    finally:
        # --- shutdown: корректно закрываем пул соединений ---
        await sessionmanager.close()
    

app = FastAPI(lifespan=lifespan)

app.include_router(api_v1.router)