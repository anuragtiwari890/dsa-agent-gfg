"""
Streamlit UI implementation for GeeksforGeeks Problem Scraper.
This file contains only UI-specific logic and delegates business logic to services.
"""

import streamlit as st
import logging
from typing import Optional

# Business logic imports
from ..services.problem_service import ProblemService
from ..services.ai_service import AIService
from ..services.session_service import StreamlitSessionService
from ..models.problem import Problem
from ..models.ai_solution import AISolution

# UI component imports
from .components.problem_display import ProblemDisplayComponent
from .components.comments_display import CommentsDisplayComponent
from .components.ai_solution_display import AISolutionDisplayComponent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StreamlitApp:
    """Main Streamlit application class."""
    
    def __init__(self):
        """Initialize the Streamlit app with required services."""
        self.session_service = StreamlitSessionService(st.session_state)
        self.problem_service = ProblemService()
        self.ai_service = AIService()
    
    def setup_page_config(self) -> None:
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="GeeksforGeeks Problem & Comments Scraper",
            page_icon="🔍",
            layout="centered"
        )
    
    def render_header(self) -> None:
        """Render the main page header."""
        st.title("GeeksforGeeks Problem & Comments Scraper")
    
    def render_url_input(self) -> str:
        """
        Render URL input field.
        
        Returns:
            User-entered URL
        """
        return st.text_input(
            "GeeksforGeeks Problem URL:",
            placeholder="https://www.geeksforgeeks.org/problems/subarray-with-given-sum-1587115621/1",
            help="Enter a valid GeeksforGeeks problem URL"
        )
    
    def render_action_buttons(self) -> tuple[bool, bool]:
        """
        Render main action buttons.
        
        Returns:
            Tuple of (scrape_button_clicked, clear_button_clicked)
        """
        col1, col2 = st.columns([2, 1])
        
        with col1:
            scrape_clicked = st.button("🚀 Scrape Problem", type="primary")
        
        with col2:
            clear_clicked = False
            # Only show clear button if there's data
            current_problem = self.session_service.get_problem()
            if current_problem:
                clear_clicked = st.button("🗑️ Clear Results", type="secondary")
        
        return scrape_clicked, clear_clicked
    
    def handle_scrape_action(self, url: str) -> None:
        """
        Handle the scrape problem action.
        
        Args:
            url: URL to scrape
        """
        if not url or not url.strip():
            st.warning("⚠️ Please enter a URL")
            return
        
        if not self.problem_service.validate_url(url):
            st.warning("⚠️ Please enter a valid GeeksforGeeks problem URL")
            return
        
        with st.spinner("Scraping problem data..."):
            try:
                problem = self.problem_service.fetch_problem(url)
                
                # Store in session
                self.session_service.store_problem(problem)
                self.session_service.store_current_url(url.strip())
                
                # Clear any existing AI solution when loading new problem
                self.session_service.clear_ai_solution()
                
                st.success("✅ Problem scraped successfully!")
                
            except ValueError as e:
                st.error(f"❌ Error accessing the page: {str(e)}")
                logger.error(f"Validation error scraping URL {url}: {str(e)}")
                
            except Exception as e:
                st.error(f"❌ Error scraping the problem: {str(e)}")
                logger.error(f"Unexpected error scraping URL {url}: {str(e)}")
    
    def handle_clear_action(self) -> None:
        """Handle the clear results action."""
        self.session_service.clear_all()
        st.rerun()
    
    def handle_ai_solution_generated(self, solution: AISolution) -> None:
        """
        Handle when an AI solution is generated.
        
        Args:
            solution: Generated AI solution
        """
        self.session_service.store_ai_solution(solution)
        st.rerun()
    
    def handle_clear_ai_solution(self) -> None:
        """Handle clearing the AI solution."""
        self.session_service.clear_ai_solution()
        st.rerun()
    
    def render_current_url_info(self) -> None:
        """Render information about currently loaded URL."""
        current_url = self.session_service.get_current_url()
        if current_url:
            st.success(f"📄 Currently showing: {current_url}")
    
    def render_problem_sections(self, problem: Problem) -> None:
        """
        Render all problem-related sections.
        
        Args:
            problem: Problem to display
        """
        # Problem section
        ProblemDisplayComponent.display_problem_section(problem)
        
        # Comments section
        CommentsDisplayComponent.display_comments_section(problem)
        
        # AI Solution section
        current_solution = self.session_service.get_ai_solution()
        AISolutionDisplayComponent.display_ai_section(
            problem=problem,
            ai_service=self.ai_service,
            current_solution=current_solution,
            on_solution_generated=self.handle_ai_solution_generated,
            on_clear_solution=self.handle_clear_ai_solution
        )
    
    def render_debug_section(self, problem: Problem) -> None:
        """
        Render debug section with raw data.
        
        Args:
            problem: Problem to show debug info for
        """
        with st.expander("🔍 Raw Debug"):
            st.json(problem.to_dict())
    
    def render_footer(self) -> None:
        """Render page footer."""
        st.markdown("---")
        st.caption("For educational use; site structure may change.")
    
    def run(self) -> None:
        """Main application entry point."""
        # Setup
        self.setup_page_config()
        
        # Header
        self.render_header()
        
        # URL input
        url_input = self.render_url_input()
        
        # Action buttons
        scrape_clicked, clear_clicked = self.render_action_buttons()
        
        # Handle actions
        if scrape_clicked:
            self.handle_scrape_action(url_input)
        
        if clear_clicked:
            self.handle_clear_action()
        
        # Display content if available
        current_problem = self.session_service.get_problem()
        if current_problem:
            self.render_current_url_info()
            self.render_problem_sections(current_problem)
            self.render_debug_section(current_problem)
        
        # Footer
        self.render_footer()


def main() -> None:
    """Main entry point for the Streamlit application."""
    app = StreamlitApp()
    app.run()


if __name__ == "__main__":
    main()
