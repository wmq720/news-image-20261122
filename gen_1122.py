#!/usr/bin/env python3
"""news-image-20261122: hand-drawn one-page world news front page.

Draws 35 Sunday 22 November 2026 stories on a 1024x1024 page with PIL.
All art is drawn with primitive shapes (no photos, no AI images).
Run: python3 gen_1122.py  ->  entry.png in this directory.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (25, 25, 25)
RED = (163, 30, 34)
DARKRED = (125, 22, 26)
GRAY = (90, 83, 72)
LIGHT = (233, 226, 210)
OCEAN = (207, 227, 238)
LAND = (217, 196, 154)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(text, font, max_w, max_lines):
    """Greedy word wrap; returns (lines, overflowed_bool)."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    over = len(lines) > max_lines
    return lines[:max_lines], over


def text_block(d, x, y, lines, font, fill, leading):
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=font, fill=fill)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
X0, CW = 22, 980

# ---------------------------------------------------------------- header
d.text((X0, 8), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=RED)
right = "35 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
d.text((X0 + CW - F(SANS_B, 11).getlength(right), 10), right,
       font=F(SANS_B, 11), fill=INK)
d.text((X0, 26), "Sunday 22 November 2026", font=F(SERIF_B, 56), fill=INK)
sub = ("Climate deal goes to a Sunday vote \u00b7 Iran strikes US bases "
       "in Bahrain \u00b7 Russian ship still burning")
d.text(((W - F(SERIF_I, 16).getlength(sub)) / 2, 88), sub,
       font=F(SERIF_I, 16), fill=INK)
d.line([(X0, 110), (X0 + CW, 110)], fill=INK, width=2)

# ---------------------------------------------------------------- numbers
NUMS = [
    ("~200", "nations at the", "COP31 talks"),
    ("03:00", "GMT deadline for", "objections"),
    ("2", "US bases targeted", "in Bahrain"),
    ("16", "crew evacuated", "from Sparta II"),
    ("24", "dead as Nigeria", "funeral boat capsizes"),
    ("723", "seats voted on", "in Hong Kong"),
]
cell = CW / 6
for i, (big, l1, l2) in enumerate(NUMS):
    cx = X0 + i * cell
    if i:
        d.line([(cx - 6, 118), (cx - 6, 166)], fill=(180, 172, 155), width=1)
    d.text((cx, 116), big, font=F(SERIF_B, 29), fill=INK)
    d.text((cx, 150), l1, font=F(SANS, 10), fill=INK)
    d.text((cx, 162), l2, font=F(SANS, 10), fill=INK)
d.line([(X0, 174), (X0 + CW, 174)], fill=INK, width=1)

# ---------------------------------------------------------------- region bar
REGIONS = [("EUROPE 9", (31, 78, 121)), ("MIDDLE EAST 7", (150, 118, 0)),
           ("AMERICAS 4", (91, 74, 138)), ("ASIA 6", (163, 30, 34)),
           ("AFRICA 1", (46, 125, 50)), ("WORLD 8", (69, 90, 100))]
seg = CW / 6
for i, (label, col) in enumerate(REGIONS):
    x = X0 + i * seg
    d.rectangle([x, 178, x + seg - 2, 198], fill=col)
    f = F(SANS_B, 11)
    d.text((x + (seg - 2 - f.getlength(label)) / 2, 183), label,
           font=f, fill=(255, 255, 255))

# ---------------------------------------------------------------- big cards
BIG = [
    dict(n=1, tag="COP31: NEW TEXT", chip="DAY 14",
         kick="1  ANTALYA, T\u00dcRKIYE \u00b7 CLIMATE",
         title="COP31 nears deal as new text tabled",
         summ=("Objections by 03:00 GMT, vote at 06:00. "
               "The EU may walk over fossil fuels."),
         foot="CONFIRMED \u00b7 Reuters"),
    dict(n=2, tag="BAHRAIN: STRUCK", chip="2 BASES",
         kick="2  MANAMA, BAHRAIN \u00b7 IRAN WAR",
         title="Iran strikes US bases in Bahrain",
         summ=("First reported early Sunday after late Saturday strikes. "
               "No injuries; all-clear by Sunday morning."),
         foot="CONFIRMED \u00b7 Reuters"),
    dict(n=3, tag="BALTIC: SHIP ABLAZE", chip="16 SAFE",
         kick="3  GULF OF FINLAND \u00b7 UKRAINE WAR",
         title="Russian cargo ship still burning off Finland",
         summ=("Sparta II, hit by drones Saturday, drifts in Finnish waters, "
               "still burning Sunday. 16 crew safe."),
         foot="CONFIRMED \u00b7 Reuters"),
]


