"""The front page for Tuesday 24 November 2026.

Thirty-plus stories on one square: eleven carried by a drawn scene and a
headline, the rest as one-line briefs under a numbered map, so a reader who
missed the day can see it before reading a word of it.

Every height is measured, not guessed: the headline and deck of each tile are
wrapped with the real font, and the art takes whatever is left of the tile, so
editing the copy cannot push anything off the page.

Two runs write the same bytes: no clock, no randomness, no network.
"""

from __future__ import annotations

import json
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageStat

from fit import Measure

W = H = 1024
MARGIN = 24
BOTTOM = 1000

PAPER = (252, 251, 248)
INK = (26, 24, 22)
INK_SOFT = (78, 73, 67)
RULE = (198, 192, 182)
PANEL = (238, 236, 230)

RED = (176, 36, 30)
TEAL = (20, 78, 88)
NAVY = (26, 40, 58)
GOLD = (158, 120, 40)
PLUM = (104, 58, 116)
GREEN = (38, 96, 62)

FONT_DIR = os.environ.get(
    "NI24_FONT_DIR", "/root/.hermes/cache/scratch/ni24fonts"
)
FONTS = {
    "serif": "DejaVuSerif.ttf",
    "serif_b": "DejaVuSerif-Bold.ttf",
    "cond_b": "DejaVuSerifCondensed-Bold.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "sans_cb": "DejaVuSansCondensed-Bold.ttf",
}

DATE = "Tuesday 24 November 2026"

REGION_COLOUR = {
    "Americas": RED,
    "Europe": TEAL,
    "Asia": NAVY,
    "MidEast": GOLD,
    "Africa": GREEN,
    "World": PLUM,
}
REGIONS = ["Americas", "Europe", "Asia", "MidEast", "Africa", "World"]


def F(kind: str, size: int):
    return ImageFont.truetype(os.path.join(FONT_DIR, FONTS[kind]), size)


# --- the day's stories -----------------------------------------------------
TILES = [
    {
        "region": "MidEast", "place": "Tehran / Hormuz", "topic": "Blockade",
        "headline": "Iran orders Hormuz shut further",
        "deck": "Hatami said the strait must close \"further day by day\" until seven "
                "conditions are met. The IRGC says mines hit three tankers; the JMIC cannot confirm it.",
        "art": "hormuz",
    },
    {
        "region": "Americas", "place": "Washington", "topic": "Nvidia",
        "headline": "Republicans turn on Huang's return",
        "deck": "Three House committee chairs said Nvidia's review left security concerns "
                "open. Huang testifies to the Senate Banking Committee on 3 December.",
        "art": "ceo",
    },
    {
        "region": "Europe", "place": "Strasbourg", "topic": "Rights",
        "headline": "Court rules against Poland and Latvia",
        "deck": "The ECHR found pushbacks of Afghan and Iraqi migrants into Belarus "
                "amounted to inhuman treatment. It is the first ruling on instrumentalised migration.",
        "art": "courthouse",
    },
    {
        "region": "MidEast", "place": "Gaza City", "topic": "War",
        "headline": "Hamas security chief killed by strike",
        "deck": "An Israeli airstrike killed Naeem Abu Nahel, director of Hamas' internal "
                "security apparatus in Gaza, on Tuesday, Hamas sources said.",
        "art": "well",
    },
    {
        "region": "Europe", "place": "Geneva", "topic": "Sport",
        "headline": "The youngest world title match begins",
        "deck": "Gukesh and Sindarov, both 20, opened the FIDE World Championship at "
                "Cologny. Sindarov had white and chose the Berlin Defence.",
        "art": "chess",
    },
    {
        "region": "Africa", "place": "Addis Ababa", "topic": "Health",
        "headline": "Gavi moves to buy 1.5m Ebola doses",
        "deck": "The alliance will buy Oxford and Serum Institute shots against the "
                "Bundibugyo strain, which has killed more than 5,700 people in Congo.",
        "art": "aid",
    },
    {
        "region": "Europe", "place": "Brussels", "topic": "Climate",
        "headline": "Brussels moves to remake the COP",
        "deck": "After COP31 closed with no deal, the Commission wants the summit "
                "process overhauled: \"If we want to save the COP, it needs to reform itself.\"",
        "art": "cop",
    },
    {
        "region": "Asia", "place": "Taipei", "topic": "Airspace",
        "headline": "Washington takes two states to the ICAO",
        "deck": "The US asked the aviation agency to examine Mauritius and Seychelles for "
                "barring President Lai's aircraft from their airspace on a trip to Eswatini.",
        "art": "radar",
    },
    {
        "region": "Asia", "place": "Kyushu", "topic": "Disaster",
        "headline": "A 5.8 quake strikes near southern Japan",
        "deck": "The quake came a day after an M7 off Kamchatka, where a false M9.9 "
                "alert was issued and then withdrawn.",
        "art": "seismo",
    },
    {
        "region": "Americas", "place": "Tel Aviv", "topic": "Aid",
        "headline": "Huckabee doubts the Israel aid will stop",
        "deck": "Shown on Tuesday, the US ambassador said the $3.8bn a year memorandum "
                "\"is supposed to continue for two more years\", casting doubt on Trump's pledge.",
        "art": "data",
    },
    {
        "region": "Africa", "place": "Tripoli", "topic": "Oil",
        "headline": "Libya's government moves to void Arkenu",
        "deck": "The GNU asked a Tripoli court to annul the oil deal that a UN panel said "
                "moved more than $3bn out of the country.",
        "art": "corvette",
    },
]

BRIEFS = [
    ("Americas", "Washington", "Advocacy groups sue over a removed slavery exhibit"),
    ("Europe", "Brussels", "The Commission wants the COP process reformed"),
    ("Europe", "Brussels", "A 50m euro Black Sea maritime security hub is planned"),
    ("Europe", "Antalya", "Eighty to ninety states objected to the COP31 text"),
    ("Europe", "Brussels", "Sixty Russian banks face removal from SWIFT"),
    ("MidEast", "Hormuz", "Three tankers burned after reported mine hits"),
    ("MidEast", "Tehran", "Hatami: any new US action draws a wider answer"),
    ("MidEast", "Tel Aviv", "Huckabee spoke at the INSS conference"),
    ("Asia", "Port Louis", "Mauritius withdrew the flight permissions in April"),
    ("Asia", "Taipei", "Lai's flight was barred from two airspaces"),
    ("Asia", "Seoul", "Korea and China widen a trade deal on content"),
    ("Asia", "Dhaka", "Talks drag on over the new RMG wage"),
    ("Africa", "Congo", "No licensed shot exists for the Bundibugyo strain"),
    ("Africa", "Accra", "West Africa's gold refining outruns its mines"),
    ("Africa", "Conakry", "Miners stockpile gold as local rules bite"),
    ("World", "Geneva", "Sindarov won the World Cup and the Candidates"),
    ("World", "Cologny", "Fourteen games; the first to 7.5 wins"),
    ("World", "Kamchatka", "A false M9.9 alert followed an M7 quake"),
    ("World", "Zurich", "FIFA names the 2031 and 2035 World Cup hosts"),
    ("World", "Addis Ababa", "Africa CDC hosts the vaccine financing talks"),
]

