"""
Configuration management for DecisionGuide.
"""
import os
from pathlib import Path
from typing import Dict, Any, Optional
import json


class Config:
    """Application configuration with environment variable and file support."""
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    LOGIC_DIR: Path = BASE_DIR / "logic"
    DATA_DIR: Path = BASE_DIR / "data"
    CONFIG_FILE: Path = BASE_DIR / "config.json"
    
    # App settings
    APP_TITLE: str = os.getenv("APP_TITLE", "DecisionGuide")
    APP_DESCRIPTION: str = os.getenv(
        "APP_DESCRIPTION",
        "A simple, logic-based assistant for governance and audit decisions."
    )
    
    # Feature flags
    ENABLE_HISTORY: bool = os.getenv("ENABLE_HISTORY", "true").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "false").lower() == "true"
    ENABLE_RISK_SCORING: bool = os.getenv("ENABLE_RISK_SCORING", "true").lower() == "true"
    ENABLE_BACK_NAVIGATION: bool = os.getenv("ENABLE_BACK_NAVIGATION", "true").lower() == "true"
    ENABLE_CSV_EXPORT: bool = os.getenv("ENABLE_CSV_EXPORT", "true").lower() == "true"
    
    # Performance
    CACHE_TREES: bool = os.getenv("CACHE_TREES", "true").lower() == "true"
    SESSION_TIMEOUT: int = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour
    
    # Security
    MAX_HISTORY_ENTRIES: int = int(os.getenv("MAX_HISTORY_ENTRIES", "100"))
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "false").lower() == "true"
    
    # Export settings
    DEFAULT_EXPORT_FORMAT: str = os.getenv("DEFAULT_EXPORT_FORMAT", "pdf")
    INCLUDE_RISK_SCORES: bool = os.getenv("INCLUDE_RISK_SCORES", "true").lower() == "true"
    
    @classmethod
    def load_from_file(cls) -> Dict[str, Any]:
        """Load configuration from config.json file."""
        if cls.CONFIG_FILE.exists():
            try:
                with cls.CONFIG_FILE.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {}
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Ensure required directories exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGIC_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def get_user_preferences(cls) -> Dict[str, Any]:
        """Get user preferences from session or defaults."""
        # This could be extended to load from user profile
        return {
            "theme": "dark",
            "default_export": cls.DEFAULT_EXPORT_FORMAT,
            "show_progress": True,
            "enable_sounds": False
        }


# Initialize directories
Config.ensure_directories()

