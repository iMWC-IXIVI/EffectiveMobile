from pydantic import BaseModel


class UserRegistration(BaseModel):
    first_name: str
    last_name: str
    surname: str
    email: str
    password: str
    accept_password: str


class UserLogin(BaseModel):
    email: str
    password: str
