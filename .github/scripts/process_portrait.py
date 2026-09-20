#!/usr/bin/env python3
"""
Generate an animated, theme-matched visual profile banner (dark.svg / light.svg).
Theme: matches the projects panel (navy #0A101F, cyan #22D3EE, violet #A78BFA,
emerald #10B981, mono font, dotted leaders, pulsing live indicators).
"""
import json, os, sys, math, html
import numpy as np
from scipy.optimize import linear_sum_assignment
from PIL import Image

# ---------------- themes ----------------
THEMES = {
    "dark": {
        "BG": "#0A101F", "PANEL": "#0C1426", "PANEL_BAR": "#0B1222",
        "CYAN": "#22D3EE", "VIOLET": "#A78BFA", "VIOLET2": "#7C3AED",
        "EMERALD": "#10B981", "TEXT": "#F8FAFC", "MUTED": "#94A3B8",
        "DIM": "#475569", "RED": "#EF4444",
        "STROKE": "rgba(34,211,238,0.28)", "STROKE_HI": "rgba(34,211,238,0.5)",
        "STROKE_LO": "rgba(34,211,238,0.22)", "BARLINE": "rgba(255,255,255,0.08)",
        "MONO_TX": "#EDE9FE",
    },
    "light": {
        "BG": "#F8FAFC", "PANEL": "#FFFFFF", "PANEL_BAR": "#F1F5F9",
        "CYAN": "#0891B2", "VIOLET": "#7C3AED", "VIOLET2": "#7C3AED",
        "EMERALD": "#059669", "TEXT": "#0F172A", "MUTED": "#475569",
        "DIM": "#94A3B8", "RED": "#DC2626",
        "STROKE": "rgba(8,145,178,0.30)", "STROKE_HI": "rgba(8,145,178,0.55)",
        "STROKE_LO": "rgba(8,145,178,0.20)", "BARLINE": "rgba(0,0,0,0.08)",
        "MONO_TX": "#FFFFFF",
    },
}

BG = PANEL = PANEL_BAR = CYAN = VIOLET = VIOLET2 = EMERALD = TEXT = MUTED = DIM = RED = None
STROKE = STROKE_HI = STROKE_LO = BARLINE = MONO_TX = None

def set_theme(name):
    t = THEMES[name]
    g = globals()
    for k, v in t.items():
        g[k] = v

set_theme("dark")

W = 1180
H = 610
FONT = "ui-monospace,SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

SYSTEM_INFO = [
    {"label": "Subject", "value": "Subhadip Guchhait"},
    {"label": "Role", "value": "Full-Stack Developer"},
    {"label": "Origin", "value": "Kolkata, India"},
    {"label": "Education", "value": "B.Tech in CSE"},
    {"label": "Status", "value": "Building AI &amp; Web3 Platforms"},
    {"label": "ToolChain", "value": "VS Code, IntelliJ, Docker, Git"},
    {"label": "", "value": ""}, 
    {"label": "Core.Lang", "value": "Java, Python, C, Solidity"},
    {"label": "Core.Frontend", "value": "React.js, Next.js, HTML/CSS"},
    {"label": "Core.Backend", "value": "Spring Boot, Node.js, Flask"},
    {"label": "Core.Database", "value": "PostgreSQL, MongoDB, MySQL"},
    {"label": "Core.Infra", "value": "AWS, GCP, Kubernetes, CI/CD"},
]

NUM_TRAVELERS = 10000
GRID_W, GRID_H = 300, 340
OFFSET_X = 70
OFFSET_Y = 115

