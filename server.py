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
app = FastAPI(title="Savor - Scroll-Craft Culinary Studio")

def render_page(dish_val: str = "", recipe_content: str = "") -> str:
    # High-end Scroll-Craft architectural line art (Background Layer)
    blueprint_grid = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3E"
        "%3Cg fill='none' stroke='%23C2410C' stroke-width='1.2' stroke-linecap='round' stroke-linejoin='round' opacity='0.09'%3E"
        "%3C!-- Chef Knife Blueprint --%3E"
        "%3Cpath d='M20 30 L75 22 C88 22 98 32 98 42 L20 42 Z'/%3E%3Crect x='10' y='32' width='10' height='7' rx='1'/%3E"
        "%3C!-- Whisk --%3E"
        "%3Cpath d='M150 20 L175 45 M160 32 C172 20 185 32 172 45'/%3E"
        "%3C!-- Cast Iron Skillet with measurements --%3E"
        "%3Ccircle cx='50' cy='150' r='26'/%3E%3Cline x1='24' y1='150' x2='10' y2='150' stroke-width='2'/%3E"
        "%3C!-- Plated Cloche / Bell --%3E"
        "%3Cpath d='M135 160 C135 135 175 135 175 160 Z'/%3E%3Cline x1='128' y1='163' x2='182' y2='163'/%3E%3Ccircle cx='155' cy='132' r='3'/%3E"
        "%3C!-- Drafting Crosshairs --%3E"
        "%3Cpath d='M100 90 L100 110 M90 100 L110 100' stroke-width='0.8' opacity='0.6'/%3E"
        "%3C/g%3E%3C/svg%3E"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Savor — Dimensional Kitchen Pass</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-base: #F4EFE6;
            --ink-primary: #181614;
            --ink-secondary: #524E48;
            --ink-tertiary: #878177;
            --border-crisp: #DDD7C9;
            --accent-flame: #C2410C;
            --accent-warm-tint: #FFF3EB;
            --mono: 'JetBrains Mono', monospace;
            --serif: 'Instrument Serif', Georgia, serif;
            --sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            
            /* Dynamic Scroll & Mouse Parallax Variables */
            --mouse-x: 0px;
            --mouse-y: 0px;
            --scroll-offset: 0px;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: var(--sans);
            background-color: var(--bg-base);
            color: var(--ink-primary);
            min-height: 100vh;
            overflow-x: hidden;
            -webkit-font-smoothing: antialiased;
            position: relative;
        }}

        /* ==========================================================================
           SCROLL-CRAFT LAYER 1: DEEP ENVIRONMENTAL BACKGROUND PLANE
           ========================================================================== */
        .sc-plane-background {{
            position: fixed;
            inset: -40px;
            z-index: 0;
            pointer-events: none;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 15% 10%, rgba(234, 88, 12, 0.15) 0px, transparent 50%),
                radial-gradient(at 85% 15%, rgba(217, 119, 6, 0.14) 0px, transparent 45%),
                radial-gradient(at 50% 95%, rgba(180, 83, 9, 0.12) 0px, transparent 65%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.6) 0%, transparent 100%),
                url("{blueprint_grid}");
            background-repeat: repeat;
            transform: translate3d(calc(var(--mouse-x) * -0.015), calc(var(--mouse-y) * -0.015), 0);
            transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1);
            will-change: transform;
        }}

        /* Atmospheric Vignette */
        .sc-plane-background::after {{
            content: "";
            position: absolute;
            inset: 0;
            box-shadow: inset 0 0 140px rgba(120, 53, 15, 0.09);
        }}

        /* ==========================================================================
           SCROLL-CRAFT LAYER 2: INTERLEAVED ATMOSPHERIC STEAM & EMBERS
           ========================================================================== */
        .sc-plane-atmosphere {{
            position: fixed;
            inset: 0;
            z-index: 1;
            pointer-events: none;
            overflow: hidden;
        }}

        .steam-particle {{
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.75) 0%, rgba(255, 243, 235, 0.1) 70%, transparent 100%);
            filter: blur(14px);
            opacity: 0.6;
            animation: floatSteam 10s ease-in-out infinite alternate;
        }}
        .sp-1 {{ width: 220px; height: 220px; top: 8%; left: -40px; animation-duration: 9s; }}
        .sp-2 {{ width: 260px; height: 260px; top: 22%; right: -60px; animation-duration: 12s; }}
        .sp-3 {{ width: 200px; height: 200px; bottom: 15%; left: 10%; animation-duration: 11s; }}

        @keyframes floatSteam {{
            0% {{ transform: translateY(0px) scale(1) translate3d(calc(var(--mouse-x) * 0.03), calc(var(--mouse-y) * 0.03), 0); }}
            100% {{ transform: translateY(-30px) scale(1.12) translate3d(calc(var(--mouse-x) * 0.06), calc(var(--mouse-y) * 0.06), 0); }}
        }}

        /* ==========================================================================
           SCROLL-CRAFT LAYER 3: MIDGROUND SUBJECT STAGE (THE KITCHEN PASS)
           ========================================================================== */
        .sc-stage-container {{
            position: relative;
            z-index: 2;
            width: 100%;
            max-width: 690px;
            margin: 0 auto;
            padding: 48px 18px 96px;
            display: flex;
            flex-direction: column;
            gap: 24px;
        }}

        /* Masthead */
        .masthead {{
            text-align: center;
            padding-bottom: 8px;
            transform: translate3d(calc(var(--mouse-x) * 0.008), calc(var(--mouse-y) * 0.008), 0);
            transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1);
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
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(194, 65, 12, 0.22);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            padding: 6px 16px;
            border-radius: 999px;
            margin-bottom: 14px;
            box-shadow: 0 4px 12px rgba(194, 65, 12, 0.06);
        }}

        .masthead h1 {{
            font-family: var(--serif);
            font-size: 56px;
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
            font-size: 15.5px;
            color: var(--ink-secondary);
            margin: 0;
            line-height: 1.5;
        }}

        /* The Working Surface (Interactive Search) */
        .entry-box {{
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid var(--border-crisp);
            border-radius: 22px;
            padding: 22px;
            box-shadow: 
                0 20px 42px -10px rgba(120, 53, 15, 0.09),
                0 4px 12px rgba(0, 0, 0, 0.03);
            transform: translate3d(calc(var(--mouse-x) * 0.012), calc(var(--mouse-y) * 0.012), 0);
            transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
        }}

        .entry-box:hover {{
            box-shadow: 
                0 24px 48px -8px rgba(120, 53, 15, 0.14),
                0 6px 16px rgba(0, 0, 0, 0.04);
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
            padding: 16px 20px;
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
            box-shadow: 0 0 0 3px rgba(194, 65, 12, 0.1);
        }}

        .input-group input::placeholder {{
            color: var(--ink-tertiary);
        }}

        .cook-button {{
            background: var(--ink-primary);
            color: #FFFFFF;
            border: none;
            border-radius: 14px;
            padding: 0 26px;
            font-family: var(--sans);
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
            box-shadow: 0 4px 14px rgba(24, 22, 20, 0.16);
        }}

        .cook-button:hover {{
            background: var(--accent-flame);
            transform: scale(0.98);
        }}

        .cook-button:active {{
            transform: scale(0.95);
        }}

        /* Catalog Strip */
        .catalog-strip {{
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
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
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid var(--border-crisp);
            color: var(--ink-secondary);
            padding: 6px 14px;
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

        /* Physical Restaurant Slip / Docket (Elevated Layer) */
        .recipe-slip {{
            background: #FFFFFF;
            border: 1px solid var(--border-crisp);
            border-radius: 22px;
            box-shadow: 
                0 30px 60px -15px rgba(120, 53, 15, 0.14),
                0 6px 16px rgba(0, 0, 0, 0.04);
            position: relative;
            overflow: hidden;
            transform: translate3d(calc(var(--mouse-x) * 0.018), calc(var(--mouse-y) * 0.018), 0);
            transition: transform 0.15s cubic-bezier(0.16, 1, 0.3, 1);
            animation: slipReveal 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes slipReveal {{
            from {{ opacity: 0; transform: translateY(20px) scale(0.98); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        /* Perforated Top Bar */
        .slip-header {{
            background: #FAF8F4;
            border-bottom: 1px dashed var(--border-crisp);
            padding: 14px 28px;
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
            padding: 36px 40px 48px;
            font-size: 15.5px;
            line-height: 1.7;
            color: var(--ink-secondary);
        }}

        .slip-content h1 {{
            font-family: var(--serif);
            font-size: 38px;
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
            margin: 32px 0 14px;
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

        /* Table */
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
            padding: 12px 16px;
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

        /* Instructions */
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
            padding: 24px 0;
        }}

        /* ==========================================================================
           SCROLL-CRAFT LAYER 4: FLOATING FOREGROUND EMBERS & PARTICLES
           ========================================================================== */
        .sc-plane-foreground {{
            position: fixed;
            inset: 0;
            z-index: 3;
            pointer-events: none;
            overflow: hidden;
        }}

        .floating-accent {{
            position: absolute;
            font-size: 26px;
            filter: drop-shadow(0 8px 16px rgba(194, 65, 12, 0.15));
            opacity: 0.7;
            user-select: none;
            will-change: transform;
            transition: transform 0.1s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .fa-1 {{ top: 18%; left: 8%; transform: translate3d(calc(var(--mouse-x) * 0.05), calc(var(--mouse-y) * 0.05), 0); }}
        .fa-2 {{ top: 32%; right: 7%; transform: translate3d(calc(var(--mouse-x) * -0.04), calc(var(--mouse-y) * -0.04), 0); }}
        .fa-3 {{ bottom: 25%; left: 6%; transform: translate3d(calc(var(--mouse-x) * 0.06), calc(var(--mouse-y) * 0.06), 0); }}
        .fa-4 {{ bottom: 15%; right: 9%; transform: translate3d(calc(var(--mouse-x) * -0.05), calc(var(--mouse-y) * -0.05), 0); }}
    </style>
</head>
<body>
    <!-- Layer 1: Deep Environmental Background -->
    <div class="sc-plane-background"></div>

    <!-- Layer 2: Interleaved Atmospheric Steam Clouds -->
    <div class="sc-plane-atmosphere">
        <div class="steam-particle sp-1"></div>
        <div class="steam-particle sp-2"></div>
        <div class="steam-particle sp-3"></div>
    </div>

    <!-- Layer 3: Midground Working Surface Stage -->
    <main class="sc-stage-container">
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
    </main>

    <!-- Layer 4: Floating Foreground Embers & Culinary Accents -->
    <div class="sc-plane-foreground">
        <div class="floating-accent fa-1">🧂</div>
        <div class="floating-accent fa-2">🌿</div>
        <div class="floating-accent fa-3">🌶️</div>
        <div class="floating-accent fa-4">🍋</div>
    </div>

    <script>
        // Scroll-Craft Multi-Plane Pointer & Scroll Physics Engine
        let targetX = 0, targetY = 0;
        let currentX = 0, currentY = 0;

        window.addEventListener('mousemove', (e) => {{
            const {{ innerWidth, innerHeight }} = window;
            targetX = e.clientX - innerWidth / 2;
            targetY = e.clientY - innerHeight / 2;
        }});

        function updateParallax() {{
            // Smooth lerp (linear interpolation) for Apple/Scroll-Craft buttery feel
            currentX += (targetX - currentX) * 0.08;
            currentY += (targetY - currentY) * 0.08;

            document.documentElement.style.setProperty('--mouse-x', `${{currentX.toFixed(2)}}px`);
            document.documentElement.style.setProperty('--mouse-y', `${{currentY.toFixed(2)}}px`);

            requestAnimationFrame(updateParallax);
        }}
        requestAnimationFrame(updateParallax);

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
