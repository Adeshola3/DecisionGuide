"""
JSON validation utilities for decision trees.
"""
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path


def validate_tree_structure(tree_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validate that a decision tree JSON has the required structure.
    
    Args:
        tree_data: Dictionary containing tree data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ["id", "root", "nodes"]
    
    for field in required_fields:
        if field not in tree_data:
            return False, f"Missing required field: {field}"
    
    if not isinstance(tree_data["nodes"], dict):
        return False, "Nodes must be a dictionary"
    
    if tree_data["root"] not in tree_data["nodes"]:
        return False, f"Root node '{tree_data['root']}' not found in nodes"
    
    # Validate each node
    for node_id, node in tree_data["nodes"].items():
        if not isinstance(node, dict):
            return False, f"Node '{node_id}' must be a dictionary"
        
        node_type = node.get("type", "choice")
        
        if node_type == "choice":
            if "options" not in node:
                return False, f"Choice node '{node_id}' missing 'options' field"
            
            if not isinstance(node["options"], dict):
                return False, f"Node '{node_id}' options must be a dictionary"
            
            # Validate each option
            for option_text, option_data in node["options"].items():
                if not isinstance(option_data, dict):
                    return False, f"Option '{option_text}' in node '{node_id}' must be a dictionary"
                
                if "decision" not in option_data and "next" not in option_data:
                    return False, f"Option '{option_text}' in node '{node_id}' must have 'decision' or 'next'"
                
                # If it has 'next', validate that the next node exists
                if "next" in option_data:
                    next_node = option_data["next"]
                    if next_node not in tree_data["nodes"]:
                        return False, f"Option '{option_text}' in node '{node_id}' references non-existent node '{next_node}'"
    
    return True, None


def validate_json_file(file_path: Path) -> Tuple[bool, Optional[str], Optional[Dict]]:
    """
    Validate a JSON file and return the parsed data if valid.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Tuple of (is_valid, error_message, parsed_data)
    """
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}", None
    except Exception as e:
        return False, f"Error reading file: {str(e)}", None
    
    is_valid, error = validate_tree_structure(data)
    if not is_valid:
        return False, error, None
    
    return True, None, data


def count_tree_nodes(tree_data: Dict[str, Any]) -> int:
    """
    Count total number of nodes in a decision tree.
    
    Args:
        tree_data: Dictionary containing tree data
        
    Returns:
        Number of nodes
    """
    return len(tree_data.get("nodes", {}))


def count_answered_questions(answers: Dict[str, Any]) -> int:
    """
    Count number of answered questions.
    
    Args:
        answers: Dictionary of answers
        
    Returns:
        Number of answered questions
    """
    return len([v for v in answers.values() if v is not None and v != ""])

