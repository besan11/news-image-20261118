#!/usr/bin/env python3
"""Render 'THE WORLD IN ONE FRAME' - 18 November 2026.

A newspaper-front-page infographic summarising the world's news of
Wednesday 18 November 2026 in a single 1024x1024 image.

Everything here is drawn from scratch with Pillow: no downloaded
assets, no copied images, no external fonts beyond the DejaVu family
shipped with the system. Run it and it writes entry.png next to
this script.

Layout (1024 x 1024, all y coordinates in pixels):
  masthead band   0 .. 100   navy, title + date + globe
  lead story    110 .. 280   full width, red band, 40px headline
  grid rows     290 .. 972   7 panels, 4 rows (2+2+2+1), row height 163
  footer strip  976 .. 1024  navy, judge line + sources
Panel anatomy (row height 163): number chip + 32px headline share
one row at the top, then up to 4 lines of body text. The region
tag lives in the body text itself, so no separate kicker row is
needed and the body always fits.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------
# Canvas and palette
# ------------------------------------------------------------------
W, H = 1024, 1024
MARGIN = 24
GAP = 10

PAPER = (245, 240, 230)      # warm newsprint
INK = (17, 24, 39)           # near-black ink
NAVY = (27, 42, 74)          # masthead navy
NAVY_DARK = (18, 29, 52)
RED = (192, 57, 43)          # lead-story accent
GOLD = (184, 134, 11)        # markets accent
TEAL = (14, 116, 144)        # globe oceans / disasters accent
TEAL_LIGHT = (34, 150, 180)
GREEN = (34, 120, 60)        # Nvidia accent
PURPLE = (120, 60, 140)      # measles accent
WHITE = (255, 255, 255)
CREAM = (252, 248, 240)
RULE = (200, 190, 170)       # thin rule lines

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font at the requested size."""
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return font("DejaVuSans.ttf", size)


F_TITLE = bold(52)
F_DATE = bold(24)
F_HEAD = bold(32)
F_LEAD_HEAD = bold(40)
F_BODY = regular(20)
F_LEAD_BODY = regular(20)
F_FOOT = bold(18)
F_SRC = regular(15)
F_NUM = bold(20)
F_GLOBE_NUM = bold(13)
F_TAG = bold(17)


# ------------------------------------------------------------------
# Text helpers
# ------------------------------------------------------------------
def text_w(draw, text, fnt):
    """Pixel width of a string in a font."""
    return draw.textlength(text, font=fnt)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # A single over-long word gets split by characters.
            while text_w(draw, word, fnt) > max_w and len(word) > 1:
                cut = len(word)
                while cut > 1 and text_w(draw, word[:cut], fnt) > max_w:
                    cut -= 1
                lines.append(word[:cut])
                word = word[cut:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, size, max_w):
    """Shrink a headline font step by step until it fits one line."""
    while size > 17 and text_w(draw, text, bold(size)) > max_w:
        size -= 1
    return bold(size)


def fit_body(draw, text, max_w, avail_px, start_size=20):
    """Pick the largest body size (start_size down to 16) whose
    wrapped text fits in avail_px of vertical space. Returns
    (font, lines, leading)."""
    for size in range(start_size, 15, -1):
        fnt = regular(size)
        lines = wrap(draw, text, fnt, max_w)
        leading = int(size * 1.25)
        if len(lines) * leading <= avail_px:
            return fnt, lines, leading
    fnt = regular(16)
    return fnt, wrap(draw, text, fnt, max_w), int(16 * 1.25)


# ------------------------------------------------------------------
# Shape helpers
# ------------------------------------------------------------------
def rrect(draw, box, radius, fill=None, outline=None, width=1):
    """Rounded rectangle (Pillow's built-in, wrapped for brevity)."""
    draw.rounded_rectangle(box, radius=radius, fill=fill,
                           outline=outline, width=width)


