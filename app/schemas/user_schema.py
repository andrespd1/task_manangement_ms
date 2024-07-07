from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    repeat_password: str


class User(UserBase):
    id: str

    class Config:
        orm_mode = True
