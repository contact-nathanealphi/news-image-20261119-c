"""Render the front-page infographic for the 19 November 2026 news entry.

Variant C: clean infographic with a self-drawn world map. Every shape and
letter is drawn here with Pillow primitives from hand-written coordinates.
No photos, no copied artwork, no network, no randomness, no timestamps, so
re-running this script produces the same PNG bytes.

Usage: python3 tools/render.py   (from anywhere; paths are script-relative)
Output: assets/entry.png, 1024x1024, under 1 MiB.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "entry.png"

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REGULAR = FONT_DIR / "DejaVuSans.ttf"

W, H = 1024, 1024
WHITE = (255, 255, 255)
INK = (22, 30, 34)
GRAY = (98, 106, 110)
TEAL = (13, 115, 110)
RED = (176, 38, 30)
LAND = (224, 231, 231)
LAND_LINE = (158, 169, 171)
PANEL = (247, 249, 249)
CARD = (246, 248, 248)
CARD_LINE = (208, 214, 214)
GRID = (233, 237, 237)

# --- simplified world map: (lon, lat) polygons, equirectangular ---

NORTH_AMERICA = [
    (-168, 66), (-160, 58), (-140, 60), (-130, 55), (-125, 49), (-124, 42),
    (-120, 34), (-114, 29), (-110, 24), (-105, 20), (-97, 16), (-92, 15),
    (-86, 12), (-83, 9), (-79, 9), (-77, 8), (-75, 10), (-70, 12),
    (-64, 18), (-68, 21), (-74, 22), (-77, 25), (-80, 32), (-75, 38),
    (-70, 42), (-65, 45), (-60, 47), (-55, 52), (-65, 60), (-75, 62),
    (-85, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71),
]
SOUTH_AMERICA = [
    (-80, 10), (-77, 7), (-75, 2), (-78, -3), (-81, -6), (-80, -12),
    (-76, -18), (-71, -22), (-70, -30), (-70, -38), (-72, -45), (-70, -50),
    (-66, -55), (-68, -52), (-65, -48), (-62, -42), (-58, -38), (-52, -33),
    (-48, -28), (-42, -24), (-39, -18), (-35, -12), (-35, -7), (-38, -4),
    (-43, -2), (-48, 0), (-52, 3), (-56, 6), (-61, 9), (-67, 11),
    (-72, 12), (-77, 9),
]
AFRICA = [
    (-17, 15), (-16, 20), (-10, 30), (-5, 35), (0, 36), (10, 37),
    (20, 32), (30, 31), (35, 28), (43, 12), (51, 11), (48, 5),
    (42, 0), (40, -5), (40, -10), (36, -18), (32, -26), (28, -33),
    (20, -35), (16, -28), (12, -18), (9, -2), (9, 4), (-8, 5),
    (-13, 8), (-17, 12),
]
EURASIA = [
    (-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (5, 60),
    (10, 62), (18, 69), (25, 71), (35, 68), (45, 68), (55, 69), (65, 70),
    (75, 72), (85, 74), (95, 76), (110, 74), (130, 72), (150, 70),
    (170, 66), (178, 65), (170, 60), (162, 58), (158, 52), (150, 45),
    (142, 40), (140, 35), (135, 34), (130, 31), (127, 35), (122, 38),
    (120, 32), (122, 28), (118, 25), (110, 20), (108, 12), (105, 9),
    (100, 8), (98, 12), (95, 16), (92, 21), (89, 22), (86, 20),
    (80, 15), (77, 8), (74, 10), (72, 20), (66, 25), (60, 25),
    (56, 26), (52, 28), (50, 30), (48, 29), (44, 29), (40, 31),
    (36, 36), (30, 36), (26, 38), (22, 37), (18, 40), (12, 44),
    (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37),
]
AUSTRALIA = [
    (114, -22), (114, -30), (115, -34), (118, -35), (124, -33), (129, -32),
    (132, -32), (136, -35), (140, -38), (146, -39), (150, -37), (153, -32),
    (153, -27), (150, -22), (146, -19), (142, -14), (142, -11), (137, -12),
    (135, -15), (132, -12), (128, -14), (124, -16), (122, -17), (118, -20),
]
UK = [(-5, 50), (-3, 53), (-2, 55), (-4, 58), (-6, 57), (-5, 53)]
JAPAN = [
    (130, 31), (132, 33), (135, 34), (138, 35), (140, 36), (141, 39),
    (142, 42), (144, 44), (142, 45), (140, 43), (138, 38), (135, 35),
    (132, 33), (130, 32),
]
NEW_ZEALAND = [
    (167, -45), (170, -42), (174, -41), (177, -38), (175, -37),
    (173, -35), (170, -40), (167, -45),
]
INDONESIA = [
    (95, 5), (98, 3), (101, 0), (104, -3), (107, -6), (110, -7),
    (113, -8), (116, -9), (119, -9), (120, -10), (119, -8), (114, -7),
    (110, -6), (106, -3), (102, 1), (98, 4), (95, 5),
]
BORNEO = [
    (109, 1), (111, 3), (114, 4), (117, 6), (118, 2), (117, -2),
    (115, -3), (112, -4), (110, -3), (109, 0),
]
NEW_GUINEA = [
    (131, -1), (135, -2), (138, -3), (141, -3), (143, -5), (146, -6),
    (148, -8), (146, -9), (143, -8), (140, -8), (137, -6), (134, -4),
    (131, -2),
]

CONTINENTS = [
    NORTH_AMERICA, SOUTH_AMERICA, AFRICA, EURASIA, AUSTRALIA,
    UK, JAPAN, NEW_ZEALAND, INDONESIA, BORNEO, NEW_GUINEA,
]

# Map frame and projection (lon -180..180, lat 75..-60).
MAP_X, MAP_Y, MAP_W, MAP_H = 24, 172, 976, 264
LAT_TOP, LAT_BOT = 75.0, -60.0


def project(lon: float, lat: float) -> tuple[int, int]:
    x = MAP_X + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return int(round(x)), int(round(y))


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    if not path.exists():
        raise SystemExit(f"missing font file: {path}")
    return ImageFont.truetype(str(path), size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont,
         max_width: int) -> list[str]:
    """Greedy word wrap measured with the real font; never splits a word."""
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = f"{current} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw: ImageDraw.ImageDraw, x: int, y: int, text: str,
               fnt: ImageFont.FreeTypeFont, max_width: int,
               fill: tuple[int, int, int], line_gap: int = 4,
               max_lines: int = 3) -> int:
    """Draw wrapped text; return the y just below the last line."""
    lines = wrap(draw, text, fnt, max_width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def dot(d: ImageDraw.ImageDraw, cx: int, cy: int, num: str,
        f_num: ImageFont.FreeTypeFont, colour: tuple[int, int, int] = TEAL,
        r: int = 13) -> None:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour,
              outline=WHITE, width=2)
    w = d.textlength(num, font=f_num)
    d.text((cx - w / 2, cy - f_num.size / 2 - 1), num, font=f_num,
           fill=WHITE)


def star(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int,
         fill: tuple[int, int, int]) -> None:
    d.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28),
               (cx + r, cy), (cx + r * 0.28, cy + r * 0.28),
               (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
               (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=fill)


def main() -> None:
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    f_mast = font(BOLD, 62)
    f_date = font(BOLD, 27)
    f_kick = font(BOLD, 16)
    f_lab = font(BOLD, 13)
    f_num = font(BOLD, 15)
    f_card_num = font(BOLD, 30)
    f_title = font(BOLD, 20)
    f_sum = font(REGULAR, 16)
    f_stat_h = font(BOLD, 15)
    f_stat_n = font(BOLD, 30)
    f_stat_l = font(REGULAR, 14)
    f_foot = font(REGULAR, 14)

    # ---------- Masthead ----------
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 22), title,
           font=f_mast, fill=INK)
    date = "THURSDAY, 19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 96), date,
           font=f_date, fill=TEAL)
    d.line([(24, 138), (1000, 138)], fill=TEAL, width=3)
    d.line([(24, 144), (1000, 144)], fill=INK, width=1)

    # ---------- Map ----------
    d.text((24, 152), "WHERE IT HAPPENED", font=f_kick, fill=INK)
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                fill=PANEL, outline=CARD_LINE, width=1)
    # faint graticule
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0)
        d.line([(x, MAP_Y), (x, MAP_Y + MAP_H)], fill=GRID, width=1)
    for lat in (60, 30, 0, -30):
        _, y = project(0, lat)
        d.line([(MAP_X, y), (MAP_X + MAP_W, y)], fill=GRID, width=1)
    # continents
    for poly in CONTINENTS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_LINE)

    # numbered dots: (number, lon, lat, label, label dx, dy, colour)
    # Gaza (5) and Jerusalem (6) share one tiny spot, so 6 is offset
    # with a short leader line to its true place.
    spots = [
        (1, 114.1, 22.5, "SHENZHEN", 8, -26, TEAL),
        (2, 56.5, 26.5, "GULF", 17, -14, RED),
        (3, 36.5, 45.3, "KERCH", 10, -26, RED),
        (4, -74.0, 40.7, "NEW YORK", -78, -24, TEAL),
        (5, 34.5, 31.5, "GAZA", -52, 14, RED),
        (7, 4.3, 52.1, "THE HAGUE", -104, -8, TEAL),
    ]
    for num, lon, lat, label, dx, dy, colour in spots:
        cx, cy = project(lon, lat)
        dot(d, cx, cy, str(num), f_num, colour)
        d.text((cx + dx, cy + dy), label, font=f_lab, fill=INK)
    # 6 Jerusalem, offset below Gaza with a leader line
    jx, jy = project(35.2, 31.8)
    d.line([(jx, jy), (jx + 12, jy + 18)], fill=INK, width=1)
    dot(d, jx + 16, jy + 24, "6", f_num, TEAL)
    d.text((jx + 34, jy + 18), "JERUSALEM", font=f_lab, fill=INK)
    # 8 Voyager 1: in deep space, top-right of the map
    vx, vy = 946, 196
    d.arc([vx - 34, vy - 30, vx + 34, vy + 30], start=200, end=340,
          fill=GRAY, width=2)
    star(d, vx - 26, vy - 20, 9, TEAL)
    dot(d, vx, vy, "8", f_num, TEAL)
    d.text((vx - 66, vy + 18), "DEEP SPACE", font=f_lab, fill=INK)

    # ---------- Numbered story cards: 2 columns x 4 rows ----------
    # (number, colour, title, one-sentence summary)
    cards = [
        (1, TEAL, "Three-way Shenzhen summit",
         "Trump, Xi and Putin meet at the APEC sidelines; nuclear arms, "
         "Ukraine and Iran on the agenda."),
        (2, RED, "Strikes across the Gulf",
         "Iran fires at US bases in Kuwait and Bahrain; the US hits a "
         "Guard missile site on Qeshm; a tanker is struck in Hormuz."),
        (3, RED, "Kerch Bridge hit again",
         "Ukraine strikes the Crimean Bridge for the third time this week."),
        (4, TEAL, "Anthropic's record debut",
         "Shares start on Nasdaq as ANT after a record $81.3bn IPO "
         "priced at $83 a share."),
        (5, RED, "Floods swamp Gaza",
         "Four nations urge Israel to let aid in; heavy rain displaces "
         "46,000+ households."),
        (6, TEAL, "Eisenkot to form government",
         "President Herzog asks the ex-army chief to try; the Knesset "
         "elects Matan Kahana speaker with 66 votes."),
        (7, TEAL, "Court to rule on Myanmar",
         "The UN's top court is to rule on genocide claims against "
         "Myanmar over the Rohingya."),
        (8, TEAL, "Voyager 1's light-day",
         "NASA's probe is believed to have reached a 'light-day' "
         "from Earth."),
    ]
    cols = [24, 524]
    rows = [452, 560, 668, 776]
    cw, ch = 476, 100
    for i, (num, colour, head, summ) in enumerate(cards):
        cx = cols[i % 2]
        cy = rows[i // 2]
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD,
                    outline=CARD_LINE, width=1)
        # number badge
        bx, by = cx + 26, cy + 26
        d.ellipse([bx - 18, by - 18, bx + 18, by + 18], fill=colour)
        w = d.textlength(str(num), font=f_card_num)
        d.text((bx - w / 2, by - 16), str(num), font=f_card_num, fill=WHITE)
        tx = cx + 56
        d.text((tx, cy + 12), head, font=f_title, fill=INK)
        text_block(d, tx, cy + 42, summ, f_sum, cw - 72, GRAY,
                   line_gap=2, max_lines=2)

    # ---------- Numbers strip ----------
    d.line([(24, 894), (1000, 894)], fill=INK, width=2)
    d.text((24, 906), "AROUND THE WORLD IN NUMBERS", font=f_stat_h, fill=INK)
    stats = [
        ("$81.3bn", "Anthropic IPO, the largest on record"),
        ("46,000+", "households displaced by Gaza floods"),
        ("1,600", "developers in Bengaluru on GTA 6"),
    ]
    sx = [24, 360, 696]
    for (num, lab), x in zip(stats, sx):
        d.text((x, 930), num, font=f_stat_n, fill=TEAL)
        text_block(d, x, 966, lab, f_stat_l, 300, GRAY, line_gap=1,
                   max_lines=1)

    # ---------- Footer ----------
    foot = "DRAWN FROM REPORTS PUBLISHED 19 NOVEMBER 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 996), foot,
           font=f_foot, fill=GRAY)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
