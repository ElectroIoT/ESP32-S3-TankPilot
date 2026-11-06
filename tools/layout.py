"""TankPilot PCB placement (planning data). Board 100 x 70 mm, origin lower-left, y up, mm.
ref -> (x_center, y_center, width, height, rotation). Sizes are estimates, NOT EasyEDA footprints.
Every block has a fixed rectangle (its top-silkscreen box); parts must lie inside their own rectangle."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import REF_SEC

BOARD_W, BOARD_H = 94.0, 70.0
SLOT = dict(x=72.4, w=1.3, y0=1.5, y1=67.0)             # isolation slot: mains zone to the right, low voltage to the left
HOLES = [(4.0, 4.0), (4.0, 66.0), (90.0, 66.0)]
R1206 = (4.6, 2.6)
S603 = (2.6, 1.6)
SOT6 = (3.4, 3.2)
L = {}


def put(ref, x, y, w, h, rot=0):
    L[ref] = (x, y, w, h, rot)


def small(ref, x, y, size=R1206):
    put(ref, x, y, size[0], size[1])


# ---- ultrasonic port (top-left)
put("J2", 13.1, 68.7, 10.2, 2.5)
small("R15", 10.5, 63.5)
small("R16", 15.5, 63.5)
small("C14", 10.5, 59.5)
# ---- float ports (top edge)
put("J3", 24.5, 66, 10.2, 8)
small("R8", 22, 58.5)
small("R4", 27, 58.5)
small("C12", 32, 58.5)
put("U4", 33, 55, *SOT6)
# ---- DHT11 header (top edge, where the second float used to be)
put("J12", 39.5, 66, 2.5, 7.6)
put("R23", 39.5, 59.5, 4.6, 2.6, 90)
# ---- extra 5 V terminal and LDR (low-voltage free area right of the MCU)
put("J10", 65.5, 61.2, 10.2, 8)
put("J11", 65.5, 52.2, 10.2, 8)
small("R22", 62.0, 44.4)
small("R24", 67.0, 44.4)
small("C15", 62.0, 41.2)
# ---- 5 V power (left side)
put("J1", 7.5, 43, 14.5, 9)
small("F1", 19, 46)
put("D1", 19, 41, 5.4, 4.4)
put("D2", 26, 46, 5.4, 4.4)
put("D3", 26, 41, 5.4, 4.4)
put("C1", 34, 43, 9, 9)
put("U2", 22, 36.5, 4, 3.4)
small("C2", 27, 36.5)
small("C3", 31.5, 36.5)
small("C5", 36.5, 36.5)
# ---- USB-C
put("J5", 4.5, 28, 9, 7.5)
small("R1", 13, 30)
small("R2", 13, 26)
put("U3", 19, 28, *SOT6)
small("C7", 13, 23.5)
# ---- probe port (bottom edge)
put("J4", 15.6, 4, 15.2, 8)
put("J8", 32, 4, 15.2, 8)
small("C11", 42.5, 6)
for i, ref in enumerate(["R10", "R11", "R12", "R13", "R14"]):
    small(ref, 10.5 + 5.3 * i, 11.2)
for i, ref in enumerate(["R17", "R18", "R19", "R20", "R21"]):
    small(ref, 10.5 + 5.3 * i, 14.8)
# ---- ESP32-C3 core
put("U1", 50.5, 61.2, 13.2, 16.6)
put("SW1", 47, 45, 5.5, 5.5)
put("SW2", 54, 45, 5.5, 5.5)
small("R3", 46.5, 39.5)
small("C8", 51.5, 39.5)
small("C10", 55.2, 31)
small("C4", 46, 35.5)
small("C9", 51, 35.5)
put("LED1", 46, 31, *S603)
small("R6", 50.5, 31)
put("LED2", 46, 28.5, *S603)
small("R7", 50.5, 28.5)
# ---- expansion header
put("J6", 65.0, 68.7, 10.2, 2.5)
# ---- HLK 5 V output parts
put("D4", 49.5, 12, 5.4, 4.4)
small("C6", 49.5, 18)
# ---- HLK 230 V option
put("U8", 74.5, 14.5, 38, 23)
put("F2", 79, 47, 7, 24)
put("RV1", 88, 54, 6, 11)
put("J9", 89.5, 40, 8, 10.2)

# id, title, colour, refs, (x0, y0, x1, y1) silkscreen rectangle
BLOCKS = [
    ("ultra", "ULTRASONIC", "#2fbf71", ["J2", "R15", "R16", "C14"], (7.4, 57.5, 18.8, 70.0)),
    ("floats", "FLOAT SWITCH", "#00bcd4", ["J3", "R8", "R4", "C12", "U4"], (19.4, 53.2, 35.2, 70.0)),
    ("dht", "DHT11", "#8bc34a", ["J12", "R23"], (36.6, 56.9, 42.4, 70.0)),
    ("power", "5 V POWER", "#ff9f43", ["J1", "F1", "D1", "D2", "D3", "C1", "U2", "C2", "C3", "C5"], (0.0, 34.4, 42.0, 51.8)),
    ("usb", "USB-C", "#4895ef", ["J5", "R1", "R2", "U3", "C7"], (0.0, 21.8, 24.0, 33.2)),
    ("probes", "PROBES (COM + 5)", "#ec407a", ["J4", "J8", "C11", "R10", "R11", "R12", "R13", "R14", "R17", "R18", "R19", "R20", "R21"], (7.4, 0.0, 45.5, 21.0)),
    ("mcu", "ESP32-C3", "#a66cff", ["U1", "SW1", "SW2", "R3", "C8", "C10", "C4", "C9", "LED1", "R6", "LED2", "R7"], (43.0, 26.8, 57.8, 69.6)),
    ("exp", "EXPANSION", "#9aa5b5", ["J6"], (59.4, 65.8, 70.6, 70.0)),
    ("hlk_out", "HLK 5V OUT", "#ff7043", ["D4", "C6"], (46.2, 9.0, 52.8, 20.6)),
    ("vin", "5 V IN (TERMINAL)", "#ff9f43", ["J10"], (59.4, 57.0, 71.2, 65.4)),
    ("ldr", "LDR (LIGHT)", "#c0ca33", ["J11", "R22", "R24", "C15"], (59.4, 38.9, 71.2, 56.4)),
    ("hlk", "HLK 230 V (OPTION)", "#ff4d4d", ["U8"], (55.0, 2.6, 93.8, 26.4)),
    ("hlk_ac", "AC IN 230 V (OPTION)", "#ff4d4d", ["F2", "RV1", "J9"], (75.2, 27.0, 93.9, 62.0)),
]
REF_BLOCK = {r: b[0] for b in BLOCKS for r in b[3]}


def rect(v):
    x, y, w, h, r = v
    if r in (90, 270):
        w, h = h, w
    return (x - w / 2, y - h / 2, x + w / 2, y + h / 2)


def box_of(block_id):
    return [b for b in BLOCKS if b[0] == block_id][0][4]


def check():
    prob = []
    rs = {k: rect(v) for k, v in L.items()}
    keys = list(rs)
    edge = {"J1", "J2", "J3", "J4", "J8", "J5", "J6", "J9", "J12"}
    for i in range(len(keys)):
        a = rs[keys[i]]
        inside = a[0] >= 0.5 and a[1] >= 0.5 and a[2] <= BOARD_W - 0.5 and a[3] <= BOARD_H - 0.5
        on_board = a[0] >= -0.01 and a[1] >= -0.01 and a[2] <= BOARD_W + 0.01 and a[3] <= BOARD_H + 0.01
        if not inside and not (keys[i] in edge and on_board):
            prob.append(f"{keys[i]} outside board {tuple(round(t, 1) for t in a)}")
        for j in range(i + 1, len(keys)):
            b = rs[keys[j]]
            ox = min(a[2], b[2]) - max(a[0], b[0])
            oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.2 and oy > 0.2:
                prob.append(f"overlap {keys[i]} / {keys[j]} ({ox:.1f} x {oy:.1f})")
        for (hx, hy) in HOLES:
            cx = min(max(hx, a[0]), a[2])
            cy = min(max(hy, a[1]), a[3])
            if (cx - hx) ** 2 + (cy - hy) ** 2 < 3.4 ** 2:
                prob.append(f"{keys[i]} touches mounting hole at ({hx},{hy})")
    for r in REF_SEC:
        if r not in L and r != "F2H":
            prob.append(f"part {r} has no placement")
    # every part must lie inside its own block rectangle, and in no other
    for ref, a in rs.items():
        own = box_of(REF_BLOCK[ref])
        if a[0] < own[0] - 0.01 or a[1] < own[1] - 0.01 or a[2] > own[2] + 0.01 or a[3] > own[3] + 0.01:
            prob.append(f"part {ref} sticks out of its silkscreen box ({REF_BLOCK[ref]})")
        for b in BLOCKS:
            if b[0] == REF_BLOCK[ref]:
                continue
            bx = b[4]
            ox = min(a[2], bx[2]) - max(a[0], bx[0])
            oy = min(a[3], bx[3]) - max(a[1], bx[1])
            if ox > 0.05 and oy > 0.05:
                prob.append(f"part {ref} lies inside the silkscreen box of {b[0]}")
    ids = [b[0] for b in BLOCKS]
    for i in range(len(ids)):
        bi = box_of(ids[i])
        for (hx, hy) in HOLES:
            cx = min(max(hx, bi[0]), bi[2])
            cy = min(max(hy, bi[1]), bi[3])
            if (cx - hx) ** 2 + (cy - hy) ** 2 < 3.4 ** 2:
                prob.append(f"silkscreen box {ids[i]} touches a mounting hole")
        for j in range(i + 1, len(ids)):
            a, b = bi, box_of(ids[j])
            if min(a[2], b[2]) - max(a[0], b[0]) > -0.3 and min(a[3], b[3]) - max(a[1], b[1]) > -0.3:
                prob.append(f"silkscreen boxes {ids[i]} / {ids[j]} overlap or are closer than 0.3 mm")
    # low-voltage parts keep 3.2 mm from the mains-only parts (F2, RV1, J9)
    for k, a in rs.items():
        if k in ("U8", "F2", "RV1", "J9"):
            continue
        for m in ("F2", "RV1", "J9"):
            b = rs[m]
            dx = max(b[0] - a[2], a[0] - b[2], 0)
            dy = max(b[1] - a[3], a[1] - b[3], 0)
            if (dx * dx + dy * dy) ** 0.5 < 3.2:
                prob.append(f"{k} is closer than 3.2 mm to mains part {m}")
    # antenna keep-out: nothing above U1 up to the board edge
    u = rs["U1"]
    for ref, a in rs.items():
        if ref != "U1" and a[0] < u[2] + 0.5 and a[2] > u[0] - 0.5 and a[3] > u[3] - 0.01:
            prob.append(f"{ref} is inside the antenna keep-out above U1")
    return prob


if __name__ == "__main__":
    pr = check()
    print(len(L), "parts,", len(BLOCKS), "blocks,", len(pr), "problems")
    for p in pr:
        print(" ", p)
