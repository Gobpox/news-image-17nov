#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: one newspaper front page that sums up
Tuesday 17 November 2026 in a single 1024x1024 PNG. Pure Pillow, no network,
no randomness, no timestamps: the same bytes every run."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 243, 230)
CARD = (255, 253, 244)
INK = (20, 32, 46)
RED = (179, 49, 42)
GREY = (96, 104, 112)
LIGHT = (233, 226, 205)
FD = "/usr/share/fonts/truetype/dejavu/"

def F(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

REGION_COLOR = {
    "EUROPE": (36, 86, 166), "MIDDLE EAST": (179, 49, 42),
    "ASIA": (14, 122, 95), "AFRICA": (176, 110, 10),
    "GLOBAL": (106, 79, 163), "AMERICAS": (31, 122, 140),
    "US": (31, 122, 140), "RUSSIA": (90, 74, 140),
}

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(d, x, y, text, font, fill, maxw, leading, max_lines=None):
    lines = wrap(d, text, font, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def center(d, y, text, font, fill, cx=W // 2):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)

def badge(d, x, y, n, r=11):
    d.ellipse([x - r - 1.6, y - r - 1.6, x + r + 1.6, y + r + 1.6], fill=(255, 253, 244))
    d.ellipse([x - r, y - r, x + r, y + r], fill=RED)
    f = SANS_B(13 if n < 10 else 11)
    s = str(n)
    w = d.textlength(s, font=f)
    d.text((x - w / 2, y - 8), s, font=f, fill=(255, 255, 255))

HEROES = [
    (1, "EUROPE", "EUROPE · WAR", "bridge",
     "Ukraine hits Crimean Bridge again — span falls into strait",
     "Road span in the strait; rail resumed. Zelenskyy hails “unprecedented operation”."),
    (2, "MIDDLE EAST", "MIDDLE EAST · WAR", "hormuz",
     "Iran drones hit US radar in Bahrain; US jets strike Qeshm",
     "All drones downed, US & Bahrain say. Iran says mines set tanker ablaze — unverified."),
    (3, "ASIA", "ASIA · DIPLOMACY", "quad",
     "Trump holds first Quad summit in Manila",
     "US, India, Japan & Australia: minerals deals. Trump–Xi–Putin to meet in Shenzhen."),
]

CARDS = [
    (4, "AFRICA", "AFRICA · HEALTH", "virus",
     "Ebola in DR Congo tops 11,000 cases",
     "WHO: 5,400 dead; doubled in 3 months; no vaccine."),
    (5, "GLOBAL", "GLOBAL · CLIMATE", "climate",
     "COP31 split over fossil-fuel phase-out",
     "Draft seeks $120bn/yr climate finance by 2035; ends Friday."),
    (6, "AMERICAS", "AMERICAS · HEALTH", "measles",
     "Three countries lose measles-free status",
     "PAHO: US, Mexico, Bolivia. US held 26 yrs; 5,700+ cases."),
    (7, "US", "US · MARKETS", "chart",
     "Nvidia sales double; Dow falls 849 points",
     "Quarterly sales hit $115.8bn as AI stocks slide."),
    (8, "MIDDLE EAST", "MIDDLE EAST · GAZA", "tents",
     "UN told Gaza risks collapse",
     "Winter floods ruin food; 1.4m face acute hunger; aid held up."),
    (9, "ASIA", "ASIA · POLITICS", "building",
     "Mongolia's president says he will resign",
     "He denies a $25m graft claim; parliament must accept."),
    (10, "EUROPE", "EUROPE · POLITICS", "parliament",
     "Serbia students take parliament majority",
     "Student list holds 140 of 250 seats; Vučić party in opposition."),
    (11, "ASIA", "ASIA · LABOUR", "shirt",
     "Bangladesh garment workers tear-gassed",
     "Workers seek Tk 30,000/mo, up from 12,500; 37 factories shut."),
    (12, "RUSSIA", "RUSSIA · AIR CRASH", "plane",
     "Russian An-12 crash kills all 19 aboard",
     "Air force plane down near Kemerovo, Siberia; fault suspected."),
    (13, "AFRICA", "AFRICA · JUSTICE", "gavel",
     "Mozambique puts Mondlane on trial",
     "5 charges over deadly 2024 protests; he denies them."),
]

ALSO = [
    "Russia: record 1,441 drones downed overnight",
    "Kyiv: Dnipro bridges hit; power, water cut",
    "UN: Ukraine civilian deaths top all of 2025",
    "Prague: two trains collide; 46 injured",
    "France strike: 146,000 march (CGT: 500,000)",
    "Poland: Tusk govt survives vote 242–200",
    "Deutsche Bank −6% after huge data leak",
    "Moldova shuts airspace as drone nears capital",
    "Turkey police seize broadcaster Sözcü TV",
    "Pope Leo XIV back from South America tour",
    "UK sanctions 8 Israeli settlement firms",
    "Israel: Kahana elected Knesset speaker 66–52",
    "Settlers kill woman, 72, near Jericho",
    "Oman hosts Iran talks on shipping safety",
    "Cyclone Akvan grows; Odisha evacuates",
    "India: bus in Uttarakhand gorge; 8 dead",
    "Japan protests Russian jet near Fukuoka",
    "China–Canada: more tariff cuts agreed",
    "Malaysia–France: strategic partnership sealed",
    "Thailand to scrap tariffs on US goods",
    "IMF lifts S. Korea 2026 growth to 3.9%",
    "Brazil thrash Singapore 7–0; Vinícius hat-trick",
    "Norway win 3–2 in Denmark; Haaland twice",
    "Togo beat Algeria 3–0 in AFCON qualifier",
    "Kenya: WFP feeds 30,000 fleeing Ethiopia",
    "Haiti: Aristide party fields no candidates",
    "US Senate: Van Hollen challenges Schumer",
    "Australia eases backpacker visa curbs",
    "M6.6 Banda Sea quake felt in Darwin",
    "Apple outage: Pay, iCloud, App Store hit",
]

# ---------------- scenes (flat, schematic; labels carry the meaning) --------
SKY = (207, 224, 235)
SEA = (84, 138, 178)
LAND = (216, 196, 148)
SMOKE = (120, 124, 130)

def scene_bridge(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=SKY)
    d.rectangle([x0, y1 - 26, x1, y1], fill=SEA)
    for i in range(3):
        d.line([x0, y1 - 20 + i * 6, x1, y1 - 20 + i * 6], fill=(120, 170, 200), width=1)
    deck = y0 + 44
    d.rectangle([x0 + 26, deck - 26, x0 + 34, deck], fill=INK)
    d.rectangle([x1 - 60, deck - 26, x1 - 52, deck], fill=INK)
    d.line([x0 + 4, deck, x0 + 130, deck], fill=INK, width=5)
    d.line([x1 - 128, deck, x1 - 4, deck], fill=INK, width=5)
    # suspension cables from both pylons
    for px in (x0 + 30, x1 - 56):
        for ex in (px - 22, px - 8, px + 10, px + 24):
            d.line([px, deck - 26, ex, deck], fill=(70, 80, 92), width=1)
    # small ship passing under the standing span
    sx, sy = x1 - 108, y1 - 14
    d.polygon([(sx, sy), (sx + 34, sy), (sx + 28, sy + 7), (sx + 5, sy + 7)], fill=(60, 70, 84))
    d.rectangle([sx + 12, sy - 6, sx + 24, sy], fill=(60, 70, 84))
    # fallen span, tilted in the water
    d.polygon([(x0 + 138, deck + 16), (x1 - 136, deck + 8), (x1 - 132, deck + 20), (x0 + 142, deck + 28)], fill=INK)
    for cx, cy, r in [(x0 + 120, y0 + 22, 13), (x0 + 140, y0 + 15, 17), (x1 - 120, y0 + 20, 12)]:
        d.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=SMOKE)

def scene_hormuz(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(170, 205, 225))
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 30), (x0 + 90, y0 + 44), (x0, y0 + 38)], fill=LAND)
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 26), (x0 + 150, y1 - 40), (x0, y1 - 30)], fill=LAND)
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 + 4
    d.polygon([(cx - 52, cy + 8), (cx + 40, cy + 8), (cx + 28, cy + 20), (cx - 40, cy + 20)], fill=INK)
    d.rectangle([cx - 30, cy - 2, cx + 8, cy + 8], fill=(90, 90, 96))
    d.polygon([(cx + 16, cy - 16), (cx + 24, cy - 2), (cx + 8, cy - 2)], fill=(232, 120, 40))
    d.polygon([(cx + 20, cy - 24), (cx + 26, cy - 8), (cx + 14, cy - 8)], fill=(240, 180, 50))
    # distant second tanker, upper right of the strait
    d.polygon([(x1 - 92, y0 + 40), (x1 - 48, y0 + 40), (x1 - 54, y0 + 48), (x1 - 86, y0 + 48)], fill=(90, 100, 114))
    d.rectangle([x1 - 80, y0 + 33, x1 - 60, y0 + 40], fill=(90, 100, 114))
    for wx in range(x0 + 16, x1 - 12, 34):
        d.arc([wx, y1 - 22, wx + 18, y1 - 10], start=200, end=340, fill=(70, 120, 160), width=2)
    for dx, dy in [(-96, -22), (-70, -30), (88, -26)]:
        d.polygon([(cx + dx, cy + dy), (cx + dx + 16, cy + dy + 4), (cx + dx, cy + dy + 8)], fill=INK)
    d.arc([x0 + 18, cy - 18, x0 + 52, cy + 16], start=270, end=60, fill=INK, width=3)
    d.line([x0 + 35, cy + 14, x0 + 35, cy + 26], fill=INK, width=3)

