"""
Integration tests for DecisionGuide.
"""
import pytest
from pathlib import Path
import json
from utils.validation import validate_json_file
from utils.export import export_to_json, export_to_csv
from utils.history import add_to_history, get_recent_history, clear_history
from utils.analytics import get_statistics, search_history
from utils.security import validate_circular_reference


class TestIntegration:
    """Integration tests for full workflows."""
    
    def test_complete_assessment_flow(self):
        """Test complete assessment flow from start to finish."""
        # Clear history first
        clear_history()
        
        # Simulate assessment
        tree_id = "test_tree"
        tree_title = "Test Assessment"
        decision = "TEST_DECISION"
        explanation = "Test explanation"
        path = ["Q1 → Yes", "Q2 → No"]
        answers = {"q1": "Yes", "q2": "No"}
        
        # Add to history
        result = add_to_history(tree_id, tree_title, decision, explanation, path, answers)
        assert result is True
        
        # Retrieve history
        history = get_recent_history(limit=1)
        assert len(history) == 1
        assert history[0]["decision"] == decision
        assert history[0]["tree_id"] == tree_id
    
    def test_export_formats(self):
        """Test all export formats."""
        tree_title = "Test Assessment"
        decision = "TEST_DECISION"
        explanation = "Test explanation"
        path = ["Step 1", "Step 2"]
        
        # Test JSON export
        json_data = export_to_json(tree_title, decision, explanation, path)
        assert "assessment" in json_data
        assert decision in json_data
        
        # Test CSV export
        csv_data = export_to_csv(tree_title, decision, explanation, path)
        assert "DecisionGuide" in csv_data
        assert decision in csv_data
    
    def test_analytics_integration(self):
        """Test analytics with history."""
        clear_history()
        
        # Add some test data
        for i in range(3):
            add_to_history(
                f"tree_{i % 2}",
                f"Tree {i % 2}",
                f"Decision {i}",
                "Explanation",
                ["Step 1"],
                {"q1": "Yes"}
            )
        
        stats = get_statistics()
        assert stats["total_assessments"] == 3
        assert len(stats["tree_usage"]) > 0
    
    def test_search_functionality(self):
        """Test history search."""
        clear_history()
        
        add_to_history(
            "test_tree",
            "Vendor Assessment",
            "HIGH_RISK",
            "High risk vendor",
            ["Step 1"],
            {}
        )
        
        results = search_history("vendor", limit=5)
        assert len(results) > 0
        assert any("vendor" in r.get("tree_title", "").lower() for r in results)
    
    def test_circular_reference_validation(self):
        """Test circular reference detection."""
        # Valid tree
        valid_tree = {
            "id": "test",
            "root": "q1",
            "nodes": {
                "q1": {
                    "type": "choice",
                    "text": "Question 1",
                    "options": {
                        "Yes": {"decision": "YES"}
                    }
                }
            }
        }
        is_valid, error = validate_circular_reference(valid_tree)
        assert is_valid is True
        
        # Tree with circular reference
        circular_tree = {
            "id": "test",
            "root": "q1",
            "nodes": {
                "q1": {
                    "type": "choice",
                    "text": "Question 1",
                    "options": {
                        "Yes": {"next": "q2"}
                    }
                },
                "q2": {
                    "type": "choice",
                    "text": "Question 2",
                    "options": {
                        "Yes": {"next": "q1"}  # Circular!
                    }
                }
            }
        }
        is_valid, error = validate_circular_reference(circular_tree)
        assert is_valid is False
        assert "Circular" in error or "circular" in error

