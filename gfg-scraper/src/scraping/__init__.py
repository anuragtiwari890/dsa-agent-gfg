"""
Scraping package for GeeksforGeeks and other coding platforms.
"""

from .geeksforgeeks import scrape_problem, fetch_comments
from .utils import validate_gfg_url, fetch_html_data, format_problem_statement
from .base import BaseScraper, GeeksforGeeksScraper, create_scraper

__all__ = [
    'scrape_problem', 
    'fetch_comments',
    'validate_gfg_url', 
    'fetch_html_data',
    'format_problem_statement',
    'BaseScraper',
    'GeeksforGeeksScraper', 
    'create_scraper'
]
