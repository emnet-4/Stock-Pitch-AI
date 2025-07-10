"""
Configuration management for Stock Pitch AI
Handles environment variables, API keys, and application settings.
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()

class Config(BaseSettings):
    """Configuration class for Stock Pitch AI."""
    
    # API Keys
    openai_api_key: Optional[str] = Field(None, description="OpenAI API key")
    alpha_vantage_api_key: Optional[str] = Field(None, description="Alpha Vantage API key")
    
    # Application settings
    app_name: str = "Stock Pitch AI"
    app_version: str = "1.0.0"
    debug: bool = Field(False, description="Enable debug mode")
    
    # Data settings
    default_analysis_period: str = "1y"
    cache_enabled: bool = Field(True, description="Enable caching")
    cache_duration_minutes: int = Field(60, description="Cache duration in minutes")
    
    # AI settings
    default_ai_model: str = "gpt-4"
    max_tokens: int = 2000
    temperature: float = 0.7
    
    # Output settings
    output_directory: str = "./output"
    presentation_format: str = "pptx"
    
    # Logging settings
    log_level: str = Field("INFO", description="Log level")
    log_file: str = "stock_pitch_ai.log"
    
    def __init__(self, api_key: Optional[str] = None, **kwargs):
        """Initialize configuration with optional API key override."""
        if api_key:
            kwargs['openai_api_key'] = api_key
        super().__init__(**kwargs)
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

# Global configuration instance can be created with API key when needed
# config = Config(openai_api_key="your_api_key_here")
