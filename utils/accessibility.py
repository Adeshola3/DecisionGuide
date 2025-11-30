"""
Accessibility utilities for DecisionGuide.
"""
from typing import Dict, Any, Optional


def get_aria_label(text: str, context: Optional[str] = None) -> str:
    """
    Generate ARIA label for accessibility.
    
    Args:
        text: Element text
        context: Additional context
        
    Returns:
        ARIA label string
    """
    if context:
        return f"{context}: {text}"
    return text


def get_aria_described_by(description: str) -> str:
    """
    Generate ARIA described-by attribute.
    
    Args:
        description: Description text
        
    Returns:
        ID for described-by attribute
    """
    # In a real implementation, this would generate unique IDs
    return description.replace(" ", "-").lower()


def format_for_screen_reader(text: str) -> str:
    """
    Format text for better screen reader compatibility.
    
    Args:
        text: Text to format
        
    Returns:
        Formatted text
    """
    # Remove excessive punctuation that screen readers might struggle with
    text = text.replace("...", ".")
    text = text.replace("--", "-")
    return text

