from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
import random

OUTPUT = Path("outputs/BEYOND_11_titlecard.png")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)


def load_font(size, bold=False):
    candidates = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def create_gradient(width, height):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    pixels = img.load()
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(12 + 26 * t)
        g = int(18 + 36 * t)
        b = int(34 + 60 * t)
        for x in range(width):
            pixels[x, y] = (r, g, b, 255)
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    gdraw.ellipse((2100, 60, 3600, 2000), fill=(200, 120, 70, 120))
    return Image.alpha_composite(img, glow)


def draw_manga_lines(draw, width, height):
    panel_color = (255, 255, 255, 35)
    for x in range(200, width, 520):
        draw.line((x, 0, x, height), fill=panel_color, width=2)
    for y in range(120, height, 430):
        draw.line((0, y, width, y), fill=panel_color, width=2)
    for i in range(10):
        x1 = 170 + i * 90
        y1 = 150 + i * 25
        x2 = x1 + 270
        y2 = y1 + 10
        draw.line((x1, y1, x2, y2), fill=(255, 255, 255, 28), width=4)


def draw_silhouette(draw, cx, cy, scale=1.1):
    draw.ellipse((cx - 110 * scale, cy - 80 * scale, cx + 110 * scale, cy + 100 * scale),
                 fill=(18, 22, 30))
    draw.rounded_rectangle((cx - 95 * scale, cy + 70 * scale, cx + 95 * scale, cy + 330 * scale),
                           radius=50, fill=(18, 22, 30))
    draw.ellipse((cx - 58 * scale, cy - 70 * scale, cx + 58 * scale, cy + 35 * scale),
                 fill=(18, 22, 30))
    draw.line((cx + 30 * scale, cy + 150 * scale, cx + 200 * scale, cy + 60 * scale),
              fill=(228, 176, 92), width=12)
    draw.line((cx + 20 * scale, cy + 160 * scale, cx - 120 * scale, cy + 220 * scale),
              fill=(18, 22, 30), width=18)
    draw.ellipse((cx + 200 * scale, cy + 15 * scale, cx + 255 * scale, cy + 70 * scale),
                 fill=(245, 245, 245))
    draw.ellipse((cx + 212 * scale, cy + 25 * scale, cx + 244 * scale, cy + 60 * scale),
                 fill=(220, 140, 80))


def add_paper_texture(img):
    width, height = img.size
    tex = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tex)
    for _ in range(1200):
        x = random.randint(0, width)
        y = random.randint(0, height)
        alpha = random.randint(8, 35)
        tdraw.point((x, y), fill=(255, 255, 255, alpha))
    return Image.alpha_composite(img, tex)


def draw_text(draw, width, height):
    title = "BEYOND 11"
    subtitle = "A STORY OF THE BALL, THE BREATH, AND THE RETURN"

    title_font = load_font(210, bold=True)
    sub_font = load_font(48, bold=True)

    title_box = draw.textbbox((0, 0), title, font=title_font)
    tx = (width - (title_box[2] - title_box[0])) / 2
    ty = 330

    sub_box = draw.textbbox((0, 0), subtitle, font=sub_font)
    sx = (width - (sub_box[2] - sub_box[0])) / 2
    sy = 600

    draw.text((tx + 8, ty + 8), title, font=title_font, fill=(18, 22, 30))
    draw.text((tx, ty), title, font=title_font, fill=(248, 243, 234))

    draw.text((sx + 8, sy + 8), subtitle, font=sub_font, fill=(20, 26, 34))
    draw.text((sx, sy), subtitle, font=sub_font, fill=(236, 231, 224))

    accent_y = sy + 86
    draw.line((width * 0.28, accent_y, width * 0.72, accent_y), fill=(220, 150, 80), width=8)


def generate():
    width, height = 3840, 2160
    img = create_gradient(width, height)
    draw = ImageDraw.Draw(img)
    draw_manga_lines(draw, width, height)
    draw_silhouette(draw, int(width * 0.52), int(height * 0.58), scale=1.2)
    draw_text(draw, width, height)
    draw.rounded_rectangle((32, 32, width - 32, height - 32), radius=26,
                           outline=(255, 255, 255, 120), width=4)
    img = add_paper_texture(img)
    img = img.filter(ImageFilter.GaussianBlur(0.35))
    img.save(OUTPUT)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    generate()
