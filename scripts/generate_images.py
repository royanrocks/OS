#!/usr/bin/env python3
from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"
IMAGE_DIR.mkdir(exist_ok=True, parents=True)


def _grain_overlay(size: tuple[int, int], opacity: int = 26) -> Image.Image:
    noise = Image.effect_noise(size, 42).convert("L")
    noise = ImageOps.autocontrast(noise)
    return Image.merge("RGBA", (noise, noise, noise, Image.new("L", size, opacity)))


def _vertical_gradient(size: tuple[int, int], top: int, bottom: int) -> Image.Image:
    w, h = size
    grad = Image.new("L", (1, h))
    for y in range(h):
        v = int(top + (bottom - top) * (y / max(1, h - 1)))
        grad.putpixel((0, y), v)
    return grad.resize((w, h))


def build_hero() -> None:
    size = (2600, 1500)
    base = Image.new("L", size, color=5)
    draw = ImageDraw.Draw(base)

    # Brutalist architecture blocks with stronger depth.
    for i in range(24):
        x = random.randint(-260, 2200)
        y = random.randint(130, 1320)
        w = random.randint(200, 560)
        h = random.randint(130, 480)
        fill = random.randint(16, 54)
        draw.rectangle((x, y, x + w, y + h), fill=fill)
        if i % 2 == 0:
            draw.rectangle((x + 8, y + 8, x + w - 8, y + h - 8), outline=random.randint(60, 95), width=2)

    # Architectural guide lines and perspective floor bands.
    for x in range(-350, 2850, 120):
        draw.line((x, 0, x + 440, size[1]), fill=24, width=2)
    for y in range(840, 1500, 46):
        draw.line((0, y, size[0], y + int((y - 840) * 0.12)), fill=20, width=2)

    light = _vertical_gradient(size, top=140, bottom=8)
    base = ImageChops.screen(base, light.filter(ImageFilter.GaussianBlur(46)))
    beam = Image.new("L", size, 0)
    bdraw = ImageDraw.Draw(beam)
    bdraw.polygon([(0, 200), (1350, 520), (1550, 900), (0, 900)], fill=96)
    base = ImageChops.screen(base, beam.filter(ImageFilter.GaussianBlur(60)))
    base = base.filter(ImageFilter.GaussianBlur(1.4))
    rgb = ImageOps.colorize(base, black="#030303", white="#6f7279")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.34)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.83)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.2)
    rgb = Image.alpha_composite(rgb.convert("RGBA"), _grain_overlay(size, opacity=24))
    rgb.convert("RGB").save(IMAGE_DIR / "hero-architecture.jpg", quality=92, optimize=True)


def build_founder() -> None:
    size = (1400, 1800)
    canvas = Image.new("L", size, color=10)
    draw = ImageDraw.Draw(canvas)

    # Soft-focus brutalist background.
    for _ in range(22):
        x = random.randint(-150, 1350)
        y = random.randint(-100, 1700)
        w = random.randint(220, 620)
        h = random.randint(190, 600)
        shade = random.randint(20, 50)
        draw.rectangle((x, y, x + w, y + h), fill=shade)

    # High contrast key light sweep.
    sweep = Image.new("L", size, 0)
    sweep_draw = ImageDraw.Draw(sweep)
    for i in range(20):
        radius = 350 + i * 40
        alpha = max(0, 120 - i * 6)
        bbox = (-130, 260 - i * 10, radius * 2, 260 + radius * 2)
        sweep_draw.ellipse(bbox, fill=alpha)
    canvas = ImageChops.screen(canvas, sweep.filter(ImageFilter.GaussianBlur(45)))

    # Team-oriented silhouette composition for OS Master Trainers.
    portrait = Image.new("L", size, 0)
    pdraw = ImageDraw.Draw(portrait)
    figures = [
        ((250, 760, 530, 1040), (220, 1060, 560, 1760)),
        ((520, 680, 860, 1080), (470, 1040, 920, 1780)),
        ((860, 750, 1160, 1060), (820, 1070, 1200, 1760)),
    ]
    for head_box, torso_box in figures:
        pdraw.ellipse(head_box, fill=36)
        hx1, hy1, hx2, hy2 = torso_box
        pdraw.polygon(
            [
                (hx1, hy2 - 80),
                (hx1 + 80, hy1 + 60),
                (hx2 - 70, hy1 + 40),
                (hx2, hy2 - 60),
                (hx2 - 140, hy2 + 30),
                (hx1 + 100, hy2 + 20),
            ],
            fill=26,
        )
        pdraw.polygon(
            [
                (hx1 + 75, hy2 - 120),
                (hx1 + 140, hy1 + 130),
                (hx2 - 150, hy1 + 110),
                (hx2 - 90, hy2 - 130),
            ],
            fill=9,
        )

    # Rim highlight to create cinematic depth.
    rim = portrait.filter(ImageFilter.GaussianBlur(9))
    rim = ImageEnhance.Brightness(rim).enhance(1.9)
    canvas = ImageChops.screen(canvas, rim)
    canvas = ImageChops.multiply(canvas, ImageOps.invert(portrait).point(lambda p: min(255, p + 220)))
    canvas = ImageChops.screen(canvas, portrait)
    canvas = canvas.filter(ImageFilter.GaussianBlur(0.9))
    canvas = ImageEnhance.Contrast(canvas).enhance(1.52)
    canvas = ImageEnhance.Sharpness(canvas).enhance(1.8)

    out = ImageOps.colorize(canvas, black="#050505", white="#f4f4f4")
    out = Image.alpha_composite(out.convert("RGBA"), _grain_overlay(size, opacity=32))
    out.convert("RGB").save(IMAGE_DIR / "founder.jpg", quality=93, optimize=True)


