"""
GeeksforGeeks Problem & Comments Scraper - Main Entry Point

A Streamlit application to scrape and display GeeksforGeeks coding problems.
This file now serves as a simple entry point that delegates to the new architecture.
"""

from dotenv import load_dotenv
from src.ui.streamlit_app import main

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":
    main()
