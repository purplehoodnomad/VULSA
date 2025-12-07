# from uuid import UUID, uuid4
# import secrets, string
# from datetime import datetime, timezone
# from typing import List

# from ....domain.link.repository import AbstractLinkRepository
# from ....domain.link.schemas import LinkDTO, LinkCreateDTO, LinkUpdateDTO
# from ....domain.link.exceptions import LinkDoesNotExist, SuffixDoesNotExist


# class InMemoryLinkRepository(AbstractLinkRepository):
#     def __init__(self) -> None:
#         self._db: dict[UUID, Link] = {}
#         self._suffixes_db: dict[str, Link] = {}


#     def _generate_suffix(self, dto: LinkCreateDTO | LinkUpdateDTO) -> str:
#         # закидываю сюда объект на случай если логика генерации станет зависеть от оригинальной ссылки
#         while True:
#             suffix = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))
#             if suffix not in self._suffixes_db:
#                 return suffix


#     def get(self, entity_id: UUID) -> Link:
#         try:
#             return self._db[entity_id]
#         except KeyError:
#             raise LinkDoesNotExist(entity_id)


#     def get_by_suffix(self, suffix: str) -> Link:
#         try:
#             link = self._suffixes_db[suffix]
#             return link
#         except KeyError:
#             raise SuffixDoesNotExist(suffix)


#     def list(self, *, limit: int = 100, offset: int = 0) -> List[Link]:
#         if len(self._db) == 0:
#             return []
#         if offset >= len(self._db):
#             raise LinkDoesNotExist()
        
#         db_list = list(self._db.values())
#         return db_list[offset:offset+limit]


#     def create(self, dto: LinkCreateDTO) -> Link:
#         url_id = uuid4() # правильно ли это? Необходимо ли генерацию uuid сделать абстрактной?
#         suffix = self._generate_suffix(dto)

#         link = Link(
#             owner_id=dto.owner_id,
#             url_id=url_id,
#             base_url=dto.base_url,
#             suffix=suffix,
#             expires_at=dto.expires_at,
#             redirect_limit=dto.redirect_limit,
#             times_used=0,
#             is_active=False,
#         )

#         self._db[link.url_id] = link
#         self._suffixes_db[link.suffix] = link
#         return link


#     def update(self, entity_id: UUID, dto: LinkUpdateDTO, wipe=False) -> Link:
#         try:
#             existing = self._db[entity_id]

#             fields = list(dto.__annotations__.keys())
#             for field in fields:
#                 if wipe:  # PUT
#                     new_value = getattr(dto, field)
                    
#                     match field:
#                         case "is_active":
#                             new_value = False if new_value is None else new_value
                    
#                     setattr(existing, field, new_value)
                
#                 else:  # PATCH
#                     new_value = getattr(dto, field)
#                     if new_value is not None:
#                         setattr(existing, field, new_value)

#             return existing

#         except KeyError:
#             raise LinkDoesNotExist(entity_id)


#     def delete(self, entity_id: UUID) -> None:
#         try:
#             link_dto = self.get(entity_id)
#             del self._suffixes_db[link_dto.suffix]
#             del self._db[link_dto.url_id]
        
#         except KeyError:
#             raise LinkDoesNotExist(entity_id)


#     def get_user_links(self, owner_id: UUID) -> List[Link]:
#         return [link for link in self._db.values() if owner_id == link.owner_id]


#     def get_all_expired(self, owner_id: UUID) -> List[Link]:
#         now = datetime.now(timezone.utc)
#         return [link for link in self._db.values() if owner_id == link.owner_id and link.expires_at is not None and link.expires_at < now]
    

#     def is_owner(self, url_id: UUID, owner_id: UUID) -> bool:
#         try:
#             return self._db[url_id].owner_id == owner_id
        
#         except KeyError:
#             raise LinkDoesNotExist(url_id)