"""TankPilot (ESP32-C3 water tank sensor node) design data: sections, parts, pin-to-net data, BOM info.
All connections are PLANNED (no schematic exists yet). Pin names follow the planned symbols; check them in EasyEDA."""

# id, title, colour, description
SECTIONS = [
 ("power", "5 V POWER (DC jack, USB, 3.3 V)", "#ff9f43", "5 V from the DC jack J1 or the 2-pin screw terminal J10 (both through the PTC fuse + TVS), or USB-C, or the optional HLK module, OR-ed with Schottky diodes, then an AP2112K 3.3 V LDO."),
 ("hlk", "HLK 230 V -> 5 V (OPTIONAL)", "#ff4d4d", "Optional mains supply: AC in terminal, fuse, varistor and the HLK-5M05 module. Leave all of these parts off if you power the board from a 5 V adapter."),
 ("usb", "USB-C PROGRAMMING", "#4895ef", "C165948 USB-C, native USB on GPIO18 / GPIO19, 5.1 k CC resistors, ESD part."),
 ("mcu", "ESP32-C3 CORE", "#a66cff", "ESP32-C3-MINI-1-N4 module, EN / BOOT buttons, status LEDs, decoupling, expansion header."),
 ("ultra", "ULTRASONIC PORT", "#2fbf71", "J2 header for JSN-SR04T / HC-SR04: +5V, TRIG, ECHO (5 V to 3.3 V divider), GND."),
 ("floats", "FLOAT SWITCH PORTS", "#00bcd4", "J3: one dry-contact float switch input, with pull-up, series resistor, filter capacitor and ESD (the second float input was dropped to free a GPIO for the DHT11)."),
 ("sens", "EXTRA SENSORS (LDR light, DHT11)", "#8bc34a", "J11 2-pin terminal for an LDR (light sensor) with a 10 k divider into the ADC pin GPIO0, and J12 3-pin header for a DHT11 temperature / humidity sensor on GPIO2 (strapping pin, must be high at reset: the DHT11 idles high with its 10 k pull-up) ."),
 ("probes", "PROBE PORT (COM + 5 LEVELS)", "#ec407a", "J4 + J8: COM (AC-coupled drive) and five level probes 20 / 40 / 60 / 80 / FULL, each with a series resistor and a pull-down."),
]
SEC = {s[0]: s for s in SECTIONS}

# page groups of the schematic guide: id, title, [sections]
PAGES = [
 ("p1", "Sheet 1: Power (DC jack, 5 V terminal, USB-C, HLK option)", ["power", "hlk", "usb"]),
 ("p2", "Sheet 2: ESP32-C3 core", ["mcu"]),
 ("p3", "Sheet 3: Sensor ports (ultrasonic, float, probes, LDR, DHT11)", ["ultra", "floats", "probes", "sens"]),
]

