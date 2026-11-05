# TankPilot - ESP32-C3 water tank sensor node (planning draft)

Small low-cost board for the water tank. One board, three sensor ports, use whichever sensor you have:

- **Ultrasonic** (JSN-SR04T, HC-SR04, A02YYUW) on a 1x4 header
- **Float switch** x2 on screw terminals
- **Stainless conductive probes**: COM + 5 level probes (20 %, 40 %, 60 %, 80 %, FULL) on two 3-pin screw terminals, driven with AC so the probes do not corrode
- 5 V DC jack or USB-C power, ESP32-C3-MINI-1 module, ESPHome over Wi-Fi to Home Assistant (separate board: no change to BorePilot; a Home Assistant automation starts the pump below a set level)

**Status (2026-11-05): plan only.** No schematic, PCB or firmware yet. The PCB is laid out by the owner in EasyEDA. Read [PLAN.md](PLAN.md): MCU advice, GPIO table, port circuits, LCSC BOM, size and placement hints, open questions.

| What | Where |
|---|---|
| Plan | [PLAN.md](PLAN.md) |
| LCSC BOM (draft) | [hardware/bom/tank-node-bom-v0.csv](hardware/bom/tank-node-bom-v0.csv) |

License: [MIT](LICENSE).
