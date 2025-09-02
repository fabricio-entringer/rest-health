# rest-health

<div align="center">
  <img src="https://raw.githubusercontent.com/fabricio-entringer/rest-health/master/assets/rest-health-logo.png" alt="rest-health logo" width="200">
</div>

**Framework-agnostic REST healthcheck endpoints for Python web apps**

`rest-health` provides a simple, lightweight way to expose standardized REST healthcheck endpoints across different Python web frameworks. No unnecessary complexity - just clean, production-ready health monitoring.

## Features

- **Framework-agnostic**: Works with FastAPI, Flask, and any other Python web framework
- **Lightweight**: Zero external dependencies for core functionality
- **Simple API**: Register health checks as simple functions
- **Production-ready**: Proper error handling and standard HTTP status codes
- **Extensible**: Easy to add custom health checks

## Installation

```bash
pip install rest-health
```

For framework-specific integrations:

```bash
# For FastAPI
pip install rest-health[fastapi]

# For Flask
pip install rest-health[flask]
```

## Quick Start

### Basic Usage

```python
from rest_health import HealthCheck

# Create a health checker
health = HealthCheck()

# Add a simple check
def database_check():
    # Your database connectivity check logic
    return True  # or False if unhealthy

health.add_check("database", database_check)

# Run all checks
result = health.run()
# Returns: {"status": "ok", "checks": {"database": {"status": "ok", "success": True}}}
```

### FastAPI Integration

```python
from fastapi import FastAPI
from rest_health import HealthCheck
from rest_health.adapters.fastapi import create_fastapi_healthcheck

app = FastAPI()

# Setup health checks
health = HealthCheck()

def database_check():
    # Check database connectivity
    return True

def cache_check():
    # Check cache connectivity  
    return True

health.add_check("database", database_check)
health.add_check("cache", cache_check)

# Add health endpoint
health_router = create_fastapi_healthcheck(health)
app.include_router(health_router)

# Now GET /health returns health status
```

### Flask Integration

```python
from flask import Flask
from rest_health import HealthCheck
from rest_health.adapters.flask import create_flask_healthcheck

app = Flask(__name__)

# Setup health checks
health = HealthCheck()

def database_check():
    # Check database connectivity
    return True

health.add_check("database", database_check)

# Add health endpoint
health_blueprint = create_flask_healthcheck(health)
app.register_blueprint(health_blueprint)

# Now GET /health returns health status
```

## Advanced Usage

### Custom Health Checks

```python
from rest_health import HealthCheck
import requests

health = HealthCheck()

def external_api_check():
    """Check if external API is responsive."""
    try:
        response = requests.get("https://api.example.com/ping", timeout=5)
        return response.status_code == 200
    except:
        return False

def database_check():
    """Check database connectivity."""
    try:
        # Your database check logic here
        return True
    except:
        return False

health.add_check("external_api", external_api_check)
health.add_check("database", database_check)
```

### Error Handling

When a health check raises an exception, it's automatically caught and the check is marked as failed:

```python
def failing_check():
    raise ValueError("Something went wrong")

health.add_check("problematic_service", failing_check)

result = health.run()
# Returns:
# {
#   "status": "fail",
#   "checks": {
#     "problematic_service": {
#       "status": "fail",
#       "success": False,
#       "error": "Something went wrong"
#     }
#   }
# }
```

### Custom Endpoint Path

```python
# FastAPI - custom path
health_router = create_fastapi_healthcheck(health, path="/api/health")

# Flask - custom path  
health_blueprint = create_flask_healthcheck(health, path="/api/health")
```

## Response Format

Health check endpoints return JSON with the following structure:

```json
{
  "status": "ok",  // "ok" or "fail"
  "checks": {
    "database": {
      "status": "ok",     // "ok" or "fail"
      "success": true
    },
    "cache": {
      "status": "fail",
      "success": false,
      "error": "Connection timeout"  // Only present on error
    }
  }
}
```

## HTTP Status Codes

- `200 OK`: All health checks passed
- `503 Service Unavailable`: One or more health checks failed

## Design Philosophy

`rest-health` follows these principles:

- **Simplicity**: No background tasks, no async complexity, no unnecessary features
- **Framework-agnostic**: Core logic works with any Python web framework
- **Lightweight**: Minimal dependencies and overhead
- **Production-ready**: Proper error handling and observability

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

For detailed technical information, development setup, coding standards, and contribution guidelines, please see our [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