def flag(d, x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if kind == "us":
        for i in range(5):
            d.rectangle([x, y + i * h // 5, x + w, y + (i + 1) * h // 5], fill=(200, 60, 55) if i % 2 == 0 else (245, 245, 245))
        d.rectangle([x, y, x + w * 0.42, y + h * 0.55], fill=(40, 60, 140))
    elif kind == "in":
        d.rectangle([x, y, x + w, y + h // 3], fill=(240, 140, 40))
        d.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(245, 245, 245))
        d.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(40, 140, 70))
        d.ellipse([x + w / 2 - 4, y + h / 2 - 4, x + w / 2 + 4, y + h / 2 + 4], outline=(40, 60, 160), width=2)
    elif kind == "jp":
        d.rectangle([x, y, x + w, y + h], fill=(248, 248, 248))
        d.ellipse([x + w / 2 - 7, y + h / 2 - 7, x + w / 2 + 7, y + h / 2 + 7], fill=(200, 40, 50))
    else:
        d.rectangle([x, y, x + w, y + h], fill=(35, 60, 150))
        for sx, sy in [(8, 6), (22, 12), (34, 5), (14, 20), (30, 22)]:
            d.text((x + sx, y + sy), "*", font=SANS_B(11), fill=(255, 255, 255))

def scene_quad(d, b):
    x0, y0, x1, y1 = b
    d.rectangle(b, fill=(222, 232, 220))
    kinds = ["us", "in", "jp", "au"]
    fw, fh, gap = 62, 40, 14
    total = 4 * fw + 3 * gap
    sx = x0 + (x1 - x0 - total) // 2
    for i, k in enumerate(kinds):
        fx = sx + i * (fw + gap)
        d.line([fx + fw // 2, y0 + 12, fx + fw // 2, y0 + 66], fill=INK, width=2)
        flag(d, fx, y0 + 12, fw, fh, k)
    d.rectangle([x0 + 30, y1 - 26, x1 - 30, y1 - 16], fill=(120, 84, 50))
    for i in range(4):
        px = sx + i * (fw + gap) + fw // 2
        d.ellipse([px - 7, y1 - 40, px + 7, y1 - 26], fill=(70, 80, 95))

def mini_bg(d, b, color):
    d.rectangle(b, fill=color)

def scene_card(d, kind, b):
    x0, y0, x1, y1 = b
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    if kind == "virus":
        mini_bg(d, b, (232, 222, 240))
        for ang in range(0, 360, 45):
            import math
            ex = cx + 13 * math.cos(math.radians(ang)); ey = cy + 13 * math.sin(math.radians(ang))
            d.line([cx, cy, ex, ey], fill=(130, 70, 160), width=3)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(130, 70, 160))
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(150, 90, 180))
    elif kind == "climate":
        mini_bg(d, b, (250, 232, 190))
        d.ellipse([x0 + 14, y0 + 5, x0 + 36, y0 + 27], fill=(245, 180, 40))
        d.rectangle([cx + 16, y0 + 6, cx + 22, y1 - 8], outline=INK, width=2)
        d.ellipse([cx + 13, y1 - 14, cx + 25, y1 - 2], fill=RED)
        d.rectangle([cx + 18, y1 - 20, cx + 20, y1 - 10], fill=RED)
    elif kind == "measles":
        mini_bg(d, b, (245, 224, 220))
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(250, 205, 170), outline=INK)
        for dx, dy in [(-6, -4), (5, -7), (0, 3), (7, 6), (-8, 7)]:
            d.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2], fill=RED)
    elif kind == "chart":
        mini_bg(d, b, (224, 236, 224))
        d.line([x0 + 10, y0 + 8, x0 + 44, y0 + 8], fill=(40, 150, 70), width=3)
        d.polygon([(x0 + 44, y0 + 3), (x0 + 52, y0 + 8), (x0 + 44, y0 + 13)], fill=(40, 150, 70))
        d.line([x0 + 10, y1 - 22, x1 - 40, y1 - 10], fill=RED, width=3)
        d.line([x1 - 40, y1 - 10, x1 - 14, y1 - 4], fill=RED, width=3)
        d.polygon([(x1 - 14, y1 - 12), (x1 - 6, y1 - 2), (x1 - 20, y1 - 1)], fill=RED)
    elif kind == "tents":
        mini_bg(d, b, (205, 218, 230))
        for tx in (x0 + 16, cx - 16, x1 - 48):
            d.polygon([(tx, y1 - 6), (tx + 16, y0 + 8), (tx + 32, y1 - 6)], fill=(240, 240, 235), outline=INK)
        for rx in range(x0 + 12, x1 - 8, 22):
            d.line([rx, y0 + 4, rx - 3, y0 + 12], fill=(70, 110, 160), width=2)
    elif kind == "building":
        mini_bg(d, b, (228, 230, 240))
        d.rectangle([cx - 26, cy - 2, cx + 26, y1 - 5], fill=(200, 205, 220), outline=INK)
        d.polygon([(cx - 30, cy - 2), (cx + 30, cy - 2), (cx, cy - 15)], fill=(120, 130, 160))
        d.line([cx + 34, y0 + 6, cx + 34, y1 - 10], fill=RED, width=3)
        d.polygon([(cx + 28, y1 - 16), (cx + 40, y1 - 16), (cx + 34, y1 - 6)], fill=RED)
    elif kind == "parliament":
        mini_bg(d, b, (230, 226, 205))
        for i, px in enumerate(range(cx - 27, cx + 28, 11)):
            d.rectangle([px, y0 + 9, px + 6, y1 - 9], fill=(170, 160, 135), outline=INK)
        d.rectangle([cx - 32, y0 + 4, cx + 32, y0 + 9], fill=INK)
        d.rectangle([cx - 32, y1 - 9, cx + 32, y1 - 4], fill=INK)
    elif kind == "shirt":
        mini_bg(d, b, (220, 236, 240))
        d.polygon([(cx - 8, y0 + 6), (cx - 22, y0 + 12), (cx - 16, y0 + 22), (cx - 10, y0 + 19),
                   (cx - 10, y1 - 5), (cx + 10, y1 - 5), (cx + 10, y0 + 19), (cx + 16, y0 + 22),
                   (cx + 22, y0 + 12), (cx + 8, y0 + 6)], fill=(90, 160, 200), outline=INK)
    elif kind == "plane":
        mini_bg(d, b, (215, 222, 232))
        d.polygon([(cx - 30, cy + 6), (cx + 18, cy - 8), (cx + 30, cy - 2), (cx - 14, cy + 12)], fill=(90, 98, 112))
        d.polygon([(cx - 30, cy + 6), (cx - 40, cy - 6), (cx - 32, cy - 7), (cx - 20, cy + 2)], fill=(90, 98, 112))
        for dx, dy, r in [(38, 8, 7), (48, 12, 10)]:
            d.ellipse([cx + dx - r, cy + dy - r * 0.7, cx + dx + r, cy + dy + r * 0.7], fill=SMOKE)
    elif kind == "gavel":
        mini_bg(d, b, (238, 228, 205))
        d.line([cx - 16, cy - 12, cx + 6, cy + 10], fill=(140, 95, 45), width=5)
        d.rectangle([cx - 24, cy - 18, cx - 2, cy - 8], fill=(110, 72, 30))
        d.rectangle([cx - 18, y1 - 8, cx + 22, y1 - 4], fill=(110, 72, 30))
    else:
        mini_bg(d, b, LIGHT)

