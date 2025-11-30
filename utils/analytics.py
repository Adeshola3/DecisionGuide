"""
Analytics and statistics utilities for DecisionGuide.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict
from utils.history import load_history


def get_statistics() -> Dict[str, Any]:
    """
    Get usage statistics from history.
    
    Returns:
        Dictionary of statistics
    """
    history = load_history()
    
    if not history:
        return {
            "total_assessments": 0,
            "tree_usage": {},
            "decision_distribution": {},
            "recent_activity": []
        }
    
    # Tree usage
    tree_usage = Counter(entry.get("tree_id", "unknown") for entry in history)
    
    # Decision distribution
    decision_distribution = Counter(entry.get("decision", "unknown") for entry in history)
    
    # Recent activity (last 7 days)
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_activity = []
    for entry in history:
        try:
            timestamp_str = entry.get("timestamp", "")
            if timestamp_str:
                entry_date = datetime.fromisoformat(timestamp_str)
                if entry_date > seven_days_ago:
                    recent_activity.append(entry)
        except (ValueError, AttributeError, TypeError):
            # Skip entries with invalid timestamps
            continue
    
    # Daily activity
    daily_activity = defaultdict(int)
    for entry in history:
        try:
            date = datetime.fromisoformat(entry.get("timestamp", "")).date()
            daily_activity[str(date)] += 1
        except (ValueError, AttributeError):
            pass
    
    return {
        "total_assessments": len(history),
        "tree_usage": dict(tree_usage),
        "decision_distribution": dict(decision_distribution),
        "recent_activity_count": len(recent_activity),
        "daily_activity": dict(daily_activity),
        "most_used_tree": tree_usage.most_common(1)[0][0] if tree_usage else None,
        "most_common_decision": decision_distribution.most_common(1)[0][0] if decision_distribution else None
    }


def search_history(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search history by query string.
    
    Args:
        query: Search query
        limit: Maximum results to return
        
    Returns:
        List of matching history entries
    """
    history = load_history()
    query_lower = query.lower()
    
    matches = []
    for entry in reversed(history):  # Most recent first
        if (query_lower in entry.get("tree_title", "").lower() or
            query_lower in entry.get("decision", "").lower() or
            query_lower in entry.get("explanation", "").lower()):
            matches.append(entry)
            if len(matches) >= limit:
                break
    
    return matches


def filter_history(
    tree_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    decision: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Filter history by criteria.
    
    Args:
        tree_id: Filter by tree ID
        start_date: Filter by start date
        end_date: Filter by end date
        decision: Filter by decision
        
    Returns:
        List of filtered history entries
    """
    history = load_history()
    filtered = []
    
    for entry in history:
        # Tree filter
        if tree_id and entry.get("tree_id") != tree_id:
            continue
        
        # Date filter
        try:
            entry_date = datetime.fromisoformat(entry.get("timestamp", ""))
            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue
        except (ValueError, AttributeError):
            continue
        
        # Decision filter
        if decision and entry.get("decision") != decision:
            continue
        
        filtered.append(entry)
    
    return list(reversed(filtered))  # Most recent first

