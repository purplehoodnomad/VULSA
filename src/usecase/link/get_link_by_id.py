# from abc import ABC, abstractmethod
# from uuid import UUID

# from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW
# from domain.value_objects.common import LinkId
# from usecase.common.mappers import link_entity_to_schema
# from api.v1.link.schemas import LinkSchema


# class GetLinkByIdUseCase(ABC):
#     @abstractmethod
#     async def execute(
#         self,
#         link_id: UUID
#     ) -> LinkSchema:
#         raise NotImplementedError
        

# class GetLinkByIdUseCaseImpl(GetLinkByIdUseCase):
#     def __init__(self, uow: PostgreSQLLinkUoW):
#         self.uow = uow
    
#     async def execute(self, link_id: UUID) -> LinkSchema:
#         async with self.uow as uow:
#             if uow.repository is not None:
#                 link = await uow.repository.get(LinkId(link_id))
#             return link_entity_to_schema(link)