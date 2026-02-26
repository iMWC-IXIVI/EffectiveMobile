from pydantic import BaseModel, UUID4


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


class User(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    surname: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    email: str
    last_name: str
