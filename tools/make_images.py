"""Make the social / blog image pack for TankPilot from the EasyEDA 3D screenshots in docs/images/renders.
    python -X utf8 tools/make_images.py
Writes PNG files to docs/images/social/."""
import os, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RN = os.path.join(ROOT, "docs", "images", "renders")
OUT = os.path.join(ROOT, "docs", "images", "social")
os.makedirs(OUT, exist_ok=True)
FD = "C:/Windows/Fonts/"
NAVY, BLUE, CYAN, WHITE = (3, 27, 52), (10, 74, 122), (8, 145, 178), (255, 255, 255)


def font(size, bold=False, light=False):
    return ImageFont.truetype(FD + ("segoeuib.ttf" if bold else "segoeuil.ttf" if light else "segoeui.ttf"), size)


def gradient(w, h, stops, angle=135):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(angle)
    t = (xx * math.cos(a) + yy * math.sin(a))
    t = (t - t.min()) / (t.max() - t.min())
    out = np.zeros((h, w, 3), np.float32)
    n = len(stops) - 1
    for i in range(n):
        m = (t >= i / n) & (t <= (i + 1) / n + 1e-6)
        u = ((t - i / n) * n)[m][:, None]
        out[m] = np.array(stops[i], np.float32) * (1 - u) + np.array(stops[i + 1], np.float32) * u
    return Image.fromarray(out.astype(np.uint8)).convert("RGBA")


