"""
Tests for the core health checker functionality.
"""

from rest_health.core.checker import HealthCheck


def test_health_check_creation():
    """Test that a HealthCheck instance can be created."""
    health = HealthCheck()
    assert health is not None


def test_health_check_run():
    """Test running a health check with no checks configured."""
    health = HealthCheck()
    result = health.run()

    assert result["status"] == "ok"
    assert "checks" in result
    assert isinstance(result["checks"], dict)


def test_health_check_with_custom_check():
    """Test adding a custom health check."""
    health = HealthCheck()

    def dummy_check():
        return True  # Should return boolean, not dict

    health.add_check("dummy", dummy_check)
    result = health.run()

    assert result["status"] == "ok"
    assert "dummy" in result["checks"]
    assert result["checks"]["dummy"]["status"] == "ok"
    assert result["checks"]["dummy"]["success"] is True


def test_health_check_with_failing_check():
    """Test health check with a failing check."""
    health = HealthCheck()

    def failing_check():
        return False  # Should return boolean, not dict

    health.add_check("failing", failing_check)
    result = health.run()

    assert result["status"] == "fail"  # Overall status should be "fail"
    assert "failing" in result["checks"]
    assert result["checks"]["failing"]["status"] == "fail"
    assert result["checks"]["failing"]["success"] is False
