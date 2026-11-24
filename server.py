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
app = FastAPI(title="Savor - iOS Food Studio")

def render_page(dish_val: str = "", recipe_content: str = "") -> str:
    # High-end iOS food pattern with warm culinary line art
    ios_food_pattern = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160' viewBox='0 0 160 160'%3E"
        "%3Cg fill='none' stroke='%23ea580c' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round' opacity='0.16'%3E"
        "%3C!-- Chef Hat --%3E"
        "%3Cpath d='M25 45 C15 35 25 22 36 26 C42 16 58 16 64 26 C75 22 85 35 75 45 Z'/%3E"
        "%3Cpath d='M28 45 L72 45 L69 52 L31 52 Z'/%3E"
        "%3C!-- Pizza Slice --%3E"
        "%3Cpath d='M115 25 L145 35 L125 60 Z'/%3E%3Ccircle cx='126' cy='36' r='2' fill='%23ea580c'/%3E"
        "%3C!-- Croissant / Bakery --%3E"
        "%3Cpath d='M35 110 C25 125 45 145 65 135 C75 128 55 105 35 110 Z'/%3E"
        "%3C!-- Ramen Bowl & Steam --%3E"
        "%3Cpath d='M105 125 C105 145 135 145 135 125 Z'/%3E%3Cpath d='M102 125 L138 125'/%3E"
        "%3Cpath d='M112 115 Q115 110 112 105 M120 116 Q123 111 120 106 M128 115 Q131 110 128 105'/%3E"
        "%3C!-- Avocado --%3E"
        "%3Cpath d='M90 75 C82 62 70 70 70 85 C70 98 88 98 88 85 Z'/%3E%3Ccircle cx='79' cy='84' r='4'/%3E"
        "%3C/g%3E%3C/svg%3E"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Savor — Kitchen Studio</title>
    <style>
        :root {{
            --bg-canvas: #FFFBF7;
            --surface-glass: rgba(255, 255, 255, 0.82);
            --surface-border: rgba(234, 88, 12, 0.16);
            --surface-shadow: 0 20px 48px -12px rgba(194, 65, 12, 0.12), 0 8px 24px -6px rgba(0, 0, 0, 0.04);
            
            --ios-coral: #FF5A36;
            --ios-orange: #FF8A00;
            --ios-peach: #FFF0E6;
            --ios-dark: #1F1916;
            --ios-subtext: #7C6E65;
            --ios-pill-bg: rgba(255, 255, 255, 0.7);
            
            --radius-xl: 32px;
            --radius-lg: 24px;
            --radius-md: 16px;
            --radius-pill: 9999px;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            margin: 0;
            padding: 32px 18px 80px;
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", -system-ui, sans-serif;
            background-color: var(--bg-canvas);
            background-image: 
                radial-gradient(at 15% 15%, rgba(255, 138, 0, 0.12) 0px, transparent 55%),
                radial-gradient(at 85% 10%, rgba(255, 90, 54, 0.14) 0px, transparent 50%),
                radial-gradient(at 50% 90%, rgba(255, 214, 170, 0.25) 0px, transparent 65%),
                url("{ios_food_pattern}");
            background-repeat: repeat;
            background-attachment: fixed;
            color: var(--ios-dark);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            letter-spacing: -0.015em;
            -webkit-font-smoothing: antialiased;
            position: relative;
        }}

        /* Subtle iOS Floating Food Elements */
        .ios-doodle {{
            position: fixed;
            font-size: 32px;
            opacity: 0.65;
            filter: drop-shadow(0 6px 12px rgba(255, 90, 54, 0.15));
            pointer-events: none;
            user-select: none;
            z-index: 0;
            animation: floatEmoji 6s ease-in-out infinite alternate;
        }}
        .d-1 {{ top: 38px; left: 32px; animation-duration: 5.5s; }}
        .d-2 {{ top: 120px; right: 36px; animation-duration: 7s; }}
        .d-3 {{ bottom: 100px; left: 40px; animation-duration: 6.5s; }}
        .d-4 {{ bottom: 60px; right: 45px; animation-duration: 8s; }}

        @keyframes floatEmoji {{
            0% {{ transform: translateY(0px) rotate(0deg); }}
            100% {{ transform: translateY(-12px) rotate(6deg); }}
        }}

        .app-shell {{
            width: 100%;
            max-width: 680px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: relative;
            z-index: 1;
        }}

        /* Header */
        .header {{
            text-align: center;
            padding: 16px 0 8px;
        }}

        .brand-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            background: rgba(255, 255, 255, 0.75);
            border: 1px solid rgba(255, 90, 54, 0.2);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            font-size: 13px;
            font-weight: 600;
            color: var(--ios-coral);
            box-shadow: 0 4px 12px rgba(255, 90, 54, 0.08);
            margin-bottom: 12px;
        }}

        .title {{
            font-size: 40px;
            font-weight: 800;
            letter-spacing: -0.035em;
            margin: 0;
            color: var(--ios-dark);
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }}

        .title span.highlight {{
            background: linear-gradient(135deg, #FF5A36 0%, #FF8A00 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .subtitle {{
            font-size: 16px;
            color: var(--ios-subtext);
            margin: 6px 0 0;
            font-weight: 450;
        }}

        /* iOS Glass Search Card */
        .glass-card {{
            background: var(--surface-glass);
            backdrop-filter: blur(35px) saturate(190%);
            -webkit-backdrop-filter: blur(35px) saturate(190%);
            border: 1px solid var(--surface-border);
            border-radius: var(--radius-xl);
            padding: 24px;
            box-shadow: var(--surface-shadow);
        }}

        form.search-box {{
            display: flex;
            gap: 12px;
            align-items: center;
        }}

        .input-wrapper {{
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
        }}

        .input-icon {{
            position: absolute;
            left: 18px;
            font-size: 20px;
            pointer-events: none;
        }}

        .search-field {{
            width: 100%;
            background: rgba(255, 255, 255, 0.9);
            border: 1.5px solid rgba(234, 88, 12, 0.15);
            border-radius: 20px;
            padding: 16px 20px 16px 52px;
            font-size: 16.5px;
            font-family: inherit;
            color: var(--ios-dark);
            outline: none;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.02);
        }}

        .search-field::placeholder {{
            color: #A89C94;
        }}

        .search-field:focus {{
            background: #FFFFFF;
            border-color: var(--ios-coral);
            box-shadow: 0 0 0 4px rgba(255, 90, 54, 0.12);
        }}

        .cook-action-btn {{
            background: linear-gradient(135deg, #FF5A36 0%, #FF8A00 100%);
            color: #FFFFFF;
            border: none;
            border-radius: 20px;
            padding: 0 26px;
            height: 54px;
            font-size: 16px;
            font-weight: 700;
            font-family: inherit;
            cursor: pointer;
            box-shadow: 0 8px 20px -4px rgba(255, 90, 54, 0.4);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            white-space: nowrap;
        }}

        .cook-action-btn:hover {{
            transform: scale(0.98) translateY(-1px);
            box-shadow: 0 10px 24px -2px rgba(255, 90, 54, 0.5);
        }}

        .cook-action-btn:active {{
            transform: scale(0.94);
        }}

        /* iOS Horizontal Scrolling Pills */
        .food-pills {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 16px;
            overflow-x: auto;
            scrollbar-width: none;
            -webkit-overflow-scrolling: touch;
            padding-bottom: 2px;
        }}

        .food-pills::-webkit-scrollbar {{
            display: none;
        }}

        .food-pill {{
            padding: 8px 16px;
            background: var(--ios-pill-bg);
            border: 1px solid rgba(234, 88, 12, 0.16);
            border-radius: var(--radius-pill);
            color: var(--ios-dark);
            font-size: 13.5px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.2s ease;
            user-select: none;
        }}

        .food-pill:hover {{
            background: #FFFFFF;
            border-color: var(--ios-coral);
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(255, 90, 54, 0.12);
        }}

        .food-pill:active {{
            transform: scale(0.95);
        }}

        /* Recipe Result Sheet */
        .recipe-sheet {{
            background: var(--surface-glass);
            backdrop-filter: blur(40px) saturate(190%);
            -webkit-backdrop-filter: blur(40px) saturate(190%);
            border: 1px solid var(--surface-border);
            border-radius: var(--radius-xl);
            padding: 36px 38px;
            box-shadow: var(--surface-shadow);
            animation: sheetIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes sheetIn {{
            from {{ opacity: 0; transform: translateY(16px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Action Top Bar */
        .sheet-top {{
            display: flex;
            justify-content: flex-end;
            margin-bottom: 20px;
        }}

        .copy-pill {{
            background: rgba(255, 255, 255, 0.9);
            border: 1px solid rgba(234, 88, 12, 0.2);
            color: var(--ios-dark);
            padding: 8px 16px;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
            font-family: inherit;
        }}

        .copy-pill:hover {{
            background: #FFFFFF;
            border-color: var(--ios-coral);
        }}

        /* Recipe Typography */
        .recipe-body {{
            line-height: 1.7;
            color: #332B27;
            font-size: 15.5px;
        }}

        .recipe-body h1, 
        .recipe-body h2, 
        .recipe-body h3 {{
            color: var(--ios-dark);
            letter-spacing: -0.025em;
            margin-top: 26px;
            margin-bottom: 12px;
            font-weight: 750;
        }}

        .recipe-body h2 {{
            font-size: 22px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1.5px solid rgba(234, 88, 12, 0.12);
            padding-bottom: 8px;
        }}

        .recipe-body hr {{
            border: none;
            border-top: 1px dashed rgba(234, 88, 12, 0.2);
            margin: 26px 0;
        }}

        /* iOS Card Inset Table */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            background: rgba(255, 255, 255, 0.7);
            border-radius: var(--radius-md);
            overflow: hidden;
            border: 1px solid rgba(234, 88, 12, 0.15);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
        }}

        th {{
            background: var(--ios-peach);
            color: #9A3412;
            font-size: 12.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            padding: 13px 18px;
            text-align: left;
            border-bottom: 1px solid rgba(234, 88, 12, 0.12);
        }}

        td {{
            padding: 13px 18px;
            border-top: 1px solid rgba(234, 88, 12, 0.08);
            font-size: 14.5px;
            color: var(--ios-dark);
        }}

        tr:nth-child(even) td {{
            background: rgba(255, 247, 240, 0.5);
        }}

        ol, ul {{
            padding-left: 22px;
            margin: 14px 0;
        }}

        li {{
            margin-bottom: 10px;
        }}

        strong {{
            color: #C2410C;
            font-weight: 700;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            padding: 16px;
            font-size: 13px;
            color: var(--ios-subtext);
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <!-- Floating iOS Food Emojis -->
    <div class="ios-doodle d-1">🥑</div>
    <div class="ios-doodle d-2">🍕</div>
    <div class="ios-doodle d-3">🍜</div>
    <div class="ios-doodle d-4">🥞</div>

    <div class="app-shell">
        <header class="header">
            <div class="brand-pill">👨‍🍳 Kitchen Studio</div>
            <h1 class="title">Savor <span class="highlight">Studio</span></h1>
            <p class="subtitle">Craft delicious, step-by-step culinary recipes in seconds.</p>
        </header>

        <div class="glass-card">
            <form method="post" action="/recipe" class="search-box">
                <div class="input-wrapper">
                    <span class="input-icon">🍽️</span>
                    <input 
                        type="text" 
                        name="dish" 
                        id="dishInput" 
                        class="search-field" 
                        placeholder="What are we cooking today? (e.g. Pasta, Tacos...)" 
                        value="{dish_val}" 
                        required 
                        autocomplete="off"
                        autofocus
                    />
                </div>
                <button type="submit" class="cook-action-btn">
                    <span>Cook It</span>
                    <span>✨</span>
                </button>
            </form>

            <div class="food-pills">
                <span class="food-pill" onclick="quickFill('Butter Chicken')">🍗 Butter Chicken</span>
                <span class="food-pill" onclick="quickFill('Creamy Pasta Carbonara')">🍝 Carbonara</span>
                <span class="food-pill" onclick="quickFill('Crispy Falafel Bowl')">🧆 Falafel Bowl</span>
                <span class="food-pill" onclick="quickFill('Fluffy Pancakes')">🥞 Fluffy Pancakes</span>
                <span class="food-pill" onclick="quickFill('Fresh Guacamole & Salsa')">🥑 Guacamole</span>
            </div>
        </div>

        {recipe_content}

        <footer class="footer">
            Designed with iOS Frosted Glass & Warm Culinary Aesthetics
        </footer>
    </div>

    <script>
        function quickFill(name) {{
            const input = document.getElementById('dishInput');
            input.value = name;
            input.form.submit();
        }}

        function copyRecipe() {{
            const content = document.querySelector('.recipe-body');
            if (content) {{
                navigator.clipboard.writeText(content.innerText).then(() => {{
                    const btn = document.getElementById('copyBtn');
                    if (btn) {{
                        btn.innerHTML = '✓ Copied';
                        setTimeout(() => {{ btn.innerHTML = '📋 Copy Recipe'; }}, 2000);
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
        <div class="recipe-sheet" style="border-color: rgba(255, 90, 54, 0.4);">
            <div style="color: #C2410C; font-weight: 600;">Configuration Notice: GROQ_API_KEY environment variable is not set.</div>
        </div>
        '''
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Give me a complete, mouthwatering recipe for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a fun, expert executive chef. When given a dish name, generate a mouthwatering, "
                        "vibrant, and easy-to-follow recipe formatted in clean markdown. Include:\n"
                        "1. Dish Name & brief tantalizing description with food emojis\n"
                        "2. Prep Time, Cook Time, and Servings (in a markdown table)\n"
                        "3. Ingredients list with measurements (in a markdown table)\n"
                        "4. Step-by-step numbered cooking instructions\n"
                        "5. Chef's Pro Secret Tip"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        recipe_md = response.choices[0].message.content
        html_recipe = md.render(recipe_md)
        box = f'''
        <div class="recipe-sheet">
            <div class="sheet-top">
                <button class="copy-pill" id="copyBtn" onclick="copyRecipe()">📋 Copy Recipe</button>
            </div>
            <div class="recipe-body">{html_recipe}</div>
        </div>
        '''
    except Exception as e:
        box = f'''
        <div class="recipe-sheet" style="border-color: rgba(255, 90, 54, 0.4);">
            <div style="color: #C2410C;">⚠️ Error: {e}</div>
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
