"""Builds the Google Play graphics from the raw app captures in ./raw.

Run from anywhere:  python build_graphics.py
Outputs (../graphics): phone-1..6.png (1080x1920) and feature-graphic.png (1024x500).
Needs Google Chrome; paths below match this PC.
"""
import os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "graphics"))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
os.makedirs(OUT, exist_ok=True)

def url(p):
    return "file:///" + p.replace("\\", "/")

FONTS = url(os.path.join(ROOT, "vendor", "fonts.css"))
ICON = url(os.path.join(ROOT, "icons", "icon-512.png"))
RAW = lambda n: url(os.path.join(HERE, "raw", n))

BASE_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{overflow:hidden}
body{font-family:'Inter',system-ui,sans-serif;color:#fff;
 background:radial-gradient(120% 80% at 80% 0%,#3a56c4 0%,#233a94 38%,#14246b 70%,#0d1745 100%)}
.glow{position:absolute;border-radius:50%;filter:blur(60px);opacity:.35}
"""

def phone_page(head, sub, img):
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{BASE_CSS}
body{{width:1080px;height:1920px;position:relative}}
.glow.a{{width:700px;height:700px;background:#4f7cff;right:-200px;top:300px}}
.glow.b{{width:520px;height:520px;background:#1fa35a;left:-200px;top:1250px;opacity:.22}}
.tag{{position:absolute;left:90px;top:84px;display:flex;align-items:center;gap:18px}}
.tag img{{width:68px;height:68px;border-radius:16px}}
.tag span{{font-size:30px;font-weight:700;letter-spacing:.16em;opacity:.85}}
h1{{position:absolute;left:90px;right:90px;top:200px;font-size:92px;line-height:1.05;font-weight:800;letter-spacing:-.02em}}
p{{position:absolute;left:90px;right:90px;top:430px;font-size:42px;line-height:1.3;font-weight:500;opacity:.88}}
.phone{{position:absolute;left:150px;top:600px;width:780px;padding:14px 14px 0;border-radius:72px 72px 0 0;
 background:#0a1030;box-shadow:0 40px 90px -20px rgba(0,0,0,.7),0 0 0 3px #2a3a86}}
.phone img{{display:block;width:100%;border-radius:58px 58px 0 0}}
</style></head><body>
<div class="glow a"></div><div class="glow b"></div>
<div class="tag"><img src="{ICON}"><span>POS. BILLING. SALES.</span></div>
<h1>{head}</h1><p>{sub}</p>
<div class="phone"><img src="{RAW(img)}"></div>
</body></html>"""

def feature_page():
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>{BASE_CSS}
body{{width:1024px;height:500px;position:relative}}
.glow.a{{width:420px;height:420px;background:#4f7cff;right:60px;top:-80px}}
.logo{{position:absolute;left:64px;top:66px;width:96px;height:96px;border-radius:22px;box-shadow:0 12px 30px -10px rgba(0,0,0,.6)}}
h1{{position:absolute;left:64px;top:190px;font-size:56px;line-height:1.02;font-weight:800;letter-spacing:-.02em}}
.tg{{position:absolute;left:66px;top:274px;font-size:26px;font-weight:700;letter-spacing:.2em;color:#9fc0ff}}
ul{{position:absolute;left:66px;top:336px;list-style:none;font-size:25px;font-weight:600;line-height:1.5}}
li::before{{content:"";display:inline-block;width:10px;height:10px;border-radius:50%;background:#3ddc84;margin-right:14px}}
.ph{{position:absolute;border-radius:34px 34px 0 0;padding:7px 7px 0;background:#0a1030;box-shadow:0 24px 50px -14px rgba(0,0,0,.75),0 0 0 2px #2a3a86}}
.ph img{{display:block;width:100%;border-radius:28px 28px 0 0}}
.p1{{left:776px;top:92px;width:226px;transform:rotate(5deg)}}
.p2{{left:596px;top:48px;width:236px;transform:rotate(-3deg)}}
</style></head><body>
<div class="glow a"></div>
<img class="logo" src="{ICON}">
<h1>Shop Calculator</h1>
<div class="tg">POS. BILLING. SALES.</div>
<ul><li>Bills with discount &amp; tax</li><li>Daily totals &amp; history</li><li>PDF and Excel reports</li></ul>
<div class="ph p1"><img src="{RAW('e-history.jpg')}"></div>
<div class="ph p2"><img src="{RAW('b-enter.jpg')}"></div>
</body></html>"""

JOBS = [
    ("phone-1.png", 1080, 1920, phone_page("Ring up sales<br>in seconds", "Item, quantity, price, discount and tax", "b-enter.jpg")),
    ("phone-2.png", 1080, 1920, phone_page("Totals that<br>always add up", "Subtotal, tax and grand total, written out in words", "c-sale.jpg")),
    ("phone-3.png", 1080, 1920, phone_page("Share the bill<br>your way", "PDF, WhatsApp, Email or copy the text", "d-share.jpg")),
    ("phone-4.png", 1080, 1920, phone_page("Your logo on<br>every bill", "Add your address, phone and tax number", "g-shop.jpg")),
    ("phone-5.png", 1080, 1920, phone_page("Daily totals<br>at a glance", "Pick any dates and see every day's sales", "e-history.jpg")),
    ("phone-6.png", 1080, 1920, phone_page("Reports in<br>PDF or Excel", "Every sale and item, ready to send or save", "f-sales.jpg")),
    ("feature-graphic.png", 1024, 500, feature_page()),
]

tmp = tempfile.mkdtemp(prefix="gfx_")
for name, w, h, html in JOBS:
    f = os.path.join(HERE, "_tmp_" + name + ".html")
    open(f, "w", encoding="utf-8").write(html)
    out = os.path.join(OUT, name)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--allow-file-access-from-files", f"--user-data-dir={tmp}", f"--window-size={w},{h}",
                    "--virtual-time-budget=4000", f"--screenshot={out}", url(f)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
    os.remove(f)
    print("wrote", out)
