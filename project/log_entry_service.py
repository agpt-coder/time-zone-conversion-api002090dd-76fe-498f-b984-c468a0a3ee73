from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateLogEntryResponse(BaseModel):
    """
    The response model for the log entry creation operation, confirming the successful creation of a log entry.
    """

    success: bool
    log_id: Optional[str] = None
    message: Optional[str] = None


async def log_entry(
    action: str, description: Optional[str], ConversionRequestId: Optional[str]
) -> CreateLogEntryResponse:
    """
    Records a log entry for system events.

    Args:
        action (str): The action that occurred, triggering this log entry.
        description (Optional[str]): A detailed description of the event or error encountered.
        ConversionRequestId (Optional[str]): The unique identifier of the conversion request related to this log, if any.

    Returns:
        CreateLogEntryResponse: The response model for the log entry creation operation, confirming the successful creation of a log entry.
    """
    new_log = await prisma.models.Log.prisma().create(
        data={
            "action": action,
            "description": description,
            "ConversionRequestId": ConversionRequestId,
        }
    )
    return CreateLogEntryResponse(
        success=True, log_id=new_log.id, message="Log entry successfully created."
    )
