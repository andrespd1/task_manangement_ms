from datetime import timedelta, timezone, datetime
from typing import Annotated, Union
from fastapi import Depends, HTTPException, status
import jwt
from pydantic import BaseModel
from jwt.exceptions import InvalidTokenError
import os
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = (
    os.getenv("JWT_SECRET_KEY")
    if os.getenv("JWT_SECRET_KEY") is not None
    else "ecbd52b7622644f4b663c513c6360cf0b0b187908179a00cd5a169ec0cd1b85b"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    """
    Pydantic model representing a JWT token.

    Attributes:
    - access_token (str): The JWT token string.
    - token_type (str): The type of the token (usually "bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Pydantic model for storing token data.

    Attributes:
    - email (Union[str, None]): The email extracted from the token payload.
    """

    email: Union[str, None] = None


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Creates a JWT access token.

    Parameters:
    - data (dict): The data to encode in the token.
    - expires_delta (Union[timedelta, None], optional): The expiration time delta. Defaults to 15 minutes if not provided.

    Returns:
    - str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    Retrieves the current user from the JWT token.

    Parameters:
    - token (Annotated[str, Depends]): The JWT token.

    Returns:
    - TokenData: The token data containing the user's email.

    Raises:
    - HTTPException(401): If the token is invalid or the credentials could not be validated.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
