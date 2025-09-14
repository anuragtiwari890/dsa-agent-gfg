# GeeksforGeeks Problem Scraper

A simple Python + Streamlit application to scrape and display GeeksforGeeks coding problems. Extracts question titles, problem statements, and the first 5 comments from the Comments section.

## Features

- 🔍 Scrape GeeksforGeeks coding problems by URL
- 📝 Extract question title and problem statement (HTML)
- 💬 Get the first 5 comments from the Comments section
- 🌐 Web-based interface using Streamlit
- 🛡️ Robust error handling and retry logic
- 📱 Responsive and user-friendly UI

## Tech Stack

- **Python 3.10+**
- **Streamlit** - Web interface
- **requests** - HTTP client
- **BeautifulSoup4 + lxml** - HTML parsing
- **tenacity** - Retry logic
- **html5lib** - Additional HTML parsing support

## Quick Start

### 1. Clone and Setup Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

## Usage

1. **Enter URL**: Paste a GeeksforGeeks problem URL in the input field
2. **Scrape**: Click the "🚀 Scrape Problem" button
3. **View Results**: The app will display:
   - Question title
   - Problem statement (formatted HTML)
   - First 5 comments from the Comments section

### Sample URLs

The `sample_urls.txt` file contains tested GeeksforGeeks problem URLs you can use:

- Subarray with Given Sum
- Kadane's Algorithm
- Missing Number in Array

## Project Structure

```
gfg-scraper/
├── app.py                    # Main Streamlit application
├── scraper/
│   ├── __init__.py          # Package initialization
│   └── geeksforgeeks.py     # Core scraping logic
├── tests/
│   └── test_geeksforgeeks.py # Unit tests
├── sample_urls.txt          # Sample problem URLs
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Development

### Running Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=scraper
```

### Code Style

- Type hints are used throughout the codebase
- Error handling with appropriate timeouts
- Robust selectors with fallback strategies
- Comprehensive logging for debugging

## Notes

- This tool is for educational purposes only
- Please respect GeeksforGeeks' terms of service
- The scraper includes rate limiting and polite crawling practices
- Fallback strategies are implemented for different HTML structures

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is for educational use only. Please respect the terms of service of GeeksforGeeks.
