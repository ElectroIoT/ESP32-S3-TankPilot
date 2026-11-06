"""Footprint-style pin guides for TankPilot: U1 ESP32-C3-MINI-1 (top view, pad numbers as in the Espressif data sheet v1.7, figure 3)
and the SOT-23-6 ESD parts USBLC6-2SC6 (U3 and U4). Used by gen_docs.py (schematic page)."""
import html

e = html.escape
INK, MUTE = "var(--ink)", "var(--mute)"
COL = {"gnd": "#475569", "pwr": "#ca8a04", "probe": "#ec407a", "float": "#00bcd4", "ultra": "#16a34a", "sens": "#65a30d",
       "usb": "#8e24aa", "ctl": "#7c3aed", "nc": "#dc2626", "v5": "#ea580c"}
KNAME = {"gnd": "GND", "pwr": "3.3 V", "probe": "probes", "float": "float", "ultra": "ultrasonic", "sens": "LDR / DHT11", "usb": "USB", "ctl": "EN / BOOT / LED", "nc": "not connected"}

# pad -> (pin name, net or None, kind, where it goes)
U1 = {
    1: ("GND", "GND", "gnd", "GND symbol"), 2: ("GND", "GND", "gnd", "GND symbol"), 3: ("3V3", "+3V3", "pwr", "+3V3 rail"),
    4: ("NC", None, "nc", ""), 5: ("IO2", "DHT", "sens", "J12 pin 2, R23 (high at reset)"), 6: ("IO3", "PROBE_60", "probe", "J8.1 via R12, R19"),
    7: ("NC", None, "nc", ""), 8: ("EN", "EN", "ctl", "R3, C8, SW1"), 9: ("NC", None, "nc", ""), 10: ("NC", None, "nc", ""), 11: ("GND", "GND", "gnd", "GND symbol"),
    12: ("IO0", "LDR", "sens", "J11 via R24, R22, C15"), 13: ("IO1", "PROBE_40", "probe", "J4.3 via R11, R18"), 14: ("GND", "GND", "gnd", "GND symbol"), 15: ("NC", None, "nc", ""),
    16: ("IO10", "PROBE_20", "probe", "J4.2 via R10, R17"), 17: ("NC", None, "nc", ""), 18: ("IO4", "PROBE_COM", "probe", "J4.1 via C11"), 19: ("IO5", "PROBE_80", "probe", "J8.2 via R13, R20"),
    20: ("IO6", "PROBE_FULL", "probe", "J8.3 via R14, R21"), 21: ("IO7", "FLOAT1", "float", "J3 via R8, R4, C12"), 22: ("IO8", "LED_ST", "ctl", "R7 to LED2"), 23: ("IO9", "BOOT", "ctl", "SW2 to GND"),
    24: ("NC", None, "nc", ""), 25: ("NC", None, "nc", ""), 26: ("IO18", "USB_DN", "usb", "U3.4 (USB D-)"), 27: ("IO19", "USB_DP", "usb", "U3.6 (USB D+)"), 28: ("NC", None, "nc", ""), 29: ("NC", None, "nc", ""),
    30: ("RXD0 / IO20", "US_ECHO", "ultra", "J2.3 via R15, R16 (ECHO)"), 31: ("TXD0 / IO21", "US_TRIG", "ultra", "J2.2 (TRIG)"),
    32: ("NC", None, "nc", ""), 33: ("NC", None, "nc", ""), 34: ("NC", None, "nc", ""), 35: ("NC", None, "nc", ""),
}
for n in list(range(36, 54)):
    U1[n] = ("GND", "GND", "gnd", "GND symbol")
LEFT = list(range(1, 12))            # top to bottom
BOTTOM = list(range(12, 25))         # left to right
RIGHT = list(range(35, 24, -1))      # top to bottom
TOPROW = [53] + list(range(48, 35, -1)) + [50]    # left to right
BOTROW = [52] + BOTTOM + [51]


def tx(x, y, s, size=11, anchor="start", color=INK, weight="400", rot=None, mono=True):
    fam = ' font-family="Consolas,monospace"' if mono else ""
    tr = f' transform="translate({x},{y}) rotate({rot})"' if rot is not None else f' x="{x}" y="{y}"'
    return f'<text{tr} font-size="{size}" text-anchor="{anchor}" fill="{color}" font-weight="{weight}"{fam}>{e(str(s))}</text>'


def ln(pts, color, w=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(f"{x},{y}" for x, y in pts)}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"{d}/>'


