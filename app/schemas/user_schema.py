from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base schema for a user.

    Attributes:
    - name (str): The name of the user.
    - email (EmailStr): The email address of the user.
    """

    name: str
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.

    Attributes:
    - password (str): The password for the user.
    - repeat_password (str): The repeated password for confirmation.
    """

    password: str
    repeat_password: str


class User(UserBase):
    """
    Schema for a user with an ID.

    Attributes:
    - id (str): The unique identifier of the user.
    """

    id: str

    class Config:
        orm_mode = True
