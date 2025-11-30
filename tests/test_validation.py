"""
Tests for validation utilities.
"""
import pytest
from pathlib import Path
from utils.validation import (
    validate_tree_structure,
    validate_json_file,
    count_tree_nodes,
    count_answered_questions
)


class TestValidation:
    """Test validation functions."""
    
    def test_validate_tree_structure_valid(self):
        """Test validation of valid tree structure."""
        valid_tree = {
            "id": "test_tree",
            "root": "q1",
            "nodes": {
                "q1": {
                    "type": "choice",
                    "text": "Test question?",
                    "options": {
                        "Yes": {"decision": "YES_DECISION", "explanation": "Yes explanation"},
                        "No": {"decision": "NO_DECISION", "explanation": "No explanation"}
                    }
                }
            }
        }
        is_valid, error = validate_tree_structure(valid_tree)
        assert is_valid is True
        assert error is None
    
    def test_validate_tree_structure_missing_id(self):
        """Test validation fails when ID is missing."""
        invalid_tree = {
            "root": "q1",
            "nodes": {}
        }
        is_valid, error = validate_tree_structure(invalid_tree)
        assert is_valid is False
        assert "id" in error
    
    def test_validate_tree_structure_missing_root(self):
        """Test validation fails when root is missing."""
        invalid_tree = {
            "id": "test",
            "nodes": {}
        }
        is_valid, error = validate_tree_structure(invalid_tree)
        assert is_valid is False
        assert "root" in error
    
    def test_count_tree_nodes(self):
        """Test counting nodes in tree."""
        tree = {
            "nodes": {
                "q1": {},
                "q2": {},
                "q3": {}
            }
        }
        assert count_tree_nodes(tree) == 3
    
    def test_count_answered_questions(self):
        """Test counting answered questions."""
        answers = {
            "q1": "Yes",
            "q2": "No",
            "q3": None,
            "q4": ""
        }
        assert count_answered_questions(answers) == 2

