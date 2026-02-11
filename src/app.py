from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.v1 import routers as api_v1
from redirect import routers as redirect
from container import Container
from settings import settings

from domain.exceptions import DomainException
from api.v1.exceptions import domain_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container.get_wired_container()
    
    sessionmanager = container.session_manager()
    sessionmanager.init(settings.database.get_url())

    redis = container.redis_client()
    redis.init(settings.cache.get_url())
    
    try:
        yield

    finally:
        await sessionmanager.close()
        await redis.close()
    

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(redirect.router)
app.include_router(api_v1.router)