# BOM info by LCSC number: mpn, maker, stock, unit price, tier, status
INFO = {
 "C2838502": ("ESP32-C3-MINI-1-N4", "Espressif", 15184, 3.0672, "1+", "LISTING 2026-11-05; datasheet v1.7 pin table read"),
 "C51118": ("AP2112K-3.3TRG1", "Diodes Inc", 4510, 0.1792, "5+", "LISTING (stock from 2026-10-28)"),
 "C7519": ("USBLC6-2SC6", "ST", 39325, 0.1814, "5+", "LISTING (stock from 2026-10-28)"),
 "C136744": ("DC-005-20A", "Korean Hroparts", 24115, 0.1398, "5+", "LISTING 2026-11-05; 2.0 mm centre pin variant, 2.1 mm plugs fit: check"),
 "C165948": ("TYPE-C-31-M-12", "Korean Hroparts", 283620, 0.1886, "5+", "VERIFIED 2026-10-28 (same as BorePilot)"),
 "C163512": ("1206L050YR", "Littelfuse", 11040, 0.0742, "10+", "LISTING 2026-11-05; alt ASMD1206-050 C135338"),
 "C5121739": ("SMAJ5.0A", "Prosemi", 1750, 0.1056, "20+", "LISTING 2026-11-05 (other suppliers); cheaper alt C2991090 at 280+"),
 "C2758511": ("UMW SS34B", "UMW", 77840, 0.0378, "20+", "LISTING (same as BorePilot)"),
 "C492402": ("PZ254V-11-03P", "XFCN", "not read", 0.02, "20+", "LISTING 2026-11-05 (1x3 header; stock and price not shown on the page, price estimated from the 4P part)"),
 "C2691448": ("PZ254V-11-04P", "XFCN", 591680, 0.0264, "20+", "LISTING (stock from 2026-10-28)"),
 "C474952": ("KF128-5.08-2P-AA", "Cixi Kefa", 51090, 0.1944, "5+", "LISTING; rating not read"),
 "C474953": ("KF128-5.08-3P-AA", "Cixi Kefa", 8510, 0.3251, "5+", "LISTING (stock from 2026-10-28); no 6P part on LCSC"),
 "C318884": ("TS-1187A-B-A-B", "XKB", 887660, 0.0208, "20+", "LISTING (stock from 2026-10-28)"),
 "C965798": ("XL-1608SURC-04", "Xinglight", 270700, 0.0057, "100+", "LISTING (red, inferred from name)"),
 "C2986059": ("19-217/GHC-YR1S2/6T", "Everlight", 718400, 0.018, "50+", "LISTING (green, inferred from name)"),
 "C47344174": ("ERG16V470M8X12", "JIERR", 64670, 0.0579, "10+", "LISTING"),
 "C9807": ("CL31A106KAHNNNE", "Samsung", 493250, 0.053, "10+", "VERIFIED listing 2026-10-28"),
 "C24497": ("CL31B104KBCNNNC", "Samsung", 125980, 0.0222, "20+", "VERIFIED listing 2026-10-28"),
 "C1848": ("CL31B105KBHNNNE", "Samsung", 147470, 0.0628, "10+", "LISTING 2026-11-05"),
 "C26033": ("1206W4F5101T5E", "Uni-Royal", 166000, 0.005, "100+", "VERIFIED listing"),
 "C17902": ("1206W4F1002T5E", "Uni-Royal", 1059900, 0.0079, "100+", "VERIFIED listing"),
 "C4410": ("1206W4F1001T5E", "Uni-Royal", 655650, 0.0086, "50+", "VERIFIED listing"),
 "C17944": ("1206W4F2001T5E", "Uni-Royal", 1321900, 0.0078, "100+", "LISTING 2026-11-05"),
 "C17997": ("1206W4F4703T5E", "Uni-Royal", 9000, 0.0074, "100+", "LISTING 2026-11-05; value to tune on the bench"),
 "C209907": ("HLK-5M05", "Hi-Link", 3052, 2.9474, "1+", "VERIFIED + datasheet read (BorePilot work); 38 x 23 x 18 mm, 90-265 VAC, 3000 VAC isolation"),
 "C142727": ("0218.500MXP", "Littelfuse", 900, 0.2257, "5+", "LISTING 2026-10-28; 0.5 A slow-blow 5x20, HLK datasheet value"),
 "C3131": ("BLX-A XC-7", "Xucheng", 85140, 0.0854, "5+", "LISTING 2026-10-28; 2 clips per fuse, rating to confirm"),
 "C2839517": ("10D561K", "Surging", 38910, 0.0494, "10+", "LISTING 2026-10-28; varistor value from the HLK datasheet"),
}

