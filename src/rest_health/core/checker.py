"""
Core healthcheck functionality for rest-health library.

This module provides the main HealthCheck class that manages health checks
and generates health status reports.
"""

from typing import Dict, Any, Callable


class HealthCheck:
    """
    A simple healthcheck registry that stores and executes health checks.

    The HealthCheck class allows registering multiple health checks as functions
    and provides a unified way to execute them and collect their results.
    """

    def __init__(self) -> None:
        """Initialize a new HealthCheck instance."""
        self._checks: Dict[str, Callable[[], bool]] = {}

    def add_check(self, name: str, func: Callable[[], bool]) -> None:
        """
        Register a new health check function.

        Args:
            name: Unique identifier for the health check
            func: Function that returns True if healthy, False otherwise
        """
        self._checks[name] = func

    def run(self) -> Dict[str, Any]:
        """
        Execute all registered health checks and return results.

        Returns:
            Dictionary containing:
            - status: "ok" if all checks pass, "fail" if any check fails
            - checks: Dictionary mapping check names to their results
        """
        results = {}
        overall_status = "ok"

        for name, check_func in self._checks.items():
            try:
                check_result = check_func()
                results[name] = {
                    "status": "ok" if check_result else "fail",
                    "success": check_result,
                }
                if not check_result:
                    overall_status = "fail"
            except Exception as e:
                results[name] = {"status": "fail", "success": False, "error": str(e)}
                overall_status = "fail"

        return {"status": overall_status, "checks": results}
