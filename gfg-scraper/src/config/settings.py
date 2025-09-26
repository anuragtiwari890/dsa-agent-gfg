"""
Configuration settings for the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application configuration settings."""
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Application Configuration
    DEFAULT_COMMENTS_LIMIT: int = 5
    
    # UI Configuration
    PAGE_TITLE: str = "GeeksforGeeks Problem & Comments Scraper"
    PAGE_ICON: str = "🔍"
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def has_openai_key(cls) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(cls.OPENAI_API_KEY and cls.OPENAI_API_KEY != 'your_openai_api_key_here')


# Global settings instance
settings = Settings()
