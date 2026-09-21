from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

BASE = Path(__file__).parent
PHOTO_DIR = BASE / "photos"
OUTPUT_DIR = BASE / "output"
W, H = 1800, 2700  # 12x18 inches at 150 DPI

def get_font(size, bold=False):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()

def fit_photo(path, size):
    return ImageOps.fit(Image.open(path).convert("RGB"), size,
                        method=Image.Resampling.LANCZOS)

def center_text(draw, y, text, size, bold=False):
    f = get_font(size, bold)
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((W - (box[2] - box[0])) // 2, y), text, font=f, fill="#6f4934")

def main():
    photos = sorted([p for p in PHOTO_DIR.iterdir()
                     if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}])

    img = Image.new("RGB", (W, H), "#f7efe7")
    d = ImageDraw.Draw(img)

    # Frame border
    d.rounded_rectangle((35, 35, W-35, H-35), 35, outline="#8a6a4a", width=24)
    d.rounded_rectangle((75, 75, W-75, H-75), 25, outline="#d4b483", width=6)

    center_text(d, 125, "HAPPY WEDDING ANNIVERSARY ❤️", 78, True)
    center_text(d, 235, "Our Memories • Our Journey • Our Love", 36)

    # Main photo
    mx, my, mw, mh = 150, 360, W-300, 720
    if photos:
        img.paste(fit_photo(photos[0], (mw, mh)), (mx, my))
    else:
        d.rounded_rectangle((mx, my, mx+mw, my+mh), 20, fill="#ead8c5")
        center_text(d, my+mh//2, "Add photos to the photos folder", 38)
    d.rounded_rectangle((mx, my, mx+mw, my+mh), 20, outline="white", width=10)

    center_text(d, 1145, "Together is our favorite place to be ❤️", 44, True)

    # 8 memory photos
    gx, gy, gap = 150, 1260, 24
    cols, rows = 4, 2
    cw, ch = (W-2*gx-gap*3)//4, 430

    for i in range(8):
        x = gx + (i % cols) * (cw + gap)
        y = gy + (i // cols) * (ch + gap)
        if i+1 < len(photos):
            img.paste(fit_photo(photos[i+1], (cw, ch)), (x, y))
        else:
            d.rounded_rectangle((x, y, x+cw, y+ch), 14, fill="#ead8c5")
            text = f"Memory {i+1}"
            f = get_font(28, True)
            b = d.textbbox((0,0), text, font=f)
            d.text((x+(cw-b[2]+b[0])//2, y+(ch-b[3]+b[1])//2),
                   text, font=f, fill="#8a6a4a")
        d.rounded_rectangle((x, y, x+cw, y+ch), 14, outline="white", width=8)

    center_text(d, 2215, "Still choosing you, every day. ❤️", 48, True)
    center_text(d, 2300, "From our first memories to forever...", 32)

    for x, y in [(130, 270), (1640, 270), (120, 2500), (1650, 2500)]:
        d.text((x, y), "♥", font=get_font(52, True), fill="#b66b5c")

    OUTPUT_DIR.mkdir(exist_ok=True)
    out = OUTPUT_DIR / "wedding_anniversary_frame_12x18.jpg"
    img.save(out, quality=95, dpi=(150, 150))
    print(out)

if __name__ == "__main__":
    main()
