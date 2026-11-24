from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
import sys
import re
from dotenv import load_dotenv
from groq import Groq
from markdown_it import MarkdownIt

md = MarkdownIt("commonmark").enable(["table", "strikethrough"])
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key) if api_key else None
app = FastAPI(title="Savor - Taste the Moment")

def get_dish_photo(dish: str) -> str:
    d = dish.lower()
    if any(k in d for k in ["steak", "ribeye", "beef", "sirloin", "tenderloin"]):
        return "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["pasta", "tagliatelle", "carbonara", "spaghetti", "lasagna", "fettuccine", "penne"]):
        return "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["taco", "tacos", "mexican", "burrito", "fajita"]):
        return "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["ramen", "noodle", "noodles", "soup", "pho", "udon"]):
        return "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["burger", "cheeseburger", "sandwich", "sliders"]):
        return "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["pizza", "margherita", "calzone"]):
        return "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["scallop", "salmon", "seafood", "fish", "shrimp", "lobster", "tuna"]):
        return "https://images.unsplash.com/photo-1532550907401-a500c9a57435?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["chicken", "curry", "biryani", "tikka", "krapow"]):
        return "https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["pancake", "pancakes", "waffle", "dessert", "cake", "cookie", "chocolate"]):
        return "https://images.unsplash.com/photo-1528207776546-365bb710ee93?auto=format&fit=crop&w=1600&q=85"
    if any(k in d for k in ["salad", "bowl", "greens", "vegan", "quinoa"]):
        return "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=1600&q=85"
    return "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1600&q=85"

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
           4. FULL-PHOTO CINEMATIC TILES (NO CLUNKY BOXES)
           ========================================================================== */
        .showcase-section {{
            max-width: 1240px;
            margin: 20px auto 60px;
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
            border-color: rgba(6, 193, 103, 0.5);
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(6, 193, 103, 0.3);
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
           5. SEAMLESSLY BLENDED DISH RECIPE SECTION (WITH EMERALD GREEN GLOW ACCENTS)
           ========================================================================== */
        .recipe-section {{
            max-width: 1080px;
            margin: 40px auto 100px;
            padding: 0 32px;
            position: relative;
            z-index: 10;
        }}

        /* Sizzling Dish Banner with Feathered Gradient Fade */
        .dish-hero-banner {{
            position: relative;
            min-height: 380px;
            border-radius: var(--radius-tile);
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.7);
            display: flex;
            align-items: flex-end;
            padding: 44px;
            background: transparent;
        }}

        .dish-hero-img {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center 55%;
            filter: brightness(0.72) contrast(1.1);
        }}

        /* Continuous vignette gradient melting photo directly into background */
        .dish-hero-gradient {{
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to bottom,
                rgba(9, 9, 11, 0.15) 0%,
                rgba(9, 9, 11, 0.55) 50%,
                rgba(9, 9, 11, 0.95) 90%,
                #09090B 100%
            );
            pointer-events: none;
        }}

        .dish-hero-meta {{
            position: relative;
            z-index: 2;
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            gap: 24px;
        }}

        .dish-hero-text {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-width: 680px;
        }}

        .dish-badge-pill {{
            align-self: flex-start;
            background: var(--brand-green);
            color: #000000;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 5px 14px;
            border-radius: var(--radius-pill);
            box-shadow: 0 0 16px rgba(6, 193, 103, 0.4);
        }}

        .dish-hero-headline {{
            font-size: 44px;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -0.03em;
            color: #FFFFFF;
            margin: 0;
            text-shadow: 0 4px 20px rgba(0, 0, 0, 0.8);
        }}

        .dish-hero-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-shrink: 0;
        }}

        .btn-copy-recipe {{
            background: var(--brand-green);
            color: #000000;
            border: none;
            padding: 12px 26px;
            border-radius: var(--radius-pill);
            font-family: inherit;
            font-size: 14px;
            font-weight: 800;
            cursor: pointer;
            transition: all 0.15s ease;
            box-shadow: 0 4px 18px rgba(6, 193, 103, 0.45);
        }}

        .btn-copy-recipe:hover {{
            background: var(--brand-green-hover);
            transform: scale(0.98);
        }}

        .btn-print-recipe {{
            background: rgba(255, 255, 255, 0.12);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            padding: 12px 22px;
            border-radius: var(--radius-pill);
            font-family: inherit;
            font-size: 14px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
        }}

        .btn-print-recipe:hover {{
            background: rgba(255, 255, 255, 0.25);
        }}

        /* Completely Blended Recipe Body (No Hard Box, No Isolated Frame) */
        .recipe-editorial-body {{
            background: transparent;
            border: none;
            padding: 36px 8px 60px;
            color: #D4D4D8;
            font-size: 16px;
            line-height: 1.7;
        }}

        .recipe-editorial-body h1 {{
            display: none; /* Rendered prominently on the hero banner */
        }}

        .recipe-editorial-body h2 {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #FFFFFF;
            margin: 40px 0 18px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .recipe-editorial-body h2::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 18px;
            background: var(--brand-green);
            border-radius: var(--radius-pill);
            box-shadow: 0 0 10px var(--brand-green);
        }}

        .recipe-editorial-body p {{
            margin: 0 0 18px;
            color: #D1D1D6;
        }}

        .recipe-editorial-body hr {{
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            margin: 36px 0;
        }}

        /* Floating Translucent Metric Tables */
        .recipe-editorial-body table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 20px 0 36px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            overflow: hidden;
        }}

        .recipe-editorial-body th {{
            background: rgba(255, 255, 255, 0.06);
            color: #FFFFFF;
            font-size: 12.5px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 16px 22px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
            text-align: left;
        }}

        .recipe-editorial-body td {{
            padding: 16px 22px;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 15px;
            color: #EDEDED;
            line-height: 1.5;
        }}

        .recipe-editorial-body tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        /* Floating Translucent Chef Step Cards (With Emerald Number Badges) */
        .recipe-editorial-body ol {{
            list-style: none;
            counter-reset: chef-step;
            padding: 0;
            display: flex;
            flex-direction: column;
            gap: 16px;
            margin: 24px 0 36px;
        }}

        .recipe-editorial-body ol li {{
            counter-increment: chef-step;
            position: relative;
            padding: 22px 24px 22px 72px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            font-size: 15.5px;
            line-height: 1.65;
            color: #EDEDED;
            transition: all 0.2s ease;
        }}

        .recipe-editorial-body ol li:hover {{
            border-color: rgba(6, 193, 103, 0.4);
            background: rgba(6, 193, 103, 0.03);
            box-shadow: 0 8px 24px rgba(6, 193, 103, 0.08);
            transform: translateX(3px);
        }}

        .recipe-editorial-body ol li::before {{
            content: counter(chef-step, decimal-leading-zero);
            position: absolute;
            left: 22px;
            top: 22px;
            width: 34px;
            height: 34px;
            background: rgba(6, 193, 103, 0.16);
            color: var(--brand-green);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12.5px;
            font-weight: 800;
            letter-spacing: -0.02em;
            border: 1px solid rgba(6, 193, 103, 0.35);
            box-shadow: 0 0 14px rgba(6, 193, 103, 0.25);
        }}

        /* Illuminated Chef Secret Card (With Emerald Accent & Glow) */
        .recipe-editorial-body blockquote {{
            margin: 36px 0 20px;
            padding: 24px 28px;
            background: linear-gradient(135deg, rgba(6, 193, 103, 0.08) 0%, rgba(16, 16, 20, 0.95) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(6, 193, 103, 0.35);
            border-left: 5px solid var(--brand-green);
            border-radius: 16px;
            color: #FFFFFF;
            font-size: 15.5px;
            line-height: 1.6;
            box-shadow: 0 8px 28px rgba(6, 193, 103, 0.12);
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
            .dish-hero-meta {{ flex-direction: column; align-items: flex-start; }}
            .dish-hero-banner {{ padding: 28px; }}
            .recipe-editorial-body {{ padding: 32px 12px; }}
        }}

        @media (max-width: 640px) {{
            .hero-title {{ font-size: 36px; }}
            .dish-hero-headline {{ font-size: 30px; }}
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

    <!-- 4. Full-Photo Cinematic Tiles -->
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

    <!-- 5. Seamlessly Blended Dish Recipe Section (With Restored Emerald Glow) -->
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
            const body = document.querySelector('.recipe-editorial-body');
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
        <div class="recipe-editorial-body" style="color: #FF5A36;">
            GROQ_API_KEY environment variable is not set.
        </div>
        '''
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Give me an executive restaurant chef recipe for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an acclaimed executive restaurant chef creating a masterclass recipe. "
                        "Do NOT use any emojis anywhere in your output.\n\n"
                        "Format your response cleanly in markdown with the following structure:\n"
                        "# " + dish + "\n"
                        "A vivid, 1-sentence introduction describing the flavors, aromas, and texture.\n\n"
                        "## Prep & Cook Overview\n"
                        "| Prep Time | Cook Time | Total Time | Servings |\n"
                        "| :--- | :--- | :--- | :--- |\n"
                        "| (e.g. 15 min) | (e.g. 20 min) | (e.g. 35 min) | (e.g. 4 servings) |\n\n"
                        "## Mise En Place & Measurements\n"
                        "| Ingredient | Exact Measurement | Chef's Notes |\n"
                        "| :--- | :--- | :--- |\n\n"
                        "## Step-By-Step Culinary Method\n"
                        "Provide numbered steps (1., 2., 3., etc.). Keep each step concise, actionable, and focused on technique (heat control, searing, seasoning, resting).\n\n"
                        "## Executive Chef's Secret Technique\n"
                        "> The single crucial pro tip that elevates this dish from home cooking to Michelin-star standard."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        recipe_md = response.choices[0].message.content
        html_recipe = md.render(recipe_md)
        photo_url = get_dish_photo(dish)

        box = f'''
        <div class="dish-hero-banner">
            <img src="{photo_url}" alt="{dish}" class="dish-hero-img" />
            <div class="dish-hero-gradient"></div>
            <div class="dish-hero-meta">
                <div class="dish-hero-text">
                    <span class="dish-badge-pill">Chef Masterclass</span>
                    <h1 class="dish-hero-headline">{dish}</h1>
                </div>
                <div class="dish-hero-actions">
                    <button class="btn-copy-recipe" id="copyRecipeBtn" onclick="copyRecipeText()">Copy Recipe</button>
                    <button class="btn-print-recipe" onclick="window.print()">Print</button>
                </div>
            </div>
        </div>
        <div class="recipe-editorial-body">
            {html_recipe}
        </div>
        '''
    except Exception as e:
        box = f'''
        <div class="recipe-editorial-body" style="color: #FF5A36;">
            Error generating recipe: {e}
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
