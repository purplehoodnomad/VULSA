from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from api.v1.dependencies import get_authentificated_user_id

from domain.value_objects.common import UserId
from domain.link.exceptions import LinkDoesNotExist, ShortLinkDoesNotExist #, ShortLinkAlreadyExists

from usecase.link.dto import LinkCreateDTO
from usecase.link import (
    CreateLinkUsecase,
    GetLinkByIdUseCase,
    LinkRedirectUseCase,
    GetLinkListUsecase
)
from .dependencies import (
    get_link_create_usecase,
    get_link_get_by_id_usecase,
    get_link_redirect_usecase,
    get_link_list_usecase
)

from .schemas import LinkSchema, LinkCreateSchema, LinkListSchema, LinkListQueryParams 


router = APIRouter(prefix="/links")


@router.post("", response_model=LinkSchema)
async def create_short_link(
    payload: LinkCreateSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: CreateLinkUsecase = Depends(get_link_create_usecase),
) -> JSONResponse:
    
    dto = LinkCreateDTO(
        user_id=user_id,
        long=str(payload.long),
        short = payload.short,
        expires_at=payload.expires_at,
        redirect_limit=payload.redirect_limit
    )
    link = await usecase.execute(dto)

    return JSONResponse(content=link.model_dump(mode="json"), status_code=status.HTTP_201_CREATED)



# @router.get("/details/{url_id}", response_model=LinkSchema)
# async def get_link_data(
#     link_id: UUID,
#     usecase: GetLinkByIdUseCase = Depends(get_link_get_by_id_usecase)
# ) -> JSONResponse:
#     try:
#         link = await usecase.execute(link_id)
#     except LinkDoesNotExist:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     return JSONResponse(content=link.model_dump(mode="json"), status_code=status.HTTP_200_OK)


# @router.get("/{suffix}")
# async def process_redirect(
#     suffix: str,
#     usecase: LinkRedirectUseCase = Depends(get_link_redirect_usecase)
#  ) -> RedirectResponse:
#     try:
#         link = await usecase.execute(suffix)
#     except LinkDoesNotExist:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#     return RedirectResponse(url=link.long, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


# @router.get("", response_model=LinkListSchema)
# async def get_links_list(
#     params: LinkListQueryParams = Depends(),
#     usecase: GetLinkListUsecase = Depends(get_link_list_usecase)
# ) -> JSONResponse:
    
#     links = await usecase.execute(
#         offset=params.offset,
#         limit=params.limit,
#         user=params.user,
#         older_than=params.older_than,
#         newer_than=params.newer_than,
#         active_status=params.active_status,
#         has_expiration_date=params.has_expiration_date,
#         has_redirect_limit=params.has_redirect_limit
#     )

#     return JSONResponse(content=links.model_dump(mode="json"), status_code=status.HTTP_200_OK)