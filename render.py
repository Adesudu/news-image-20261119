#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261119: a one-page newspaper
front page summing up the world news of Thursday 19 November 2026.

Pure Pillow drawing (no external assets). Run once at build time:
    python3 render.py   ->  entry.png (1024x1024, < 1 MiB)

Stories are real events reported on 19 November 2026 (Reuters, AP, BBC,
TradingView/Bloomberg, Fast Company): Anthropic's record IPO debuts on
Nasdaq; GTA VI launches worldwide; Trump, Putin and Xi meet in Shenzhen
while Europe's allies gather in Berlin; Hakeem Jeffries is set to become
the first Black Speaker of the US House; Israel launches a ground
operation in central Gaza; the Crimea bridge is hit again; Cyclone Akvan
nears India's coast; Voyager 1 reaches one light-day from Earth.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 246, 238)      # newsprint cream
INK = (24, 24, 30)           # near-black
NAVY = (18, 38, 74)          # masthead band
RED = (178, 30, 40)          # accent red
BLUE = (30, 84, 150)         # accent blue
GOLD = (176, 124, 30)        # accent gold
TEAL = (14, 96, 88)
GREY = (96, 92, 86)
RULE = (190, 182, 168)
LIGHT = (236, 230, 216)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, fill, width, leading=None):
    """Draw wrapped paragraph; return y after last line."""
    lh = leading or int(fnt.size * 1.28)
    for line in wrap(d, text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def headline(d, x, y, text, size, width, fill=INK, fnt_path=SERIF):
    fnt = F(fnt_path, size)
    return para(d, x, y, text, fnt, fill, width, leading=int(size * 1.12))


def kicker(d, x, y, text, color=RED):
    fnt = F(SANS_B, 15)
    d.text((x, y), text.upper(), font=fnt, fill=color)
    return y + 22


def rule(d, x0, y, x1, width=2, color=RULE):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def draw_ipo_chart(d, x, y, w, h):
    """Rising market chart with ANT ticker: dark panel, green line, $83."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 52))
    # grid
    for gy in range(1, 4):
        yy = y + h * gy // 4
        d.line([(x + 14, yy), (x + w - 14, yy)], fill=(52, 84, 112), width=1)
    # rising line + area
    pts = [(x + 20 + i * (w - 40) // 8, y + h - 26 - int(v * (h - 60)))
           for i, v in enumerate([0.08, 0.14, 0.12, 0.30, 0.38, 0.52, 0.66, 0.80, 0.94])]
    area = pts + [(pts[-1][0], y + h - 12), (pts[0][0], y + h - 12)]
    d.polygon(area, fill=(24, 88, 66))
    d.line(pts, fill=(74, 222, 158), width=4, joint="curve")
    d.ellipse([pts[-1][0] - 7, pts[-1][1] - 7, pts[-1][0] + 7, pts[-1][1] + 7],
              fill=(74, 222, 158))
    d.text((x + 18, y + 12), "ANT  ·  NASDAQ", font=F(SANS_B, 20),
           fill=(190, 210, 225))
    d.text((x + w - 150, y + 8), "$83", font=F(SERIF, 44), fill=(255, 255, 255))
    d.text((x + 18, y + h - 34), "priced above its $70–$78 range",
           font=F(SANS, 16), fill=(150, 175, 195))


def draw_vice_city(d, x, y, w, h):
    """Neon Vice City sunset: pink-orange sky, sun, palms, skyline."""
    for i in range(h):
        t = i / h
        r = int(255 - 60 * t)
        g = int(120 + 60 * t)
        b = int(150 + 40 * t)
        d.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    # sun
    cx, cy, r = x + w // 2, y + h // 2 - 6, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 90))
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10],
              fill=(255, 240, 170))
    # skyline silhouettes
    import random
    rnd = random.Random(7)
    base = y + h
    bx = x
    while bx < x + w:
        bw = rnd.randint(28, 52)
        bh = rnd.randint(28, 84)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(38, 16, 54))
        bx += bw + 4
    # palm silhouettes
    for px in (x + 26, x + w - 34):
        d.line([(px, base), (px + 4, base - 74)], fill=(30, 12, 44), width=5)
        for ang in (-50, -25, 0, 25, 50):
            import math
            a = math.radians(ang - 90)
            ex = px + 4 + int(34 * math.cos(a))
            ey = base - 74 + int(34 * math.sin(a))
            d.line([(px + 4, base - 74), (ex, ey)], fill=(30, 12, 44), width=4)
    d.rectangle([x, y, x + w, y + h], outline=(30, 12, 44), width=3)
    d.text((x + 14, y + 10), "VICE CITY", font=F(SANS_B, 22), fill=(255, 255, 255))


def draw_flag(d, x, y, w, h, kind):
    """Tiny simplified flags: us / ru / cn."""
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    if kind == "us":
        for i in range(7):
            d.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7],
                        fill=(255, 255, 255) if i % 2 == 0 else (178, 30, 40))
        d.rectangle([x, y, x + int(w * 0.42), y + int(h * 0.54)], fill=(28, 52, 110))
        for r in range(4):
            for c in range(5):
                d.ellipse([x + 6 + c * 11, y + 5 + r * 8, x + 10 + c * 11, y + 9 + r * 8],
                          fill=(255, 255, 255))
    elif kind == "ru":
        for i, col in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
            d.rectangle([x, y + i * h // 3, x + w, y + (i + 1) * h // 3], fill=col)
    else:  # cn
        d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        d.ellipse([x + 8, y + 7, x + 24, y + 23], fill=(255, 222, 0))
        for sx, sy in [(34, 10), (42, 18), (42, 28), (34, 34)]:
            d.ellipse([x + sx, y + sy, x + sx + 7, y + sy + 7], fill=(255, 222, 0))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28                      # margin
    R = W - M                   # right edge

    # ---------- masthead ----------
    d.rectangle([M, M, R, 108], fill=NAVY)
    d.text((M + 16, M + 6), "THE WORLD IN ONE DAY",
           font=F(SERIF, 44), fill=(255, 255, 255))
    d.text((M + 16, 80), "THURSDAY 19 NOVEMBER 2026  •  ONE DAY, ONE PAGE",
           font=F(SANS_B, 17), fill=(255, 214, 90))

    # ---------- lead: Anthropic IPO (left, wide) ----------
    y = 122
    y = kicker(d, M, y, "Markets — the biggest debut ever")
    y = headline(d, M, y, "Anthropic's $81bn debut: the biggest IPO in history hits Nasdaq",
                 32, 600)
    y = para(d, M, y + 6,
             "Shares in the maker of Claude start trading today under the ticker "
             "ANT, priced at $83 — above the $70–$78 range — in an offering that "
             "raised $81.3 billion and values the AI lab at about $1.5 trillion.",
             F(SANS, 19), INK, 600)
    draw_ipo_chart(d, M, y + 12, 600, 128)
    lead_bottom = y + 12 + 150

    # ---------- GTA VI (right column) ----------
    gx = 656
    gy = 122
    gy = kicker(d, gx, gy, "Culture — gaming", color=TEAL)
    gy = headline(d, gx, gy, "After 13 years, GTA VI arrives", 30, R - gx)
    gy = para(d, gx, gy + 4,
              "Grand Theft Auto VI begins its global rollout today, sending "
              "players back to Vice City in the most awaited game launch ever.",
              F(SANS, 18), INK, R - gx)
    draw_vice_city(d, gx, gy + 10, R - gx, 150)
    gta_bottom = gy + 10 + 168

    mid = max(lead_bottom, gta_bottom) + 16
    rule(d, M, mid, R, width=3, color=INK)

    # ---------- Shenzhen summit (full width) ----------
    y = mid + 14
    y = kicker(d, M, y, "Diplomacy — three leaders, one summit")
    y = headline(d, M, y,
                 "Trump, Putin and Xi meet in Shenzhen — as Europe's allies gather in Berlin",
                 28, R - M)
    # flags row
    fy = y + 4
    fx = M
    for kind, label in (("us", "USA"), ("ru", "RUSSIA"), ("cn", "CHINA")):
        draw_flag(d, fx, fy, 96, 60, kind)
        d.text((fx, fy + 66), label, font=F(SANS_B, 13), fill=GREY)
        fx += 118
    tx = M + 380
    ty = fy - 2
    ty = para(d, tx, ty,
              "The three presidents hold trilateral talks at the APEC summit, with "
              "Ukraine on the agenda. Hours earlier, Germany, France, Britain, "
              "Poland and Italy met in Berlin with Trump's envoys Witkoff and "
              "Kushner, demanding a seat at the peace talks — days after the EU "
              "proposed a €45bn loan for Kyiv.",
              F(SANS, 17), INK, R - tx)
    summit_bottom = max(fy + 88, ty) + 6
    rule(d, M, summit_bottom, R)

    # ---------- three columns ----------
    y = summit_bottom + 14
    col_w = 304
    gap = 20
    cols = [
        ("Washington", RED,
         "Jeffries set to make history as Speaker",
         "Democrats nominate Hakeem Jeffries to lead the House — the first "
         "African-American Speaker in US history."),
        ("Gaza", TEAL,
         "Israel launches ground operation in central Gaza",
         "Troops move into an area left under last year's ceasefire deal, "
         "and dozens of displaced families flee their tents."),
        ("Crimea", BLUE,
         "Crimea bridge hit again, traffic halted",
         "The strategic bridge to Russia is struck for a second day running, "
         "days after Ukrainian drones brought down a road span."),
    ]
    col_bottom = y
    for i, (tag, color, head, body) in enumerate(cols):
        cx = M + i * (col_w + gap)
        cy = y
        cy = kicker(d, cx, cy, tag, color=color)
        cy = headline(d, cx, cy, head, 20, col_w)
        cy = para(d, cx, cy + 4, body, F(SANS, 15), INK, col_w)
        col_bottom = max(col_bottom, cy)
    rule(d, M, col_bottom + 12, R)

    # ---------- also today strip ----------
    y = col_bottom + 24
    d.rectangle([M, y, R, y + 62], fill=LIGHT)
    d.text((M + 14, y + 7), "ALSO TODAY", font=F(SANS_B, 16), fill=RED)
    items = [
        "Cyclone Akvan nears India's east coast",
        "Voyager 1 reaches one light-day",
        "Australia sanctions settlers",
        "India–Japan 2+2 defence talks",
        "Fed minutes point to more rate rises",
    ]
    yy = y + 28
    d.text((M + 14, yy), "  •  ".join(items[:3]), font=F(SANS, 15), fill=INK)
    d.text((M + 14, yy + 21), "  •  ".join(items[3:]), font=F(SANS, 15), fill=INK)

    # ---------- footer ----------
    fy = y + 62 + 8
    d.text((M, fy), "Sources: Reuters, AP, BBC, Bloomberg, TradingView — all events reported on 19 November 2026",
           font=F(SANS, 12), fill=GREY)
    d.text((R - 200, fy), "make.fun · news-image-20261119", font=F(SANS, 12), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
