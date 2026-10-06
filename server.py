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
app = FastAPI(title="SavorAI Recipe Generator")

def render_page(dish_val: str = "", recipe_content: str = "") -> str:
    # Food background doodles as repeating SVG patterns
    food_pattern = (
        "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120' viewBox='0 0 120 120'%3E"
        "%3Cg fill='none' stroke='%23e07a5f' stroke-width='1.4' stroke-linecap='round' stroke-linejoin='round' opacity='0.22'%3E"
        "%3C!-- Pizza Slice --%3E"
        "%3Cpath d='M15 15 L35 22 L22 38 Z'/%3E%3Ccircle cx='23' cy='23' r='2' fill='%23e07a5f'/%3E"
        "%3C!-- Burger --%3E"
        "%3Cpath d='M75 18 Q88 10 101 18 L101 22 L75 22 Z'/%3E%3Cpath d='M73 24 Q88 27 103 24'/%3E%3Cpath d='M75 26 L101 26 Q88 34 75 26 Z'/%3E"
        "%3C!-- Chef Hat --%3E"
        "%3Cpath d='M20 75 Q15 65 25 60 Q32 50 40 60 Q48 55 50 68 L48 75 Z'/%3E%3Cline x1='20' y1='75' x2='48' y2='75'/%3E"
        "%3C!-- Fork & Knife --%3E"
        "%3Cpath d='M78 65 L78 88 M75 65 L75 73 Q75 76 78 76 Q81 76 81 73 L81 65'/%3E"
        "%3Cpath d='M92 65 Q96 68 96 76 L96 88 M92 65 L92 88'/%3E"
        "%3C!-- Bowl with Noodles & Chopsticks --%3E"
        "%3Cpath d='M50 100 Q65 118 80 100 Z'/%3E%3Cpath d='M48 100 Q65 96 82 100'/%3E%3Cline x1='45' y1='90' x2='85' y2='108'/%3E"
        "%3C!-- Carrot --%3E"
        "%3Cpath d='M10 105 L22 93 Q25 96 22 99 Z'/%3E%3Cpath d='M22 93 L26 89 M23 95 L28 94'/%3E"
        "%3C/g%3E%3C/svg%3E"
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🍳 SavorAI - Recipe Kitchen</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #fef9f3;
            background-image: url("{food_pattern}");
            background-repeat: repeat;
            color: #2b2320;
            margin: 0;
            padding: 30px 16px;
            min-height: 100vh;
            position: relative;
        }}

        /* Floating food emojis scattered across the canvas */
        .food-doodle {{
            position: fixed;
            font-size: 38px;
            opacity: 0.35;
            user-select: none;
            pointer-events: none;
            animation: floatSlow 7s ease-in-out infinite alternate;
            z-index: 0;
        }}
        .d1 {{ top: 40px; left: 35px; animation-duration: 6s; }}
        .d2 {{ top: 120px; right: 50px; animation-duration: 8s; }}
        .d3 {{ bottom: 120px; left: 45px; animation-duration: 7s; }}
        .d4 {{ bottom: 80px; right: 60px; animation-duration: 9s; }}
        .d5 {{ top: 48%; left: 15px; animation-duration: 6.5s; }}
        .d6 {{ top: 42%; right: 25px; animation-duration: 7.5s; }}

        @keyframes floatSlow {{
            0% {{ transform: translateY(0px) rotate(0deg); }}
            100% {{ transform: translateY(-16px) rotate(8deg); }}
        }}

        .wrapper {{
            position: relative;
            z-index: 1;
            max-width: 820px;
            margin: 0 auto;
        }}

        .header {{
            text-align: center;
            margin-bottom: 24px;
        }}

        .logo-tag {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #ffe3d1;
            color: #d9480f;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            border: 2px dashed #f76707;
            margin-bottom: 12px;
        }}

        h1 {{
            font-size: 42px;
            font-weight: 800;
            color: #1e130c;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }}

        h1 span.script {{
            font-family: 'Caveat', cursive;
            color: #d9480f;
            font-size: 50px;
            font-weight: 700;
        }}

        p.subtitle {{
            color: #795548;
            font-size: 16px;
            margin: 8px 0 0;
            font-weight: 500;
        }}

        /* Main Card */
        .card {{
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(10px);
            border: 3px solid #f6d8c8;
            border-radius: 24px;
            padding: 32px 36px;
            box-shadow: 0 16px 40px rgba(186, 74, 30, 0.08), 0 2px 8px rgba(0,0,0,0.03);
            position: relative;
        }}

        .card::before {{
            content: '🍕  🍔  🍜  🌮  🥗  🍣  🥞  🥑  🍩';
            position: absolute;
            top: -15px;
            left: 50%;
            transform: translateX(-50%);
            background: #fff;
            padding: 2px 18px;
            border-radius: 20px;
            border: 2px solid #f6d8c8;
            font-size: 15px;
            letter-spacing: 4px;
        }}

        /* Search Form */
        form {{
            display: flex;
            gap: 12px;
            margin-top: 14px;
            margin-bottom: 20px;
        }}

        .input-group {{
            flex: 1;
            position: relative;
        }}

        .input-group input {{
            width: 100%;
            padding: 16px 20px 16px 48px;
            font-size: 17px;
            font-family: inherit;
            border: 2px solid #e9ecef;
            border-radius: 14px;
            outline: none;
            background: #fff;
            color: #2b2320;
            transition: all 0.2s ease;
        }}

        .input-group input:focus {{
            border-color: #d9480f;
            box-shadow: 0 0 0 4px rgba(217, 72, 15, 0.12);
        }}

        .input-icon {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 20px;
            pointer-events: none;
        }}

        button.cook-btn {{
            padding: 16px 30px;
            background: linear-gradient(135deg, #f76707 0%, #d9480f 100%);
            color: #fff;
            font-size: 17px;
            font-weight: 700;
            font-family: inherit;
            border: none;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.2s;
            box-shadow: 0 6px 18px rgba(217, 72, 15, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }}

        button.cook-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(217, 72, 15, 0.4);
        }}

        /* Quick Inspiration Badges */
        .quick-tags {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 8px;
            margin-bottom: 24px;
            font-size: 13px;
            color: #8c6b5e;
        }}
        .tag-pill {{
            background: #fff3ec;
            color: #c92a2a;
            border: 1px solid #ffd8a8;
            padding: 4px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.15s;
        }}
        .tag-pill:hover {{
            background: #ffe3d1;
            transform: scale(1.04);
        }}

        /* Recipe Box */
        .recipe-box {{
            border-top: 2px dashed #f6d8c8;
            padding-top: 28px;
            margin-top: 10px;
            line-height: 1.7;
        }}

        .recipe-box h1, .recipe-box h2, .recipe-box h3 {{
            color: #1e130c;
            margin-top: 24px;
            margin-bottom: 12px;
            font-weight: 700;
        }}

        .recipe-box h2 {{
            border-bottom: 2px solid #ffe3d1;
            padding-bottom: 8px;
            font-size: 24px;
        }}

        .recipe-box hr {{
            border: none;
            border-top: 1px dashed #ffd8a8;
            margin: 24px 0;
        }}

        /* Ingredients Table */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #ffd8a8;
        }}

        th {{
            background: #ffe3d1;
            color: #a61e4d;
            font-weight: 700;
            padding: 12px 16px;
            text-align: left;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        td {{
            padding: 12px 16px;
            border-top: 1px solid #fff0e6;
            background: #fffcf9;
            font-size: 15px;
        }}

        tr:nth-child(even) td {{
            background: #fff8f3;
        }}

        ol, ul {{
            padding-left: 24px;
        }}

        li {{
            margin-bottom: 10px;
        }}

        strong {{
            color: #c92a2a;
        }}

        /* Footer */
        .footer {{
            text-align: center;
            margin-top: 24px;
            color: #9c7b6d;
            font-size: 13px;
            font-weight: 500;
        }}
    </style>
</head>
<body>
    <!-- Floating food emojis around canvas -->
    <div class="food-doodle d1">🍕</div>
    <div class="food-doodle d2">🥑</div>
    <div class="food-doodle d3">🍔</div>
    <div class="food-doodle d4">🍜</div>
    <div class="food-doodle d5">🌮</div>
    <div class="food-doodle d6">🍣</div>

    <div class="wrapper">
        <div class="header">
            <div class="logo-tag">✨ Chef's Secret Recipe Book</div>
            <h1>🍳 Savor<span class="script">Kitchen</span></h1>
            <p class="subtitle">Type any dish name below — we'll whip up your personalized recipe in seconds!</p>
        </div>

        <div class="card">
            <form method="post" action="/recipe">
                <div class="input-group">
                    <span class="input-icon">🍽️</span>
                    <input type="text" name="dish" id="dishInput" placeholder="e.g., Paneer Butter Masala, Creamy Carbonara, Tacos..." value="{dish_val}" required autofocus />
                </div>
                <button type="submit" class="cook-btn">👨‍🍳 Cook It!</button>
            </form>

            <div class="quick-tags">
                <span>💡 Quick picks:</span>
                <span class="tag-pill" onclick="pickDish('Butter Chicken')">🍗 Butter Chicken</span>
                <span class="tag-pill" onclick="pickDish('Pasta Carbonara')">🍝 Pasta Carbonara</span>
                <span class="tag-pill" onclick="pickDish('Crispy Falafel Bowl')">🧆 Crispy Falafel</span>
                <span class="tag-pill" onclick="pickDish('Classic Fluffy Pancakes')">🥞 Fluffy Pancakes</span>
                <span class="tag-pill" onclick="pickDish('Biryani')">🍚 Dum Biryani</span>
            </div>

            {recipe_content}
        </div>

        <div class="footer">
            🥖 🧀 🍓 Handcrafted with love for foodies & home chefs everywhere 🌶️ 🍋 🧄
        </div>
    </div>

    <script>
        function pickDish(name) {{
            const input = document.getElementById('dishInput');
            input.value = name;
            input.form.submit();
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
        box = '<div class="recipe-box" style="color: red;">⚠️ Error: GROQ_API_KEY environment variable is not set in Vercel settings.</div>'
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Give me a complete recipe for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a fun, friendly professional chef. When given a dish name, generate a clear, "
                        "easy-to-follow recipe formatted in markdown. Include:\n"
                        "1. Dish Name & brief mouthwatering description with emojis\n"
                        "2. Prep Time, Cook Time, and Servings (in a markdown table)\n"
                        "3. Ingredients list with measurements (in a markdown table)\n"
                        "4. Step-by-step numbered cooking instructions\n"
                        "5. A pro chef secret tip"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        recipe_md = response.choices[0].message.content
        html_recipe = md.render(recipe_md)
        box = f'<div class="recipe-box">{html_recipe}</div>'
    except Exception as e:
        box = f'<div class="recipe-box" style="color: red;">⚠️ Error: {e}</div>'
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
