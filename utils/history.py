"""
History tracking utilities for DecisionGuide.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


HISTORY_FILE = Path(__file__).parent.parent / "data" / "decision_history.json"


def ensure_data_directory():
    """Ensure data directory exists."""
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_history() -> List[Dict[str, Any]]:
    """
    Load decision history from file.
    
    Returns:
        List of history entries
    """
    ensure_data_directory()
    
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with HISTORY_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history: List[Dict[str, Any]]) -> bool:
    """
    Save decision history to file.
    
    Args:
        history: List of history entries
        
    Returns:
        True if successful, False otherwise
    """
    ensure_data_directory()
    
    try:
        with HISTORY_FILE.open("w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def add_to_history(
    tree_id: str,
    tree_title: str,
    decision: str,
    explanation: str,
    path: List[str],
    answers: Dict[str, Any]
) -> bool:
    """
    Add a decision to history.
    
    Args:
        tree_id: ID of the decision tree
        tree_title: Title of the decision tree
        decision: Final decision
        explanation: Explanation text
        path: Decision path taken
        answers: Answers provided
        
    Returns:
        True if successful, False otherwise
    """
    history = load_history()
    
    entry = {
        "timestamp": datetime.now().isoformat(),
        "tree_id": tree_id,
        "tree_title": tree_title,
        "decision": decision,
        "explanation": explanation,
        "path": path,
        "answers": answers
    }
    
    history.append(entry)
    
    # Keep only last 100 entries
    if len(history) > 100:
        history = history[-100:]
    
    return save_history(history)


def get_recent_history(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent history entries.
    
    Args:
        limit: Maximum number of entries to return
        
    Returns:
        List of recent history entries (most recent first)
    """
    history = load_history()
    return list(reversed(history[-limit:]))


def clear_history() -> bool:
    """
    Clear all history.
    
    Returns:
        True if successful, False otherwise
    """
    return save_history([])

