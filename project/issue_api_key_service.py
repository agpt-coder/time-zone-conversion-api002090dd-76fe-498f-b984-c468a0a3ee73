import uuid
from datetime import datetime, timedelta
from typing import List

import prisma
import prisma.enums
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class IssueApiKeyResponse(BaseModel):
    """
    Response model for issuing a new API key. Includes the API key and info on the permissions granted.
    """

    api_key: str
    permissions: List[str]
    expiration_date: datetime


async def issue_api_key(user_id: str, permissions: List[str]) -> IssueApiKeyResponse:
    """
    Issues a new API key for authorized services.

    This function generates a new API key for a user, sets an expiration date,
    and updates the user record in the database with the new API key and its associated permissions.

    Args:
        user_id (str): The unique identifier of the user making the request. Used to verify if the user has the permissions to issue new API keys.
        permissions (List[str]): A list of permissions associated with the API key being requested. This will determine what actions the key holder may perform.

    Returns:
        IssueApiKeyResponse: Response model for issuing a new API key. Includes the API key and info on the permissions granted.

    Example:
        issue_api_key('1234', ['read', 'write'])
        > IssueApiKeyResponse(api_key='newapikey123', permissions=['read', 'write'], expiration_date=datetime.datetime(2023, 9, 30))
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if user.role != prisma.enums.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Insufficient permissions.")
    new_api_key = str(uuid.uuid4())
    expiration_date = datetime.now() + timedelta(days=365)
    await prisma.models.User.prisma().update(
        where={"id": user_id}, data={"apiKey": new_api_key}
    )
    return IssueApiKeyResponse(
        api_key=new_api_key, permissions=permissions, expiration_date=expiration_date
    )
