# GeeksforGeeks Scraper - Clean Architecture

This document explains the new clean architecture implemented for the GeeksforGeeks Problem Scraper.

## Problem with Original Architecture

The original `app.py` file was doing too much:
- **Mixed UI and Business Logic**: Streamlit-specific UI code was mixed with business logic
- **Hard to Test**: Business logic was tightly coupled to UI framework
- **Not Reusable**: Couldn't easily switch to different UI frameworks
- **Poor Separation of Concerns**: Single file handling data processing, API calls, UI rendering, and session management

## New Architecture

### 1. Models Layer (`src/models/`)
**Pure data structures with no external dependencies**

- `problem.py` - Problem and Comment data models
- `ai_solution.py` - AI solution data model

**Benefits:**
- Framework-agnostic data representation
- Built-in validation and convenience methods
- Easy to test and serialize

### 2. Services Layer (`src/services/`)
**Business logic separated from UI concerns**

- `problem_service.py` - Problem fetching and validation logic
- `ai_service.py` - AI solution generation logic  
- `session_service.py` - Abstract session management with framework-specific implementations

**Benefits:**
- Reusable across different UI frameworks
- Easy to unit test
- Clear separation of concerns
- Framework-agnostic business logic

### 3. UI Layer (`src/ui/`)
**Framework-specific presentation logic only**

- `streamlit_app.py` - Main Streamlit application
- `flask_app.py` - Example Flask implementation
- `components/` - Reusable UI components
- `formatters/` - UI-specific text formatting

**Benefits:**
- Pure presentation logic
- Components can be reused
- Easy to switch UI frameworks
- No business logic in UI code

### 4. Configuration (`src/config/`)
**Centralized configuration management**

- `settings.py` - Application settings and environment variables

## Key Improvements

### Framework Independence
```python
# Business logic (same for all UI frameworks)
from src.services.problem_service import ProblemService
from src.services.ai_service import AIService

problem_service = ProblemService()
ai_service = AIService()

# UI-specific session management
streamlit_session = StreamlitSessionService(st.session_state)
flask_session = FlaskSessionService()
```

### Easy Testing
```python
# Can test business logic without UI
def test_problem_service():
    service = ProblemService()
    assert service.validate_url("https://www.geeksforgeeks.org/problems/test/1")
```

### Reusable Components
```python
# Same business logic, different UI
# Streamlit
problem = problem_service.fetch_problem(url)
ProblemDisplayComponent.display_problem_section(problem)

# Flask
problem = problem_service.fetch_problem(url)
return render_template('problem.html', problem=problem)
```

## Usage Examples

### Adding a New UI Framework

To add support for a new UI framework (e.g., FastAPI + React):

1. **Create session service implementation:**
```python
class FastAPISessionService(SessionService):
    def __init__(self, request):
        self.request = request
    
    def store_problem(self, problem: Problem) -> None:
        # Store in database or cache
        pass
```

2. **Create API endpoints:**
```python
@app.post("/api/scrape")
async def scrape_problem(request: ScrapeRequest):
    problem = problem_service.fetch_problem(request.url)
    session_service.store_problem(problem)
    return {"problem": problem.to_dict()}
```

3. **Use same business logic:**
```python
# Same services, different UI
problem_service = ProblemService()
ai_service = AIService()
```

### Running Different UIs

**Streamlit UI (original):**
```bash
streamlit run app.py
```

**Flask UI (example):**
```bash
python src/ui/flask_app.py
```

Both use the exact same business logic!

## File Structure
```
src/
├── models/           # Data models
│   ├── problem.py
│   └── ai_solution.py
├── services/         # Business logic
│   ├── problem_service.py
│   ├── ai_service.py
│   └── session_service.py
├── ui/              # UI implementations
│   ├── streamlit_app.py
│   ├── flask_app.py
│   └── components/
├── config/          # Configuration
│   └── settings.py
└── ...              # Existing scraping logic
```

## Benefits Summary

1. **Maintainability**: Clear separation makes code easier to understand and modify
2. **Testability**: Business logic can be tested independently of UI
3. **Reusability**: Same business logic works with any UI framework
4. **Scalability**: Easy to add new features without affecting existing code
5. **Flexibility**: Can easily switch or support multiple UI frameworks

This architecture follows the **Single Responsibility Principle** and **Dependency Inversion Principle**, making the codebase much more robust and maintainable.
