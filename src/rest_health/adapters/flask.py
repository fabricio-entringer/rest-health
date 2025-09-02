"""
Flask adapter for rest-health library.

This module provides integration with Flask to expose health check endpoints.
"""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Blueprint, Response

from ..core.checker import HealthCheck


def create_flask_healthcheck(health: HealthCheck, path: str = "/health") -> "Blueprint":
    """
    Create a Flask blueprint with a health check endpoint.

    Args:
        health: HealthCheck instance to use for health checks
        path: URL path for the health endpoint (default: "/health")

    Returns:
        Flask Blueprint with the health check endpoint

    Raises:
        RuntimeError: If Flask is not installed
    """
    try:
        from flask import Blueprint, Response
    except ImportError:
        raise RuntimeError("Flask is not installed. Install it with: pip install flask")

    blueprint = Blueprint("health", __name__)

    @blueprint.route(path, methods=["GET"])
    def health_check() -> "Response":
        """Health check endpoint."""
        result = health.run()
        status_code = 200 if result["status"] == "ok" else 503

        return Response(
            response=json.dumps(result), status=status_code, mimetype="application/json"
        )

    return blueprint
