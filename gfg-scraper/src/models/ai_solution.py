"""
Data models for AI-generated solutions.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AISolution:
    """Represents an AI-generated solution for a problem."""
    code: str
    language: str = "python"
    explanation: Optional[str] = None
    complexity_analysis: Optional[str] = None
    
    def has_content(self) -> bool:
        """Check if solution has meaningful content."""
        return bool(self.code and self.code.strip())
    
    def get_formatted_code(self) -> str:
        """Get properly formatted code."""
        return self.code.strip() if self.code else ""
