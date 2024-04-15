from datetime import datetime, timedelta

import jwt
import prisma
import prisma.models
from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel


class AuthenticationResponse(BaseModel):
    """
    The response object containing the access token for an authenticated session.
    """

    access_token: str
    token_type: str


SECRET_KEY = "YOUR_SECRET_KEY"

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hashed version.

    Args:
        plain_password (str): Plain text password to verify.
        hashed_password (str): Hashed version of the password to verify against.

    Returns:
        bool: True if the verification is successful, False otherwise.

    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(username: str) -> prisma.models.User:
    """
    Fetches a user by the username from the database.

    Args:
        username (str): The username of the user to fetch.

    Returns:
        prisma.models.User: The user object if the user exists.

    Raises:
        HTTPException: If the user does not exist.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Creates a JWT access token with specified data and expiry.

    Args:
        data (dict): Payload data for the token.
        expires_delta (timedelta, optional): Expiry duration for the token. Defaults to 15 minutes.

    Returns:
        str: The JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + expires_delta})
    else:
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=15)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str) -> AuthenticationResponse:
    """
    Authenticates a user using their username and password.

    Args:
        username (str): The user's username.
        password (str): The user's password.

    Returns:
        AuthenticationResponse: An object containing the JWT access token and the token type upon successful authentication.

    Raises:
        HTTPException: With status code 401 Unauthorized, if authentication fails.
    """
    user = await get_user(username)
    if not await verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return AuthenticationResponse(access_token=access_token, token_type="bearer")
