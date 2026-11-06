"""TankPilot schematic sheets drawn as simplified SVG symbols (planning drawings, not an EasyEDA project).
Every reference designator and net name matches tools/data.py. Run via gen_docs.py."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from schem_lib import *   # noqa: F401,F403

C_PRB, C_FLT, C_LDR, C_ULT = "#ec407a", "#00bcd4", "#8bc34a", "#16a34a"
MUTE = "var(--mute)"


def sheet1():
    """Power: DC jack / 5 V terminal / USB-C / optional HLK -> +5V -> 3.3 V LDO."""
    o = []
    j1, p1 = ic(20, 30, 130, 100, "J1", "DC jack 5.5/2.1", [], ["1  tip +", "2  sleeve -"], C_5V, y0=52, step=36)
    j10, p10 = ic(20, 150, 130, 100, "J10", "5 V terminal 2P", [], ["1  +5V", "2  GND"], C_5V, y0=52, step=36)
    o += [j1, j10]
    a, b = p1["1  tip +"], p10["1  +5V"]
    o.append(line([a, (210, a[1])], C_5V) + line([b, (210, b[1])], C_5V) + line([(210, a[1]), (210, b[1])], C_5V)
             + dot(210, a[1], C_5V) + dot(210, b[1], C_5V) + label(218, (a[1] + b[1]) // 2, "DC_IN", C_5V))
    for p in (p1["2  sleeve -"], p10["2  GND"]):
        o.append(line([p, (p[0] + 22, p[1])], C_GND) + gnd(p[0] + 22, p[1]))
    y = a[1]
    o.append(line([(210, y), (250, y)], C_5V) + res(250, y, "F1", "PTC 0.5 A", True, 80, C_5V))
    o.append(line([(330, y), (350, y)], C_5V) + dot(350, y, C_5V) + label(334, y - 12, "DC_F", C_5V))
    o.append(diode(350, y, "D1 TVS", "SMAJ5.0A", False, 60, INK, True) + gnd(350, y + 60))
    o.append(line([(350, y), (400, y)], C_5V) + diode(400, y, "D2", "SS34B", True, 60, C_5V))
    o.append(line([(460, y), (790, y)], C_5V) + label(480, y - 12, "+5V", C_5V))
    RY = y
    # --- USB-C
    j5, p5 = ic(20, 300, 150, 250, "J5 USB-C", "TYPE-C 16P", [], ["VBUS", "GND", "CC1", "CC2", "D+", "D-"], C_USB, y0=54, step=34)
    o.append(j5)
    vb = p5["VBUS"]
    o.append(line([vb, (520, vb[1])], C_USB) + label(vb[0] + 8, vb[1] - 8, "VBUS", C_USB))
    g = p5["GND"]
    o.append(line([g, (g[0] + 20, g[1])], C_GND) + gnd(g[0] + 20, g[1]))
    for nm, rf in (("CC1", "R1"), ("CC2", "R2")):
        c = p5[nm]
        o.append(line([c, (c[0] + 26, c[1])], C_USB) + res(c[0] + 26, c[1], rf + "  5.1k", "", True, 70, C_USB) + line([(c[0] + 96, c[1]), (c[0] + 110, c[1])], C_USB) + gnd(c[0] + 110, c[1]))
    o.append(dot(330, vb[1], C_USB) + cap(330, vb[1], "C7", "100n", False, 36) + gnd(330, vb[1] + 36))
    dp, dn = p5["D+"], p5["D-"]
    u3, p3 = ic(380, dp[1] - 30, 150, 100, "U3", "USBLC6-2SC6", ["I/O1", "I/O2"], ["I/O1 ", "I/O2 "], C_USB, top=["VBUS"], bottom=["GND"], y0=30, step=34)
    o.append(u3)
    o.append(line([p3["VBUS"], (p3["VBUS"][0], vb[1])], C_USB) + dot(p3["VBUS"][0], vb[1], C_USB) + gnd(*p3["GND"]))
    o.append(line([dp, p3["I/O1"]], C_USB) + label(dp[0] + 8, dp[1] - 8, "USB_DP_J", C_USB))
    o.append(line([dn, p3["I/O2"]], C_USB) + label(dn[0] + 8, dn[1] + 16, "USB_DN_J", C_USB))
    o.append(line([(548, dp[1]), (590, dp[1])], C_USB) + label(596, dp[1] + 4, "USB_DP", C_USB))
    o.append(line([(548, dn[1]), (590, dn[1])], C_USB) + label(596, dn[1] + 4, "USB_DN", C_USB))
    o.append(line([(520, vb[1]), (560, vb[1])], C_USB) + diode(560, vb[1], "D3", "SS34B", True, 60, C_USB))
    o.append(line([(620, vb[1]), (680, vb[1]), (680, RY)], C_5V) + dot(680, RY, C_5V))
    # --- rail parts
    o.append(dot(720, RY, C_5V) + cap(720, RY, "C1", "470u", False, 60, INK, True) + gnd(720, RY + 60))
    o.append(dot(780, RY, C_5V) + cap(780, RY, "C5", "100n", False, 60) + gnd(780, RY + 60))
    o.append(line([(790, RY), (870, RY)], C_5V) + dot(840, RY, C_5V) + cap(840, RY, "C2", "10u", False, 60) + gnd(840, RY + 60))
    u2, p2 = ic(890, RY - 50, 150, 110, "U2", "AP2112K-3.3", ["VIN", "EN"], ["VOUT"], C_3V3, bottom=["GND"], y0=50, step=24)
    o.append(u2)
    o.append(line([(870, RY), p2["VIN"]], C_5V) + line([p2["EN"], (870, p2["EN"][1]), (870, RY)], C_5V) + gnd(*p2["GND"]))
    vo = p2["VOUT"]
    o.append(line([vo, (vo[0] + 90, vo[1])], C_3V3) + label(vo[0] + 8, vo[1] - 12, "+3V3", C_3V3) + dot(vo[0] + 50, vo[1], C_3V3)
             + cap(vo[0] + 50, vo[1], "C3", "10u", False, 60) + gnd(vo[0] + 50, vo[1] + 60) + label(vo[0] + 96, vo[1] + 4, "to sheets 2, 3", C_3V3))
    # --- HLK option
    H = 640
    o.append(box(20, H, 1000, 190, "", "", C_AC, "8 6", False) + text(34, H + 20, "OPTIONAL MAINS (230 V, HIGH VOLTAGE): leave all of this off unless an engineer has reviewed it", 12, "start", C_AC, "700"))
    j9, p9 = ic(40, H + 30, 110, 110, "J9", "AC in 2P", [], ["1  L", "2  N"], C_AC, y0=52, step=40)
    o.append(j9)
    ly, ny = p9["1  L"][1], p9["2  N"][1]
    o.append(line([p9["1  L"], (200, ly)], C_AC) + res(200, ly, "F2", "0.5 A slow 5x20", True, 100, C_AC))
    u8, p8 = ic(480, H + 30, 180, 110, "U8 HLK-5M05", "230 V AC to 5 V / 1 A", ["AC/L", "AC/N"], ["+Vo", "-Vo"], C_AC, y0=52, step=40)
    o.append(u8)
    o.append(line([(300, ly), p8["AC/L"]], C_AC) + dot(350, ly, C_AC) + label(306, ly - 12, "AC_LF", C_AC))
    o.append(line([p9["2  N"], p8["AC/N"]], C_N) + dot(350, ny, C_N) + label(166, ny - 8, "AC_N", C_N))
    o.append(res(350, ly, "RV1", "10D561K", False, ny - ly, C_AC))
    vp, vm = p8["+Vo"], p8["-Vo"]
    o.append(line([vp, (790, vp[1])], C_5V) + dot(710, vp[1], C_5V) + label(vp[0] + 6, vp[1] - 12, "+5V_HLK", C_5V))
    o.append(cap(710, vp[1], "C6", "100n", False, vm[1] - vp[1]) + line([vm, (730, vm[1])], C_GND) + dot(710, vm[1], C_GND) + gnd(730, vm[1]))
    o.append(diode(790, vp[1], "D4", "SS34B", True, 60, C_5V))
    o.append(line([(850, vp[1]), (900, vp[1]), (900, H - 10), (680, H - 10), (680, vb[1])], C_5V) + dot(680, vb[1], C_5V) + label(906, vp[1] - 12, "to +5V", C_5V))
    o.append(text(30, H + 215, "Power sources are OR-ed with Schottky diodes (D2 = DC jack / J10, D3 = USB-C, D4 = HLK): the highest one wins, none can back-feed another.", 12, "start", MUTE))
    o.append(text(30, H + 233, "USB_DP / USB_DN go through the ESD part U3 to ESP32-C3 IO19 / IO18 on sheet 2 (native USB, no USB-UART chip).", 12, "start", MUTE))
    return svg(1100, H + 250, "".join(o))


def sheet2():
    """ESP32-C3 core with its support circuits."""
    o = []
    left = ["3V3  p3", "EN  p8", "IO0  p12", "IO1  p13", "IO2  p5", "IO3  p6", "IO4  p18", "IO5  p19", "IO6  p20", "GND  p1"]
    right = ["IO7  p21", "IO8  p22", "IO9  p23", "IO10  p16", "IO18  p26", "IO19  p27", "IO20  p30", "IO21  p31", "GND  p36"]
    u1, p = ic(380, 30, 240, 330, "U1", "ESP32-C3-MINI-1-N4 (PCB antenna on top)", left, right, C_SIG, y0=56, step=28)
    o.append(u1)
    lab = {"IO0  p12": ("LDR", C_LDR), "IO1  p13": ("PROBE_40", C_PRB), "IO2  p5": ("DHT", C_LDR), "IO3  p6": ("PROBE_60", C_PRB),
           "IO4  p18": ("PROBE_COM", C_PRB), "IO5  p19": ("PROBE_80", C_PRB), "IO6  p20": ("PROBE_FULL", C_PRB), "EN  p8": ("EN", C_SIG)}
    for k, (n, c) in lab.items():
        x, y = p[k]
        o.append(line([(x, y), (x - 70, y)], c) + label(x - 76, y + 4, n, c, "end"))
    rl = {"IO7  p21": ("FLOAT1", C_FLT), "IO8  p22": ("LED_ST", C_SIG), "IO9  p23": ("BOOT", C_SIG), "IO10  p16": ("PROBE_20", C_PRB),
          "IO18  p26": ("USB_DN", C_USB), "IO19  p27": ("USB_DP", C_USB), "IO20  p30": ("US_TRIG", C_ULT), "IO21  p31": ("US_ECHO", C_ULT)}
    for k, (n, c) in rl.items():
        x, y = p[k]
        o.append(line([(x, y), (x + 70, y)], c) + label(x + 76, y + 4, n, c))
    x, y = p["3V3  p3"]
    o.append(line([(x, y), (x - 40, y)], C_3V3) + rail(x - 40, y, "+3V3", C_3V3))
    x, y = p["GND  p1"]
    o.append(line([(x, y), (x - 30, y)], C_GND) + gnd(x - 30, y))
    x, y = p["GND  p36"]
    o.append(line([(x, y), (x + 30, y)], C_GND) + gnd(x + 30, y))
    o.append(text(500, 392, "Module pins 1, 2, 11, 14 and the pad pins 36-53 all go to GND.", 11, "middle", MUTE))
    o.append(text(500, 408, "Pins 4, 7, 9, 10, 15, 17, 24, 25, 28, 29, 32-35 are not connected.", 11, "middle", MUTE))
    # --- EN / BOOT
    o.append(box(20, 430, 340, 320, "", "", C_SIG, "8 6", False) + text(34, 450, "EN (reset) and BOOT buttons", 12, "start", C_SIG, "700"))
    o.append(label(34, 546, "EN", C_SIG) + line([(34, 552), (330, 552)], C_SIG))
    o.append(rail(120, 502, "+3V3", C_3V3) + res(120, 502, "R3", "10k", False, 50) + dot(120, 552, C_SIG))
    o.append(dot(190, 552, C_SIG) + cap(190, 552, "C8", "100n", False, 50) + gnd(190, 602))
    o.append(dot(260, 552, C_SIG) + sw(260, 552, "SW1 EN", 50) + gnd(260, 602))
    o.append(label(34, 650, "BOOT", C_SIG) + line([(34, 656), (330, 656)], C_SIG))
    o.append(dot(260, 656, C_SIG) + sw(260, 656, "SW2 BOOT", 50) + gnd(260, 706))
    o.append(text(34, 735, "SW2 pulls GPIO9 low: hold it while plugging USB in", 10.5, "start", MUTE))
    # --- LEDs
    o.append(box(380, 430, 330, 320, "", "", C_SIG, "8 6", False) + text(394, 450, "LEDs", 12, "start", C_SIG, "700"))
    o.append(rail(450, 490, "+3V3", C_3V3) + res(450, 490, "R6", "1k", False, 50) + led(450, 540, "LED1", "red, power", 60, "#dc2626") + gnd(450, 600))
    o.append(label(540, 506, "LED_ST", C_SIG) + line([(540, 512), (580, 512)], C_SIG))
    o.append(res(580, 512, "R7", "1k", False, 50) + led(580, 562, "LED2", "green, status", 60, "#16a34a") + gnd(580, 622))
    o.append(text(394, 660, "LED1 shows the 3.3 V rail;", 10.5, "start", MUTE) + text(394, 676, "LED2 is driven by GPIO8.", 10.5, "start", MUTE))
    # --- decoupling
    o.append(box(730, 430, 340, 140, "", "", C_3V3, "8 6", False) + text(744, 450, "3.3 V decoupling at the module", 12, "start", C_3V3, "700"))
    o.append(line([(750, 490), (1050, 490)], C_3V3) + label(756, 480, "+3V3", C_3V3))
    for x, r, v in ((810, "C4", "10u"), (910, "C9", "100n"), (1000, "C10", "100n")):
        o.append(dot(x, 490, C_3V3) + cap(x, 490, r, v, False, 40) + gnd(x, 530))
    # --- J6
    o.append(box(730, 590, 340, 160, "", "", "#9aa5b5", "8 6", False) + text(744, 610, "J6 expansion header (not fitted by default)", 12, "start", "#64748b", "700"))
    j6, p6 = ic(760, 626, 140, 110, "J6", "1x4 header", [], ["1  +5V", "2  +3V3", "3  GND", "4  IO2"], "#9aa5b5", y0=50, step=15)
    o.append(j6)
    for k, (n, c) in (("1  +5V", ("+5V", C_5V)), ("2  +3V3", ("+3V3", C_3V3)), ("3  GND", ("GND", C_GND)), ("4  IO2", ("DHT (IO2)", C_LDR))):
        x, y = p6[k]
        o.append(line([(x, y), (x + 20, y)], c) + label(x + 26, y + 4, n, c))
    return svg(1100, 770, "".join(o))


def probe_chain(x0, y, ref_s, ref_p, sig):
    o = [line([(x0, y), (x0 + 30, y)], C_PRB) + res(x0 + 30, y, ref_s, "1k", True, 70, C_PRB) + dot(x0 + 100, y, C_PRB)
         + res(x0 + 100, y, ref_p, "470k", False, 36, C_PRB) + gnd(x0 + 100, y + 36)]
    o.append(line([(x0 + 100, y), (x0 + 190, y)], C_PRB) + label(x0 + 196, y + 4, sig, C_PRB))
    return "".join(o)


def sheet3():
    """Sensor ports: ultrasonic, float, probes, LDR, DHT11."""
    o = []
    # ---- ultrasonic
    o.append(box(10, 10, 450, 205, "", "", C_ULT, "8 6", False) + text(24, 30, "ULTRASONIC (J2): JSN-SR04T / HC-SR04", 12, "start", C_ULT, "700"))
    j2, p = ic(30, 44, 130, 150, "J2", "1x4 header", [], ["1  +5V", "2  TRIG", "3  ECHO", "4  GND"], C_ULT, y0=52, step=28)
    o.append(j2)
    x, y = p["1  +5V"]
    o.append(line([(x, y), (x + 30, y)], C_5V) + rail(x + 30, y, "+5V", C_5V))
    x, y = p["2  TRIG"]
    o.append(line([(x, y), (x + 100, y)], C_ULT) + label(x + 106, y + 4, "US_TRIG", C_ULT))
    x, y = p["3  ECHO"]
    o.append(label(x + 6, y - 8, "ECHO_5V", C_ULT) + line([(x, y), (x + 70, y)], C_ULT) + res(x + 70, y, "R15", "1k", True, 70, C_ULT) + dot(x + 140, y, C_ULT)
             + res(x + 140, y, "R16", "2k", False, 36, C_ULT) + gnd(x + 140, y + 36) + line([(x + 140, y), (x + 200, y)], C_ULT) + label(x + 206, y + 4, "US_ECHO", C_ULT))
    x, y = p["4  GND"]
    o.append(line([(x, y), (x + 20, y)], C_GND) + gnd(x + 20, y))
    o.append(rail(400, 50, "+5V", C_5V) + cap(400, 50, "C14", "100n", False, 40) + gnd(400, 90))
    o.append(text(30, 207, "to U1 IO20 (TRIG) and IO21 (ECHO)", 10.5, "start", MUTE))
    # ---- float
    o.append(box(480, 10, 590, 205, "", "", C_FLT, "8 6", False) + text(494, 30, "FLOAT SWITCH (J3): dry contact", 12, "start", C_FLT, "700"))
    j3, p = ic(500, 44, 120, 110, "J3", "float 2P", [], ["1", "2  GND"], C_FLT, y0=52, step=40)
    o.append(j3)
    x, y = p["1"]
    o.append(line([(x, y), (700, y)], C_FLT) + label(x + 8, y - 8, "FLOAT1_T", C_FLT) + dot(700, y, C_FLT))
    o.append(line([(700, y), (700, y + 40)], C_FLT) + box(650, y + 40, 100, 50, "U4", "USBLC6 ESD", C_FLT) + line([(700, y + 90), (700, y + 104)], C_GND) + gnd(700, y + 104))
    o.append(line([(700, y), (730, y)], C_FLT) + res(730, y, "R8", "1k", True, 70, C_FLT) + line([(800, y), (820, y)], C_FLT) + dot(820, y, C_FLT))
    o.append(rail(820, y - 40, "+3V3", C_3V3) + res(820, y - 40, "R4", "10k", False, 40) + cap(820, y, "C12", "100n", False, 40) + gnd(820, y + 40))
    o.append(line([(820, y), (910, y)], C_FLT) + label(916, y + 4, "FLOAT1", C_FLT))
    x, y = p["2  GND"]
    o.append(line([(x, y), (x + 20, y)], C_GND) + gnd(x + 20, y))
    o.append(text(850, 150, "U4: pins 1+6 on FLOAT1_T,", 10.5, "start", MUTE) + text(850, 166, "pin 5 +3V3, pin 2 GND,", 10.5, "start", MUTE) + text(850, 182, "pins 3+4 not used.", 10.5, "start", MUTE))
    o.append(text(916, 124, "to U1 IO7", 10.5, "start", MUTE))
    # ---- probes
    P = 235
    o.append(box(10, P, 1060, 320, "", "", C_PRB, "8 6", False) + text(24, P + 20, "PROBES: COM + 5 levels (J4 and J8). COM is driven with an AC burst through C11. Terminal-side nets are PROBE_xx_T.", 12, "start", C_PRB, "700"))
    j4, p4 = ic(30, P + 36, 130, 215, "J4", "probe 3P", [], ["1  COM", "2  20 %", "3  40 %"], C_PRB, y0=56, step=64)
    o.append(j4)
    x0, y1 = p4["1  COM"]
    o.append(line([(x0, y1), (x0 + 30, y1)], C_PRB) + cap(x0 + 30, y1, "C11", "1u", True, 60, C_PRB) + line([(x0 + 90, y1), (x0 + 190, y1)], C_PRB) + label(x0 + 196, y1 + 4, "PROBE_COM", C_PRB))
    x0, y = p4["2  20 %"]
    o.append(probe_chain(x0, y, "R10", "R17", "PROBE_20"))
    x0, y = p4["3  40 %"]
    o.append(probe_chain(x0, y, "R11", "R18", "PROBE_40"))
    j8, p8 = ic(560, P + 36, 130, 215, "J8", "probe 3P", [], ["1  60 %", "2  80 %", "3  FULL"], C_PRB, y0=56, step=64)
    o.append(j8)
    for k, rs, rp, sig in (("1  60 %", "R12", "R19", "PROBE_60"), ("2  80 %", "R13", "R20", "PROBE_80"), ("3  FULL", "R14", "R21", "PROBE_FULL")):
        x0, y = p8[k]
        o.append(probe_chain(x0, y, rs, rp, sig))
    o.append(text(24, P + 305, "U5, U6, U7 (optional USBLC6): terminal-side nets on pins 1+6 and 3+4 (COM + 20 %, 40 % + 60 %, 80 % + FULL), pin 5 +3V3, pin 2 GND.   Signals go to U1 IO4, IO10, IO1, IO3, IO5, IO6.", 10.5, "start", MUTE))
    # ---- LDR
    L = 575
    o.append(box(10, L, 520, 215, "", "", C_LDR, "8 6", False) + text(24, L + 20, "LDR LIGHT SENSOR (J11) on GPIO0 (ADC)", 12, "start", "#4d7c0f", "700"))
    j11, p = ic(30, L + 40, 120, 110, "J11", "LDR 2P", [], ["1", "2  GND"], C_LDR, y0=52, step=40)
    o.append(j11)
    x, y = p["1"]
    o.append(line([(x, y), (x + 30, y)], C_LDR) + label(x + 4, y - 8, "LDR_T", C_LDR) + res(x + 30, y, "R24", "1k", True, 70, C_LDR) + dot(x + 100, y, C_LDR))
    o.append(rail(x + 100, y - 40, "+3V3", C_3V3) + res(x + 100, y - 40, "R22", "10k", False, 40) + cap(x + 100, y, "C15", "100n", False, 50) + gnd(x + 100, y + 50))
    o.append(line([(x + 100, y), (x + 200, y)], C_LDR) + label(x + 206, y + 4, "LDR", C_LDR))
    x, y = p["2  GND"]
    o.append(line([(x, y), (x + 20, y)], C_GND) + gnd(x + 20, y))
    o.append(text(24, L + 190, "Dark = near 3.3 V, bright = low (invert in firmware). To U1 IO0 (ADC1 channel 0).", 10.5, "start", MUTE))
    # ---- DHT11
    o.append(box(550, L, 520, 215, "", "", C_LDR, "8 6", False) + text(564, L + 20, "DHT11 TEMPERATURE / HUMIDITY (J12) on GPIO2", 12, "start", "#4d7c0f", "700"))
    j12, p = ic(570, L + 40, 130, 130, "J12", "1x3 header", [], ["1  +3V3", "2  DATA", "3  GND"], C_LDR, y0=52, step=30)
    o.append(j12)
    x, y = p["1  +3V3"]
    o.append(line([(x, y), (x + 30, y)], C_3V3) + rail(x + 30, y, "+3V3", C_3V3))
    x, y = p["2  DATA"]
    o.append(label(x + 6, y - 8, "DHT", C_LDR) + line([(x, y), (x + 170, y)], C_LDR) + dot(x + 100, y, C_LDR) + rail(x + 100, y - 50, "+3V3", C_3V3) + res(x + 100, y - 50, "R23", "10k", False, 50) + label(x + 176, y + 4, "DHT", C_LDR))
    x, y = p["3  GND"]
    o.append(line([(x, y), (x + 20, y)], C_GND) + gnd(x + 20, y))
    o.append(text(564, L + 190, "To U1 IO2 (strapping pin, must be high at reset: R23 keeps it high). Check the pin order of your DHT11 board against J12 before ordering.", 10.5, "start", MUTE))
    return svg(1090, L + 235, "".join(o))


SHEETS = {"p1": sheet1, "p2": sheet2, "p3": sheet3}
