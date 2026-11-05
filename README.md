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
| LCSC BOM v1 (68 pieces, about $10.4; $6.7 without HLK) | [hardware/bom/tank-node-bom-v1.csv](hardware/bom/tank-node-bom-v1.csv), [page 1](docs/page1-power.html) |
| Connection map | [docs/connection-diagram.html](docs/connection-diagram.html) |
| BOM + wiring, 3 pages | [docs/page1-power.html](docs/page1-power.html), [page 2](docs/page2-esp32-core.html), [page 3](docs/page3-sensors.html) |
| Schematic guide | [docs/schematic-guide.html](docs/schematic-guide.html) |
| PCB placement guide (100 x 70 mm) | [docs/pcb-section-guide.html](docs/pcb-section-guide.html) |

License: [MIT](LICENSE).
