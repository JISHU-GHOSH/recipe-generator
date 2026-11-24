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
app = FastAPI(title="Savor - Editorial Culinary Studio")

def render_page(dish_val: str = "", recipe_content: str = "") -> str:
    # High-end Taste-Skill culinary blueprint watermark pattern
    blueprint_grid = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='180' viewBox='0 0 180 180'%3E"
        "%3Cg fill='none' stroke='%23C2410C' stroke-width='1.2' stroke-linecap='round' stroke-linejoin='round' opacity='0.08'%3E"
        "%3C!-- Chef Knife Blueprint --%3E"
        "%3Cpath d='M20 30 L65 24 C75 24 85 32 85 40 L20 40 Z'/%3E%3Crect x='10' y='32' width='10' height='6' rx='1'/%3E"
        "%3C!-- Whisk --%3E"
        "%3Cpath d='M135 20 L155 40 M145 30 C155 20 165 30 155 40'/%3E"
        "%3C!-- Cast Iron Skillet with measurement ticks --%3E"
        "%3Ccircle cx='45' cy='135' r='22'/%3E%3Cline x1='23' y1='135' x2='10' y2='135' stroke-width='2'/%3E"
        "%3C!-- Plated Cloche / Bell --%3E"
        "%3Cpath d='M120 145 C120 125 155 125 155 145 Z'/%3E%3Cline x1='115' y1='147' x2='160' y2='147'/%3E%3Ccircle cx='137.5' cy='123' r='2.5'/%3E"
        "%3C!-- Subtle Drafting Grid Crosses --%3E"
        "%3Cpath d='M90 85 L90 95 M85 90 L95 90' stroke-width='0.8' opacity='0.5'/%3E"
        "%3C/g%3E%3C/svg%3E"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Savor — Kitchen Studio & Recipe Card</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #F4EFE6;
            --ink-primary: #181614;
            --ink-secondary: #524E48;
            --ink-tertiary: #878177;
            --card-paper: #FFFFFF;
            --border-crisp: #DDD7C9;
            --accent-flame: #C2410C;
            --accent-warm-tint: #FFF3EB;
            --mono: 'JetBrains Mono', monospace;
            --serif: 'Instrument Serif', Georgia, serif;
            --sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            margin: 0;
            padding: 44px 16px 88px;
            font-family: var(--sans);
            background-color: var(--bg-base);
            /* Multi-layer atmospheric culinary lighting + blueprint watermark */
            background-image: 
                radial-gradient(at 15% 10%, rgba(234, 88, 12, 0.12) 0px, transparent 45%),
                radial-gradient(at 85% 15%, rgba(217, 119, 6, 0.10) 0px, transparent 40%),
                radial-gradient(at 50% 95%, rgba(180, 83, 9, 0.08) 0px, transparent 60%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.5) 0%, transparent 100%),
                url("{blueprint_grid}");
            background-repeat: repeat;
            background-attachment: fixed;
            color: var(--ink-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            -webkit-font-smoothing: antialiased;
            position: relative;
        }}

        /* Subtle Ambient Culinary Vignette Border */
        body::before {{
            content: "";
            position: fixed;
            inset: 0;
            box-shadow: inset 0 0 120px rgba(120, 53, 15, 0.07);
            pointer-events: none;
            z-index: 0;
        }}

        .studio-layout {{
            width: 100%;
            max-width: 690px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            position: relative;
            z-index: 1;
        }}

        /* Editorial Header */
        .masthead {{
            text-align: center;
            padding-bottom: 8px;
        }}

        .meta-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-family: var(--mono);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: var(--accent-flame);
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(194, 65, 12, 0.22);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 6px 15px;
            border-radius: 999px;
            margin-bottom: 14px;
            box-shadow: 0 2px 8px rgba(194, 65, 12, 0.05);
        }}

        .masthead h1 {{
            font-family: var(--serif);
            font-size: 54px;
            font-weight: 400;
            line-height: 1.05;
            letter-spacing: -0.02em;
            margin: 0 0 8px;
            color: var(--ink-primary);
            text-shadow: 0 2px 16px rgba(255, 255, 255, 0.6);
        }}

        .masthead h1 em {{
            font-style: italic;
            color: var(--accent-flame);
        }}

        .masthead p {{
            font-size: 15.5px;
            color: var(--ink-secondary);
            margin: 0;
            line-height: 1.5;
        }}

        /* Clean Search Bar with Glass Elevation */
        .entry-box {{
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-crisp);
            border-radius: 22px;
            padding: 20px;
            box-shadow: 
                0 16px 36px -10px rgba(120, 53, 15, 0.08),
                0 2px 6px rgba(0, 0, 0, 0.02);
        }}

        form.dish-form {{
            display: flex;
            gap: 10px;
        }}

        .input-group {{
            flex: 1;
            position: relative;
            display: flex;
            align-items: center;
        }}

        .input-group input {{
            width: 100%;
            padding: 15px 18px;
            font-family: var(--sans);
            font-size: 16px;
            color: var(--ink-primary);
            background: #FAF8F5;
            border: 1px solid var(--border-crisp);
            border-radius: 14px;
            outline: none;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .input-group input:focus {{
            background: #FFFFFF;
            border-color: var(--ink-primary);
            box-shadow: 0 0 0 3px rgba(194, 65, 12, 0.08);
        }}

        .input-group input::placeholder {{
            color: var(--ink-tertiary);
        }}

        .cook-button {{
            background: var(--ink-primary);
            color: #FFFFFF;
            border: none;
            border-radius: 14px;
            padding: 0 24px;
            font-family: var(--sans);
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
            box-shadow: 0 4px 12px rgba(24, 22, 20, 0.15);
        }}

        .cook-button:hover {{
            background: var(--accent-flame);
            transform: scale(0.98);
        }}

        .cook-button:active {{
            transform: scale(0.95);
        }}

        /* Editorial Quick Picks */
        .catalog-strip {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 14px;
            overflow-x: auto;
            scrollbar-width: none;
            padding-bottom: 2px;
        }}

        .catalog-strip::-webkit-scrollbar {{
            display: none;
        }}

        .catalog-tag {{
            font-family: var(--mono);
            font-size: 12px;
            background: rgba(255, 255, 255, 0.7);
            border: 1px solid var(--border-crisp);
            color: var(--ink-secondary);
            padding: 6px 13px;
            border-radius: 8px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }}

        .catalog-tag:hover {{
            border-color: var(--accent-flame);
            color: var(--accent-flame);
            background: #FFFFFF;
            transform: translateY(-1px);
        }}

        /* Physical Restaurant Slip / Docket */
        .recipe-slip {{
            background: #FFFFFF;
            border: 1px solid var(--border-crisp);
            border-radius: 22px;
            box-shadow: 
                0 24px 48px -12px rgba(120, 53, 15, 0.12),
                0 4px 12px rgba(0, 0, 0, 0.03);
            position: relative;
            overflow: hidden;
            animation: slipIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slipIn {{
            from {{ opacity: 0; transform: translateY(14px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Perforated top bar */
        .slip-header {{
            background: #FAF8F4;
            border-bottom: 1px dashed var(--border-crisp);
            padding: 14px 26px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--mono);
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--ink-tertiary);
        }}

        .action-chip {{
            background: #FFFFFF;
            border: 1px solid var(--border-crisp);
            color: var(--ink-primary);
            font-family: var(--mono);
            font-size: 11px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .action-chip:hover {{
            border-color: var(--ink-primary);
        }}

        /* Main Slip Body */
        .slip-content {{
            padding: 34px 38px 44px;
            font-size: 15.5px;
            line-height: 1.7;
            color: var(--ink-secondary);
        }}

        .slip-content h1 {{
            font-family: var(--serif);
            font-size: 36px;
            font-weight: 400;
            color: var(--ink-primary);
            margin: 0 0 12px;
            line-height: 1.15;
            letter-spacing: -0.015em;
        }}

        .slip-content h2 {{
            font-family: var(--mono);
            font-size: 13px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--ink-primary);
            margin: 30px 0 12px;
            padding-bottom: 6px;
            border-bottom: 1px solid var(--border-crisp);
        }}

        .slip-content h3 {{
            font-size: 17px;
            color: var(--ink-primary);
            margin: 20px 0 8px;
        }}

        .slip-content hr {{
            border: none;
            border-top: 1px dashed var(--border-crisp);
            margin: 28px 0;
        }}

        /* Structured Spec Table */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
            border: 1px solid var(--border-crisp);
            border-radius: 10px;
            overflow: hidden;
            background: #FAF8F4;
        }}

        th {{
            background: #F1ECE1;
            font-family: var(--mono);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--ink-primary);
            padding: 11px 16px;
            text-align: left;
            border-bottom: 1px solid var(--border-crisp);
        }}

        td {{
            padding: 13px 16px;
            border-bottom: 1px solid #EAE4D8;
            color: var(--ink-primary);
            background: #FFFFFF;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        /* Step instructions */
        ol {{
            padding-left: 20px;
            margin: 14px 0;
        }}

        li {{
            margin-bottom: 12px;
            color: var(--ink-secondary);
        }}

        li strong {{
            color: var(--ink-primary);
            font-weight: 600;
        }}

        /* Footer */
        .studio-footer {{
            text-align: center;
            font-family: var(--mono);
            font-size: 11px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: var(--ink-tertiary);
            padding: 16px 0;
        }}
    </style>
</head>
<body>
    <div class="studio-layout">
        <header class="masthead">
            <div class="meta-pill">Recipe Docket — Table No. 01</div>
            <h1>Savor <em>Studio</em></h1>
            <p>Every dish has an architecture. Enter a dish name for your exact kitchen docket.</p>
        </header>

        <div class="entry-box">
            <form method="post" action="/recipe" class="dish-form">
                <div class="input-group">
                    <input 
                        type="text" 
                        name="dish" 
                        id="dishInput" 
                        placeholder="Enter dish name (e.g. Cacio e Pepe, Tacos al Pastor...)" 
                        value="{dish_val}" 
                        required 
                        autocomplete="off"
                        autofocus
                    />
                </div>
                <button type="submit" class="cook-button">Order Recipe</button>
            </form>

            <div class="catalog-strip">
                <span class="catalog-tag" onclick="orderDish('Cacio e Pepe')">Cacio e Pepe</span>
                <span class="catalog-tag" onclick="orderDish('Chicken Tikka Masala')">Chicken Tikka Masala</span>
                <span class="catalog-tag" onclick="orderDish('Crispy Smash Burger')">Smash Burger</span>
                <span class="catalog-tag" onclick="orderDish('Japanese Tonkatsu')">Tonkatsu</span>
                <span class="catalog-tag" onclick="orderDish('Classic French Omelette')">French Omelette</span>
            </div>
        </div>

        {recipe_content}

        <footer class="studio-footer">
            Savor Editorial Kitchen · Measured in Grams & Minutes
        </footer>
    </div>

    <script>
        function orderDish(name) {{
            const input = document.getElementById('dishInput');
            input.value = name;
            input.form.submit();
        }}

        function copySlip() {{
            const content = document.querySelector('.slip-content');
            if (content) {{
                navigator.clipboard.writeText(content.innerText).then(() => {{
                    const btn = document.getElementById('copyBtn');
                    if (btn) {{
                        btn.innerHTML = '✓ Printed';
                        setTimeout(() => {{ btn.innerHTML = 'Copy Slip'; }}, 2000);
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
        <div class="recipe-slip">
            <div class="slip-header">Notice</div>
            <div class="slip-content" style="color: #C2410C;">GROQ_API_KEY environment variable is not configured.</div>
        </div>
        '''
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Produce an exact, chef-grade kitchen docket for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an executive chef at a world-class restaurant. When given a dish name, generate a concise, "
                        "flawlessly measured recipe formatted in clean markdown like a physical kitchen docket. Avoid marketing fluff or generic adjectives.\n\n"
                        "Format strictly:\n"
                        "1. Dish Name (h1) with a one-sentence culinary summary\n"
                        "2. Timing & Yield (markdown table: Prep Time, Cook Time, Total Time, Servings)\n"
                        "3. Mise En Place / Ingredients (markdown table: Ingredient, Exact Quantity, Prep Notes)\n"
                        "4. Method (Numbered chronological kitchen steps, clear and actionable)\n"
                        "5. Chef's Critical Note (One technical pro tip that prevents common failures)"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        recipe_md = response.choices[0].message.content
        html_recipe = md.render(recipe_md)
        box = f'''
        <div class="recipe-slip">
            <div class="slip-header">
                <span>Docket #0829 · Kitchen Station</span>
                <button class="action-chip" id="copyBtn" onclick="copySlip()">Copy Slip</button>
            </div>
            <div class="slip-content">{html_recipe}</div>
        </div>
        '''
    except Exception as e:
        box = f'''
        <div class="recipe-slip">
            <div class="slip-header">Error</div>
            <div class="slip-content" style="color: #C2410C;">Error: {e}</div>
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
