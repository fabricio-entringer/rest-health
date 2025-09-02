"""
Unit tests for rest-health library.
"""

import pytest
from rest_health import HealthCheck


class TestHealthCheck:
    """Test cases for the HealthCheck class."""

    def test_empty_healthcheck(self):
        """Test health check with no registered checks."""
        health = HealthCheck()
        result = health.run()

        assert result["status"] == "ok"
        assert result["checks"] == {}

    def test_single_passing_check(self):
        """Test health check with a single passing check."""
        health = HealthCheck()

        def dummy_check():
            return True

        health.add_check("database", dummy_check)
        result = health.run()

        assert result["status"] == "ok"
        assert result["checks"]["database"]["status"] == "ok"
        assert result["checks"]["database"]["success"] is True

    def test_single_failing_check(self):
        """Test health check with a single failing check."""
        health = HealthCheck()

        def failing_check():
            return False

        health.add_check("service", failing_check)
        result = health.run()

        assert result["status"] == "fail"
        assert result["checks"]["service"]["status"] == "fail"
        assert result["checks"]["service"]["success"] is False

    def test_mixed_checks(self):
        """Test health check with both passing and failing checks."""
        health = HealthCheck()

        def passing_check():
            return True

        def failing_check():
            return False

        health.add_check("database", passing_check)
        health.add_check("cache", failing_check)
        result = health.run()

        # Overall status should be fail if any check fails
        assert result["status"] == "fail"
        assert result["checks"]["database"]["status"] == "ok"
        assert result["checks"]["cache"]["status"] == "fail"

    def test_exception_handling(self):
        """Test that exceptions in checks are handled gracefully."""
        health = HealthCheck()

        def error_check():
            raise ValueError("Something went wrong")

        health.add_check("error_prone", error_check)
        result = health.run()

        assert result["status"] == "fail"
        assert result["checks"]["error_prone"]["status"] == "fail"
        assert result["checks"]["error_prone"]["success"] is False
        assert "Something went wrong" in result["checks"]["error_prone"]["error"]

    def test_multiple_checks_with_exception(self):
        """Test multiple checks where one throws an exception."""
        health = HealthCheck()

        def passing_check():
            return True

        def error_check():
            raise RuntimeError("Connection failed")

        health.add_check("healthy_service", passing_check)
        health.add_check("failing_service", error_check)
        result = health.run()

        assert result["status"] == "fail"
        assert result["checks"]["healthy_service"]["status"] == "ok"
        assert result["checks"]["failing_service"]["status"] == "fail"
        assert "error" in result["checks"]["failing_service"]
