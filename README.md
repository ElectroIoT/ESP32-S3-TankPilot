# TankPilot - ESP32-C3 water tank sensor node (planning draft)

Small low-cost board for the water tank. One board, three sensor ports, use whichever sensor you have:

- **Ultrasonic** (JSN-SR04T, HC-SR04, A02YYUW) on a 1x4 header
- **Float switch** on a screw terminal, plus an **LDR** (2-pin terminal) and a **DHT11** (3-pin header)
- **Stainless conductive probes**: COM + 5 level probes (20 %, 40 %, 60 %, 80 %, FULL) on two 3-pin screw terminals, driven with AC so the probes do not corrode
- 5 V DC jack or 2-pin terminal, USB-C, or optional on-board HLK-5M05 (230 V AC, engineer review) power, ESP32-C3-MINI-1 module, ESPHome over Wi-Fi to Home Assistant (separate board: no change to BorePilot; a Home Assistant automation starts the pump below a set level)

**Status (2026-11-05): plan + BOM + connection and placement guides.** No schematic, PCB file or firmware yet. The PCB is laid out by the owner in EasyEDA. Read [PLAN.md](PLAN.md): MCU advice, GPIO table, port circuits, LCSC BOM, size and placement hints, open questions.

| What | Where |
|---|---|
| Plan | [PLAN.md](PLAN.md) |
| BOM (68 pieces, about $10.4; $6.7 without HLK) | [docs/bom.html](docs/bom.html), [CSV](hardware/bom/tank-node-bom-v1.csv) |
| Wiring (system map, external wiring, pin-to-net) | [docs/wiring-by-section.html](docs/wiring-by-section.html) |
| Schematic by section | [docs/schematic-sections.html](docs/schematic-sections.html) |
| PCB floorplan 100 x 70 mm | [docs/pcb-floorplan.html](docs/pcb-floorplan.html) |

License: [MIT](LICENSE).
