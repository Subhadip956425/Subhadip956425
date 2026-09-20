import math
import os
from PIL import Image
import numpy as np
from scipy.optimize import linear_sum_assignment

# --- CONFIGURATION ---
PALETTE = {
    "bg": "#0A101F",
    "chrome_light": "#22D3EE",
    "chrome_dark": "#089182",
    "portrait_dark_mode": "#A78BFA",
    "portrait_light_mode": "#7C3AED",
    "text_main": "#94A3B8",
    "text_bright": "#F8FAFC",
}

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
    {"label": "", "value": ""},
    {"label": "- Contact", "value": ""},
    {"label": "Grid.Mail", "value": "subhadipguchhait106@gmail.com"},
    {"label": "Grid.Portfolio", "value": "subhadip-s-portfolio.vercel.app"},
    {"label": "Grid.LinkedIn", "value": "subhadip-guchhait-675395252"},
    {"label": "Grid.GitHub", "value": "@Subhadip956425"},
    {"label": "Grid.Facebook", "value": "@subhadipguchhait.guchhait.3"},
]

# Identical point density across both modes for uniform clarity and design
NUM_TRAVELERS = 3000
GRID_OFFSET_X = 60
GRID_OFFSET_Y = 120
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_image_path(filename):
  p1 = os.path.join(BASE_DIR, filename)
  p2 = os.path.join(BASE_DIR, "..", "..", filename)
  if os.path.exists(p1):
    return p1
  if os.path.exists(p2):
    return p2
  return filename


def get_shape_coords(image_name, invert=False, resize=(200, 200)):
  try:
    img_path = get_image_path(image_name)
    img = Image.open(img_path).convert("RGBA")

    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    bg.paste(img, (0, 0), img)
    img = bg.convert("L").resize(resize, Image.Resampling.LANCZOS)

    pixels = np.array(img)
    y, x = np.where(pixels < 128)

    y += (340 - resize[1]) // 2
    x += (300 - resize[0]) // 2
    coords = np.column_stack((x, y))

    if len(coords) == 0:
      raise ValueError(f"No black pixels found in {image_name}")

    if len(coords) > NUM_TRAVELERS:
      indices = np.random.choice(len(coords), NUM_TRAVELERS, replace=False)
      return coords[indices]

    while len(coords) < NUM_TRAVELERS:
      coords = np.vstack((coords, coords))
    return coords[:NUM_TRAVELERS]

  except Exception as e:
    print(f"Failed to process {image_name}: {e}")
    return np.column_stack(
        (np.linspace(50, 250, NUM_TRAVELERS), np.ones(NUM_TRAVELERS) * 100)
    ).astype(int)