def cross(x, y, c=COL["nc"]):
    return ln([(x - 7, y - 7), (x + 7, y + 7)], c, 3) + ln([(x - 7, y + 7), (x + 7, y - 7)], c, 3)


def gnd_sym(x, y, horiz=None):
    c = COL["gnd"]
    return ln([(x, y), (x, y + 8)], c) + ln([(x - 9, y + 8), (x + 9, y + 8)], c) + ln([(x - 6, y + 12), (x + 6, y + 12)], c) + ln([(x - 3, y + 16), (x + 3, y + 16)], c)


def pad(n, x, y, w=22, h=20, k=None):
    k = k or U1[n][2]
    c = COL[k]
    return (f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="3" fill="{c}" fill-opacity="{".28" if k == "nc" else ".18"}" stroke="{c}" stroke-width="2"/>'
            + tx(x, y + 4, n, 10.5, "middle", c, "700"))


def legend(x=20, y=14):
    o, xx = [], x
    for k in ("gnd", "pwr", "probe", "float", "ultra", "sens", "usb", "ctl"):
        o.append(f'<rect x="{xx}" y="{y}" width="14" height="14" rx="3" fill="{COL[k]}" fill-opacity=".25" stroke="{COL[k]}" stroke-width="2"/>' + tx(xx + 20, y + 11, KNAME[k], 11.5, mono=False))
        xx += 34 + len(KNAME[k]) * 6.6
    o.append(cross(xx + 8, y + 7) + tx(xx + 22, y + 11, "= place a No-Connect flag", 11.5, "start", COL["nc"], "700", mono=False))
    return "".join(o)


def u1_svg():
    x0, x1, y0 = 500, 880, 56
    ant = 70
    ytop = y0 + ant + 24            # top pad row
    yl0, pitch = ytop + 44, 36      # left/right pin 1.. rows
    y1 = yl0 + 10 * pitch + 90      # body bottom
    ybot = y1 - 14
    o = [legend()]
    o.append('<defs><pattern id="ant" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#94a3b8" stroke-width="1.5"/></pattern></defs>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" rx="6" fill="#64748b" fill-opacity=".10" stroke="#475569" stroke-width="2.5"/>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{ant}" fill="url(#ant)" fill-opacity=".25" stroke="#475569" stroke-width="1.5"/>')
    o.append(tx((x0 + x1) / 2, y0 + 30, "PCB ANTENNA (keep-out zone)", 12, "middle", "#334155", "700", mono=False))
    o.append(tx((x0 + x1) / 2, y0 + 50, "no copper, no parts, no pour under or above it", 10.5, "middle", "#334155", "400", mono=False))
    cx = (x0 + x1) / 2
    o.append(tx(cx, yl0 + 70, "U1", 22, "middle", INK, "700", mono=False))
    o.append(tx(cx, yl0 + 94, "ESP32-C3-MINI-1-N4", 13, "middle", INK, "400", mono=False))
    o.append(tx(cx, yl0 + 112, "top view, pad numbers as on the footprint", 10.5, "middle", MUTE, "400", mono=False))
    # EPAD
    ey = yl0 + 150
    o.append(f'<rect x="{cx - 70}" y="{ey}" width="140" height="96" rx="4" fill="{COL["gnd"]}" fill-opacity=".20" stroke="{COL["gnd"]}" stroke-width="2"/>')
    o.append(tx(cx, ey + 40, "49  centre pad", 13, "middle", INK, "700") + tx(cx, ey + 60, "thermal pad: GND", 11, "middle", MUTE))
    # top row (all GND)
    sx = x0 + 18
    for i, n in enumerate(TOPROW):
        o.append(pad(n, sx + i * 25, ytop, 21, 20))
    o.append(tx(cx, ytop + 28, "top pads 36-48 + corner pads 50, 53 = all GND", 10.5, "middle", COL["gnd"], "700", mono=False))
    # left side
    for i, n in enumerate(LEFT):
        y = yl0 + i * pitch
        nm, net, k, where = U1[n]
        c = COL[k]
        o.append(pad(n, x0 + 14, y))
        o.append(tx(x0 + 32, y + 4, nm, 11.5, "start", INK, "700"))
        if k == "nc":
            o.append(ln([(x0 + 2, y), (x0 - 40, y)], c, 2, "3 3") + cross(x0 - 50, y) + tx(x0 - 66, y + 4, "NC flag", 11.5, "end", c, "700", mono=False))
        elif k == "gnd":
            o.append(ln([(x0 + 2, y), (x0 - 28, y)], c, 2) + gnd_sym(x0 - 28, y) + tx(x0 - 44, y + 4, "GND", 11.5, "end", c, "700"))
        elif k == "pwr":
            o.append(ln([(x0 + 2, y), (x0 - 40, y)], c, 2) + tx(x0 - 46, y + 4, "+3V3  rail", 11.5, "end", c, "700"))
        else:
            o.append(ln([(x0 + 2, y), (x0 - 40, y)], c, 2) + tx(x0 - 46, y + 4, f"{net}  >  {where}", 11, "end", INK))
    # right side
    for i, n in enumerate(RIGHT):
        y = yl0 + i * pitch
        nm, net, k, where = U1[n]
        c = COL[k]
        o.append(pad(n, x1 - 14, y))
        o.append(tx(x1 - 32, y + 4, nm, 11.5, "end", INK, "700"))
        if k == "nc":
            o.append(ln([(x1 - 2, y), (x1 + 40, y)], c, 2, "3 3") + cross(x1 + 50, y) + tx(x1 + 66, y + 4, "NC flag", 11.5, "start", c, "700", mono=False))
        else:
            o.append(ln([(x1 - 2, y), (x1 + 40, y)], c, 2) + tx(x1 + 46, y + 4, f"{net}  >  {where}", 11, "start", INK))
    # bottom row
    bx = x0 + 18
    for i, n in enumerate(BOTROW):
        x = bx + i * 25
        if n in (52, 51):
            o.append(pad(n, x, ybot, 21, 20, "gnd"))
            continue
        nm, net, k, where = U1[n]
        c = COL[k]
        o.append(pad(n, x, ybot, 21, 20))
        o.append(tx(x + 4, ybot - 16, nm, 10.5, "start", INK, "700", rot=-90))
        if k == "nc":
            o.append(ln([(x, ybot + 12), (x, y1 + 36)], c, 2, "3 3") + cross(x, y1 + 46) + tx(x + 4, y1 + 62, "NC flag", 11, "start", c, "700", rot=90, mono=False))
        elif k == "gnd":
            o.append(ln([(x, ybot + 12), (x, y1 + 30)], c, 2) + gnd_sym(x, y1 + 30) + tx(x + 4, y1 + 62, "GND", 11, "start", c, "700", rot=90))
        else:
            o.append(ln([(x, ybot + 12), (x, y1 + 40)], c, 2) + tx(x + 4, y1 + 48, f"{net}  >  {where}", 11, "start", INK, rot=90))
    o.append(pad(52, bx, ybot, 21, 20, "gnd") + pad(51, bx + 14 * 25, ybot, 21, 20, "gnd"))
    H = y1 + 420
    return f'<svg viewBox="0 0 1400 {H}" xmlns="http://www.w3.org/2000/svg" role="img" font-family="Segoe UI,Roboto,Arial,sans-serif">' + "".join(o) + "</svg>"


