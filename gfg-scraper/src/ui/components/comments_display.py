"""
Comments display component for Streamlit UI.
"""

import streamlit as st
from typing import List
from ...models.problem import Problem, Comment
from ..formatters.text_formatters import TextFormatter


class CommentsDisplayComponent:
    """Component for displaying comments in Streamlit."""
    
    @staticmethod
    def display_comment(comment: Comment, comment_number: int) -> None:
        """Display a single comment."""
        header = TextFormatter.format_comment_header(
            comment_number=comment_number,
            user_name=comment.user_name,
            created_at=comment.created_at,
            votes=comment.votes
        )
        
        with st.expander(header, expanded=False):
            if comment.text:
                st.markdown(comment.text, unsafe_allow_html=True)
            else:
                st.info("No comment text available")
    
    @staticmethod
    def display_comments_section(problem: Problem, limit: int = 5) -> None:
        """Display the complete comments section."""
        st.header("💬 Comments (Top 5)")
        
        comments = problem.get_top_comments(limit)
        
        if comments:
            for i, comment in enumerate(comments, 1):
                CommentsDisplayComponent.display_comment(comment, i)
                
                # Add separator between comments (except for the last one)
                if i < len(comments):
                    st.markdown("---")
        else:
            st.info("No comments found")
        
        st.markdown("---")
