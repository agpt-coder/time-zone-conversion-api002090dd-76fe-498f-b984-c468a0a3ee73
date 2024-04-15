import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.authenticate_user_service
import project.convert_timestamp_service
import project.health_check_service
import project.issue_api_key_service
import project.log_entry_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Time Zone Conversion API",
    lifespan=lifespan,
    description="To build a system that accepts a timestamp and its source time zone, then converts it to a specified target time zone while handling Daylight Saving Time (DST) adjustments, and returns the converted timestamp in ISO 8601 format, follow these steps with the specified tech stack:\n\n1. **Programming Language:** Python\n- Python is versatile and widely supported, ideal for datetime and timezone manipulations.\n\n2. **API Framework:** FastAPI\n- FastAPI will serve as the backend framework to receive timestamp conversion requests via API calls. It's fast, easy to use, and automatically generates interactive API documentation.\n\n3. **Database:** PostgreSQL\n- Although this task might not require database storage, PostgreSQL is chosen for potential future enhancements like logging or storing conversion histories.\n\n4. **ORM:** Prisma\n- Prisma will manage our PostgreSQL database interactions. Even though it's not essential for the timestamp conversion itself, it's included for potential future database-related features.\n\n**Implementation Steps:**\n- Install the required packages (`fastapi`, `uvicorn` for serving the app, `pytz` for timezone handling).\n\n- Define a FastAPI endpoint to accept `timestamp`, `source timezone`, and `target timezone` as input. Ensure inputs are validated.\n\n- Use Python's `datetime` and `pytz` libraries to handle the actual conversion:\n  - Parse the input timestamp and source timezone.\n  - Localize the timestamp to the source timezone making it aware.\n  - Convert the aware timestamp to the target timezone.\n  - Apply DST adjustments automatically with `pytz`'s transition rules.\n  - Format the converted timestamp into ISO 8601 format using `datetime.isoformat()`.\n\n- Return the converted timestamp in ISO format as the API response.\n\nHere's a simplified Python snippet representing the core functionality:\n\n```python\nfrom fastapi import FastAPI\nfrom datetime import datetime\nimport pytz\n\napp = FastAPI()\n\n@app.post('/convert-timestamp/')\ndef convert_timestamp(source_timestamp: str, source_tz: str, target_tz: str):\n    # Parse the timestamp\n    dt = datetime.fromisoformat(source_timestamp)\n    # Localize to source timezone\n    source_timezone = pytz.timezone(source_tz)\n    dt_source_tz = source_timezone.localize(dt)\n    # Convert to target timezone\n    target_timezone = pytz.timezone(target_tz)\n    dt_target_tz = dt_source_tz.astimezone(target_timezone)\n    # Return the converted timestamp in ISO 8601 format\n    return {'converted_timestamp': dt_target_tz.isoformat()}\n```\n\n- To serve the FastAPI app, run `uvicorn main:app --reload` where `main` is the file name.\n\nThis setup accomplishes the task of converting timestamps between time zones with DST adjustment and returns the converted timestamp in ISO 8601 format.",
)


@app.post(
    "/auth/api-key/", response_model=project.issue_api_key_service.IssueApiKeyResponse
)
async def api_post_issue_api_key(
    user_id: str, permissions: List[str]
) -> project.issue_api_key_service.IssueApiKeyResponse | Response:
    """
    Issues a new API key for authorized services.
    """
    try:
        res = await project.issue_api_key_service.issue_api_key(user_id, permissions)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/convert-timestamp/",
    response_model=project.convert_timestamp_service.TimestampConversionResponse,
)
async def api_post_convert_timestamp(
    source_timestamp: str, source_tz: str, target_tz: str
) -> project.convert_timestamp_service.TimestampConversionResponse | Response:
    """
    Converts a specified timestamp from one time zone to another considering DST adjustments.
    """
    try:
        res = project.convert_timestamp_service.convert_timestamp(
            source_timestamp, source_tz, target_tz
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/monitor/health/", response_model=project.health_check_service.HealthCheckResponse
)
async def api_get_health_check() -> project.health_check_service.HealthCheckResponse | Response:
    """
    Returns the system's health status.
    """
    try:
        res = project.health_check_service.health_check()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/logs/create/", response_model=project.log_entry_service.CreateLogEntryResponse
)
async def api_post_log_entry(
    action: str, description: Optional[str], ConversionRequestId: Optional[str]
) -> project.log_entry_service.CreateLogEntryResponse | Response:
    """
    Records a log entry for system events.
    """
    try:
        res = await project.log_entry_service.log_entry(
            action, description, ConversionRequestId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login/",
    response_model=project.authenticate_user_service.AuthenticationResponse,
)
async def api_post_authenticate_user(
    username: str, password: str
) -> project.authenticate_user_service.AuthenticationResponse | Response:
    """
    Authenticates user credentials and returns an access token.
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(
            username, password
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
