from pydantic import BaseModel


class Success(BaseModel):
    message: str = 'success'


class JWTTokens(BaseModel):
    access_token: str
    refresh_token: str
