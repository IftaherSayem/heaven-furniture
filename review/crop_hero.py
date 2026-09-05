"""
Crop a clean landscape hero from a Heaven photo, removing the baked-in
watermark text that sits in the upper portion of the square source image.

We take the green velvet bed shot (the strongest luxury image) and keep a
wide band from the lower part of the frame — the bed + headboard — which is
free of the "MAJESTY GLAME" text and the top logo.

Output: images/hero.jpg  (landscape ~16:9)

Requires: pip install pillow
"""

import pathlib
from PIL import Image, ImageEnhance

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
REF = pathlib.Path("D:/antigravity/ref")
# Navy & gold velvet sofa: watermark text is only in the TOP band; the sofa
# fills the lower ~two-thirds, so a lower crop is clean AND keeps the subject.
SRC = REF / "784251271_1726752032789622_4156846528064326637_n.jpg"
OUT = PROJECT / "images" / "hero.jpg"

img = Image.open(SRC).convert("RGB")
w, h = img.size

# Skip the top band that holds "CRAFTED FOR LUXURY LIVING"; keep the sofa below.
top = int(h * 0.30)
band = img.crop((0, top, w, h))
bw, bh = band.size

# Now make it a pleasing landscape (16:9) by cropping height if needed,
# keeping the center of the remaining band.
target_ratio = 16 / 9
if bw / bh < target_ratio:
    # too tall -> trim height
    new_h = int(bw / target_ratio)
    y0 = (bh - new_h) // 2
    band = band.crop((0, y0, bw, y0 + new_h))

# Gentle polish: slight contrast + warmth so it reads rich, not flat.
band = ImageEnhance.Contrast(band).enhance(1.04)
band = ImageEnhance.Color(band).enhance(1.06)

band.save(OUT, "JPEG", quality=88)
print("wrote", OUT, band.size)
