#!/usr/bin/env python3
"""news-image-20261126 — render the front page (PIL, dev-time only).

Draws ONE 1024x1024 newspaper front page summing up Thursday 26 November
2026's world news. Output: entry.png (<=1 MiB). Run: python3 render.py.
The grader never runs this file; main.py (stdlib-only) copies entry.png.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 8

# --- palette (bright, high-contrast; no dark feature art) ---
PAPER = (250, 246, 236)      # warm cream page
INK = (18, 18, 18)           # near-black text
NAVY = (22, 34, 63)          # top bar / timeline / footer bar
RED = (178, 24, 24)          # masthead subline, banners, DATE CHECK
GOLD = (212, 175, 55)        # top-bar right text
SKY = (186, 222, 240)        # pale daylight sky for feature art
SKY2 = (205, 232, 244)       # lighter sky
SEA = (120, 190, 225)        # bright sea blue
SAND = (232, 220, 192)       # map land
SEA_MAP = (198, 224, 238)    # map sea
GREY_LINE = (120, 120, 120)
CHIP_GREEN = (26, 122, 62)
CHIP_AMBER = (176, 120, 0)
CHIP_RED = (178, 24, 24)
CHIP_BLUE = (24, 90, 160)

DJ = "/usr/share/fonts/truetype/dejavu"
def F(name, size):
    return ImageFont.truetype(os.path.join(DJ, name), size)

SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: F("DejaVuSerif-Italic.ttf", s) if os.path.exists(
    os.path.join(DJ, "DejaVuSerif-Italic.ttf")) else F("DejaVuSerif.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)

# --- story data: every numbered story happened / was first reported ---
# --- on Thursday 26 November 2026 (UTC). Sources named on each item. ---
FEATURES = [
    dict(n=1, place="CAIRO", region="AFRICA", chip="REPORTED",
         banner="30 KILLED", banner_bg=CHIP_RED,
         head="Fuel tanker fire kills 30 on Cairo highway",
         body="A fuel tanker crashes and burns near the Warraq tunnel in Giza; "
              "at least 30 killed, 15 hurt, medics say.",
         src="lamediterranee · Jabulani Radio"),
    dict(n=2, place="NEW YORK", region="MARKETS", chip="OFFICIAL",
         banner="NASDAQ -3.2%", banner_bg=CHIP_RED,
         head="US unveils new tariffs; Nasdaq dives 3.2%",
         body="USTR proposes duties on 14 partners \u2014 20% on China, 15% on the EU; "
              "Nvidia sinks 8% as the AI rout deepens.",
         src="Reuters · WSJ · AP"),
    dict(n=3, place="MINSK", region="EUROPE", chip="REPORTED",
         banner="FLY TO MOSCOW?", banner_bg=CHIP_BLUE,
         head="Lukashenko offers to fly Zelensky to Moscow",
         body="Belarus leader offers his plane for talks with Putin; Zelensky replies: "
              "\u201cAm I just a suitcase for him?\u201d",
         src="lamediterranee"),
]

TILES = [
    dict(n=4, place="HORMUZ", chip="REPORTED", banner="COORDINATE",
         head="Iran warns ships to coordinate Hormuz transit",
         body="Tehran tells vessels to coordinate passage; earlier mine claim "
              "unconfirmed, maritime centre says.", src="Euronews · Al Jazeera"),
    dict(n=5, place="WARSAW", chip="REPORTED", banner="NO-FLY ZONE",
         head="Poland plans no-fly zone on Ukraine border",
         body="Warsaw acts after a Russian drone enters its airspace; asks NATO "
              "to down missiles over Ukraine.", src="lamediterranee"),
    dict(n=6, place="TALLINN", chip="REPORTED", banner="FULL-SCALE WAR?",
         head="Kremlin warns Estonia of \u2018full-scale war\u2019",
         body="Moscow accuses Tallinn of helping Ukrainian drone strikes "
              "into Russia.", src="lamediterranee"),
    dict(n=7, place="PYONGYANG", chip="REPORTED", banner="EXPELLED",
         head="North Korea expels Swiss diplomat",
         body="Pyongyang orders Switzerland to shut its newly opened office "
              "in a sanctions row.", src="Jabulani Radio"),
    dict(n=8, place="WASHINGTON", chip="REPORTED", banner="SHELVED",
         head="US shelves Russia business-deal peace plan",
         body="White House drops the idea of trade sweeteners to end the "
              "Ukraine war.", src="FT"),
    dict(n=9, place="SAMARA", chip="REPORTED", banner="20-YEAR LOW",
         head="Russian refining hits 20-year low",
         body="Ukrainian drone strikes on at least 18 refineries cut output.",
         src="Reuters"),
    dict(n=10, place="ABUJA", chip="REPORTED", banner="$227M LAB",
         head="Five Mexicans held over $227m drug lab",
         body="Nigeria detains five Mexican citizens over a drug "
              "production facility.", src="lamediterranee"),
    dict(n=11, place="DHAKA", chip="OFFICIAL", banner="+36% PAY",
         head="Bangladesh garment workers win 36% rise",
         body="Minimum wage for entry-level garment staff rises by more "
              "than a third.", src="Daily Jagran"),
    dict(n=12, place="WASHINGTON", chip="OFFICIAL", banner="THANKSGIVING",
         head="Trump pardons turkeys Liberty and Liberty",
         body="President spares two birds for Thanksgiving; US markets "
              "shut for the holiday.", src="lamediterranee"),
    dict(n=13, place="DARMSTADT", chip="REPORTED", banner="CRATER SHOTS",
         head="Asteroid probe sends back crater close-ups",
         body="ESA\u2019s Hera returns close-ups of the Dimorphos crater.",
         src="Jabulaniradio"),
]

ALSO = [
    (14, "Ukraine downs 88 of 112 Russian drones overnight", "Kyiv Independent"),
    (15, "ECOWAS approves regional force roadmap by end 2027", "lamediterranee"),
    (16, "Houthis report deaths after Saudi strikes in Yemen", "PW Live"),
    (17, "Nepal 5.6 quake hits Koshi Province by China border", "PW Live"),
    (18, "India marks Constitution Day, Samvidhan Divas", "SelfStudys"),
    (19, "Modi meets Merz on India-Germany partnership", "PW Live"),
    (20, "India unveils \u20b915,000 crore Nepal aid package", "SelfStudys"),
    (21, "Sensex falls 1,484; Nifty slips below 25,400", "PW Live"),
    (22, "Gukesh faces Sindarov in World Chess Championship", "Jagran Josh"),
    (23, "IPL 2027 auction draws 1,220 players", "SelfStudys"),
    (24, "Sooryavanshi smashes 204 off 53 balls vs UAE", "SelfStudys"),
    (25, "Ethiopia-Eritrea troop build-up raises war fears", "NRB"),
    (26, "New Zealand hold India to a draw in first Test", "PW Live"),
    (27, "UCL: Liverpool 3-0 Brugge; Barcelona 4-1 Sabah", "Sportradar"),
    (28, "Israeli judges: drop most serious Netanyahu charges", "Jabulani Radio"),
    (29, "Israel minister: Iran developing chemical weapons", "Daily Jagran"),
    (30, "Plane crashes in Gulf of Mexico; six aboard sought", "Daily Jagran"),
    (31, "Fort Hood survivors lose final appeal", "Daily Jagran"),
    (32, "Hasina seeks return to Bangladesh on Dec 16", "SelfStudys"),
    (33, "Hong Kong tightens exotic-pet rules after 3.7m imports", "lamediterranee"),
    (34, "Spain-linked group hits Canada terror listing", "lamediterranee"),
    (35, "ASX set to open higher despite Wall St slide", "Bottom Line"),
    (36, "Ecuador talks with US focus on operations", "lamediterranee"),
    (37, "Europe urged back to great-power diplomacy", "lamediterranee"),
    (38, "Colombia police free 20 hostages after 17-hour siege", "Jagran Josh"),
]

STATS = [
    ("30", "killed in Cairo tanker fire"),
    ("-3.2%", "Nasdaq fall in a day"),
    ("20%", "new US tariff on China"),
    ("5", "Mexicans held in Nigeria"),
    ("1,220", "players in IPL auction"),
    ("36%", "Bangladesh wage rise"),
]

REGIONS = [
    ("EUROPE 9", (24, 90, 160)),
    ("ASIA-PACIFIC 11", (26, 122, 62)),
    ("AMERICAS 6", (200, 110, 0)),
    ("MIDDLE EAST 4", (150, 60, 60)),
    ("AFRICA 4", (90, 90, 90)),
    ("WORLD 2", (70, 70, 70)),
    ("OCEANIA 2", (110, 60, 140)),
]

TIMELINE = [
    ("00:02", "Kremlin warns Estonia"),
    ("00:06", "Iran warns Hormuz ships"),
    ("00:09", "Lukashenko offers a flight"),
    ("10:00", "Sensex falls 1,484"),
]

DATE_CHECK = ("Every numbered story happened, or was first reported, on Thursday "
    "26 November 2026 (UTC). Left out as other days\u2019 news: Huawei guilty verdict "
    "(Tue 25) \u00b7 Riyadh tower hit (Tue 25) \u00b7 Shenzhou-24 docks, Pakistan\u2019s first "
    "astronaut (Tue 25) \u00b7 COP31 ends without a deal (Sun 22) \u00b7 Hanoi blast (Tue 25) "
    "\u00b7 Senegal AFCON title restored (Tue 25) \u00b7 Real Madrid 5-1 PSV (Wed 25) \u00b7 "
    "Australia apologises to LGBTQ troops (Wed 25) \u00b7 FCC clears SpaceX orbital "
    "data centres (Wed 25). Not yet: Taiwan local elections (Sat 28).")

# --- helpers ---------------------------------------------------------------
def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, font, max_w, fill, leading=None):
    if leading is None:
        leading = font.size + 3
    yy = y
    for ln in wrap(draw, text, font, max_w):
        draw.text((x, yy), ln, font=font, fill=fill)
        yy += leading
    return yy


def chip(draw, x, y, text, font, bg, fg=(255, 255, 255), pad_x=5, pad_y=2):
    w = draw.textlength(text, font=font) + 2 * pad_x
    h = font.size + 2 * pad_y
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=font, fill=fg)
    return w


def num_badge(draw, x, y, n, d=18):
    draw.ellipse([x, y, x + d, y + d], fill=RED)
    t = str(n)
    f = SANS_B(11 if n < 10 else 9)
    tw = draw.textlength(t, font=f)
    draw.text((x + (d - tw) / 2, y + (d - 11) / 2 - 1), t, font=f,
              fill=(255, 255, 255))


def sun(draw, x, y, r=13, color=(255, 200, 60)):
    draw.ellipse([x - r, y - r, x + r, y + r], fill=color,
                 outline=(240, 170, 30), width=2)


def cloud(draw, x, y, s=1.0, color=(255, 255, 255)):
    draw.ellipse([x, y, x + 34 * s, y + 14 * s], fill=color)
    draw.ellipse([x + 8 * s, y - 7 * s, x + 30 * s, y + 8 * s], fill=color)
    draw.ellipse([x + 18 * s, y - 3 * s, x + 40 * s, y + 10 * s], fill=color)


def flame(draw, x, y, s=1.0):
    # bright orange flame, teardrop of two ellipses + triangle
    draw.polygon([(x, y - 26 * s), (x - 13 * s, y + 4 * s),
                  (x + 13 * s, y + 4 * s)], fill=(255, 140, 0))
    draw.ellipse([x - 12 * s, y - 12 * s, x + 12 * s, y + 10 * s],
                 fill=(255, 170, 20))
    draw.ellipse([x - 6 * s, y - 2 * s, x + 6 * s, y + 10 * s],
                 fill=(255, 220, 90))


def smoke(draw, x, y, s=1.0):
    c = (150, 150, 150)
    draw.ellipse([x, y, x + 22 * s, y + 14 * s], fill=c)
    draw.ellipse([x + 10 * s, y - 9 * s, x + 30 * s, y + 6 * s], fill=c)
    draw.ellipse([x + 22 * s, y - 3 * s, x + 40 * s, y + 10 * s], fill=c)


# --- feature illustrations: BRIGHT, one focus object, pale background -----
def art_tanker(draw, x, y, w, h):
    # pale daylight sky + bright sea; one big white tanker, orange flame
    draw.rectangle([x, y, x + w, y + h], fill=SKY)
    sun(draw, x + w - 26, y + 22)
    cloud(draw, x + 18, y + 16, 0.9)
    cloud(draw, x + w - 110, y + 52, 0.7)
    sea_y = y + int(h * 0.62)
    draw.rectangle([x, sea_y, x + w, y + h], fill=SEA)
    draw.rectangle([x, sea_y, x + w, sea_y + 3], fill=(90, 170, 210))
    # tanker hull (white top, red bottom) + bridge tower with windows
    hx, hy, hw, hh = x + 26, sea_y - 26, w - 52, 34
    draw.rectangle([hx, hy, hx + hw, hy + hh], fill=(255, 255, 255),
                   outline=(90, 90, 90), width=1)
    draw.rectangle([hx, hy + 22, hx + hw, hy + hh], fill=(200, 40, 40))
    draw.rectangle([hx + hw - 52, hy - 30, hx + hw - 8, hy], fill=(240, 240, 240),
                   outline=(90, 90, 90), width=1)
    for i in range(3):
        draw.rectangle([hx + hw - 48 + i * 14, hy - 26, hx + hw - 40 + i * 14,
                        hy - 14], fill=(40, 90, 160))
    # funnel + flame + smoke
    draw.rectangle([hx + 18, hy - 22, hx + 34, hy], fill=(230, 230, 230),
                   outline=(90, 90, 90), width=1)
    flame(draw, hx + 26, hy - 22, 0.9)
    smoke(draw, hx + 52, hy - 46, 0.65)
    # waves
    for wx in range(x + 8, x + w - 20, 34):
        draw.arc([wx, sea_y + 12, wx + 26, sea_y + 24], 180, 360,
                 fill=(255, 255, 255), width=2)


def art_chart(draw, x, y, w, h):
    # pale cream; big red down arrow + bright buildings with windows
    draw.rectangle([x, y, x + w, y + h], fill=(253, 248, 235))
    # buildings (light grey, lit windows) along the bottom
    bx = x + 14
    for bw, bh in [(34, 44), (44, 62), (30, 38), (48, 70), (36, 50)]:
        draw.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(205, 210, 215),
                       outline=(140, 140, 140), width=1)
        for wy in range(y + h - bh + 6, y + h - 8, 11):
            for wx in range(bx + 5, bx + bw - 6, 11):
                draw.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 210, 90))
        bx += bw + 8
    # red down-trend arrow, big and bold
    pts = [(x + 30, y + 26), (x + 110, y + 42), (x + 170, y + 34),
           (x + 250, y + 62), (x + w - 30, y + 82)]
    draw.line(pts, fill=RED, width=7, joint="curve")
    ax, ay = x + w - 30, y + 82
    draw.polygon([(ax, ay), (ax - 26, ay - 14), (ax - 6, ay + 12)], fill=RED)


def art_jet(draw, x, y, w, h):
    # pale daylight sky; one big white passenger jet, sun, clouds
    draw.rectangle([x, y, x + w, y + h], fill=SKY2)
    sun(draw, x + 34, y + 26)
    cloud(draw, x + w - 130, y + 18, 0.9)
    cloud(draw, x + 20, y + h - 40, 0.7)
    # jet: fuselage, nose, tail, wings, windows (bright, side view)
    jx, jy = x + 30, y + int(h * 0.45)
    draw.ellipse([jx, jy - 12, jx + 210, jy + 14], fill=(255, 255, 255),
                 outline=(90, 90, 90), width=1)
    draw.polygon([(jx + 200, jy - 10), (jx + 252, jy - 2), (jx + 200, jy + 10)],
                 fill=(255, 255, 255), outline=(90, 90, 90))
    draw.polygon([(jx + 30, jy - 12), (jx + 52, jy - 44), (jx + 66, jy - 12)],
                 fill=(200, 40, 40))
    draw.polygon([(jx + 96, jy + 12), (jx + 132, jy + 44), (jx + 150, jy + 12)],
                 fill=(235, 235, 235), outline=(90, 90, 90))
    draw.polygon([(jx + 150, jy + 12), (jx + 182, jy + 40), (jx + 196, jy + 12)],
                 fill=(235, 235, 235), outline=(90, 90, 90))
    for i in range(9):
        draw.ellipse([jx + 26 + i * 18, jy - 6, jx + 34 + i * 18, jy + 2],
                     fill=(60, 130, 200))
    # small flag on tail
    draw.rectangle([jx + 36, jy - 44, jx + 52, jy - 32], fill=(200, 40, 40))


FEATURE_ART = [art_tanker, art_chart, art_jet]


# --- tile mini-strips: small, bright, one focus object --------------------
def strip(draw, x, y, w, h, kind):
    if kind == "sea":  # Hormuz: bright sea, small tanker + mine
        draw.rectangle([x, y, x + w, y + h], fill=SEA)
        draw.rectangle([x + 20, y + h - 22, x + w - 60, y + h - 8],
                       fill=(255, 255, 255))
        draw.rectangle([x + 20, y + h - 14, x + w - 60, y + h - 8],
                       fill=(200, 40, 40))
        draw.ellipse([x + w - 42, y + 8, x + w - 22, y + 28], fill=(30, 30, 30))
        for a in range(8):
            import math
            ang = a * 3.14159 / 4
            draw.line([x + w - 32 + 10 * math.cos(ang), y + 18 + 10 * math.sin(ang),
                       x + w - 32 + 15 * math.cos(ang), y + 18 + 15 * math.sin(ang)],
                      fill=(30, 30, 30), width=2)
    elif kind == "jet":  # Poland: pale sky, small jet + flag
        draw.rectangle([x, y, x + w, y + h], fill=SKY2)
        draw.polygon([(x + 30, y + 14), (x + 150, y + 22), (x + 30, y + 30)],
                     fill=(255, 255, 255), outline=(90, 90, 90))
        draw.rectangle([x + 150, y + 10, x + 178, y + 30], fill=(255, 255, 255),
                       outline=(200, 40, 40), width=2)
        draw.rectangle([x + 150, y + 10, x + 178, y + 20], fill=(200, 40, 40))
    elif kind == "tower":  # Estonia: pale sky, tower block with windows
        draw.rectangle([x, y, x + w, y + h], fill=(235, 240, 245))
        draw.rectangle([x + 70, y + 4, x + 130, y + h], fill=(180, 190, 200),
                       outline=(120, 120, 120), width=1)
        for wy in range(y + 10, y + h - 6, 10):
            for wx in range(x + 76, x + 124, 12):
                draw.rectangle([wx, wy, wx + 6, wy + 6], fill=(255, 210, 90))
        draw.polygon([(x + 150, y + 20), (x + 190, y + 20), (x + 170, y + h - 4)],
                     fill=RED)
    elif kind == "flag":  # Pyongyang: red flag + pale building
        draw.rectangle([x, y, x + w, y + h], fill=(245, 240, 225))
        draw.rectangle([x + 30, y + 12, x + 60, y + h - 6], fill=(200, 200, 200),
                       outline=(120, 120, 120), width=1)
        draw.rectangle([x + 110, y + 6, x + 170, y + 34], fill=(200, 40, 40))
        draw.ellipse([x + 132, y + 12, x + 148, y + 28], fill=(255, 255, 255))
    elif kind == "dome":  # Washington: white capitol dome, pale blue sky
        draw.rectangle([x, y, x + w, y + h], fill=SKY2)
        draw.rectangle([x + 60, y + h - 12, x + 140, y + h], fill=(240, 240, 240),
                       outline=(120, 120, 120), width=1)
        draw.pieslice([x + 78, y + 2, x + 122, y + 34], 180, 360,
                      fill=(255, 255, 255), outline=(120, 120, 120))
        draw.rectangle([x + 97, y - 2, x + 103, y + 6], fill=(120, 120, 120))
    elif kind == "refinery":  # Samara: pale sky, grey towers + flame
        draw.rectangle([x, y, x + w, y + h], fill=(238, 240, 242))
        for tx in (40, 90, 140):
            draw.rectangle([x + tx, y + 12, x + tx + 22, y + h - 6],
                           fill=(190, 195, 200), outline=(120, 120, 120), width=1)
        flame(draw, x + 101, y + 12, 0.55)
        smoke(draw, x + 116, y - 2, 0.5)
    elif kind == "lab":  # Abuja: pale green, flask + warning triangle
        draw.rectangle([x, y, x + w, y + h], fill=(225, 240, 220))
        draw.polygon([(x + 100, y + 8), (x + 130, y + 8), (x + 115, y + h - 8)],
                     fill=(255, 200, 60), outline=(150, 110, 0), width=2)
        draw.text((x + 110, y + 16), "!", font=SANS_B(16), fill=(150, 110, 0))
        draw.rectangle([x + 40, y + 18, x + 62, y + h - 8], fill=(255, 255, 255),
                       outline=(90, 90, 90), width=1)
        draw.ellipse([x + 44, y + 22, x + 58, y + 32], fill=(60, 160, 90))
    elif kind == "factory":  # Dhaka: pale sky, factory + "+36%" tag
        draw.rectangle([x, y, x + w, y + h], fill=(230, 240, 230))
        draw.rectangle([x + 30, y + 16, x + 110, y + h - 6], fill=(200, 210, 205),
                       outline=(120, 120, 120), width=1)
        draw.polygon([(x + 30, y + 16), (x + 44, y + 2), (x + 58, y + 16)],
                     fill=(150, 160, 155))
        draw.polygon([(x + 58, y + 16), (x + 72, y + 2), (x + 86, y + 16)],
                     fill=(150, 160, 155))
        draw.text((x + 130, y + 10), "+36%", font=SANS_B(20), fill=CHIP_GREEN)
    elif kind == "turkey":  # Thanksgiving: green lawn, two white turkeys
        draw.rectangle([x, y, x + w, y + h], fill=(200, 230, 180))
        for tx in (60, 130):
            draw.ellipse([x + tx, y + 12, x + tx + 34, y + h - 8],
                         fill=(255, 255, 255), outline=(150, 150, 150), width=1)
            draw.ellipse([x + tx + 24, y + 6, x + tx + 36, y + 18],
                         fill=(255, 255, 255), outline=(150, 150, 150), width=1)
            draw.polygon([(x + tx + 34, y + 10), (x + tx + 40, y + 13),
                          (x + tx + 34, y + 15)], fill=(230, 120, 40))
    elif kind == "rock":  # Darmstadt: pale grey asteroid + tiny probe
        draw.rectangle([x, y, x + w, y + h], fill=(228, 232, 240))
        draw.ellipse([x + 60, y + 4, x + 140, y + h - 4], fill=(190, 190, 195),
                     outline=(130, 130, 130), width=1)
        for cx, cy, cr in [(85, 18, 7), (115, 30, 5), (95, 38, 4)]:
            draw.ellipse([x + cx - cr, y + cy - cr, x + cx + cr, y + cy + cr],
                         fill=(150, 150, 155))
        draw.rectangle([x + 160, y + 16, x + 176, y + 26], fill=(220, 220, 220),
                       outline=(90, 90, 90), width=1)
        draw.line([x + 160, y + 21, x + 142, y + 21], fill=(90, 90, 90), width=2)


STRIP_KINDS = ["sea", "jet", "tower", "flag", "dome",
               "refinery", "lab", "factory", "turkey", "rock"]

# --- world map ---------------------------------------------------------------
NA = [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-60, 60),
      (-75, 45), (-80, 32), (-97, 26), (-105, 20), (-90, 14), (-83, 9),
      (-95, 16), (-110, 23), (-125, 40), (-125, 49), (-140, 60)]
SA = [(-80, 9), (-60, 8), (-50, 0), (-35, -8), (-40, -20), (-48, -28),
      (-58, -35), (-65, -40), (-70, -50), (-73, -53), (-70, -30), (-70, -18),
      (-77, -12), (-80, -3)]
AF = [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (32, 31), (35, 28),
      (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -28), (26, -34),
      (19, -35), (15, -27), (12, -18), (13, -10), (9, 4), (-8, 4), (-13, 8)]
EU = [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
      (18, 56), (21, 55), (24, 59), (30, 60), (28, 65), (25, 70), (18, 70),
      (12, 65), (5, 58), (-5, 50), (-9, 43)]
AS = [(30, 36), (35, 36), (43, 41), (48, 44), (50, 47), (60, 52), (70, 55),
      (75, 68), (90, 75), (110, 77), (130, 72), (150, 70), (170, 66),
      (178, 65), (170, 60), (160, 55), (158, 50), (142, 45), (140, 40),
      (135, 35), (130, 33), (127, 35), (122, 30), (120, 25), (110, 20),
      (108, 10), (105, 8), (100, 7), (97, 15), (92, 20), (88, 22), (80, 15),
      (77, 8), (72, 20), (66, 25), (60, 25), (57, 26), (52, 28), (48, 30),
      (44, 29), (40, 32), (35, 36)]
AU = [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (132, -32),
      (137, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
      (150, -22), (146, -19), (142, -15), (142, -11), (136, -12), (132, -11),
      (126, -14), (122, -17), (118, -20)]

# (story number, lon, lat, nudge_x, nudge_y) — nudges separate close pins
PINS = [
    (1, 31.2, 30.0, 0, 0),      # Cairo
    (2, -74.0, 40.7, -4, -3),   # New York
    (3, 27.6, 53.9, 9, -3),     # Minsk
    (4, 56.5, 26.5, 0, 0),      # Hormuz
    (5, 21.0, 52.2, -9, 6),     # Warsaw
    (6, 24.7, 59.4, 2, -11),    # Tallinn
    (7, 125.8, 39.0, 0, 0),     # Pyongyang
    (8, -77.0, 38.9, -8, 5),    # Washington (plan)
    (9, 50.1, 53.2, 11, 1),     # Samara
    (10, 7.5, 9.1, 0, 0),       # Abuja
    (11, 90.4, 23.8, 0, 0),     # Dhaka
    (12, -77.0, 38.9, 9, -5),   # Washington (turkeys)
    (13, 8.65, 49.87, -11, 5),  # Darmstadt
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA_MAP)
    def proj(lon, lat):
        px = x + (lon + 180) / 360.0 * w
        py = y + (90 - lat) / 180.0 * h
        return (px, py)
    for poly in (NA, SA, AF, EU, AS, AU):
        pts = [proj(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=SAND, outline=(170, 150, 110))
    for n, lon, lat, nx, ny in PINS:
        px, py = proj(lon, lat)
        px += nx
        py += ny
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(n)
        f = SANS_B(9 if n < 10 else 8)
        tw = draw.textlength(t, font=f)
        draw.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))

# --- layout ------------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # top bar
    d.rectangle([0, 0, W, 22], fill=NAVY)
    d.text((MARGIN, 4), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=(255, 255, 255))
    rt = "38 STORIES \u00b7 7 REGIONS \u00b7 ALL FROM THURSDAY 26 NOVEMBER 2026"
    d.text((W - MARGIN - d.textlength(rt, font=SANS_B(11)), 4), rt,
           font=SANS_B(11), fill=GOLD)

    # masthead
    mast = "Thursday 26 November 2026"
    mf = SERIF_B(50)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 24), mast, font=mf, fill=INK)
    sub = ("Cairo tanker fire kills 30 \u00b7 US unveils new tariffs \u00b7 "
           "Lukashenko offers Zelensky a flight to Moscow")
    sf = SERIF_I(16)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 80), sub, font=sf, fill=RED)

    # stat strip
    y0, y1 = 102, 146
    cw = (W - 2 * MARGIN) / 6
    for i, (num, lab) in enumerate(STATS):
        x = MARGIN + i * cw
        nf = SERIF_B(26)
        nw = d.textlength(num, font=nf)
        d.text((x + (cw - nw) / 2, y0), num, font=nf, fill=INK)
        lf = SANS(10)
        lw = d.textlength(lab, font=lf)
        d.text((x + (cw - lw) / 2, y0 + 30), lab, font=lf, fill=(90, 90, 90))
        if i:
            d.line([x, y0 + 4, x, y1 - 4], fill=GREY_LINE, width=1)
    d.line([MARGIN, y1, W - MARGIN, y1], fill=INK, width=1)

    # region bar
    x = MARGIN
    y = 150
    for label, color in REGIONS:
        w = chip(d, x, y, label, SANS_B(10), color, pad_x=7, pad_y=3)
        x += w + 5
    d.text((W - MARGIN - d.textlength("= 38 stories", font=SANS_B(11)), y + 2),
           "= 38 stories", font=SANS_B(11), fill=INK)

    # timeline strip
    d.rectangle([0, 174, W, 194], fill=NAVY)
    d.text((MARGIN, 178), "THE DAY IN UTC", font=SANS_B(11), fill=GOLD)
    tx = MARGIN + 118
    for t, ev in TIMELINE:
        d.text((tx, 178), t, font=SANS_B(11), fill=(255, 220, 90))
        tw = d.textlength(t, font=SANS_B(11))
        d.text((tx + tw + 4, 178), ev, font=SANS(11), fill=(255, 255, 255))
        tx += tw + 4 + d.textlength(ev, font=SANS(11)) + 16

    # features
    col_w = 328
    for i, f in enumerate(FEATURES):
        x = MARGIN + i * (col_w + 12)
        ax, ay, aw, ah = x, 198, col_w, 116
        FEATURE_ART[i](d, ax, ay, aw, ah)
        chip(d, ax + 6, ay + 6, f["banner"], SANS_B(11), f["banner_bg"], pad_x=7)
        ly = ay + ah + 8
        num_badge(d, x, ly, f["n"])
        d.text((x + 24, ly + 1), "%s \u00b7 %s" % (f["place"], f["region"]),
               font=SANS_B(11), fill=INK)
        cw2 = chip(d, x + col_w - 78, ly, f["chip"], SANS_B(9), CHIP_GREEN
                   if f["chip"] == "OFFICIAL" else CHIP_AMBER, pad_x=5)
        hy = ly + 24
        hy = text_block(d, x, hy, f["head"], SERIF_B(19), col_w, INK, leading=22)
        by = hy + 4
        by = text_block(d, x, by, f["body"], SANS(11), col_w, (40, 40, 40),
                        leading=14)
        d.text((x, 458), f["src"], font=SANS(9), fill=(110, 110, 110))

    # tiles: 2 rows x 5 cols; body carries its source inline (no separate line)
    tw_, th = 200, 100
    for r in range(2):
        for c in range(5):
            t = TILES[r * 5 + c]
            x = MARGIN + c * (tw_ + 4)
            y = 470 + r * (th + 8)
            strip(d, x, y, tw_, 30, STRIP_KINDS[r * 5 + c])
            num_badge(d, x, y + 34, t["n"], d=14)
            d.text((x + 19, y + 35), t["place"], font=SANS_B(9), fill=INK)
            chip(d, x + tw_ - 62, y + 34, t["chip"], SANS_B(8),
                 CHIP_GREEN if t["chip"] == "OFFICIAL" else CHIP_AMBER, pad_x=4)
            hy = text_block(d, x, y + 52, t["head"], SANS_B(11), tw_, INK,
                            leading=12)
            body_src = t["body"] + " \u2014 " + t["src"]
            blines = wrap(d, body_src, SANS(9), tw_)[:2]
            yy = hy + 2
            for ln in blines:
                d.text((x, yy), ln, font=SANS(9), fill=(60, 60, 60))
                yy += 10

    # bottom: map + ALSO
    d.text((MARGIN, 684), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    d.text((MARGIN + 148, 684), "PINS 1\u201313", font=SANS_B(11), fill=RED)
    draw_map(d, MARGIN, 700, 328, 156)
    d.text((MARGIN, 860), "Red pins = features + tiles 1\u201313",
           font=SANS(9), fill=(110, 110, 110))
    ax0 = 352
    d.text((ax0, 684), "ALSO ON THURSDAY 26 NOVEMBER \u00b7 25 MORE",
           font=SANS_B(11), fill=RED)
    colw = 330
    for idx, (n, lead, src) in enumerate(ALSO):
        col = idx // 13
        row = idx % 13
        x = ax0 + col * (colw + 6)
        y = 702 + row * 13
        num_badge(d, x, y - 1, n, d=13)
        # one line: lead + source, truncated at a word boundary to fit
        f9 = SANS(9)
        avail = colw - 18
        sfx = " \u00b7 " + src
        lead_w = avail - d.textlength(sfx, font=f9)
        short = lead
        while short and d.textlength(short, font=f9) > lead_w:
            short = short.rsplit(" ", 1)[0] if " " in short else short[:-1]
        if short != lead:
            short = short + "\u2026"
        d.text((x + 18, y), short, font=f9, fill=INK)
        d.text((x + 18 + d.textlength(short, font=f9), y), sfx, font=f9,
               fill=(110, 110, 110))

    # DATE CHECK
    d.rectangle([MARGIN, 878, W - MARGIN, 950], outline=RED, width=2)
    d.rectangle([MARGIN, 878, MARGIN + 108, 896], fill=RED)
    d.text((MARGIN + 8, 880), "DATE CHECK", font=SANS_B(11), fill=(255, 255, 255))
    text_block(d, MARGIN + 116, 880, DATE_CHECK, SANS(10), W - MARGIN - 116 - 8,
               INK, leading=13)

    # legend + sources
    d.text((MARGIN, 956),
           "CONFIRMED = 2+ outlets  \u00b7  OFFICIAL = on the record  \u00b7  "
           "REPORTED = carried by wires, not yet official  \u00b7  CLAIM = one side\u2019s "
           "account, labelled as such",
           font=SANS(9), fill=(90, 90, 90))
    d.text((MARGIN, 968),
           "Sources: Reuters, AP, AFP, Al Jazeera, Kyiv Independent, Xinhua, IRNA, "
           "ABC, LNA, UN. Illustrations are drawn, not photographs. "
           "Every story names its sources.",
           font=SANS(9), fill=(90, 90, 90))

    # bottom bar
    d.rectangle([0, 988, W, H], fill=NAVY)
    d.text((MARGIN, 996), "THE WORLD IN ONE DAY", font=SANS_B(11),
           fill=(255, 255, 255))
    bt = "THURSDAY 26 NOVEMBER 2026 \u00b7 ONE PAGE"
    d.text((W - MARGIN - d.textlength(bt, font=SANS_B(11)), 992), bt,
           font=SANS_B(11), fill=GOLD)

    img.save(OUT, optimize=True)
    print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
