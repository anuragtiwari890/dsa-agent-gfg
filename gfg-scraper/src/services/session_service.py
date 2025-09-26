"""
Service layer for session/state management.
Framework-agnostic session management that can be adapted to different UI frameworks.
"""

from typing import Optional, Dict, Any
from ..models.problem import Problem
from ..models.ai_solution import AISolution


class SessionService:
    """
    Framework-agnostic session service.
    Concrete implementations should inherit from this and implement storage methods.
    """
    
    def store_problem(self, problem: Problem) -> None:
        """Store problem data in session."""
        raise NotImplementedError("Subclasses must implement store_problem")
    
    def get_problem(self) -> Optional[Problem]:
        """Retrieve problem data from session."""
        raise NotImplementedError("Subclasses must implement get_problem")
    
    def store_ai_solution(self, solution: AISolution) -> None:
        """Store AI solution in session."""
        raise NotImplementedError("Subclasses must implement store_ai_solution")
    
    def get_ai_solution(self) -> Optional[AISolution]:
        """Retrieve AI solution from session."""
        raise NotImplementedError("Subclasses must implement get_ai_solution")
    
    def store_current_url(self, url: str) -> None:
        """Store current URL in session."""
        raise NotImplementedError("Subclasses must implement store_current_url")
    
    def get_current_url(self) -> Optional[str]:
        """Retrieve current URL from session."""
        raise NotImplementedError("Subclasses must implement get_current_url")
    
    def clear_all(self) -> None:
        """Clear all session data."""
        raise NotImplementedError("Subclasses must implement clear_all")
    
    def clear_ai_solution(self) -> None:
        """Clear only AI solution from session."""
        raise NotImplementedError("Subclasses must implement clear_ai_solution")


class StreamlitSessionService(SessionService):
    """Streamlit-specific implementation of SessionService."""
    
    def __init__(self, session_state):
        """
        Initialize with Streamlit session state.
        
        Args:
            session_state: Streamlit session state object
        """
        self.session_state = session_state
    
    def store_problem(self, problem: Problem) -> None:
        """Store problem data in Streamlit session state."""
        self.session_state['problem_data'] = problem.to_dict()
        self.session_state['problem_object'] = problem
    
    def get_problem(self) -> Optional[Problem]:
        """Retrieve problem data from Streamlit session state."""
        if 'problem_object' in self.session_state:
            return self.session_state['problem_object']
        
        # Fallback to dictionary format for backward compatibility
        if 'problem_data' in self.session_state:
            return Problem.from_dict(self.session_state['problem_data'])
        
        return None
    
    def store_ai_solution(self, solution: AISolution) -> None:
        """Store AI solution in Streamlit session state."""
        self.session_state['ai_solution'] = solution.get_formatted_code()
        self.session_state['ai_solution_object'] = solution
    
    def get_ai_solution(self) -> Optional[AISolution]:
        """Retrieve AI solution from Streamlit session state."""
        if 'ai_solution_object' in self.session_state:
            return self.session_state['ai_solution_object']
        
        # Fallback to string format for backward compatibility
        if 'ai_solution' in self.session_state:
            return AISolution(code=self.session_state['ai_solution'])
        
        return None
    
    def store_current_url(self, url: str) -> None:
        """Store current URL in Streamlit session state."""
        self.session_state['current_url'] = url
    
    def get_current_url(self) -> Optional[str]:
        """Retrieve current URL from Streamlit session state."""
        return self.session_state.get('current_url')
    
    def clear_all(self) -> None:
        """Clear all session data from Streamlit session state."""
        keys_to_clear = [
            'problem_data', 'problem_object', 
            'ai_solution', 'ai_solution_object', 
            'current_url'
        ]
        for key in keys_to_clear:
            if key in self.session_state:
                del self.session_state[key]
    
    def clear_ai_solution(self) -> None:
        """Clear only AI solution from Streamlit session state."""
        ai_keys = ['ai_solution', 'ai_solution_object']
        for key in ai_keys:
            if key in self.session_state:
                del self.session_state[key]