def u1_table():
    rows = []
    sig = [n for n in sorted(U1) if U1[n][2] not in ("nc", "gnd")]
    for n in sig:
        nm, net, k, where = U1[n]
        side = "left" if n <= 11 else ("bottom" if n <= 24 else "right")
        act = "wire to the +3V3 power symbol" if k == "pwr" else f"put net label <b>{e(net)}</b> on the pin, then wire / label to {e(where)}"
        rows.append(f'<tr><td><b>{n}</b></td><td>{side}</td><td class="mpn">{e(nm)}</td><td><span style="color:{COL[k]};font-weight:700">{e(net)}</span></td><td>{act}</td></tr>')
    gn = [n for n in sorted(U1) if U1[n][2] == "gnd"]
    nc = [n for n in sorted(U1) if U1[n][2] == "nc"]
    rows.append(f'<tr><td><b>1, 2, 11, 14, 36-53</b></td><td>left, bottom, top, corners, centre</td><td class="mpn">GND</td><td><span style="color:{COL["gnd"]};font-weight:700">GND</span></td><td>one GND power symbol on <b>every</b> GND pin ({len(gn)} pins; pins 49-53 are the thermal / corner pads, in the symbol they may be merged into one pin: still connect it)</td></tr>')
    rows.append(f'<tr style="background:#dc262615"><td><b>{", ".join(str(n) for n in nc)}</b></td><td>all sides</td><td class="mpn">NC</td><td><span style="color:{COL["nc"]};font-weight:700">no connect</span></td><td><b>place a No-Connect flag (X) on each of these {len(nc)} pins</b>; do not connect anything to them</td></tr>')
    return '<div class="scroll"><table><thead><tr><th>Pin</th><th>Side</th><th>Name</th><th>Net</th><th>What to do in EasyEDA</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"