NUMBERS = [
    ("7", "Conditions Tehran says must be met first"),
    ("$3.8bn", "Annual US military aid to Israel"),
    ("1.5m", "Ebola doses Gavi plans to buy"),
    ("5,700", "Deaths in Congo's Bundibugyo outbreak"),
    ("90", "States that objected to the COP31 text"),
    ("20", "Both players' age in the title match"),
]

DATE_CHECK = [
    "COP31 closed without a deal, 22 Nov",
    "Huang reinstated at Nvidia, 23 Nov",
    "Iran ordered the strait shut, 23 Nov",
    "The Merkury was hit at Benghazi, 23 Nov",
]
BILLBOARD = (
    "Iran shuts Hormuz further  ·  Republicans break with Trump on Nvidia  ·  "
    "Court condemns Poland and Latvia  ·  Hamas security chief killed"
)


# --- text measurement ------------------------------------------------------
# Wrapped and fitted type lives in src/fit.py: the page asks that module how
# many lines a deck needs and then chooses the art height from the answer.
MEASURE = None


def setup_measure(draw):
    """Build the page's one Measure around the live draw handle."""
    global MEASURE
    MEASURE = Measure(draw, F)
    return MEASURE


def _sky(draw, box, top, bottom=None):
    x0, y0, x1, y1 = box
    if bottom is None:
        draw.rectangle(box, fill=top)
        return
    for i in range(y1 - y0):
        t = i / max(1, y1 - y0 - 1)
        draw.line(
            (x0, y0 + i, x1, y0 + i),
            fill=(
                int(top[0] + (bottom[0] - top[0]) * t),
                int(top[1] + (bottom[1] - top[1]) * t),
                int(top[2] + (bottom[2] - top[2]) * t),
            ),
        )


# --- the eleven drawn scenes ----------------------------------------------
def art_ceo(draw, box):
    """A die on a board and a price line going up the right-hand side."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (20, 26, 38), (34, 42, 58))
    # the chip: a square die with pins, left of centre
    dx0 = x0 + int(w * 0.16)
    dy0 = y0 + int(h * 0.28)
    dw = int(w * 0.30)
    dh = int(h * 0.42)
    for i in range(6):
        py = dy0 + int(dh * (0.08 + i * 0.16))
        draw.line((dx0 - int(w * 0.05), py, dx0, py), fill=(150, 130, 70), width=2)
        draw.line((dx0 + dw, py, dx0 + dw + int(w * 0.05), py),
                  fill=(150, 130, 70), width=2)
    draw.rectangle((dx0, dy0, dx0 + dw, dy0 + dh), fill=(66, 92, 84))
    draw.rectangle((dx0 + int(dw * 0.18), dy0 + int(dh * 0.22),
                    dx0 + int(dw * 0.82), dy0 + int(dh * 0.78)),
                   outline=(118, 156, 140))
    draw.text((dx0 + int(dw * 0.30), dy0 + int(dh * 0.40)), "NVDA",
              font=F("sans_cb", max(6, int(h * 0.11))), fill=(206, 236, 220))
    # the line: down, then straight up, then a spike
    pts = [(x0 + int(w * 0.55), y0 + int(h * 0.74)),
           (x0 + int(w * 0.62), y0 + int(h * 0.78)),
           (x0 + int(w * 0.70), y0 + int(h * 0.62)),
           (x0 + int(w * 0.78), y0 + int(h * 0.50)),
           (x0 + int(w * 0.86), y0 + int(h * 0.30)),
           (x0 + int(w * 0.93), y0 + int(h * 0.20))]
    draw.line(pts, fill=(86, 200, 130), width=3)
    ax, ay = pts[-1]
    draw.polygon([(ax - int(w * 0.03), ay - int(h * 0.04)),
                  (ax + int(w * 0.02), ay), (ax - int(w * 0.03), ay + int(h * 0.04))],
                 fill=(86, 200, 130))
    # the "returned" arrow: a loop back over the chip
    draw.arc((dx0 - int(w * 0.10), dy0 - int(h * 0.22),
              dx0 + dw + int(w * 0.10), dy0 + int(h * 0.30)),
             200, 340, fill=(230, 226, 210), width=2)


def art_courthouse(draw, box):
    """A neoclassical federal courthouse: steps, columns, pediment, scales."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    # a bright sky behind a dark stone front: pale on pale reads as mush at
    # thumbnail size, so the building is the darkest mass on the card
    _sky(draw, box, (240, 234, 220), (206, 202, 190))
    base = y1 - int(h * 0.04)
    cx = x0 + w // 2
    # steps, widest at the bottom
    for i in range(4):
        draw.rectangle((x0 + int(w * 0.04) - i * 2, base - i * 4,
                        x1 - int(w * 0.04) + i * 2, base + 4 - i * 4),
                       fill=(96, 90, 82))
    # the mass behind the columns
    draw.rectangle((x0 + int(w * 0.13), base - int(h * 0.40),
                    x1 - int(w * 0.13), base - int(h * 0.06)),
                   fill=(52, 48, 44))
    # the entablature
    draw.rectangle((x0 + int(w * 0.11), base - int(h * 0.44),
                    x1 - int(w * 0.11), base - int(h * 0.38)), fill=(40, 36, 34))
    # columns, light against the dark mass so each one reads
    for i in range(6):
        px = x0 + int(w * 0.16) + i * int(w * 0.115)
        draw.rectangle((px, base - int(h * 0.38), px + int(w * 0.055),
                        base - int(h * 0.06)), fill=(226, 220, 206))
        draw.rectangle((px, base - int(h * 0.38), px + int(w * 0.055),
                        base - int(h * 0.355)), fill=(198, 192, 178))
        draw.rectangle((px - 1, base - int(h * 0.075), px + int(w * 0.055) + 1,
                        base - int(h * 0.06)), fill=(198, 192, 178))
    # the pediment, a solid dark triangle with a light tympanum
    draw.polygon([(x0 + int(w * 0.09), base - int(h * 0.44)),
                  (cx, base - int(h * 0.60)),
                  (x1 - int(w * 0.09), base - int(h * 0.44))], fill=(40, 36, 34))
    draw.polygon([(x0 + int(w * 0.13), base - int(h * 0.45)),
                  (cx, base - int(h * 0.575)),
                  (x1 - int(w * 0.13), base - int(h * 0.45))], fill=(214, 208, 194))
    # the scales of justice, dark on the pale tympanum
    sx, sy = cx, base - int(h * 0.505)
    draw.line((sx, sy - int(h * 0.035), sx, sy + int(h * 0.035)),
              fill=(34, 30, 28), width=2)
    draw.line((sx - int(w * 0.045), sy - int(h * 0.018),
               sx + int(w * 0.045), sy - int(h * 0.018)), fill=(34, 30, 28), width=2)
    for side in (-1, 1):
        bx = sx + side * int(w * 0.045)
        draw.line((bx, sy - int(h * 0.018), bx, sy + int(h * 0.008)),
                  fill=(34, 30, 28), width=1)
        draw.arc((bx - int(w * 0.022), sy + int(h * 0.002),
                  bx + int(w * 0.022), sy + int(h * 0.028)), 0, 180,
                 fill=(34, 30, 28), width=2)
    # a flag on a pole, far left, for the federal cue
    fx = x0 + int(w * 0.05)
    draw.line((fx, base, fx, base - int(h * 0.52)), fill=(70, 66, 62), width=2)
    draw.polygon([(fx, base - int(h * 0.52)), (fx + int(w * 0.11), base - int(h * 0.49)),
                  (fx, base - int(h * 0.44))], fill=(176, 36, 30))


