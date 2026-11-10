"""Generate the animated SVGs used in README.md (SMIL animation, no scripts: GitHub shows them inside <img>).
    python -X utf8 tools/gen_svgs.py"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "images")
FONT = "Segoe UI,Roboto,Helvetica,Arial,sans-serif"


def hero():
    W, H = 1280, 440
    D = 12.0                       # cycle length in seconds
    y_low, y_high = 309.0, 80.0    # water surface y at 15 % and 100 %
    t_up, t_top, t_fall0, t_fall1 = 0.0, 6.6, 7.8, 11.4   # seconds: start, reaches top, starts falling, empty
    tips = {"20": 296, "40": 242, "60": 188, "80": 134, "FULL": 108}

    def t_rise(yt):
        return t_up + (y_low - yt) / (y_low - y_high) * (t_top - t_up)

    def t_down(yt):
        return t_fall0 + (yt - y_high) / (y_low - y_high) * (t_fall1 - t_fall0)

    kt = lambda *v: ";".join(f"{x / D:.4f}" for x in v)
    wy_vals = f"{y_low};{y_high};{y_high};{y_low};{y_low}"
    wy_kt = kt(0, t_top, t_fall0, t_fall1, D)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="TankPilot animated banner: water level rising in a tank with ultrasonic and probe sensors">']
    s.append('<defs>'
             '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#031b34"/><stop offset=".5" stop-color="#0a4a7a"/><stop offset="1" stop-color="#0891b2"/></linearGradient>'
             '<linearGradient id="wt" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#67e8f9"/><stop offset="1" stop-color="#0284c7"/></linearGradient>'
             '<clipPath id="tk"><rect x="872" y="80" width="236" height="270" rx="20"/></clipPath>'
             '<clipPath id="lid"><rect x="880" y="62" width="220" height="300"/></clipPath>'
             '<radialGradient id="gl" cx=".7" cy=".4" r=".6"><stop offset="0" stop-color="#7ee8ff" stop-opacity=".35"/><stop offset="1" stop-color="#7ee8ff" stop-opacity="0"/></radialGradient>'
             '</defs>')
    s.append(f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="28" fill="url(#gl)"/>')
    # background waves (drift)
    for i, (op, dy, dur) in enumerate(((.10, 0, 9), (.07, 18, 13))):
        s.append(f'<g opacity="{op * 2}"><path d="M-200 {360 + dy} q150 -40 300 0 t300 0 t300 0 t300 0 t300 0 t300 0 V{H} H-200Z" fill="#fff">'
                 f'<animateTransform attributeName="transform" type="translate" values="0 0;-300 0" dur="{dur}s" repeatCount="indefinite"/></path></g>')
    # title block
    s.append(f'<text x="64" y="150" font-family="{FONT}" font-size="104" font-weight="800" fill="#fff">Tank<tspan fill="#7deaff">Pilot</tspan></text>')
    s.append(f'<text x="68" y="206" font-family="{FONT}" font-size="31" fill="#e6f6ff">Know your tank level in %.</text>')
    s.append(f'<text x="68" y="248" font-family="{FONT}" font-size="31" fill="#e6f6ff">Let Home Assistant start the pump.</text>')
    x = 68
    for label, w, fill in (("ESP32-C3", 150, ".16"), ("ESPHome", 140, ".16"), ("Home Assistant", 210, ".16"), ("Ultrasonic", 150, ".26"), ("5 probes", 130, ".26"), ("Float", 90, ".26")):
        row = 290 if label in ("ESP32-C3", "ESPHome", "Home Assistant") else 340
        if label == "Ultrasonic":
            x = 68
        s.append(f'<rect x="{x}" y="{row}" width="{w}" height="40" rx="20" fill="#fff" fill-opacity="{fill}" stroke="#fff" stroke-opacity=".5"/>'
                 f'<text x="{x + w / 2}" y="{row + 27}" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#fff">{label}</text>')
        x += w + 12
        if label == "Home Assistant":
            x = 68
    s.append(f'<text x="68" y="410" font-family="{FONT}" font-size="21" fill="#cfeaf7">Open-source water tank level node  |  94 x 70 mm  |  IP67 box ready</text>')
    # pump status (visible while the level is low and rising)
    s.append(f'<g font-family="{FONT}" font-weight="800" font-size="22"><rect x="640" y="300" width="190" height="44" rx="22" fill="#16a34a" fill-opacity=".9">'
             f'<animate attributeName="opacity" values="1;0.35;1;0.35;1;0;0;1;1" keyTimes="{kt(0, 1.6, 3.2, 4.8, t_rise(tips["FULL"]) - .2, t_rise(tips["FULL"]), t_down(80), t_fall1 - .6, D)}" dur="{D}s" repeatCount="indefinite"/></rect>'
             f'<text x="735" y="330" text-anchor="middle" fill="#fff">PUMP ON</text></g>')
    s.append(f'<g font-family="{FONT}" font-weight="800" font-size="22"><rect x="640" y="300" width="190" height="44" rx="22" fill="#475569" fill-opacity=".9" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{kt(0, t_rise(tips["FULL"]), t_rise(tips["FULL"]) + .01, t_down(80), t_down(80) + .01)}" dur="{D}s" repeatCount="indefinite"/></rect>'
             f'<text x="735" y="330" text-anchor="middle" fill="#fff" opacity="0">PUMP OFF<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{kt(0, t_rise(tips["FULL"]), t_rise(tips["FULL"]) + .01, t_down(80), t_down(80) + .01)}" dur="{D}s" repeatCount="indefinite"/></text></g>')
    # wifi arcs from tank to the left (pulse)
    for i, r in enumerate((26, 44, 62)):
        s.append(f'<path d="M{805 - r} {232 - r * .72} A{r} {r} 0 0 0 {805 - r} {232 + r * .72}" fill="none" stroke="#7deaff" stroke-width="5" stroke-linecap="round" opacity="0">'
                 f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;.4;1" dur="2.2s" begin="{i * .3}s" repeatCount="indefinite"/></path>')
    s.append('<circle cx="812" cy="232" r="7" fill="#7deaff"><animate attributeName="r" values="6;9;6" dur="2.2s" repeatCount="indefinite"/></circle>')
    # tank body
    s.append('<rect x="870" y="78" width="240" height="274" rx="22" fill="#fff" fill-opacity=".10" stroke="#fff" stroke-opacity=".85" stroke-width="5"/>')
    tv = ";".join("0 " + v for v in wy_vals.split(";"))
    s.append(f'<g clip-path="url(#tk)"><g><animateTransform attributeName="transform" type="translate" values="{tv}" keyTimes="{wy_kt}" dur="{D}s" repeatCount="indefinite"/>')
    s.append('<g><animateTransform attributeName="transform" type="translate" values="0 0;-80 0" dur="2.4s" repeatCount="indefinite"/>'
             '<path d="M800 0 q20 -14 40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 t40 0 V320 H800Z" fill="url(#wt)" opacity=".95"/></g></g></g>')
    # lid + ultrasonic sensor
    s.append('<rect x="858" y="52" width="264" height="30" rx="15" fill="#fff" fill-opacity=".35" stroke="#fff" stroke-width="4"/>')
    s.append('<rect x="960" y="34" width="60" height="30" rx="8" fill="#fff"/><circle cx="978" cy="49" r="8" fill="#0891b2"/><circle cx="1002" cy="49" r="8" fill="#0891b2"/>')
    s.append('<g clip-path="url(#lid)">')
    for i in range(3):
        s.append(f'<circle cx="990" cy="66" r="10" fill="none" stroke="#fde68a" stroke-width="3" opacity="0"><animate attributeName="r" values="10;120" dur="2.4s" begin="{i * .8}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.9;0" dur="2.4s" begin="{i * .8}s" repeatCount="indefinite"/></circle>')
    s.append('</g>')
    # probes (rods + indicators)
    rods = [("COM", 1096, 340), ("20", 1072, 296), ("40", 1048, 242), ("60", 1024, 188), ("80", 1000, 134), ("FULL", 976, 108)]
    for name, rx, tip in rods:
        s.append(f'<line x1="{rx}" y1="82" x2="{rx}" y2="{tip}" stroke="#e2e8f0" stroke-width="5" stroke-linecap="round"/>')
        if name == "COM":
            s.append(f'<circle cx="{rx}" cy="{tip}" r="7" fill="#fde68a"/>')
        else:
            tr, tf = t_rise(tip), t_down(tip)
            s.append(f'<circle cx="{rx}" cy="{tip}" r="8" fill="#475569"><animate attributeName="fill" values="#475569;#4ade80;#475569;#475569" keyTimes="{kt(0, tr, tf, D)}" calcMode="discrete" dur="{D}s" repeatCount="indefinite"/></circle>')
    # level readout inside the tank (label of highest wet probe)
    order = ["20", "40", "60", "80", "FULL"]
    for k, name in enumerate(order):
        tip = tips[name]
        a, b = t_rise(tip), (t_rise(tips[order[k + 1]]) if k < 4 else None)
        if k < 4:
            c, dd = t_down(tips[order[k + 1]]), t_down(tip)
            vals, kts = "0;1;0;1;0;0", kt(0, a, b, c, dd, D)
        else:
            vals, kts = "0;1;0;0", kt(0, a, t_down(tip), D)
        label = "FULL" if name == "FULL" else f"{name} %"
        s.append(f'<text x="918" y="226" text-anchor="middle" font-family="{FONT}" font-size="44" font-weight="800" fill="#fff" stroke="#0a4a7a" stroke-width="2" paint-order="stroke" opacity="0">{label}'
                 f'<animate attributeName="opacity" values="{vals}" keyTimes="{kts}" calcMode="discrete" dur="{D}s" repeatCount="indefinite"/></text>')
    s.append(f'<text x="918" y="392" text-anchor="middle" font-family="{FONT}" font-size="18" fill="#cfeaf7">ultrasonic + 5 probes + float</text>')
    s.append("</svg>")
    return "".join(s)


def flow():
    W, H = 1280, 300
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="TankPilot data flow: sensors, ESP32-C3 board, Wi-Fi, Home Assistant, pump">']
    s.append('<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#031b34"/><stop offset="1" stop-color="#0a4a7a"/></linearGradient>'
             '<marker id="ar" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#7deaff"/></marker></defs>')
    s.append(f'<rect width="{W}" height="{H}" rx="26" fill="url(#bg)"/>')
    nodes = [("Tank sensors", "ultrasonic / probes / float"), ("TankPilot board", "ESP32-C3 picks the best source"), ("Wi-Fi + ESPHome", "level %, source, health"),
             ("Home Assistant", "your limits, automation"), ("Pump", "start below 20 %, stop at full")]
    bw, gap = 200, 55
    x0 = (W - (5 * bw + 4 * gap)) / 2
    cy = 130
    for i, (hd, sub) in enumerate(nodes):
        x = x0 + i * (bw + gap)
        s.append(f'<rect x="{x}" y="50" width="{bw}" height="170" rx="22" fill="#fff" fill-opacity=".10" stroke="#fff" stroke-opacity=".55" stroke-width="2"/>')
        icx = x + bw / 2
        # icons
        if i == 0:      # tank with rising water
            s.append(f'<rect x="{icx - 24}" y="72" width="48" height="52" rx="8" fill="none" stroke="#fff" stroke-width="3"/>'
                     f'<rect x="{icx - 21}" y="100" width="42" height="21" rx="5" fill="#38bdf8"><animate attributeName="y" values="112;92;112" dur="4s" repeatCount="indefinite"/><animate attributeName="height" values="9;29;9" dur="4s" repeatCount="indefinite"/></rect>')
        elif i == 1:    # chip
            s.append(f'<rect x="{icx - 22}" y="76" width="44" height="44" rx="6" fill="none" stroke="#fff" stroke-width="3"/>'
                     + "".join(f'<line x1="{icx + d}" y1="68" x2="{icx + d}" y2="76" stroke="#fff" stroke-width="3"/><line x1="{icx + d}" y1="120" x2="{icx + d}" y2="128" stroke="#fff" stroke-width="3"/>' for d in (-12, 0, 12))
                     + f'<circle cx="{icx}" cy="98" r="6" fill="#7deaff"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>')
        elif i == 2:    # wifi
            for k, r in enumerate((14, 25, 36)):
                s.append(f'<path d="M{icx - r} {124 - r * .6} A{r} {r} 0 0 1 {icx + r} {124 - r * .6}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".3"><animate attributeName="opacity" values=".25;1;.25" dur="1.8s" begin="{k * .25}s" repeatCount="indefinite"/></path>')
            s.append(f'<circle cx="{icx}" cy="126" r="5" fill="#fff"/>')
        elif i == 3:    # house
            s.append(f'<path d="M{icx - 30} 100 L{icx} 72 L{icx + 30} 100" fill="none" stroke="#fff" stroke-width="4" stroke-linejoin="round"/><rect x="{icx - 22}" y="100" width="44" height="26" fill="none" stroke="#fff" stroke-width="4"/><rect x="{icx - 6}" y="110" width="12" height="16" fill="#7deaff"/>')
        else:           # pump
            s.append(f'<circle cx="{icx}" cy="98" r="26" fill="none" stroke="#fff" stroke-width="4"/>'
                     f'<g><animateTransform attributeName="transform" type="rotate" values="0 {icx} 98;360 {icx} 98" dur="2s" repeatCount="indefinite"/><line x1="{icx - 14}" y1="98" x2="{icx + 14}" y2="98" stroke="#7deaff" stroke-width="5"/><line x1="{icx}" y1="84" x2="{icx}" y2="112" stroke="#7deaff" stroke-width="5"/></g>'
                     f'<rect x="{icx + 24}" y="90" width="22" height="16" fill="none" stroke="#fff" stroke-width="3"/>')
        s.append(f'<text x="{icx}" y="168" text-anchor="middle" font-family="{FONT}" font-size="22" font-weight="800" fill="#fff">{hd}</text>')
        s.append(f'<text x="{icx}" y="196" text-anchor="middle" font-family="{FONT}" font-size="15" fill="#cfeaf7">{sub}</text>')
        if i < 4:
            ax = x + bw + 6
            s.append(f'<line x1="{ax}" y1="{cy}" x2="{ax + gap - 14}" y2="{cy}" stroke="#7deaff" stroke-width="5" stroke-dasharray="10 8" marker-end="url(#ar)"><animate attributeName="stroke-dashoffset" values="36;0" dur="1.2s" repeatCount="indefinite"/></line>')
            s.append(f'<circle r="6" fill="#fde68a"><animateMotion dur="1.8s" begin="{i * .45}s" repeatCount="indefinite" path="M{ax} {cy} L{ax + gap - 14} {cy}"/></circle>')
    s.append(f'<text x="{W / 2}" y="268" text-anchor="middle" font-family="{FONT}" font-size="19" fill="#e6f6ff">If one sensor fails, TankPilot falls back to the next one and reports which source it is using.</text>')
    s.append("</svg>")
    return "".join(s)


if __name__ == "__main__":
    for name, fn in (("tankpilot-hero-animated.svg", hero), ("tankpilot-flow-animated.svg", flow)):
        p = os.path.join(OUT, name)
        open(p, "w", encoding="utf-8").write(fn())
        print(name, os.path.getsize(p))
