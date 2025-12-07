from dataclasses import asdict

from .link.schemas import LinkSchema
from ...domain.link.schemas import LinkDTO

def link_dto_to_schema(dto: LinkDTO) -> LinkSchema:
    return LinkSchema(**asdict(dto))