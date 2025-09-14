"""
GeeksforGeeks Problem Scraper

This module handles the scraping logic for GeeksforGeeks coding problems.
Extracts question title, statement/explanation HTML, and first 5 comments.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
import logging
import time
import re
from urllib.parse import urljoin, urlparse
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class GeeksforGeeksScraper:
    """
    A scraper class for extracting data from GeeksforGeeks coding problems.
    
    Attributes:
        session: requests.Session object for HTTP requests
        timeout: Request timeout in seconds
        headers: HTTP headers for requests
    """
    
    def __init__(self, timeout: int = 10) -> None:
        """
        Initialize the GeeksforGeeks scraper.
        
        Args:
            timeout: Request timeout in seconds (default: 10)
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        self.session.headers.update(self.headers)
    
    def _clean_text(self, element) -> str:
        """
        Extract clean readable text from a BeautifulSoup element.
        
        Args:
            element: BeautifulSoup element or text
            
        Returns:
            str: Cleaned text with normalized whitespace
        """
        if element is None:
            return ""
        
        text = element.get_text() if hasattr(element, 'get_text') else str(element)
        # Normalize whitespace and remove extra spaces/newlines
        return re.sub(r'\s+', ' ', text.strip())
    
    def _select_first(self, soup: BeautifulSoup, selector: str):
        """
        Safely select the first element matching the CSS selector.
        
        Args:
            soup: BeautifulSoup object
            selector: CSS selector string
            
        Returns:
            BeautifulSoup element or None if not found
        """
        try:
            return soup.select_one(selector)
        except Exception as e:
            logger.debug(f"Selector '{selector}' failed: {e}")
            return None
    
    def _maybe_absolute(self, base_url: str, href: str) -> str:
        """
        Convert relative URL to absolute URL if needed.
        
        Args:
            base_url: Base URL for resolving relative URLs
            href: URL that might be relative
            
        Returns:
            str: Absolute URL
        """
        if not href:
            return href
        return urljoin(base_url, href)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetch and parse a webpage with retry logic.
        
        Args:
            url: The URL to fetch
            
        Returns:
            BeautifulSoup: Parsed HTML content
            
        Raises:
            ValueError: If HTTP status is not 200
            requests.RequestException: If the request fails after retries
        """
        logger.info(f"Fetching URL: {url}")
        response = self.session.get(url, timeout=self.timeout)
        
        if response.status_code != 200:
            raise ValueError(f"HTTP {response.status_code}: Failed to fetch {url}")
        
        return BeautifulSoup(response.content, 'lxml')
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """
        Extract the problem title from the page.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Optional[str]: The problem title or None if not found
        """
        # Primary selector
        title_elem = self._select_first(soup, '.problems_header_content__o_4YA .problems_header_content__title__L2cB2.g-mb-0 h3.g-m-0')
        if title_elem:
            return self._clean_text(title_elem)
        
        # Fallback: any h1, h2, h3 inside problems_header_content
        header_containers = soup.find_all(class_=re.compile(r'problems_header_content', re.I))
        for container in header_containers:
            for tag in ['h1', 'h2', 'h3']:
                title_elem = container.find(tag)
                if title_elem:
                    return self._clean_text(title_elem)
        
        # Ultimate fallback: og:title meta tag
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return self._clean_text(og_title['content'])
        
        return None
    
    def _extract_problem_statement(self, soup: BeautifulSoup) -> tuple[Optional[str], Optional[str]]:
        """
        Extract the problem statement/explanation HTML and text.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            tuple: (statement_html, statement_text) or (None, None) if not found
        """
        # Primary selector
        statement_elem = self._select_first(soup, '.problems_problem_content__Xm_eO')
        if statement_elem:
            return str(statement_elem), self._clean_text(statement_elem)
        
        # Fallback: any element with class containing "problem_content"
        problem_content_elems = soup.find_all(class_=re.compile(r'problem_content', re.I))
        if problem_content_elems:
            elem = problem_content_elems[0]
            return str(elem), self._clean_text(elem)
        
        # Heuristic fallback: largest div containing keywords
        keywords = ['Example', 'Input', 'Output', 'Explanation', 'Constraints']
        candidate_divs = []
        
        for div in soup.find_all('div'):
            text = self._clean_text(div)
            if any(keyword in text for keyword in keywords):
                candidate_divs.append((len(text), div))
        
        if candidate_divs:
            # Return the largest div containing keywords
            largest_div = max(candidate_divs, key=lambda x: x[0])[1]
            return str(largest_div), self._clean_text(largest_div)
        
        return None, None
    
    def _extract_comments(self, soup: BeautifulSoup, base_url: str, limit: int = 5) -> List[str]:
        """
        Extract the first N comments from the Comments section.
        
        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative URLs
            limit: Maximum number of comments to extract (default: 5)
            
        Returns:
            List[str]: List of comment text strings (up to limit)
        """
        comments = []
        
        # Strategy 1: Try to find comments on the same page
        bottom_content = self._select_first(soup, '.bottom_container .bottom_contents')
        if bottom_content:
            comment_elements = bottom_content.select('.single_comment .items .right .text')
            for elem in comment_elements[:limit]:
                comment_text = self._clean_text(elem)
                if comment_text:
                    comments.append(comment_text)
        
        # Strategy 2: If no comments found, look for Comments tab/link
        if not comments:
            # Look for comments link in menu
            menu_bar = self._select_first(soup, '.problems_header_menu__aKU8f')
            if menu_bar:
                comments_link = None
                for link in menu_bar.find_all('a'):
                    link_text = self._clean_text(link)
                    if 'comments' in link_text.lower():
                        href = link.get('href')
                        if href:
                            comments_link = self._maybe_absolute(base_url, href)
                            break
                
                # Fetch comments page if link found
                if comments_link:
                    try:
                        comments_soup = self._fetch_page(comments_link)
                        bottom_content = self._select_first(comments_soup, '.bottom_container .bottom_contents')
                        if bottom_content:
                            comment_elements = bottom_content.select('.single_comment .items .right .text')
                            for elem in comment_elements[:limit]:
                                comment_text = self._clean_text(elem)
                                if comment_text:
                                    comments.append(comment_text)
                    except Exception as e:
                        logger.debug(f"Failed to fetch comments from {comments_link}: {e}")
        
        # Strategy 3: Last resort - look for any single_comment divs
        if not comments:
            single_comments = soup.find_all(class_=re.compile(r'single_comment', re.I))
            for comment_div in single_comments[:limit]:
                # Try to find text within the comment structure
                text_elem = comment_div.select_one('.items .right .text')
                if not text_elem:
                    # Fallback: just get the text from the comment div
                    text_elem = comment_div
                
                comment_text = self._clean_text(text_elem)
                if comment_text:
                    comments.append(comment_text)
        
        return comments[:limit]
    
    def fetch_problem_and_comments(self, url: str) -> Dict[str, Any]:
        """
        Scrape a GeeksforGeeks problem page for title, statement, and comments.
        
        Args:
            url: The GeeksforGeeks problem URL to scrape
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - url: Original URL
                - title: Problem title (str or None)
                - statement_html: Problem statement HTML (str or None)
                - statement_text: Problem statement text (str or None)
                - comments: List of up to 5 comment strings
                
        Raises:
            ValueError: If HTTP status is not 200
            requests.RequestException: If scraping fails after retries
        """
        logger.info(f"Scraping GeeksforGeeks problem: {url}")
        
        # Fetch the main page
        soup = self._fetch_page(url)
        
        # Extract title
        title = self._extract_title(soup)
        logger.debug(f"Extracted title: {title}")
        
        # Extract problem statement (HTML and text)
        statement_html, statement_text = self._extract_problem_statement(soup)
        logger.debug(f"Extracted statement: {'Found' if statement_html else 'Not found'}")
        
        # Extract comments
        comments = self._extract_comments(soup, url, limit=5)
        logger.debug(f"Extracted {len(comments)} comments")
        
        result = {
            "url": url,
            "title": title,
            "statement_html": statement_html,
            "statement_text": statement_text,
            "comments": comments
        }
        
        return result
    
    def validate_url(self, url: str) -> bool:
        """
        Validate if the URL is a valid GeeksforGeeks problem URL.
        
        Args:
            url: The URL to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not url or not isinstance(url, str):
            return False
        
        try:
            parsed = urlparse(url)
            
            # Check domain
            if parsed.netloc.lower() not in ['www.geeksforgeeks.org', 'geeksforgeeks.org']:
                return False
            
            # Check path structure - should contain "/problems/"
            if '/problems/' not in parsed.path:
                return False
            
            return True
            
        except Exception:
            return False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup resources."""
        if hasattr(self, 'session'):
            self.session.close()
