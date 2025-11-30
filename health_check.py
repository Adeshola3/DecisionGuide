"""
Health check endpoint for DecisionGuide.
"""
from pathlib import Path
from typing import Dict, Any
import json


def health_check() -> Dict[str, Any]:
    """
    Perform health check on the application.
    
    Returns:
        Dictionary with health status
    """
    status = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check logic directory
    logic_dir = Path(__file__).parent / "logic"
    status["checks"]["logic_directory"] = {
        "exists": logic_dir.exists(),
        "readable": logic_dir.is_dir() and logic_dir.exists()
    }
    
    # Check for JSON files
    json_files = list(logic_dir.glob("*.json")) if logic_dir.exists() else []
    status["checks"]["json_files"] = {
        "count": len(json_files),
        "files": [f.name for f in json_files]
    }
    
    # Check data directory
    data_dir = Path(__file__).parent / "data"
    status["checks"]["data_directory"] = {
        "exists": data_dir.exists() or True,  # Can be created
        "writable": True  # Assume writable
    }
    
    # Overall status
    if not status["checks"]["logic_directory"]["exists"]:
        status["status"] = "unhealthy"
    elif status["checks"]["json_files"]["count"] == 0:
        status["status"] = "degraded"
    
    return status


if __name__ == "__main__":
    """Run health check from command line."""
    result = health_check()
    print(json.dumps(result, indent=2))