SCENES = {"bridge": scene_bridge, "hormuz": scene_hormuz, "quad": scene_quad}

# ---------------- world map (dotted grid from continent ellipses) -----------
LAND_ELLIPSES = [
    (-100, 47, 42, 16), (-88, 36, 22, 10), (-152, 64, 14, 5), (-42, 73, 12, 6),
    (-62, -12, 14, 17), (-70, -32, 8, 12),
    (16, 52, 20, 9), (14, 63, 10, 6), (-3, 43, 9, 5), (22, 40, 10, 5), (-2, 54, 4, 4),
    (18, 8, 21, 15), (24, -16, 15, 13), (47, -19, 5, 7),
    (62, 52, 52, 13), (88, 34, 26, 13), (78, 21, 9, 9), (104, 16, 8, 9),
    (48, 24, 13, 7), (35, 39, 10, 5), (138, 37, 5, 5),
    (113, -1, 16, 4), (131, -3, 8, 3),
    (134, -25, 15, 8), (172, -42, 5, 5),
]

def is_land(lon, lat):
    for clon, clat, rx, ry in LAND_ELLIPSES:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
            return True
    return False

PINS = [  # (number, lon, lat, dx, dy)
    (1, 31, 45, 10, -10), (2, 50, 26, 14, 8), (3, 121, 14, 0, 0),
    (4, 23, -1, 0, 0), (5, 30, 37, -14, -10), (6, -108, 38, 0, 0),
    (7, -74, 41, 4, -4), (8, 34, 31, 6, 12), (9, 106, 47, 0, 0),
    (10, 21, 44, -14, 6), (11, 90, 24, 0, 0), (12, 86, 55, 0, 0),
    (13, 35, -19, 0, 0),
]
BRIEF_DOTS = [
    (37, 56), (30, 50), (14, 50), (2, 49), (21, 52), (13, 52), (28, 47),
    (29, 41), (12, 42), (0, 51), (35, 32), (58, 23), (85, 20), (79, 30),
    (130, 33), (116, 40), (101, 3), (100, 14), (127, 37), (-52, -10),
    (10, 60), (1, 8), (36, -1), (-72, 19), (-77, 39), (151, -33),
    (130, -5), (-122, 37),
]

