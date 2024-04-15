from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """
    This model encapsulates the health status of the system, providing key performance indicators such as uptime, response time, and error rates to give a comprehensive view of system health.
    """

    status: str
    uptime: str
    response_time_avg: float
    error_rate: float


def health_check() -> HealthCheckResponse:
    """
    Returns the system's health status.

    This function simulates a health check by constructing a HealthCheckResponse object
    with fictional data since there's no real system or monitoring data to query.

    Args:


    Returns:
        HealthCheckResponse: This model encapsulates the health status of the system, providing key performance
        indicators such as uptime, response time, and error rates to give a comprehensive view of system health.
    """
    uptime = "48:00:00"
    response_time_avg = 0.5
    error_rate = 0.02
    status = "Healthy" if response_time_avg < 1 and error_rate < 0.05 else "Unhealthy"
    health_status = HealthCheckResponse(
        status=status,
        uptime=uptime,
        response_time_avg=response_time_avg,
        error_rate=error_rate,
    )
    return health_status
