"""
Text formatting utilities for UI display.
Framework-agnostic text processing.
"""

from typing import Optional


class TextFormatter:
    """Utility class for text formatting operations."""
    
    @staticmethod
    def format_problem_statement(statement_html: str) -> str:
        """
        Format HTML statement for display.
        
        Args:
            statement_html: Raw HTML statement
            
        Returns:
            Formatted statement ready for display
        """
        if not statement_html:
            return ""
        
        # Convert \\n escape sequences to actual newlines for better rendering
        formatted_html = statement_html.replace('\\n', '\n')
        
        return formatted_html
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing unwanted characters.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Replace non-breaking spaces with regular spaces
        cleaned_text = text.replace('\xa0', ' ')
        
        return cleaned_text
    
    @staticmethod
    def format_comment_header(
        comment_number: int,
        user_name: str,
        created_at: Optional[str] = None,
        votes: int = 0
    ) -> str:
        """
        Format comment header for display.
        
        Args:
            comment_number: Comment number (1-based)
            user_name: User who posted the comment
            created_at: Optional creation timestamp
            votes: Number of votes
            
        Returns:
            Formatted header string
        """
        header = f"Comment {comment_number} by {user_name or 'Anonymous'}"
        
        if created_at:
            header += f" • {created_at}"
        
        if votes != 0:
            header += f" • {votes} votes"
        
        return header