def build_pillar(name: str, angle: float, shade: int, mode: str) -> None:
    size = (1400, 920)
    layer = Image.new("L", size, 12)
    draw = ImageDraw.Draw(layer)
    w, h = size

    for i in range(12):
        offset = int(i * 80)
        x1 = -300 + offset
        y1 = 130
        x2 = 220 + offset
        y2 = h - 120
        draw.polygon([(x1, y1), (x2, y1 - 70), (x2 + 180, y2), (x1 + 20, y2 + 110)], fill=20 + i * 3)

    if mode == "women":
        # Curved protection arcs + pulse markers.
        cx, cy = int(w * 0.7), int(h * 0.56)
        for ring in range(8):
            r = 95 + ring * 38
            strength = max(0, 138 - ring * 13)
            draw.arc((cx - r, cy - r, cx + r, cy + r), 200, 20, fill=34 + strength, width=4)
        for i in range(7):
            x = int(180 + i * 160)
            draw.ellipse((x, 700, x + 26, 726), fill=70 + i * 8)
    elif mode == "power":
        # Barbell and lane-inspired geometry.
        draw.rectangle((220, 500, 1180, 538), fill=120)
        for x in (260, 1140):
            for r in (42, 74, 100):
                draw.ellipse((x - r, 520 - r, x + r, 520 + r), outline=94 + (r // 8), width=6)
        for y in range(210, 860, 110):
            draw.line((740, y, 1320, y - 20), fill=66, width=4)
    else:
        # Strength and conditioning matrix.
        for gx in range(420, 1260, 96):
            draw.line((gx, 180, gx, 860), fill=55, width=3)
        for gy in range(200, 860, 84):
            draw.line((340, gy, 1320, gy), fill=55, width=3)
        for i in range(9):
            x = 420 + i * 96
            draw.rectangle((x - 12, 640 - (i % 3) * 60, x + 12, 860), fill=110)

    diag = Image.new("L", size, 0)
    ddraw = ImageDraw.Draw(diag)
    rad = math.radians(angle)
    for k in range(-8, 11):
        x = int((k * 150) + 100)
        ddraw.line((x, 0, int(x + h * math.cos(rad)), int(h * math.sin(rad))), fill=45, width=2)

    layer = ImageChops.screen(layer, diag)
    layer = ImageEnhance.Contrast(layer.filter(ImageFilter.GaussianBlur(0.6))).enhance(1.28)
    tint = ImageOps.colorize(layer, black="#090909", white=f"#{shade:02x}{shade:02x}{shade + 8:02x}")
    tint = Image.alpha_composite(tint.convert("RGBA"), _grain_overlay(size, opacity=20))
    tint.convert("RGB").save(IMAGE_DIR / name, quality=91, optimize=True)


def build_mark() -> None:
    size = (512, 512)
    base = Image.new("RGB", size, "#050505")
    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle((26, 26, 486, 486), radius=70, outline="#8f9398", width=3)
    draw.text((136, 180), "OS", fill="#eef0f2")
    base.save(IMAGE_DIR / "os-mark.png", optimize=True)


if __name__ == "__main__":
    random.seed(7)
    build_hero()
    build_founder()
    build_pillar("neural-recovery.jpg", 56, 120, "women")
    build_pillar("biometric-sync.jpg", 41, 112, "power")
    build_pillar("architectural-strength.jpg", 65, 118, "conditioning")
    build_mark()
    print(f"Generated assets in {IMAGE_DIR}")
