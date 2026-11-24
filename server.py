from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
import sys
from dotenv import load_dotenv
from groq import Groq
from markdown_it import MarkdownIt

md = MarkdownIt("commonmark").enable(["table", "strikethrough"])
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None
app = FastAPI(title="Savor - Culinary Assistant")

def render_page(dish_val: str = "", recipe_content: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Savor — Recipe Studio</title>
    <style>
        :root {{
            --bg-color: #000000;
            --surface-bg: rgba(28, 28, 30, 0.72);
            --surface-border: rgba(255, 255, 255, 0.12);
            --surface-hover: rgba(44, 44, 46, 0.85);
            --pill-bg: rgba(255, 255, 255, 0.08);
            --pill-border: rgba(255, 255, 255, 0.12);
            --text-primary: #FFFFFF;
            --text-secondary: #8E8E93;
            --text-tertiary: #636366;
            --ios-blue: #007AFF;
            --ios-accent: #FF9F0A;
            --radius-lg: 28px;
            --radius-md: 18px;
            --radius-sm: 12px;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            margin: 0;
            padding: 40px 16px 80px;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", sans-serif;
            background-color: var(--bg-color);
            background-image: 
                radial-gradient(at 10% 20%, rgba(255, 159, 10, 0.14) 0px, transparent 50%),
                radial-gradient(at 90% 10%, rgba(0, 122, 255, 0.14) 0px, transparent 50%),
                radial-gradient(at 50% 80%, rgba(175, 82, 222, 0.12) 0px, transparent 60%);
            background-attachment: fixed;
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
        }}

        .app-container {{
            width: 100%;
            max-width: 680px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        /* Header / Navigation Bar */
        .header {{
            text-align: center;
            padding: 24px 0 10px;
        }}

        .brand-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 999px;
            background: var(--pill-bg);
            border: 1px solid var(--surface-border);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 14px;
        }}

        .title {{
            font-size: 42px;
            font-weight: 700;
            letter-spacing: -0.035em;
            margin: 0 0 8px 0;
            color: var(--text-primary);
        }}

        .subtitle {{
            font-size: 16px;
            font-weight: 400;
            color: var(--text-secondary);
            margin: 0;
            line-height: 1.45;
        }}

        /* iOS Glass Search Card */
        .glass-card {{
            background: var(--surface-bg);
            backdrop-filter: blur(30px) saturate(180%);
            -webkit-backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid var(--surface-border);
            border-radius: var(--radius-lg);
            padding: 22px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
        }}

        form.search-form {{
            display: flex;
            gap: 10px;
            position: relative;
        }}

        .search-field {{
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
        }}

        .search-icon {{
            position: absolute;
            left: 18px;
            width: 18px;
            height: 18px;
            color: var(--text-secondary);
            pointer-events: none;
        }}

        .search-input {{
            width: 100%;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            padding: 15px 18px 15px 46px;
            font-size: 16px;
            font-family: inherit;
            color: var(--text-primary);
            outline: none;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .search-input::placeholder {{
            color: var(--text-tertiary);
        }}

        .search-input:focus {{
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.24);
            box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.06);
        }}

        .submit-btn {{
            background: #FFFFFF;
            color: #000000;
            border: none;
            border-radius: 18px;
            padding: 0 24px;
            font-size: 15px;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .submit-btn:hover {{
            background: #E5E5EA;
            transform: scale(0.98);
        }}

        .submit-btn:active {{
            transform: scale(0.95);
        }}

        /* Segmented / Suggestion Pills */
        .suggestions-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 14px;
            overflow-x: auto;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
            padding-bottom: 2px;
        }}

        .suggestions-row::-webkit-scrollbar {{
            display: none;
        }}

        .suggestion-chip {{
            padding: 7px 14px;
            background: var(--pill-bg);
            border: 1px solid var(--pill-border);
            border-radius: 999px;
            color: var(--text-secondary);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s ease;
            user-select: none;
        }}

        .suggestion-chip:hover {{
            background: rgba(255, 255, 255, 0.16);
            color: var(--text-primary);
            border-color: rgba(255, 255, 255, 0.24);
        }}

        .suggestion-chip:active {{
            transform: scale(0.96);
        }}

        /* Recipe Result Container */
        .recipe-wrapper {{
            background: var(--surface-bg);
            backdrop-filter: blur(30px) saturate(180%);
            -webkit-backdrop-filter: blur(30px) saturate(180%);
            border: 1px solid var(--surface-border);
            border-radius: var(--radius-lg);
            padding: 32px 36px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Recipe Typography & Markdown Styling */
        .recipe-content {{
            line-height: 1.65;
            color: #E5E5EA;
            font-size: 15px;
        }}

        .recipe-content h1, 
        .recipe-content h2, 
        .recipe-content h3 {{
            color: var(--text-primary);
            letter-spacing: -0.025em;
            margin-top: 26px;
            margin-bottom: 12px;
        }}

        .recipe-content h2 {{
            font-size: 20px;
            font-weight: 600;
            border-bottom: 1px solid var(--surface-border);
            padding-bottom: 8px;
        }}

        .recipe-content p {{
            margin: 10px 0;
            color: #D1D1D6;
        }}

        .recipe-content hr {{
            border: none;
            border-top: 1px solid var(--surface-border);
            margin: 24px 0;
        }}

        /* Modern iOS Inset Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
            background: rgba(0, 0, 0, 0.25);
            border-radius: var(--radius-md);
            overflow: hidden;
            border: 1px solid var(--surface-border);
        }}

        th {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid var(--surface-border);
        }}

        td {{
            padding: 13px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-primary);
            font-size: 14px;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        /* Lists */
        ol, ul {{
            padding-left: 20px;
            margin: 14px 0;
        }}

        li {{
            margin-bottom: 10px;
            color: #E5E5EA;
        }}

        strong {{
            color: #FFFFFF;
            font-weight: 600;
        }}

        /* Action Bar */
        .action-bar {{
            display: flex;
            justify-content: flex-end;
            gap: 10px;
            margin-bottom: 20px;
        }}

        .icon-btn {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--surface-border);
            color: var(--text-secondary);
            padding: 8px 14px;
            border-radius: 999px;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: inherit;
        }}

        .icon-btn:hover {{
            background: rgba(255, 255, 255, 0.14);
            color: var(--text-primary);
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 16px;
            font-size: 13px;
            color: var(--text-tertiary);
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <header class="header">
            <div class="brand-badge">Recipe Studio</div>
            <h1 class="title">Savor</h1>
            <p class="subtitle">Enter any dish to generate a clean, step-by-step culinary guide.</p>
        </header>

        <div class="glass-card">
            <form method="post" action="/recipe" class="search-form">
                <div class="search-field">
                    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                        <circle cx="11" cy="11" r="8"></circle>
                        <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    </svg>
                    <input 
                        type="text" 
                        name="dish" 
                        id="dishInput" 
                        class="search-input" 
                        placeholder="Search or enter a dish..." 
                        value="{dish_val}" 
                        required 
                        autocomplete="off"
                        autofocus
                    />
                </div>
                <button type="submit" class="submit-btn">Generate</button>
            </form>

            <div class="suggestions-row">
                <span class="suggestion-chip" onclick="quickFill('Butter Chicken')">Butter Chicken</span>
                <span class="suggestion-chip" onclick="quickFill('Pasta Carbonara')">Pasta Carbonara</span>
                <span class="suggestion-chip" onclick="quickFill('Crispy Falafel Bowl')">Falafel Bowl</span>
                <span class="suggestion-chip" onclick="quickFill('Fluffy Pancakes')">Fluffy Pancakes</span>
                <span class="suggestion-chip" onclick="quickFill('Guacamole & Chips')">Fresh Guacamole</span>
            </div>
        </div>

        {recipe_content}

        <footer class="footer">
            Designed with SF Pro & Dark Glass Aesthetics
        </footer>
    </div>

    <script>
        function quickFill(name) {{
            const input = document.getElementById('dishInput');
            input.value = name;
            input.form.submit();
        }}

        function copyRecipe() {{
            const content = document.querySelector('.recipe-content');
            if (content) {{
                navigator.clipboard.writeText(content.innerText).then(() => {{
                    const btn = document.getElementById('copyBtn');
                    if (btn) {{
                        btn.innerHTML = '✓ Copied';
                        setTimeout(() => {{ btn.innerHTML = 'Copy'; }}, 2000);
                    }}
                }});
            }}
        }}
    </script>
</body>
</html>"""

@app.get("/", response_class=HTMLResponse)
def index():
    return render_page()

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "recipe-generator"}

@app.post("/recipe", response_class=HTMLResponse)
def get_recipe(dish: str = Form(...)):
    if not client:
        box = '''
        <div class="recipe-wrapper" style="border-color: rgba(255, 69, 58, 0.4);">
            <div style="color: #FF453A; font-weight: 500;">Configuration Notice: GROQ_API_KEY environment variable is not set.</div>
        </div>
        '''
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Give me a complete, refined recipe for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert executive chef. When given a dish name, generate an elegant, "
                        "concise, and beautifully structured recipe formatted in clean markdown. Include:\n"
                        "1. Dish Name & brief description\n"
                        "2. Prep Time, Cook Time, and Servings (in a clean markdown table)\n"
                        "3. Ingredients list with measurements (in a markdown table)\n"
                        "4. Step-by-step numbered cooking instructions\n"
                        "5. Chef's Secret Tip"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        recipe_md = response.choices[0].message.content
        html_recipe = md.render(recipe_md)
        box = f'''
        <div class="recipe-wrapper">
            <div class="action-bar">
                <button class="icon-btn" id="copyBtn" onclick="copyRecipe()">Copy Recipe</button>
            </div>
            <div class="recipe-content">{html_recipe}</div>
        </div>
        '''
    except Exception as e:
        box = f'''
        <div class="recipe-wrapper" style="border-color: rgba(255, 69, 58, 0.4);">
            <div style="color: #FF453A;">Error: {e}</div>
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
