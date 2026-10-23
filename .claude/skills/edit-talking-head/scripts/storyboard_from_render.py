"""Storyboard from real frames: base video frames + rendered overlay test frames, labeled tiles.
usage: python3 -I storyboard_from_render.py <project_dir> "<title>"
expects <project_dir>/sb3/list.json = [[timecode, label, t], ...], sb3/bg<k>.png (base frames at t),
and sb3/ov/t_<t>.png (from render_overlay.js test mode). Writes <project_dir>/storyboard.png"""
import sys, json, glob
from PIL import Image, ImageDraw, ImageFont
P, title = sys.argv[1], sys.argv[2]; L = json.load(open(f"{P}/sb3/list.json"))
fb = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Bold.otf", 19)
fs = ImageFont.truetype("/usr/share/fonts/opentype/inter/Inter-Medium.otf", 15)
ovs = {float(x.split('t_')[1][:-4]): x for x in glob.glob(f"{P}/sb3/ov/t_*.png")}
tiles = []
for k, (tc, name, t) in enumerate(L):
    o = min(ovs, key=lambda v: abs(v - t))
    im = Image.alpha_composite(Image.open(f"{P}/sb3/bg{k}.png").convert("RGBA"), Image.open(ovs[o]).convert("RGBA")).resize((330, 587))
    tile = Image.new("RGB", (330, 647), "white"); tile.paste(im.convert("RGB"), (0, 60))
    d = ImageDraw.Draw(tile); d.text((6, 8), f"{k+1}. {tc}", font=fb, fill=(217, 130, 43)); d.text((6, 33), name, font=fs, fill=(29, 27, 24)); tiles.append(tile)
W = 4; H = (len(tiles) + W - 1) // W
sheet = Image.new("RGB", (W * 340 + 10, H * 657 + 70), (246, 242, 234)); ImageDraw.Draw(sheet).text((12, 18), title, font=fb, fill=(29, 27, 24))
for k, tl in enumerate(tiles): sheet.paste(tl, (10 + (k % W) * 340, 60 + (k // W) * 657))
sheet.save(f"{P}/storyboard.png")