def tag_bar(x, y, w, label, size=11):
    f = F(SANS_B, size)
    tw = f.getlength(label) + 14
    d.rectangle([x, y, x + tw, y + 18], fill=RED)
    d.text((x + 7, y + 2), label, font=f, fill=(255, 255, 255))


def chip(x, y, label, size=9):
    f = F(SANS_B, size)
    tw = f.getlength(label) + 12
    d.rectangle([x, y, x + tw, y + 16], fill=(15, 15, 15))
    d.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))


def illu_big(idx, x, y, w, h):
    if idx == 0:  # earth + thermometer
        d.rectangle([x, y, x + w, y + h], fill=(188, 216, 234))
        cx, cy, r = x + 105, y + 72, 52
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 111, 176))
        d.ellipse([cx - 30, cy - 34, cx + 6, cy - 6], fill=(96, 168, 92))
        d.ellipse([cx - 8, cy + 12, cx + 30, cy + 38], fill=(96, 168, 92))
        d.ellipse([cx + 18, cy - 30, cx + 40, cy - 10], fill=(96, 168, 92))
        d.arc([cx - r - 6, cy - r - 6, cx + r + 6, cy + r + 6],
              start=200, end=330, fill=(255, 255, 255), width=2)
        tx = x + w - 52
        d.rounded_rectangle([tx, y + 16, tx + 16, y + h - 26],
                            radius=8, fill=(255, 255, 255),
                            outline=(120, 120, 120), width=2)
        d.rectangle([tx + 5, y + 34, tx + 11, y + h - 34], fill=(200, 40, 40))
        d.ellipse([tx - 3, y + h - 34, tx + 19, y + h - 12],
                  fill=(200, 40, 40))
        d.text((tx - 2, y + h - 10), "", font=F(SANS, 9), fill=INK)
    elif idx == 1:  # night sky + missiles
        d.rectangle([x, y, x + w, y + h], fill=(16, 26, 51))
        for sx, sy in [(30, 18), (80, 30), (150, 14), (210, 26), (260, 16),
                       (55, 48), (120, 40), (190, 52), (240, 44), (300, 36)]:
            d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                      fill=(255, 255, 255))
        d.ellipse([x + w - 78, y + 12, x + w - 46, y + 44], fill=(238, 230, 200))
        for mx, my in [(40, 60), (130, 44), (220, 66)]:
            d.line([(x + mx, y + my), (x + mx + 46, y + my - 16)],
                   fill=(255, 170, 60), width=3)
            d.ellipse([x + mx + 44, y + my - 20, x + mx + 54, y + my - 10],
                      fill=(255, 210, 90))
        d.ellipse([x + 26, y + h - 46, x + 66, y + h - 6], fill=(255, 140, 40))
        d.ellipse([x + 36, y + h - 36, x + 56, y + h - 16], fill=(255, 210, 90))
        for bx, bw, bh in [(150, 26, 58), (182, 20, 40), (208, 30, 66),
                           (244, 22, 46), (272, 26, 60)]:
            d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                        fill=(5, 7, 15))
            for wy in range(y + h - bh + 6, y + h - 6, 10):
                d.rectangle([x + bx + 5, wy, x + bx + 9, wy + 4],
                            fill=(255, 220, 120))
    else:  # burning cargo ship
        d.rectangle([x, y, x + w, y + h], fill=(232, 130, 58))
        d.ellipse([x + w - 84, y + 14, x + w - 36, y + 62], fill=(250, 214, 150))
        d.rectangle([x, y + 92, x + w, y + h], fill=(47, 111, 143))
        for wy in (102, 118):
            for wx in range(0, w, 44):
                d.arc([x + wx, y + wy, x + wx + 34, y + wy + 12],
                      start=180, end=360, fill=(255, 255, 255), width=2)
        d.rectangle([x + 34, y + 78, x + w - 30, y + 100], fill=(34, 38, 43))
        for cx0, cc in [(52, (200, 60, 60)), (104, (60, 120, 180)),
                        (156, (220, 170, 60)), (208, (90, 160, 90))]:
            d.rectangle([x + cx0, y + 52, x + cx0 + 44, y + 78], fill=cc)
        for fx in (70, 130, 190, 250):
            d.polygon([(x + fx - 12, y + 56), (x + fx, y + 22),
                       (x + fx + 12, y + 56)], fill=(255, 170, 40))
            d.polygon([(x + fx - 6, y + 56), (x + fx, y + 36),
                       (x + fx + 6, y + 56)], fill=(255, 220, 90))
        for sx, sy, sr in [(150, 30, 10), (168, 20, 13), (186, 30, 9)]:
            d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                      fill=(90, 90, 90))


