from pathlib import Path
from PIL import Image, ImageOps

# Where the input pictures are
src = Path("C:/Migration/STI/images/in")

# Where the results will go
thumbs = Path("C:/Migration/STI/images/thumbs"); thumbs.mkdir(parents=True, exist_ok=True)
full = Path("C:/Migration/STI/images/full"); full.mkdir(parents=True, exist_ok=True)

def save_webp(img, path, quality=82):
    img.save(path, format="WEBP", quality=quality, method=6)

for p in src.glob("*"):
    if p.suffix.lower() not in {".jpg",".jpeg",".png",".webp"}: 
        continue
    im = Image.open(p).convert("RGB")
    w, h = im.size

    # Full image: longest side 1600px
    im_full = ImageOps.contain(im, (1600,1600))
    save_webp(im_full, full / (p.stem + ".webp"), quality=82)

    # Thumbnail: portrait = 600x800, landscape = 800x600
    if w > h:
        box = (800, 600)   # landscape
    else:
        box = (600, 800)   # portrait
    im_fit = ImageOps.contain(im, box)
    thumb = ImageOps.pad(im_fit, box, color=(11,11,11), centering=(0.5,0.5))
    save_webp(thumb, thumbs / (p.stem + ".webp"), quality=80)
