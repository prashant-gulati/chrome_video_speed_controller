"""Generate PNG icons for the Chrome extension (no external dependencies)."""
import struct
import zlib
import os
import math

def make_png(width, height, pixels_rgb):
    """Build a minimal valid PNG from raw RGB pixel data (list of (r,g,b) tuples)."""
    def chunk(tag, data):
        raw = tag + data
        return struct.pack('>I', len(data)) + raw + struct.pack('>I', zlib.crc32(raw) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
    raw_rows = b''
    for y in range(height):
        raw_rows += b'\x00'  # filter: None
        for x in range(width):
            r, g, b = pixels_rgb[y * width + x]
            raw_rows += bytes([r, g, b])

    signature = b'\x89PNG\r\n\x1a\n'
    return (
        signature
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', zlib.compress(raw_rows, 9))
        + chunk(b'IEND', b'')
    )


def draw_icon(size):
    """Draw a rounded-rectangle icon with a play symbol and a speed bar."""
    pixels = []
    cx, cy = size / 2, size / 2
    radius = size * 0.42
    pad = size * 0.08

    # Colors
    bg       = (15,  15,  19)   # near-black background
    accent   = (99,  102, 241)  # indigo
    white    = (240, 240, 248)

    for y in range(size):
        for x in range(size):
            nx, ny = x - cx, y - cy

            # Rounded rect mask (superellipse approximation)
            in_bg = (abs(nx) / (radius) ** 4 + abs(ny) / (radius) ** 4) < (1 / (radius) ** 3 * radius) \
                     if False else True  # full square; we'll crop corners below

            # Simple corner rounding via distance from corners
            r = size * 0.18
            in_bg = True
            corners = [(pad, pad), (size-1-pad, pad), (pad, size-1-pad), (size-1-pad, size-1-pad)]
            for (cx2, cy2) in corners:
                if x < cx2 + r and x > cx2 - r and y < cy2 + r and y > cy2 - r:
                    dist = math.hypot(x - cx2, y - cy2)
                    if dist > r:
                        in_bg = False
                        break

            if not in_bg:
                pixels.append((0, 0, 0))
                continue

            # Draw lightning bolt / play triangle
            # Simple equilateral triangle pointing right, centered
            tri_cx = cx - size * 0.04
            tri_h  = size * 0.42
            tri_w  = tri_h * 0.87

            # Triangle: tip at (tri_cx + tri_w*0.5, cy),
            #           base left corners at (tri_cx - tri_w*0.5, cy ± tri_h/2)
            tx = x - tri_cx
            ty = y - cy

            # Is point inside triangle?
            # Using barycentric check for right-pointing triangle
            half_h = tri_h / 2
            half_w = tri_w / 2
            in_tri = False
            if tx >= -half_w and tx <= half_w:
                # At horizontal position tx, the allowed vertical span shrinks linearly to the tip
                allowed = half_h * (1 - (tx + half_w) / tri_w)
                if abs(ty) <= allowed:
                    in_tri = True

            # Speed bar: small bar beneath (only for larger icons)
            bar_h = max(2, size // 16)
            bar_w = size * 0.55
            bar_y = cy + tri_h * 0.55
            in_bar = (abs(x - cx) <= bar_w / 2) and (abs(y - bar_y) <= bar_h / 2)

            # Right-side bar (shorter, lighter)
            bar2_x = cx + bar_w * 0.18
            bar2_w = bar_w * 0.4
            bar2_y = cy + tri_h * 0.55 + bar_h * 2.2
            in_bar2 = (x >= bar2_x - bar2_w / 2) and (x <= bar2_x + bar2_w / 2) \
                      and (abs(y - bar2_y) <= bar_h / 2) and size >= 32

            if in_tri:
                pixels.append(white)
            elif in_bar:
                pixels.append(accent)
            elif in_bar2:
                r2, g2, b2 = accent
                pixels.append((r2, g2, b2))
            else:
                pixels.append(bg)

    return pixels


os.makedirs('icons', exist_ok=True)
for size in [16, 48, 128]:
    pixels = draw_icon(size)
    png_data = make_png(size, size, pixels)
    path = f'icons/icon{size}.png'
    with open(path, 'wb') as f:
        f.write(png_data)
    print(f'Created {path}  ({len(png_data)} bytes)')

print('Done.')
