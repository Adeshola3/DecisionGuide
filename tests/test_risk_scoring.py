"""
Tests for risk scoring functionality.
"""
import pytest
from risk_scoring import RiskScorer


class TestRiskScoring:
    """Test risk scoring functions."""
    
    @pytest.fixture
    def sample_tree(self):
        """Create a sample tree with scoring."""
        return {
            "id": "test_tree",
            "scoring": {
                "thresholds": {
                    "low": 0,
                    "medium": 30,
                    "high": 60,
                    "critical": 85
                }
            },
            "nodes": {
                "q1": {
                    "type": "choice",
                    "text": "Test question?",
                    "options": {
                        "High risk": {
                            "risk_weight": 50,
                            "next": "q2"
                        },
                        "Low risk": {
                            "risk_weight": 10,
                            "next": "q2"
                        }
                    }
                },
                "q2": {
                    "type": "choice",
                    "text": "Another question?",
                    "options": {
                        "Yes": {
                            "risk_weight": 30,
                            "decision": "DECISION"
                        }
                    }
                }
            }
        }
    
    def test_calculate_score(self, sample_tree):
        """Test score calculation."""
        scorer = RiskScorer(sample_tree)
        answers = [
            {"node_id": "q1", "choice": "High risk"},
            {"node_id": "q2", "choice": "Yes"}
        ]
        score = scorer.calculate_score(answers)
        assert score == 80  # 50 + 30
    
    def test_get_risk_level_low(self, sample_tree):
        """Test risk level determination for low risk."""
        scorer = RiskScorer(sample_tree)
        level, icon, color = scorer.get_risk_level(20)
        assert level == "LOW RISK"
        assert icon == "🟢"
        assert color == "green"
    
    def test_get_risk_level_critical(self, sample_tree):
        """Test risk level determination for critical risk."""
        scorer = RiskScorer(sample_tree)
        level, icon, color = scorer.get_risk_level(90)
        assert level == "CRITICAL"
        assert icon == "🔴"
        assert color == "red"