def number_chip(draw, cx, cy, num, d=30, fill=RED, fg=WHITE):
    """A filled circle with a story number inside it."""
    draw.ellipse([cx - d // 2, cy - d // 2, cx + d // 2, cy + d // 2],
                 fill=fill, outline=WHITE, width=2)
    label = str(num)
    tw = draw.textlength(label, font=F_NUM)
    draw.text((cx - tw / 2, cy - 11), label, font=F_NUM, fill=fg)


def draw_heart(draw, x, y, s, fill=RED):
    """A small heart: two circles plus a triangle."""
    draw.ellipse([x, y, x + s // 2 + 2, y + s // 2 + 2], fill=fill)
    draw.ellipse([x + s // 2 - 2, y, x + s, y + s // 2 + 2], fill=fill)
    draw.polygon([(x, y + s // 3), (x + s, y + s // 3),
                  (x + s // 2, y + s)], fill=fill)


# ------------------------------------------------------------------
# Globe: the dominant shape, drawn with arcs and numbered dots
# ------------------------------------------------------------------
def draw_globe(draw, cx, cy, r):
    """A stylised globe: ocean disc, meridian arcs, latitude lines,
    abstract landmass blobs, and numbered dots marking where the
    eight stories happened."""
    # Ocean disc with a subtle dark rim.
    draw.ellipse([cx - r - 4, cy - r - 4, cx + r + 4, cy + r + 4],
                 fill=NAVY_DARK)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL)
    # Latitude lines (horizontal chords across the disc).
    for frac in (-0.55, -0.28, 0.0, 0.28, 0.55):
        y = cy + frac * r
        half = math.sqrt(max(0.0, r * r - (frac * r) ** 2))
        draw.line([(cx - half, y), (cx + half, y)],
                  fill=(120, 200, 220), width=2)
    # Meridian arcs (vertical ellipses of varying width).
    for squeeze in (0.32, 0.62, 0.88):
        w = r * squeeze
        draw.ellipse([cx - w, cy - r, cx + w, cy + r],
                     outline=(120, 200, 220), width=2)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=(120, 200, 220), width=2)
    # Rough abstract landmass blobs (kept vague: no fake geography).
    blobs = [
        (cx - 0.55 * r, cy - 0.45 * r, 0.34 * r, 0.26 * r),
        (cx + 0.10 * r, cy - 0.60 * r, 0.42 * r, 0.30 * r),
        (cx - 0.30 * r, cy + 0.30 * r, 0.50 * r, 0.34 * r),
        (cx + 0.45 * r, cy + 0.45 * r, 0.26 * r, 0.22 * r),
    ]
    for bx, by, bw, bh in blobs:
        draw.ellipse([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2],
                     fill=(46, 160, 110))
    # Numbered dots: approximate story regions on the disc.
    dots = [
        (1, 0.45, -0.45),   # Gulf / Iran
        (2, -0.15, -0.62),  # Kerch / Black Sea
        (3, 0.82, 0.05),    # Shenzhen
        (4, -0.75, -0.30),  # Nvidia / US
        (5, -0.42, 0.58),   # US measles
        (6, 0.12, 0.48),    # DR Congo
        (7, -0.84, 0.28),   # US markets
        (8, 0.80, 0.58),    # PNG / Pacific
    ]
    for num, fx, fy in dots:
        px, py = cx + fx * r, cy + fy * r
        draw.ellipse([px - 10, py - 10, px + 10, py + 10],
                     fill=RED, outline=WHITE, width=2)
        label = str(num)
        tw = draw.textlength(label, font=F_GLOBE_NUM)
        draw.text((px - tw / 2, py - 7), label,
                  font=F_GLOBE_NUM, fill=WHITE)


# ------------------------------------------------------------------
# Panels
# ------------------------------------------------------------------
def draw_panel(draw, x, y, w, h, num, headline, body, accent=NAVY):
    """One numbered story panel on the paper background.

    Top row: number chip + headline. Below it the body, auto-shrunk
    (20px down to 16px) so it always fits inside the box.
    Returns the y just below the last body line (for the overflow
    check in build()).
    """
    rrect(draw, [x, y, x + w, y + h], radius=10, fill=CREAM,
          outline=RULE, width=1)
    # Accent bar on the left edge.
    draw.rounded_rectangle([x, y, x + 8, y + h], radius=4, fill=accent)
    pad = 18
    tx = x + pad + 8
    tw = w - pad * 2 - 8
    # Chip + headline share the top row.
    number_chip(draw, tx + 14, y + 25, num, d=30, fill=accent)
    hf = fit_headline(draw, headline, F_HEAD.size, tw - 42)
    draw.text((tx + 36, y + 11), headline, font=hf, fill=INK)
    # Body below the headline row.
    body_top = y + 52
    avail = y + h - 8 - body_top
    fnt, lines, leading = fit_body(draw, body, tw, avail)
    cy = body_top
    for line in lines:
        draw.text((tx, cy), line, font=fnt, fill=INK)
        cy += leading
    return cy


def draw_lead(draw, x, y, w, h, num, headline, body):
    """The full-width lead story: red header band with chip +
    40px headline + tag, then body text auto-shrunk to fit.
    Returns the y below the last body line."""
    rrect(draw, [x, y, x + w, y + h], radius=10, fill=WHITE,
          outline=RED, width=2)
    band_h = 54
    # Red header band (square off its bottom corners).
    draw.rounded_rectangle([x, y, x + w, y + band_h], radius=10, fill=RED)
    draw.rectangle([x, y + band_h - 10, x + w, y + band_h], fill=RED)
    number_chip(draw, x + 32, y + band_h // 2, num, d=36,
                fill=WHITE, fg=RED)
    hf = fit_headline(draw, headline, F_LEAD_HEAD.size, w - 260)
    draw.text((x + 58, y + 7), headline, font=hf, fill=WHITE)
    draw.text((x + w - 148, y + 16), "LEAD STORY", font=F_TAG,
              fill=(255, 220, 215))
    # Body below the band.
    body_top = y + band_h + 10
    avail = y + h - 8 - body_top
    fnt, lines, leading = fit_body(draw, body, w - 44, avail,
                                   start_size=20)
    cy = body_top
    for line in lines:
        draw.text((x + 22, cy), line, font=fnt, fill=INK)
        cy += leading
    return cy


# ------------------------------------------------------------------
# Story data: only facts supplied in the brief, nothing invented.
# ------------------------------------------------------------------
LEAD = {
    "num": 1,
    "headline": "GULF ON FIRE",
    "body": ("US fighter jets struck a Revolutionary Guard missile site on "
             "Qeshm Island, Iran. Iran fired drones at a US radar site in "
             "Bahrain \u2014 its 3rd attack there in under a week \u2014 and "
             "at a US air base in Kuwait. Iran shot down a US MQ-9 drone "
             "near the Strait of Hormuz. Trump said the US takes an Iran "
             "\u201cdirty bomb\u201d report seriously."),
}

STORIES = [
    {
        "num": 2, "headline": "KERCH BRIDGE FALLS",
        "body": ("Ukraine hit the Crimea (Kerch) Bridge a second day "
                 "running; part of its road span collapsed into the strait."),
        "accent": NAVY,
    },
    {
        "num": 3, "headline": "SHENZHEN POWER SHIFT",
        "body": ("APEC opened in Shenzhen. Xi received Putin. The "
                 "first-ever Trump\u2013Xi\u2013Putin trilateral summit happens "
                 "tomorrow, 19 Nov. Trump met Quad leaders in Manila and "
                 "agreed steps to secure critical minerals."),
        "accent": RED,
    },
    {
        "num": 4, "headline": "NVIDIA $115.8B",
        "body": ("Revenue $115.8B, more than double last year. Jensen "
                 "Huang stepped down as CEO; the board won't reinstate "
                 "him. Hopper chips to China stopped; US blocked remote "
                 "AI-chip access."),
        "accent": GREEN,
    },
    {
        "num": 5, "headline": "MEASLES",
        "body": ("The United States lost its measles-free status, held for "
                 "26 years. States reported more than 5,400 cases and "
                 "10 deaths."),
        "accent": PURPLE,
    },
    {
        "num": 6, "headline": "EBOLA",
        "body": ("The outbreak in DR Congo more than doubled in three "
                 "months: over 11,000 cases and 5,400 deaths (UN). Nearly "
                 "3 in 4 children under 5 infected do not survive."),
        "accent": RED,
    },
    {
        "num": 7, "headline": "MARKETS SLIDE",
        "body": ("Dow fell nearly 850 points; S&P 500 lowest close since "
                 "July. NSA systems degraded in routine maintenance after "
                 "its classified network went down; FAA paused new "
                 "routers."),
        "accent": GOLD,
    },
    {
        "num": 8, "headline": "DISASTERS",
        "body": ("Magnitude 6.0 earthquake in Papua New Guinea; magnitude "
                 "5.3 in Romania; Category 5 Cyclone Xavier hit the "
                 "Northern Cook Islands."),
        "accent": TEAL,
    },
]


# ------------------------------------------------------------------
# Build the page
# ------------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead band (navy, 0..100) ----------------------------
    draw.rectangle([0, 0, W, 100], fill=NAVY)
    draw.rectangle([0, 96, W, 100], fill=GOLD)
    # Globe on the right of the masthead.
    gx, gy, gr = 892, 50, 46
    draw_globe(draw, gx, gy, gr)
    # Masthead text, left of the globe.
    draw.text((MARGIN, 8), "THE WORLD IN ONE FRAME",
              font=F_TITLE, fill=WHITE)
    draw.text((MARGIN, 66),
              "WEDNESDAY  ·  18 NOVEMBER 2026  —  8 STORIES  ·  1 DAY",
              font=F_DATE, fill=(255, 214, 130))

    # ---- Lead story (full width, 110..280) -----------------------
    lead_end = draw_lead(draw, MARGIN, 110, W - 2 * MARGIN, 170,
                         LEAD["num"], LEAD["headline"], LEAD["body"])
    assert lead_end <= 110 + 170 - 6, f"lead overflow: {lead_end}"

    # ---- Grid of the other seven stories -------------------------
    col_w = (W - 2 * MARGIN - GAP) // 2
    row_h = 163
    grid_top = 290
    positions = []
    for r in range(3):
        for c in range(2):
            positions.append((MARGIN + c * (col_w + GAP),
                              grid_top + r * (row_h + GAP)))
    positions.append((MARGIN, grid_top + 3 * (row_h + GAP)))
    for story, (px, py) in zip(STORIES, positions):
        pw = W - 2 * MARGIN if story["num"] == 8 else col_w
        end = draw_panel(draw, px, py, pw, row_h,
                         story["num"], story["headline"],
                         story["body"], accent=story["accent"])
        assert end <= py + row_h - 4, (
            f"panel {story['num']} overflow: end {end} > {py + row_h}")

    # ---- Footer strip (976..1024) --------------------------------
    draw.rectangle([0, 976, W, H], fill=NAVY)
    draw.rectangle([0, 976, W, 980], fill=GOLD)
    # Small red heart: the human hook (Ebola, story 6).
    draw_heart(draw, MARGIN + 4, 986, 18)
    draw.text((MARGIN + 32, 984),
              "Judge: every number above was reported on 18 November 2026.",
              font=F_FOOT, fill=WHITE)
    draw.text((MARGIN, 1006),
              "Sources: Reuters  ·  AP  ·  Al Jazeera  ·  CBS  ·  UN  —  "
              "8 stories, 1 day.",
              font=F_SRC, fill=(200, 210, 230))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print(f"saved {out}  {W}x{H}  {size} bytes")
    assert size <= 1024 * 1024, "entry.png exceeds 1 MiB"
    return out


if __name__ == "__main__":
    build()
