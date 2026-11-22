"""Draw the PWA icons (the hero, sword raised, behind a brick wall). No image libraries needed: python3 tools/make_icons.py"""
import math, os, struct, zlib

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# the legend hero's sword-raised pose, cut off below the shoulders (the wall hides the rest)
ORIGIN = (-4, -1)
PAL = {"a": "#050505", "b": "#ffffff", "c": "#f0d878", "d": "#784016", "e": "#fcd820", "f": "#b01814", "g": "#d0a40c", "h": "#eeb92c", "i": "#f2b27a", "j": "#78401c", "k": "#dc3830", "l": "#b07c18"}
ROWS = [
    ".aa..................",
    "abca........aaa......",
    "abca....aaaaadda.....",
    "abbca.aaaddadddaaaa..",
    ".abca.adaddddddadda..",
    "..abcadddddddddddda..",
    "..abccadddddddeeda...",
    "...abcaadddddeefea...",
    "...abccaaageeeeeea...",
    "....abcahhadiiiiia...",
    "....abcchhadiaiaia...",
    "...ahahhhaiiiaiaia...",
    "...ahaiiaddiiiiiia...",
    "...ahaiijaaaiiiia....",
    "....aadaakkkaaaa.....",
    "......aadhhkkllkaaa..",
    "......aahhhlkkkhahha.",
]

BRICKS = [("#f0a060", "#d86a30", "#8c3818"), ("#f8d868", "#d8a828", "#8c6410"), ("#88d0d8", "#4898a8", "#205868"),
          ("#78a0e0", "#3868b8", "#1c3870"), ("#e07858", "#b84030", "#702018")]
WALL = [(64 * i, 448) for i in range(8)] + [(64 * i, 384) for i in range(8)]
SIZE = 512   # everything is laid out on this canvas, then averaged down to each icon size
rgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def master(scale, ox, oy, posts):
    img = [[None] * SIZE for _ in range(SIZE)]
    def rect(x, y, w, h, col):
        c = rgb(col)
        for j in range(max(0, int(y)), min(SIZE, int(y + h))):
            for i in range(max(0, int(x)), min(SIZE, int(x + w))):
                img[j][i] = c
    for y in range(0, SIZE, 8):   # rays, with a lighter disc behind the head
        for x in range(0, SIZE, 8):
            ray = int((math.atan2(y + 4 - 250, x + 4 - 256) + math.pi) / (math.pi / 10)) % 2
            rect(x, y, 8, 8, "#1f6068" if math.hypot(x + 4 - 264, y + 4 - 232) < 180 else "#154a56" if ray else "#103c48")
    for j, row in enumerate(ROWS):
        for i, ch in enumerate(row):
            if ch != ".":
                rect(ox + (ORIGIN[0] + i) * scale, oy + (ORIGIN[1] + j) * scale, scale, scale, PAL[ch])
    for n, (x, y) in enumerate(WALL + posts):
        hi, mid, lo = BRICKS[(n * 2 + (n > 7)) % 5]
        s, u = 64, 8
        rect(x, y, s, s, "#14101c"); rect(x + 4, y + 4, s - u, s - u, mid)
        rect(x + 4, y + 4, s - u, u, hi); rect(x + 4, y + 4, u, s - u, hi)
        rect(x + 4, y + s - 12, s - u, u, lo); rect(x + s - 12, y + 4, u, s - u, lo)
    return img


def save(img, size, path):
    raw = bytearray()
    span = lambda k: range(k * SIZE // size, max(k * SIZE // size + 1, math.ceil((k + 1) * SIZE / size)))
    for y in range(size):
        raw.append(0)
        for x in range(size):
            px = [img[j][i] for j in span(y) for i in span(x)]
            raw.extend(round(sum(v) / len(px)) for v in zip(*px))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)) \
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    with open(os.path.join(root, path), "wb") as f:
        f.write(data)


REGULAR = (19, 124, 106)
MASKABLE = (16, 146, 154)   # smaller, so face and sword stay inside the safe circle (80% of the icon)

if __name__ == "__main__":
    img = master(*REGULAR, [(448, 320), (0, 320)])
    save(img, 192, "icons/icon-192.png")
    save(img, 512, "icons/icon-512.png")
    save(img, 180, "icons/apple-touch-icon.png")
    save(master(*MASKABLE, []), 512, "icons/maskable-512.png")
    print("icons written")
