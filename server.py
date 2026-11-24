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
    <title>Savor — Good Food Made Effortless</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --brand-green: #06C167;
            --brand-green-hover: #05A357;
            --surface-white: #FFFFFF;
            --surface-soft: #F8F9FA;
            --ink-black: #0F0F0F;
            --ink-charcoal: #2C2C2E;
            --ink-muted: #6E6E6E;
            --ink-faint: #A0A0A0;
            --border-light: rgba(0, 0, 0, 0.08);
            --shadow-card: 0 4px 16px rgba(0, 0, 0, 0.05);
            --shadow-hover: 0 16px 36px rgba(0, 0, 0, 0.12);
            --radius-pill: 9999px;
            --radius-card: 18px;
        }}

        * {{
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }}

        body {{
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--surface-soft);
            color: var(--ink-black);
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
            padding: 9px 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            letter-spacing: -0.01em;
            position: relative;
            z-index: 101;
        }}

        .top-banner span.promo-badge {{
            background: var(--brand-green);
            color: #000000;
            font-size: 11px;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: var(--radius-pill);
            text-transform: uppercase;
        }}

        /* ==========================================================================
           2. CINEMATIC OVERLAID NAVIGATION
           ========================================================================== */
        .brand-nav {{
            position: absolute;
            top: 36px;
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
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
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
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: var(--radius-pill);
            padding: 4px;
            border: 1px solid rgba(255, 255, 255, 0.25);
        }}

        .nav-switcher-btn {{
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            background: transparent;
            color: rgba(255, 255, 255, 0.85);
            transition: all 0.15s ease;
        }}

        .nav-switcher-btn.active {{
            background: #FFFFFF;
            color: var(--ink-black);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }}

        .nav-cta {{
            background: #FFFFFF;
            color: #000000;
            padding: 10px 24px;
            border-radius: var(--radius-pill);
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 700;
            transition: transform 0.15s ease, background 0.15s;
            box-shadow: 0 4px 16px rgba(0,0,0,0.25);
        }}

        .nav-cta:hover {{
            background: var(--brand-green);
            color: #FFFFFF;
            transform: scale(0.98);
        }}

        /* ==========================================================================
           3. CINEMATIC FULL-BLEED FOOD HERO
           ========================================================================== */
        .cinematic-hero {{
            position: relative;
            min-height: 560px;
            padding: 150px 32px 90px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #111111;
            overflow: hidden;
        }}

        /* High-res cinematic food backdrop with rich gradient vignette */
        .hero-bg-media {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center 65%;
            filter: brightness(0.72) contrast(1.08);
            transform: scale(1.02);
        }}

        .hero-cinematic-overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to bottom,
                rgba(0, 0, 0, 0.75) 0%,
                rgba(0, 0, 0, 0.35) 40%,
                rgba(0, 0, 0, 0.82) 100%
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
            gap: 20px;
        }}

        .hero-badge-tag {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 6px 18px;
            background: rgba(255, 255, 255, 0.16);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #FFFFFF;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.02em;
        }}

        .hero-title {{
            font-size: 62px;
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: #FFFFFF;
            margin: 0;
            text-shadow: 0 4px 28px rgba(0, 0, 0, 0.6);
        }}

        .hero-title span.accent {{
            color: var(--brand-green);
        }}

        .hero-desc {{
            font-size: 19px;
            line-height: 1.5;
            color: rgba(255, 255, 255, 0.88);
            margin: 0;
            max-width: 620px;
            text-shadow: 0 2px 12px rgba(0,0,0,0.5);
        }}

        /* Elevated High-Impact Search Input */
        .search-container {{
            width: 100%;
            max-width: 780px;
            margin-top: 12px;
            background: #FFFFFF;
            border-radius: var(--radius-pill);
            padding: 7px 7px 7px 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(255, 255, 255, 0.4);
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
            stroke: var(--ink-charcoal);
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
            color: var(--ink-black);
            background: transparent;
        }}

        .search-field::placeholder {{
            color: var(--ink-faint);
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
            margin-top: 6px;
        }}

        .quick-tag {{
            background: rgba(255, 255, 255, 0.18);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.25);
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
           4. UBEREATS CUISINE ROUND THUMBNAIL STRIP
           ========================================================================== */
        .cuisine-subbar {{
            background: #FFFFFF;
            border-bottom: 1px solid var(--border-light);
            padding: 14px 40px;
            overflow-x: auto;
            scrollbar-width: none;
            box-shadow: 0 4px 16px rgba(0,0,0,0.03);
        }}

        .cuisine-subbar::-webkit-scrollbar {{
            display: none;
        }}

        .cuisine-strip {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
        }}

        .cuisine-pill {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            text-decoration: none;
            color: var(--ink-charcoal);
            padding: 4px;
            transition: all 0.18s ease;
            white-space: nowrap;
        }}

        .cuisine-pill:hover {{
            transform: translateY(-2px);
            color: var(--brand-green);
        }}

        .cuisine-pill .thumb-round {{
            width: 50px;
            height: 50px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid var(--border-light);
            background: #FAFAFA;
            transition: border-color 0.18s, transform 0.18s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }}

        .cuisine-pill:hover .thumb-round {{
            border-color: var(--brand-green);
            transform: scale(1.06);
        }}

        .cuisine-pill .thumb-round img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .cuisine-pill .label {{
            font-size: 12px;
            font-weight: 700;
            letter-spacing: -0.01em;
        }}

        /* ==========================================================================
           5. UBEREATS POPULAR FOOD FEED GRID
           ========================================================================== */
        .marketplace-feed {{
            max-width: 1240px;
            margin: 48px auto 0;
            padding: 0 40px;
        }}

        .feed-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 24px;
        }}

        .feed-title {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0;
        }}

        .feed-subtitle {{
            font-size: 14.5px;
            color: var(--ink-muted);
            margin: 4px 0 0;
        }}

        .uber-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 24px;
        }}

        .uber-card {{
            background: var(--surface-white);
            border-radius: var(--radius-card);
            overflow: hidden;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: var(--shadow-card);
            display: flex;
            flex-direction: column;
            border: 1px solid var(--border-light);
        }}

        .uber-card:hover {{
            transform: translateY(-5px);
            box-shadow: var(--shadow-hover);
            border-color: rgba(6, 193, 103, 0.4);
        }}

        .uber-img-wrap {{
            width: 100%;
            aspect-ratio: 16 / 9.5;
            position: relative;
            overflow: hidden;
            background: #EFEFEF;
        }}

        .uber-img-wrap img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
            transition: transform 0.4s ease;
        }}

        .uber-card:hover .uber-img-wrap img {{
            transform: scale(1.05);
        }}

        .uber-tag-promo {{
            position: absolute;
            top: 12px;
            left: 12px;
            background: var(--brand-green);
            color: #FFFFFF;
            padding: 4px 10px;
            border-radius: var(--radius-pill);
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }}

        .uber-badge-time {{
            position: absolute;
            bottom: 12px;
            right: 12px;
            background: #FFFFFF;
            color: var(--ink-black);
            padding: 5px 12px;
            border-radius: var(--radius-pill);
            font-size: 12px;
            font-weight: 700;
            box-shadow: 0 4px 10px rgba(0,0,0,0.12);
        }}

        .uber-details {{
            padding: 16px 18px 20px;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .uber-title-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .uber-dish-name {{
            font-size: 17px;
            font-weight: 800;
            color: var(--ink-black);
            margin: 0;
            letter-spacing: -0.02em;
        }}

        .uber-rating-badge {{
            background: rgba(0, 0, 0, 0.05);
            color: var(--ink-black);
            font-size: 12.5px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .uber-rating-badge span.star {{
            color: #E29500;
        }}

        .uber-meta-row {{
            font-size: 13.5px;
            color: var(--ink-muted);
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .uber-dot {{
            width: 3px;
            height: 3px;
            border-radius: 50%;
            background: var(--ink-muted);
        }}

        /* ==========================================================================
           6. RECIPE OUTPUT SECTION
           ========================================================================== */
        .recipe-section {{
            max-width: 900px;
            margin: 56px auto;
            padding: 0 24px;
        }}

        .recipe-card-brand {{
            background: #FFFFFF;
            border-radius: var(--radius-card);
            box-shadow: 0 24px 60px -12px rgba(0, 0, 0, 0.16);
            overflow: hidden;
            border: 1px solid var(--border-light);
            animation: popIn 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        @keyframes popIn {{
            from {{ opacity: 0; transform: translateY(24px) scale(0.98); }}
            to {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        .recipe-header-bar {{
            background: var(--ink-black);
            color: #FFFFFF;
            padding: 18px 32px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .recipe-header-badge {{
            font-size: 13px;
            font-weight: 700;
            color: var(--brand-green);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .copy-btn-brand {{
            background: rgba(255, 255, 255, 0.15);
            color: #FFF;
            border: none;
            padding: 7px 18px;
            border-radius: var(--radius-pill);
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            transition: background 0.15s;
            font-family: inherit;
        }}

        .copy-btn-brand:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}

        .recipe-main-body {{
            padding: 44px;
            line-height: 1.7;
            font-size: 16px;
            color: var(--ink-charcoal);
        }}

        .recipe-main-body h1 {{
            font-size: 36px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0 0 12px;
            color: var(--ink-black);
        }}

        .recipe-main-body h2 {{
            font-size: 20px;
            font-weight: 800;
            margin: 32px 0 14px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--surface-soft);
            color: var(--ink-black);
        }}

        .recipe-main-body hr {{
            border: none;
            border-top: 1px solid var(--border-light);
            margin: 28px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-light);
        }}

        th {{
            background: var(--surface-soft);
            color: var(--ink-black);
            font-size: 13px;
            font-weight: 700;
            padding: 13px 18px;
            text-align: left;
        }}

        td {{
            padding: 14px 18px;
            border-top: 1px solid var(--border-light);
            font-size: 14.5px;
        }}

        ol, ul {{
            padding-left: 24px;
        }}

        li {{
            margin-bottom: 12px;
        }}

        /* ==========================================================================
           7. FOOTER
           ========================================================================== */
        .brand-footer {{
            background: var(--ink-black);
            color: #FFFFFF;
            padding: 56px 40px 40px;
            margin-top: 88px;
        }}

        .footer-inner {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.12);
            padding-bottom: 36px;
        }}

        .footer-brand {{
            font-size: 26px;
            font-weight: 800;
            color: #FFFFFF;
        }}

        .footer-copy {{
            max-width: 1240px;
            margin: 28px auto 0;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.4);
            display: flex;
            justify-content: space-between;
        }}

        @media (max-width: 960px) {{
            .uber-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .hero-title {{ font-size: 42px; }}
            .brand-nav, .cuisine-subbar, .marketplace-feed {{ padding-left: 20px; padding-right: 20px; }}
            .nav-switchers {{ display: none; }}
        }}

        @media (max-width: 640px) {{
            .uber-grid {{ grid-template-columns: 1fr; }}
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
            <button class="nav-switcher-btn active">Home Cooking</button>
            <button class="nav-switcher-btn">15-Min Quick</button>
            <button class="nav-switcher-btn">Healthy & Keto</button>
        </div>

        <a href="#popular" class="nav-cta">Cook Tonight</a>
    </nav>

    <!-- 3. Cinematic Food Photography Hero -->
    <header class="cinematic-hero">
        <img 
            src="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=2000&q=85" 
            alt="Sizzling Gourmet Feast" 
            class="hero-bg-media"
        />
        <div class="hero-cinematic-overlay"></div>

        <div class="hero-container">
            <div class="hero-badge-tag">Curated Kitchen Intelligence</div>
            <h1 class="hero-title">
                Order from your fridge.<br>
                Cook like a <span class="accent">pro.</span>
            </h1>
            <p class="hero-desc">
                Enter any dish name. Savor immediately calculates exact measurements, restaurant techniques, and step-by-step instructions.
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
                    placeholder="What do you feel like eating? (e.g. Butter Chicken, Carbonara...)" 
                    value="{dish_val}" 
                    required 
                    autocomplete="off"
                    autofocus
                />
                <button type="submit" class="cook-action-btn">Get Recipe</button>
            </form>

            <div class="quick-searches">
                <span>Popular:</span>
                <span class="quick-tag" onclick="quickOrder('Butter Chicken')">Butter Chicken</span>
                <span class="quick-tag" onclick="quickOrder('Pasta Carbonara')">Carbonara</span>
                <span class="quick-tag" onclick="quickOrder('Falafel Bowl')">Falafel Bowl</span>
                <span class="quick-tag" onclick="quickOrder('Fluffy Pancakes')">Pancakes</span>
                <span class="quick-tag" onclick="quickOrder('Tacos al Pastor')">Tacos</span>
            </div>
        </div>
    </header>

    <!-- 4. Clean Cuisine Photo Strip -->
    <div class="cuisine-subbar">
        <div class="cuisine-strip">
            <div class="cuisine-pill" onclick="quickOrder('Pizza Margherita')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=120&q=80" alt="Pizza"></div>
                <span class="label">Pizza</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Smash Cheeseburger')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=120&q=80" alt="Burgers"></div>
                <span class="label">Burgers</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Pasta Carbonara')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=120&q=80" alt="Italian"></div>
                <span class="label">Italian</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Chicken Biryani')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=120&q=80" alt="Indian"></div>
                <span class="label">Indian</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Street Tacos')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=120&q=80" alt="Mexican"></div>
                <span class="label">Mexican</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Tonkotsu Ramen')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=120&q=80" alt="Ramen"></div>
                <span class="label">Ramen</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Salmon Sushi Roll')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1579871494447-9811cf80d66c?auto=format&fit=crop&w=120&q=80" alt="Japanese"></div>
                <span class="label">Japanese</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Mediterranean Salad')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=120&q=80" alt="Healthy"></div>
                <span class="label">Healthy</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Fluffy Blueberry Pancakes')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=120&q=80" alt="Breakfast"></div>
                <span class="label">Breakfast</span>
            </div>
            <div class="cuisine-pill" onclick="quickOrder('Chocolate Glazed Donut')">
                <div class="thumb-round"><img src="https://images.unsplash.com/photo-1527515862127-a4fc05baf7a5?auto=format&fit=crop&w=120&q=80" alt="Desserts"></div>
                <span class="label">Desserts</span>
            </div>
        </div>
    </div>

    <!-- 5. UberEats-Style Popular Food Feed Grid -->
    <main class="marketplace-feed" id="popular">
        <div class="feed-header">
            <div>
                <h2 class="feed-title">Popular Dishes to Cook Tonight</h2>
                <p class="feed-subtitle">Select any dish card below to generate your custom chef recipe</p>
            </div>
        </div>

        <div class="uber-grid">
            <!-- Card 1 -->
            <div class="uber-card" onclick="quickOrder('Butter Chicken with Garlic Naan')">
                <div class="uber-img-wrap">
                    <img src="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=800&q=80" alt="Butter Chicken">
                    <div class="uber-tag-promo">Top Rated</div>
                    <div class="uber-badge-time">35 min</div>
                </div>
                <div class="uber-details">
                    <div class="uber-title-row">
                        <h3 class="uber-dish-name">Murgh Makhani (Butter Chicken)</h3>
                        <div class="uber-rating-badge"><span class="star">★</span> 4.9</div>
                    </div>
                    <div class="uber-meta-row">
                        <span>North Indian</span>
                        <span class="uber-dot"></span>
                        <span>Rich Tomato & Fenugreek Gravy</span>
                    </div>
                </div>
            </div>

            <!-- Card 2 -->
            <div class="uber-card" onclick="quickOrder('Classic Roman Pasta Carbonara')">
                <div class="uber-img-wrap">
                    <img src="https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=800&q=80" alt="Pasta Carbonara">
                    <div class="uber-tag-promo">Chef Pick</div>
                    <div class="uber-badge-time">20 min</div>
                </div>
                <div class="uber-details">
                    <div class="uber-title-row">
                        <h3 class="uber-dish-name">Authentic Pasta Carbonara</h3>
                        <div class="uber-rating-badge"><span class="star">★</span> 4.8</div>
                    </div>
                    <div class="uber-meta-row">
                        <span>Italian</span>
                        <span class="uber-dot"></span>
                        <span>Crispy Guanciale & Egg Yolks</span>
                    </div>
                </div>
            </div>

            <!-- Card 3 -->
            <div class="uber-card" onclick="quickOrder('Crispy Double Smash Cheeseburger')">
                <div class="uber-img-wrap">
                    <img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=80" alt="Smash Cheeseburger">
                    <div class="uber-badge-time">15 min</div>
                </div>
                <div class="uber-details">
                    <div class="uber-title-row">
                        <h3 class="uber-dish-name">Double Smash Cheeseburger</h3>
                        <div class="uber-rating-badge"><span class="star">★</span> 4.9</div>
                    </div>
                    <div class="uber-meta-row">
                        <span>American</span>
                        <span class="uber-dot"></span>
                        <span>Lacy Crust, Secret Sauce</span>
                    </div>
                </div>
            </div>

            <!-- Card 4 -->
            <div class="uber-card" onclick="quickOrder('Street-Style Tacos al Pastor')">
                <div class="uber-img-wrap">
                    <img src="https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=800&q=80" alt="Tacos al Pastor">
                    <div class="uber-badge-time">25 min</div>
                </div>
                <div class="uber-details">
                    <div class="uber-title-row">
                        <h3 class="uber-dish-name">Tacos al Pastor</h3>
                        <div class="uber-rating-badge"><span class="star">★</span> 4.7</div>
                    </div>
                    <div class="uber-meta-row">
                        <span>Mexican</span>
                        <span class="uber-dot"></span>
                        <span>Achiote Pork & Charred Pineapple</span>
                    </div>
                </div>
            </div>

            <!-- Card 5 -->
            <div class="uber-card" onclick="quickOrder('Rich Tonkotsu Ramen with Chashu')">
                <div class="uber-img-wrap">
                    <img src="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=800&q=80" alt="Tonkotsu Ramen">
                    <div class="uber-tag-promo">Comfort Food</div>
                    <div class="uber-badge-time">45 min</div>
                </div>
                <div class="uber-details">
                    <div class="uber-title-row">
                        <h3 class="uber-dish-name">Tonkotsu Ramen</h3>
                        <div class="uber-rating-badge"><span class="star">★</span> 4.9</div>
                    </div>
                    <div class="uber-meta-row">
                        <span>Japanese</span>
                        <span class="uber-dot"></span>
                        <span>Silky Pork Broth & Ajitsuke Tamago</span>
                    </div>
                </div>
            </div>

            <!-- Card 6 -->
            <div class="uber-card" onclick="quickOrder('Artisan Woodfired Pizza Margherita')">
                <div class="uber-img-wrap">
                    <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=800&q=80" alt="Pizza Margherita">
                    <div class="uber-badge-time">20 min</div>
                </div>
                <div class="uber-details">
                    <div class="uber-title-row">
                        <h3 class="uber-dish-name">Neapolitan Pizza Margherita</h3>
                        <div class="uber-rating-badge"><span class="star">★</span> 4.8</div>
                    </div>
                    <div class="uber-meta-row">
                        <span>Italian</span>
                        <span class="uber-dot"></span>
                        <span>San Marzano & Fresh Fior di Latte</span>
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- 6. Recipe Output Anchor Area -->
    <div id="kitchen-pass" class="recipe-section">
        {recipe_content}
    </div>

    <!-- 7. Brand Footer -->
    <footer class="brand-footer">
        <div class="footer-inner">
            <div class="footer-brand">Savor.</div>
            <div style="font-size: 14px; color: rgba(255,255,255,0.6);">Delicious food, made effortless for everyone.</div>
        </div>
        <div class="footer-copy">
            <span>© 2026 Savor Kitchen Inc. All rights reserved.</span>
            <span>Crafted for food lovers everywhere.</span>
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
                        "You are a top restaurant chef. When given a dish name, create a clean, elegant, "
                        "and crystal-clear step-by-step recipe in markdown. Do NOT use any emojis anywhere.\n\n"
                        "Include:\n"
                        "1. Dish Name (h1) with a brief 1-sentence intro\n"
                        "2. Prep & Cook Times table (Prep Time, Cook Time, Total Time, Servings)\n"
                        "3. Ingredients table (Ingredient, Measurement, Notes)\n"
                        "4. Numbered step-by-step instructions\n"
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
        <div class="recipe-card-brand">
            <div class="recipe-header-bar">
                <div class="recipe-header-badge">Custom Recipe</div>
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
