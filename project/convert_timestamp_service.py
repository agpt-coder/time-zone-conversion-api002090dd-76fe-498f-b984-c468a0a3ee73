from datetime import datetime

import pytz
from pydantic import BaseModel


class TimestampConversionResponse(BaseModel):
    """
    The result of converting a given timestamp from the source time zone to the target time zone, represented in ISO 8601 format.
    """

    converted_timestamp: str


def convert_timestamp(
    source_timestamp: str, source_tz: str, target_tz: str
) -> TimestampConversionResponse:
    """
    Converts a specified timestamp from one time zone to another considering DST adjustments.

    Args:
        source_timestamp (str): The original timestamp to be converted, in ISO 8601 format.
        source_tz (str): The IANA time zone name for the source timestamp's time zone.
        target_tz (str): The IANA time zone name for the target time zone to which the timestamp will be converted.

    Returns:
        TimestampConversionResponse: The result of converting a given timestamp from the source time zone to the target time zone, represented in ISO 8601 format.
    """
    dt = datetime.fromisoformat(source_timestamp)
    source_timezone = pytz.timezone(source_tz)
    dt_source_tz = source_timezone.localize(dt)
    target_timezone = pytz.timezone(target_tz)
    dt_target_tz = dt_source_tz.astimezone(target_timezone)
    return TimestampConversionResponse(converted_timestamp=dt_target_tz.isoformat())
