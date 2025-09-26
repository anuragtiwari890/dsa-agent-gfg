"""
Base scraper classes and interfaces for coding platforms.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class for coding platform scrapers.
    This allows easy extension to other platforms like LeetCode, HackerRank, etc.
    """
    
    def __init__(self, platform_name: str):
        """
        Initialize the scraper.
        
        Args:
            platform_name: Name of the coding platform
        """
        self.platform_name = platform_name
        self.logger = logging.getLogger(f"{__name__}.{platform_name}")
    
    @abstractmethod
    def validate_url(self, url: str) -> bool:
        """
        Validate if the URL is a valid problem URL for this platform.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        pass
    
    @abstractmethod
    def scrape_problem(self, url: str) -> Dict[str, Any]:
        """
        Scrape problem data from the given URL.
        
        Args:
            url: Problem URL to scrape
            
        Returns:
            Dictionary containing problem data
        """
        pass
    
    @abstractmethod
    def fetch_comments(self, problem_id: str, max_comments: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch comments for a problem.
        
        Args:
            problem_id: ID of the problem
            max_comments: Maximum number of comments to fetch
            
        Returns:
            List of comment dictionaries
        """
        pass
    
    def get_platform_name(self) -> str:
        """Get the name of the platform."""
        return self.platform_name


class GeeksforGeeksScraper(BaseScraper):
    """
    GeeksforGeeks specific scraper implementation.
    This wraps the existing functions in a class structure for consistency.
    """
    
    def __init__(self):
        super().__init__("GeeksforGeeks")
    
    def validate_url(self, url: str) -> bool:
        """Validate GeeksforGeeks problem URL."""
        from .utils import validate_gfg_url
        return validate_gfg_url(url)
    
    def scrape_problem(self, url: str) -> Dict[str, Any]:
        """Scrape GeeksforGeeks problem."""
        from .geeksforgeeks import scrape_problem
        return scrape_problem(url)
    
    def fetch_comments(self, problem_id: str, max_comments: int = 5) -> List[Dict[str, Any]]:
        """Fetch GeeksforGeeks comments."""
        from .geeksforgeeks import fetch_comments
        return fetch_comments(problem_id, max_comments)


# Factory function for creating scrapers
def create_scraper(platform: str) -> Optional[BaseScraper]:
    """
    Factory function to create appropriate scraper based on platform.
    
    Args:
        platform: Name of the platform ('geeksforgeeks', 'leetcode', etc.)
        
    Returns:
        Scraper instance or None if platform not supported
    """
    scrapers = {
        'geeksforgeeks': GeeksforGeeksScraper,
        'gfg': GeeksforGeeksScraper,  # Alias
    }
    
    scraper_class = scrapers.get(platform.lower())
    if scraper_class:
        return scraper_class()
    
    logger.warning(f"Unsupported platform: {platform}")
    return None
