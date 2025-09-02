"""
rest-health: Framework-agnostic REST healthcheck endpoints for Python web apps.

A simple, lightweight library for exposing standardized health check endpoints
across different Python web frameworks.
"""

from .core.checker import HealthCheck

__version__ = "0.1.0"
__all__ = ["HealthCheck"]
