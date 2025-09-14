"""
GeeksforGeeks Problem & Comments Scraper - Streamlit App

A Streamlit application to scrape and display GeeksforGeeks coding problems.
Extracts question title, statement, and first 5 comments from the Comments section.
"""

import streamlit as st
from typing import Dict, Any
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from scraper.geeksforgeeks import GeeksforGeeksScraper


def validate_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid GeeksforGeeks problem URL.
    
    Args:
        url: The URL string to validate
        
    Returns:
        bool: True if valid GeeksforGeeks problem URL, False otherwise
    """
    if not url or not url.strip():
        return False
    
    scraper = GeeksforGeeksScraper()
    return scraper.validate_url(url.strip())


def display_problem_sections(problem_data: Dict[str, Any]) -> None:
    """
    Display the scraped problem data in three main sections.
    
    Args:
        problem_data: Dictionary containing title, statement, and comments
    """
    # Section 1: Question
    st.header("📝 Question")
    
    # Display title (large)
    if problem_data.get('title'):
        st.markdown(f"## {problem_data['title']}")
    else:
        st.warning("⚠️ Problem title not found")
    
    # Display formatted statement
    if problem_data.get('statement_html'):
        st.markdown(problem_data['statement_html'], unsafe_allow_html=True)
    elif problem_data.get('statement_text'):
        st.write(problem_data['statement_text'])
    else:
        st.warning("⚠️ Problem statement not found")
    
    st.markdown("---")
    
    # Section 2: Comments (Top 5)
    st.header("💬 Comments (Top 5)")
    
    comments = problem_data.get('comments', [])
    if comments:
        # Show comments as bullet list using st.markdown
        comment_list = "\n".join([f"• {comment}" for comment in comments])
        st.markdown(comment_list)
    else:
        st.info("No comments found")
    
    st.markdown("---")
    
    # Section 3: Raw Debug (expandable)
    with st.expander("🔍 Raw Debug"):
        st.json(problem_data)


def create_sidebar():
    """Create sidebar with selector information."""
    st.sidebar.header("🔍 Selector Information")
    
    st.sidebar.subheader("Title Selector")
    st.sidebar.code(
        ".problems_header_content__o_4YA .problems_header_content__title__L2cB2.g-mb-0 h3.g-m-0",
        language="css"
    )
    
    st.sidebar.subheader("Statement Container")
    st.sidebar.code(
        ".problems_problem_content__Xm_eO",
        language="css"
    )
    
    st.sidebar.subheader("Comments Area")
    st.sidebar.code(
        ".bottom_container .bottom_contents",
        language="css"
    )
    st.sidebar.code(
        ".single_comment .items .right .text",
        language="css"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 These are the primary CSS selectors used. The scraper includes fallback strategies for robustness.")


def main() -> None:
    """Main Streamlit application function."""
    st.set_page_config(
        page_title="GeeksforGeeks Problem & Comments Scraper",
        page_icon="🔍",
        layout="wide"
    )
    
    # Create sidebar
    create_sidebar()
    
    # Main title
    st.title("GeeksforGeeks Problem & Comments Scraper")
    
    # URL input
    url_input = st.text_input(
        "GeeksforGeeks Problem URL:",
        placeholder="https://www.geeksforgeeks.org/problems/subarray-with-given-sum-1587115621/1",
        help="Enter a valid GeeksforGeeks problem URL"
    )
    
    # Submit button
    submit_button = st.button("🚀 Submit", type="primary")
    
    # Handle form submission
    if submit_button:
        if not url_input or not url_input.strip():
            st.warning("⚠️ Please enter a URL")
            return
        
        if not validate_url(url_input):
            st.warning("⚠️ Please enter a valid GeeksforGeeks problem URL")
            return
        
        with st.spinner("Scraping problem data..."):
            try:
                with GeeksforGeeksScraper() as scraper:
                    problem_data = scraper.fetch_problem_and_comments(url_input.strip())
                    display_problem_sections(problem_data)
                    
            except ValueError as e:
                st.error(f"❌ Error accessing the page: {str(e)}")
                logger.error(f"HTTP error scraping URL {url_input}: {str(e)}")
                
            except Exception as e:
                st.error(f"❌ Error scraping the problem: {str(e)}")
                logger.error(f"Unexpected error scraping URL {url_input}: {str(e)}")
    
    # Code editor placeholder
    st.markdown("---")
    st.header("💻 Your Solution (optional)")
    
    solution_code = st.text_area(
        "Code Editor",
        placeholder="# Write your solution here...",
        height=200,
        help="This is a simple text area for writing your solution. Code is not executed."
    )
    
    # Footer
    st.markdown("---")
    st.caption("For educational use; site structure may change.")


if __name__ == "__main__":
    main()
