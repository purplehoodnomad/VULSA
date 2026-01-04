from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from usecase.redirect.abstract import AbstractLinkRedirectUseCase
from .dependencies import get_link_redirect_usecase


router = APIRouter()


@router.get("/{short}")
async def process_redirect(
    short: str,
    usecase: AbstractLinkRedirectUseCase = Depends(get_link_redirect_usecase)
 ) -> RedirectResponse:
    link = await usecase.execute(short)
    return RedirectResponse(url=link.long, status_code=status.HTTP_307_TEMPORARY_REDIRECT)