big_w = int((CW - 20) / 3)
warns = []
for i, c in enumerate(BIG):
    bx = X0 + i * (big_w + 10)
    by = 202
    illu_big(i, bx, by, big_w, 140)
    tag_bar(bx, by, big_w, c["tag"], 11)
    chip(bx, by + 140 - 20, c["chip"], 9)
    d.text((bx, 348), c["kick"], font=F(SANS_B, 12), fill=RED)
    tlines, over = wrap(c["title"], F(SERIF_B, 17), big_w, 3)
    if over:
        warns.append("big title %d over" % c["n"])
    text_block(d, bx, 366, tlines, F(SERIF_B, 17), INK, 21)
    slines, over = wrap(c["summ"], F(SANS, 11), big_w, 2)
    if over:
        warns.append("big summ %d over" % c["n"])
    text_block(d, bx, 432, slines, F(SANS, 11), INK, 14)
    d.text((bx, 470), c["foot"], font=F(SANS_B, 10), fill=DARKRED)

# ---------------------------------------------------------------- small cards
SMALL = [
    dict(n=4, tag="BITCOIN $60K", kick="4  GLOBAL \u00b7 MARKETS",
         title="Bitcoin back above $60,000",
         summ="Rebounds from a two-year low near $55,106 to $60,192. +2.2% in 24h.",
         src="CoinStats"),
    dict(n=5, tag="NATO", kick="5  WARSAW, POLAND \u00b7 SECURITY",
         title="NATO chief visits Warsaw",
         summ="Rutte vows to defend every inch of Poland. NATO council meets Monday.",
         src="Reuters"),
    dict(n=6, tag="TRUMP \u00b7 IRAN", kick="6  WASHINGTON \u00b7 DIPLOMACY",
         title="Trump seeks a \u201cpermanent\u201d deal with Iran",
         summ="Trump wants a deal no president can undo. Iran: enrichment is a red line.",
         src="Dawn"),
    dict(n=7, tag="KYIV: 161 DOWN", kick="7  KYIV, UKRAINE \u00b7 WAR",
         title="Ukraine downs 161 of 186 Russian drones",
         summ="161 of 186 drones downed or suppressed by 08:00 Sunday; 18 sites hit.",
         src="Ukrinform"),
    dict(n=8, tag="F1 LAS VEGAS", kick="8  LAS VEGAS, USA \u00b7 SPORT",
         title="Verstappen wins Las Vegas Grand Prix",
         summ="Holds off Norris by 0.639s. Hamilton and Leclerc collide; both penalised 10s.",
         src="Reuters"),
    dict(n=9, tag="NWSL TITLE", kick="9  KANSAS CITY, USA \u00b7 SPORT",
         title="Kansas City win first NWSL title",
         summ="DiBernardo\u2019s Olympic goal and Debinha\u2019s late strike seal a 2\u20131 win.",
         src="Reuters"),
    dict(n=10, tag="HOOCH: 16", kick="10  MANIPUR, INDIA \u00b7 DISASTER",
         title="India hooch deaths rise to 16",
         summ="Tainted liquor toll hits 16, about 600 in hospital; 6 arrested.",
         src="Xinhua"),
    dict(n=11, tag="BOAT: 24 DEAD", kick="11  BAYELSA, NIGERIA \u00b7 DISASTER",
         title="Nigeria funeral boat toll rises to 24",
         summ="Capsized funeral boat toll rises to 24; search goes on.",
         src="Reuters"),
    dict(n=12, tag="HK: 723 SEATS", kick="12  HONG KONG \u00b7 POLITICS",
         title="Hong Kong votes for 723 seats",
         summ="856 candidates contest 723 seats; turnout 97% by 4pm.",
         src="SCMP"),
    dict(n=13, tag="EU\u2013INDONESIA", kick="13  BRUSSELS \u00b7 TRADE",
         title="EU and Indonesia sign landmark deal",
         summ="After 10 years of talks, tariffs fall on 98.5% of EU lines.",
         src="Reuters"),
]


