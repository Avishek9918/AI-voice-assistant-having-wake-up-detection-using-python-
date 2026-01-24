"""
Configuration loader utility
"""

import sys
from config import Config

def load_config():
    """
    Load configuration from config.py
    
    Returns:
        Config: Configuration object
    """
    try:
        return Config()
    except Exception as e:
        print(f"Error loading configuration: {e}")
        sys.exit(1)