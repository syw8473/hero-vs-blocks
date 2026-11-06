"""Draw the PWA icons from the hero's own pixel art in tile-kiln.html (no image libraries needed)."""
import re, zlib, struct, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
src = open(os.path.join(root, "tile-kiln.html"), encoding="utf-8").read()
hexes = lambda block: {k: v for k, v in re.findall(r'(\w):"(#[0-9a-fA-F]{6})"', block)}
pal = hexes(re.search(r"const BASE = \{(.*?)\};", src, re.S).group(1))
pal.update(hexes(re.search(r"const HERO_PAL = \{(.*?)\};", src, re.S).group(1)))
rows = re.findall(r'"([^"]+)"', re.search(r"const HERO_ROWS = \[(.*?)\];", src, re.S).group(1))
legs = re.findall(r'"([^"]+)"', re.search(r"const HERO_WALK = \[\s*\[(.*?)\],", src, re.S).group(1))
rows = rows[:21] + legs
W, H = len(rows[0]), len(rows)
on = lambda x, y: 0 <= x < W and 0 <= y < H and rows[y][x] != "."
grid = {}
for y in range(-1, H + 1):
    for x in range(-1, W + 1):
        if on(x, y): grid[(x, y)] = pal[rows[y][x]]
        elif on(x-1, y) or on(x+1, y) or on(x, y-1) or on(x, y+1): grid[(x, y)] = "#1a1420"
rgb = lambda h: tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def icon(size, path, pad):
    bg, glow, floor = rgb("#0e2a2d"), rgb("#163a3e"), rgb("#2a5a5e")
    scale = int(size * (1 - 2 * pad) / (H + 2))
    ox = (size - (W + 2) * scale) // 2; oy = (size - (H + 2) * scale) // 2
    img = [[bg] * size for _ in range(size)]
    cx, cy, r = size / 2, size / 2, size * (.5 - pad) * .95
    for y in range(size):
        for x in range(size):
            if (x - cx) ** 2 + (y - cy) ** 2 < r * r: img[y][x] = glow
    fy = oy + (H + 1) * scale
    for y in range(fy, min(size, fy + max(2, scale // 2))):
        for x in range(int(size * .2), int(size * .8)): img[y][x] = floor
    for (gx, gy), col in grid.items():
        c = rgb(col)
        for yy in range(oy + (gy + 1) * scale, oy + (gy + 2) * scale):
            for xx in range(ox + (gx + 1) * scale, ox + (gx + 2) * scale): img[yy][xx] = c
    raw = b"".join(b"\0" + bytes(v for px in row for v in px) for row in img)
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    open(os.path.join(root, path), "wb").write(data)
icon(192, "icons/icon-192.png", .08)
icon(512, "icons/icon-512.png", .08)
icon(512, "icons/maskable-512.png", .18)   # extra margin so round/squircle masks never clip the hero
icon(180, "icons/apple-touch-icon.png", .08)
print("icons written")