# ref, section, name, LCSC, qty, pins "pin=net,pin=net" ('-' = no connect)
PARTS = [
 # ---- power
 ("J1", "power", "DC barrel jack 5.5/2.1 mm: external 5 V in", "C136744", 1, "1 tip +=DC_IN,2 sleeve -=GND,3 switch=-"),
 ("J10", "power", "5 V DC screw terminal 2P (+5 V, GND): external 5 V in", "C474952", 1, "1 +5V=DC_IN,2 GND=GND"),
 ("F1", "power", "PTC fuse 0.5 A 6 V, 1206", "C163512", 1, "1=DC_IN,2=DC_F"),
 ("D1", "power", "TVS 5 V (SMAJ5.0A) across the supply", "C5121739", 1, "A=GND,K=DC_F"),
 ("D2", "power", "Schottky OR-ing: DC jack to +5V", "C2758511", 1, "A=DC_F,K=+5V"),
 ("D3", "power", "Schottky OR-ing: USB VBUS to +5V", "C2758511", 1, "A=VBUS,K=+5V"),
 ("C1", "power", "470 uF 16 V bulk on +5V", "C47344174", 1, "+=+5V,-=GND"),
 ("U2", "power", "AP2112K-3.3 LDO, SOT-25", "C51118", 1, "1 VIN=+5V,2 GND=GND,3 EN=+5V,4 NC=-,5 VOUT=+3V3"),
 ("C2", "power", "10 uF 1206, LDO input", "C9807", 1, "1=+5V,2=GND"),
 ("C3", "power", "10 uF 1206, LDO output", "C9807", 1, "1=+3V3,2=GND"),
 ("C5", "power", "100 nF 1206 on +5V", "C24497", 1, "1=+5V,2=GND"),
 # ---- optional HLK
 ("J9", "hlk", "OPTIONAL AC in screw terminal 2P (230 V)", "C474952", 1, "1=AC_L,2=AC_N"),
 ("F2", "hlk", "OPTIONAL fuse 0.5 A slow-blow 5x20 (ships separately)", "C142727", 1, "1=AC_L,2=AC_LF"),
 ("F2H", "hlk", "OPTIONAL 5x20 fuse clips (2 pieces)", "C3131", 2, "1 clip=AC_L,2 clip=AC_LF"),
 ("RV1", "hlk", "OPTIONAL varistor 560 V (10D561K) across L-N", "C2839517", 1, "1=AC_LF,2=AC_N"),
 ("U8", "hlk", "OPTIONAL HLK-5M05 AC-DC 5 V 1 A module", "C209907", 1, "AC(L)=AC_LF,AC(N)=AC_N,+Vo=+5V_HLK,-Vo=GND"),
 ("D4", "hlk", "OPTIONAL Schottky OR-ing: HLK to +5V", "C2758511", 1, "A=+5V_HLK,K=+5V"),
 ("C6", "hlk", "OPTIONAL 100 nF 1206 on the HLK output", "C24497", 1, "1=+5V_HLK,2=GND"),
 # ---- usb
 ("J5", "usb", "USB-C 16-pin receptacle (programming and 5 V)", "C165948", 1, "A4B9 VBUS=VBUS,B4A9 VBUS=VBUS,A1B12 GND=GND,B1A12 GND=GND,A5 CC1=CC1,B5 CC2=CC2,A6 DP1=USB_DP_J,B6 DP2=USB_DP_J,A7 DN1=USB_DN_J,B7 DN2=USB_DN_J,A8 SBU1=-,B8 SBU2=-,EH1-4 shell=GND"),
 ("U3", "usb", "USBLC6-2SC6 ESD on USB D+/D-", "C7519", 1, "1 I/O1 (J5 side)=USB_DP_J,6 I/O1 (MCU side)=USB_DP,3 I/O2 (J5 side)=USB_DN_J,4 I/O2 (MCU side)=USB_DN,5 VBUS=VBUS,2 GND=GND"),
 ("R1", "usb", "5.1 k 1206, CC1 pull-down", "C26033", 1, "1=CC1,2=GND"),
 ("R2", "usb", "5.1 k 1206, CC2 pull-down", "C26033", 1, "1=CC2,2=GND"),
 ("C7", "usb", "100 nF 1206 on VBUS", "C24497", 1, "1=VBUS,2=GND"),
 # ---- mcu
 ("U1", "mcu", "ESP32-C3-MINI-1-N4 module", "C2838502", 1, "1 GND=GND,2 GND=GND,3 3V3=+3V3,5 IO2=DHT,6 IO3=PROBE_60,8 EN=EN,11 GND=GND,12 IO0=LDR,13 IO1=PROBE_40,14 GND=GND,16 IO10=PROBE_20,18 IO4=PROBE_COM,19 IO5=PROBE_80,20 IO6=PROBE_FULL,21 IO7=FLOAT1,22 IO8=LED_ST,23 IO9=BOOT,26 IO18=USB_DN,27 IO19=USB_DP,30 RXD0 IO20=US_ECHO,31 TXD0 IO21=US_TRIG,36-53 GND pads=GND"),
 ("SW1", "mcu", "Reset button (EN)", "C318884", 1, "1=EN,3=GND"),
 ("SW2", "mcu", "BOOT / PAIR button (GPIO9)", "C318884", 1, "1=BOOT,3=GND"),
 ("R3", "mcu", "10 k 1206, EN pull-up", "C17902", 1, "1=+3V3,2=EN"),
 ("C8", "mcu", "100 nF 1206, EN to GND", "C24497", 1, "1=EN,2=GND"),
 ("C4", "mcu", "10 uF 1206, 3V3 at the module", "C9807", 1, "1=+3V3,2=GND"),
 ("C9", "mcu", "100 nF 1206, module 3V3", "C24497", 1, "1=+3V3,2=GND"),
 ("C10", "mcu", "100 nF 1206, module 3V3", "C24497", 1, "1=+3V3,2=GND"),
 ("LED1", "mcu", "Red LED: power (3.3 V)", "C965798", 1, "A=LED1_A,K=GND"),
 ("R6", "mcu", "1 k 1206, LED1 series", "C4410", 1, "1=+3V3,2=LED1_A"),
 ("LED2", "mcu", "Green LED: status (GPIO8)", "C2986059", 1, "A=LED2_A,K=GND"),
 ("R7", "mcu", "1 k 1206, LED2 series", "C4410", 1, "1=LED_ST,2=LED2_A"),
 ("J6", "mcu", "OPTIONAL expansion header 1x4 (5V, 3V3, GND, IO2 shared with the DHT11 line)", "C2691448", 1, "1=+5V,2=+3V3,3=GND,4=DHT"),
 # ---- ultrasonic
 ("J2", "ultra", "Ultrasonic sensor header 1x4 (JSN-SR04T / HC-SR04)", "C2691448", 1, "1 +5V=+5V,2 TRIG=US_TRIG,3 ECHO=ECHO_5V,4 GND=GND"),
 ("R15", "ultra", "1 k 1206, ECHO series (divider top)", "C4410", 1, "1=ECHO_5V,2=US_ECHO"),
 ("R16", "ultra", "2 k 1206, ECHO divider to GND", "C17944", 1, "1=US_ECHO,2=GND"),
 ("C14", "ultra", "100 nF 1206 on the sensor +5V", "C24497", 1, "1=+5V,2=GND"),
 # ---- floats
 ("J3", "floats", "Float switch terminal 2P (dry contact)", "C474952", 1, "1=FLOAT1_T,2=GND"),
 ("R8", "floats", "1 k 1206, FLOAT1 series", "C4410", 1, "1=FLOAT1_T,2=FLOAT1"),
 ("R4", "floats", "10 k 1206, FLOAT1 pull-up", "C17902", 1, "1=+3V3,2=FLOAT1"),
 ("C12", "floats", "100 nF 1206, FLOAT1 filter", "C24497", 1, "1=FLOAT1,2=GND"),
 ("U4", "floats", "USBLC6-2SC6 ESD for the float line (second channel unused)", "C7519", 1, "1 I/O1=FLOAT1_T,6 I/O1=FLOAT1_T,3 I/O2=-,4 I/O2=-,5 VBUS=+3V3,2 GND=GND"),
 # ---- extra sensors
 ("J11", "sens", "LDR screw terminal 2P (light sensor on a cable)", "C474952", 1, "1=LDR_T,2=GND"),
 ("R24", "sens", "1 k 1206, LDR series", "C4410", 1, "1=LDR_T,2=LDR"),
 ("R22", "sens", "10 k 1206, LDR divider pull-up", "C17902", 1, "1=+3V3,2=LDR"),
 ("C15", "sens", "100 nF 1206, LDR filter", "C24497", 1, "1=LDR,2=GND"),
 ("J12", "sens", "DHT11 header 1x3 (3V3, DATA, GND)", "C492402", 1, "1 +3V3=+3V3,2 DATA=DHT,3 GND=GND"),
 ("R23", "sens", "10 k 1206, DHT11 data pull-up", "C17902", 1, "1=+3V3,2=DHT"),
 # ---- probes
 ("J4", "probes", "Probe terminal 3P: COM, 20 %, 40 %", "C474953", 1, "1 COM=PROBE_COM_T,2 20%=PROBE_20_T,3 40%=PROBE_40_T"),
 ("J8", "probes", "Probe terminal 3P: 60 %, 80 %, FULL", "C474953", 1, "1 60%=PROBE_60_T,2 80%=PROBE_80_T,3 FULL=PROBE_FULL_T"),
 ("C11", "probes", "1 uF 1206 coupling capacitor on PROBE_COM (no DC in the water)", "C1848", 1, "1=PROBE_COM,2=PROBE_COM_T"),
 ("R10", "probes", "1 k 1206, probe 20 % series", "C4410", 1, "1=PROBE_20_T,2=PROBE_20"),
 ("R11", "probes", "1 k 1206, probe 40 % series", "C4410", 1, "1=PROBE_40_T,2=PROBE_40"),
 ("R12", "probes", "1 k 1206, probe 60 % series", "C4410", 1, "1=PROBE_60_T,2=PROBE_60"),
 ("R13", "probes", "1 k 1206, probe 80 % series", "C4410", 1, "1=PROBE_80_T,2=PROBE_80"),
 ("R14", "probes", "1 k 1206, probe FULL series", "C4410", 1, "1=PROBE_FULL_T,2=PROBE_FULL"),
 ("R17", "probes", "470 k 1206, probe 20 % pull-down", "C17997", 1, "1=PROBE_20,2=GND"),
 ("R18", "probes", "470 k 1206, probe 40 % pull-down", "C17997", 1, "1=PROBE_40,2=GND"),
 ("R19", "probes", "470 k 1206, probe 60 % pull-down", "C17997", 1, "1=PROBE_60,2=GND"),
 ("R20", "probes", "470 k 1206, probe 80 % pull-down", "C17997", 1, "1=PROBE_80,2=GND"),
 ("R21", "probes", "470 k 1206, probe FULL pull-down", "C17997", 1, "1=PROBE_FULL,2=GND"),
]
REF_SEC = {p[0]: p[1] for p in PARTS}
BYREF = {p[0]: p for p in PARTS}
OPTIONAL = {r for r, s, n, c, q, pins in PARTS if "OPTIONAL" in n}
TOTAL_PIECES = sum(p[4] for p in PARTS)


