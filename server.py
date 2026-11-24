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
            --surface-soft: #F7F7F7;
            --surface-subtle: #EEEEEE;
            --ink-black: #0F0F0F;
            --ink-charcoal: #2C2C2E;
            --ink-muted: #6E6E6E;
            --ink-faint: #9E9E9E;
            --border-light: rgba(0, 0, 0, 0.08);
            --shadow-card: 0 12px 32px rgba(0, 0, 0, 0.07);
            --shadow-pop: 0 20px 48px -12px rgba(0, 0, 0, 0.12);
            --radius-pill: 9999px;
            --radius-card: 22px;
            --radius-inner: 16px;
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
           1. TOP ANNOUNCEMENT TICKER
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
           2. BRAND NAVIGATION BAR
           ========================================================================== */
        .brand-nav {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-bottom: 1px solid var(--border-light);
            padding: 14px 32px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .nav-left {{
            display: flex;
            align-items: center;
            gap: 28px;
        }}

        .brand-logo {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.04em;
            color: var(--ink-black);
            display: flex;
            align-items: center;
            gap: 6px;
            text-decoration: none;
        }}

        .brand-logo .dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--brand-green);
        }}

        .nav-switchers {{
            display: flex;
            align-items: center;
            background: var(--surface-soft);
            border-radius: var(--radius-pill);
            padding: 4px;
            border: 1px solid var(--border-light);
        }}

        .nav-switcher-btn {{
            padding: 6px 16px;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            background: transparent;
            color: var(--ink-muted);
            transition: all 0.15s ease;
        }}

        .nav-switcher-btn.active {{
            background: #FFFFFF;
            color: var(--ink-black);
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }}

        .nav-right {{
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .nav-link {{
            color: var(--ink-charcoal);
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
            transition: color 0.15s;
        }}

        .nav-link:hover {{
            color: var(--brand-green);
        }}

        .nav-cta {{
            background: var(--ink-black);
            color: #FFFFFF;
            padding: 10px 20px;
            border-radius: var(--radius-pill);
            text-decoration: none;
            font-size: 13.5px;
            font-weight: 700;
            transition: transform 0.15s ease, background 0.15s;
        }}

        .nav-cta:hover {{
            background: var(--brand-green);
            transform: scale(0.98);
        }}

        /* ==========================================================================
           3. PROFESSIONAL CUISINE CATEGORIES BAR (PHOTO THUMBNAILS - NO EMOJIS)
           ========================================================================== */
        .cuisine-subbar {{
            background: #FFFFFF;
            border-bottom: 1px solid var(--border-light);
            padding: 12px 32px;
            overflow-x: auto;
            scrollbar-width: none;
        }}

        .cuisine-subbar::-webkit-scrollbar {{
            display: none;
        }}

        .cuisine-strip {{
            max-width: 1180px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 24px;
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
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .cuisine-pill:hover {{
            transform: translateY(-2px);
            color: var(--brand-green);
        }}

        .cuisine-pill .thumb-round {{
            width: 44px;
            height: 44px;
            border-radius: 50%;
            overflow: hidden;
            border: 2px solid var(--border-light);
            background: #FAFAFA;
            transition: border-color 0.15s;
        }}

        .cuisine-pill:hover .thumb-round {{
            border-color: var(--brand-green);
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
           4. VIBRANT HERO SECTION
           ========================================================================== */
        .hero-banner {{
            background: #FFFFFF;
            padding: 48px 32px 64px;
            position: relative;
            border-bottom: 1px solid var(--border-light);
        }}

        .hero-wrap {{
            max-width: 1180px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 56px;
            align-items: center;
        }}

        .hero-content {{
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            padding: 6px 14px;
            background: rgba(6, 193, 103, 0.1);
            color: #038E4B;
            border-radius: var(--radius-pill);
            font-size: 13px;
            font-weight: 700;
            width: fit-content;
        }}

        .hero-title {{
            font-size: 56px;
            font-weight: 800;
            line-height: 1.05;
            letter-spacing: -0.04em;
            color: var(--ink-black);
            margin: 0;
        }}

        .hero-title span.accent {{
            color: var(--brand-green);
        }}

        .hero-desc {{
            font-size: 17.5px;
            line-height: 1.5;
            color: var(--ink-muted);
            margin: 0;
            max-width: 520px;
        }}

        /* UberEats Search Input */
        .search-container {{
            margin-top: 8px;
            background: var(--surface-white);
            border-radius: var(--radius-pill);
            padding: 6px 6px 6px 20px;
            border: 2px solid var(--ink-black);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.08);
            display: flex;
            align-items: center;
            gap: 12px;
            transition: box-shadow 0.2s, transform 0.2s;
        }}

        .search-container:focus-within {{
            box-shadow: 0 20px 44px rgba(6, 193, 103, 0.22);
            border-color: var(--brand-green);
            transform: translateY(-2px);
        }}

        .search-icon-svg {{
            width: 20px;
            height: 20px;
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
            padding: 16px 32px;
            border-radius: var(--radius-pill);
            font-family: inherit;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }}

        .cook-action-btn:hover {{
            background: var(--brand-green-hover);
            transform: scale(0.98);
        }}

        .cook-action-btn:active {{
            transform: scale(0.95);
        }}

        /* Quick Search Pill Tags */
        .quick-searches {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
            font-size: 13px;
            color: var(--ink-muted);
            margin-top: 4px;
        }}

        .quick-tag {{
            background: var(--surface-soft);
            color: var(--ink-charcoal);
            padding: 5px 14px;
            border-radius: var(--radius-pill);
            cursor: pointer;
            font-weight: 600;
            transition: all 0.15s;
        }}

        .quick-tag:hover {{
            background: #EAEAEA;
            color: var(--ink-black);
        }}

        /* Hero Food Mosaic Collage */
        .hero-mosaic {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            position: relative;
        }}

        .mosaic-card {{
            border-radius: var(--radius-card);
            overflow: hidden;
            box-shadow: var(--shadow-card);
            position: relative;
            background: #EEE;
            aspect-ratio: 1;
            transition: transform 0.25s ease, box-shadow 0.25s;
        }}

        .mosaic-card:hover {{
            transform: translateY(-4px) scale(1.02);
            box-shadow: var(--shadow-pop);
        }}

        .mosaic-card:nth-child(2) {{
            transform: translateY(24px);
        }}
        .mosaic-card:nth-child(2):hover {{
            transform: translateY(20px) scale(1.02);
        }}

        .mosaic-card img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .mosaic-tag {{
            position: absolute;
            bottom: 12px;
            left: 12px;
            background: rgba(15, 15, 15, 0.78);
            backdrop-filter: blur(8px);
            color: #FFF;
            padding: 5px 12px;
            border-radius: var(--radius-pill);
            font-size: 12px;
            font-weight: 700;
        }}

        /* ==========================================================================
           5. POPULAR DISH CARDS
           ========================================================================== */
        .category-shelf {{
            max-width: 1180px;
            margin: 48px auto 0;
            padding: 0 32px;
        }}

        .shelf-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 22px;
        }}

        .shelf-title {{
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.03em;
            margin: 0;
        }}

        .shelf-subtitle {{
            font-size: 14.5px;
            color: var(--ink-muted);
            margin: 4px 0 0;
        }}

        .food-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 22px;
        }}

        .food-item-card {{
            background: var(--surface-white);
            border-radius: var(--radius-card);
            overflow: hidden;
            border: 1px solid var(--border-light);
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            text-align: left;
        }}

        .food-item-card:hover {{
            transform: translateY(-6px);
            box-shadow: var(--shadow-pop);
            border-color: rgba(6, 193, 103, 0.3);
        }}

        .food-item-card .thumb {{
            width: 100%;
            height: 165px;
            position: relative;
            overflow: hidden;
            background: #FAFAF7;
        }}

        .food-item-card .thumb img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.35s ease;
        }}

        .food-item-card:hover .thumb img {{
            transform: scale(1.06);
        }}

        .food-item-card .badge-time {{
            position: absolute;
            top: 10px;
            right: 10px;
            background: #FFFFFF;
            color: var(--ink-black);
            padding: 4px 10px;
            border-radius: var(--radius-pill);
            font-size: 11.5px;
            font-weight: 700;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}

        .food-item-details {{
            padding: 16px;
        }}

        .food-item-title {{
            font-size: 16px;
            font-weight: 700;
            color: var(--ink-black);
            margin: 0 0 4px;
        }}

        .food-item-meta {{
            font-size: 13px;
            color: var(--ink-muted);
        }}

        /* ==========================================================================
           6. RECIPE OUTPUT SECTION
           ========================================================================== */
        .recipe-section {{
            max-width: 880px;
            margin: 48px auto;
            padding: 0 24px;
        }}

        .recipe-card-brand {{
            background: var(--surface-white);
            border-radius: var(--radius-card);
            box-shadow: var(--shadow-pop);
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
            padding: 18px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .recipe-header-badge {{
            display: flex;
            align-items: center;
            gap: 8px;
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
            padding: 7px 16px;
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
            padding: 40px;
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
            border-top: 1px solid var(--surface-subtle);
            margin: 28px 0;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            border-radius: var(--radius-inner);
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
           7. BRAND PERKS (CLEAN SVG ICONS - NO EMOJIS)
           ========================================================================== */
        .perks-strip {{
            background: var(--surface-white);
            border-top: 1px solid var(--border-light);
            border-bottom: 1px solid var(--border-light);
            padding: 64px 32px;
            margin-top: 72px;
        }}

        .perks-grid {{
            max-width: 1180px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
        }}

        .perk-card {{
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}

        .perk-icon-svg {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            background: rgba(6, 193, 103, 0.12);
            color: var(--brand-green);
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .perk-icon-svg svg {{
            width: 24px;
            height: 24px;
            stroke: currentColor;
            fill: none;
            stroke-width: 2.2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}

        .perk-heading {{
            font-size: 18px;
            font-weight: 800;
            color: var(--ink-black);
            margin: 0;
        }}

        .perk-text {{
            font-size: 14.5px;
            color: var(--ink-muted);
            line-height: 1.5;
            margin: 0;
        }}

        /* Footer */
        .brand-footer {{
            background: var(--ink-black);
            color: #FFFFFF;
            padding: 56px 32px 40px;
        }}

        .footer-inner {{
            max-width: 1180px;
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
            max-width: 1180px;
            margin: 28px auto 0;
            font-size: 13px;
            color: rgba(255, 255, 255, 0.4);
            display: flex;
            justify-content: space-between;
        }}

        /* Responsive */
        @media (max-width: 900px) {{
            .hero-wrap {{ grid-template-columns: 1fr; gap: 40px; }}
            .hero-title {{ font-size: 42px; }}
            .food-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .perks-grid {{ grid-template-columns: 1fr; gap: 32px; }}
            .nav-switchers, .nav-links {{ display: none; }}
        }}
    </style>
</head>
<body>
    <!-- 1. Top Announcement Ticker -->
    <div class="top-banner">
        <span class="promo-badge">PRO V2.5</span>
        <span>Generate calibrated chef recipes with exact gram measurements in seconds</span>
    </div>

    <!-- 2. Brand Navigation Bar -->
    <nav class="brand-nav">
        <div class="nav-left">
            <a href="/" class="brand-logo">
                Savor<span class="dot"></span>
            </a>
            <div class="nav-switchers">
                <button class="nav-switcher-btn active">Home Cooking</button>
                <button class="nav-switcher-btn">15-Min Quick</button>
                <button class="nav-switcher-btn">Healthy & Keto</button>
            </div>
        </div>

        <div class="nav-right">
            <a href="#popular" class="nav-link">Trending Dishes</a>
            <a href="#why-savor" class="nav-link">Why Savor</a>
            <a href="#search-anchor" class="nav-cta">Cook Tonight</a>
        </div>
    </nav>

    <!-- 3. Clean Photo-Thumbnail Categories (Zero Emojis, Real Photography) -->
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

    <!-- 4. Hero Section -->
    <header class="hero-banner">
        <div class="hero-wrap">
            <div class="hero-content">
                <div class="hero-badge">Curated Kitchen Intelligence</div>
                <h1 class="hero-title">
                    Order from your fridge.<br>
                    Cook like a <span class="accent">pro.</span>
                </h1>
                <p class="hero-desc">
                    Craving authentic tacos, creamy pasta, or buttery curry? Enter any dish name and Savor serves up the exact measurements, steps, and chef secrets.
                </p>

                <!-- Search Input -->
                <div id="search-anchor">
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
                        <button type="submit" class="cook-action-btn">
                            <span>Get Recipe</span>
                            <span>→</span>
                        </button>
                    </form>

                    <div class="quick-searches">
                        <span>Popular:</span>
                        <span class="quick-tag" onclick="quickOrder('Butter Chicken')">Butter Chicken</span>
                        <span class="quick-tag" onclick="quickOrder('Pasta Carbonara')">Carbonara</span>
                        <span class="quick-tag" onclick="quickOrder('Falafel Bowl')">Falafel Bowl</span>
                        <span class="quick-tag" onclick="quickOrder('Fluffy Pancakes')">Pancakes</span>
                    </div>
                </div>
            </div>

            <!-- Welcoming Food Mosaic -->
            <div class="hero-mosaic">
                <div class="mosaic-card">
                    <img src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=600&q=80" alt="Restaurant Dish">
                    <div class="mosaic-tag">Pasta & Noodles</div>
                </div>
                <div class="mosaic-card">
                    <img src="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?auto=format&fit=crop&w=600&q=80" alt="Artisan Pizza">
                    <div class="mosaic-tag">Woodfired Pizza</div>
                </div>
                <div class="mosaic-card">
                    <img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=600&q=80" alt="Juicy Burger">
                    <div class="mosaic-tag">Smash Burgers</div>
                </div>
                <div class="mosaic-card">
                    <img src="https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=600&q=80" alt="Biryani Bowl">
                    <div class="mosaic-tag">Aromatic Biryani</div>
                </div>
            </div>
        </div>
    </header>

    <!-- Popular Dishes Shelf -->
    <section class="category-shelf" id="popular">
        <div class="shelf-header">
            <div>
                <h2 class="shelf-title">Popular Cravings Today</h2>
                <p class="shelf-subtitle">Select any dish below to generate your custom recipe instantly</p>
            </div>
        </div>

        <div class="food-grid">
            <div class="food-item-card" onclick="quickOrder('Butter Chicken with Garlic Naan')">
                <div class="thumb">
                    <img src="https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=600&q=80" alt="Butter Chicken">
                    <div class="badge-time">35 min</div>
                </div>
                <div class="food-item-details">
                    <h3 class="food-item-title">Butter Chicken</h3>
                    <div class="food-item-meta">Rich & Creamy · North Indian</div>
                </div>
            </div>

            <div class="food-item-card" onclick="quickOrder('Classic Roman Pasta Carbonara')">
                <div class="thumb">
                    <img src="https://images.unsplash.com/photo-1612874742237-6526221588e3?auto=format&fit=crop&w=600&q=80" alt="Pasta Carbonara">
                    <div class="badge-time">20 min</div>
                </div>
                <div class="food-item-details">
                    <h3 class="food-item-title">Pasta Carbonara</h3>
                    <div class="food-item-meta">Guanciale & Pecorino · Italian</div>
                </div>
            </div>

            <div class="food-item-card" onclick="quickOrder('Crispy Double Cheeseburger')">
                <div class="thumb">
                    <img src="https://images.unsplash.com/photo-1550547660-d9450f859349?auto=format&fit=crop&w=600&q=80" alt="Cheeseburger">
                    <div class="badge-time">15 min</div>
                </div>
                <div class="food-item-details">
                    <h3 class="food-item-title">Smash Cheeseburger</h3>
                    <div class="food-item-meta">Caramelized Edges · American</div>
                </div>
            </div>

            <div class="food-item-card" onclick="quickOrder('Street-Style Tacos al Pastor')">
                <div class="thumb">
                    <img src="https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=600&q=80" alt="Tacos">
                    <div class="badge-time">25 min</div>
                </div>
                <div class="food-item-details">
                    <h3 class="food-item-title">Tacos al Pastor</h3>
                    <div class="food-item-meta">Spiced Pork & Pineapple · Mexican</div>
                </div>
            </div>
        </div>
    </section>

    <!-- Recipe Output Anchor Area -->
    <div id="kitchen-pass" class="recipe-section">
        {recipe_content}
    </div>

    <!-- Perks / Why Savor (Clean Minimalist Vector Icons) -->
    <section class="perks-strip" id="why-savor">
        <div class="perks-grid">
            <div class="perk-card">
                <div class="perk-icon-svg">
                    <svg viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>
                </div>
                <h3 class="perk-heading">Instant Generation</h3>
                <p class="perk-text">Zero 2,000-word food blog preludes. Get pure ingredients and numbered steps in under 2 seconds.</p>
            </div>
            <div class="perk-card">
                <div class="perk-icon-svg">
                    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                </div>
                <h3 class="perk-heading">Tested Chef Tips</h3>
                <p class="perk-text">Every recipe includes a restaurant-grade secret tip to guarantee balanced flavor and perfect texture.</p>
            </div>
            <div class="perk-card">
                <div class="perk-icon-svg">
                    <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                </div>
                <h3 class="perk-heading">Exact Mise En Place</h3>
                <p class="perk-text">Clear ingredient ratios and timings calibrated so you never guess oven temperatures or pan heat again.</p>
            </div>
        </div>
    </section>

    <!-- Brand Footer -->
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
