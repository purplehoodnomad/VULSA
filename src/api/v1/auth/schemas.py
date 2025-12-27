from pydantic import BaseModel, EmailStr, model_validator


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str
