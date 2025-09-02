"""
FastAPI adapter for rest-health library.

This module provides integration with FastAPI to expose health check endpoints.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, Union

try:
    from fastapi import APIRouter, status
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel
except ImportError:
    raise RuntimeError("FastAPI is not installed. Install it with: pip install fastapi")

if TYPE_CHECKING:
    from ..core.checker import HealthCheck


class HealthResponse(BaseModel):
    """
    Pydantic model for the health check response.
    This provides a clear contract for the API.
    """

    status: str
    checks: Dict[str, Any]


def create_fastapi_healthcheck(health: HealthCheck, path: str = "/health") -> APIRouter:
    """
    Create a FastAPI router with a health check endpoint.

    Args:
        health: HealthCheck instance to use for health checks
        path: URL path for the health endpoint (default: "/health")

    Returns:
        FastAPI APIRouter with the health check endpoint
    """
    router = APIRouter()

    @router.get(
        path,
        response_model=HealthResponse,
        status_code=status.HTTP_200_OK,
        responses={
            200: {"description": "Service is healthy", "model": HealthResponse},
            503: {
                "description": "Service is unhealthy - one or more health checks failed",
                "model": HealthResponse,
            },
        },
    )
    def health_check() -> Union[Dict[str, Any], JSONResponse]:
        """Health check endpoint."""
        result = health.run()
        if result["status"] == "ok":
            return result

        # When returning a 503 status, you must use a custom JSONResponse
        # to override the default behavior.
        return JSONResponse(
            content=result, status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )

    return router
