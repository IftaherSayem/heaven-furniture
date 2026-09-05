"""
Clean the baked-in marketing overlay (HEAVEN logo, "CRAFTED FOR LUXURY LIVING"
headline, and the bottom location/@handle bar) off Heaven's real product photos,
then drop them into the correct image slots.

Strategy: on every branded post the furniture sits in the middle of the frame.
The logo + headline live in the TOP band and the location bar in the BOTTOM
sliver. We crop those bands away, leaving a clean editorial furniture shot.
The page uses CSS background cover, so exact aspect ratio doesn't matter — we
just need the text gone. A gentle contrast/warmth polish keeps it rich.

Hero is left untouched (already cropped clean by crop_hero.py).

Output: images/<slot>.jpg
Requires: pip install pillow
"""

import pathlib
from PIL import Image, ImageEnhance

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parent
REF = pathlib.Path("D:/antigravity/ref")
OUT = PROJECT / "images"

# slot -> (source filename, top_crop_frac, bottom_crop_frac)
# Branded posts: strip top 33% (logo + headline) and bottom 10% (location bar).
# Office shot: only a small corner caption at the very bottom -> trim bottom only.
JOBS = {
    "studio":      ("768205284_1711404377657721_1644144981235924073_n.jpg", 0.33, 0.10),
    "living-room": ("761596606_1700154842116008_2266593655759211928_n.jpg", 0.33, 0.10),
    "bedroom":     ("781162830_1725721782892647_3495497836840174995_n.jpg", 0.33, 0.10),
    "dining":      ("789032972_1731039082360917_6016848336243028580_n.jpg", 0.33, 0.10),
    "office":      ("737191325_1672336838231142_2215111771442126262_n.jpg", 0.00, 0.12),
    "bespoke":     ("768371614_1710462144418611_5698540196193769070_n.jpg", 0.33, 0.10),
    "cta":         ("775777922_1719636230167869_56427641527955046_n.jpg",  0.33, 0.10),
}


def process(src_name, top_frac, bottom_frac, out_path):
    src = REF / src_name
    img = Image.open(src).convert("RGB")
    w, h = img.size

    top = int(h * top_frac)
    bottom = int(h * (1 - bottom_frac))
    band = img.crop((0, top, w, bottom))

    # Gentle polish so it reads rich, not flat.
    band = ImageEnhance.Contrast(band).enhance(1.04)
    band = ImageEnhance.Color(band).enhance(1.05)

    band.save(out_path, "JPEG", quality=88)
    print("wrote", out_path.name, band.size)


def main():
    for slot, (src_name, top_frac, bottom_frac) in JOBS.items():
        process(src_name, top_frac, bottom_frac, OUT / (slot + ".jpg"))
    print("\nDone. Cleaned images in:", OUT)


if __name__ == "__main__":
    main()