# ------------------------------------------------------------------ USBLC6-2SC6 (SOT-23-6)
ESD = [
    ("U3", "USB data lines", {1: ("USB_DP_J", "from J5 (USB-C D+)"), 2: ("GND", ""), 3: ("USB_DN_J", "from J5 (USB-C D-)"), 4: ("USB_DN", "to U1 pin 26 (IO18)"), 5: ("VBUS", "from J5 / VBUS net"), 6: ("USB_DP", "to U1 pin 27 (IO19)")},
     "The data line goes IN on pin 1 and OUT on pin 6 (D+), IN on pin 3 and OUT on pin 4 (D-). Do not join pin 1 to pin 6 with a wire: the two pins are joined inside the chip."),
    ("U4", "float switch J3", {1: ("FLOAT1_T", "terminal net (before R8)"), 2: ("GND", ""), 3: (None, ""), 4: (None, ""), 5: ("+3V3", ""), 6: ("FLOAT1_T", "same net as pin 1")},
     "Used only as a clamp: pins 1 and 6 on the same net. The second channel (pins 3, 4) is not used: No-Connect flags."),
]
NETKIND = {"GND": "gnd", "+3V3": "pwr", "VBUS": "usb"}


def _kind_of(net):
    if net is None:
        return "nc"
    if net in NETKIND:
        return NETKIND[net]
    if net.startswith("USB"):
        return "usb"
    if net.startswith("PROBE"):
        return "probe"
    return "float"


def esd_svg(ref, title, pins):
    W, Hh = 560, 200
    o = [tx(10, 18, f"{ref}  USBLC6-2SC6  (SOT-23-6, top view): {title}", 12.5, "start", INK, "700", mono=False)]
    bx0, bx1, by0, by1 = 215, 345, 40, 170
    o.append(f'<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" height="{by1 - by0}" rx="8" fill="#64748b" fill-opacity=".10" stroke="#475569" stroke-width="2.5"/>')
    o.append(f'<circle cx="{bx0 + 14}" cy="{by0 + 14}" r="4" fill="#475569"/>')
    o.append(tx((bx0 + bx1) / 2, 112, ref, 18, "middle", INK, "700", mono=False))
    left = [(1, 66), (2, 105), (3, 144)]
    right = [(6, 66), (5, 105), (4, 144)]
    for side, lst in (("l", left), ("r", right)):
        for n, y in lst:
            net, note = pins[n]
            k = _kind_of(net)
            c = COL[k]
            xp = bx0 - 12 if side == "l" else bx1 + 12
            o.append(pad(n, xp, y, 24, 22, k))
            nmn = {1: "I/O1", 2: "GND", 3: "I/O2", 4: "I/O2", 5: "VBUS", 6: "I/O1"}[n]
            o.append(tx(bx0 + 10 if side == "l" else bx1 - 10, y + 4, nmn, 11, "start" if side == "l" else "end", INK, "700"))
            if net is None:
                if side == "l":
                    o.append(ln([(xp - 14, y), (xp - 44, y)], c, 2, "3 3") + cross(xp - 54, y) + tx(xp - 68, y + 4, "NC flag", 11.5, "end", c, "700", mono=False))
                else:
                    o.append(ln([(xp + 14, y), (xp + 44, y)], c, 2, "3 3") + cross(xp + 54, y) + tx(xp + 68, y + 4, "NC flag", 11.5, "start", c, "700", mono=False))
            elif net == "GND":
                if side == "l":
                    o.append(ln([(xp - 14, y), (xp - 40, y)], c, 2) + gnd_sym(xp - 40, y) + tx(xp - 62, y + 4, "GND", 11.5, "end", c, "700"))
                else:
                    o.append(ln([(xp + 14, y), (xp + 40, y)], c, 2) + gnd_sym(xp + 40, y) + tx(xp + 62, y + 4, "GND", 11.5, "start", c, "700"))
            else:
                if side == "l":
                    o.append(ln([(xp - 14, y), (xp - 40, y)], c, 2) + tx(xp - 46, y - 2, net, 11.5, "end", c, "700") + tx(xp - 46, y + 12, note, 9.5, "end", MUTE, "400", mono=False))
                else:
                    o.append(ln([(xp + 14, y), (xp + 40, y)], c, 2) + tx(xp + 46, y - 2, net, 11.5, "start", c, "700") + tx(xp + 46, y + 12, note, 9.5, "start", MUTE, "400", mono=False))
    return f'<svg viewBox="0 0 {W} {Hh}" xmlns="http://www.w3.org/2000/svg" role="img" font-family="Segoe UI,Roboto,Arial,sans-serif">' + "".join(o) + "</svg>"


