"""
UI component for downloading solutions.
"""

import streamlit as st
from ...models.problem import Problem
from ...models.ai_solution import AISolution
from ...services.save_service import SaveService


class SaveSolutionComponent:
    """Component for downloading solutions."""
    
    @staticmethod
    def display_download_button(problem: Problem, solution: AISolution) -> None:
        """
        Display download solution button.
        
        Args:
            problem: Problem data
            solution: AI solution to download
        """
        # Only show download button if we have both problem and solution
        if not problem.has_content() or not solution.has_content():
            return
        
        # Prepare file for download
        save_service = SaveService()
        filename, file_content = save_service.prepare_download(problem, solution)
        
        # Download button
        st.download_button(
            label="💾 Download Solution",
            data=file_content,
            file_name=filename,
            mime="text/plain",
            type="secondary",
            help="Download the AI solution as a Python file"
        )
    
    @staticmethod 
    def display_download_info() -> None:
        """Display information about the download functionality."""
        with st.expander("ℹ️ About Download Functionality"):
            st.markdown("""
            **Download Solution** allows you to save AI-generated solutions to your computer.
            
            **Features:**
            - 📁 Browser's native download dialog
            - 🔧 Automatic filename generation from problem titles
            - 📝 Includes problem statement and source URL in downloaded files
            - 💻 Works on all platforms and browsers
            
            **File Format:**
            - Files are saved as `.py` files with problem info in comments
            - Problem title becomes filename (spaces → underscores)
            - Contains full problem statement and AI solution code
            
            **Example filename:**
            `Minimum_Number_of_Coins.py`
            """)