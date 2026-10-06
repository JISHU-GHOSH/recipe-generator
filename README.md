# AI Recipe Generator (Groq API)

A simple AI-powered recipe generator assignment project built with Python and Groq.

## Files
- `recipe.py` - Command-line script to generate recipes directly in your terminal.
- `server.py` - Web application (FastAPI) providing an interactive UI in your browser.
- `.env` - Contains your `GROQ_API_KEY` (kept secret and git-ignored).

## How to Run

### 1. Terminal / CLI Mode
Pass a dish name as an argument:
```bash
python recipe.py "Butter Chicken"
```
Or run interactively:
```bash
python recipe.py
```

### 2. Web UI Mode
Start the web app:
```bash
python server.py
```
Then open your browser and navigate to:
**http://127.0.0.1:8000**
