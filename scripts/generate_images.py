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
    size = (2200, 1300)
    base = Image.new("L", size, color=5)
    draw = ImageDraw.Draw(base)

    # Brutalist architecture blocks.
    for i in range(16):
        x = random.randint(-200, 1800)
        y = random.randint(120, 1100)
        w = random.randint(180, 520)
        h = random.randint(120, 420)
        fill = random.randint(18, 52)
        draw.rectangle((x, y, x + w, y + h), fill=fill)
        if i % 2 == 0:
            draw.rectangle((x + 8, y + 8, x + w - 8, y + h - 8), outline=random.randint(60, 95), width=2)

    # Architectural guide lines.
    for x in range(-250, 2400, 130):
        draw.line((x, 0, x + 380, size[1]), fill=24, width=2)

    light = _vertical_gradient(size, top=130, bottom=15)
    base = ImageChops.screen(base, light.filter(ImageFilter.GaussianBlur(40)))
    base = base.filter(ImageFilter.GaussianBlur(1.5))
    rgb = ImageOps.colorize(base, black="#030303", white="#6f7279")
    rgb = ImageEnhance.Contrast(rgb).enhance(1.25)
    rgb = ImageEnhance.Brightness(rgb).enhance(0.86)
    rgb = Image.alpha_composite(rgb.convert("RGBA"), _grain_overlay(size))
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

    # Stylized portrait silhouette (editorial framing).
    portrait = Image.new("L", size, 0)
    pdraw = ImageDraw.Draw(portrait)
    pdraw.polygon(
        [
            (455, 1580),
            (610, 1120),
            (800, 1040),
            (930, 1180),
            (1040, 1580),
            (800, 1700),
            (520, 1680),
        ],
        fill=28,
    )
    pdraw.polygon(
        [
            (550, 1530),
            (640, 1190),
            (780, 1115),
            (890, 1220),
            (975, 1560),
            (810, 1640),
            (590, 1615),
        ],
        fill=8,
    )
    pdraw.ellipse((625, 560, 905, 900), fill=34)
    pdraw.polygon([(620, 760), (560, 960), (690, 930), (710, 760)], fill=22)

    # Hair and shoulder structures.
    pdraw.pieslice((560, 500, 1000, 980), 190, 360, fill=12)
    pdraw.polygon([(620, 820), (560, 1040), (690, 1110), (780, 905)], fill=15)
    pdraw.polygon([(880, 825), (1025, 1010), (910, 1110), (800, 905)], fill=14)

    # Rim highlight to create cinematic edge.
    rim = portrait.filter(ImageFilter.GaussianBlur(8))
    rim = ImageEnhance.Brightness(rim).enhance(1.9)
    canvas = ImageChops.screen(canvas, rim)
    canvas = ImageChops.multiply(canvas, ImageOps.invert(portrait).point(lambda p: min(255, p + 220)))
    canvas = ImageChops.screen(canvas, portrait)
    canvas = canvas.filter(ImageFilter.GaussianBlur(0.8))
    canvas = ImageEnhance.Contrast(canvas).enhance(1.45)
    canvas = ImageEnhance.Sharpness(canvas).enhance(1.7)

    out = ImageOps.colorize(canvas, black="#050505", white="#f4f4f4")
    out = Image.alpha_composite(out.convert("RGBA"), _grain_overlay(size, opacity=34))
    out.convert("RGB").save(IMAGE_DIR / "founder.jpg", quality=93, optimize=True)


def build_pillar(name: str, angle: float, shade: int) -> None:
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

    cx, cy = int(w * 0.72), int(h * 0.52)
    for ring in range(9):
        r = 70 + ring * 42
        strength = max(0, 130 - ring * 12)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=30 + strength, width=3)

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
    build_pillar("neural-recovery.jpg", 56, 120)
    build_pillar("biometric-sync.jpg", 41, 112)
    build_pillar("architectural-strength.jpg", 65, 118)
    build_mark()
    print(f"Generated assets in {IMAGE_DIR}")
