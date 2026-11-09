"""Builds the app icon: a calculator whose display shows the bconnTech logo mark.

Run:  python tools/make_icons.py        (needs Google Chrome + Pillow)
Writes the web/PWA icons into ../icons and the Android launcher icons in
android-app/android/app/src/main/res/mipmap-*.
"""
import os, subprocess, tempfile
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
ICONS = os.path.join(ROOT, "icons")
RES = os.path.join(ROOT, "android-app", "android", "app", "src", "main", "res")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
LOGO = "file:///" + os.path.join(ROOT, "bconntech_logo.png").replace("\\", "/")

def calc_group():
    # calculator body 560x740 at (232,142) inside a 1024 canvas
    x, y, w, h = 232, 142, 560, 740
    pad, dh = 38, 262
    dx, dy, dw = x + pad, y + pad + 6, w - 2 * pad
    ky0 = dy + dh + 34
    gap, kh = 16, 78
    kw = (dw - 3 * gap) / 4
    keys = []
    for r in range(4):
        for c in range(4):
            kx = dx + c * (kw + gap)
            ky = ky0 + r * (kh + gap)
            if c == 3:
                fill = "#1fa35a" if r == 3 else "#3a56c4"
            else:
                fill = "#c9d1ee"
            keys.append(f'<rect x="{kx:.1f}" y="{ky:.1f}" width="{kw:.1f}" height="{kh}" rx="20" fill="{fill}"/>')
            if c == 3 and r < 3:   # lighter top edge on the operator keys
                keys.append(f'<rect x="{kx+10:.1f}" y="{ky+8:.1f}" width="{kw-20:.1f}" height="6" rx="3" fill="#fff" opacity=".25"/>')
    # logo glyph (cropped square around the three nodes) centred in the display
    gs = dh + 40
    gx, gy = dx + dw / 2 - gs / 2, dy + dh / 2 - gs / 2
    return f"""
    <rect x="{x}" y="{y+16}" width="{w}" height="{h}" rx="64" fill="#000" opacity=".28" filter="url(#blur)"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="64" fill="#f4f6ff"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="64" fill="none" stroke="#ffffff" stroke-width="3" opacity=".7"/>
    <rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="26" fill="#0f2174"/>
    <rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="26" fill="none" stroke="#2b3f9a" stroke-width="3"/>
    <svg x="{dx}" y="{dy}" width="{dw}" height="{dh}" viewBox="0 0 {dw} {dh}">
      <defs><radialGradient id="fade" cx="50%" cy="50%" r="50%"><stop offset="0.9" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>
      <mask id="m"><rect width="{gs}" height="{gs}" fill="url(#fade)"/></mask></defs>
      <g transform="translate({dw/2-gs/2:.1f} {dh/2-gs/2:.1f})">
        <image href="{LOGO}" x="{-270*gs/500:.1f}" y="{-230*gs/500:.1f}" width="{1024*gs/500:.1f}" height="{1024*gs/500:.1f}" mask="url(#m)"/>
      </g>
    </svg>
        {''.join(keys)}
    """

def page(variant):
    bg = """<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2d45a6"/><stop offset="1" stop-color="#101c4f"/></linearGradient>
    <filter id="blur"><feGaussianBlur stdDeviation="18"/></filter></defs>"""
    group = calc_group()
    if variant == "any":      # rounded-square tile, transparent corners
        body = f'<rect width="1024" height="1024" rx="228" fill="url(#g)"/>{group}'
    else:                     # full-bleed, content a bit smaller (safe for masks / adaptive icons)
        body = f'<rect width="1024" height="1024" fill="url(#g)"/><g transform="translate(512 512) scale(0.8) translate(-512 -512)">{group}</g>'
    return f'<!doctype html><html><body style="margin:0;background:transparent"><svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">{bg}{body}</svg></body></html>'

tmp = tempfile.mkdtemp(prefix="ico_")
masters = {}
for v in ("any", "bleed"):
    f = os.path.join(tmp, v + ".html")
    open(f, "w", encoding="utf-8").write(page(v))
    out = os.path.join(tmp, v + ".png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", "--default-background-color=00000000",
                    f"--user-data-dir={tmp}\\prof", "--window-size=1024,1024", "--virtual-time-budget=4000",
                    f"--screenshot={out}", "file:///" + f.replace("\\", "/")],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    masters[v] = Image.open(out).convert("RGBA")
    print(v, masters[v].size)

def save(img, path, size):
    img.resize((size, size), Image.LANCZOS).save(path)

any_, bleed = masters["any"], masters["bleed"]
save(any_, os.path.join(ICONS, "icon-512.png"), 512)
save(any_, os.path.join(ICONS, "icon-192.png"), 192)
save(bleed, os.path.join(ICONS, "icon-maskable-512.png"), 512)
save(bleed, os.path.join(ICONS, "apple-touch-icon.png"), 180)
save(bleed, os.path.join(ICONS, "store-icon-1024.png"), 1024)

if os.path.isdir(RES):
    for d, legacy, fg in (("mdpi", 48, 108), ("hdpi", 72, 162), ("xhdpi", 96, 216), ("xxhdpi", 144, 324), ("xxxhdpi", 192, 432)):
        base = os.path.join(RES, "mipmap-" + d)
        save(any_, os.path.join(base, "ic_launcher.png"), legacy)
        save(bleed, os.path.join(base, "ic_launcher_foreground.png"), fg)
        r = bleed.resize((legacy * 4, legacy * 4), Image.LANCZOS)          # supersample for a clean circle
        m = Image.new("L", r.size, 0); ImageDraw.Draw(m).ellipse((0, 0, r.size[0] - 1, r.size[1] - 1), fill=255)
        r.putalpha(m); r.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(base, "ic_launcher_round.png"))
print("icons written")
