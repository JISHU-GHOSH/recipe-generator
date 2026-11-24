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
app = FastAPI(title="Savor - Taste the Moment")

def render_page(dish_val: str = "", recipe_content: str = "") -> str:
    scroll_script = "<script>window.location.hash = 'kitchen-pass';</script>" if recipe_content else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Savor — Intelligent Culinary Studio</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-obsidian: #09090B;
            --bg-card: #141417;
            --brand-green: #06C167;
            --brand-green-hover: #05A357;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(6, 193, 103, 0.5);
            --text-pure: #FFFFFF;
            --text-dim: #A1A1AA;
            --text-faint: #71717A;
            --radius-pill: 9999px;
            --radius-tile: 20px;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-obsidian);
            color: var(--text-pure);
            -webkit-font-smoothing: antialiased;
            overflow-x: hidden;
        }}

        /* ==========================================================================
           1. TOP ANNOUNCEMENT BANNER
           ========================================================================== */
        .top-banner {{
            background: #000000;
            color: #FFFFFF;
            font-size: 13px;
            font-weight: 600;
            padding: 10px 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            letter-spacing: -0.01em;
            position: relative;
            z-index: 101;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }}

        .top-banner span.promo-badge {{
            background: var(--brand-green);
            color: #000000;
            font-size: 11px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: var(--radius-pill);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        /* ==========================================================================
           2. CINEMATIC OVERLAID NAVIGATION
           ========================================================================== */
        .brand-nav {{
            position: absolute;
            top: 38px;
            left: 0;
            right: 0;
            z-index: 100;
            background: transparent;
            padding: 18px 48px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand-logo {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
            text-shadow: 0 2px 10px rgba(0,0,0,0.6);
        }}

        .brand-logo .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--brand-green);
            box-shadow: 0 0 12px var(--brand-green);
        }}

        .nav-switchers {{
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: var(--radius-pill);
            padding: 4px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }}

        .nav-switcher-btn {{
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            background: transparent;
            color: rgba(255, 255, 255, 0.8);
            transition: all 0.15s ease;
        }}

        .nav-switcher-btn.active {{
            background: #FFFFFF;
            color: #000000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }}

        .nav-cta {{
            background: rgba(255, 255, 255, 0.12);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 9px 22px;
            border-radius: var(--radius-pill);
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 700;
            transition: all 0.2s ease;
        }}

        .nav-cta:hover {{
            background: var(--brand-green);
            color: #FFFFFF;
            border-color: var(--brand-green);
        }}

        /* ==========================================================================
           3. CINEMATIC FULL-BLEED FOOD HERO WITH SEAMLESS BLEND
           ========================================================================== */
        .cinematic-hero {{
            position: relative;
            min-height: 580px;
            padding: 160px 32px 100px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--bg-obsidian);
            overflow: hidden;
        }}

        .hero-bg-media {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center 60%;
            filter: brightness(0.65) contrast(1.1);
            transform: scale(1.02);
        }}

        .hero-cinematic-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to bottom,
                rgba(9, 9, 11, 0.75) 0%,
                rgba(9, 9, 11, 0.28) 40%,
                rgba(9, 9, 11, 0.8) 75%,
                #09090B 100%
            );
            pointer-events: none;
        }}

        .hero-container {{
            position: relative;
            z-index: 2;
            max-width: 860px;
            width: 100%;
            margin: 0 auto;
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 22px;
        }}

        .hero-badge-tag {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 18px;
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.22);
            color: #FFFFFF;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.02em;
        }}

        .hero-title {{
            font-size: 64px;
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: #FFFFFF;
            margin: 0;
            text-shadow: 0 4px 30px rgba(0, 0, 0, 0.7);
        }}

        .hero-title span.accent {{
            color: var(--brand-green);
        }}

        .hero-desc {{
            font-size: 19px;
            line-height: 1.5;
            color: rgba(255, 255, 255, 0.85);
            margin: 0;
            max-width: 620px;
            text-shadow: 0 2px 12px rgba(0,0,0,0.6);
        }}

        /* Elevated Search Input */
        .search-container {{
            width: 100%;
            max-width: 780px;
            margin-top: 10px;
            background: #FFFFFF;
            border-radius: var(--radius-pill);
            padding: 7px 7px 7px 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), 0 0 0 1px rgba(255, 255, 255, 0.3);
            display: flex;
            align-items: center;
            gap: 12px;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .search-container:focus-within {{
            box-shadow: 0 24px 64px rgba(6, 193, 103, 0.4), 0 0 0 3px var(--brand-green);
            transform: translateY(-2px);
        }}

        .search-icon-svg {{
            width: 22px;
            height: 22px;
            stroke: #2C2C2E;
            fill: none;
            stroke-width: 2.2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}

        .search-field {{
            flex: 1;
            border: none;
            outline: none;
            font-family: inherit;
            font-size: 17px;
            font-weight: 600;
            color: #0F0F0F;
            background: transparent;
        }}

        .search-field::placeholder {{
            color: #8E8E93;
            font-weight: 500;
        }}

        .cook-action-btn {{
            background: var(--brand-green);
            color: #FFFFFF;
            border: none;
            padding: 16px 36px;
            border-radius: var(--radius-pill);
            font-family: inherit;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .cook-action-btn:hover {{
            background: var(--brand-green-hover);
            transform: scale(0.98);
        }}

        .quick-searches {{
            display: flex;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            font-size: 13.5px;
            color: rgba(255, 255, 255, 0.85);
            margin-top: 4px;
        }}

        .quick-tag {{
            background: rgba(255, 255, 255, 0.14);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            font-weight: 600;
            transition: all 0.15s;
        }}

        .quick-tag:hover {{
            background: #FFFFFF;
            color: #000000;
            transform: translateY(-1px);
        }}

        /* ==========================================================================
           4. OPTION 2: FULL-PHOTO CINEMATIC TILES (NO CLUNKY TEXT BOXES)
           ========================================================================== */
        .showcase-section {{
            max-width: 1240px;
            margin: 20px auto 70px;
            padding: 0 40px;
            position: relative;
            z-index: 5;
        }}

        .showcase-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 28px;
            padding-bottom: 18px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .showcase-title {{
            font-size: 28px;
            font-weight: 800;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            margin: 0;
        }}

        .showcase-subtitle {{
            font-size: 15px;
            color: var(--text-dim);
            margin: 6px 0 0;
        }}

        .showcase-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 28px;
        }}

        .cinematic-tile {{
            position: relative;
            aspect-ratio: 16 / 11;
            border-radius: var(--radius-tile);
            overflow: hidden;
            cursor: pointer;
            border: 1px solid var(--border-subtle);
            background: #000000;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
        }}

        .cinematic-tile:hover {{
            transform: translateY(-6px);
            border-color: var(--border-hover);
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.7), 0 0 0 1px var(--border-hover);
        }}

        .tile-img {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1), filter 0.6s ease;
            filter: brightness(0.88);
        }}

        .cinematic-tile:hover .tile-img {{
            transform: scale(1.06);
            filter: brightness(0.98);
        }}

        /* Subtle dark gradient overlay covering bottom half */
        .tile-gradient-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0.15) 0%,
                rgba(0, 0, 0, 0.15) 35%,
                rgba(9, 9, 11, 0.82) 75%,
                rgba(9, 9, 11, 0.98) 100%
            );
            pointer-events: none;
        }}

        /* Top floating frosted pills */
        .tile-top-badges {{
            position: absolute;
            top: 16px;
            left: 16px;
            right: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 2;
            pointer-events: none;
        }}

        .tile-badge {{
            background: rgba(10, 10, 14, 0.72);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: #FFFFFF;
            padding: 5px 12px;
            border-radius: var(--radius-pill);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .tile-badge.accent {{
            background: var(--brand-green);
            color: #000000;
            border-color: transparent;
        }}

        /* Integrated Bottom Content on the photo */
        .tile-bottom-content {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 24px 22px;
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .tile-title {{
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            margin: 0;
            letter-spacing: -0.02em;
            line-height: 1.25;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.8);
        }}

        .tile-desc {{
            font-size: 13.5px;
            color: rgba(255, 255, 255, 0.78);
            margin: 0;
            line-height: 1.45;
            text-shadow: 0 1px 4px rgba(0, 0, 0, 0.8);
        }}

        .tile-action-row {{
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--brand-green);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.01em;
            transition: gap 0.2s ease;
        }}

        .cinematic-tile:hover .tile-action-row {{
            gap: 10px;
        }}

        /* ==========================================================================
           5. RECIPE OUTPUT SECTION (CHEF PASS)
           ========================================================================== */
        .recipe-section {{
            max-width: 940px;
            margin: 40px auto 80px;
            padding: 0 24px;
        }}

        .recipe-card-brand {{
            background: var(--bg-card);
            border-radius: var(--radius-tile);
            box-shadow: 0 30px 70px rgba(0, 0, 0, 0.6);
            overflow: hidden;
            border: 1px solid var(--border-subtle);
            animation: popIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes popIn {{
            from {{ opacity: 0; transform: translateY(24px) scale(0.98); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        .recipe-header-bar {{
            background: #0E0E10;
            color: #FFFFFF;
            padding: 18px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .recipe-header-badge {{
            font-size: 13px;
            font-weight: 700;
            color: var(--brand-green);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .copy-btn-brand {{
            background: rgba(255, 255, 255, 0.1);
            color: #FFF;
            border: 1px solid rgba(255, 255, 255, 0.15);
            padding: 8px 20px;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s;
            font-family: inherit;
        }}

        .copy-btn-brand:hover {{
            background: var(--brand-green);
            color: #000000;
            border-color: var(--brand-green);
        }}

        .recipe-main-body {{
            padding: 44px;
            line-height: 1.7;
            font-size: 16px;
            color: #D4D4D8;
        }}

        .recipe-main-body h1 {{
            font-size: 36px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0 0 12px;
            color: #FFFFFF;
        }}

        .recipe-main-body h2 {{
            font-size: 20px;
            font-weight: 800;
            margin: 36px 0 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border-subtle);
            color: #FFFFFF;
        }}

        .recipe-main-body hr {{
            border: none;
            border-top: 1px solid var(--border-subtle);
            margin: 32px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 22px 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-subtle);
        }}

        th {{
            background: #1F1F24;
            color: #FFFFFF;
            font-size: 13.5px;
            font-weight: 700;
            padding: 14px 20px;
            text-align: left;
            border-bottom: 1px solid var(--border-subtle);
        }}

        td {{
            padding: 14px 20px;
            border-top: 1px solid var(--border-subtle);
            font-size: 14.5px;
            color: #E4E4E7;
            background: rgba(24, 24, 28, 0.5);
        }}

        ol, ul {{
            padding-left: 24px;
        }}

        li {{
            margin-bottom: 14px;
        }}

        /* ==========================================================================
           6. FOOTER
           ========================================================================== */
        .brand-footer {{
            background: #050507;
            color: #FFFFFF;
            padding: 56px 40px 40px;
            border-top: 1px solid var(--border-subtle);
        }}

        .footer-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-subtle);
            padding-bottom: 32px;
        }}

        .footer-brand {{
            font-size: 26px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.03em;
        }}

        .footer-copy {{
            max-width: 1240px;
            margin: 24px auto 0;
            font-size: 13px;
            color: var(--text-faint);
            display: flex;
            justify-content: space-between;
        }}

        @media (max-width: 960px) {{
            .showcase-grid {{ grid-template-columns: 1fr; }}
            .hero-title {{ font-size: 44px; }}
            .brand-nav, .showcase-section {{ padding-left: 20px; padding-right: 20px; }}
            .nav-switchers {{ display: none; }}
        }}

        @media (max-width: 640px) {{
            .hero-title {{ font-size: 36px; }}
        }}
    </style>
</head>
<body>
    <!-- 1. Top Announcement Ticker -->
    <div class="top-banner">
        <span class="promo-badge">PRO V2.5</span>
        <span>Generate calibrated chef recipes with exact gram measurements in seconds</span>
    </div>

    <!-- 2. Cinematic Overlaid Brand Navigation Bar -->
    <nav class="brand-nav">
        <a href="/" class="brand-logo">
            Savor<span class="dot"></span>
        </a>

        <div class="nav-switchers">
            <button class="nav-switcher-btn active">Chef Studio</button>
            <button class="nav-switcher-btn">15-Min Dinners</button>
            <button class="nav-switcher-btn">High-Protein</button>
        </div>

        <a href="#showcase" class="nav-cta">Featured Dishes</a>
    </nav>

    <!-- 3. Cinematic Food Photography Hero With Continuous Dark Fade -->
    <header class="cinematic-hero">
        <img 
            src="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=2000&q=85" 
            alt="Sizzling Gourmet Feast" 
            class="hero-bg-media"
        />
        <div class="hero-cinematic-overlay"></div>

        <div class="hero-container">
            <div class="hero-badge-tag">Curated Culinary Intelligence</div>
            <h1 class="hero-title">
                Cook like a restaurant chef.<br>
                Starting with your <span class="accent">craving.</span>
            </h1>
            <p class="hero-desc">
                Type any dish name below. Savor immediately calculates precise measurements, prep times, and step-by-step master techniques.
            </p>

            <form method="post" action="/recipe" class="search-container">
                <svg class="search-icon-svg" viewBox="0 0 24 24">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input 
                    type="text" 
                    name="dish" 
                    id="dishInput" 
                    class="search-field" 
                    placeholder="What would you like to cook? (e.g. Truffle Tagliatelle, Ribeye Steak...)" 
                    value="{dish_val}" 
                    required 
                    autocomplete="off"
                    autofocus
                />
                <button type="submit" class="cook-action-btn">Get Recipe</button>
            </form>

            <div class="quick-searches">
                <span>Trending:</span>
                <span class="quick-tag" onclick="quickOrder('Truffle Tagliatelle')">Truffle Tagliatelle</span>
                <span class="quick-tag" onclick="quickOrder('Garlic Herb Ribeye')">Ribeye Steak</span>
                <span class="quick-tag" onclick="quickOrder('Pan-Seared Scallops')">Pan-Seared Scallops</span>
                <span class="quick-tag" onclick="quickOrder('Spicy Thai Basil Chicken')">Thai Basil Chicken</span>
                <span class="quick-tag" onclick="quickOrder('Murgh Makhani')">Butter Chicken</span>
            </div>
        </div>
    </header>

    <!-- 4. Option 2: Full-Photo Cinematic Tiles (No Clunky Boxes) -->
    <main class="showcase-section" id="showcase">
        <div class="showcase-header">
            <div>
                <h2 class="showcase-title">Trending Chef Creations</h2>
                <p class="showcase-subtitle">Hand-picked culinary masterclasses ready to cook tonight</p>
            </div>
        </div>

        <div class="showcase-grid">
            <!-- Tile 1 -->
            <div class="cinematic-tile" onclick="quickOrder('Garlic Herb Basted Prime Ribeye')">
                <img src="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1000&q=80" alt="Prime Ribeye" class="tile-img">
                <div class="tile-gradient-overlay"></div>
                <div class="tile-top-badges">
                    <span class="tile-badge accent">15 Min Prep</span>
                    <span class="tile-badge">Steakhouse</span>
                </div>
                <div class="tile-bottom-content">
                    <h3 class="tile-title">Garlic Herb Basted Ribeye</h3>
                    <p class="tile-desc">Cast-iron seared ribeye basted with foaming rosemary, thyme & cracked garlic butter.</p>
                    <div class="tile-action-row">Generate Recipe →</div>
                </div>
            </div>

            <!-- Tile 2 -->
            <div class="cinematic-tile" onclick="quickOrder('Truffle Tagliatelle with Wild Mushrooms')">
                <img src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80" alt="Truffle Tagliatelle" class="tile-img">
                <div class="tile-gradient-overlay"></div>
                <div class="tile-top-badges">
                    <span class="tile-badge accent">20 Min Prep</span>
                    <span class="tile-badge">Italian</span>
                </div>
                <div class="tile-bottom-content">
                    <h3 class="tile-title">Truffle Tagliatelle</h3>
                    <p class="tile-desc">Silky hand-rolled pasta, pan-roasted forest chanterelles & shaved black truffle.</p>
                    <div class="tile-action-row">Generate Recipe →</div>
                </div>
            </div>

            <!-- Tile 3 -->
            <div class="cinematic-tile" onclick="quickOrder('Pan-Seared Jumbo Scallops in Lemon Butter')">
                <img src="https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=1000&q=80" alt="Pan-Seared Scallops" class="tile-img">
                <div class="tile-gradient-overlay"></div>
                <div class="tile-top-badges">
                    <span class="tile-badge accent">12 Min Prep</span>
                    <span class="tile-badge">Seafood</span>
                </div>
                <div class="tile-bottom-content">
                    <h3 class="tile-title">Pan-Seared Scallops</h3>
                    <p class="tile-desc">Golden crusted sea scallops with garlic cauliflower puree, lemon butter & microgreens.</p>
                    <div class="tile-action-row">Generate Recipe →</div>
                </div>
            </div>
        </div>
    </main>

    <!-- 5. Recipe Output Section (Chef Pass) -->
    <div id="kitchen-pass" class="recipe-section">
        {recipe_content}
    </div>

    <!-- 6. Brand Footer -->
    <footer class="brand-footer">
        <div class="footer-inner">
            <div class="footer-brand">Savor.</div>
            <div style="font-size: 14px; color: var(--text-dim);">Intelligent culinary engineering for every kitchen.</div>
        </div>
        <div class="footer-copy">
            <span>© 2026 Savor Studio Inc. All rights reserved.</span>
            <span>Crafted for true food lovers. Zero compromises.</span>
        </div>
    </footer>

    <script>
        function quickOrder(dishName) {{
            const input = document.getElementById('dishInput');
            input.value = dishName;
            document.querySelector('.search-container').submit();
        }}

        function copyRecipeText() {{
            const body = document.querySelector('.recipe-main-body');
            if (body) {{
                navigator.clipboard.writeText(body.innerText).then(() => {{
                    const btn = document.getElementById('copyRecipeBtn');
                    if (btn) {{
                        btn.innerHTML = 'Copied to Clipboard';
                        setTimeout(() => {{ btn.innerHTML = 'Copy Recipe'; }}, 2000);
                    }}
                }});
            }}
        }}
    </script>
    {scroll_script}
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
        <div class="recipe-card-brand">
            <div class="recipe-header-bar">
                <div class="recipe-header-badge">Notice</div>
            </div>
            <div class="recipe-main-body" style="color: #FF5A36;">
                GROQ_API_KEY environment variable is not set.
            </div>
        </div>
        '''
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Give me a professional, complete step-by-step recipe for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an acclaimed executive restaurant chef. When given a dish name, "
                        "craft an immaculate, elegant, step-by-step master recipe in markdown. "
                        "Do NOT use any emojis anywhere.\n\n"
                        "Format your response cleanly with the following sections:\n"
                        "1. Dish Name (h1) with a brief 1-sentence intro\n"
                        "2. Prep & Cook Times table (Prep Time, Cook Time, Total Time, Servings)\n"
                        "3. Ingredients table (Ingredient, Quantity, Chef Notes)\n"
                        "4. Numbered Step-by-Step Instructions\n"
                        "5. Executive Chef's Secret Technique"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        recipe_md = response.choices[0].message.content
        html_recipe = md.render(recipe_md)
        box = f'''
        <div class="recipe-card-brand">
            <div class="recipe-header-bar">
                <div class="recipe-header-badge">Chef Pass Recipe</div>
                <button class="copy-btn-brand" id="copyRecipeBtn" onclick="copyRecipeText()">Copy Recipe</button>
            </div>
            <div class="recipe-main-body">{html_recipe}</div>
        </div>
        '''
    except Exception as e:
        box = f'''
        <div class="recipe-card-brand">
            <div class="recipe-header-bar">
                <div class="recipe-header-badge">Error</div>
            </div>
            <div class="recipe-main-body" style="color: #FF5A36;">Error: {e}</div>
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
