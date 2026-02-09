#!/usr/bin/env python3
"""
Generate Homepage_Desktop_EveryoneHasAPrice.webp
Layout: matches Website_v5_Desktop_Top.webp — laurels in horizontal row across top.
Title HUMAN RESOURCE and tagline at bottom.
Uses top 5 normalized laurels, font paths and palette from poster scripts.
Output: 2700x4000 WebP.
"""

import os, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

# === PATHS ===
BASE = "/Users/mcg/Library/Mobile Documents/com~apple~CloudDocs/Projects/HUMAN RESOURCE"
STILLS_DIR = os.path.join(BASE, "HR Stills", "Processed")
LAURELS_DIR = os.path.join(BASE, "HR Stills", "Laurels", "Normalized")
OUTPUT_DIR = "/Users/mcg/Library/Mobile Documents/com~apple~CloudDocs/Website/Live/images"

# === FONTS (from poster scripts) ===
FC = "/System/Library/Fonts/Supplemental/Futura.ttc"
FR = "/System/Library/Fonts/Avenir Next.ttc"
FC_CONDENSED_EXBOLD = 4
FC_CONDENSED_MED = 3
FR_REG = 7

# === COLORS (from poster scripts) ===
CREAM = (235, 232, 222)
TAG_COLOR = (200, 210, 220)
CREDIT_COLOR = (195, 192, 185)
SHADOW_COLOR = (15, 18, 22)

# === DIMENSIONS (match Website_v5_Desktop_Top.webp exactly) ===
PW, PH = 2700, 4000

# === TOP 5 LAURELS ===
TOP_5_LAURELS = [
    "01_CFF_Chattanooga.png",
    "02_DWF_DancesWithFilms.png",
    "03_ScreamfestNOLA.png",
    "04_BIFF_Beloit.png",
    "05_BigBear.png",
]

CREDIT_LINE = "Starring Mia Vallet · Veanne Cox  |  Directed by Henry Chaisson  |  Written by Max Coyne-Green"
TAGLINE = "EVERYONE HAS A PRICE."


# === HELPERS (from poster scripts) ===

def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)

def _font(path, size, idx=0):
    return ImageFont.truetype(path, size, index=idx)

def tw(font, text):
    bb = font.getbbox(text)
    return bb[2] - bb[0]

def tracked_w(font, text, tracking):
    total = 0
    for i, c in enumerate(text):
        total += tw(font, c) + (tracking if i < len(text) - 1 else 0)
    return total

def draw_tracked(draw, x, y, text, font, color, tracking):
    for ch in text:
        cw = tw(font, ch)
        draw.text((x, y), ch, font=font, fill=color)
        x += cw + tracking

def draw_tracked_shadow(draw, x, y, text, font, color, tracking, sc=SHADOW_COLOR):
    for ox, oy in [(0, 3), (1, 3), (2, 2)]:
        cx = x + ox
        for ch in text:
            cw = tw(font, ch)
            draw.text((cx, y + oy), ch, font=font, fill=sc)
            cx += cw + tracking
    draw_tracked(draw, x, y, text, font, color, tracking)

def draw_shadow(draw, x, y, text, font, color, sc=SHADOW_COLOR):
    for ox, oy in [(0, 3), (1, 3), (2, 2)]:
        draw.text((x + ox, y + oy), text, font=font, fill=sc)
    draw.text((x, y), text, font=font, fill=color)

def smooth_gradient(img, direction, color, strength, sp=0.0, ep=1.0):
    w, h = img.size
    r, g, b = color
    if direction in ("up", "down"):
        strip = Image.new("L", (1, h), 0)
        px = strip.load()
        for y in range(h):
            f = y / max(h - 1, 1)
            if direction == "up":
                f = 1.0 - f
            t = (f - sp) / (ep - sp) if ep != sp else (1.0 if f >= sp else 0.0)
            px[0, y] = int(smoothstep(t) * strength * 255)
        a = strip.resize((w, h), Image.NEAREST)
    else:
        strip = Image.new("L", (w, 1), 0)
        px = strip.load()
        for x in range(w):
            f = x / max(w - 1, 1)
            if direction == "left":
                f = 1.0 - f
            t = (f - sp) / (ep - sp) if ep != sp else (1.0 if f >= sp else 0.0)
            px[x, 0] = int(smoothstep(t) * strength * 255)
        a = strip.resize((w, h), Image.NEAREST)
    cl = Image.new("RGB", (w, h), (r, g, b))
    cl.putalpha(a)
    return Image.alpha_composite(img.convert("RGBA"), cl).convert("RGB")

