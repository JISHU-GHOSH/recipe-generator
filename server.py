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
            --bg-warm: #F7F5F0;
            --ink-primary: #181614;
            --ink-secondary: #5C5852;
            --ink-tertiary: #8C877E;
            --card-paper: #FFFFFF;
            --border-crisp: #E6E2D8;
            --accent-flame: #D9480F;
            --accent-warm-tint: #FFF4ED;
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
            padding: 40px 16px 80px;
            font-family: var(--sans);
            background-color: var(--bg-warm);
            color: var(--ink-primary);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            -webkit-font-smoothing: antialiased;
            background-image: radial-gradient(circle at 50% 0%, rgba(217, 72, 15, 0.04) 0%, transparent 60%);
        }}

        .studio-layout {{
            width: 100%;
            max-width: 680px;
            display: flex;
            flex-direction: column;
            gap: 24px;
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
            background: var(--accent-warm-tint);
            border: 1px solid rgba(217, 72, 15, 0.2);
            padding: 5px 14px;
            border-radius: 999px;
            margin-bottom: 14px;
        }}

        .masthead h1 {{
            font-family: var(--serif);
            font-size: 52px;
            font-weight: 400;
            line-height: 1.05;
            letter-spacing: -0.02em;
            margin: 0 0 8px;
            color: var(--ink-primary);
        }}

        .masthead h1 em {{
            font-style: italic;
            color: var(--accent-flame);
        }}

        .masthead p {{
            font-size: 15px;
            color: var(--ink-secondary);
            margin: 0;
            line-height: 1.5;
        }}

        /* Clean Search Bar */
        .entry-box {{
            background: var(--card-paper);
            border: 1px solid var(--border-crisp);
            border-radius: 20px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
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
            background: #FAFAF7;
            border: 1px solid var(--border-crisp);
            border-radius: 14px;
            outline: none;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .input-group input:focus {{
            background: #FFFFFF;
            border-color: var(--ink-primary);
            box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.04);
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
            background: #FAFAF7;
            border: 1px solid var(--border-crisp);
            color: var(--ink-secondary);
            padding: 6px 12px;
            border-radius: 8px;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.15s ease;
        }}

        .catalog-tag:hover {{
            border-color: var(--ink-primary);
            color: var(--ink-primary);
            background: #FFFFFF;
        }}

        /* Physical Restaurant Slip / Index Card */
        .recipe-slip {{
            background: var(--card-paper);
            border: 1px solid var(--border-crisp);
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04), 0 1px 3px rgba(0, 0, 0, 0.02);
            position: relative;
            overflow: hidden;
            animation: slipIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slipIn {{
            from {{ opacity: 0; transform: translateY(12px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Perforated top bar */
        .slip-header {{
            background: #FAFAF7;
            border-bottom: 1px dashed var(--border-crisp);
            padding: 14px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--mono);
            font-size: 11px;
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
            padding: 5px 12px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .action-chip:hover {{
            border-color: var(--ink-primary);
        }}

        /* Main Slip Body */
        .slip-content {{
            padding: 32px 36px 40px;
            font-size: 15px;
            line-height: 1.7;
            color: var(--ink-secondary);
        }}

        .slip-content h1 {{
            font-family: var(--serif);
            font-size: 34px;
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
            margin: 28px 0 12px;
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
            margin: 18px 0;
            font-size: 14px;
            border: 1px solid var(--border-crisp);
            border-radius: 10px;
            overflow: hidden;
        }}

        th {{
            background: #FAFAF7;
            font-family: var(--mono);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: var(--ink-tertiary);
            padding: 10px 14px;
            text-align: left;
            border-bottom: 1px solid var(--border-crisp);
        }}

        td {{
            padding: 12px 14px;
            border-bottom: 1px solid #F0EEE6;
            color: var(--ink-primary);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        /* Interactive Checklist Instructions */
        ol {{
            padding-left: 20px;
            margin: 14px 0;
        }}

        li {{
            margin-bottom: 12px;
            color: var(--ink-secondary);
            transition: color 0.2s ease;
        }}

        li strong {{
            color: var(--ink-primary);
            font-weight: 600;
        }}

        /* Chef Tip Callout */
        blockquote, .chef-note {{
            background: var(--accent-warm-tint);
            border-left: 3px solid var(--accent-flame);
            padding: 14px 18px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
            font-size: 14.5px;
            color: #7C2D12;
        }}

        /* Footer */
        .studio-footer {{
            text-align: center;
            font-family: var(--mono);
            font-size: 11px;
            letter-spacing: 0.06em;
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
            <div class="slip-content" style="color: #D9480F;">GROQ_API_KEY environment variable is not configured.</div>
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
            <div class="slip-content" style="color: #D9480F;">Error: {e}</div>
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