def illu_small(idx, x, y, w, h):
    if idx == 0:  # bitcoin
        d.rectangle([x, y, x + w, y + h], fill=(16, 26, 51))
        d.ellipse([x + 14, y + 8, x + 50, y + 44], fill=(247, 183, 40))
        d.text((x + 26, y + 12), "B", font=F(SANS_B, 24), fill=(16, 26, 51))
        d.line([(x + 62, y + 40), (x + 86, y + 28), (x + 104, y + 34),
                (x + 128, y + 14)], fill=(90, 200, 90), width=3)
        d.polygon([(x + 128, y + 14), (x + 116, y + 16), (x + 126, y + 26)],
                  fill=(90, 200, 90))
    elif idx == 1:  # nato
        d.rectangle([x, y, x + w, y + h], fill=(31, 78, 121))
        for sx in range(16, w - 10, 18):
            d.ellipse([x + sx, y + 8, x + sx + 5, y + 13], fill=(255, 255, 255))
        d.rectangle([x + 30, y + 26, x + w - 30, y + h], fill=(120, 130, 140))
        for wy in range(y + 32, y + h - 4, 9):
            d.rectangle([x + 36, wy, x + 42, wy + 4], fill=(255, 220, 120))
            d.rectangle([x + w - 48, wy, x + w - 42, wy + 4],
                        fill=(255, 220, 120))
    elif idx == 2:  # two flags
        d.rectangle([x, y, x + w, y + h], fill=(233, 226, 210))
        for fx, cols in [(18, [(178, 34, 52), (255, 255, 255), (178, 34, 52)]),
                         (100, [(0, 122, 61), (255, 255, 255), (218, 0, 0)])]:
            for j, cc in enumerate(cols):
                d.rectangle([x + fx, y + 8 + j * 12, x + fx + 70, y + 20 + j * 12],
                            fill=cc)
            d.rectangle([x + fx - 2, y + 6, x + fx + 72, y + 46],
                        outline=(120, 120, 120), width=1)
    elif idx == 3:  # drones at night
        d.rectangle([x, y, x + w, y + h], fill=(16, 26, 51))
        for dx, dy in [(30, 16), (80, 26), (130, 14), (160, 30)]:
            d.ellipse([x + dx - 4, y + dy - 4, x + dx + 4, y + dy + 4],
                      fill=(255, 170, 60))
            d.line([(x + dx, y + dy + 4), (x + dx - 6, y + dy + 14)],
                   fill=(255, 170, 60), width=2)
        d.polygon([(x + 100, y + 30), (x + 108, y + 40), (x + 120, y + 40),
                   (x + 110, y + 48), (x + 114, y + 58), (x + 100, y + 52),
                   (x + 86, y + 58), (x + 90, y + 48), (x + 80, y + 40),
                   (x + 92, y + 40)], fill=(255, 210, 90))
    elif idx == 4:  # chequered flag + track
        d.rectangle([x, y, x + w, y + h], fill=(30, 30, 34))
        for r in range(3):
            for cix in range(8):
                if (r + cix) % 2 == 0:
                    d.rectangle([x + 14 + cix * 12, y + 8 + r * 12,
                                 x + 26 + cix * 12, y + 20 + r * 12],
                                fill=(255, 255, 255))
        d.line([(x + 120, y + 44), (x + 160, y + 30), (x + w - 12, y + 36)],
               fill=(220, 60, 60), width=4)
        d.ellipse([x + 150, y + 24, x + 162, y + 36], fill=(255, 255, 255))
    elif idx == 5:  # football pitch
        d.rectangle([x, y, x + w, y + h], fill=(46, 125, 50))
        d.ellipse([x + w / 2 - 16, y + 12, x + w / 2 + 16, y + 44],
                  outline=(255, 255, 255), width=2)
        d.line([(x + w / 2, y + 6), (x + w / 2, y + h - 4)],
               fill=(255, 255, 255), width=2)
        d.ellipse([x + 22, y + 30, x + 44, y + 52], fill=(255, 255, 255))
        d.ellipse([x + 30, y + 38, x + 36, y + 44], fill=(20, 20, 20))
    elif idx == 6:  # bottle + warning
        d.rectangle([x, y, x + w, y + h], fill=(232, 180, 90))
        d.rectangle([x + 30, y + 14, x + 54, y + 48], fill=(60, 40, 20))
        d.rectangle([x + 38, y + 6, x + 46, y + 14], fill=(60, 40, 20))
        d.polygon([(x + 130, y + 8), (x + 158, y + 46), (x + 102, y + 46)],
                  fill=(200, 40, 40))
        d.text((x + 126, y + 24), "!", font=F(SANS_B, 16), fill=(255, 255, 255))
    elif idx == 7:  # boat on water
        d.rectangle([x, y, x + w, y + h], fill=(47, 111, 143))
        d.polygon([(x + 40, y + 30), (x + 150, y + 30), (x + 136, y + 46),
                   (x + 56, y + 46)], fill=(120, 72, 30))
        d.rectangle([x + 88, y + 16, x + 100, y + 30], fill=(200, 200, 200))
        for wy in (48,):
            for wx in range(6, w - 20, 34):
                d.arc([x + wx, y + wy, x + wx + 26, y + wy + 8],
                      start=180, end=360, fill=(255, 255, 255), width=2)
    elif idx == 8:  # ballot box
        d.rectangle([x, y, x + w, y + h], fill=(233, 226, 210))
        d.rectangle([x + 60, y + 22, x + 130, y + 50], fill=(163, 30, 34))
        d.rectangle([x + 78, y + 22, x + 112, y + 27], fill=(25, 25, 25))
        d.rectangle([x + 84, y + 8, x + 106, y + 22], fill=(255, 255, 255),
                    outline=(120, 120, 120), width=1)
        d.line([(x + 140, y + 16), (x + 148, y + 26), (x + 164, y + 8)],
               fill=(46, 125, 50), width=4)
    else:  # EU stars + containers
        d.rectangle([x, y, x + w, y + h], fill=(188, 216, 234))
        for k in range(8):
            import math
            a = k * math.pi / 4
            sx = x + 40 + int(22 * math.cos(a))
            sy = y + 27 + int(18 * math.sin(a))
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(247, 200, 40))
        for cx0, cc in [(92, (200, 60, 60)), (128, (60, 120, 180)),
                        (164, (220, 170, 60))]:
            d.rectangle([x + cx0, y + 26, x + cx0 + 30, y + 46], fill=cc)