def get_dense_shape_coords(image_name):
    try:
        if not os.path.exists(image_name):
            print(f"Warning: File {image_name} not found.")
            return np.zeros((NUM_TRAVELERS, 2), dtype=int)
            
        img = Image.open(image_name).convert("RGBA")
        bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
        bg.paste(img, (0, 0), img)
        img = bg.convert("L").resize((GRID_W, GRID_H), Image.Resampling.LANCZOS)
        
        pixels = np.array(img)
        y, x = np.where(pixels < 180)
        coords = np.column_stack((x, y))
        
        if len(coords) == 0:
            return np.zeros((NUM_TRAVELERS, 2), dtype=int)
            
        if len(coords) >= NUM_TRAVELERS:
            indices = np.random.choice(len(coords), NUM_TRAVELERS, replace=False)
            coords = coords[indices]
        else:
            idx = np.random.choice(len(coords), NUM_TRAVELERS - len(coords), replace=True)
            extra = coords[idx]
            coords = np.vstack((coords, extra))
            
        return coords
    except Exception as e:
        print(f"Failed to process shape {image_name}: {e}")
        return np.zeros((NUM_TRAVELERS, 2), dtype=int)

def get_dense_portrait_coords():
    try:
        # Use the raw portrait or dithered preview with an inclusive threshold so the face isn't blank
        p_path = "preview_dither.png"
        if not os.path.exists(p_path):
            p_path = "preview_dither_2.png"
        if not os.path.exists(p_path):
            p_path = "portrait.png" if os.path.exists("portrait.png") else "portrait.jpg"
            
        img = Image.open(p_path).convert("L").resize((GRID_W, GRID_H), Image.Resampling.LANCZOS)
        pixels = np.array(img)
        
        # Capture face details and shading (pixels < 220 grabs skin tones, glasses, hair, and suit)
        y, x = np.where(pixels < 220)
        coords = np.column_stack((x, y))
        
        if len(coords) == 0:
            return np.zeros((NUM_TRAVELERS, 2), dtype=int)
            
        if len(coords) >= NUM_TRAVELERS:
            indices = np.random.choice(len(coords), NUM_TRAVELERS, replace=False)
            coords = coords[indices]
        else:
            idx = np.random.choice(len(coords), NUM_TRAVELERS - len(coords), replace=True)
            extra = coords[idx]
            coords = np.vstack((coords, extra))
        return coords
    except Exception as e:
        print(f"Failed to process portrait coords: {e}")
        return np.zeros((NUM_TRAVELERS, 2), dtype=int)

