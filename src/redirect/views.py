from fastapi import status, APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from usecase.redirect.abstract import AbstractLinkRedirectUseCase

from .dependencies import get_link_redirect_usecase, register_click
from infrastructure.broker.kafka.dependencies import get_producer
from infrastructure.broker.abstract.producer import AbstractProducer


router = APIRouter()


@router.get("/{short}")
async def process_redirect(
   short: str,
   request: Request,
   producer: AbstractProducer = Depends(get_producer),
   usecase: AbstractLinkRedirectUseCase = Depends(get_link_redirect_usecase),
) -> RedirectResponse:
   link = await usecase.execute(short)
   await register_click(request, producer) # registering after executing -> 410 wouldn't be registered etc.

   return RedirectResponse(url=link.long, status_code=status.HTTP_307_TEMPORARY_REDIRECT)