sm_w = int((CW - 32) / 5)
sm_h = 143
for row in range(2):
    for col in range(5):
        c = SMALL[row * 5 + col]
        sx = X0 + col * (sm_w + 8)
        sy = 496 + row * (sm_h + 6)
        illu_small(row * 5 + col, sx, sy, sm_w, 54)
        tag_bar(sx, sy, sm_w, c["tag"], 8)
        d.text((sx, sy + 58), c["kick"], font=F(SANS_B, 10), fill=RED)
        tlines, over = wrap(c["title"], F(SANS_B, 13), sm_w, 2)
        if over:
            warns.append("small title %d over" % c["n"])
        text_block(d, sx, sy + 72, tlines, F(SANS_B, 13), INK, 16)
        slines, over = wrap(c["summ"], F(SANS, 10), sm_w, 2)
        if over:
            warns.append("small summ %d over" % c["n"])
        text_block(d, sx, sy + 106, slines, F(SANS, 10), INK, 12.5)
        d.text((sx, sy + 132), "Source: " + c["src"], font=F(SANS, 9),
               fill=GRAY)

# ---------------------------------------------------------------- map + briefs
d.text((X0, 794), "WHERE IT HAPPENED", font=F(SANS_B, 13), fill=INK)
d.text((X0, 808), "Red numbers mark stories 1\u201313 on the map.",
       font=F(SERIF_I, 10), fill=GRAY)