def build_banner(theme="dark"):
    set_theme(theme)
    gid = f"banner_grad_{theme}"
    s = []
    a = s.append

    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'font-family="{FONT}" role="img" aria-label="Terminal Banner">')
    a(f'<rect width="{W}" height="{H}" fill="{BG}" rx="15"/>')
    
    # Animated accent gradient
    a(f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{VIOLET2}"><animate attributeName="stop-color" values="{VIOLET2};{CYAN};{EMERALD};{VIOLET2}" dur="10s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{EMERALD}"><animate attributeName="stop-color" values="{EMERALD};{VIOLET2};{CYAN};{EMERALD}" dur="10s" repeatCount="indefinite"/></stop>'
      f'</linearGradient></defs>')

    # Header shell prompt
    a(f'<text x="590" y="32" text-anchor="middle" font-size="13" fill="{CYAN}">subhadipguchhait106@gmail.com - % ./profile.sh --live</text>')

    # Left Terminal Card Frame (Visual Map)
    a(f'<rect x="40" y="80" width="360" height="490" rx="12" fill="{PANEL}" stroke="{STROKE}">'
      f'<animate attributeName="stroke" values="{STROKE_LO};{STROKE_HI};{STROKE_LO}" dur="4.5s" repeatCount="indefinite"/></rect>')
    a(f'<rect x="40" y="80" width="360" height="32" rx="12" fill="{PANEL_BAR}"/>')
    a(f'<rect x="40" y="98" width="360" height="14" fill="{PANEL_BAR}"/>')
    a(f'<line x1="40" y1="112" x2="400" y2="112" stroke="{BARLINE}"/>')
    a(f'<text x="56" y="101" font-size="10" fill="{MUTED}"><tspan fill="{CYAN}">&#8226;</tspan> VISUAL.MAP</text>')
    a(f'<circle cx="384" cy="96" r="3.5" fill="{RED}"><animate attributeName="opacity" values="1;0.25;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    a(f'<text x="358" y="100" font-size="9" fill="{RED}">LIVE</text>')

    # Right Terminal Card Frame (System Info)
    a(f'<text x="430" y="80" font-size="11" letter-spacing="2" fill="{CYAN}">SYSTEM.INFO</text>')
    a(f'<line x1="430" y1="92" x2="{W-40}" y2="92" stroke="url(#{gid})" stroke-width="1.5" opacity="0.7"/>')

    # Render SYSTEM.INFO Data Rows
    start_y = 125
    line_height = 24
    for i, row in enumerate(SYSTEM_INFO):
        if not row["label"] and not row["value"]: 
            start_y += 10
            continue
        y_pos = start_y + (i * line_height)
        a(f'<text x="430" y="{y_pos}" font-size="13" fill="{CYAN}">{row["label"]}</text>')
        if row["value"]:
            if row["label"] == "Status":
                a(f'<rect x="540" y="{y_pos-14}" width="225" height="20" rx="4" fill="{VIOLET2}" opacity="0.3"/>')
                a(f'<text x="550" y="{y_pos}" font-size="12" font-weight="700" fill="{MONO_TX}">{row["value"]}</text>')
            else:
                a(f'<text x="{W-40}" y="{y_pos}" font-size="13" fill="{TEXT}" text-anchor="end">{row["value"]}</text>')
                
        if row["value"] and row["label"] != "- Contact" and row["label"] != "Status":
            dot_start = 430 + (len(row["label"]) * 8.5) + 10
            dot_end = W - 40 - (len(row["value"]) * 8.2) - 10
            if dot_end > dot_start:
                a(f'<line x1="{dot_start}" y1="{y_pos - 4}" x2="{dot_end}" y2="{y_pos - 4}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="2, 6" opacity="0.3"/>')

    # ---------------- Synchronized High-Density Shape Morphing Pipeline ----------------
    p_coords = get_dense_portrait_coords()
    s_coords = get_dense_shape_coords("springboot.png")
    l_coords = get_dense_shape_coords("langchain.png")
    so_coords = get_dense_shape_coords("solidity.png")

    if len(p_coords) > 0 and len(s_coords) > 0 and len(l_coords) > 0 and len(so_coords) > 0:
        def match_coords(c1, c2):
            dist = np.linalg.norm(c1[:, np.newaxis] - c2, axis=2)
            _, idx = linear_sum_assignment(dist)
            return c2[idx]

        p_ordered = p_coords
        s_ordered = match_coords(p_ordered, s_coords)
        l_ordered = match_coords(s_ordered, l_coords)
        so_ordered = match_coords(l_ordered, so_coords)

        p_path = " ".join([f"M{x+OFFSET_X} {y+OFFSET_Y}h1" for x, y in p_ordered])
        s_path = " ".join([f"M{x+OFFSET_X} {y+OFFSET_Y}h1" for x, y in s_ordered])
        l_path = " ".join([f"M{x+OFFSET_X} {y+OFFSET_Y}h1" for x, y in l_ordered])
        so_path = " ".join([f"M{x+OFFSET_X} {y+OFFSET_Y}h1" for x, y in so_ordered])

        # 20s Total Duration with 10k dense points and 1.0 stroke width for solid fill
        a(f'<path d="{p_path}" stroke="{VIOLET}" stroke-width="1.0" shape-rendering="crispEdges">')
        a(f'  <animate attributeName="d" values="{p_path};{p_path};{s_path};{s_path};{l_path};{l_path};{so_path};{so_path};{p_path}" '
          f'keyTimes="0; 0.225; 0.275; 0.50; 0.55; 0.775; 0.825; 0.975; 1" '
          f'dur="20s" repeatCount="indefinite" calcMode="spline" '
          f'keySplines="0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1; 0.4 0 0.2 1"/>')
        a('</path>')

    a('</svg>')
    return "".join(s)

if __name__ == "__main__":
    outdir = sys.argv[1] if len(sys.argv) > 1 else "."
    for theme, fname in (("dark", "dark.svg"), ("light", "light.svg")):
        svg_content = build_banner(theme)
        path = os.path.join(outdir, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Generated high-density portrait-fixed banner -> {path} ({theme})")