def vignette(img, strength=0.18, radius=0.80):
    w, h = img.size
    qw, qh = max(w // 6, 1), max(h // 6, 1)
    m = Image.new("L", (qw, qh), 0)
    px = m.load()
    cx, cy = qw / 2.0, qh / 2.0
    mx = math.sqrt(cx ** 2 + cy ** 2)
    for y in range(qh):
        dy2 = (y - cy) ** 2
        for x in range(qw):
            d = math.sqrt((x - cx) ** 2 + dy2) / mx
            t = smoothstep(max(0, (d - radius) / (1 - radius)) if d > radius else 0)
            px[x, y] = int(t * strength * 255)
    mask = m.resize((w, h), Image.LANCZOS)
    return Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), img, mask)

def film_grain(img, amount=5):
    w, h = img.size
    gw, gh = w // 2, h // 2
    random.seed(42)
    gs = Image.new("RGB", (gw, gh))
    gp = gs.load()
    for y in range(gh):
        for x in range(gw):
            v = max(0, min(255, int(random.gauss(128, amount * 4))))
            gp[x, y] = (v, v, v)
    grain = gs.resize((w, h), Image.BILINEAR)
    bl = ImageChops.add(img.convert("RGB"), grain, scale=2, offset=-10)
    return Image.blend(img.convert("RGB"), bl, amount / 30.0)


# === MAIN ===