d.text((342, 794), "ALSO ON SUNDAY 22 NOVEMBER \u2014 22 MORE STORIES",
       font=F(SANS_B, 13), fill=INK)
mx0, my0, mw, mh = X0, 822, 308, 122
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=OCEAN,
            outline=(120, 110, 90), width=1)
# rough continents (hand-drawn blobs, no text inside the map)
d.polygon([(mx0 + 8, my0 + 28), (mx0 + 30, my0 + 14), (mx0 + 62, my0 + 10),
           (mx0 + 86, my0 + 18), (mx0 + 96, my0 + 30), (mx0 + 88, my0 + 44),
           (mx0 + 70, my0 + 52), (mx0 + 58, my0 + 66), (mx0 + 40, my0 + 70),
           (mx0 + 28, my0 + 58), (mx0 + 12, my0 + 44)], fill=LAND)
d.polygon([(mx0 + 88, my0 + 6), (mx0 + 100, my0 + 4), (mx0 + 104, my0 + 10),
           (mx0 + 94, my0 + 14)], fill=LAND)
d.polygon([(mx0 + 62, my0 + 78), (mx0 + 78, my0 + 74), (mx0 + 92, my0 + 82),
           (mx0 + 88, my0 + 100), (mx0 + 76, my0 + 118), (mx0 + 66, my0 + 104),
           (mx0 + 58, my0 + 88)], fill=LAND)
d.polygon([(mx0 + 150, my0 + 62), (mx0 + 168, my0 + 54), (mx0 + 188, my0 + 58),
           (mx0 + 196, my0 + 72), (mx0 + 188, my0 + 92), (mx0 + 176, my0 + 108),
           (mx0 + 162, my0 + 96), (mx0 + 152, my0 + 78)], fill=LAND)
d.polygon([(mx0 + 150, my0 + 50), (mx0 + 170, my0 + 30), (mx0 + 200, my0 + 18),
           (mx0 + 240, my0 + 12), (mx0 + 280, my0 + 18), (mx0 + 300, my0 + 30),
           (mx0 + 292, my0 + 44), (mx0 + 260, my0 + 52), (mx0 + 230, my0 + 48),
           (mx0 + 210, my0 + 58), (mx0 + 190, my0 + 52), (mx0 + 168, my0 + 56)],
          fill=LAND)
for ex, ey in [(250, 70), (262, 76), (244, 80)]:
    d.ellipse([mx0 + ex, my0 + ey, mx0 + ex + 8, my0 + ey + 5], fill=LAND)
d.polygon([(mx0 + 258, my0 + 96), (mx0 + 282, my0 + 92), (mx0 + 296, my0 + 100),
           (mx0 + 288, my0 + 114), (mx0 + 264, my0 + 112)], fill=LAND)
# red numbered dots 1-13 (positions nudged apart by hand)
DOTS = [(206, 864), (224, 876), (196, 830), (140, 864), (178, 836),
        (104, 864), (200, 846), (66, 858), (88, 854), (248, 871),
        (172, 890), (265, 874), (162, 846)]
for i, (dx, dy) in enumerate(DOTS, start=1):
    d.ellipse([dx - 7, dy - 7, dx + 7, dy + 7], fill=RED,
              outline=(255, 255, 255), width=1)
    f = F(SANS_B, 8)
    s = str(i)
    d.text((dx - f.getlength(s) / 2, dy - 5), s, font=f, fill=(255, 255, 255))

