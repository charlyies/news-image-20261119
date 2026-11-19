#!/usr/bin/env python3
"""Compose the 19 November 2026 front page: THE WORLD TODAY.

Build-time only. Draws a 1024x1024 PNG newspaper front page with PIL
and real Noto fonts, then saves entry.png next to this script.
No network, no randomness, no timestamps in the output.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")
FONT_DIR = "/usr/share/fonts/truetype/noto"

W, H = 1024, 1024
PAPER = (248, 242, 223)
INK = (18, 18, 18)
RED = (178, 34, 28)
NAVY = (16, 32, 64)
GOLD = (201, 162, 39)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_BLACK = "NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SERIF = "NotoSerif-Regular.ttf"
SANS_BLACK = "NotoSans-Black.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS = "NotoSans-Regular.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centre(draw, y, text, fnt, fill, x0=0, x1=W):
    w = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - w) / 2, y), text, font=fnt, fill=fill)


def vgrad(size, top, bottom):
    """Smooth vertical gradient image of the given size."""
    w, h = size
    base = Image.new("RGB", (1, h))
    px = base.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return base.resize((w, h))


def soft_disc(layer, box, fill, blur):
    """A blurred ellipse on its own layer, composited back softly."""
    tmp = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    d.ellipse(box, fill=fill)
    tmp = tmp.filter(ImageFilter.GaussianBlur(blur))
    layer.alpha_composite(tmp)


def draw_lead_scene(draw_img, x, y, w, h):
    """Layered Shenzhen dusk skyline: sky, sun glow, haze, towers,
    lit windows, plaza, red carpet and three flags. No faces, no water."""
    scene = Image.new("RGBA", (w, h))
    # Sky: deep indigo at top to warm amber at the horizon.
    sky = vgrad((w, h), (24, 38, 82), (232, 122, 54)).convert("RGBA")
    scene.paste(sky, (0, 0))
    sd = ImageDraw.Draw(scene)
    rng = random.Random(19112026)
    # Stars fading in the upper sky.
    for _ in range(70):
        sx = rng.randint(0, w - 1)
        sy = rng.randint(0, int(h * 0.32))
        a = rng.randint(40, 150)
        sd.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255, a))
    # Low sun glow in the clear gap between the centre towers.
    soft_disc(scene, [w * 0.40, h * 0.30, w * 0.62, h * 0.78],
              (255, 214, 130, 170), 46)
    soft_disc(scene, [w * 0.45, h * 0.42, w * 0.57, h * 0.66],
              (255, 236, 180, 230), 22)
    sd = ImageDraw.Draw(scene)
    sd.ellipse([w * 0.465, h * 0.46, w * 0.535, h * 0.62],
               fill=(255, 244, 205, 255))
    # Soft cloud bands, blurred so they read as haze, not discs.
    for cy, cw, alpha in [(0.16, 0.55, 60), (0.24, 0.42, 48), (0.10, 0.38, 42)]:
        soft_disc(scene, [w * (0.5 - cw / 2), h * cy, w * (0.5 + cw / 2),
                          h * (cy + 0.07)], (255, 190, 150, alpha), 18)
    horizon = int(h * 0.66)
    # Distant skyline: pale, hazy silhouettes.
    for bx, bw, bh in [(0.00, 0.10, 0.16), (0.09, 0.07, 0.22), (0.16, 0.12, 0.13),
                       (0.28, 0.08, 0.20), (0.36, 0.10, 0.15), (0.47, 0.07, 0.24),
                       (0.55, 0.11, 0.14), (0.66, 0.08, 0.21), (0.75, 0.10, 0.15),
                       (0.86, 0.07, 0.19), (0.93, 0.07, 0.13)]:
        sd.rectangle([w * bx, horizon - h * bh, w * (bx + bw), horizon],
                     fill=(96, 84, 128, 190))
    # Midground towers: darker, with a few lit windows.
    towers = [(0.03, 0.09, 0.34), (0.13, 0.07, 0.42), (0.21, 0.10, 0.30),
              (0.32, 0.06, 0.46), (0.39, 0.09, 0.33),
              (0.57, 0.10, 0.29), (0.68, 0.06, 0.44), (0.75, 0.09, 0.32),
              (0.85, 0.07, 0.38), (0.93, 0.06, 0.28)]
    for bx, bw, bh in towers:
        tx0, tx1 = w * bx, w * (bx + bw)
        ty0 = horizon - h * bh
        sd.rectangle([tx0, ty0, tx1, horizon], fill=(30, 34, 66, 255))
        # Rooftop beacon.
        sd.rectangle([ (tx0 + tx1) / 2 - 2, ty0 - 7, (tx0 + tx1) / 2 + 2, ty0],
                     fill=(255, 80, 60, 255))
        # Lit windows: small warm rectangles, denser near the base.
        for _ in range(int(bw * 260)):
            wx = rng.uniform(tx0 + 4, tx1 - 8)
            wy = rng.uniform(ty0 + 8, horizon - 6)
            if rng.random() < 0.45:
                sd.rectangle([wx, wy, wx + 4, wy + 6],
                             fill=(255, 205, 110, rng.randint(140, 235)))
    # Ground plaza: dark foreground with a warm gradient wash.
    plaza = vgrad((w, h - horizon), (52, 44, 66), (22, 18, 34)).convert("RGBA")
    scene.paste(plaza, (0, horizon))
    sd = ImageDraw.Draw(scene)
    # A thin warm band where the towers meet the plaza, no hard shadows.
    # Red carpet running from the horizon to the bottom edge.
    sd.polygon([(w * 0.42, horizon), (w * 0.58, horizon),
                (w * 0.68, h), (w * 0.32, h)], fill=(178, 34, 28, 255))
    sd.polygon([(w * 0.42, horizon), (w * 0.58, horizon),
                (w * 0.60, h * 0.82), (w * 0.40, h * 0.82)],
               fill=(205, 52, 40, 255))
    # Gold carpet edging.
    sd.line([(w * 0.42, horizon), (w * 0.32, h)], fill=(201, 162, 39, 255), width=4)
    sd.line([(w * 0.58, horizon), (w * 0.68, h)], fill=(201, 162, 39, 255), width=4)
    # Three flagpoles with simplified flags: USA, China, Russia.
    def flag(cx, kind):
        px0 = int(w * cx)
        sd.line([(px0, horizon - 118), (px0, horizon + 6)],
                fill=(220, 220, 220, 255), width=4)
        sd.ellipse([px0 - 4, horizon - 124, px0 + 4, horizon - 116],
                   fill=(201, 162, 39, 255))
        fx0, fy0, fw, fh = px0 + 4, horizon - 116, 52, 34
        if kind == "usa":
            for i in range(7):
                sd.rectangle([fx0, fy0 + i * fh // 7, fx0 + fw,
                              fy0 + (i + 1) * fh // 7],
                             fill=(178, 34, 28, 255) if i % 2 == 0
                             else (255, 255, 255, 255))
            sd.rectangle([fx0, fy0, fx0 + fw * 0.42, fy0 + fh * 0.55],
                         fill=(16, 32, 64, 255))
            for r in range(3):
                for c in range(4):
                    sd.ellipse([fx0 + 5 + c * 8, fy0 + 4 + r * 7,
                                fx0 + 8 + c * 8, fy0 + 7 + r * 7],
                               fill=(255, 255, 255, 255))
        elif kind == "china":
            sd.rectangle([fx0, fy0, fx0 + fw, fy0 + fh], fill=(222, 41, 16, 255))
            sd.polygon([(fx0 + 9, fy0 + 6), (fx0 + 12, fy0 + 13),
                        (fx0 + 19, fy0 + 13), (fx0 + 13, fy0 + 17),
                        (fx0 + 15, fy0 + 24), (fx0 + 9, fy0 + 20),
                        (fx0 + 3, fy0 + 24), (fx0 + 5, fy0 + 17),
                        (fx0 - 1, fy0 + 13), (fx0 + 6, fy0 + 13)],
                       fill=(255, 222, 0, 255))
        else:  # russia: white / blue / red horizontal bands
            for i, col in enumerate([(255, 255, 255, 255), (0, 57, 166, 255),
                                     (213, 0, 50, 255)]):
                sd.rectangle([fx0, fy0 + i * fh // 3, fx0 + fw,
                              fy0 + (i + 1) * fh // 3], fill=col)
    flag(0.16, "usa")
    flag(0.50, "china")
    flag(0.84, "russia")
    # Warm light pooling at the foot of the carpet.
    soft_disc(scene, [w * 0.34, h * 0.86, w * 0.66, h * 1.02],
              (255, 190, 110, 90), 26)
    draw_img.paste(scene.convert("RGB"), (x, y))


def cell(draw, x, y, w, h, bg, kicker, headline, deck, accent):
    draw.rectangle([x, y, x + w, y + h], fill=bg)
    draw.rectangle([x, y, x + w, y + 5], fill=accent)
    kf = font(SANS_BOLD, 15)
    draw.text((x + 14, y + 14), kicker, font=kf, fill=accent)
    hf = font(SANS_BLACK, 27)
    lines = wrap(draw, headline, hf, w - 28)
    ly = y + 38
    for ln in lines[:2]:
        draw.text((x + 14, ly), ln, font=hf, fill=(255, 255, 255))
        ly += 32
    df = font(SANS, 17)
    for ln in wrap(draw, deck, df, w - 28)[:2]:
        draw.text((x + 14, ly + 4), ln, font=df, fill=(225, 225, 225))
        ly += 22


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36
    # ---- Masthead ----
    centre(d, 14, "THE WORLD TODAY", font(SERIF_BLACK, 76), INK)
    d.line([(mx, 104), (W - mx, 104)], fill=INK, width=3)
    centre(d, 112, "THURSDAY,  19  NOVEMBER  2026", font(SANS_BOLD, 26), INK)
    centre(d, 146, "SHENZHEN  •  THE HAGUE  •  GAZA  •  NEW YORK  •  VICE CITY",
           font(SANS_BOLD, 15), (90, 90, 90))
    d.line([(mx, 172), (W - mx, 172)], fill=RED, width=5)
    # ---- Lead kicker + headline ----
    centre(d, 184, "FIRST TRILATERAL SUMMIT  •  APEC 2026", font(SANS_BLACK, 20), RED)
    hl = font(SERIF_BLACK, 56)
    for i, ln in enumerate(["TRUMP, XI AND PUTIN", "MEET IN SHENZHEN"]):
        centre(d, 212 + i * 60, ln, hl, INK)
    # ---- Lead illustration ----
    draw_lead_scene(img, mx, 340, W - 2 * mx, 330)
    d.rectangle([mx, 340, W - mx, 670], outline=INK, width=3)
    centre(d, 678, "Three leaders, one table: nuclear arms, Ukraine and Iran on the agenda — no deal expected.",
           font(SERIF, 19), INK)
    d.line([(mx, 710), (W - mx, 710)], fill=INK, width=2)
    # ---- Secondary stories: 2 x 2 grid ----
    gw, gh, gap = (W - 2 * mx - 16) // 2, 118, 16
    gy = 726
    cell(d, mx, gy, gw, gh, (24, 24, 34), "CULTURE  •  AFTER 13 YEARS",
         "VICE CITY OPENS", "GTA VI rolls out worldwide at midnight, first in New Zealand.", (255, 64, 160))
    cell(d, mx + gw + gap, gy, gw, gh, NAVY, "MARKETS  •  RECORD IPO",
         "$81.3BN DEBUT", "Anthropic lists on Nasdaq as ANT today, valued near $1.5 trillion.", (255, 190, 60))
    cell(d, mx, gy + gh + gap, gw, gh, (14, 64, 66), "JUSTICE  •  THE HAGUE",
         "A VERDICT 7 YEARS ON", "World court rules today on the Rohingya genocide case against Myanmar.", (120, 220, 210))
    cell(d, mx + gw + gap, gy + gh + gap, gw, gh, (74, 22, 20), "WAR  •  GAZA",
         "TROOPS CROSS THE LINE", "Israel launches a rare ground operation beyond the Gaza ceasefire line.", (255, 120, 90))
    # ---- Bottom ticker ----
    d.rectangle([0, 986, W, H], fill=INK)
    centre(d, 994, "CRIMEA BRIDGE ATTACKED AGAIN  •  CYCLONE AKVAN NEARS INDIA  •  VAN GOGH SELLS FOR $190.4M",
           font(SANS_BOLD, 16), (255, 255, 255))
    img.save(OUT, format="PNG", optimize=True)
    print(f"saved {OUT} {img.size} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
