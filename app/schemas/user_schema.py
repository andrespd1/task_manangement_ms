from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    repeat_password: str


class User(UserBase):
    id: str

    class Config:
        orm_mode = True
