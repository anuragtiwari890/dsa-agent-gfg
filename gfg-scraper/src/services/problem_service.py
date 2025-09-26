"""
Service layer for problem-related business logic.
"""

import logging
from typing import Optional
from ..models.problem import Problem
from ..scraping.geeksforgeeks import scrape_problem
from ..scraping.utils import validate_gfg_url

logger = logging.getLogger(__name__)


class ProblemService:
    """Service for handling problem-related operations."""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate if URL is a valid GeeksforGeeks problem URL."""
        if not url or not url.strip():
            return False
        return validate_gfg_url(url.strip())
    
    @staticmethod
    def fetch_problem(url: str) -> Problem:
        """
        Fetch and parse a problem from GeeksforGeeks.
        
        Args:
            url: GeeksforGeeks problem URL
            
        Returns:
            Problem object with parsed data
            
        Raises:
            ValueError: If URL is invalid or problem cannot be accessed
            Exception: For other scraping errors
        """
        if not ProblemService.validate_url(url):
            raise ValueError("Invalid GeeksforGeeks problem URL")
        
        try:
            logger.info(f"Fetching problem from URL: {url}")
            problem_data = scrape_problem(url.strip())
            
            # Convert to Problem model
            problem = Problem.from_dict(problem_data)
            problem.url = url.strip()
            
            if not problem.has_content():
                raise ValueError("Problem data is empty or invalid")
            
            logger.info(f"Successfully fetched problem: {problem.title}")
            return problem
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Error fetching problem from {url}: {str(e)}")
            raise Exception(f"Failed to fetch problem: {str(e)}")
    
    @staticmethod
    def format_problem_statement(statement_html: str) -> str:
        """
        Format HTML statement for display.
        
        Args:
            statement_html: Raw HTML statement
            
        Returns:
            Formatted statement
        """
        if not statement_html:
            return ""
        
        # Convert \\n escape sequences to actual newlines for better rendering
        formatted_html = statement_html.replace('\\n', '\n')
        
        return formatted_html
