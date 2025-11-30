"""
Security utilities for DecisionGuide.
"""
import re
from typing import Any, Optional, Dict, Tuple
from datetime import datetime, timedelta
from collections import defaultdict


class RateLimiter:
    """Simple rate limiter for preventing abuse."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests per window
            window_seconds: Time window in seconds
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, identifier: str) -> bool:
        """
        Check if request is allowed.
        
        Args:
            identifier: Unique identifier (e.g., session ID)
            
        Returns:
            True if allowed, False if rate limited
        """
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window_seconds)
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if req_time > window_start
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        # Record request
        self.requests[identifier].append(now)
        return True


def sanitize_input(value: Any) -> str:
    """
    Sanitize user input to prevent XSS attacks.
    
    Args:
        value: Input value to sanitize
        
    Returns:
        Sanitized string
    """
    if value is None:
        return ""
    
    text = str(value)
    
    # Remove potentially dangerous characters and patterns
    # Remove script tags and event handlers
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'on\w+\s*=', '', text, flags=re.IGNORECASE)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    # Remove HTML tags (keep only safe ones if needed)
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    
    return text.strip()


def validate_circular_reference(tree_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate that decision tree has no circular references.
    
    Args:
        tree_data: Decision tree data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    nodes = tree_data.get("nodes", {})
    root = tree_data.get("root")
    
    if not root or root not in nodes:
        return False, "Invalid root node"
    
    visited = set()
    path = []
    
    def check_node(node_id: str) -> Tuple[bool, Optional[str]]:
        if node_id in path:
            return False, f"Circular reference detected: {' -> '.join(path)} -> {node_id}"
        
        if node_id in visited:
            return True, None
        
        visited.add(node_id)
        path.append(node_id)
        
        if node_id not in nodes:
            path.pop()
            return False, f"Node '{node_id}' not found"
        
        node = nodes[node_id]
        if node.get("type") == "choice" and "options" in node:
            for option_data in node["options"].values():
                if isinstance(option_data, dict) and "next" in option_data:
                    next_node = option_data["next"]
                    is_valid, error = check_node(next_node)
                    if not is_valid:
                        path.pop()
                        return False, error
        
        path.pop()
        return True, None
    
    return check_node(root)


def check_session_timeout(session_start: datetime, timeout_seconds: int) -> bool:
    """
    Check if session has timed out.
    
    Args:
        session_start: When session started
        timeout_seconds: Timeout in seconds
        
    Returns:
        True if session is still valid, False if timed out
    """
    elapsed = (datetime.now() - session_start).total_seconds()
    return elapsed < timeout_seconds