def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(240, 236, 218), outline=INK, width=1)
    cols, rows = 60, 30
    for r in range(rows):
        lat = 75 - (r + 0.5) * (135 / rows)
        for c in range(cols):
            lon = -180 + (c + 0.5) * (360 / cols)
            if is_land(lon, lat):
                px = x0 + (c + 0.5) * w / cols
                py = y0 + (r + 0.5) * h / rows
                d.ellipse([px - 1.7, py - 1.7, px + 1.7, py + 1.7], fill=(110, 116, 92))
    def proj(lon, lat):
        return (x0 + (lon + 180) / 360 * w, y0 + (75 - lat) / 135 * h)
    for lon, lat in BRIEF_DOTS:
        px, py = proj(lon, lat)
        d.ellipse([px - 2.4, py - 2.4, px + 2.4, py + 2.4], fill=RED)
    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        badge(d, px + dx, py + dy, n, r=8)

# ---------------- page assembly ----------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    center(d, 8, "THE WORLD'S NEWS IN ONE PICTURE", SANS_B(13), INK)
    d.line([10, 30, W - 10, 30], fill=INK, width=2)
    center(d, 36, "Tuesday 17 November 2026", SERIF_B(44), INK)
    d.rectangle([10, 88, W - 10, 112], fill=RED)
    center(d, 94, "43 STORIES · 6 CONTINENTS · ALL FROM TUESDAY 17 NOVEMBER 2026", SANS_B(14), (255, 255, 255))
    # heroes (v3: shorter scenes, larger decks at 13px)
    hy, hh, hw, hgap = 120, 224, 329, 8
    for i, (n, region, kicker, scene, head, deck) in enumerate(HEROES):
        x = 10 + i * (hw + hgap)
        d.rectangle([x, hy, x + hw, hy + hh], fill=CARD, outline=INK, width=2)
        SCENES[scene](d, (x + 2, hy + 2, x + hw - 2, hy + 94))
        badge(d, x + 16, hy + 16, n, r=12)
        d.text((x + 10, hy + 99), kicker, font=SANS_B(11), fill=REGION_COLOR[region])
        y = text_block(d, x + 10, hy + 115, head, SANS_B(20), INK, hw - 20, 24, 3)
        text_block(d, x + 10, y + 4, deck, SANS(13), (40, 48, 58), hw - 20, 16, 2)
    # cards (v3: taller cards, 36px scenes, headlines at 16px bold)
    cy0, chh, cw, cgap = 352, 146, 194, 8
    for i, (n, region, kicker, scene, head, deck) in enumerate(CARDS):
        x = 10 + (i % 5) * (cw + cgap)
        y = cy0 + (i // 5) * (chh + cgap)
        d.rectangle([x, y, x + cw, y + chh], fill=CARD, outline=INK, width=1)
        scene_card(d, scene, (x + 2, y + 2, x + cw - 2, y + 38))
        badge(d, x + 12, y + 20, n, r=10)
        d.text((x + 8, y + 43), kicker, font=SANS_B(10), fill=REGION_COLOR[region])
        yy = text_block(d, x + 8, y + 57, head, SANS_B(16), INK, cw - 16, 19, 3)
        fit = max(0, (y + chh - 4 - (yy + 2)) // 12)
        text_block(d, x + 8, yy + 2, deck, SANS(10), (40, 48, 58), cw - 16, 12, min(3, fit))
    # bottom headers
    d.text((10, 660), "WHERE IT HAPPENED", font=SANS_B(14), fill=INK)
    d.text((326, 660), "ALSO ON TUESDAY 17 NOVEMBER", font=SANS_B(15), fill=INK)
    strap = "30 MORE STORIES · Nos 14–43"
    d.text((W - 10 - d.textlength(strap, font=SANS_B(11)), 663), strap, font=SANS_B(11), fill=GREY)
    d.line([10, 682, W - 10, 682], fill=INK, width=2)
    # map + tallies (left, narrower in v3)
    draw_map(d, 10, 690, 300, 152)
    d.text((10, 846), "Pins 1–13: heroes & cards. Dots: stories 14–43.", font=SANS(9), fill=GREY)
    ty = 864
    ty = text_block(d, 10, ty, "BY REGION — Europe 12 · Asia 10 · Middle East 6 · Americas 6 · Africa 4 · Russia 2 · Oceania 2 · Global 1", SANS(11), INK, 300, 13, 3)
    ty = text_block(d, 10, ty + 3, "FIELDS — War · Politics · Health · Climate · Markets · Disaster · Justice · Sport", SANS(11), INK, 300, 13, 3)
    text_block(d, 10, ty + 3, "DATE CHECK — Excluded: anything first reported before Tuesday 17 Nov 2026.", SANS_B(10), RED, 300, 13, 2)
    # also list (right, two columns of 15, all at 13px)
    lx, lw, row_h = 326, 336, 18
    for i, item in enumerate(ALSO):
        col, row = i // 15, i % 15
        x = lx + col * (lw + 16)
        y = 690 + row * row_h
        num = f"{14 + i}."
        d.text((x, y), num, font=SANS_B(13), fill=RED)
        nw = d.textlength(num + " ", font=SANS_B(13))
        assert d.textlength(item, font=SANS(13)) <= lw - nw, f"also item {14 + i} too wide"
        d.text((x + nw, y), item, font=SANS(13), fill=INK)
    # footer
    d.line([10, 972, W - 10, 972], fill=INK, width=2)
    center(d, 980, "Every story happened or was first reported on Tuesday 17 November 2026. Contested claims are marked as claims.", SANS_B(11), INK)
    center(d, 997, "Sources: Reuters · AP · AFP · BBC · Al Jazeera · WHO · UN · PAHO · IMF  |  One picture, one day: Tuesday 17 November 2026.", SANS(10), GREY)
    img.save("entry.png", optimize=True)
    print("wrote entry.png")

if __name__ == "__main__":
    main()