def create_base():
    """Load hr poster.jpg, clean it up (same as original_v9), upscale to 2700x4000."""
    p = Image.open(os.path.join(STILLS_DIR, "hr poster.jpg")).convert("RGB")
    px = p.load()
    ow, oh = p.size

    # Remove old Chattanooga laurel (top-left corner)
    for y in range(0, 76):
        samples = [px[sx, y] for sx in range(100, 170) if sx < ow]
        avg = tuple(sum(c[i] for c in samples) // len(samples) for i in range(3))
        for x in range(0, 88):
            px[x, y] = avg
    for y in range(0, 76):
        for x in range(85, 105):
            t = (x - 85) / 20
            a = px[84, y]
            b = px[x, y]
            px[x, y] = tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))
    for y in range(72, 86):
        t = (y - 72) / 14
        for x in range(0, 100):
            a = px[x, 71]
            b = px[x, y]
            px[x, y] = tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))
    lp = p.crop((0, 0, 110, 92))
    lp = lp.filter(ImageFilter.GaussianBlur(2.0))
    p.paste(lp, (0, 0))

    # Remove mid-poster tagline
    px = p.load()
    ty_s, ty_e = 388, 416
    above_r, below_r = range(376, 388), range(418, 432)
    for x in range(130, 410):
        above = [px[x, ay] for ay in above_r if ay < oh]
        av = tuple(sum(c[i] for c in above) // len(above) for i in range(3))
        below = [px[x, by] for by in below_r if by < oh]
        bl = tuple(sum(c[i] for c in below) // len(below) for i in range(3))
        span = ty_e - ty_s
        for y in range(ty_s, ty_e + 1):
            t = (y - ty_s) / span
            px[x, y] = tuple(int(av[i] * (1 - t) + bl[i] * t) for i in range(3))

    orig = Image.open(os.path.join(STILLS_DIR, "hr poster.jpg")).convert("RGB").load()
    for x in range(120, 135):
        t = (x - 120) / 15
        for y in range(ty_s, ty_e + 1):
            ref = orig[x, y]
            mod = px[x, y]
            px[x, y] = tuple(int(ref[i] * (1 - t) + mod[i] * t) for i in range(3))
    orig_img = Image.open(os.path.join(STILLS_DIR, "hr poster.jpg")).convert("RGB")
    orig_px = orig_img.load()
    for x in range(400, 420):
        t = (x - 400) / 20
        for y in range(ty_s, ty_e + 1):
            mod = px[x, y]
            o = orig_px[x, y]
            px[x, y] = tuple(int(mod[i] * (1 - t) + o[i] * t) for i in range(3))
    for y in range(380, ty_s):
        t = (y - 380) / (ty_s - 380)
        for x in range(130, 410):
            o = orig_px[x, y]
            mod = px[x, y]
            px[x, y] = tuple(int(o[i] * (1 - t) + mod[i] * t) for i in range(3))
    for y in range(ty_e, ty_e + 8):
        t = (y - ty_e) / 8
        for x in range(130, 410):
            mod = px[x, y]
            o = orig_px[x, y]
            px[x, y] = tuple(int(mod[i] * (1 - t) + o[i] * t) for i in range(3))
    mid = p.crop((115, 376, 425, ty_e + 14))
    mid = mid.filter(ImageFilter.GaussianBlur(1.5))
    p.paste(mid, (115, 376))

    # Darken bottom
    px = p.load()
    for y in range(650, oh):
        t = min(1.0, (y - 650) / 60)
        t = t * t * (3 - 2 * t)
        for x in range(0, ow):
            r, g, b = px[x, y]
            f = 1.0 - t * 0.7
            px[x, y] = (max(0, int(r * f)), max(0, int(g * f)), max(0, int(b * f)))

    # Upscale
    p = p.resize((PW, PH), Image.LANCZOS)
    p = ImageEnhance.Sharpness(p).enhance(1.1)
    return p


def load_top5_laurels(height):
    """Load the top 5 normalized laurels at given height."""
    items = []
    for name in TOP_5_LAURELS:
        path = os.path.join(LAURELS_DIR, name)
        try:
            l = Image.open(path).convert("RGBA")
            r = height / l.height
            items.append(l.resize((int(l.width * r), height), Image.LANCZOS))
        except Exception as e:
            print(f"  WARN: {name}: {e}")
    return items


def place_laurels_top(canvas, items, y_center, gap=30):
    """Place laurels in a horizontal row centered at y_center (matching Website_v5 top layout)."""
    rgba = canvas.convert("RGBA")
    total = sum(l.width for l in items) + gap * (len(items) - 1)
    max_w = PW - 120  # some margin on sides
    its = items
    if total > max_w:
        sc = max_w / total
        its = [l.resize((int(l.width * sc), int(l.height * sc)), Image.LANCZOS) for l in items]
        total = sum(l.width for l in its) + gap * (len(its) - 1)
    x = (PW - total) // 2
    for l in its:
        rgba.paste(l, (x, y_center - l.height // 2), l)
        x += l.width + gap
    return rgba.convert("RGB")


def main():
    print("Creating clean base image...")
    base = create_base()
    print(f"  Base ready: {base.size}")

    # Apply style: grainy look (matching the poster scripts' GRAINY style)
    img = ImageEnhance.Contrast(base).enhance(1.08)
    img = vignette(img, 0.18, 0.80)
    img = film_grain(img, 5)

    # Gradient for top (to darken behind laurels) and bottom (for title/tagline)
    img = smooth_gradient(img, "down", (0, 0, 0), 0.50, 0.0, 0.15)   # top fade
    img = smooth_gradient(img, "up", (0, 0, 0), 0.65, 0.30, 1.0)     # bottom fade

    # === LAURELS AT TOP (matching Website_v5 layout) ===
    print("Loading top 5 laurels...")
    laurels = load_top5_laurels(height=100)
    print(f"  Loaded {len(laurels)} laurels")

    # Place laurels across the top — in Website_v5, they're near y ~60-80 area (proportional)
    # At 2700x4000, the top laurel strip sits at about y=70 (center of laurels)
    img = place_laurels_top(img, laurels, y_center=80, gap=35)

    # === TITLE AT BOTTOM ===
    draw = ImageDraw.Draw(img)

    title_font = _font(FC, 200, FC_CONDENSED_EXBOLD)
    tracking = 30

    # "HUMAN" and "RESOURCE" stacked, centered
    tw_human = tracked_w(title_font, "HUMAN", tracking)
    tw_resource = tracked_w(title_font, "RESOURCE", tracking)

    # Position title — comfortably above the tagline area
    title_y = PH - 700
    draw_tracked_shadow(draw, (PW - tw_human) // 2, title_y, "HUMAN", title_font, CREAM, tracking)
    draw_tracked_shadow(draw, (PW - tw_resource) // 2, title_y + 215, "RESOURCE", title_font, CREAM, tracking)

    # === TAGLINE ===
    tag_font = _font(FC, 58, FC_CONDENSED_MED)
    tag_tracking = 6
    tw_tag = tracked_w(tag_font, TAGLINE, tag_tracking)
    tag_y = title_y + 475
    draw_tracked_shadow(draw, (PW - tw_tag) // 2, tag_y, TAGLINE, tag_font, TAG_COLOR, tag_tracking)

    # === CREDIT LINE at very bottom ===
    cf = _font(FR, 24, FR_REG)
    cw = tw(cf, CREDIT_LINE)
    draw_shadow(draw, (PW - cw) // 2, PH - 55, CREDIT_LINE, cf, CREDIT_COLOR)

    # === SAVE AS WEBP ===
    output_path = os.path.join(OUTPUT_DIR, "Homepage_Desktop_EveryoneHasAPrice.webp")
    img.save(output_path, "WEBP", quality=90)
    print(f"\nSaved: {output_path}")
    print(f"Final size: {img.size}")
    print("Done!")


if __name__ == "__main__":
    main()
