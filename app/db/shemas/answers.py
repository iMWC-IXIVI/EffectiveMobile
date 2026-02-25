from pydantic import BaseModel


class Success(BaseModel):
    message: str = 'success'