def bg(w, h, waves=True):
    im = gradient(w, h, [NAVY, BLUE, CYAN], 120)
    d = ImageDraw.Draw(im, "RGBA")
    for i in range(4 if waves else 0):  # soft waves
        y0 = int(h * (0.93 + 0.022 * i))
        pts = [(x, y0 + 14 * math.sin((x / w) * 6.28 * 2 + i)) for x in range(0, w + 8, 8)]
        d.line(pts, fill=(255, 255, 255, 30), width=3)
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).ellipse((w * 0.45, h * 0.1, w * 1.05, h * 0.9), fill=(120, 230, 255, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(min(w, h) // 6))
    return Image.alpha_composite(im, glow).convert("RGB")


def render(name, crop, scale=1.7):
    im = Image.open(os.path.join(RN, name)).convert("RGB").crop(crop)
    a = np.asarray(im).astype(np.int16)
    lum = a.max(axis=2)
    alpha = np.clip((lum - 8) * 30, 0, 255).astype(np.uint8)
    rgba = Image.fromarray(np.dstack([a.astype(np.uint8), alpha]), "RGBA")
    m = np.asarray(rgba.getchannel("A")) > 40
    cols = np.where(m.sum(0) > 8)[0]
    rows = np.where(m.sum(1) > 8)[0]
    rgba = rgba.crop((int(cols[0]), int(rows[0]), int(cols[-1]) + 1, int(rows[-1]) + 1))
    rgba = rgba.resize((int(rgba.width * scale), int(rgba.height * scale)), Image.LANCZOS)
    return rgba.filter(ImageFilter.UnsharpMask(radius=1.6, percent=90, threshold=2))


ISO = render("blue_iso.jpg", (157, 55, 1225, 520))
TOP = render("blue_top.jpg", (157, 55, 1225, 520))
BOT = render("blue_bottom.jpg", (157, 55, 1225, 520))


def paste_shadow(base, im, xy, glow=True):
    x, y = xy
    if glow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        m = im.getchannel("A").point(lambda v: 110 if v > 20 else 0)
        blk = Image.new("RGBA", im.size, (0, 20, 40, 255))
        blk.putalpha(m)
        sh.paste(blk, (x + 14, y + 26), blk)
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        base.paste(sh, (0, 0), sh)
    base.paste(im, (x, y), im)


def fit(im, w=None, h=None):
    r = min((w or 1e9) / im.width, (h or 1e9) / im.height)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)


def text(d, xy, s, f, fill=WHITE, anchor="la", shadow=True):
    x, y = xy
    if shadow:
        d.text((x + 2, y + 3), s, font=f, fill=(0, 15, 30, 120), anchor=anchor)
    d.text(xy, s, font=f, fill=fill, anchor=anchor)


def title(d, x, y, size, anchor="la"):
    f = font(size, True)
    w1 = d.textlength("Tank", font=f)
    w2 = d.textlength("Pilot", font=f)
    if anchor == "ma":
        x = x - (w1 + w2) / 2
    text(d, (x, y), "Tank", f, WHITE)
    text(d, (x + w1, y), "Pilot", f, (125, 235, 255))


def chip(d, x, y, s, f, fill=(255, 255, 255, 40), outline=(255, 255, 255, 110), pad=14):
    w = d.textlength(s, font=f) + pad * 2
    h = f.size + 14
    d.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=fill, outline=outline, width=2)
    d.text((x + pad, y + h / 2), s, font=f, fill=WHITE, anchor="lm")
    return w


def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


# ---------------- glyph icons (drawn, no emoji) ----------------
def g_wave(d, x, y, s, c=WHITE):
    d.polygon([(x - s * .3, y + s * .3), (x + s * .3, y + s * .3), (x + s * .2, y + s * .5), (x - s * .2, y + s * .5)], fill=c)
    for i, r in enumerate((.35, .6, .85)):
        d.arc((x - s * r, y - s * r + s * .1, x + s * r, y + s * r + s * .1), 215, 325, fill=c, width=max(3, int(s * .07)))


def g_probe(d, x, y, s, c=WHITE):
    for i, hh in enumerate((.9, .75, .6, .45, .3)):
        xx = x - s * .5 + i * s * .25
        d.line((xx, y - s * .5, xx, y - s * .5 + s * hh), fill=c, width=max(3, int(s * .08)))
    d.line((x - s * .6, y - s * .5, x + s * .6, y - s * .5), fill=c, width=max(4, int(s * .1)))


def g_float(d, x, y, s, c=WHITE):
    d.line((x, y - s * .5, x, y - s * .05), fill=c, width=max(3, int(s * .07)))
    d.ellipse((x - s * .3, y - s * .1, x + s * .3, y + s * .5), outline=c, width=max(4, int(s * .08)))
    d.line((x - s * .2, y + s * .2, x + s * .2, y + s * .2), fill=c, width=max(3, int(s * .06)))


def g_wifi(d, x, y, s, c=WHITE):
    for r in (.25, .5, .75):
        d.arc((x - s * r, y + s * .2 - s * r, x + s * r, y + s * .2 + s * r), 225, 315, fill=c, width=max(4, int(s * .08)))
    d.ellipse((x - s * .07, y + s * .15, x + s * .07, y + s * .29), fill=c)


def g_bolt(d, x, y, s, c=WHITE):
    d.polygon([(x + s * .1, y - s * .55), (x - s * .3, y + s * .1), (x - s * .02, y + s * .1), (x - s * .12, y + s * .55), (x + s * .32, y - s * .12), (x + s * .04, y - s * .12)], fill=c)


def g_shield(d, x, y, s, c=WHITE):
    d.polygon([(x - s * .4, y - s * .45), (x + s * .4, y - s * .45), (x + s * .4, y + s * .05), (x, y + s * .55), (x - s * .4, y + s * .05)], outline=c, width=max(4, int(s * .08)))
    d.line((x - s * .18, y, x - s * .03, y + s * .15, x + s * .22, y - s * .2), fill=c, width=max(4, int(s * .08)))


def g_chip(d, x, y, s, c=WHITE):
    d.rectangle((x - s * .3, y - s * .3, x + s * .3, y + s * .3), outline=c, width=max(4, int(s * .08)))
    for i in (-.15, 0, .15):
        d.line((x + i * s * 1.2, y - s * .5, x + i * s * 1.2, y - s * .3), fill=c, width=3)
        d.line((x + i * s * 1.2, y + s * .3, x + i * s * 1.2, y + s * .5), fill=c, width=3)
        d.line((x - s * .5, y + i * s * 1.2, x - s * .3, y + i * s * 1.2), fill=c, width=3)
        d.line((x + s * .3, y + i * s * 1.2, x + s * .5, y + i * s * 1.2), fill=c, width=3)


def g_home(d, x, y, s, c=WHITE):
    d.polygon([(x - s * .5, y), (x, y - s * .45), (x + s * .5, y)], outline=c, width=max(4, int(s * .08)))
    d.rectangle((x - s * .35, y, x + s * .35, y + s * .45), outline=c, width=max(4, int(s * .08)))
    d.rectangle((x - s * .1, y + s * .15, x + s * .1, y + s * .45), fill=c)


def g_pump(d, x, y, s, c=WHITE):
    d.ellipse((x - s * .4, y - s * .4, x + s * .4, y + s * .4), outline=c, width=max(4, int(s * .08)))
    d.rectangle((x + s * .3, y - s * .12, x + s * .65, y + s * .12), outline=c, width=max(3, int(s * .06)))
    d.line((x - s * .15, y - s * .15, x + s * .15, y + s * .15), fill=c, width=max(4, int(s * .08)))
    d.line((x + s * .15, y - s * .15, x - s * .15, y + s * .15), fill=c, width=max(4, int(s * .08)))


def g_light(d, x, y, s, c=WHITE):
    d.ellipse((x - s * .22, y - s * .22, x + s * .22, y + s * .22), outline=c, width=max(4, int(s * .08)))
    for k in range(8):
        a = k * math.pi / 4
        d.line((x + math.cos(a) * s * .35, y + math.sin(a) * s * .35, x + math.cos(a) * s * .5, y + math.sin(a) * s * .5), fill=c, width=max(3, int(s * .06)))


def g_box(d, x, y, s, c=WHITE):
    d.rounded_rectangle((x - s * .5, y - s * .35, x + s * .5, y + s * .35), radius=int(s * .1), outline=c, width=max(4, int(s * .08)))
    d.line((x - s * .5, y - s * .15, x + s * .5, y - s * .15), fill=c, width=max(3, int(s * .06)))


def g_tank(d, x, y, s, level=.55, c=WHITE):
    d.rounded_rectangle((x - s * .45, y - s * .5, x + s * .45, y + s * .5), radius=int(s * .15), outline=c, width=max(4, int(s * .07)))
    ytop = y + s * .5 - s * level
    d.rounded_rectangle((x - s * .4, ytop, x + s * .4, y + s * .45), radius=int(s * .1), fill=(56, 189, 248, 230))
    d.line((x - s * .5, y - s * .5, x + s * .5, y - s * .5), fill=c, width=max(5, int(s * .1)))


GL = {"wave": g_wave, "probe": g_probe, "float": g_float, "wifi": g_wifi, "bolt": g_bolt, "shield": g_shield, "chip": g_chip,
      "home": g_home, "pump": g_pump, "light": g_light, "box": g_box, "tank": g_tank}


def icon_badge(im, x, y, r, glyph, col=(255, 255, 255, 38)):
    d = ImageDraw.Draw(im, "RGBA")
    d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=(255, 255, 255, 120), width=2)
    GL[glyph](d, x, y, r * 1.1)


