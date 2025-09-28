"""
Problem display component for Streamlit UI.
"""

import streamlit as st
from ...models.problem import Problem
from ..formatters.text_formatters import TextFormatter


class ProblemDisplayComponent:
    """Component for displaying problem information in Streamlit."""
    
    @staticmethod
    def display_title(problem: Problem) -> None:
        """Display problem title."""
        if problem.title:
            st.markdown(f"## {problem.title}")
        else:
            st.warning("⚠️ Problem title not found")
    
    @staticmethod
    def display_statement(problem: Problem) -> None:
        """Display problem statement."""
        if problem.statement_text:
            formatted_text = TextFormatter.clean_text(problem.statement_text)
            st.markdown(formatted_text)
        elif problem.statement_html:
            formatted_statement = TextFormatter.format_problem_statement(problem.statement_html)
            st.markdown(formatted_statement, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Problem statement not found")
    
    @staticmethod
    def display_problem_section(problem: Problem) -> None:
        """Display the complete problem section."""
        st.header("📝 Question")
        
        ProblemDisplayComponent.display_title(problem)
        ProblemDisplayComponent.display_statement(problem)
        
        st.markdown("---")
