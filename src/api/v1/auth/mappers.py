from .schemas import TokenSchema
from usecase.auth.utils.dto import TokenDTO

def dto_to_schema(dto: TokenDTO) -> TokenSchema:
    return TokenSchema(
        access_token=dto.access_token,
        refresh_token=dto.refresh_token
    )