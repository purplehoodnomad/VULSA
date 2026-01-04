from datetime import datetime, timedelta, timezone

from domain.value_objects.common import UserId
from domain.value_objects.token import TokenVO, TokenId
from .exceptions import RefreshTokenExpired, AccessTokenExpired


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
        """Refreshes access token.
        Raises:
            RefreshTokenExpired: When token is expired.
        """
        now = datetime.now(timezone.utc)
        self.validate_refresh_token()
        
        self._access_token = TokenVO.generate()
        self._access_token_expires_at = now + timedelta(minutes=15)
    
    
    def drop(self) -> None:
        """Sets refresh token expiration date to current time."""
        now = datetime.now(timezone.utc)
        self._refresh_token_expires_at=now


    def validate_access_token(self) -> None:
        """Validates access token.
        Raises:
            AccessTokenExpired: When token is expired.
        """
        if datetime.now(timezone.utc) > self.access_token_expires_at:
            raise AccessTokenExpired()

    def validate_refresh_token(self) -> None:
        """Validates refresh token.
        Raises:
            RefreshTokenExpired: When token is expired.
        """
        if datetime.now(timezone.utc) > self.refresh_token_expires_at:
            raise RefreshTokenExpired()