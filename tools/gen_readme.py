"""Generate README.md (BOM tables come from tools/data.py so they always match the design).
    python -X utf8 tools/gen_readme.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tot_all, tot_hlk, tot_5v = D.totals()


def bom_section(sid):
    parts = [p for p in D.PARTS if p[1] == sid]
    groups, order = {}, []
    for ref, s, name, c, q, pins in parts:
        if c not in groups:
            groups[c] = {"refs": [], "q": 0, "name": name}
            order.append(c)
        groups[c]["refs"].append(ref)
        groups[c]["q"] += q
    rows, sub = [], 0.0
    for c in order:
        g = groups[c]
        mpn, mk, st, pr, tier, status = D.INFO[c]
        line = g["q"] * pr
        sub += line
        name = g["name"] if len(g["refs"]) == 1 else " / ".join(dict.fromkeys(D.BYREF[r][2].split(",")[0].replace("OPTIONAL ", "") for r in g["refs"]))
        opt = " *(option)*" if sid == "hlk" or all(r in D.OPTIONAL for r in g["refs"]) else ""
        rows.append(f"| {', '.join(g['refs'])} | {g['q']} | {name}{opt} | `{mpn}` | [{c}](https://www.lcsc.com/product-detail/{c}.html) | {st} | ${pr:.4f} | ${line:.2f} |")
    head = "| Ref | Qty | Function | Part | LCSC | Stock | Unit | Line |\n|---|---:|---|---|---|---:|---:|---:|\n"
    return head + "\n".join(rows) + f"\n\n**Subtotal: ${sub:.2f}**\n", sub


def bom_all():
    out = []
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        out.append(f"#### {ptitle}\n")
        for sid in secs:
            title, desc = D.SEC[sid][1], D.SEC[sid][3]
            t, sub = bom_section(sid)
            out.append(f"**{title}**  \n<sub>{desc}</sub>\n\n{t}")
    return "\n".join(out)


GPIO = [("0", "LDR", "in (ADC)", "J11 via 1 k, 10 k pull-up, 100 nF"), ("1", "PROBE_40", "in", "probe line, 1 k series + 470 k pull-down"), ("2", "DHT", "io", "J12 DATA, 10 k pull-up (strapping pin, idles high)"),
        ("3", "PROBE_60", "in", "probe line"), ("4", "PROBE_COM", "out", "AC burst through C11 (1 uF) to the COM rod"), ("5", "PROBE_80", "in", "probe line"), ("6", "PROBE_FULL", "in", "probe line"),
        ("7", "FLOAT1", "in", "J3 float, 10 k pull-up"), ("8", "LED_ST", "out", "green status LED (strapping pin: LED only)"), ("9", "BOOT / PAIR", "in", "SW2 to GND (strapping pin)"),
        ("10", "PROBE_20", "in", "probe line"), ("18 / 19", "USB D- / D+", "io", "USB-C through the ESD part U3"), ("20", "US_ECHO", "in", "J2 ECHO via 1 k / 2 k divider (RXD0)"),
        ("21", "US_TRIG", "out", "J2 TRIG (TXD0)"), ("EN", "EN", "in", "SW1 reset, 10 k pull-up, 100 nF")]

PORTS = [("J1", "DC jack 5.5/2.1", "tip = +5 V, sleeve = GND"), ("J10", "5 V terminal (2P)", "1 = GND, 2 = +5 V"), ("J5", "USB-C", "programming, logs, 5 V"),
         ("J2", "Ultrasonic header (1x4)", "1 = GND, 2 = ECHO, 3 = TRIG, 4 = +5 V"), ("J3", "Float switch (2P)", "1 = GND, 2 = float (either wire order)"),
         ("J4", "Probes (3P)", "1 = 40 %, 2 = 20 %, 3 = COM"), ("J8", "Probes (3P)", "1 = FULL, 2 = 80 %, 3 = 60 %"), ("J11", "LDR (2P)", "1 = GND, 2 = LDR (either wire order)"),
         ("J12", "DHT11 header (1x3)", "1 = GND, 2 = DATA, 3 = +3V3 (check your module's order)"), ("J6", "Expansion (1x4, not fitted)", "1 = IO2 (DHT), 2 = GND, 3 = +3V3, 4 = +5 V"),
         ("J9", "AC in (2P, option)", "1 = N, 2 = L (230 V, engineer review)")]

README = f"""<div align="center">