def card(im, box, glyph, head, body, hf=30, bf=21):
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = box
    d.rounded_rectangle(box, radius=26, fill=(255, 255, 255, 30), outline=(255, 255, 255, 90), width=2)
    icon_badge(im, x0 + 52, y0 + 56, 34, glyph)
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (x0 + 104, y0 + 38), head, font(hf, True), shadow=False)
    yy = y0 + 100
    for ln in wrap(d, body, font(bf), x1 - x0 - 44):
        d.text((x0 + 24, yy), ln, font=font(bf), fill=(225, 240, 250, 235))
        yy += bf + 7


def save(im, name):
    p = os.path.join(OUT, name)
    im.convert("RGB").save(p, optimize=True)
    print(name, im.size)


# ---------------- 1. hero / Open Graph 1200x630 ----------------
def hero():
    w, h = 1200, 630
    im = bg(w, h)
    r = fit(ISO, w=760, h=560)
    paste_shadow(im, r, (w - r.width - 10, (h - r.height) // 2 + 10))
    d = ImageDraw.Draw(im, "RGBA")
    chip(d, 60, 70, "OPEN-SOURCE IoT HARDWARE", font(20, True))
    title(d, 56, 112, 112)
    for i, ln in enumerate(("Know your tank level in %.", "Let Home Assistant start the pump.")):
        text(d, (62, 262 + i * 42), ln, font(32))
    x = 62
    for s in ("ESP32-C3", "ESPHome", "Home Assistant"):
        x += chip(d, x, 372, s, font(22, True)) + 12
    x = 62
    for s in ("Ultrasonic", "5 Probes", "Float"):
        x += chip(d, x, 428, s, font(22, True), fill=(125, 235, 255, 60)) + 12
    text(d, (62, 540), "94 x 70 mm  |  IP67 box ready  |  from ~$6 in parts", font(24, light=False), (200, 235, 250))
    save(im, "01_hero_og_1200x630.png")


# ---------------- 2. square 1080 ----------------
def square():
    w = h = 1080
    im = bg(w, h)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, w / 2, 56, 130, "ma")
    text(d, (w / 2, 215), "Smart water tank level node", font(38), anchor="ma")
    r = fit(ISO, w=900, h=560)
    paste_shadow(im, r, ((w - r.width) // 2, 320))
    d = ImageDraw.Draw(im, "RGBA")
    xs = [("ESP32-C3", 0), ("ESPHome", 0), ("Home Assistant", 0)]
    total = sum(d.textlength(s, font=font(26, True)) + 28 + 14 for s, _ in xs) - 14
    x = (w - total) / 2
    for s, _ in xs:
        x += chip(d, x, 930, s, font(26, True)) + 14
    text(d, (w / 2, 1010), "Ultrasonic  +  5-probe  +  Float  |  automatic fallback", font(26), (200, 235, 250), anchor="ma")
    save(im, "02_square_1080x1080.png")


# ---------------- 3. story 1080x1920 ----------------
def story():
    w, h = 1080, 1920
    im = bg(w, h)
    d = ImageDraw.Draw(im, "RGBA")
    chip(d, 70, 90, "OPEN-SOURCE IoT HARDWARE", font(26, True))
    title(d, 64, 150, 170)
    for i, ln in enumerate(("Your tank level in %,", "your pump on autopilot.")):
        text(d, (70, 360 + i * 56), ln, font(44))
    r = fit(ISO, w=980)
    paste_shadow(im, r, ((w - r.width) // 2, 520))
    items = [("wave", "Ultrasonic level", "smooth 0-100 %"), ("probe", "5 stainless probes", "20 / 40 / 60 / 80 / FULL"),
             ("wifi", "ESPHome + Home Assistant", "Wi-Fi, encrypted API, OTA"), ("pump", "Auto pump start", "below your limit, stop at full")]
    y = 1000
    for g, hd, sub in items:
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle((70, y, w - 70, y + 150), radius=30, fill=(255, 255, 255, 34), outline=(255, 255, 255, 90), width=2)
        icon_badge(im, 150, y + 75, 42, g)
        d = ImageDraw.Draw(im, "RGBA")
        text(d, (222, y + 30), hd, font(40, True), shadow=False)
        d.text((222, y + 88), sub, font=font(30), fill=(210, 235, 248, 240))
        y += 176
    d = ImageDraw.Draw(im, "RGBA")
    d.rounded_rectangle((70, 1740, w - 70, 1850), radius=55, fill=(255, 255, 255, 255))
    d.text((w / 2, 1795), "94 x 70 mm  |  IP67 box ready  |  ~$6 parts", font=font(40, True), fill=(7, 59, 92), anchor="mm")
    save(im, "03_story_1080x1920.png")


# ---------------- 4. features infographic ----------------
def features():
    w, h = 1080, 1660
    im = bg(w, h, False)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, w / 2, 40, 110, "ma")
    text(d, (w / 2, 175), "12 reasons to build it", font(38), anchor="ma")
    cards = [("wave", "Ultrasonic level", "JSN-SR04T / HC-SR04 header with a safe 3.3 V echo divider."),
             ("probe", "5-level probes", "COM + 5 stainless probes, driven with AC so they do not corrode."),
             ("float", "Float input", "Dry contact with pull-up, filter and ESD protection."),
             ("shield", "Auto fallback", "Ultrasonic fails? Probes take over. Then the float."),
             ("wifi", "Home Assistant", "ESPHome over Wi-Fi: level %, source, health flags, OTA."),
             ("pump", "Auto pump start", "Starts below your limit, stops at full, never on stale data."),
             ("light", "Light + climate", "LDR light sensor and DHT11 temperature / humidity."),
             ("bolt", "3 power options", "5 V jack or terminal, USB-C, or optional 230 V module."),
             ("chip", "Native USB-C", "Flash and log over USB. No USB-UART chip needed."),
             ("shield", "Protected", "PTC fuse, TVS, Schottky OR-ing, USB and float ESD."),
             ("box", "IP67 ready", "94 x 70 mm board for a 120 x 80 x 55 mm clear box."),
             ("home", "Open and hackable", "Spare GPIO header, status LEDs and full design docs.")]
    cw, ch, gx, gy = 470, 232, 30, 22
    for i, (g, hd, bd) in enumerate(cards):
        c, r = i % 2, i // 2
        x0 = 50 + c * (cw + gx)
        y0 = 240 + r * (ch + gy)
        card(im, (x0, y0, x0 + cw, y0 + ch), g, hd, bd, 30, 22)
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (w / 2, 1600), "ESP32-C3  |  ESPHome  |  Home Assistant", font(30, True), (200, 235, 250), anchor="ma")
    save(im, "04_features_infographic_1080x1660.png")


# ---------------- 5. how it works ----------------
def how():
    w, h = 1600, 900
    im = bg(w, h)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, w / 2, 36, 96, "ma")
    text(d, (w / 2, 150), "How it works", font(40), anchor="ma")
    nodes = [("tank", "Tank + sensors", "ultrasonic, probes, float"), ("board", "TankPilot board", "ESP32-C3 picks the best source"),
             ("wifi", "Wi-Fi + ESPHome", "level %, source, health"), ("home", "Home Assistant", "your limits and automation"),
             ("pump", "Pump", "start below 20 %, stop at full")]
    n = len(nodes)
    bw, gap = 250, 60
    x0 = (w - (n * bw + (n - 1) * gap)) // 2
    y0, bh = 300, 380
    for i, (g, hd, sub) in enumerate(nodes):
        x = x0 + i * (bw + gap)
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle((x, y0, x + bw, y0 + bh), radius=30, fill=(255, 255, 255, 34), outline=(255, 255, 255, 100), width=2)
        if g == "board":
            r = fit(ISO, w=bw - 30)
            paste_shadow(im, r, (x + 15, y0 + 50), glow=False)
        else:
            icon_badge(im, x + bw // 2, y0 + 120, 66, g if g != "tank" else "tank")
        d = ImageDraw.Draw(im, "RGBA")
        text(d, (x + bw / 2, y0 + 232), hd, font(27, True), anchor="ma", shadow=False)
        for k, ln in enumerate(wrap(d, sub, font(21), bw - 30)):
            d.text((x + bw / 2, y0 + 280 + k * 28), ln, font=font(21), fill=(215, 238, 250, 240), anchor="ma")
        if i < n - 1:
            ax = x + bw + 8
            ay = y0 + bh // 2
            d.line((ax, ay, ax + gap - 16, ay), fill=(125, 235, 255, 255), width=6)
            d.polygon([(ax + gap - 16, ay - 14), (ax + gap - 16, ay + 14), (ax + gap + 2, ay)], fill=(125, 235, 255, 255))
    text(d, (w / 2, 770), "If one sensor fails, TankPilot switches to the next and tells you which source it uses.", font(30), (210, 238, 250), anchor="ma")
    save(im, "05_how_it_works_1600x900.png")


# ---------------- 6. sensor options ----------------
def sensors():
    w, h = 1600, 900
    im = bg(w, h)
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (w / 2, 40), "Three sensors, one board", font(70, True), anchor="ma")
    text(d, (w / 2, 134), "Use what you have. Add the others later.", font(34), (210, 238, 250), anchor="ma")
    cols = [("wave", "Ultrasonic", "JSN-SR04T on the tank lid", ["Smooth 0-100 % level", "Nice trends and bars", "Blind zone about 25 cm", "Steam / foam can fool it"]),
            ("probe", "5-level probes", "Stainless rods, COM + levels", ["Rugged, cheap, reliable", "Great for auto-start level", "Steps: 20 / 40 / 60 / 80 / FULL", "Clean the rods now and then"]),
            ("float", "Float switch", "Dry contact on a 2-wire cable", ["Simple full / low alarm", "Works with any float", "Last-resort backup", "One level only"])]
    cw, gap = 470, 40
    x0 = (w - (3 * cw + 2 * gap)) // 2
    for i, (g, hd, sub, pts) in enumerate(cols):
        x = x0 + i * (cw + gap)
        y = 230
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle((x, y, x + cw, y + 580), radius=34, fill=(255, 255, 255, 34), outline=(255, 255, 255, 100), width=2)
        icon_badge(im, x + cw // 2, y + 95, 62, g)
        d = ImageDraw.Draw(im, "RGBA")
        text(d, (x + cw / 2, y + 180), hd, font(40, True), anchor="ma", shadow=False)
        d.text((x + cw / 2, y + 236), sub, font=font(23), fill=(205, 232, 248, 240), anchor="ma")
        for k, p in enumerate(pts):
            yy = y + 300 + k * 64
            good = k < 2
            d.ellipse((x + 34, yy + 6, x + 62, yy + 34), fill=(74, 222, 128, 255) if good else (251, 191, 36, 255))
            d.text((x + 80, yy + 20), p, font=font(26), fill=WHITE, anchor="lm")
    save(im, "06_sensor_options_1600x900.png")


# ---------------- 7. spec card ----------------
def specs():
    w, h = 1200, 1200
    im = bg(w, h, False)
    d = ImageDraw.Draw(im, "RGBA")
    title(d, 60, 40, 96)
    text(d, (64, 160), "Specification", font(36), (200, 235, 250))
    r = fit(TOP, w=640, h=330)
    paste_shadow(im, r, (w - r.width - 50, 40))
    rows = [("MCU", "ESP32-C3-MINI-1-N4, Wi-Fi + BLE"), ("Firmware", "ESPHome, encrypted API, OTA"), ("Sensors", "Ultrasonic, 5 probes, float, LDR, DHT11"),
            ("Power", "5 V jack / terminal, USB-C, optional HLK-5M05"), ("Protection", "PTC fuse, TVS, ESD, Schottky OR-ing"),
            ("Board", "94 x 70 mm, 2 layers, 1.6 mm"), ("Enclosure", "120 x 80 x 55 mm IP67 clear box"), ("Parts", "65 parts, about $6.19 (5 V) / $9.84 (230 V option)"),
            ("Status", "Schematic, layout and routing done")]
    y = 410
    for k, v in rows:
        d = ImageDraw.Draw(im, "RGBA")
        d.rounded_rectangle((60, y, w - 60, y + 66), radius=18, fill=(255, 255, 255, 30), outline=(255, 255, 255, 70), width=1)
        text(d, (90, y + 15), k, font(30, True), (125, 235, 255), shadow=False)
        d.text((330, y + 15), v, font=font(29), fill=WHITE)
        y += 74
    save(im, "07_specs_card_1200x1200.png")


# ---------------- 8-10 clean renders ----------------
def clean(name, src, w, h, label):
    im = bg(w, h, False)
    r = fit(src, w=int(w * .9), h=int(h * .8))
    paste_shadow(im, r, ((w - r.width) // 2, (h - r.height) // 2 - 10))
    d = ImageDraw.Draw(im, "RGBA")
    text(d, (40, h - 62), "TankPilot", font(34, True))
    d.text((w - 40, h - 52), label, font=font(26), fill=(210, 238, 250), anchor="ra")
    save(im, name)


if __name__ == "__main__":
    hero(); square(); story(); features(); how(); sensors(); specs()
    clean("08_board_3d_angle_1600x900.png", ISO, 1600, 900, "ESP32-C3 water tank level node, 3D view")
    clean("09_board_3d_top_1600x900.png", TOP, 1600, 900, "Top side, 94 x 70 mm")
    clean("10_board_3d_bottom_1600x900.png", BOT, 1600, 900, "Bottom side")