def esd_html():
    o = ['<p class="mut">SOT-23-6 has <b>3 pins on each side</b>. Top view: pins 1, 2, 3 run down the <b>left</b> side, pins 4, 5, 6 run up the <b>right</b> side (pin 6 top right, pin 4 bottom right); the dot marks pin 1. '
         'Pin meaning (data sheet): <b>1 = I/O1, 2 = GND, 3 = I/O2, 4 = I/O2, 5 = VBUS (supply side), 6 = I/O1</b>. Pins 1 and 6 are the same channel (joined inside), and so are pins 3 and 4.</p>']
    for ref, title, pins, note in ESD:
        o.append(f'<div class="scroll">{esd_svg(ref, title, pins)}</div><p class="mut">{e(note)}</p>')
    return "".join(o)


# ------------------------------------------------------------------ symbol view (as the EasyEDA / LCSC symbol of C2838502)
SYM_TODO = {30, 31}   # not wired yet in the user's drawing (screenshot 2026-11-06)


def u1_symbol_svg():
    x0, x1, y0, pitch = 540, 790, 60, 25
    rows_l = list(range(1, 27))
    rows_r = list(range(53, 26, -1))
    H = y0 + 27 * pitch + 50
    o = [legend()]
    o.append(f'<rect x="{x0}" y="{y0 - 14}" width="{x1 - x0}" height="{27 * pitch + 22}" fill="#fffbe6" fill-opacity=".55" stroke="#9a1c1c" stroke-width="2.5"/>')
    o.append(tx((x0 + x1) / 2, y0 - 20, "U1  ESP32-C3-MINI-1-N4", 12, "middle", "#9a1c1c", "700", mono=False))
    for side, rows in (("l", rows_l), ("r", rows_r)):
        for i, n in enumerate(rows):
            y = y0 + i * pitch + 8
            nm, net, k, where = U1[n]
            c = COL[k]
            if side == "l":
                xa, xb = x0 - 34, x0
                o.append(ln([(xa, y), (xb, y)], "#9a1c1c", 2) + tx(xb - 6, y - 3, n, 9.5, "end", "#9a1c1c") + tx(xb + 6, y + 4, nm, 11, "start", INK, "700"))
                ex = xa
                if k == "nc":
                    o.append(ln([(ex, y), (ex - 18, y)], c, 2, "3 3") + cross(ex - 26, y) + tx(ex - 40, y + 4, "NC flag", 11, "end", c, "700", mono=False))
                elif k == "gnd":
                    o.append(ln([(ex, y), (ex - 14, y)], c, 2) + tx(ex - 20, y + 4, "GND", 11, "end", c, "700"))
                else:
                    lab = "+3V3" if k == "pwr" else net
                    o.append(ln([(ex, y), (ex - 14, y)], c, 2) + tx(ex - 20, y + 4, lab, 12, "end", c, "700") + tx(ex - 20 - 7.4 * len(lab) - 14, y + 4, "TODO" if n in SYM_TODO else "ok", 9, "end", "#ea580c" if n in SYM_TODO else "#16a34a", "700", mono=False))
            else:
                xa, xb = x1 + 34, x1
                o.append(ln([(xb, y), (xa, y)], "#9a1c1c", 2) + tx(xb + 6, y - 3, n, 9.5, "start", "#9a1c1c") + tx(xb - 6, y + 4, nm, 11, "end", INK, "700"))
                ex = xa
                if k == "nc":
                    o.append(ln([(ex, y), (ex + 18, y)], c, 2, "3 3") + cross(ex + 26, y) + tx(ex + 40, y + 4, "NC flag", 11, "start", c, "700", mono=False))
                elif k == "gnd":
                    o.append(ln([(ex, y), (ex + 14, y)], c, 2) + tx(ex + 20, y + 4, "GND", 11, "start", c, "700"))
                else:
                    o.append(ln([(ex, y), (ex + 14, y)], c, 2) + tx(ex + 20, y + 4, net, 12, "start", c, "700") + tx(ex + 20 + 7.4 * len(net) + 8, y + 4, ("TODO: " if n in SYM_TODO else "ok: ") + where, 9.5, "start", "#ea580c" if n in SYM_TODO else MUTE, "700" if n in SYM_TODO else "400", mono=False))
    return f'<svg viewBox="0 0 1340 {H}" xmlns="http://www.w3.org/2000/svg" role="img" font-family="Segoe UI,Roboto,Arial,sans-serif">' + "".join(o) + "</svg>"