<img src="docs/images/tankpilot-hero-animated.svg" alt="TankPilot animated banner" width="100%">

# TankPilot

**Know your water tank level in percent, and let Home Assistant start the pump before the tank runs dry.**

One small ESP32-C3 board. Three kinds of level sensors. Automatic fallback. Open source.

![ESP32-C3](https://img.shields.io/badge/MCU-ESP32--C3-0891b2?style=for-the-badge)
![ESPHome](https://img.shields.io/badge/Firmware-ESPHome-1d4ed8?style=for-the-badge)
![Home Assistant](https://img.shields.io/badge/Smart%20home-Home%20Assistant-18bcf2?style=for-the-badge)
![PCB](https://img.shields.io/badge/PCB-94%20x%2070%20mm-16a34a?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-f59e0b?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-PCB%20routed%2C%20not%20built%20yet-orange?style=for-the-badge)

[Features](#-features) | [How it works](#-how-it-works) | [Hardware](#-hardware-at-a-glance) | [Pinout](#-ports-and-pinout) | [BOM](#-bill-of-materials) | [Firmware](#-firmware-and-home-assistant) | [Docs](#-documentation) | [Status](#-project-status)

<img src="docs/images/social/08_board_3d_angle_1600x900.png" alt="TankPilot 3D render" width="90%">

</div>

> **Heads-up:** this is a design project. The schematic, PCB layout and routing are done (DRC clean), but **no board has been built or tested yet**, and the probe circuit and the firmware are still ideas to be proven on the bench. The repository name says ESP32-S3 because that is where the project started; the board uses an **ESP32-C3-MINI-1** module.

## Why TankPilot?

Float switches only say "full" or "empty". Ultrasonic sensors give a nice number but fail with steam, foam or a dirty sensor face. Probe kits are rugged and cheap but give steps. Most tank controllers lock you into one of them, with no smart-home link.

TankPilot puts all three on one open board. The ultrasonic sensor gives a smooth percentage, the stainless probes are the safety cross-check, and the float is the last resort. If one fails, the board keeps working with the next one and **tells you which source it is using**.

## Features

| | Feature | Details |
|---|---|---|
| 📏 | **Ultrasonic level** | Header for JSN-SR04T / HC-SR04 style 5 V sensors; the 5 V echo is divided to a safe 3.3 V |
| 🧪 | **5-level probe port** | COM + 5 stainless probes (20, 40, 60, 80 %, FULL) on two screw terminals, driven with **AC** through a capacitor so the probes do not corrode |
| 🔘 | **Float input** | Dry contact with pull-up, series resistor, filter capacitor and ESD protection for long cables |
| 🔁 | **Automatic fallback** | Ultrasonic fails: probes take over. Probes fouled: the float. The source is always reported |
| 🏠 | **Home Assistant ready** | ESPHome over Wi-Fi with encrypted API, OTA updates and a fallback hotspot |
| ⚡ | **Auto pump start** | A Home Assistant automation starts the pump below your limit (for example 20 %) and stops it at full |
| 🌡️ | **Light + climate** | LDR light sensor (analog) and DHT11 temperature / humidity |
| 🔌 | **3 power sources** | 5 V DC jack, 2-pin 5 V terminal, USB-C, or an optional on-board HLK-5M05 for 230 V AC |
| 🛡️ | **Protected** | 0.5 A PTC fuse, 5 V TVS, Schottky OR-ing, ESD arrays on USB and the float line, varistor + fuse on the 230 V option |
| 💾 | **Native USB-C** | Flash and read logs over USB: no USB-UART chip, EN and BOOT buttons on board |
| 📦 | **IP67 box ready** | 94 x 70 mm board sized for a 120 x 80 x 55 mm transparent IP67 enclosure |
| 🧰 | **Open and hackable** | Spare GPIO / 3.3 V / 5 V header, status LEDs, full design files and docs |

## How it works

<div align="center"><img src="docs/images/tankpilot-flow-animated.svg" alt="Data flow: sensors, board, Wi-Fi, Home Assistant, pump" width="100%"></div>

1. **Measure.** The ESP32-C3 reads the ultrasonic distance, the five probes and the float, and checks every source for health.
2. **Decide the level.** It converts the best healthy source to 0-100 %, cross-checks it against the probes and sends level, source and alerts to Home Assistant.
3. **Act.** Home Assistant compares the level with your start and stop limits and presses the pump's Start or Stop switch. If tank data is stale, it never starts the pump automatically.

### Which sensor should I buy?

| | Ultrasonic (JSN-SR04T) | 5-level probes (stainless) | Float switch |
|---|---|---|---|
| Output | smooth 0-100 % | 5 steps: 20 / 40 / 60 / 80 / FULL | one level |
| Great for | level bar, trends | auto-start at a level, overflow stop | simple backup |
| Weak point | about 25 cm blind zone; steam, foam, dirty face | rods foul over time; needs 6 wires | one level only |
| Tip | mount on the lid, facing down | COM = longest rod; a 5-probe kit gives COM + 4 levels | use only as a dry contact |

For **auto-start at a fixed level** the probes are the safest main sensor. The board supports all three, so you can add the others later.

## Hardware at a glance

| Item | Details |
|---|---|
| Microcontroller | ESP32-C3-MINI-1-N4 (Wi-Fi 2.4 GHz, Bluetooth LE, 4 MB flash, PCB antenna) |
| Firmware | ESPHome (esp-idf), native API with encryption, OTA |
| Probe port | 2 x 3-pin 5.08 mm terminals, AC-coupled COM drive, 1 k series + 470 k pull-down per line |
| Ultrasonic port | 1x4 header: +5 V, TRIG, ECHO (5 V to 3.3 V divider), GND |
| Float port | 2-pin 5.08 mm terminal, 10 k pull-up, 1 k series, 100 nF filter, ESD |
| Extra sensors | LDR (2-pin terminal, ADC) and DHT11 (3-pin header) |
| Power in | 5 V DC jack, 5 V terminal, USB-C, optional HLK-5M05 (90-265 V AC) |
| 3.3 V | AP2112K LDO, 470 uF bulk capacitor on 5 V |
| PCB | 94 x 70 mm, 2 layers, 1.6 mm, 3 mounting holes, GND pours, antenna keep-out, isolation slot for the 230 V option |
| Enclosure | 120 x 80 x 55 mm transparent ABS IP67 box (about 96 x 75 mm free floor, 43 mm inside height) |
| Parts cost | **{D.TOTAL_PIECES} parts, about ${tot_all:.2f}** with the 230 V option, **about ${tot_5v:.2f} without it** (PCB, sensors and box not included) |

<div align="center">
<img src="docs/images/social/09_board_3d_top_1600x900.png" alt="TankPilot top side 3D render" width="48%">
<img src="docs/images/social/10_board_3d_bottom_1600x900.png" alt="TankPilot bottom side 3D render" width="48%">
</div>

## Ports and pinout

Pin order below is **as built** in the EasyEDA schematic / PCB.

| Ref | Port | Pins |
|---|---|---|
""" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in PORTS) + f"""

### ESP32-C3 GPIO map

| GPIO | Net | Direction | Notes |
|---|---|---|---|
""" + "\n".join(f"| {a} | `{b}` | {c} | {d} |" for a, b, c, d in GPIO) + f"""

Strapping pins: GPIO2 must be high at reset (the DHT11 idles high through its pull-up), GPIO8 drives only the status LED, GPIO9 is BOOT. For USB download mode hold BOOT while pressing EN.

### Power

```
 5 V DC jack J1 --PTC F1--TVS D1--D2 --\\
 5 V terminal J10 ---------------------/
 USB-C VBUS J5 -------------------------D3 ----> +5V --> AP2112K --> +3V3 --> ESP32-C3
 HLK-5M05 (230 V option) ----------------D4 --/
```

The sources are combined with Schottky diodes, so the highest one wins and none can back-feed another. Because the IP67 box is sealed, use the **J10 terminal** for the 5 V supply; the DC jack and USB-C are for work with the lid open.

## Bill of materials

All parts are on LCSC (stock and prices read on 2026-11-05 and 2026-10-28; they change daily). Prices are the first quantity tier. Rows marked *(option)* belong to the optional 230 V block.

| | Pieces | Cost |
|---|---:|---:|
| **Everything** (with the 230 V option) | {D.TOTAL_PIECES} | **${tot_all:.2f}** |
| **5 V version** (without the 230 V option) | {D.TOTAL_PIECES - sum(p[4] for p in D.PARTS if p[1] == 'hlk')} | **${tot_5v:.2f}** |
| 230 V option only | {sum(p[4] for p in D.PARTS if p[1] == 'hlk')} | ${tot_hlk:.2f} |

Downloads: [`tank-node-bom-v1.csv`](hardware/bom/tank-node-bom-v1.csv) | [`bom-table.md`](hardware/bom/bom-table.md) | interactive page with tick boxes: [`docs/bom.html`](docs/bom.html)

{bom_all()}
Not in the BOM: the PCB, sensors (JSN-SR04T, probe kit, float switch, LDR, DHT11), the enclosure and cable glands, and a 5 V supply. The fuse clips (F2H, C3131) are in the BOM but not yet drawn in the schematic; check that your F2 footprint matches the 5x20 fuse.

## PCB and enclosure

- 94 x 70 mm, 2 layers, 1.6 mm, JLCPCB-style rules: default track 0.25 mm / clearance 0.2 mm, net classes for power, 230 V AC and USB.
- 63 parts, GND pours on both layers on the low-voltage side, antenna keep-out under the module end, isolation slot between the HLK module and the rest.
- DRC: **0 errors**. Mains tracks are 0.8 mm with live and neutral on different layers, but **must be reviewed by an engineer before any 230 V use**.
- Enclosure: 120 x 80 x 55 mm IP67 transparent ABS box. A 100 mm wide board would not fit; 94 x 70 mm does. Use cable glands for the sensor wires.

Floor plan, silkscreen blocks and X/Y tables: [`docs/pcb-floorplan.html`](docs/pcb-floorplan.html).

## Firmware and Home Assistant

**Planned entities (ESPHome):** `Tank level %`, `Tank level source`, `Ultrasonic distance cm`, `Probe 20 / 40 / 60 / 80 / FULL`, `Float 1`, `Ultrasonic OK`, `Probes OK`, `Sensor mode` (Auto, Ultrasonic only, Probes only, Float only), `D_empty cm`, `D_full cm`.

**Auto-start logic (Home Assistant automation):**

- **Start** when `Tank level %` is below `start_below` (default 20 %), the data is fresh, the pump is off, a minimum off time has passed and no alarm is active.
- **Stop** at `stop_at` (default FULL) or when the float says full, and after a maximum run time (default 60 min).
- If the tank node is unavailable for more than 2 minutes, the pump is never started automatically and you get a notification.
- A `Tank auto mode` switch turns the automation on or off; the pump's own buttons keep working.

<details>
<summary>Example automation (untested sketch, adjust the entity names)</summary>

```yaml
automation:
  - alias: "Tank low - start pump"
    trigger:
      - platform: numeric_state
        entity_id: sensor.tank_level
        below: input_number.tank_start_below
    condition:
      - condition: state
        entity_id: input_boolean.tank_auto_mode
        state: "on"
      - condition: state
        entity_id: switch.pump_running
        state: "off"
    action:
      - service: switch.turn_on
        target:
          entity_id: switch.start_pump
```

</details>

<details>
<summary>ESPHome starter (untested sketch, pins follow the GPIO map)</summary>

```yaml
esphome:
  name: tankpilot
esp32:
  board: esp32-c3-devkitm-1
  framework:
    type: esp-idf
logger:
api:
  encryption:
    key: !secret api_key
ota:
  platform: esphome
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
  ap:
sensor:
  - platform: ultrasonic
    trigger_pin: GPIO21
    echo_pin: GPIO20
    name: "Ultrasonic distance"
    update_interval: 5s
  - platform: adc
    pin: GPIO0
    name: "Light (LDR)"
  - platform: dht
    pin: GPIO2
    model: DHT11
    temperature: {{name: "Temperature"}}
    humidity: {{name: "Humidity"}}
binary_sensor:
  - platform: gpio
    pin: {{number: GPIO7, mode: INPUT_PULLUP, inverted: true}}
    name: "Float 1"
```

The probe-burst measurement (AC drive on GPIO4, reading GPIO10, 1, 3, 5, 6) needs a small custom component that is still to be written and bench-tested.

</details>

## Documentation

GitHub shows HTML files as source. Open them locally, or enable GitHub Pages for the `docs/` folder to read them online.

| Page | What is in it |
|---|---|
| [`docs/project-page.html`](docs/project-page.html) | the blog / website page for this project |
| [`docs/bom.html`](docs/bom.html) | BOM with tick boxes, search and copy-all C-numbers |
| [`docs/wiring-by-section.html`](docs/wiring-by-section.html) | system map, external wiring, pin-to-net diagrams |
| [`docs/schematic-sections.html`](docs/schematic-sections.html) | three schematic sheets, parts tables, pin guides for U1 and the ESD chips |
| [`docs/pcb-floorplan.html`](docs/pcb-floorplan.html) | floor plan, X/Y tables, enclosure fit |
| [`PLAN.md`](PLAN.md) | the full plan: MCU advice, circuits, level logic, open questions |

Images for posts (hero, square, story, infographics, 3D renders): [`docs/images/social/`](docs/images/social/).

## Project status

- [x] Concept, parts selection and LCSC BOM
- [x] Schematic (3 sheets) in EasyEDA
- [x] PCB layout, rules, routing, DRC clean
- [x] 3D renders, documentation, project page
- [ ] Order a small batch of boards and check footprints and pin orders
- [ ] Bench-test and tune the probe circuit
- [ ] Write the ESPHome firmware (including the probe-burst component)
- [ ] Home Assistant dashboard and automation
- [ ] Optional: engineer review of the 230 V section

**Known open points:** fuse clips for F2 are not in the schematic; the mounting hole at (4, 66) mm is close to J10 (use a low-profile screw or a plastic standoff); GPIO8 status LED can matter for USB download mode; the JSN-SR04T trigger level and several part data sheets are not read yet (see [`PLAN.md`](PLAN.md), section 11).

## Safety

The optional HLK-5M05 section connects the board to **230 V AC**, and a water tank is a wet place. Build the 5 V version first, use an IP65 or better box, keep mains wiring away from the probe cables, and have a qualified person review anything that touches mains. Never connect a float switch contact to the pump or to mains on the same wires as the sensor input.

## Repository layout

```
docs/                 HTML guides (BOM, wiring, schematic, PCB) and images
  images/social/      post graphics and 3D renders
  images/renders/     EasyEDA 3D screenshots used for the graphics
hardware/bom/         BOM as CSV and Markdown
tools/                Python generators for the BOM, docs, SVGs, images and this README
PLAN.md               full design plan
```

Regenerate: `python tools/gen_docs.py`, `python tools/gen_svgs.py`, `python tools/make_images.py`, `python tools/gen_readme.py`.

## License

MIT, see [`LICENSE`](LICENSE). Datasheets are not included (copyrighted); see the part links above.

<div align="center">

Made by **ElectroIoT** | [electroiot.in](https://electroiot.in)

</div>
"""

if __name__ == "__main__":
    p = os.path.join(ROOT, "README.md")
    open(p, "w", encoding="utf-8").write(README)
    print("README.md", len(README))
