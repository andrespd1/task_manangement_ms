from passlib.context import CryptContext

# Setting up the CryptContext for password hashing using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain password against a hashed password.

    Parameters:
    - plain_password (str): The plain text password to verify.
    - hashed_password (str): The hashed password to verify against.

    Returns:
    - bool: True if the password matches, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain password.

    Parameters:
    - password (str): The plain text password to hash.

    Returns:
    - str: The hashed password.
    """
    return pwd_context.hash(password)
