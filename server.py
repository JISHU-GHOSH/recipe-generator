from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import os
import sys
import json
import re
from dotenv import load_dotenv
from groq import Groq

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
    if any(k in d for k in ["scallop", "salmon", "seafood", "fish", "shrimp", "lobster", "tuna", "sea bass"]):
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
            --brand-green: #06C167;
            --brand-green-hover: #05A357;
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(6, 193, 103, 0.5);
            --text-pure: #FFFFFF;
            --text-dim: #A1A1AA;
            --text-faint: #71717A;
            --radius-pill: 9999px;
            --radius-tile: 22px;
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
           3. CINEMATIC FULL-BLEED FOOD HERO
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
           4. FULL-PHOTO CINEMATIC TILES
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
           5. EXACT RECIPE DESIGN MATCHING MOCKUP PICTURE
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

        /* Feathered photo melt directly into the dark background */
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
            gap: 14px;
            max-width: 720px;
        }}

        .dish-stat-pills-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .dish-badge-pill {{
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

        .dish-stat-pill {{
            background: rgba(10, 10, 14, 0.72);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            color: #FFFFFF;
            padding: 5px 13px;
            border-radius: var(--radius-pill);
            font-size: 11.5px;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
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

        /* Completely Blended Recipe Stream (No Stiff Box) */
        .recipe-stream {{
            padding: 36px 0 60px;
            display: flex;
            flex-direction: column;
            gap: 40px;
        }}

        .recipe-intro-text {{
            font-size: 18px;
            line-height: 1.6;
            color: #D1D1D6;
            margin: 0;
            font-style: italic;
        }}

        .recipe-block-title {{
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: #FFFFFF;
            margin: 0 0 20px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .recipe-block-title::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 18px;
            background: var(--brand-green);
            border-radius: var(--radius-pill);
            box-shadow: 0 0 10px var(--brand-green);
        }}

        /* Ingredients Checklist Grid */
        .ingredients-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 14px;
        }}

        .ingredient-chip {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
            cursor: pointer;
            transition: all 0.2s ease;
            user-select: none;
        }}

        .ingredient-chip:hover {{
            border-color: rgba(6, 193, 103, 0.35);
            background: rgba(6, 193, 103, 0.04);
        }}

        .ingredient-chip.checked {{
            border-color: rgba(6, 193, 103, 0.4);
            background: rgba(6, 193, 103, 0.08);
        }}

        .ingredient-chip.checked .ing-check-icon {{
            background: var(--brand-green);
            border-color: var(--brand-green);
        }}

        .ingredient-chip.checked .ing-name {{
            text-decoration: line-through;
            color: var(--text-faint);
        }}

        .ing-check-icon {{
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 2px solid rgba(255, 255, 255, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            flex-shrink: 0;
        }}

        .ing-check-icon svg {{
            width: 11px;
            height: 11px;
            stroke: #000000;
            stroke-width: 3;
            fill: none;
            stroke-linecap: round;
            stroke-linejoin: round;
        }}

        .ing-content {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .ing-name-row {{
            font-size: 15px;
            font-weight: 700;
            color: #FFFFFF;
        }}

        .ing-name-row span.ing-amt {{
            color: var(--brand-green);
            margin-right: 6px;
        }}

        .ing-notes {{
            font-size: 13px;
            color: var(--text-faint);
        }}

        /* Master Method Step Cards (Matching Mockup Picture) */
        .step-cards-list {{
            display: flex;
            flex-direction: column;
            gap: 16px;
        }}

        .step-card {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.07);
            padding: 24px 28px;
            display: flex;
            gap: 22px;
            align-items: flex-start;
            transition: all 0.2s ease;
        }}

        .step-card:hover {{
            border-color: rgba(6, 193, 103, 0.4);
            background: rgba(6, 193, 103, 0.03);
            box-shadow: 0 8px 24px rgba(6, 193, 103, 0.08);
            transform: translateX(4px);
        }}

        .step-badge {{
            width: 36px;
            height: 36px;
            background: rgba(6, 193, 103, 0.16);
            color: var(--brand-green);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 800;
            letter-spacing: -0.02em;
            border: 1px solid rgba(6, 193, 103, 0.35);
            box-shadow: 0 0 14px rgba(6, 193, 103, 0.25);
            flex-shrink: 0;
        }}

        .step-text-wrap {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .step-title {{
            font-size: 17px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.01em;
            margin: 0;
        }}

        .step-desc {{
            font-size: 15px;
            line-height: 1.65;
            color: #E4E4E7;
            margin: 0;
        }}

        /* Illuminated Chef Secret Card (Matching Mockup Picture) */
        .chef-secret-card {{
            margin-top: 10px;
            padding: 26px 30px;
            background: linear-gradient(135deg, rgba(6, 193, 103, 0.08) 0%, rgba(16, 16, 20, 0.95) 100%);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(6, 193, 103, 0.35);
            border-left: 5px solid var(--brand-green);
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
            box-shadow: 0 8px 28px rgba(6, 193, 103, 0.12);
        }}

        .chef-secret-label {{
            font-size: 12px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: var(--brand-green);
        }}

        .chef-secret-content {{
            font-size: 15.5px;
            line-height: 1.6;
            color: #FFFFFF;
            margin: 0;
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
            .ingredients-grid {{ grid-template-columns: 1fr; }}
            .recipe-section {{ padding: 0 20px; }}
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

    <!-- 5. Seamlessly Blended Recipe Section (Matching Mockup Picture) -->
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

        function toggleIng(el) {{
            el.classList.toggle('checked');
        }}

        function copyRecipeText() {{
            const stream = document.querySelector('.recipe-stream');
            if (stream) {{
                navigator.clipboard.writeText(stream.innerText).then(() => {{
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
        <div style="color: #FF5A36; padding: 40px; text-align: center;">
            GROQ_API_KEY environment variable is not set.
        </div>
        '''
        return render_page(dish_val=dish, recipe_content=box)
        
    prompt = f"Provide a complete, Michelin-level executive chef recipe for: {dish}"
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an acclaimed executive restaurant chef. Create an immaculate masterclass recipe.\n"
                        "Do NOT use any emojis anywhere.\n"
                        "Return a JSON object with this exact structure:\n"
                        "{\n"
                        '  "dish": "' + dish + '",\n'
                        '  "intro": "A 1-sentence vivid sensory description of flavors and texture",\n'
                        '  "prep_time": "15 min",\n'
                        '  "cook_time": "20 min",\n'
                        '  "servings": "4 servings",\n'
                        '  "level": "Executive Grade",\n'
                        '  "ingredients": [\n'
                        '    {"amount": "400g", "name": "Bronze-Die Tagliatelle", "note": "Use fresh egg pasta"},\n'
                        '    {"amount": "60g", "name": "Unsalted Normandy Butter", "note": "Cold, cubed"}\n'
                        '  ],\n'
                        '  "steps": [\n'
                        '    {"step_num": "01", "title": "Prep & Emulsify", "instruction": "Step details..."},\n'
                        '    {"step_num": "02", "title": "Finish & Plate", "instruction": "Step details..."}\n'
                        '  ],\n'
                        '  "secret_technique": "The single crucial pro tip that elevates this dish to Michelin standard."\n'
                        "}\n"
                        "Output strictly valid JSON only. No markdown formatting, no comments."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        photo_url = get_dish_photo(dish)

        # Build floating stat pills
        prep = data.get("prep_time", "15 min")
        cook = data.get("cook_time", "20 min")
        servings = data.get("servings", "4 servings")
        level = data.get("level", "Executive Grade")
        intro = data.get("intro", "")

        # Build Ingredients Cards
        ing_html_list = []
        for ing in data.get("ingredients", []):
            amt = ing.get("amount", "")
            name = ing.get("name", "")
            note = ing.get("note", "")
            note_html = f'<div class="ing-notes">{note}</div>' if note else ""
            ing_html_list.append(f'''
            <div class="ingredient-chip" onclick="toggleIng(this)">
                <div class="ing-check-icon">
                    <svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>
                </div>
                <div class="ing-content">
                    <div class="ing-name-row"><span class="ing-amt">{amt}</span><span class="ing-name">{name}</span></div>
                    {note_html}
                </div>
            </div>
            ''')
        ingredients_html = "".join(ing_html_list)

        # Build Steps Cards
        steps_html_list = []
        for idx, step in enumerate(data.get("steps", []), 1):
            num = step.get("step_num", f"{idx:02d}")
            title = step.get("title", f"Step {idx}")
            desc = step.get("instruction", "")
            steps_html_list.append(f'''
            <div class="step-card">
                <div class="step-badge">{num}</div>
                <div class="step-text-wrap">
                    <h4 class="step-title">{title}</h4>
                    <p class="step-desc">{desc}</p>
                </div>
            </div>
            ''')
        steps_html = "".join(steps_html_list)

        secret = data.get("secret_technique", "")

        box = f'''
        <div class="dish-hero-banner">
            <img src="{photo_url}" alt="{dish}" class="dish-hero-img" />
            <div class="dish-hero-gradient"></div>
            <div class="dish-hero-meta">
                <div class="dish-hero-text">
                    <div class="dish-stat-pills-row">
                        <span class="dish-badge-pill">Masterclass</span>
                        <span class="dish-stat-pill">{prep} prep</span>
                        <span class="dish-stat-pill">{cook} cook</span>
                        <span class="dish-stat-pill">{servings}</span>
                        <span class="dish-stat-pill">{level}</span>
                    </div>
                    <h1 class="dish-hero-headline">{dish}</h1>
                </div>
                <div class="dish-hero-actions">
                    <button class="btn-copy-recipe" id="copyRecipeBtn" onclick="copyRecipeText()">Copy Recipe</button>
                    <button class="btn-print-recipe" onclick="window.print()">Print</button>
                </div>
            </div>
        </div>

        <div class="recipe-stream">
            <p class="recipe-intro-text">"{intro}"</p>

            <div>
                <h3 class="recipe-block-title">Mise En Place & Ingredients</h3>
                <div class="ingredients-grid">
                    {ingredients_html}
                </div>
            </div>

            <div>
                <h3 class="recipe-block-title">Master Culinary Method</h3>
                <div class="step-cards-list">
                    {steps_html}
                </div>
            </div>

            <div class="chef-secret-card">
                <span class="chef-secret-label">Executive Chef's Secret Technique</span>
                <p class="chef-secret-content">{secret}</p>
            </div>
        </div>
        '''
    except Exception as e:
        box = f'''
        <div style="color: #FF5A36; padding: 40px; text-align: center;">
            Error generating recipe: {e}
        </div>
        '''
        
    return render_page(dish_val=dish, recipe_content=box)

if __name__ == "__main__":
    import uvicorn
    print("Serving recipe web app on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
