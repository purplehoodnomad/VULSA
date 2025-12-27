from datetime import datetime, timedelta

from domain.value_objects.common import UserId
from domain.value_objects.token import Token as TokenVO, TokenId
from .exceptions import RefreshTokenExpiredException


class Token:
    """Token entity"""

    def __init__(
        self,
        *,
        token_id: TokenId,
        user_id: UserId,
        access_token: TokenVO,
        refresh_token: TokenVO,
        access_token_expires_at: datetime,
        refresh_token_expires_at: datetime,   
        created_at: datetime
    ):
        self._token_id = token_id
        self._user_id = user_id
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._access_token_expires_at = access_token_expires_at
        self._refresh_token_expires_at = refresh_token_expires_at
        self._created_at = created_at


    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Token):
            return self.token_id == obj.token_id
        return False
    
    @property
    def token_id(self) -> TokenId:
        return self._token_id
    
    @property
    def user_id(self) -> UserId:
        return self._user_id
    
    @property
    def access_token(self) -> TokenVO:
        return self._access_token

    @property
    def refresh_token(self) -> TokenVO:
        return self._refresh_token
    
    @property
    def access_token_expires_at(self) -> datetime:
        return self._access_token_expires_at

    @property
    def refresh_token_expires_at(self) -> datetime:
        return self._refresh_token_expires_at

    @property
    def created_at(self) -> datetime:
        return self._created_at
    

    @staticmethod
    def create(*,
        user_id: UserId,
    ) -> "Token":
        """Creates Token entity"""
        now = datetime.now()

        return Token(
            token_id=TokenId.generate(),
            user_id=user_id,
            access_token=TokenVO.generate(),
            refresh_token=TokenVO.generate(),
            access_token_expires_at=now + timedelta(minutes=15),
            refresh_token_expires_at=now + timedelta(hours=24),
            created_at=datetime.now()
        )
    
    def refresh(self) -> None:
        "Refreshes access token"
        now = datetime.now()
        if now >= self._refresh_token_expires_at:
            raise RefreshTokenExpiredException(self.refresh_token.value)
        
        self._access_token = TokenVO.generate()
        self._access_token_expires_at = now + timedelta(minutes=15)
    
    
    def drop(self) -> None:
        now = datetime.now()
        self._refresh_token_expires_at=now


    def is_access_token_valid(self) -> bool:
        return datetime.now() < self.access_token_expires_at

    def is_refresh_token_valid(self) -> bool:
        return datetime.now() < self.refresh_token_expires_at