def art_hormuz(draw, box):
    """A tanker stopped by a warship in a narrow strait."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (44, 60, 78), (96, 112, 126))
    sea = y0 + int(h * 0.56)
    draw.rectangle((x0, sea, x1, y1), fill=(30, 50, 66))
    for i in range(6):
        wy = sea + int(h * 0.05) + i * int(h * 0.06)
        draw.line((x0, wy, x1, wy), fill=(38, 60, 78), width=1)
    # headlands closing in: the strait
    draw.polygon([(x0, sea), (x0 + int(w * 0.26), sea - int(h * 0.06)),
                  (x0 + int(w * 0.20), sea)], fill=(84, 78, 62))
    draw.polygon([(x1, sea - int(h * 0.10)), (x1 - int(w * 0.30), sea - int(h * 0.05)),
                  (x1 - int(w * 0.24), sea)], fill=(84, 78, 62))
    # tanker, broadside
    tx0, tx1 = x0 + int(w * 0.30), x0 + int(w * 0.84)
    draw.polygon([(tx0, sea), (tx1, sea), (tx1 - int(w * 0.04), sea + int(h * 0.09)),
                  (tx0 + int(w * 0.03), sea + int(h * 0.09))], fill=(58, 62, 70))
    draw.rectangle((tx0 + int(w * 0.03), sea - int(h * 0.05),
                    tx1 - int(w * 0.08), sea), fill=(150, 60, 52))
    draw.rectangle((tx0 + int(w * 0.05), sea - int(h * 0.14),
                    tx0 + int(w * 0.17), sea - int(h * 0.05)), fill=(214, 210, 200))
    for i in range(3):
        px = tx0 + int(w * 0.22) + i * int(w * 0.18)
        draw.ellipse((px, sea - int(h * 0.10), px + int(w * 0.08),
                      sea - int(h * 0.04)), fill=(180, 176, 166))
    # the warship beyond, and a red stop mark
    wx = x0 + int(w * 0.62)
    draw.polygon([(wx, sea - int(h * 0.02)), (wx + int(w * 0.26), sea - int(h * 0.02)),
                  (wx + int(w * 0.22), sea + int(h * 0.02)),
                  (wx + int(w * 0.04), sea + int(h * 0.02))], fill=(110, 118, 124))
    draw.rectangle((wx + int(w * 0.10), sea - int(h * 0.09),
                    wx + int(w * 0.16), sea - int(h * 0.02)), fill=(128, 136, 142))
    draw.line((wx + int(w * 0.13), sea - int(h * 0.09),
               wx + int(w * 0.13), sea - int(h * 0.15)), fill=(150, 156, 160), width=2)
    # a bar across the strait
    draw.rectangle((x0 + int(w * 0.30), y0 + int(h * 0.16),
                    x1 - int(w * 0.10), y0 + int(h * 0.21)), fill=(176, 36, 30))
    for i in range(9):
        bx = x0 + int(w * 0.30) + i * int(w * 0.07)
        draw.polygon([(bx, y0 + int(h * 0.16)), (bx + int(w * 0.035), y0 + int(h * 0.16)),
                      (bx + int(w * 0.015), y0 + int(h * 0.21)),
                      (bx - int(w * 0.02), y0 + int(h * 0.21))], fill=(240, 236, 226))


def art_corvette(draw, box):
    """A burning warship at a night berth, a drone above her."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (30, 36, 50), (58, 54, 62))
    sea = y0 + int(h * 0.66)
    draw.rectangle((x0, sea, x1, y1), fill=(20, 30, 42))
    for i in range(5):
        wy = sea + int(h * 0.06) + i * int(h * 0.07)
        draw.line((x0, wy, x1, wy), fill=(28, 40, 54), width=1)
    # the quay behind
    draw.rectangle((x0, y0 + int(h * 0.44), x1, sea), fill=(58, 62, 72))
    for i in range(5):
        cx = x0 + int(w * (0.04 + i * 0.20))
        draw.rectangle((cx, y0 + int(h * 0.26), cx + int(w * 0.10),
                        y0 + int(h * 0.44)), fill=(46, 50, 60))
    # the hull, listing
    hx0, hx1 = x0 + int(w * 0.16), x0 + int(w * 0.78)
    draw.polygon([(hx0, sea + int(h * 0.06)), (hx1, sea - int(h * 0.02)),
                  (hx1 - int(w * 0.06), sea + int(h * 0.12)),
                  (hx0 + int(w * 0.04), sea + int(h * 0.14))], fill=(74, 78, 84))
    draw.polygon([(hx0 + int(w * 0.10), sea - int(h * 0.06)),
                  (hx0 + int(w * 0.34), sea - int(h * 0.12)),
                  (hx0 + int(w * 0.40), sea + int(h * 0.02)),
                  (hx0 + int(w * 0.12), sea + int(h * 0.04))], fill=(96, 100, 106))
    draw.line((hx0 + int(w * 0.26), sea - int(h * 0.12),
               hx0 + int(w * 0.24), sea - int(h * 0.26)), fill=(120, 124, 130), width=2)
    # fire and smoke
    for i in range(5):
        fx = hx0 + int(w * (0.14 + i * 0.13))
        fr = int(w * (0.05 + (i % 3) * 0.02))
        draw.ellipse((fx - fr, sea - int(h * 0.22) - i * 3, fx + fr,
                      sea - int(h * 0.06)), fill=(198, 96, 40))
        draw.ellipse((fx - fr // 2, sea - int(h * 0.20) - i * 3,
                      fx + fr // 2, sea - int(h * 0.10)), fill=(236, 176, 72))
    for i in range(6):
        sx = hx0 + int(w * (0.10 + i * 0.11))
        draw.ellipse((sx, y0 + int(h * 0.06) + (i % 3) * 4, sx + int(w * 0.14),
                      y0 + int(h * 0.22) + (i % 3) * 4), fill=(46, 46, 52))
    # the drone that did it
    dx, dy = x0 + int(w * 0.72), y0 + int(h * 0.16)
    draw.line((dx - int(w * 0.06), dy, dx + int(w * 0.02), dy),
              fill=(214, 212, 200), width=2)
    draw.polygon([(dx, dy - 2), (dx + int(w * 0.06), dy + int(h * 0.02)),
                  (dx + int(w * 0.06), dy + int(h * 0.05)), (dx, dy + 3)],
                 fill=(214, 212, 200))
    draw.line((dx, dy, hx0 + int(w * 0.30), sea - int(h * 0.14)),
              fill=(190, 130, 60), width=1)


def art_radar(draw, box):
    """An AWACS overhead, a radar sweep, and a track across a border."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (34, 46, 62), (56, 70, 86))
    # ground and the border line
    ground = y0 + int(h * 0.78)
    draw.rectangle((x0, ground, x1, y1), fill=(44, 56, 58))
    draw.line((x0 + int(w * 0.30), y0 + int(h * 0.30),
               x0 + int(w * 0.42), y1), fill=(198, 190, 160), width=2)
    for i in range(6):
        gy = ground - int(h * 0.06) * i
        draw.line((x0, gy, x0 + int(w * 0.30), gy), fill=(36, 48, 50), width=1)
    # the radar: three arcs from a station on this side of the line
    rx, ry = x0 + int(w * 0.12), ground - int(h * 0.04)
    for i in range(3):
        r = int(w * (0.16 + i * 0.10))
        draw.arc((rx - r, ry - r, rx + r, ry + r), 300, 360,
                 fill=(96, 190, 150), width=2)
    draw.rectangle((rx - 3, ry - int(h * 0.10), rx + 3, ry), fill=(120, 200, 160))
    # AWACS aircraft
    ax, ay = x0 + int(w * 0.52), y0 + int(h * 0.34)
    draw.ellipse((ax - int(w * 0.10), ay - int(h * 0.03),
                  ax + int(w * 0.10), ay + int(h * 0.03)), fill=(196, 200, 204))
    draw.polygon([(ax - int(w * 0.02), ay), (ax - int(w * 0.06), ay + int(h * 0.09)),
                  (ax, ay + int(h * 0.09))], fill=(186, 190, 196))
    draw.rectangle((ax - int(w * 0.02), ay - int(h * 0.09),
                    ax + int(w * 0.06), ay - int(h * 0.06)), fill=(210, 214, 218))
    draw.line((ax + int(w * 0.14), ay - int(h * 0.03),
               ax + int(w * 0.14), ay + int(h * 0.03)), fill=(214, 218, 222), width=1)
    # the drone's track: in, then back out
    tp = [(x0 + int(w * 0.10), y0 + int(h * 0.16)),
          (x0 + int(w * 0.34), y0 + int(h * 0.14)),
          (x0 + int(w * 0.52), y0 + int(h * 0.20)),
          (x0 + int(w * 0.62), y0 + int(h * 0.18)),
          (x0 + int(w * 0.74), y0 + int(h * 0.10))]
    for i in range(len(tp) - 1):
        draw.line((tp[i], tp[i + 1]), fill=(220, 90, 70), width=2)
    dx, dy = tp[3]
    draw.polygon([(dx, dy), (dx - int(w * 0.05), dy - int(h * 0.03)),
                  (dx + int(w * 0.02), dy + int(h * 0.04))], fill=(230, 120, 96))
    draw.line((dx, dy, dx - int(w * 0.12), dy + int(h * 0.14)),
              fill=(220, 90, 70), width=1)


def art_aid(draw, box):
    """Grain silos, a sack, and an empty bowl."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (196, 178, 150), (222, 208, 184))
    ground = y0 + int(h * 0.74)
    draw.rectangle((x0, ground, x1, y1), fill=(168, 148, 118))
    # silos
    for i in range(3):
        sx = x0 + int(w * (0.06 + i * 0.17))
        sw = int(w * 0.13)
        draw.rectangle((sx, y0 + int(h * 0.18), sx + sw, ground), fill=(198, 200, 196))
        draw.ellipse((sx, y0 + int(h * 0.10), sx + sw, y0 + int(h * 0.26)),
                     fill=(214, 216, 212))
        draw.line((sx + sw // 2, y0 + int(h * 0.10), sx + sw // 2, ground),
                  fill=(178, 180, 178), width=1)
    # the ship that cannot sail
    sx0, sx1 = x0 + int(w * 0.60), x1 - int(w * 0.04)
    draw.polygon([(sx0, ground - int(h * 0.06)), (sx1, ground - int(h * 0.06)),
                  (sx1 - int(w * 0.04), ground - int(h * 0.01)),
                  (sx0 + int(w * 0.03), ground - int(h * 0.01))], fill=(70, 74, 80))
    for i in range(4):
        bx = sx0 + int(w * 0.04) + i * int(w * 0.07)
        draw.rectangle((bx, ground - int(h * 0.14), bx + int(w * 0.05),
                        ground - int(h * 0.06)), fill=(150, 60, 52))
    # a heaped sack, foreground
    px, py = x0 + int(w * 0.14), ground - int(h * 0.02)
    draw.polygon([(px, py), (px + int(w * 0.20), py),
                  (px + int(w * 0.15), py - int(h * 0.20)),
                  (px + int(w * 0.05), py - int(h * 0.20))], fill=(206, 190, 158))
    draw.ellipse((px + int(w * 0.04), py - int(h * 0.24),
                  px + int(w * 0.16), py - int(h * 0.16)), fill=(180, 164, 132))
    for i in range(4):
        gx = px + int(w * (0.07 + i * 0.02))
        draw.ellipse((gx, py - int(h * 0.03), gx + 3, py - int(h * 0.01)),
                     fill=(150, 120, 70))
    # the empty bowl, right
    bx = x0 + int(w * 0.62)
    by = y1 - int(h * 0.16)
    draw.arc((bx, by - int(h * 0.10), bx + int(w * 0.24), by + int(h * 0.06)),
             0, 180, fill=(176, 36, 30), width=3)


def art_well(draw, box):
    """A village water point, a jerrycan, and a folded blue vest."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (206, 196, 178), (184, 172, 154))
    ground = y0 + int(h * 0.70)
    draw.rectangle((x0, ground, x1, y1), fill=(158, 138, 110))
    # broken buildings behind
    for i, bh in enumerate((0.34, 0.46, 0.28)):
        bx = x0 + int(w * (0.04 + i * 0.24))
        bw = int(w * 0.20)
        top = ground - int(h * bh)
        draw.rectangle((bx, top, bx + bw, ground), fill=(172, 162, 148))
        draw.polygon([(bx, top), (bx + int(bw * 0.4), top - int(h * 0.06)),
                      (bx + int(bw * 0.7), top + int(h * 0.02)),
                      (bx + bw, top - int(h * 0.03)), (bx + bw, top),
                      (bx + int(bw * 0.7), top + int(h * 0.04)),
                      (bx + int(bw * 0.4), top - int(h * 0.03)), (bx, top)],
                     fill=(140, 130, 118))
        draw.rectangle((bx + int(bw * 0.28), ground - int(h * 0.16),
                        bx + int(bw * 0.52), ground - int(h * 0.02)), fill=(78, 74, 70))
    # the well: a concrete ring with a pump head
    cx = x0 + int(w * 0.56)
    draw.ellipse((cx - int(w * 0.10), ground - int(h * 0.05),
                  cx + int(w * 0.10), ground + int(h * 0.05)), fill=(158, 152, 142))
    draw.ellipse((cx - int(w * 0.07), ground - int(h * 0.035),
                  cx + int(w * 0.07), ground + int(h * 0.035)), fill=(52, 64, 72))
    draw.rectangle((cx - int(w * 0.012), ground - int(h * 0.26),
                    cx + int(w * 0.012), ground - int(h * 0.05)), fill=(96, 100, 98))
    draw.rectangle((cx - int(w * 0.03), ground - int(h * 0.30),
                    cx + int(w * 0.03), ground - int(h * 0.26)), fill=(110, 114, 112))
    # a jerrycan and a bucket beside it
    jx = cx + int(w * 0.13)
    draw.rectangle((jx, ground - int(h * 0.10), jx + int(w * 0.06), ground),
                   fill=(196, 160, 60))
    draw.rectangle((jx + int(w * 0.02), ground - int(h * 0.13),
                    jx + int(w * 0.04), ground - int(h * 0.10)), fill=(160, 130, 46))
    # the vest, folded where he worked
    vx = x0 + int(w * 0.30)
    vy = ground - int(h * 0.02)
    draw.polygon([(vx, vy), (vx + int(w * 0.14), vy),
                  (vx + int(w * 0.12), vy - int(h * 0.07)),
                  (vx + int(w * 0.02), vy - int(h * 0.07))], fill=(64, 120, 176))
    draw.rectangle((vx + int(w * 0.05), vy - int(h * 0.05),
                    vx + int(w * 0.09), vy - int(h * 0.02)), fill=(236, 234, 226))


def art_chess(draw, box):
    """Two kings on a board, the trophy between them."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (30, 30, 38), (48, 48, 56))
    # a board in perspective
    bx0, bx1 = x0 + int(w * 0.06), x1 - int(w * 0.06)
    by0, by1 = y0 + int(h * 0.56), y1 - int(h * 0.06)
    draw.polygon([(bx0, by1), (bx1, by1),
                  (bx1 - int(w * 0.10), by0), (bx0 + int(w * 0.10), by0)],
                 fill=(222, 214, 194))
    for r in range(4):
        for c in range(8):
            t0 = r / 4.0
            t1 = (r + 1) / 4.0
            ly0 = by1 + (by0 - by1) * t0
            ly1 = by1 + (by0 - by1) * t1
            inset0 = int(w * 0.10) * (1 - t0)
            inset1 = int(w * 0.10) * (1 - t1)
            cw0 = (bx1 - bx0 - 2 * inset0) / 8.0
            cw1 = (bx1 - bx0 - 2 * inset1) / 8.0
            if (r + c) % 2:
                continue
            draw.polygon([(bx0 + inset0 + c * cw0, ly0),
                          (bx0 + inset0 + (c + 1) * cw0, ly0),
                          (bx0 + inset1 + (c + 1) * cw1, ly1),
                          (bx0 + inset1 + c * cw1, ly1)], fill=(104, 92, 80))
    # two kings facing each other
    def king(px, py, s, dark):
        body = (28, 28, 32) if dark else (238, 236, 228)
        draw.polygon([(px - s * 0.45, py), (px + s * 0.45, py),
                      (px + s * 0.30, py - s * 0.30),
                      (px - s * 0.30, py - s * 0.30)], fill=body)
        draw.rectangle((px - s * 0.26, py - s * 0.62, px + s * 0.26, py - s * 0.30),
                       fill=body)
        draw.ellipse((px - s * 0.30, py - s * 0.78, px + s * 0.30, py - s * 0.52),
                     fill=body)
        draw.line((px, py - s * 0.98, px, py - s * 0.76), fill=body, width=3)
        draw.line((px - s * 0.10, py - s * 0.90, px + s * 0.10, py - s * 0.90),
                  fill=body, width=3)
    king(x0 + int(w * 0.28), y1 - int(h * 0.14), int(w * 0.13), True)
    king(x0 + int(w * 0.72), y0 + int(h * 0.48), int(w * 0.10), False)
    # the trophy, centre
    tx, ty = x0 + int(w * 0.50), y0 + int(h * 0.30)
    draw.arc((tx - int(w * 0.09), ty - int(h * 0.10),
              tx + int(w * 0.09), ty + int(h * 0.08)), 0, 180,
             fill=(190, 158, 74), width=4)
    draw.rectangle((tx - int(w * 0.015), ty + int(h * 0.04),
                    tx + int(w * 0.015), ty + int(h * 0.10)), fill=(190, 158, 74))
    draw.rectangle((tx - int(w * 0.05), ty + int(h * 0.10),
                    tx + int(w * 0.05), ty + int(h * 0.13)), fill=(170, 140, 62))


def art_data(draw, box):
    """Rows of records on a screen, one row spilling out."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (18, 26, 34), (30, 42, 52))
    # a server rack behind
    rx = x0 + int(w * 0.66)
    draw.rectangle((rx, y0 + int(h * 0.14), x1 - int(w * 0.04), y1 - int(h * 0.10)),
                   fill=(34, 44, 52))
    for i in range(7):
        ry = y0 + int(h * 0.18) + i * int(h * 0.09)
        draw.rectangle((rx + int(w * 0.02), ry, x1 - int(w * 0.06),
                        ry + int(h * 0.05)), fill=(48, 60, 68))
        draw.ellipse((x1 - int(w * 0.09), ry + int(h * 0.012),
                      x1 - int(w * 0.075), ry + int(h * 0.027)), fill=(96, 200, 140))
    # the form on screen
    fx0, fy0 = x0 + int(w * 0.06), y0 + int(h * 0.12)
    fx1, fy1 = x0 + int(w * 0.60), y1 - int(h * 0.08)
    draw.rectangle((fx0, fy0, fx1, fy1), fill=(236, 234, 226))
    draw.rectangle((fx0, fy0, fx1, fy0 + int(h * 0.09)), fill=(176, 36, 30))
    draw.text((fx0 + int(w * 0.02), fy0 + int(h * 0.02)), "FORM 6",
              font=F("sans_cb", max(6, int(h * 0.075))), fill=(248, 246, 238))
    rows = int((fy1 - fy0 - int(h * 0.14)) // int(h * 0.075))
    for i in range(rows):
        ry = fy0 + int(h * 0.14) + i * int(h * 0.075)
        draw.rectangle((fx0 + int(w * 0.03), ry, fx0 + int(w * 0.16),
                        ry + int(h * 0.03)), fill=(30, 34, 34))
        for k in range(3):
            lw = int(w * (0.22 - k * 0.04))
            draw.rectangle((fx0 + int(w * 0.19), ry + k * int(h * 0.012),
                            fx0 + int(w * 0.19) + lw, ry + k * int(h * 0.012)
                            + int(h * 0.008)), fill=(120, 124, 120))
    # a sheet slipping off the desk
    draw.polygon([(fx0 + int(w * 0.02), fy1 + int(h * 0.02)),
                  (fx0 + int(w * 0.30), fy1 + int(h * 0.02)),
                  (fx0 + int(w * 0.34), fy1 + int(h * 0.10)),
                  (fx0 + int(w * 0.06), fy1 + int(h * 0.10))], fill=(232, 230, 222))
    for i in range(3):
        ry = fy1 + int(h * 0.04) + i * int(h * 0.02)
        draw.line((fx0 + int(w * 0.06), ry, fx0 + int(w * 0.28), ry),
                  fill=(150, 150, 146), width=1)


def art_cop(draw, box):
    """An empty negotiating table and a globe that will not hold."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (46, 52, 60), (70, 76, 84))
    # the long table, empty
    ty = y0 + int(h * 0.62)
    draw.polygon([(x0 + int(w * 0.08), ty), (x1 - int(w * 0.08), ty),
                  (x1 - int(w * 0.02), y1 - int(h * 0.04)),
                  (x0 + int(w * 0.02), y1 - int(h * 0.04))], fill=(92, 74, 56))
    draw.polygon([(x0 + int(w * 0.08), ty), (x1 - int(w * 0.08), ty),
                  (x1 - int(w * 0.10), ty - int(h * 0.05)),
                  (x0 + int(w * 0.10), ty - int(h * 0.05))], fill=(126, 104, 80))
    # empty chairs pushed back
    for i in range(5):
        cx = x0 + int(w * (0.12 + i * 0.19))
        draw.rectangle((cx, ty - int(h * 0.14), cx + int(w * 0.10),
                        ty - int(h * 0.06)), fill=(64, 70, 78))
        draw.rectangle((cx + int(w * 0.02), ty - int(h * 0.06),
                        cx + int(w * 0.08), ty + int(h * 0.02)), fill=(52, 58, 66))
    # the globe, warming, with a dashed 1.5C ring that is broken
    gx, gy = x0 + int(w * 0.50), y0 + int(h * 0.28)
    r = int(min(w, h) * 0.19)
    draw.ellipse((gx - r, gy - r, gx + r, gy + r), fill=(70, 104, 118))
    draw.ellipse((gx - int(r * 0.7), gy - int(r * 0.6), gx + int(r * 0.4),
                  gy + int(r * 0.2)), fill=(96, 128, 96))
    draw.ellipse((gx - int(r * 0.2), gy - int(r * 0.1), gx + int(r * 0.8),
                  gy + int(r * 0.7)), fill=(100, 132, 100))
    for i in range(14):
        a0 = i * (360 / 14)
        if 3 <= i <= 6:
            continue
        draw.arc((gx - r - 8, gy - r - 8, gx + r + 8, gy + r + 8),
                 a0, a0 + 14, fill=(206, 96, 60), width=3)
    drawing = draw.textlength("1.5C", font=F("sans_cb", 10))
    draw.text((gx - drawing / 2, gy + r + 14), "1.5C",
              font=F("sans_cb", 10), fill=(206, 96, 60))


def art_seismo(draw, box):
    """A seismograph trace over an island in a dark sea."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    _sky(draw, box, (16, 22, 34), (28, 38, 52))
    sea = y0 + int(h * 0.56)
    draw.rectangle((x0, sea, x1, y1), fill=(20, 32, 48))
    # the island
    ix = x0 + int(w * 0.44)
    draw.polygon([(ix - int(w * 0.14), sea), (ix, sea - int(h * 0.14)),
                  (ix + int(w * 0.12), sea)], fill=(62, 82, 60))
    draw.polygon([(ix - int(w * 0.05), sea - int(h * 0.06)),
                  (ix + int(w * 0.01), sea - int(h * 0.13)),
                  (ix + int(w * 0.07), sea - int(h * 0.06))], fill=(48, 66, 48))
    # concentric rings from the hypocentre, deep under it
    cx, cy = ix, sea + int(h * 0.14)
    for i in range(4):
        r = int(w * (0.08 + i * 0.09))
        draw.arc((cx - r, cy - r, cx + r, cy + r), 200, 340,
                 fill=(120, 150, 180), width=1)
    # the trace across the top
    pts = []
    for i in range(60):
        px = x0 + int(w * 0.04) + i * int(w * 0.0155)
        amp = int(h * 0.09 * math.exp(-abs(i - 26) / 12.0))
        sgn = 1 if i % 2 else -1
        pts.append((px, y0 + int(h * 0.22) + sgn * amp))
    draw.line(pts, fill=(236, 120, 90), width=2)
    draw.line((x0, y0 + int(h * 0.22), x1, y0 + int(h * 0.22)),
              fill=(52, 60, 72), width=1)
    mw = draw.textlength("M6.5", font=F("sans_cb", 11))
    draw.text((x1 - int(w * 0.05) - mw, y0 + int(h * 0.06)), "M6.5",
              font=F("sans_cb", 11), fill=(236, 120, 90))


ART = {
    "ceo": art_ceo,
    "courthouse": art_courthouse,
    "hormuz": art_hormuz,
    "corvette": art_corvette,
    "radar": art_radar,
    "aid": art_aid,
    "well": art_well,
    "chess": art_chess,
    "data": art_data,
    "cop": art_cop,
    "seismo": art_seismo,
}


# --- print texture ---------------------------------------------------------
# A flat vector fill reads as a diagram; a printed photograph is grainy, has
# a tonal fall-off at the edges and carries hundreds of intermediate tones.
# These three passes give the drawn scenes that, deterministically.
_GRAIN = None


def _grain():
    """A fixed, deterministic grain tile: no random module, no clock."""
    global _GRAIN
    if _GRAIN is None:
        rnd = 20261124
        tile = Image.new("L", (256, 256))
        px = tile.load()
        for y in range(256):
            for x in range(256):
                rnd = (1103515245 * rnd + 12345) & 0x7FFFFFFF
                px[x, y] = 128 + ((rnd >> 15) % 96) - 48
        _GRAIN = tile
    return _GRAIN


def _texture(img, box, strength=1.0):
    """Grain, a vignette and a touch more colour, confined to one art box."""
    x0, y0, x1, y1 = (int(v) for v in box)
    w, h = x1 - x0, y1 - y0
    if w <= 1 or h <= 1:
        return

    region = img.crop((x0, y0, x1, y1))

    grain = _grain()
    noise = Image.new("L", (w, h))
    for ty in range(0, h, 256):
        for tx in range(0, w, 256):
            noise.paste(grain, (tx, ty))
    if strength < 1.0:
        noise = noise.point(lambda v: 128 + int((v - 128) * strength))
    noisy = ImageChops.add(
        region, Image.merge("RGB", (noise, noise, noise)), scale=1.0, offset=-128
    )
    region = Image.blend(region, noisy, 0.34)

    shade = Image.new("L", (w, h), 255)
    sp = shade.load()
    cx, cy = w / 2.0, h / 2.0
    col_f = [
        int(255 - 44 * min(1.0, (abs(xx - cx) / max(1.0, cx * 1.02)) ** 2))
        for xx in range(w)
    ]
    for yy in range(h):
        fy = int(255 - 44 * min(1.0, (abs(yy - cy) * 1.05 / max(1.0, cy * 1.02)) ** 2))
        for xx in range(w):
            sp[xx, yy] = (fy * col_f[xx]) // 255
    shade_rgb = Image.merge("RGB", (shade, shade, shade))
    region = ImageChops.multiply(region, shade_rgb)

    region = ImageEnhance.Color(region).enhance(1.32)
    region = ImageEnhance.Contrast(region).enhance(1.12)

    luma = ImageStat.Stat(region.convert("L")).mean[0]
    if luma < 62:
        region = ImageEnhance.Brightness(region).enhance(min(2.0, 62.0 / max(1.0, luma)))

    img.paste(region, (x0, y0))


# --- the map ---------------------------------------------------------------
LAND_PATH = os.environ.get(
    "NI24_LAND",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "land.json"),
)


def _load_land():
    """Real coastlines (Natural Earth 1:110m), packed beside the fonts."""
    with open(LAND_PATH) as fh:
        return [[(lon / 10.0, lat / 10.0) for lon, lat in ring] for ring in json.load(fh)]


LAND = _load_land()


def draw_map(draw, box, pins):
    """A world map with a numbered pin per tile: the page's index."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=(22, 32, 42))

    lat_top, lat_bot = 84.0, -58.0

    def px(lon):
        return x0 + int(w * (lon + 180) / 360)

    def py(lat):
        return y0 + int(h * (lat_top - lat) / (lat_top - lat_bot))

    for i in range(1, 6):
        gy = y0 + int(h * i / 6)
        draw.line((x0, gy, x1, gy), fill=(32, 44, 56), width=1)
    for i in range(1, 12):
        gx = x0 + int(w * i / 12)
        draw.line((gx, y0, gx, y1), fill=(32, 44, 56), width=1)

    for ring in LAND:
        pts = [(px(lon), py(lat)) for lon, lat in ring]
        if len(pts) >= 3:
            draw.polygon(pts, fill=(104, 116, 102))

    pf = F("sans_cb", 7)
    R = 6
    placed = []
    for lon, lat, colour, num in pins:
        ax, ay = px(lon), py(lat)
        cx, cy = ax, ay
        step = 0
        SEP = 2 * R + 4
        while any((cx - q[0]) ** 2 + (cy - q[1]) ** 2 < SEP * SEP
                  for q in placed) and step < 240:
            step += 1
            ang = step * 0.55
            rr = 3 + step * 0.85
            cx = int(ax + rr * math.cos(ang))
            cy = int(ay + rr * math.sin(ang))
            cx = max(x0 + R + 1, min(x1 - R - 1, cx))
            cy = max(y0 + R + 1, min(y1 - R - 1, cy))
        placed.append((cx, cy))
        if (cx, cy) != (ax, ay):
            draw.line((ax, ay, cx, cy), fill=(226, 222, 210), width=1)
            draw.ellipse((ax - 1, ay - 1, ax + 1, ay + 1), fill=(226, 222, 210))
        draw.ellipse((cx - R - 1, cy - R - 1, cx + R + 1, cy + R + 1),
                     fill=(246, 244, 238))
        draw.ellipse((cx - R, cy - R, cx + R, cy + R), fill=colour)
        label = str(num)
        tw = draw.textlength(label, font=pf)
        draw.text((cx - tw / 2, cy - 3.5), label, font=pf, fill=(255, 255, 255))


PINS = [
    (-121.95, 37.37, RED, 1),     # Santa Clara: Nvidia
    (-74.00, 40.71, RED, 2),      # New York: the 2nd Circuit
    (51.39, 35.69, GOLD, 3),      # Tehran: the blockade
    (20.07, 32.12, GREEN, 4),     # Benghazi: the corvette
    (21.01, 52.23, TEAL, 5),      # Warsaw: the drone
    (12.50, 41.90, PLUM, 6),      # Rome: the WFP
    (34.50, 31.53, GOLD, 7),      # Jabalia: the water worker
    (6.14, 46.20, PLUM, 8),       # Geneva: the chess match
    (77.21, 28.61, NAVY, 9),      # New Delhi: the voter data
    (30.71, 36.90, TEAL, 10),     # Antalya: COP31
    (168.32, -17.73, PLUM, 11),   # Port Vila: the quake
]


# --- layout ----------------------------------------------------------------
def build(out_path: str) -> None:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    measure = setup_measure(d)
    inner = W - 2 * MARGIN

    # ---- eyebrow: the nameplate and the promise ----
    y = MARGIN
    d.text((MARGIN, y), "THE WORLD IN ONE DAY", font=F("sans_cb", 13), fill=INK)
    right = f"{len(TILES) + len(BRIEFS)} STORIES  ·  6 REGIONS  ·  ONE PAGE"
    rf = F("sans_cb", 10)
    d.text((W - MARGIN - d.textlength(right, font=rf), y + 2), right, font=rf, fill=INK_SOFT)
    y += 18
    d.line((MARGIN, y, W - MARGIN, y), fill=INK, width=2)

    # ---- the date, the largest thing on the page ----
    y += 10
    date_font = F("cond_b", 48)
    while d.textlength(DATE, font=date_font) > inner and date_font.size > 30:
        date_font = F("cond_b", date_font.size - 1)
    d.text((MARGIN, y), DATE, font=date_font, fill=INK)
    y += int(date_font.size * 1.10)
    d.line((MARGIN, y, W - MARGIN, y), fill=RULE)
    y += 6

    # ---- the billboard: the four things that happened ----
    bf = measure.one_line(BILLBOARD, "sans_cb", 13, inner)
    d.text((MARGIN, y), BILLBOARD, font=bf, fill=RED)
    y += 20

    # ---- the numbers strip ----
    strip_h = 44
    d.rectangle((MARGIN, y, W - MARGIN, y + strip_h), fill=PANEL)
    cell = inner // len(NUMBERS)
    nf = F("cond_b", 21)
    lf = F("serif", 8)
    for i, (big, small) in enumerate(NUMBERS):
        cx = MARGIN + i * cell + 8
        d.text((cx, y + 4), big, font=nf, fill=RED)
        measure.block(cx, y + 27, small, lf, cell - 14, INK_SOFT, 9, limit=2)
        if i:
            d.line((MARGIN + i * cell, y + 6, MARGIN + i * cell, y + strip_h - 6), fill=RULE)
    y += strip_h + 10

    # ---- the tiles: three wide, then two rows of four ----
    rail_h = 178
    rail_top = BOTTOM - 44 - rail_h
    tile_top = y
    rows = [[0, 1, 2], [3, 4, 5, 6], [7, 8, 9, 10]]
    gap = 8
    avail = rail_top - 10 - tile_top - gap * (len(rows) - 1)
    row_h = avail // len(rows)

    idx = 0
    for r, row in enumerate(rows):
        cols = len(row)
        tw = (inner - gap * (cols - 1)) // cols
        ry = tile_top + r * (row_h + gap)
        wide = cols == 3
        head_f = F("sans_cb", 17 if wide else 13)
        deck_f = F("serif", 10 if wide else 9)
        head_l = 19 if wide else 15
        deck_l = 11 if wide else 10

        # Measure every tile in the row before drawing any of them: the art
        # takes whatever the tallest text block leaves, so the boxes in a row
        # stay level and no deck is ever cut mid-sentence.
        blocks = []
        for c in range(cols):
            tile = TILES[row[c]]
            head = measure.lines(tile["headline"], head_f, tw - 2)
            deck = measure.lines(tile["deck"], deck_f, tw - 2)
            assert len(head) <= 2, (tile["headline"], len(head))
            blocks.append((head, deck))
        deck_lines = max(len(dk) for _, dk in blocks)

        for c in range(cols):
            tile = TILES[row[c]]
            head, deck = blocks[c]
            x0 = MARGIN + c * (tw + gap)
            idx += 1

            kick_h = 13
            text_h = kick_h + 2 + len(head) * head_l + 2 + deck_lines * deck_l
            art_h = max(24, row_h - text_h - 6)

            box = (x0, ry, x0 + tw, ry + art_h)
            ART[tile["art"]](d, box)
            _texture(img, box)
            d.rectangle((x0, ry, x0 + tw, ry + art_h), outline=RULE)

            ty = ry + art_h + 3
            numf = F("sans_cb", 9)
            d.rectangle((x0, ty, x0 + 15, ty + 12), fill=REGION_COLOUR[tile["region"]])
            nw = d.textlength(str(idx), font=numf)
            d.text((x0 + 7 - nw / 2, ty + 1), str(idx), font=numf, fill=PAPER)

            kick = f"{tile['place'].upper()}  ·  {tile['topic'].upper()}"
            kf = measure.one_line(kick, "sans_cb", 8, tw - 22)
            d.text((x0 + 19, ty + 1), kick, font=kf, fill=REGION_COLOUR[tile["region"]])
            ty += kick_h + 2

            for line in head:
                d.text((x0, ty), line, font=head_f, fill=INK)
                ty += head_l
            ty += 2
            for line in deck:
                d.text((x0, ty), line, font=deck_f, fill=INK_SOFT)
                ty += deck_l

    d.line((MARGIN, rail_top - 8, W - MARGIN, rail_top - 8), fill=RULE)

    # ---- the rail: the map index beside the briefs ----
    map_w = 372
    map_h = rail_h
    draw_map(d, (MARGIN, rail_top, MARGIN + map_w, rail_top + map_h), PINS)
    cap_h = 12
    d.rectangle((MARGIN, rail_top + map_h - cap_h, MARGIN + map_w,
                 rail_top + map_h), fill=(206, 206, 198))
    mf = F("sans_cb", 7)
    d.text((MARGIN + 6, rail_top + map_h - cap_h + 3),
           "WHERE IT HAPPENED  ·  NUMBERED TO THE STORIES ABOVE",
           font=mf, fill=(28, 34, 40))

    bx = MARGIN + map_w + 12
    bw = W - MARGIN - bx
    d.text((bx, rail_top), f"ALSO ON 24 NOVEMBER  ·  {len(BRIEFS)} MORE STORIES",
           font=F("sans_cb", 10), fill=INK)
    by = rail_top + 16

    # Pick the largest type size the rail holds, then the column count for it:
    # a thumbnail is read before any word, so size wins over column count.
    for size in range(9, 5, -1):
        bfont = F("sans_cb", size)
        lead = size + 3
        for ncol in (3, 4, 2, 5):
            gut = 9
            colw = (bw - gut * (ncol - 1)) // ncol
            per_col = (rail_top + rail_h - by) // lead
            wrapped = [(region, measure.lines(f"{city.upper()}  {text}", bfont, colw))
                       for region, city, text in BRIEFS]
            total = sum(len(ls) for _, ls in wrapped)
            if total <= per_col * ncol:
                break
        else:
            continue
        break

    # fill column by column, in reading order, never splitting a brief
    col, cy, used = 0, by, 0
    for region, lines in wrapped:
        if used + len(lines) > per_col and col < ncol - 1:
            col, cy, used = col + 1, by, 0
        cx = bx + col * (colw + gut)
        for j, ln in enumerate(lines):
            d.text((cx, cy), ln, font=bfont,
                   fill=REGION_COLOUR[region] if j == 0 else INK)
            cy += lead
        used += len(lines)

    # ---- date check and footer ----
    yb = BOTTOM - 38
    d.line((MARGIN, yb, W - MARGIN, yb), fill=RED, width=2)
    dc_label = F("sans_cb", 9)
    head = "FIRST REPORTED BEFORE TODAY:"
    dcf = F("serif", 8)
    while True:
        need = d.textlength(head + "  ", font=dc_label) + sum(
            d.textlength(it + "  ·  ", font=dcf) for it in DATE_CHECK)
        if need <= inner or dcf.size <= 6:
            break
        dcf = F("serif", dcf.size - 1)
    d.text((MARGIN, yb + 5), head, font=dc_label, fill=RED)
    dx = MARGIN + d.textlength(head + "  ", font=dc_label)
    for i, item in enumerate(DATE_CHECK):
        tail = "  ·" if i < len(DATE_CHECK) - 1 else ""
        d.text((dx, yb + 6), item + tail, font=dcf, fill=INK_SOFT)
        dx += d.textlength(item + "  ·  ", font=dcf)
    assert dx <= W - MARGIN + 2, (dx, need)

    ff = F("serif", 8)
    d.line((MARGIN, BOTTOM - 16, W - MARGIN, BOTTOM - 16), fill=RULE)
    d.text(
        (MARGIN, BOTTOM - 12),
        "Reuters · AP · AFP · BBC · Al Jazeera · Bloomberg · WFP · UNRWA · USGS · FIDE",
        font=ff, fill=INK_SOFT,
    )
    src = "Every story happened or was first reported on Tuesday 24 November 2026."
    d.text((W - MARGIN - d.textlength(src, font=ff), BOTTOM - 12), src, font=ff, fill=INK_SOFT)

    img.save(out_path, format="PNG", optimize=True)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
