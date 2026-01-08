from contextlib import asynccontextmanager

from fastapi import FastAPI
import asyncpg

from api.v1 import routers as api_v1
from redirect import routers as redirect
from container import Container
from settings import settings

from domain.exceptions import DomainException
from api.v1.exceptions import domain_exception_handler

from usecase.common.event_bus import EventBus
from domain.link.events import LinkClickEvent
from usecase.redirect.utils.handlers import LinkVisitedHandler


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
    
    s = settings.database
    pool = await asyncpg.create_pool(
        dsn=f"postgresql://{s.user}:{s.password.get_secret_value()}@{s.host}:{s.port}/{s.name}",
        min_size=1,
        max_size=10
    )
    app.state.db_pool = pool
    
    from factory import make_link_uow_factory
    link_uow_factory = make_link_uow_factory(sessionmanager, container)

    bus = EventBus()

    bus.subscribe(LinkClickEvent, LinkVisitedHandler(uow_factory=link_uow_factory))
    
    app.state.event_bus = bus

    sessionmanager.init(settings.database.get_database_url())
    try:
        yield

    finally:
        await pool.close()
        await sessionmanager.close()
    

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(DomainException, domain_exception_handler)

app.include_router(redirect.router)
app.include_router(api_v1.router)