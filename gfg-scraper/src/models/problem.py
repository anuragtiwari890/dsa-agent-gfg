"""
Data models for GeeksforGeeks problems.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Comment:
    """Represents a comment on a GeeksforGeeks problem."""
    user_name: str = ""
    text: str = ""
    created_at: str = ""
    votes: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Comment':
        """Create Comment from dictionary data."""
        return cls(
            user_name=data.get('user_name', ''),
            text=data.get('text', ''),
            created_at=data.get('created_at', ''),
            votes=data.get('votes', 0)
        )


@dataclass
class Problem:
    """Represents a GeeksforGeeks problem with all its data."""
    title: str = ""
    statement_text: str = ""
    statement_html: str = ""
    comments: List[Comment] = field(default_factory=list)
    url: str = ""
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Problem':
        """Create Problem from scraped data dictionary."""
        comments_data = data.get('comments', [])
        comments = [Comment.from_dict(comment) for comment in comments_data]
        
        return cls(
            title=data.get('title', ''),
            statement_text=data.get('statement_text', ''),
            statement_html=data.get('statement_html', ''),
            comments=comments,
            url=data.get('url', '')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Problem to dictionary."""
        return {
            'title': self.title,
            'statement_text': self.statement_text,
            'statement_html': self.statement_html,
            'comments': [
                {
                    'user_name': comment.user_name,
                    'text': comment.text,
                    'created_at': comment.created_at,
                    'votes': comment.votes
                }
                for comment in self.comments
            ],
            'url': self.url
        }
    
    def has_content(self) -> bool:
        """Check if problem has meaningful content."""
        return bool(self.title or self.statement_text or self.statement_html)
    
    def get_statement(self) -> str:
        """Get the best available statement (text preferred over HTML)."""
        if self.statement_text:
            return self.statement_text.replace('\xa0', ' ')
        return self.statement_html
    
    def get_top_comments(self, limit: int = 5) -> List[Comment]:
        """Get top N comments."""
        return self.comments[:limit]
