from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from domain.link.exceptions import (
    ShortLinkDoesNotExistException,
    UnprocessableShortLinkException,
)

from usecase.link import AbstractLinkRedirectUseCase
from .dependencies import get_link_redirect_usecase


router = APIRouter()


@router.get("/{short}")
async def process_redirect(
    suffix: str,
    usecase: AbstractLinkRedirectUseCase = Depends(get_link_redirect_usecase)
 ) -> RedirectResponse:
    try:
        link = await usecase.execute(suffix)
    except ShortLinkDoesNotExistException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_404_NOT_FOUND)
    except UnprocessableShortLinkException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_410_GONE)
    except ValueError as e:
        raise HTTPException(detail="Short link does not exist", status_code=status.HTTP_404_NOT_FOUND)

    return RedirectResponse(url=link.long, status_code=status.HTTP_307_TEMPORARY_REDIRECT)