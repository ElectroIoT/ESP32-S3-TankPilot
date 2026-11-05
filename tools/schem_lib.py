"""Tiny SVG schematic helpers (adapted from the HexRelay project tools; no external deps)."""
import html
import re


C_AC, C_N, C_GND, C_5V, C_3V3, C_SIG, C_USB, C_REL = (
    "#dc2626", "#2563eb", "#475569", "#ea580c", "#ca8a04", "#7c3aed", "#059669", "#92400e")
INK = "var(--ink)"


def esc(s):
    return html.escape(str(s))


def line(pts, color=INK, w=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(f"{x},{y}" for x, y in pts)
    return f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linejoin="round"{d}/>'


def dot(x, y, color=INK):
    return f'<circle cx="{x}" cy="{y}" r="3.5" fill="{color}"/>'


def text(x, y, s, size=12, anchor="start", color=INK, weight="400", mono=False):
    fam = ' font-family="Consolas,monospace"' if mono else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" fill="{color}" '
            f'font-weight="{weight}"{fam}>{esc(s)}</text>')


def label(x, y, s, color=INK, anchor="start"):
    """Net label."""
    return text(x, y, s, 12, anchor, color, "700", True)


def gnd(x, y, color=C_GND):
    return (line([(x, y), (x, y + 8)], color) + line([(x - 9, y + 8), (x + 9, y + 8)], color)
            + line([(x - 6, y + 12), (x + 6, y + 12)], color) + line([(x - 3, y + 16), (x + 3, y + 16)], color))


def rail(x, y, name, color=C_5V):
    return line([(x, y), (x, y - 8)], color) + line([(x - 9, y - 8), (x + 9, y - 8)], color) + label(x, y - 13, name, color, "middle")


def res(x, y, ref, val, h=False, L=40, color=INK):
    if h:
        a, b = x + L / 2 - 14, x + L / 2 + 14
        return (line([(x, y), (a, y)], color) + line([(b, y), (x + L, y)], color)
                + f'<rect x="{a}" y="{y-5}" width="28" height="10" fill="none" stroke="{color}" stroke-width="2"/>'
                + text(x + L / 2, y - 10, ref, 11, "middle", INK, "700") + text(x + L / 2, y + 20, val, 10.5, "middle", "var(--mute)"))
    a, b = y + L / 2 - 14, y + L / 2 + 14
    return (line([(x, y), (x, a)], color) + line([(x, b), (x, y + L)], color)
            + f'<rect x="{x-5}" y="{a}" width="10" height="28" fill="none" stroke="{color}" stroke-width="2"/>'
            + text(x + 10, y + L / 2 - 2, ref, 11, "start", INK, "700") + text(x + 10, y + L / 2 + 11, val, 10.5, "start", "var(--mute)"))


def cap(x, y, ref, val, h=False, L=40, color=INK, polar=False):
    if h:
        m = x + L / 2
        return (line([(x, y), (m - 3, y)], color) + line([(m + 3, y), (x + L, y)], color)
                + line([(m - 3, y - 9), (m - 3, y + 9)], color) + line([(m + 3, y - 9), (m + 3, y + 9)], color)
                + text(m, y - 13, ref, 11, "middle", INK, "700") + text(m, y + 24, val, 10.5, "middle", "var(--mute)"))
    m = y + L / 2
    s = (line([(x, y), (x, m - 3)], color) + line([(x, m + 3), (x, y + L)], color)
         + line([(x - 9, m - 3), (x + 9, m - 3)], color) + line([(x - 9, m + 3), (x + 9, m + 3)], color)
         + text(x + 14, m - 2, ref, 11, "start", INK, "700") + text(x + 14, m + 11, val, 10.5, "start", "var(--mute)"))
    if polar:
        s += text(x - 14, m - 6, "+", 12, "end", INK, "700")
    return s


