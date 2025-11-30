"""
Tests for export functions.
"""
import pytest
from utils.export import (
    export_to_json, export_to_text, export_to_csv,
    export_history_to_csv, get_filename
)


class TestExport:
    """Test export functions."""
    
    def test_export_to_json(self):
        """Test JSON export."""
        data = export_to_json(
            "Test Assessment",
            "TEST_DECISION",
            "Test explanation",
            ["Step 1", "Step 2"]
        )
        assert isinstance(data, str)
        assert "Test Assessment" in data
        assert "TEST_DECISION" in data
    
    def test_export_to_text(self):
        """Test text export."""
        data = export_to_text(
            "Test Assessment",
            "TEST_DECISION",
            "Test explanation",
            ["Step 1", "Step 2"]
        )
        assert "DecisionGuide" in data
        assert "TEST_DECISION" in data
    
    def test_export_to_csv(self):
        """Test CSV export."""
        data = export_to_csv(
            "Test Assessment",
            "TEST_DECISION",
            "Test explanation",
            ["Step 1", "Step 2"]
        )
        assert "DecisionGuide" in data
        assert "TEST_DECISION" in data
        assert "Step 1" in data
    
    def test_export_to_csv_with_risk_score(self):
        """Test CSV export with risk score."""
        risk_score = {"score": 75, "level": "HIGH RISK"}
        data = export_to_csv(
            "Test Assessment",
            "TEST_DECISION",
            "Test explanation",
            ["Step 1"],
            risk_score=risk_score
        )
        assert "75" in data
        assert "HIGH RISK" in data
    
    def test_export_history_to_csv(self):
        """Test history CSV export."""
        history = [
            {
                "timestamp": "2024-01-01T00:00:00",
                "tree_id": "test",
                "tree_title": "Test",
                "decision": "DECISION",
                "explanation": "Explanation",
                "path": ["Step 1"],
                "answers": {"q1": "Yes"}
            }
        ]
        data = export_history_to_csv(history)
        assert "test" in data
        assert "DECISION" in data
    
    def test_get_filename(self):
        """Test filename generation."""
        filename = get_filename("Test Assessment", "pdf")
        assert filename.startswith("DecisionGuide_")
        assert filename.endswith(".pdf")
        assert "Test_Assessment" in filename