def pins_of(ref):
    out = []
    for it in BYREF[ref][5].split(","):
        a, b = it.rsplit("=", 1)
        out.append((a.strip(), None if b.strip() == "-" else b.strip()))
    return out


def bom_rows():
    """Group identical LCSC parts: returns list of (refs, qty, name, lcsc, mpn, stock, price, tier, status, subtotal)."""
    by = {}
    order = []
    for ref, sec, name, c, q, pins in PARTS:
        if c not in by:
            by[c] = {"refs": [], "q": 0, "names": []}
            order.append(c)
        by[c]["refs"].append(ref)
        by[c]["q"] += q
        by[c]["names"].append(name)
    rows = []
    for c in order:
        d = by[c]
        mpn, mk, st, pr, tier, status = INFO[c]
        rows.append((", ".join(d["refs"]), d["q"], d["names"][0] if len(d["names"]) == 1 else " / ".join(sorted(set(n.split(",")[0] for n in d["names"])))[:90], c, mpn, mk, st, pr, tier, status, d["q"] * pr))
    return rows


def totals():
    rows = bom_rows()
    all_ = sum(r[10] for r in rows)
    opt_refs = OPTIONAL
    opt = sum(BYREF[r][4] * INFO[BYREF[r][3]][3] for r in opt_refs)
    hlk = sum(BYREF[r][4] * INFO[BYREF[r][3]][3] for r in BYREF if BYREF[r][1] == "hlk")
    return all_, hlk, all_ - hlk
