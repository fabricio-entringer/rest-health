"""
FastAPI adapter for rest-health library.

This module provides integration with FastAPI to expose health check endpoints.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import APIRouter, Response

from ..core.checker import HealthCheck


def create_fastapi_healthcheck(
    health: HealthCheck, path: str = "/health"
) -> "APIRouter":
    """
    Create a FastAPI router with a health check endpoint.

    Args:
        health: HealthCheck instance to use for health checks
        path: URL path for the health endpoint (default: "/health")

    Returns:
        FastAPI APIRouter with the health check endpoint

    Raises:
        RuntimeError: If FastAPI is not installed
    """
    try:
        from fastapi import APIRouter
    except ImportError:
        raise RuntimeError(
            "FastAPI is not installed. Install it with: pip install fastapi"
        )

    router = APIRouter()

    @router.get(path)
    def health_check() -> "Response":
        """Health check endpoint."""
        import json

        result = health.run()
        status_code = 200 if result["status"] == "ok" else 503

        from fastapi import Response

        return Response(
            content=json.dumps(result),
            status_code=status_code,
            media_type="application/json",
        )

    return router
