# GeeksforGeeks Problem Scraper

A simple Python + Streamlit application to scrape and display GeeksforGeeks coding problems. Extracts question titles, problem statements, and the first 5 comments from the Comments section.

## Features

- 🔍 Scrape GeeksforGeeks coding problems by URL
- 📝 Extract question title and problem statement (HTML)
- 💬 Get the first 5 comments from the Comments section
- 🤖 AI-powered solution generation using OpenAI GPT
- 🌐 Web-based interface using Streamlit
- 🔑 Environment variable support for API keys (.env file)
- 🛡️ Robust error handling and retry logic
- 📱 Responsive and user-friendly UI

## Tech Stack

- **Python 3.10+**
- **Streamlit** - Web interface
- **requests** - HTTP client
- **BeautifulSoup4 + lxml** - HTML parsing
- **OpenAI** - AI solution generation
- **LangChain** - LLM orchestration
- **python-dotenv** - Environment variable loading

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

### 3. Setup Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

**Get your OpenAI API key from**: https://platform.openai.com/api-keys

### 4. Run the Application

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
4. **Generate AI Solution**: Click "🚀 Generate AI Solution" to get an AI-powered Python solution
   - If you've set up the `.env` file, the API key will be loaded automatically
   - Otherwise, you can enter your OpenAI API key manually

### Sample URLs

The `sample_urls.txt` file contains tested GeeksforGeeks problem URLs you can use:

- Subarray with Given Sum
- Kadane's Algorithm
- Missing Number in Array

## Project Structure

```
gfg-scraper/
├── app.py                    # Main Streamlit application
├── src/
│   ├── __init__.py          # Package initialization
│   ├── geeksforgeeks.py     # Core scraping logic
│   ├── ai_solution_generator.py # AI solution generation
│   └── utils.py             # Utility functions
├── tests/
│   └── test_geeksforgeeks.py # Unit tests
├── .env.example             # Example environment file
├── .gitignore              # Git ignore rules
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
