"""Create an original 512px listing mark; packaging asset, not buyer runtime."""
from pathlib import Path
from PIL import Image, ImageDraw

image = Image.new("RGB", (512, 512), "#142b40")
draw = ImageDraw.Draw(image)
for y in (122, 226, 330):
    draw.rounded_rectangle((96, y, 208, y + 60), radius=15, fill="#eaf0f5")
    draw.rounded_rectangle((252, y, 364, y + 60), radius=15, fill="#eaf0f5")
draw.line([(275, 263), (300, 288), (395, 187)], fill="#e2af53", width=28, joint="curve")
image.save(Path(__file__).resolve().parent / "listing-logo.png")
