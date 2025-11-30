"""
Tree versioning utilities for DecisionGuide.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib


def get_tree_version(tree_data: Dict[str, Any]) -> str:
    """
    Generate a version hash for a decision tree.
    
    Args:
        tree_data: Decision tree data
        
    Returns:
        Version hash string
    """
    # Create a stable representation of the tree
    tree_str = json.dumps(tree_data, sort_keys=True)
    return hashlib.md5(tree_str.encode()).hexdigest()[:8]


def get_tree_metadata(tree_path: Path) -> Dict[str, Any]:
    """
    Get metadata for a decision tree file.
    
    Args:
        tree_path: Path to tree JSON file
        
    Returns:
        Dictionary with metadata
    """
    stat = tree_path.stat()
    
    try:
        with tree_path.open("r", encoding="utf-8") as f:
            tree_data = json.load(f)
        
        return {
            "file_path": str(tree_path),
            "file_name": tree_path.name,
            "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "size_bytes": stat.st_size,
            "tree_id": tree_data.get("id"),
            "tree_title": tree_data.get("title"),
            "version": get_tree_version(tree_data),
            "node_count": len(tree_data.get("nodes", {}))
        }
    except Exception:
        return {
            "file_path": str(tree_path),
            "file_name": tree_path.name,
            "error": "Failed to read tree"
        }


def compare_tree_versions(tree1_data: Dict[str, Any], tree2_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare two versions of a tree.
    
    Args:
        tree1_data: First tree data
        tree2_data: Second tree data
        
    Returns:
        Comparison results
    """
    v1 = get_tree_version(tree1_data)
    v2 = get_tree_version(tree2_data)
    
    return {
        "version1": v1,
        "version2": v2,
        "are_identical": v1 == v2,
        "tree1_node_count": len(tree1_data.get("nodes", {})),
        "tree2_node_count": len(tree2_data.get("nodes", {}))
    }

