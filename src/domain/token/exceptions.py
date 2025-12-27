from uuid import UUID


class AccessTokenExpiredException(Exception):
    def __init__(self, access_token: str | None = None) -> None:
        if access_token is not None:
            self.msg = f"Access token {access_token} is outdated"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.access_token = access_token


class RefreshTokenExpiredException(Exception):
    def __init__(self, refresh_token: str | None = None) -> None:
        if refresh_token is not None:
            self.msg = f"Access token {refresh_token} is outdated"
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.refresh_token = refresh_token


class TokenDoesNotExistException(Exception):
    def __init__(self,
        *,
        access_token: str | None = None,
        refresh_token: str | None = None,
        token_id: UUID | None = None
    ) -> None:
        if access_token is not None:
            self.msg = f"Access token {access_token} does not exist"
            data = token_id
        if refresh_token is not None:
            self.msg = f"Refresh token {access_token} does not exist"
            data = access_token
        if token_id is not None:
            self.msg = f"Token with id {token_id} does not exist"
            data = refresh_token
        else:
            self.msg = ""
        super().__init__(self.msg)
        
        self.data = data