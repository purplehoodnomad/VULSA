from uuid import UUID

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from api.v1.dependencies import get_authentificated_user_id

from domain.link.exceptions import (
    ShortLinkDoesNotExistException,
    UnprocessableShortLinkException,
    ShortLinkAlreadyExistsException
)

from usecase.link.utils.dto import LinkDTO, LinkCreateDTO, LinkFilterDto
from usecase.link import AbstractCreateLinkUseCase, AbstractLinkRedirectUseCase, AbstractGetUserLinksUseCase
    
from .dependencies import (
    get_link_create_usecase,
    get_link_redirect_usecase,
    get_get_user_links_usecase
    # get_link_get_by_id_usecase,
    
)

from .schemas import LinkSchema, LinkCreateSchema, LinkListSchema, LinkListQueryParams
from .mappers import dto_to_schema


router = APIRouter(prefix="/links")


@router.post("", response_model=LinkSchema)
async def create_short_link(
    payload: LinkCreateSchema,
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractCreateLinkUseCase = Depends(get_link_create_usecase),
) -> JSONResponse:
    dto = LinkCreateDTO(
        user_id=user_id,
        long=str(payload.long),
        short = payload.short,
        expires_at=payload.expires_at,
        redirect_limit=payload.redirect_limit
    )
    try:
        link_dto = await usecase.execute(dto)
    except ShortLinkAlreadyExistsException as e:
        raise HTTPException(detail=e.msg, status_code=status.HTTP_409_CONFLICT)
    except ValueError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_422_UNPROCESSABLE_CONTENT)

    return JSONResponse(content=dto_to_schema(link_dto).model_dump(mode="json"), status_code=status.HTTP_201_CREATED)

@router.get("/{suffix}")
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


@router.get("", response_model=LinkListSchema)
async def get_links_list(
    params: LinkListQueryParams = Depends(),
    user_id: UUID = Depends(get_authentificated_user_id),
    usecase: AbstractGetUserLinksUseCase = Depends(get_get_user_links_usecase)
) -> JSONResponse:
    
    dto = LinkFilterDto(
        offset=params.offset,
        limit=params.limit,
        user=user_id,
        older_than=params.older_than,
        newer_than=params.newer_than,
        active_status=params.active_status,
        has_expiration_date=params.has_expiration_date,
        has_redirect_limit=params.has_redirect_limit
    )

    links = await usecase.execute(dto)

    links_schemas = [dto_to_schema(link) for link in links]

    return JSONResponse(content=LinkListSchema(data=links_schemas).model_dump(mode="json"), status_code=status.HTTP_200_OK)




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