def diode(x, y, ref, val, h=False, L=40, color=INK, flip=False):
    """Anode at the start, cathode at the end (flip swaps)."""
    if h:
        m = x + L / 2
        d = 1 if not flip else -1
        tri = f"{m-8*d},{y-8} {m-8*d},{y+8} {m+8*d},{y}"
        bar = line([(m + 8 * d, y - 8), (m + 8 * d, y + 8)], color)
        return (line([(x, y), (x + L, y)], color) + f'<polygon points="{tri}" fill="none" stroke="{color}" stroke-width="2"/>' + bar
                + text(m, y - 13, ref, 11, "middle", INK, "700") + text(m, y + 26, val, 10.5, "middle", "var(--mute)"))
    m = y + L / 2
    d = 1 if not flip else -1
    tri = f"{x-8},{m-8*d} {x+8},{m-8*d} {x},{m+8*d}"
    bar = line([(x - 8, m + 8 * d), (x + 8, m + 8 * d)], color)
    return (line([(x, y), (x, y + L)], color) + f'<polygon points="{tri}" fill="none" stroke="{color}" stroke-width="2"/>' + bar
            + text(x + 14, m - 2, ref, 11, "start", INK, "700") + text(x + 14, m + 11, val, 10.5, "start", "var(--mute)"))


def led(x, y, ref, val, L=40, color="#16a34a"):
    m = y + L / 2
    return (diode(x, y, ref, val, L=L, color=color)
            + line([(x + 10, m - 8), (x + 18, m - 16)], color) + line([(x + 14, m - 4), (x + 22, m - 12)], color))


def sw(x, y, ref, L=40):
    return (line([(x, y), (x, y + 12)]) + line([(x, y + L - 12), (x, y + L)])
            + dot(x, y + 12) + dot(x, y + L - 12) + line([(x - 10, y + 10), (x + 10, y + 12)], w=2)
            + text(x + 14, y + L / 2 + 4, ref, 11, "start", INK, "700"))


def nmos(x, y, ref, val):
    """gate pin (x,y); drain pin (x+40,y-30); source pin (x+40,y+30)."""
    g = x + 16
    c = x + 22
    return (line([(x, y), (g, y)]) + line([(g, y - 13), (g, y + 13)])
            + line([(c, y - 14), (c, y - 8)]) + line([(c, y - 4), (c, y + 4)]) + line([(c, y + 8), (c, y + 14)])
            + line([(c, y - 11), (x + 40, y - 11), (x + 40, y - 30)]) + line([(c, y + 11), (x + 40, y + 11), (x + 40, y + 30)])
            + line([(c, y), (x + 34, y), (x + 34, y + 11)])
            + text(x + 50, y - 2, ref, 11, "start", INK, "700") + text(x + 50, y + 11, val, 10.5, "start", "var(--mute)"))


def box(x, y, w, h, title, sub="", color="#2563eb", dash=None, fill=True):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    f = f'fill="{color}" fill-opacity="0.10"' if fill else 'fill="none"'
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" {f} stroke="{color}" stroke-width="2"{d}/>'
    if title:
        s += text(x + w / 2, y + 18, title, 13, "middle", INK, "700")
    if sub:
        s += text(x + w / 2, y + 33, sub, 10.5, "middle", "var(--mute)")
    return s


def ic(x, y, w, h, title, sub, left, right, color="#2563eb", top=None, bottom=None, step=22, y0=54):
    """IC box; left/right = list of pin labels (None = gap). Returns (svg, pins dict name -> (x,y))."""
    s = box(x, y, w, h, title, sub, color)
    pins = {}
    for side, lst in (("l", left), ("r", right)):
        for i, name in enumerate(lst):
            if name is None:
                continue
            py = y + y0 + i * step
            px = x if side == "l" else x + w
            ex = px - 18 if side == "l" else px + 18
            s += line([(px, py), (ex, py)], C_GND if name.startswith("GND") else INK, 2)
            s += text(px + (8 if side == "l" else -8), py + 4, name, 10.5, "start" if side == "l" else "end", INK, "400", True)
            pins[name] = (ex, py)
    for side, lst in (("t", top or []), ("b", bottom or [])):
        for i, name in enumerate(lst):
            px = x + 30 + i * 40
            py = y if side == "t" else y + h
            ey = py - 16 if side == "t" else py + 16
            s += line([(px, py), (px, ey)], C_GND if name.startswith("GND") else INK, 2)
            s += text(px, py + (14 if side == "t" else -6), name, 10.5, "middle", INK, "400", True)
            pins[name] = (px, ey)
    return s, pins


def svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'font-family="Segoe UI,Roboto,Arial,sans-serif">{body}</svg>')


