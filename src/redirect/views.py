from fastapi import status, APIRouter, Depends
from fastapi.responses import RedirectResponse

from usecase.redirect.abstract import AbstractLinkRedirectUseCase
from usecase.redirect.utils.dto import ClickMetadataDTO

from .dependencies import get_link_redirect_usecase, get_click_metadata


router = APIRouter()


@router.get("/{short}")
async def process_redirect(
    short: str,
    metadata: ClickMetadataDTO = Depends(get_click_metadata),
    usecase: AbstractLinkRedirectUseCase = Depends(get_link_redirect_usecase),
 ) -> RedirectResponse:
    link = await usecase.execute(short, metadata)
    return RedirectResponse(url=link.long, status_code=status.HTTP_307_TEMPORARY_REDIRECT)