BRIEFS = [
    (14, "COP31 deadlock; groups call it \u2018most disappointing COP\u2019. (Al Jazeera)"),
    (15, "Iran to begin rolling blackouts from Sunday as war damage bites. (AFP)"),
    (16, "Hormuz tanker attacks at highest level since the war began. (Gulf News)"),
    (17, "Houthis deny Mecca threat; Saudi alert issued, then lifted. (Times Now)"),
    (18, "Saudi coalition says it downed a Houthi missile aimed west. (Yeni Safak)"),
    (19, "Zelensky seeks ceasefire to free 15 occupied villages. (Ukrainska Pravda)"),
    (20, "Ukraine guards down a new Russian Filin cruise missile. (Ukrinform)"),
    (21, "Kyiv: Russia lost 2,310 troops in a day; total ~1,637,170. (Ukrinform)"),
    (22, "Qatar team in Tehran; minister meets CENTCOM chief in Doha. (Yeni Safak)"),
    (23, "China opposes FCC vote on Chinese telecoms in US numbers. (Reuters)"),
    (24, "Myanmar government calls an ASEAN decision \u2018unfair, unbalanced\u2019. (Reuters)"),
    (25, "Indonesia factory fire kills 3; 36 workers missing in West Java. (Reuters)"),
    (26, "North Korea moves its 2027 Pyongyang marathon to October. (Reuters)"),
    (27, "Iraq MPs probe Basra power fire that killed 4, injured 35. (Shafaq News)"),
    (28, "PL: Leeds 4-1 Chelsea, Arsenal 2-2 Newcastle, City 1-1 Fulham. (AFP)"),
    (29, "US stocks in worst week since the pandemic: Dow -8%, Nasdaq -10%. (IBD)"),
    (30, "Brent $92.57, down 3.41% for a third weekly fall. (FinanceFeeds)"),
    (31, "Gold down ~9.4% in a week, biggest drop in eight months. (Weekly recap)"),
    (32, "Asteroid \u20182026 QQ8\u2019, a 2m \u2018mini-moon\u2019, leaves in early December. (CNN)"),
    (33, "SpaceX Cargo Dragon splashes down off LA with lab-grown tissue. (NASA)"),
    (34, "Curiosity finds \u2018potato-chip\u2019 crystals at its Nazca site. (Times of India)"),
    (35, "Signal blocks in-app screenshots on Android and iOS. (Daily AI Brief)"),
]
bf = F(SANS, 9)
bnf = F(SANS_B, 9)
for i, (n, txt) in enumerate(BRIEFS):
    col = 0 if i < 11 else 1
    bx = 342 + col * 334
    by = 812 + (i % 11) * 12.5
    num = str(n) + "  "
    d.text((bx, by), num, font=bnf, fill=RED)
    d.text((bx + bnf.getlength(num), by), txt, font=bf, fill=INK)
    w = bnf.getlength(num) + bf.getlength(txt)
    if w > 326:
        warns.append("brief %d over by %.0fpx" % (n, w - 326))

# ---------------------------------------------------------------- date check
d.rectangle([X0, 949, X0 + CW, 1001], outline=RED, width=2)
d.text((X0 + 8, 953), "DATE CHECK", font=F(SANS_B, 11), fill=RED)
dc = ("Wires read up to 05:30 UTC, Sunday 22 November 2026. Counted as Sunday news: "
      "Bahrain strikes (late Saturday, first reported early Sunday); Sparta II (hit Saturday, "
      "still burning Sunday); EU\u2013Indonesia deal (signed Saturday, announced Sunday); tolls "
      "updated Sunday; Las Vegas GP and NWSL final (Saturday night US time, so Sunday). "
      "Left out: Russia\u2019s 400-drone barrage (Fri 20 Nov), Peru quake (Fri 20 Nov), Kryvyi Rih "
      "(Fri night), El Chapo Isidro (Fri night), Kuwait air base (Wed 18 Nov), Kerch Bridge, "
      "Shenzhen (Thu 19 Nov). Not yet: COP31 vote 06:00 GMT, ATP final 17:00 UTC.")
dlines, over = wrap(dc, F(SANS, 9), CW - 16, 3)
if over:
    warns.append("datecheck over")
text_block(d, X0 + 8, 967, dlines, F(SANS, 9), INK, 11.5)

# ---------------------------------------------------------------- footer
foot = ("Sources: Reuters, BBC, Al Jazeera, AP, AFP, DW, Straits Times, Sky News, CNA, ABC, "
        "Times of India, Guardian, Kyiv Independent \u00b7 Every story names its outlet "
        "\u00b7 Original drawings")
d.text((X0, 1006), foot, font=F(SANS, 9), fill=GRAY)

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
print("stories:", len(BIG) + len(SMALL) + len(BRIEFS),
      "numbers:", [c["n"] for c in BIG] + [c["n"] for c in SMALL] +
      [n for n, _ in BRIEFS])
print("regions sum:", sum(v for _, v in
      [(r[0], int(r[0].rsplit(" ", 1)[1])) for r in REGIONS]))
print("warnings:", warns if warns else "none")
