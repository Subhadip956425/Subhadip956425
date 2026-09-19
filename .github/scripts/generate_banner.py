import math
import json
import os

PALETTE = {
    "bg": "#0A101F",
    "chrome_light": "#22D3EE",
    "chrome_dark": "#089182",
    "accent": "#10B981",
    "portrait_dark_mode": "#A78BFA",
    "portrait_light_mode": "#7C3AED",
    "text_main": "#94A3B8",
    "text_bright": "#F8FAFC"
}

SYSTEM_INFO = [
    {"label": "Subject", "value": "Subhadip Guchhait"},
    {"label": "Role", "value": "Full-Stack Developer"},
    {"label": "Origin", "value": "Kolkata, India"},
    {"label": "Education", "value": "B.Tech in CSE"},
    {"label": "Status", "value": "Building AI & Web3 Platforms"},
    {"label": "ToolChain", "value": "VS Code, IntelliJ, Docker, Git"},
    {"label": "", "value": ""}, 
    {"label": "Core.Lang", "value": "Java, Python, C, Solidity"},
    {"label": "Core.Frontend", "value": "React.js, Next.js, HTML/CSS"},
    {"label": "Core.Backend", "value": "Spring Boot, Node.js, Flask"},
    {"label": "Core.Database", "value": "PostgreSQL, MongoDB, MySQL"},
    {"label": "Core.Infra", "value": "AWS, GCP, Kubernetes, CI/CD"},
    {"label": "", "value": ""}, 
    {"label": "- Contact", "value": ""},
    {"label": "Grid.Mail", "value": "subhadipguchhait106@gmail.com"},
    {"label": "Grid.Portfolio", "value": "subhadip-s-portfolio.vercel.app"},
    {"label": "Grid.LinkedIn", "value": "subhadip-guchhait-675395252"},
    {"label": "Grid.GitHub", "value": "@Subhadip956425"},
    {"label": "Grid.Facebook", "value": "@subhadipguchhait.guchhait.3"}
]

def generate_svg(theme="dark"):
    width, height = 1180, 610
    bg_color = PALETTE["bg"] if theme == "dark" else "#FFFFFF"
    portrait_color = PALETTE["portrait_dark_mode"] if theme == "dark" else PALETTE["portrait_light_mode"]
    
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="{bg_color}" rx="15"/>',
        f'<g font-family="monospace" font-size="13" fill="{PALETTE["chrome_light"]}">',
        f'<text x="590" y="35" text-anchor="middle">subhadipguchhait106@gmail.com - % ./profile.sh --live</text>',
        '</g>',
        f'<path d="M 50 100 L 50 80 L 70 80 M 350 80 L 370 80 L 370 100 M 50 510 L 50 530 L 70 530 M 350 530 L 370 530 L 370 510" fill="none" stroke="{PALETTE["chrome_dark"]}" stroke-width="2"/>',
        f'<text x="50" y="70" font-family="monospace" font-size="10" fill="{PALETTE["chrome_dark"]}" letter-spacing="2">VISUAL.MAP</text>',
        f'<text x="450" y="100" font-family="monospace" font-size="14" font-weight="bold" fill="{PALETTE["chrome_light"]}">SYSTEM.INFO</text>',
        f'<circle cx="1080" cy="95" r="4" fill="#EF4444">',
        f'  <animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/>',
        f'</circle>',
        f'<text x="1090" y="100" font-family="monospace" font-size="12" fill="#EF4444">LIVE</text>',
        f'<rect x="450" y="120" width="230" height="24" rx="4" fill="{portrait_color}"/>',
        f'<text x="460" y="137" font-family="monospace" font-size="14" font-weight="bold" fill="{PALETTE["bg"]}">subhadip.connect@gmail.com</text>'
    ]

    start_y = 170
    line_height = 23
    
    for i, row in enumerate(SYSTEM_INFO):
        if not row["label"] and not row["value"]: 
            start_y += line_height
            continue
            
        y_pos = start_y + (i * line_height)
        svg.append(f'<text x="450" y="{y_pos}" font-family="monospace" font-size="14" fill="{PALETTE["chrome_light"]}" textLength="{len(row["label"]) * 8.4}" lengthAdjust="spacingAndGlyphs">{row["label"]}</text>')
        
        if row["value"]:
            svg.append(f'<text x="1100" y="{y_pos}" font-family="monospace" font-size="14" fill="{PALETTE["text_bright"]}" text-anchor="end" textLength="{len(row["value"]) * 8.4}" lengthAdjust="spacingAndGlyphs">{row["value"]}</text>')
        
        if row["value"] and row["label"] != "- Contact":
            char_width = 8.4
            label_len = len(row["label"]) * char_width
            value_len = len(row["value"]) * char_width
            dot_start = 450 + label_len + 15
            dot_end = 1100 - value_len - 15
            
            if dot_end > dot_start:
                svg.append(f'<line x1="{dot_start}" y1="{y_pos - 4}" x2="{dot_end}" y2="{y_pos - 4}" stroke="{PALETTE["text_main"]}" stroke-width="2" stroke-dasharray="2, 6" opacity="0.3"/>')

    svg.append(f'<text x="450" y="550" font-family="monospace" font-size="12" fill="{PALETTE["text_main"]}">▶ More about me &amp; projects below in README ↓ █</text>')
    
    # Placeholder for Python Dithering/Morphing array (17,000 dots + 1,000 travelers)
    
    svg.append('</svg>')
    
    with open(f"{theme}.svg", "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

if __name__ == "__main__":
    generate_svg("dark")
    generate_svg("light")
