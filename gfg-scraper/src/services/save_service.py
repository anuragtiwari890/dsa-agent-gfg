"""
Service for preparing AI solutions for download.
"""

import re
from typing import Tuple
from ..models.problem import Problem
from ..models.ai_solution import AISolution


class SaveService:
    """Service for preparing AI solutions for download."""
    
    def sanitize_filename(self, title: str) -> str:
        """
        Convert problem title to a valid filename.
        
        Args:
            title: Problem title
            
        Returns:
            Sanitized filename with .py extension
        """
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
        
        # Replace spaces with underscores
        sanitized = re.sub(r'\s+', '_', sanitized.strip())
        
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = "untitled_problem"
        
        # Add .py extension
        return f"{sanitized}.py"
    
    def create_file_content(self, problem: Problem, solution: AISolution) -> str:
        """
        Create the content for the downloaded file.
        
        Args:
            problem: Problem data
            solution: AI solution data
            
        Returns:
            Complete file content
        """
        content_parts = []
        
        # Add header comment with problem info
        content_parts.append('"""')
        content_parts.append(f"Problem: {problem.title}")
        if problem.url:
            content_parts.append(f"Source: {problem.url}")
        content_parts.append("")
        
        # Add problem statement
        if problem.statement_text:
            content_parts.append("Problem Statement:")
            # Split long lines and add proper formatting
            statement_lines = problem.statement_text.strip().split('\n')
            for line in statement_lines:
                content_parts.append(line.strip())
        
        content_parts.append('"""')
        content_parts.append("")
        
        # Add the solution code
        if solution.code:
            content_parts.append(solution.code.strip())
        
        return '\n'.join(content_parts)
    
    def prepare_download(self, problem: Problem, solution: AISolution) -> Tuple[str, str]:
        """
        Prepare file content and filename for download.
        
        Args:
            problem: Problem data
            solution: AI solution data
            
        Returns:
            Tuple of (filename, file_content)
        """
        filename = self.sanitize_filename(problem.title)
        content = self.create_file_content(problem, solution)
        return filename, content