def generate_svg(theme="dark"):
  width, height = 1180, 610
  bg_color = PALETTE["bg"] if theme == "dark" else "#FFFFFF"
  portrait_color = (
      PALETTE["portrait_dark_mode"]
      if theme == "dark"
      else PALETTE["portrait_light_mode"]
  )

  # Theme configuration mapping #22D3EE for text in light mode
  if theme == "dark":
    header_text_color = PALETTE["chrome_light"]
    label_color = PALETTE["chrome_light"]
    value_color = PALETTE["text_bright"]
    dot_line_color = PALETTE["text_main"]
    logo_color = PALETTE["chrome_light"]
    logo_stroke = "3.2"
  else:
    header_text_color = "#22D3EE"
    label_color = "#22D3EE"
    value_color = "#22D3EE"
    dot_line_color = "#94A3B8"
    logo_color = "#7C3AED"  # Rich violet logo tone for light mode
    logo_stroke = "3.5"

  svg = [
      f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}"'
      f' width="{width}" height="{height}">',
      f'<rect width="{width}" height="{height}" fill="{bg_color}" rx="15"/>',
      f'<g font-family="monospace" font-size="13" fill="{header_text_color}">',
      '<text x="590" y="35" text-anchor="middle">subhadipguchhait106@gmail.com'
      " - % ./profile.sh --live</text>",
      "</g>",
      f'<path d="M 50 100 L 50 80 L 70 80 M 350 80 L 370 80 L 370 100 M 50 510'
      f' L 50 530 L 70 530 M 350 530 L 370 530 L 370 510" fill="none"'
      f' stroke="{PALETTE["chrome_dark"]}" stroke-width="2"/>',
      '<text x="50" y="70" font-family="monospace" font-size="10"'
      f' fill="{PALETTE["chrome_dark"]}"'
      ' letter-spacing="2">VISUAL.MAP</text>',
      f'<text x="450" y="100" font-family="monospace" font-size="14"'
      f' font-weight="bold" fill="{header_text_color}">SYSTEM.INFO</text>',
      '<circle cx="1080" cy="95" r="4" fill="#EF4444">',
      '  <animate attributeName="opacity" values="1;0.2;1" dur="2s"'
      ' repeatCount="indefinite"/>',
      "</circle>",
      '<text x="1090" y="100" font-family="monospace" font-size="12"'
      ' fill="#EF4444">LIVE</text>',
      f'<rect x="450" y="120" width="230" height="24" rx="4"'
      f' fill="{portrait_color}"/>',
      f'<text x="460" y="137" font-family="monospace" font-size="14"'
      f' font-weight="bold" fill="{PALETTE["bg"]}">subhadip.connect@gmail.com</text>',
  ]

  start_y = 170
  line_height = 23
  for i, row in enumerate(SYSTEM_INFO):
    if not row["label"] and not row["value"]:
      start_y += line_height
      continue
    y_pos = start_y + (i * line_height)
    svg.append(
        f'<text x="450" y="{y_pos}" font-family="monospace" font-size="14"'
        f' fill="{label_color}" textLength="{len(row["label"]) * 8.4}"'
        f' lengthAdjust="spacingAndGlyphs">{row["label"]}</text>'
    )
    if row["value"]:
      svg.append(
          f'<text x="1100" y="{y_pos}" font-family="monospace" font-size="14"'
          f' fill="{value_color}" text-anchor="end"'
          f' textLength="{len(row["value"]) * 8.4}"'
          f' lengthAdjust="spacingAndGlyphs">{row["value"]}</text>'
      )
    if row["value"] and row["label"] != "- Contact":
      dot_start = 450 + (len(row["label"]) * 8.4) + 15
      dot_end = 1100 - (len(row["value"]) * 8.4) - 15
      if dot_end > dot_start:
        svg.append(
            f'<line x1="{dot_start}" y1="{y_pos - 4}" x2="{dot_end}"'
            f' y2="{y_pos - 4}" stroke="{dot_line_color}" stroke-width="2"'
            ' stroke-dasharray="2, 6" opacity="0.4"/>'
        )

  try:
    port_img = Image.open(get_image_path("preview_dither.png")).convert("L")

    orig_path = get_image_path("portrait.jpg")
    if not os.path.exists(orig_path):
      orig_path = get_image_path("portrait.png")

    orig_img = (
        Image.open(orig_path)
        .convert("L")
        .resize((300, 340), Image.Resampling.LANCZOS)
    )

    pixels = np.array(port_img)
    orig_pixels = np.array(orig_img)

    if theme == "dark":
      mask = orig_pixels < 245
      py, px = np.where((pixels == 255) & mask)
    else:
      py, px = np.where(pixels == 0)

    if len(px) > 0:
      portrait_path = " ".join(
          [f"M{x+GRID_OFFSET_X} {y+GRID_OFFSET_Y}h1" for x, y in zip(px, py)]
      )
      svg.append(
          f'<path d="{portrait_path}" stroke="{portrait_color}" stroke-width="1.2"'
          ' shape-rendering="crispEdges">'
      )
      svg.append(
          '  <animate attributeName="opacity"'
          ' values="1;1;0;0;0;0;1"'
          ' keyTimes="0;0.21;0.28;0.88;0.93;0.96;1" dur="14.2s"'
          ' repeatCount="indefinite"/>'
      )
      svg.append("</path>")
  except Exception as e:
    print(f"Could not load portrait images: {e}")

  s_coords = get_shape_coords("springboot.png")
  l_coords = get_shape_coords("langchain.png")
  so_coords = get_shape_coords("solidity.png")

  dist_1 = np.linalg.norm(s_coords[:, np.newaxis] - l_coords, axis=2)
  _, l_idx = linear_sum_assignment(dist_1)
  l_coords_ordered = l_coords[l_idx]

  dist_2 = np.linalg.norm(l_coords_ordered[:, np.newaxis] - so_coords, axis=2)
  _, so_idx = linear_sum_assignment(dist_2)
  so_coords_ordered = so_coords[so_idx]

  path_1 = " ".join([f"M{x+GRID_OFFSET_X} {y+GRID_OFFSET_Y}h1" for x, y in s_coords])
  path_2 = " ".join(
      [f"M{x+GRID_OFFSET_X} {y+GRID_OFFSET_Y}h1" for x, y in l_coords_ordered]
  )
  path_3 = " ".join(
      [
          f"M{x+GRID_OFFSET_X} {y+GRID_OFFSET_Y}h1"
          for x, y in so_coords_ordered
      ]
  )

  svg.append(
      f'<path d="{path_1}" stroke="{logo_color}" stroke-width="{logo_stroke}"'
      ' shape-rendering="crispEdges" opacity="0">'
  )
  svg.append(
      '  <animate attributeName="opacity"'
      ' values="0;0;1;1;1;1;1;1;0;0"'
      ' keyTimes="0;0.21;0.28;0.42;0.51;0.65;0.74;0.88;0.95;1" dur="14.2s"'
      ' repeatCount="indefinite"/>'
  )
  svg.append(
      f'  <animate attributeName="d"'
      f' values="{path_1};{path_1};{path_2};{path_2};{path_3};{path_3};{path_1}"'
      ' keyTimes="0;0.28;0.42;0.51;0.65;0.74;1" dur="14.2s"'
      ' repeatCount="indefinite"/>'
  )
  svg.append("</path>")

  svg.append("</svg>")

  with open(f"{theme}.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg))


if __name__ == "__main__":
  generate_svg("dark")
  generate_svg("light")
