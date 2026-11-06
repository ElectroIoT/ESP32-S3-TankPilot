"""Generate the HTML pages and BOM files for TankPilot. Run from the repo root:
    python -X utf8 -I tools/gen_docs.py
Writes docs/bom.html, wiring-by-section.html, schematic-sections.html, pcb-floorplan.html (same look as the HexRelay variants pages),
docs/images/pcb-floorplan.svg and hardware/bom/*. All connections are PLANNED (no schematic exists yet)."""
import os, sys, csv, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import layout as PL
import sheets as SH
import pinguides as PG

e = html.escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
os.makedirs(os.path.join(DOCS, "images"), exist_ok=True)

CSS = """:root{--bg:#f4f6fb;--card:#fff;--ink:#16202f;--fg:#16202f;--mut:#64748b;--mute:#64748b;--line:#e2e8f0;--acc:#2563eb;--board:#e8efe4}
@media (prefers-color-scheme:dark){:root{--bg:#0b1220;--card:#131c2e;--ink:#e6edf7;--fg:#e6edf7;--mut:#93a3b8;--mute:#93a3b8;--line:#243049;--acc:#60a5fa;--board:#16251d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,Segoe UI,Roboto,sans-serif}
header{padding:36px 16px 70px;background:linear-gradient(120deg,#0f172a,#1e3a8a 55%,#0e7490);color:#fff}
.wrap{max-width:1100px;margin:0 auto;padding:0 16px}
header h1{margin:0 0 6px;font-size:clamp(24px,4vw,36px)}
header p{margin:0;opacity:.85}
header nav a{color:#fff;background:#ffffff22;padding:5px 12px;border-radius:99px;margin:10px 8px 0 0;text-decoration:none;font-size:13.5px;display:inline-block}
header nav a.on{background:#fff;color:#0f172a;font-weight:700}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:-48px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px;box-shadow:0 6px 20px rgba(0,0,0,.08)}
.stat b{display:block;font-size:26px}.stat span{color:var(--mut);font-size:13px}
.top{margin-top:-48px}
.bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:22px 0 8px}
.bar input[type=search],.bar input[type=number]{padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);color:var(--ink);font:inherit}
.bar input[type=search]{flex:1;min-width:200px}.bar input[type=number]{width:80px}
button{padding:9px 14px;border:0;border-radius:10px;background:var(--acc);color:#fff;font:inherit;cursor:pointer}
button.ghost{background:transparent;color:var(--acc);border:1px solid var(--acc)}
.prog{height:8px;border-radius:99px;background:var(--line);overflow:hidden;margin:6px 0 20px}
.prog i{display:block;height:100%;width:0;background:linear-gradient(90deg,#10b981,#22d3ee);transition:width .3s}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;margin:0 0 18px;overflow:hidden}
.card>h2{margin:0;padding:12px 16px;font-size:17px;color:#fff;background:var(--c,#475569);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
.card>*:not(h2){margin-left:16px;margin-right:16px}.card>h2+*{margin-top:12px}.card>*:last-child{margin-bottom:16px}
.card>h2 .cnt,.card>h2 label{color:#fff}.cnt{font-weight:400;font-size:13px;opacity:.92}
h3{font-size:1rem;margin:16px 0 6px}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:640px;font-size:14px}
th,td{padding:8px 10px;text-align:left;border-top:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);border-top:0;white-space:nowrap}
td.num,td.n{text-align:right;white-space:nowrap}
tr.ok,tr.done{opacity:.5}tr.ok td,.step.ok span{text-decoration:line-through}
input.ck{width:18px;height:18px}
.mpn{display:block;font-family:ui-monospace,Consolas,monospace;font-size:13px}
.note{display:block;color:var(--mut);font-size:12.5px;margin-top:2px}.mut{color:var(--mut);font-size:13px}
a{color:var(--acc)}
.tag{display:inline-block;padding:1px 8px;border-radius:99px;font-size:11.5px;font-weight:600;background:#dcfce7;color:#166534}
.tag.LISTING{background:#fef3c7;color:#92400e}.tag.opt{background:#e2e8f0;color:#334155}.tag.VERIFIED{background:#dcfce7;color:#166534}
@media (prefers-color-scheme:dark){.tag{background:#14532d;color:#bbf7d0}.tag.LISTING{background:#78350f;color:#fde68a}.tag.opt{background:#334155;color:#e2e8f0}}
.warn{background:var(--card);border-left:5px solid #dc2626;border-radius:8px;padding:8px 12px;margin:16px 0;font-size:13px;border-top:1px solid var(--line);border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.rec{border-left:4px solid #10b981;padding:6px 12px;background:rgba(16,185,129,.1);border-radius:6px;margin:12px 0}
.chips{position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:5;display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:14px}
.chips a,.chip{padding:4px 10px;border-radius:14px;color:#fff;text-decoration:none;font-size:12px;font-weight:700}
.pbar{height:8px;background:var(--line);border-radius:5px;overflow:hidden;min-width:140px}.pbar div{height:100%;background:#10b981;width:0}
ul.rules li,ol.steps li{margin:5px 0}.step{display:flex;gap:10px;padding:6px 0;border-bottom:1px dashed var(--line)}
svg.plan,svg.dia{max-width:100%;height:auto}svg.dia text{fill:var(--ink);font-family:system-ui,Segoe UI,sans-serif}.ref{font-size:12px;font-weight:700}.role{font-size:10.5px;fill:var(--mut)!important}.lab{font-size:9.5px;fill:var(--mut)!important}
.pin{font-size:11px}.net{font-size:11px;font-weight:700}.flag{font-size:10px;font-weight:700;fill:#10151c!important}.pill{font-size:11px;font-weight:700;fill:#fff!important}
.bx{cursor:pointer}.bx.ok{opacity:.35}
.w{cursor:pointer;transition:opacity .15s}svg.hl .w{opacity:.15}svg.hl .w.on{opacity:1}.w.done line{stroke-dasharray:4 4}.pt{cursor:pointer}.pt.ok rect{fill-opacity:.1;stroke-dasharray:.6 .6}.pt.ok text{opacity:.4}
.legend{margin:12px 0}.legend span{display:inline-block;margin-right:12px;font-size:12px;color:var(--mut)}.legend i{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:5px;vertical-align:middle}
footer{color:var(--mut);font-size:13px;padding:10px 0 40px}
@media print{header{background:#fff;color:#000}.bar,button,.chips{display:none}}"""

NAV = [("bom.html", "BOM"), ("wiring-by-section.html", "Wiring"), ("schematic-sections.html", "Schematic"), ("pcb-floorplan.html", "PCB floorplan")]
HEAD_SUB = "ESP32-C3 water tank sensor node &middot; ultrasonic, float, 5-probe, LDR, DHT11 &middot; LCSC listings read 2026-11-05 &middot; Sheet N here = Sheet N on every page"


def head(title, sub, nav="", active="bom.html", stats=""):
    nv = "".join(f'<a class="{"on" if f == active else ""}" href="{f}">{n}</a>' for f, n in NAV)
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><style>{CSS}</style></head><body>'
            f'<header><div class="wrap"><h1>{e(title)}</h1><p>{sub}</p><nav>{nv}</nav></div></header><div class="wrap">' + stats +
            '<div class="warn"><b>Plan stage.</b> Planned design, not a finished schematic or PCB: nets come from PLAN.md, pin names and footprints must be checked in EasyEDA and against datasheets. The optional HLK 230 V block involves mains voltage: engineer review before any mains power; use the 5 V adapter or USB if unsure.</div>' + nav)


def links():
    return '<footer id="top-all">Generated by <code>tools/gen_docs.py</code>. Prices are the first LCSC tier shown and change daily; stock is from the check date. Datasheets of some parts are not read yet (see PLAN.md, section 11).</footer>'


NETCOL = {"GND": "#8a93a3", "+5V": "#fb8c00", "+5V_HLK": "#fb8c00", "DC_IN": "#fb8c00", "DC_F": "#fb8c00", "VBUS": "#fb8c00", "+3V3": "#f4b400"}
RAILS = ("+5V", "+5V_HLK", "VBUS", "+3V3")


def ncol(n):
    if n in NETCOL: return NETCOL[n]
    if n.startswith("AC_"): return "#e53935"
    if n.startswith(("USB_", "CC")): return "#8e24aa"
    if n.startswith("PROBE"): return "#ec407a"
    if n.startswith(("FLOAT", "US_", "ECHO")): return "#2fbf71"
    if n in ("EN", "BOOT", "EXP", "LDR", "DHT") or n.startswith(("LED",)): return "#a66cff"
    return "#00bcd4"


# ------------------------------------------------------------------ BOM files
def write_bom():
    rows = D.bom_rows()
    w = csv.writer(open(os.path.join(ROOT, "hardware/bom/tank-node-bom-v1.csv"), "w", newline="", encoding="utf-8"))
    w.writerow(["Refs", "Qty", "Function", "LCSC #", "MPN", "Manufacturer", "Stock", "Unit price USD", "Tier", "Status", "Line total USD", "Optional (HLK 230 V block)"])
    for refs, q, name, c, mpn, mk, st, pr, tier, status, sub in rows:
        opt = "yes" if all(D.BYREF[r][1] == "hlk" for r in refs.split(", ")) else ""
        w.writerow([refs, q, name, c, mpn, mk, st, pr, tier, status, f"{sub:.4f}", opt])
    return rows


def bom_md():
    rows = D.bom_rows()
    o = ["| Refs | Qty | Function | LCSC | Stock | Unit $ (tier) | Status |", "|---|---|---|---|---|---|---|"]
    for refs, q, name, c, mpn, mk, st, pr, tier, status, sub in rows:
        o.append(f"| {refs} | {q} | {name} | [{c}](https://www.lcsc.com/product-detail/{c}.html) {mpn} | {st} | {pr:.4f} ({tier}) | {status} |")
    return "\n".join(o)


# ------------------------------------------------------------------ wiring diagrams
def gnd_sym(x, y, c, right=True):
    s = 1 if right else -1
    return (f'<line x1="{x}" y1="{y}" x2="{x+12*s}" y2="{y}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+12*s}" y1="{y-7}" x2="{x+12*s}" y2="{y+7}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+16*s}" y1="{y-4}" x2="{x+16*s}" y2="{y+4}" stroke="{c}" stroke-width="2"/>'
            f'<line x1="{x+20*s}" y1="{y-2}" x2="{x+20*s}" y2="{y+2}" stroke="{c}" stroke-width="2"/>')


def section_svg(sid):
    parts = [p for p in D.PARTS if p[1] == sid]
    PXR = 300
    y = 16
    boxes, pinpos = [], []
    for ref, s, name, c, q, pins in parts:
        pl = D.pins_of(ref)
        h = 34 + 16 * len(pl)
        boxes.append((ref, name, c, pl, y, h))
        for k, (pin, net) in enumerate(pl):
            pinpos.append((ref, pin, net, y + 40 + 16 * k))
        y += h + 14
    lanes = []
    for ref, pin, net, py in pinpos:
        if net and net not in D_RAILS and net != "GND" and net not in lanes:
            lanes.append(net)
    lx = {n: 520 + 24 * i for i, n in enumerate(lanes)}
    Wd, Ht = 520 + 24 * len(lanes) + 30, y + 20
    o = [f'<svg viewBox="0 0 {Wd} {Ht}" width="{Wd}" height="{Ht}" class="dia" data-sec="{sid}">']
    for ref, name, c, pl, by, bh in boxes:
        opt = ref in D.OPTIONAL
        o.append(f'<g class="bx" data-ref="{ref}"><rect x="8" y="{by}" width="{PXR-8}" height="{bh}" rx="7" fill="var(--card)" stroke="var(--line)" stroke-width="2" {"stroke-dasharray=\"5 3\"" if opt else ""}/>'
                 f'<text x="16" y="{by+14}" class="ref">{e(ref)}</text><text x="{16+8*len(ref)+8}" y="{by+14}" class="role">{e(name[:44])}</text><text x="16" y="{by+27}" class="lab">[{c}]{" optional" if opt else ""}</text></g>')
    for ref, pin, net, py in pinpos:
        o.append(f'<text x="{PXR-14}" y="{py+3.5}" text-anchor="end" class="pin">{e(pin)}</text>')
        if not net:
            o.append(f'<g class="w"><line x1="{PXR}" y1="{py}" x2="{PXR+10}" y2="{py}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+10}" y1="{py-4}" x2="{PXR+16}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><line x1="{PXR+16}" y1="{py-4}" x2="{PXR+10}" y2="{py+4}" stroke="#9aa5b5" stroke-width="2"/><text x="{PXR+22}" y="{py+3.5}" class="lab">no connect</text></g>')
            continue
        c = ncol(net)
        if net == "GND":
            o.append(f'<g class="w" data-net="GND">{gnd_sym(PXR, py, c)}<text x="{PXR+28}" y="{py+3.5}" class="net" fill="{c}">GND</text></g>')
        elif net in D_RAILS:
            wd = 7 * len(net) + 10
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{PXR+14}" y2="{py}" stroke="{c}" stroke-width="3"/><rect x="{PXR+14}" y="{py-8}" width="{wd}" height="16" rx="4" fill="{c}"/><text x="{PXR+19}" y="{py+3.5}" class="flag">{e(net)}</text></g>')
        else:
            x2 = lx[net]
            pw = 6.6 * len(net) + 14
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{PXR}" y1="{py}" x2="{x2}" y2="{py}" stroke="{c}" stroke-width="2"/><circle cx="{PXR}" cy="{py}" r="3" fill="{c}"/><circle cx="{x2}" cy="{py}" r="2.6" fill="{c}"/><rect x="{PXR+14}" y="{py-9}" width="{pw:.0f}" height="18" rx="9" fill="{c}"/><text x="{PXR+22}" y="{py+4}" class="pill">{e(net)}</text></g>')
    for net in lanes:
        ys = [py for _, _, n, py in pinpos if n == net]
        if len(ys) > 1:
            o.append(f'<g class="w" data-net="{e(net)}"><line x1="{lx[net]}" y1="{min(ys)}" x2="{lx[net]}" y2="{max(ys)}" stroke="{ncol(net)}" stroke-width="2"/></g>')
    o.append("</svg>")
    return "".join(o)


D_RAILS = set(RAILS)


def tagcls(status):
    return "VERIFIED" if status.startswith("VERIFIED") else "LISTING"


def sheet_color(secs):
    return D.SEC[secs[0]][2]


def page_bom():
    total = len(D.PARTS)
    tot = D.totals()
    stats = ('<div class="stats top">'
             f'<div class="stat"><b>{D.TOTAL_PIECES}</b><span>parts per board</span></div>'
             f'<div class="stat"><b>{len(D.PAGES)}</b><span>schematic sheets</span></div>'
             f'<div class="stat"><b id="cost">${tot[0]:.2f}</b><span>parts cost, 1st price tier</span></div>'
             '<div class="stat"><b id="ticked">0%</b><span>ticked off</span></div></div>')
    o = [head("TankPilot - Bill of materials", HEAD_SUB, "", "bom.html", stats)]
    o.append('<div class="bar"><input type="search" id="q" placeholder="Search ref, MPN, C-number, function..."><label>Boards <input type="number" id="boards" min="1" value="1"></label>'
             '<label><input type="checkbox" id="hlk" checked> include optional HLK 230 V parts</label><button id="copy">Copy all C-numbers</button><button class="ghost" id="reset">Clear ticks</button></div><div class="prog"><i id="pbar"></i></div>')
    o.append('<div class="rec"><b>Whole board about USD %.2f</b> (%d pieces); <b>USD %.2f without</b> the optional HLK 230 V parts (USD %.2f: HLK-5M05, fuse + clips, varistor, AC terminal, diode, capacitor). PCB, sensors, enclosure and the 5 V adapter are not included.</div>' % (tot[0], D.TOTAL_PIECES, tot[2], tot[1]))
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        parts = [p for p in D.PARTS if p[1] in secs]
        cost = sum(p[4] * D.INFO[p[3]][3] for p in parts)
        o.append(f'<section class="card" id="{pid}" style="--c:{sheet_color(secs)}"><h2>{e(ptitle)}<span class="cnt">{len(parts)} lines, {sum(p[4] for p in parts)} pieces, about ${cost:.2f}</span></h2>')
        o.append('<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Function</th><th>Part</th><th>LCSC #</th><th>Qty</th><th>Stock</th><th>$ each</th></tr></thead><tbody>')
        for sid in secs:
            o.append(f'<tr><td colspan="8" style="background:{D.SEC[sid][2]}22"><b>{e(D.SEC[sid][1])}</b></td></tr>')
            for ref, s, name, c, q, pins in D.PARTS:
                if s != sid:
                    continue
                mpn, mk, st, pr, tier, status = D.INFO[c]
                opt = ref in D.OPTIONAL or s == "hlk"
                tg = ' <span class="tag opt">optional</span>' if opt else ""
                o.append(f'<tr data-ref="{ref}" data-sub="{q*pr:.4f}" data-opt="{1 if s == "hlk" else 0}" data-c="{c}" data-q="{q}"><td><input type="checkbox" class="ck" data-k="{ref}"></td><td class="ref"><b>{ref}</b></td>'
                         f'<td class="f">{e(name)}{tg}</td><td><span class="mpn">{e(mpn)}</span><span class="note">{e(mk)}</span><span class="tag {tagcls(status)}">{e(status.split(";")[0].split(" ")[0])}</span><span class="note">{e(status)}</span></td>'
                         f'<td><a href="https://www.lcsc.com/product-detail/{c}.html" target="_blank" rel="noopener">{c}</a></td><td class="n">{q}</td><td class="n">{st}</td><td class="n">{pr:.4f} <span class="note">{tier}</span></td></tr>')
        o.append("</tbody></table></div></section>")
    o.append(links() + """<script>
const K='tank-bom-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const rows=[...document.querySelectorAll('tr[data-ref]')],cks=[...document.querySelectorAll('.ck')];
function money(){const b=Math.max(1,+document.getElementById('boards').value||1),inc=document.getElementById('hlk').checked;let s=0;
 rows.forEach(r=>{const off=r.dataset.opt==='1'&&!inc;r.style.opacity=off?'.3':'';if(!off)s+=+r.dataset.sub});document.getElementById('cost').textContent='$'+(s*b).toFixed(2)}
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('ticked').textContent=Math.round(100*n/cks.length)+'%';document.getElementById('pbar').style.width=(100*n/cks.length)+'%';
 rows.forEach(r=>r.classList.toggle('done',r.querySelector('.ck').checked));try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});
document.getElementById('reset').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};
document.getElementById('boards').oninput=money;document.getElementById('hlk').onchange=money;
document.getElementById('q').oninput=ev=>{const v=ev.target.value.toLowerCase();rows.forEach(r=>r.style.display=r.innerText.toLowerCase().includes(v)?'':'none')};
document.getElementById('copy').onclick=()=>{const b=Math.max(1,+document.getElementById('boards').value||1),inc=document.getElementById('hlk').checked,m={};
 rows.forEach(r=>{if(r.dataset.opt==='1'&&!inc)return;m[r.dataset.c]=(m[r.dataset.c]||0)+(+r.dataset.q)*b});
 const t=Object.entries(m).map(([c,q])=>c+','+q).join('\\n');const btn=document.getElementById('copy');
 (navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>{btn.textContent='Copied '+Object.keys(m).length+' lines (C#,qty)'},()=>{prompt('Copy:',t)})};
upd();money();
</script></div></body></html>""")
    return "".join(o)



ASBUILT = [
 ("J1", "DC jack", "1 tip (+5 V in), 2 sleeve (GND), 3 switch pin not used"),
 ("J10", "5 V terminal", "<b>1 = GND, 2 = +5 V</b> (the drawings show the reverse: follow this table and put + / - on the silkscreen)"),
 ("J2", "ultrasonic header", "<b>1 = GND, 2 = ECHO, 3 = TRIG, 4 = +5 V</b> (reverse of the drawings)"),
 ("J3", "float switch", "<b>1 = GND, 2 = FLOAT1_T</b> (either wire order works)"),
 ("J4", "probes", "<b>1 = 40 %, 2 = 20 %, 3 = COM</b>"),
 ("J8", "probes", "<b>1 = FULL, 2 = 80 %, 3 = 60 %</b>"),
 ("J11", "LDR", "<b>1 = GND, 2 = LDR_T</b> (either wire order works)"),
 ("J12", "DHT11", "<b>1 = GND, 2 = DATA, 3 = +3V3</b>: check your DHT11 board order before plugging it in"),
 ("J6", "expansion (not fitted)", "<b>1 = IO2 (DHT), 2 = GND, 3 = +3V3, 4 = +5 V</b>"),
 ("J9", "AC in (option)", "<b>1 = N, 2 = L</b> (L goes to fuse F2)"),
 ("U8", "HLK-5M05", "1 = AC after fuse (AC_LF), 2 = N, 3 = -Vo (GND), 4 = +Vo"),
]
ASBUILT_HTML = (
    '<section class="card" style="--c:#0f766e"><h2>As-built pin order (read from your EasyEDA schematic, 2026-11-06)</h2>'
    '<p class="mut">Your schematic uses the <b>reverse pin order</b> on most connectors compared with the drawings on this site. Everything is electrically correct: it only matters when you crimp cables and print the silkscreen. Use this table for the cables.</p>'
    '<div class="scroll"><table><thead><tr><th>Part</th><th>What</th><th>Pin order in your schematic / PCB</th></tr></thead><tbody>'
    + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in ASBUILT)
    + '</tbody></table></div>'
    '<div class="warn"><b>Checks found in your schematic:</b> (1) <b>RV1 (varistor 10D561K) is missing</b>: the HLK-5M05 data sheet asks for it across L and N after the fuse; add it if you fit the HLK block. '
    '(2) The four USB-C shell pins (J5 pins 1 to 4) are not connected: connect them to GND. '
    '(3) Check the polarity of the LEDs and diodes against the silkscreen when you place the parts (pin 1 is the cathode in your wiring). '
    '(4) F2 is placed but the two fuse clips (C3131) are not in the schematic: add them or use a fuse holder.</div></section>')

EXTERNAL = [
 ("5 V in (J1, J10 or J5)", "Regulated <b>5 V only</b>. Use <b>one</b> of: J1 DC jack 5.5 / 2.1 mm (centre +), J10 2-pin screw terminal (pin 1 = +5 V, pin 2 = GND) or USB-C J5. The PTC F1 limits to about 0.5 A on J1 / J10. Never 12 V."),
 ("Optional mains (J9, HLK block)", "L and N from a breaker, strain-relieved, in an IP65 box, away from the probe wiring. Leave the whole HLK block off unless an engineer has reviewed it. Mains is near water here."),
 ("Ultrasonic (J2)", "Pin 1 +5 V, pin 2 TRIG, pin 3 ECHO, pin 4 GND (JSN-SR04T: match your module's labels). ECHO is divided to 3.3 V on the board."),
 ("Float switch (J3)", "Two wires, either way round, dry contact only (never mains or the pump contactor on the same wires). One float input only."),
 ("Probes (J4 + J8)", "J4: 1 COM, 2 = 20 %, 3 = 40 %. J8: 1 = 60 %, 2 = 80 %, 3 = FULL. With the 5-probe kit use COM + 4 levels and leave one terminal empty. Wire COM to the longest probe."),
 ("LDR (J11)", "Two wires to an LDR, either way round, up to a few metres of cable."),
 ("DHT11 (J12)", "Pin 1 +3V3, pin 2 DATA, pin 3 GND. Check your DHT11 board's pin order first."),
 ("Expansion (J6, not fitted)", "Pin 1 +5 V, pin 2 +3V3, pin 3 GND, pin 4 IO2 (shared with the DHT11 line)."),
 ("USB-C (J5)", "Programming, logs and 5 V. Native USB, no USB-UART chip: hold BOOT while plugging in if the first flash fails."),
]


def page_wiring():
    o = [head("TankPilot - Wiring by section", HEAD_SUB.replace("LCSC listings read 2026-11-05 &middot; ", ""), "", "wiring-by-section.html")]
    o.append('<p class="legend"><span><i style="background:#e53935"></i>AC (optional HLK)</span><span><i style="background:#fb8c00"></i>5 V / VBUS</span><span><i style="background:#f4b400"></i>3.3 V</span><span><i style="background:#8a93a3"></i>GND</span><span><i style="background:#2fbf71"></i>sensor signals</span><span><i style="background:#ec407a"></i>probes</span><span><i style="background:#8e24aa"></i>USB</span><span><i style="background:#a66cff"></i>MCU control</span><span><i style="background:#00bcd4"></i>other nets</span></p>')
    o.append('<section class="card" style="--c:#1e3a8a"><h2>System wiring (connection map)</h2>' + map_body() + '</section>')
    o.append('<section class="card" style="--c:#dc2626"><h2>External wiring (what you connect by hand)</h2><div class="scroll"><table><thead><tr><th>Connection</th><th>How</th></tr></thead><tbody>'
             + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td></tr>" for a, b in EXTERNAL) + '</tbody></table></div></section>')
    o.append(ASBUILT_HTML)
    o.append('<div class="bar"><progress id="pg" value="0" max="1" style="width:240px"></progress><span id="pt" class="mut"></span><button class="ghost" id="rs">Clear ticks</button></div><p class="mut">Pin-to-net per section: each box is a part (dashed = optional); the flag on a pin is the net name, put the same net label in EasyEDA and the pins join. Hover a wire to highlight its net, click to mark it wired (saved in this browser).</p>')
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        o.append(f'<section class="card" id="{pid}" style="--c:{sheet_color(secs)}"><h2>{e(ptitle)}</h2>')
        for sid in secs:
            _, title, col, desc = D.SEC[sid]
            o.append(f'<div data-sec="{sid}" class="sec"><h3 style="color:{col}">{e(title)} <span class="mut secprog"></span></h3><p class="mut">{e(desc)}</p><div class="scroll">{section_svg(sid)}</div></div>')
        o.append("</section>")
    o.append(links() + """<script>
const K='tank-wiring-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const svgs=[...document.querySelectorAll('svg.dia')];
function nets(svg){return [...new Set([...svg.querySelectorAll('.w[data-net]')].map(w=>w.dataset.net))]}
function apply(){let done=0,total=0;svgs.forEach(svg=>{const sid=svg.dataset.sec,ns=nets(svg);let d=0;
 svg.querySelectorAll('.w[data-net]').forEach(w=>w.classList.toggle('done',!!st[sid+'|'+w.dataset.net]));ns.forEach(n=>{if(st[sid+'|'+n])d++});
 svg.closest('.sec').querySelector('.secprog').textContent=d+' / '+ns.length+' nets wired';done+=d;total+=ns.length});
 document.getElementById('pg').max=total;document.getElementById('pg').value=done;document.getElementById('pt').textContent=done+' / '+total+' nets wired';try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
svgs.forEach(svg=>{const sid=svg.dataset.sec;svg.querySelectorAll('.w[data-net]').forEach(w=>{
 w.addEventListener('mouseenter',()=>{svg.classList.add('hl');svg.querySelectorAll('.w[data-net="'+w.dataset.net+'"]').forEach(x=>x.classList.add('on'))});
 w.addEventListener('mouseleave',()=>{svg.classList.remove('hl');svg.querySelectorAll('.w.on').forEach(x=>x.classList.remove('on'))});
 w.addEventListener('click',()=>{const k=sid+'|'+w.dataset.net;if(st[k])delete st[k];else st[k]=1;apply()})})});
document.getElementById('rs').onclick=()=>{if(confirm('Clear all net ticks?')){st={};apply()}};apply();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ connection map
def box(x, y, w, h, col, title, lines, dash=False):
    d = ' stroke-dasharray="7 5"' if dash else ""
    s = f'<g><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{col}" fill-opacity=".09" stroke="{col}" stroke-width="2"{d}/><rect x="{x}" y="{y}" width="{w}" height="26" rx="12" fill="{col}" fill-opacity=".9"/><text x="{x+12}" y="{y+18}" font-size="13" font-weight="700" fill="#fff">{e(title)}</text>'
    for i, l in enumerate(lines):
        s += f'<text x="{x+12}" y="{y+46+i*17}" font-size="12" fill="currentColor">{e(l)}</text>'
    return s + "</g>"


def arrow(pts, col, label="", dashed=False, lx=None, ly=None):
    d = " ".join(("M" if i == 0 else "L") + f"{a},{b}" for i, (a, b) in enumerate(pts))
    dd = ' stroke-dasharray="7 5"' if dashed else ""
    mid = pts[len(pts) // 2]
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="3"{dd} marker-end="url(#ah{col[1:]})"/>'
    if label:
        s += f'<text x="{lx if lx is not None else mid[0]+6}" y="{ly if ly is not None else mid[1]-6}" font-size="11" font-weight="700" fill="{col}">{e(label)}</text>'
    return s


def map_body():
    cols = ["#fb8c00", "#f4b400", "#2fbf71", "#ec407a", "#8e24aa", "#e53935", "#00bcd4"]
    s = ['<svg viewBox="0 0 1240 700" width="1240" class="dia" style="color:var(--fg)"><defs>']
    for c in cols:
        s.append(f'<marker id="ah{c[1:]}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>')
    s.append("</defs>")
    s.append(box(20, 20, 330, 150, "#ff9f43", "5 V INPUTS (use any one)", ["J1 DC jack 5.5/2.1 mm  or J10 2-pin terminal", "F1 PTC 0.5 A + D1 TVS, D2 Schottky", "J5 USB-C (VBUS) + D3 Schottky", "D4 Schottky from the HLK module (option)"]))
    s.append(box(20, 210, 330, 130, "#ff4d4d", "HLK 230 V OPTION (leave off if unsure)", ["J9 AC in (L, N)", "F2 fuse 0.5 A + RV1 varistor", "U8 HLK-5M05  230 V AC -> 5 V 1 A", "isolation slot to the low-voltage side"], dash=True))
    s.append(box(420, 20, 330, 150, "#ff9f43", "+5 V RAIL AND 3.3 V", ["C1 470 uF bulk, C2 / C5 decoupling", "U2 AP2112K-3.3 LDO", "+3V3 to the ESP32 and the sensor ports", "LED1 power LED"]))
    s.append(box(420, 210, 330, 190, "#a66cff", "ESP32-C3 CORE", ["U1 ESP32-C3-MINI-1-N4 (PCB antenna)", "SW1 EN reset, SW2 BOOT / PAIR", "LED2 status (GPIO8), J6 expansion", "GPIO10, 1, 3, 5, 6 = probes 20..FULL", "GPIO4 = probe COM, GPIO7 = float", "GPIO0 = LDR (ADC), GPIO2 = DHT11", "GPIO21 TRIG, GPIO20 ECHO"]))
    s.append(box(820, 20, 400, 150, "#8e24aa", "USB-C PROGRAMMING (J5)", ["native USB: GPIO18 D-, GPIO19 D+", "U3 USBLC6 ESD, R1 / R2 5.1 k on CC1 / CC2", "flash, logs, 5 V power", "no USB-UART chip"]))
    s.append(box(820, 210, 400, 120, "#2fbf71", "ULTRASONIC (J2)", ["+5V, TRIG, ECHO (5 V), GND", "R15 1 k + R16 2 k divider on ECHO", "JSN-SR04T / HC-SR04 / A02YYUW"]))
    s.append(box(820, 360, 400, 130, "#00bcd4", "FLOAT SWITCH (J3)", ["dry contact to GND, 3 m cable ok", "R8 1 k, R4 10 k pull-up, C12 100 nF", "U4 ESD (clamps to 3.3 V)", "LDR J11 (GPIO0) and DHT11 J12 (GPIO2) are on sheet 3"]))
    s.append(box(420, 450, 800, 220, "#ec407a", "PROBES (J4 + J8): COM + 20 %, 40 %, 60 %, 80 %, FULL", ["GPIO4 PROBE_COM -> C11 1 uF -> J4 COM (AC only, no DC in the water)", "five probe wires -> R10..R14 1 k -> GPIO10, GPIO1, GPIO3, GPIO5, GPIO6", "R17..R21 470 k pull-downs: a wet probe follows the AC burst, a dry one stays low", "no ESD parts on the probe lines (1 k series resistors only)", "level = highest wet probe (20 / 40 / 60 / 80 / FULL)"]))
    s.append(arrow([(350, 95), (420, 95)], cols[0], "+5V", lx=358, ly=88))
    s.append(arrow([(350, 270), (385, 270), (385, 140), (420, 140)], cols[5], "+5V_HLK", lx=360, ly=262))
    s.append(arrow([(585, 170), (585, 210)], cols[1], "+3V3", lx=592, ly=196))
    s.append(arrow([(820, 100), (750, 100)], cols[4], "VBUS", lx=760, ly=94))
    s.append(arrow([(985, 170), (985, 190), (790, 190), (790, 260), (750, 260)], cols[4], "D+ D-", lx=800, ly=250))
    s.append(arrow([(820, 270), (750, 270)], cols[2], "TRIG / ECHO", lx=752, ly=262))
    s.append(arrow([(820, 420), (790, 420), (790, 300), (750, 300)], cols[2], "FLOAT1", lx=752, ly=316))
    s.append(arrow([(585, 450), (585, 400)], cols[3], "PROBE_*", lx=592, ly=432))
    s.append("</svg>")
    leg = '<p class="legend"><span><i style="background:#fb8c00"></i>5 V</span><span><i style="background:#f4b400"></i>3.3 V</span><span><i style="background:#2fbf71"></i>ultrasonic / float signals</span><span><i style="background:#ec407a"></i>probes</span><span><i style="background:#8e24aa"></i>USB</span><span><i style="background:#e53935"></i>230 V option</span></p>'
    gp = [("10", "PROBE_20", "J4 pin 2 via R10 / R17"), ("1", "PROBE_40", "J4 pin 3 via R11 / R18"), ("3", "PROBE_60", "J8 pin 1 via R12 / R19"), ("5", "PROBE_80", "J8 pin 2 via R13 / R20"), ("6", "PROBE_FULL", "J8 pin 3 via R14 / R21"),
          ("4", "PROBE_COM", "C11 to J4 pin 1"), ("7", "FLOAT1", "J3 via R8, R4"), ("2", "DHT", "J12 pin 2, R23 10 k pull-up; also J6 pin 4"), ("21", "US_TRIG", "J2 pin 2 (TXD0)"), ("20", "US_ECHO", "J2 pin 3 via R15 / R16 (RXD0)"),
          ("8", "LED_ST", "LED2 via R7"), ("9", "BOOT / PAIR", "SW2"), ("18 / 19", "USB D- / D+", "J5 via U3"), ("0", "LDR (ADC)", "J11 via R24, R22 divider, C15"), ("EN", "EN", "SW1, R3, C8")]
    tab = "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td></tr>" for a, b, c in gp)
    return (leg + f'<div class="scroll" style="background:var(--card);border-radius:12px;padding:8px">{"".join(s)}</div>'
            f'<h3>GPIO assignment (ESP32-C3-MINI-1)</h3><div class="scroll"><table><thead><tr><th>GPIO</th><th>Net</th><th>Goes to</th></tr></thead><tbody>{tab}</tbody></table></div><p class="mut">GPIO11 to 17 belong to the module flash; GPIO2, 8, 9 are strapping pins (2 = DHT11 line, idles high with its 10 k pull-up; 8 = LED only; 9 = BOOT).</p>')


# ------------------------------------------------------------------ schematic guide
PAGE_STEPS = {
 "p1": [
  ("J1 DC jack: pin 1 (tip, +) to net <b>DC_IN</b>, pin 2 (sleeve, -) to GND. Add F1 (PTC) from DC_IN to <b>DC_F</b>, D1 TVS from DC_F to GND (cathode at DC_F). <b>J10</b> (2-pin screw terminal, +5 V and GND) joins the same nets as J1: pin 1 to DC_IN, pin 2 to GND; use J1 or J10, not both at once.", "power"),
  ("D2: anode DC_F, cathode <b>+5V</b>. D3: anode <b>VBUS</b>, cathode +5V. C1 470 uF (+ to +5V), C2 and C5 on +5V to GND.", "power"),
  ("U2 AP2112K: VIN and EN to +5V, GND to GND, VOUT to <b>+3V3</b>; C3 10 uF on +3V3. Check the symbol pin order (VIN 1, GND 2, EN 3, NC 4, VOUT 5).", "power"),
  ("OPTIONAL HLK block: J9 L and N to nets AC_L and AC_N; F2 from AC_L to <b>AC_LF</b> (F2H = its two clips); RV1 across AC_LF and AC_N; U8 AC pins to AC_LF / AC_N, +Vo to <b>+5V_HLK</b>, -Vo to GND; D4 from +5V_HLK to +5V; C6 on +5V_HLK. Draw a MAINS WARNING box around AC_L / AC_N / AC_LF.", "hlk"),
  ("J5 USB-C: VBUS pins (A4B9, B4A9) to VBUS, GND pins and EH1-4 to GND, A5 CC1 to R1 (5.1 k) to GND, B5 CC2 to R2 to GND, SBU1 / SBU2 no-connect.", "usb"),
  ("D+ pins A6 and B6 joined = <b>USB_DP_J</b>, D- pins A7 and B7 joined = <b>USB_DN_J</b>. U3 USBLC6: pin 1 USB_DP_J, pin 6 USB_DP, pin 3 USB_DN_J, pin 4 USB_DN, pin 5 VBUS, pin 2 GND. C7 on VBUS.", "usb"),
 ],
 "p2": [
  ("Place U1 ESP32-C3-MINI-1-N4 (C2838502). Pins 1, 2, 11, 14 and the pad pins 36-53 to GND, pin 3 to +3V3. Add C4 10 uF and C9, C10 100 nF on +3V3.", "mcu"),
  ("EN (pin 8): R3 10 k to +3V3, C8 100 nF to GND, SW1 to GND. BOOT: SW2 from net <b>BOOT</b> (pin 23, GPIO9) to GND. Tact switch pins 1+2 are joined, 3+4 are joined: use pin 1 and pin 3.", "mcu"),
  ("USB: pin 26 (IO18) to <b>USB_DN</b>, pin 27 (IO19) to <b>USB_DP</b> (sheet 1).", "mcu"),
  ("Net labels on the sensor pins: pin 16 IO10 <b>PROBE_20</b>, pin 13 IO1 <b>PROBE_40</b>, pin 6 IO3 <b>PROBE_60</b>, pin 19 IO5 <b>PROBE_80</b>, pin 20 IO6 <b>PROBE_FULL</b>, pin 18 IO4 <b>PROBE_COM</b>, pin 21 IO7 <b>FLOAT1</b>, pin 5 IO2 <b>DHT</b>, pin 12 IO0 <b>LDR</b>, pin 30 (RXD0, IO20) <b>US_ECHO</b>, pin 31 (TXD0, IO21) <b>US_TRIG</b>.", "mcu"),
  ("LED_ST: pin 22 (IO8) to R7 1 k to LED2 (green) to GND. LED1 (red) with R6 1 k from +3V3 to GND (power LED). DHT: pin 5 (IO2) also to J6 pin 4; J6 pins 1 +5V, 2 +3V3, 3 GND (not fitted by default).", "mcu"),
  ("Leave the NC pins (4, 7, 9, 10, 15, 17, 24, 25, 28, 29, 32-35) unconnected with No-Connect flags. Nothing except SW2 on GPIO9.", "mcu"),
 ],
 "p3": [
  ("<b>Ultrasonic J2</b>: pin 1 +5V (C14 100 nF to GND), pin 2 TRIG to net US_TRIG, pin 3 ECHO to net <b>ECHO_5V</b>, pin 4 GND. R15 1 k from ECHO_5V to <b>US_ECHO</b>, R16 2 k from US_ECHO to GND (5 V to 3.3 V divider).", "ultra"),
  ("<b>Float J3</b>: pin 1 to <b>FLOAT1_T</b>, pin 2 to GND. R8 1 k from FLOAT1_T to FLOAT1; R4 10 k from +3V3 to FLOAT1; C12 100 nF from FLOAT1 to GND. U4 USBLC6: pins 1+6 FLOAT1_T, pins 3 and 4 no-connect, pin 5 +3V3, pin 2 GND.", "floats"),
  ("<b>Probes J4 + J8</b>: J4 pin 1 COM = <b>PROBE_COM_T</b>, pin 2 = PROBE_20_T, pin 3 = PROBE_40_T; J8 pin 1 = PROBE_60_T, pin 2 = PROBE_80_T, pin 3 = PROBE_FULL_T. C11 1 uF from PROBE_COM to PROBE_COM_T (blocks DC).", "probes"),
  ("Each probe line: 1 k series (R10 to R14) from PROBE_xx_T to PROBE_xx, then 470 k (R17 to R21) from PROBE_xx to GND.", "probes"),
  ("<b>LDR J11</b> (2-pin terminal for an LDR on a cable): pin 1 = <b>LDR_T</b>, pin 2 = GND. R24 1 k from LDR_T to net <b>LDR</b>; R22 10 k from +3V3 to LDR; C15 100 nF from LDR to GND. LDR goes to GPIO0 (ADC1 channel 0, not a strapping pin). Dark = high voltage, bright = low (invert in firmware).", "sens"),
  ("<b>DHT11 J12</b> (1x3 header): pin 1 +3V3, pin 2 DATA = net <b>DHT</b> (to GPIO2: a strapping pin that must be high at reset; the DHT11 idles high through R23, so it is safe), pin 3 GND. R23 10 k from +3V3 to DHT. <b>Check the pin order of your DHT11 board</b>: bare sensors are VCC, DATA, NC, GND; 3-pin modules are often DATA, VCC, GND or VCC, DATA, GND.", "sens"),
 ],
}
PAGE_NOTES = {
 "p1": ["Nets leaving this page: +5V, +3V3, VBUS, GND, USB_DP, USB_DN, +5V_HLK. AC_L / AC_N / AC_LF stay on this page only.", "Diode orientation: the bar (cathode) is on the +5V side of D2, D3, D4 and at DC_F for D1."],
 "p2": ["Every GPIO net label here must appear again on sheet 3 (or sheet 1 for USB). Single-use labels are typos.", "Antenna end of the module: nothing above it on the PCB (see the layout guide)."],
 "p3": ["Terminal-side nets end in _T so the pull-ups and series resistors sit between the cable and the GPIO.", "The probe circuit is an untested design idea: keep the resistor footprints so values can be changed on the bench."],
}
SETUP = ["Open EasyEDA Pro (web), new project TankPilot with one schematic and one PCB.", "Make 3 schematic sheets named as above (page names 1_POWER_USB, 2_MCU, 3_SENSORS).",
         "Place parts by searching the LCSC number (C#) in the library search; set the Designator to the Ref in the table.", "Use net labels for every connection that leaves a page; use the same name on both pages. Names are case-sensitive.",
         "Mark optional parts (HLK block, J6) with the Not-in-BOM attribute when you do not fit them.", "Run the schematic check after each page and fix every warning."]
FINAL = ["Every net label is used at least twice. One GND, one +5V, one +3V3. AC_* nets exist only if you fit the HLK block.", "Compare the part count with the BOM page (%d pieces, optional parts included)." % D.TOTAL_PIECES,
         "Compare every footprint with its datasheet before the layout: C165948 USB-C, DC-005 jack (centre pin), ESP32-C3-MINI-1, KF128 terminals, SOT-25 LDO.", "Export the schematic PDF and send it for a check."]


def sheet_parts_table(secs):
    groups, order = {}, []
    for ref, s, name, c, q, pins in D.PARTS:
        if s in secs:
            if c not in groups:
                groups[c] = [[], 0, name]
                order.append(c)
            groups[c][0].append(ref)
            groups[c][1] += q
    body = ""
    for c in order:
        refs, q, name = groups[c]
        mpn = D.INFO[c][0]
        fn = name if len(refs) == 1 else " / ".join(dict.fromkeys(D.BYREF[r][2].split(",")[0] for r in refs))
        opt = ' <span class="tag opt">optional</span>' if all(r in D.OPTIONAL or D.BYREF[r][1] == "hlk" for r in refs) else ""
        body += (f'<tr><td><b>{e(", ".join(refs))}</b></td><td class="n">{q}</td><td>{e(fn)}{opt}</td><td><span class="mpn">{e(mpn)}</span></td>'
                 f'<td><a href="https://www.lcsc.com/product-detail/{c}.html" target="_blank" rel="noopener">{c}</a></td></tr>')
    return f'<div class="scroll"><table><thead><tr><th>Ref</th><th>Qty</th><th>Function</th><th>Part</th><th>LCSC</th></tr></thead><tbody>{body}</tbody></table></div>'


def page_schem():
    total = len(D.PARTS) + sum(len(v) for v in PAGE_STEPS.values()) + len(SETUP) + len(FINAL)
    o = [head("TankPilot - Schematic by section", "Three sheets, simplified symbols, with the parts of each sheet; the same Sheet 1, 2, 3 as on the BOM and Wiring pages. Draw the real schematic in EasyEDA.",
              "", "schematic-sections.html")]
    o.append('<p class="mut">Jump to: <a href="#u1pins">U1 pin guide (with No-Connect flags)</a> &middot; <a href="#esdpins">U3 and U4 ESD pin guide</a></p><div class="warn"><b>Planning drawing.</b> Symbols are simplified: draw the real schematic in EasyEDA from this page and the Wiring page. Check all pin numbers in the EasyEDA symbols (the module pin numbers p1 to p36 are from the ESP32-C3-MINI-1 datasheet v1.7).</div>')
    o.append('<p class="legend"><span><i style="background:#e53935"></i>AC mains</span><span><i style="background:#fb8c00"></i>5 V</span><span><i style="background:#f4b400"></i>3.3 V</span><span><i style="background:#8a93a3"></i>GND</span><span><i style="background:#a66cff"></i>MCU control</span><span><i style="background:#8e24aa"></i>USB</span><span><i style="background:#16a34a"></i>ultrasonic</span><span><i style="background:#00bcd4"></i>float</span><span><i style="background:#ec407a"></i>probes</span><span><i style="background:#8bc34a"></i>LDR / DHT11</span></p>')
    o.append(f'<div class="bar"><progress id="pg" value="0" max="{total}" style="width:240px"></progress><span id="pt" class="mut"></span><button class="ghost" id="rs">Clear ticks</button></div>')
    o.append('<section class="card" id="setup" style="--c:#475569"><h2>Setup in EasyEDA</h2>' + "".join(f'<div class="step"><input type="checkbox" class="ck" data-k="setup{i}"><span><b>{i}.</b> {e(s)}</span></div>' for i, s in enumerate(SETUP, 1)) + "</section>")
    for n, (pid, ptitle, secs) in enumerate(D.PAGES, 1):
        col = D.SEC[secs[0]][2]
        o.append(f'<section class="card" id="{pid}" style="--c:{col}"><h2>{e(ptitle)}</h2><div class="scroll">{SH.SHEETS[pid]()}</div>')
        for tx in PAGE_NOTES[pid]:
            o.append(f'<p class="mut">{e(tx)}</p>')
        o.append('<h3>Parts of this sheet</h3>' + sheet_parts_table(secs))
        o.append('<details><summary><b>Build steps</b> (tick as you draw this sheet)</summary>')
        for i, (txt, sec) in enumerate(PAGE_STEPS[pid], 1):
            o.append(f'<div class="step"><input type="checkbox" class="ck" data-k="{pid}-s{i}"><span><b>{i}.</b> {txt}</span></div>')
        o.append("</details></section>")
    o.append('<section class="card" id="u1pins" style="--c:#7c3aed"><h2>Pin guide: U1 ESP32-C3-MINI-1 (all 53 pads)</h2>'
             '<p class="mut">Top view exactly as the footprint: antenna at the top, pads 1 to 11 down the left, 12 to 24 along the bottom, 25 to 35 up the right, pads 36 to 48 along the top and the centre pad 49. '
             'Coloured line = wire or net label to put on the pin; <b style="color:#dc2626">red X = place a No-Connect flag</b>. Pin names and numbers are from the Espressif data sheet v1.7 (checked against its pin-layout figure).</p>'
             '<h3>1. Symbol view (the symbol you have in EasyEDA: pins 1 to 26 on the left, 53 down to 27 on the right)</h3><div class="scroll">' + PG.u1_symbol_svg() + '</div><p class="mut">"ok" = matches your schematic screenshot of 2026-11-06. <b style="color:#ea580c">TODO</b> = still to be wired: pin 31 (TXD0) = US_TRIG and pin 30 (RXD0) = US_ECHO.</p><h3>2. Footprint view (as the pads sit on the PCB)</h3><div class="scroll">' + PG.u1_svg() + '</div><h3>3. What to do on each pin</h3>' + PG.u1_table() +
             '<div class="warn"><b>GPIO2 (pin 5)</b> is a strapping pin and must be high at reset (data sheet table 6), so it carries the DHT11 line, which idles high through R23. The LDR is on GPIO0 (pin 12), which is not a strapping pin. GPIO8 (pin 22, status LED) and GPIO9 (pin 23, BOOT) are the other strapping pins: for USB download mode hold SW2 (BOOT) while pressing SW1 (EN).</div></section>')
    o.append('<section class="card" id="esdpins" style="--c:#8e24aa"><h2>Pin guide: USBLC6-2SC6 (C7519) for U3 and U4</h2>' + PG.esd_html() + '</section>')
    o.append('<section class="card" id="final" style="--c:#10b981"><h2>Final checks</h2>' + "".join(f'<div class="step"><input type="checkbox" class="ck" data-k="final{i}"><span><b>{i}.</b> {e(s)}</span></div>' for i, s in enumerate(FINAL, 1)) + "</section>")
    o.append(links() + """<script>
const K='tank-schem-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
const cks=[...document.querySelectorAll('.ck')];
function upd(){const n=cks.filter(c=>c.checked).length;document.getElementById('pg').value=n;document.getElementById('pt').textContent=n+' / '+cks.length+' done';cks.forEach(c=>{const r=c.closest('.step');if(r)r.classList.toggle('ok',c.checked)});try{localStorage.setItem(K,JSON.stringify(Object.fromEntries(cks.filter(c=>c.checked).map(c=>[c.dataset.k,1]))))}catch(e){}}
cks.forEach(c=>{c.checked=!!st[c.dataset.k];c.addEventListener('change',upd)});document.getElementById('rs').onclick=()=>{cks.forEach(c=>c.checked=false);upd()};upd();
</script></div></body></html>""")
    return "".join(o)


# ------------------------------------------------------------------ PCB guide

# ------------------------------------------------------------------ enclosure
ENC_OUT = (120.0, 80.0)
ENC_POST = 11.5       # corner screw post, square, measured from the outer wall (data-sheet drawing, approx.)
ENC_BOSS_X = 11.5     # mid-side boss reaches this far from the outer wall
ENC_BOSS_Y = (40.0, 4.5)   # boss centre height and half-height (approx.)
PCB_OFF = ((ENC_OUT[0] - PL.BOARD_W) / 2, (ENC_OUT[1] - PL.BOARD_H) / 2)


def enclosure_svg():
    W, H = ENC_OUT
    ox, oy = PCB_OFF
    o = [f'<svg viewBox="-6 -6 {W+12} {H+14}" width="720" class="plan" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">']
    o.append(f'<rect x="0" y="0" width="{W}" height="{H}" rx="3" fill="none" stroke="var(--ink)" stroke-width="0.5"/>')
    o.append(f'<rect x="2.6" y="2.6" width="{W-5.2}" height="{H-5.2}" rx="3" fill="var(--board)" stroke="var(--ink)" stroke-width="0.3"/>')
    for (cx, cy) in ((0, 0), (W - ENC_POST, 0), (0, H - ENC_POST), (W - ENC_POST, H - ENC_POST)):
        o.append(f'<rect x="{cx}" y="{cy}" width="{ENC_POST}" height="{ENC_POST}" rx="2" fill="#9aa5b5" fill-opacity=".55" stroke="#64748b" stroke-width="0.3"/>')
        o.append(f'<circle cx="{cx+ENC_POST/2 if cx == 0 else cx+ENC_POST/2}" cy="{cy+ENC_POST/2}" r="2.1" fill="var(--board)" stroke="#64748b" stroke-width="0.25"/>')
    for sx in (0, 1):
        bx = 0 if sx == 0 else W - ENC_BOSS_X
        o.append(f'<rect x="{bx}" y="{ENC_BOSS_Y[0]-ENC_BOSS_Y[1]}" width="{ENC_BOSS_X}" height="{2*ENC_BOSS_Y[1]}" rx="3" fill="#9aa5b5" fill-opacity=".55" stroke="#64748b" stroke-width="0.3"/>')
    o.append(f'<rect x="{ox}" y="{oy}" width="{PL.BOARD_W}" height="{PL.BOARD_H}" rx="3" fill="#2fbf71" fill-opacity=".18" stroke="#2fbf71" stroke-width="0.5"/>')
    o.append(f'<text x="{W/2}" y="{H/2+1}" text-anchor="middle" font-size="5" font-weight="700" fill="var(--ink)">PCB {PL.BOARD_W:.0f} x {PL.BOARD_H:.0f}</text>')
    o.append(f'<text x="{W/2}" y="{H+4.5}" text-anchor="middle" font-size="3.2" fill="var(--mute)">box 120 x 80 mm outside; grey = screw posts and bosses (approximate, from the data-sheet drawing); green = the PCB, centred</text>')
    o.append("</svg>")
    return "".join(o)


ENCL_HTML = (
    '<div class="rec"><b>Fit check.</b> The data sheet gives 120 x 80 mm outside and about 115 x 75 mm inside, but the four lid-screw posts (about 11.5 mm square) and two mid-side bosses (105 mm apart) reduce the free floor to about <b>96 x 75 mm</b>. '
    f'The board is <b>{PL.BOARD_W:.0f} x {PL.BOARD_H:.0f} mm</b>, so it fits with about 1 mm to the bosses and 2.5 mm top and bottom, and stays well under the 100 x 100 mm limit. '
    'A 100 mm wide board would NOT fit. Height inside is about 43 mm: the tallest parts (470 uF C1 about 12 mm, HLK module 18 mm, screw terminals about 10 mm) are fine.</div>'
    '<div class="scroll">' + enclosure_svg() + '</div>'
    '<ul class="rules"><li><b>Mounting:</b> the box has no documented PCB posts, so use 3 M3 standoffs on adhesive pads or a small mounting plate through the three holes of the board; confirm the real posts on the box before ordering the PCB.</li>'
    '<li><b>Cable entries (IP67):</b> drill the box for cable glands (PG7 / PG9): 5 V, ultrasonic, float, probes (one gland for the 6 wires), LDR and DHT11 cable. Keep the glands on the bottom edge next to the screw terminals J4, J8, J10, J11. Because the box is sealed, <b>use the J10 screw terminal for the 5 V supply</b>; the DC jack J1 and the USB-C J5 are only for use with the lid open.</li>'
    '<li><b>230 V option:</b> only with an engineer review; keep the mains gland and wiring away from the probe cables, and note the clear lid shows everything.</li>'
    '<li>The drawing file (.dwg, AutoCAD 2018) could not be opened on this PC; the numbers above come from the data-sheet image (120 / 80 / 55 mm, holes 111.5 x 71.5 mm, 105 mm between inner bosses, 43 mm inside height). Export the DWG as PDF or DXF if you want the exact inner shape checked.</li></ul>')

BW, BH = PL.BOARD_W, PL.BOARD_H
BLK = {b[0]: b for b in PL.BLOCKS}
REF_NAME = {p[0]: p[2] for p in D.PARTS}
REF_C = {p[0]: p[3] for p in D.PARTS}
BLOCK_NOTES = {
 "ultra": ["J2 on the top edge (cable goes up); R15 / R16 divider right next to the ECHO pin; C14 on the +5V pin."],
 "floats": ["J3 on the top edge, cable out to the top. Pull-up, series resistor, filter capacitor and the ESD part U4 sit directly under the terminal.", "Keep the float line short and away from the antenna side."],
 "dht": ["J12 3-pin header on the top edge (DHT11 plugs in or goes on a short cable); R23 pull-up just below it.", "Check the pin order of your DHT11 against J12 before ordering."],
 "vin": ["J10 2-pin screw terminal (+5 V, GND) for an external 5 V supply; silkscreen + and - and 5 V DC ONLY. Joins the DC jack net before the PTC fuse F1."],
 "ldr": ["J11 2-pin terminal for the LDR on a cable; R24, R22 and C15 right below it, close to each other.", "GPIO0 is the ADC input; keep the line short."],
 "hlk_ac": ["OPTIONAL: J9 (AC in), F2 fuse clips and RV1 on the mains side right of the slot, at least 6.4 mm from low-voltage copper. Leave all of it off if you power the board from 5 V."],
 "power": ["J1 DC jack on the left edge, then F1, D1 (TVS) and the Schottky diodes in a row to C1; U2 and its capacitors next to C1.", "Silkscreen: 5 V DC ONLY at the jack, + / - polarity mark."],
 "usb": ["J5 USB-C on the left edge, shield tabs to the edge. D+ / D- as a short pair straight through U3 to the ESP32; R1 / R2 at the CC pins."],
 "probes": ["J4 and J8 side by side on the bottom edge, cables down. Series resistors right above the terminals, pull-downs and the optional ESD parts above them; C11 next to the COM terminal.", "Keep these lines far from the antenna and from the 230 V option."],
 "mcu": ["U1 at the top right: antenna end to the top edge, nothing above it (no copper, no parts, no pour).", "SW1 / SW2 on the lower side, LEDs and decoupling around the module; C4 / C9 / C10 close to the 3V3 pin."],
 "exp": ["J6 optional 1x4 header on the top edge (5V, 3V3, GND, IO2 shared with the DHT11 line)."],
 "hlk_out": ["D4 and C6 just left of the HLK +5V pins, inside the low-voltage zone."],
 "hlk": ["OPTIONAL 230 V block: leave U8 off if you use a 5 V adapter or USB. U8 lies across the slot: AC pins at the right end, 5 V pins at the left end; check the real pin pitch.", "Mains is near water here: enclosure IP65 and an engineer review are required."],
}
NETS = [("AC_L, AC_N, AC_LF (option)", "1.0 mm min, 6.4 mm to low-voltage copper", "Mains side only, right of the slot."), ("+5V_HLK, +5V, DC_F", "0.8 mm", "Peak about 0.5 A."), ("+3V3", "0.6 mm", "ESP32-C3 bursts to about 0.35 A."),
        ("GND", "pour on both layers", "Low-voltage side only; no pour on the mains side or across the slot."), ("USB_DP / USB_DN", "0.2 mm pair, 90 ohm", "Short, no stubs."), ("PROBE_*, FLOAT*, US_*, others", "0.25 mm", "Plain signals; keep probe lines away from the antenna."),
        ("Isolation slot", "1.3 mm wide", "Routed slot; ends 3.2 mm past the mains copper (only needed if the HLK block is fitted).")]
STEPS = ["In EasyEDA PCB draw the outline " + f"{BW:.0f} x {BH:.0f}" + " mm, 3 mm corners, three 3.2 mm non-plated holes at " + ", ".join(f"({x:g},{y:g})" for x, y in PL.HOLES) + " mm, and (if you fit the HLK block) the slot x " + f"{PL.SLOT['x']:.1f} to {PL.SLOT['x']+PL.SLOT['w']:.1f}" + " mm, y " + f"{PL.SLOT['y0']:g} to {PL.SLOT['y1']:g}" + " mm.",
         "Import the schematic (Design > Update/Convert Schematic to PCB). Check every footprint against its datasheet first.", "Place block by block with the X / Y tables, ticking each part here.",
         "Draw one rectangle per block on the Top Silkscreen layer with its title (the dashed boxes).", "Draw the net classes from the table above, then pour GND on the low-voltage side.", "Route the HLK block (if fitted) and the USB pair first, then power, then sensors.",
         "Run DRC with a 6.4 mm clearance rule between mains and low-voltage nets. Add silkscreen: 5 V DC ONLY, MAINS WARNING, terminal pin names (COM, 20%, 40%, 60%, 80%, FULL, F, GND, 5V, TRIG, ECHO).", "Export Gerber and have the PCB maker check the slot and the spacing."]


def rect_of(v):
    x, y, w, h, r = v
    if r in (90, 270):
        w, h = h, w
    return x, y, w, h


def part_svg(ref, dim=False):
    x, y, w, h = rect_of(PL.L[ref])
    col = BLK[PL.REF_BLOCK[ref]][2]
    f = 1.5 if min(w, h) > 3.2 else 1.15
    rot = f' transform="rotate(-90 {x:.2f} {-y:.2f})"' if h > 1.6 * w and h > 9 else ""
    opt = ref in D.OPTIONAL
    return (f'<g class="pt" data-ref="{ref}" opacity="{".22" if dim else "1"}"><title>{e(ref)}: {e(REF_NAME[ref])} [{e(REF_C[ref])}] x={x:.1f} y={y:.1f} mm</title>'
            f'<rect x="{x-w/2:.2f}" y="{-(y+h/2):.2f}" width="{w:.2f}" height="{h:.2f}" rx="0.3" fill="{col}" fill-opacity=".30" stroke="{col}" stroke-width="0.22"{" stroke-dasharray=\"0.8 0.5\"" if opt else ""}/>'
            f'<text x="{x:.2f}" y="{-y+f/3:.2f}" text-anchor="middle" font-size="{f}" font-weight="700" fill="var(--fg)"{rot} style="pointer-events:none">{e(ref)}</text></g>')


def board_inner(full, active=None):
    o = [f'<rect x="0" y="{-BH}" width="{BW}" height="{BH}" rx="3" fill="var(--board)" stroke="var(--fg)" stroke-width="0.35"/>']
    for gx in range(10, int(BW), 10):
        o.append(f'<line x1="{gx}" y1="{-BH}" x2="{gx}" y2="0" stroke="var(--line)" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if full: o.append(f'<text x="{gx}" y="{-BH-0.8}" text-anchor="middle" font-size="1.4" fill="#5b6677">{gx}</text>')
    for gy in range(10, int(BH), 10):
        o.append(f'<line x1="0" y1="{-gy}" x2="{BW}" y2="{-gy}" stroke="var(--line)" stroke-width="0.08" stroke-dasharray="0.5 1"/>')
        if full: o.append(f'<text x="-0.8" y="{-gy+0.5}" text-anchor="end" font-size="1.4" fill="#5b6677">{gy}</text>')
    s = PL.SLOT
    o.append(f'<rect x="{s["x"]+s["w"]:.2f}" y="{-BH+0.15}" width="{BW-s["x"]-s["w"]-0.15:.2f}" height="{BH-0.3}" fill="#e53935" fill-opacity=".06"/>')
    o.append(f'<rect x="{s["x"]}" y="{-s["y1"]}" width="{s["w"]}" height="{s["y1"]-s["y0"]}" rx="0.65" fill="#b71c1c" opacity=".7"/>')
    for (hx, hy) in PL.HOLES:
        o.append(f'<circle cx="{hx}" cy="{-hy}" r="3.2" fill="none" stroke="#9aa5b5" stroke-width="0.2" stroke-dasharray="0.6 0.4"/><circle cx="{hx}" cy="{-hy}" r="1.6" fill="var(--board)" stroke="#9aa5b5" stroke-width="0.2"/>')
    for b in PL.BLOCKS:
        bx = b[4]
        dim = active is not None and b[0] != active
        tw = len(b[1]) * 0.95 + 1.2
        tx, ty = bx[0] + 1.6, -bx[3] + 0.5
        o.append(f'<g opacity="{".35" if dim else "1"}"><rect x="{bx[0]:.2f}" y="{-bx[3]:.2f}" width="{bx[2]-bx[0]:.2f}" height="{bx[3]-bx[1]:.2f}" rx="0.6" fill="none" stroke="{b[2]}" stroke-width="0.28" stroke-dasharray="1.2 0.7"/><rect x="{tx-0.5:.2f}" y="{ty-1.15:.2f}" width="{tw:.2f}" height="1.6" fill="var(--board)"/><text x="{tx:.2f}" y="{ty:.2f}" font-size="1.4" font-weight="700" fill="{b[2]}">{e(b[1])}</text></g>')
    for ref in PL.L:
        o.append(part_svg(ref, dim=(active is not None and PL.REF_BLOCK[ref] != active)))
    return "".join(o)


def board_svg(view=None, active=None, width_px=760):
    vx0, vy0, vx1, vy1 = view or (-3, -3, BW + 3, BH + 3)
    w, h = vx1 - vx0, vy1 - vy0
    return (f'<svg viewBox="{vx0:.2f} {-vy1:.2f} {w:.2f} {h:.2f}" width="{width_px:.0f}" height="{width_px*h/w:.0f}" class="plan" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif">{board_inner(view is None, active)}</svg>')


def parts_table(block):
    refs = sorted(block[3], key=lambda r: (r[0] != "U", r[0] != "J", r[0], int("".join(c for c in r if c.isdigit()) or 0)))
    t = '<div class="scroll"><table><thead><tr><th></th><th>Ref</th><th>Part</th><th>LCSC</th><th>X mm</th><th>Y mm</th><th>Rot</th><th>Size mm (est.)</th></tr></thead><tbody>'
    for r in refs:
        x, y, w, h, rot = PL.L[r]
        t += f'<tr data-ref="{r}"><td><input type="checkbox" class="ck" data-k="{r}"></td><td><b>{r}</b></td><td>{e(REF_NAME[r])}</td><td>{e(REF_C[r])}</td><td class="num">{x:.1f}</td><td class="num">{y:.1f}</td><td class="num">{rot}&deg;</td><td>{w:.1f} x {h:.1f}</td></tr>'
    return t + "</tbody></table></div>"


def page_pcb():
    total = len(PL.L)
    used = sum(v[2] * v[3] for v in PL.L.values())
    o = [head(f"TankPilot - PCB floorplan {PL.BOARD_W:.0f} x {PL.BOARD_H:.0f} mm", f"{PL.BOARD_W:.0f} x {PL.BOARD_H:.0f} mm, fits the 120 x 80 x 55 mm IP67 clear box, 2 layers. One zoomed drawing, one dashed silkscreen box and one X / Y table per block; tick each part as you place it in EasyEDA (saved in this browser).",
              '<div class="chips">' + '<a style="background:#607d8b" href="#size">Board size</a><a style="background:#607d8b" href="#plan">Floor plan</a>' + "".join(f'<a style="background:{b[2]}" href="#{b[0]}">{e(b[1])}</a>' for b in PL.BLOCKS) + f'<a style="background:#607d8b" href="#nets">Nets</a><a style="background:#607d8b" href="#steps">Steps</a><span class="mut">placed <b id="tot">0</b> / {total}</span><div class="pbar"><div id="barfill"></div></div><button class="ghost" id="reset">Reset ticks</button></div>', "pcb-floorplan.html")]
    o.append(f'<section class="card" id="size"><h2>Board size: {BW:.0f} x {BH:.0f} mm</h2><div class="rec"><b>2 layers, 1.6 mm FR-4, 1 oz copper, {BW:.0f} x {BH:.0f} mm, 3 mm corners, three M3 holes (3.2 mm, non-plated, no pad).</b> Parts add up to about {used:.0f} mm&sup2; of {BW*BH:.0f} mm&sup2; ({used/(BW*BH/100):.0f} %). The size is set by the optional 230 V block: the HLK-5M05 module alone is 38 x 23 mm and needs the fuse, varistor, AC terminal and a 6.4 mm slot. <b>Without the HLK block</b> the board shrinks to about 72 x 70 mm (nothing right of x 72 mm is needed). Both stay under 100 x 100 mm, the cheapest PCB price tier, and the full board fits the enclosure below.</div>'
             f'<h3>Outline, holes, slot</h3><div class="scroll"><table><thead><tr><th>Item</th><th>X mm</th><th>Y mm</th><th>Size</th></tr></thead><tbody><tr><td>Board outline</td><td class="num">0 - {BW:.0f}</td><td class="num">0 - {BH:.0f}</td><td>{BW:.0f} x {BH:.0f}, corner radius 3 mm</td></tr>'
             + "".join(f'<tr><td>MH{i} M3 hole</td><td class="num">{hx:.1f}</td><td class="num">{hy:.1f}</td><td>3.2 mm, non-plated, no pad</td></tr>' for i, (hx, hy) in enumerate(PL.HOLES, 1))
             + f'<tr><td>Isolation slot (HLK block only)</td><td class="num">{PL.SLOT["x"]:.1f} - {PL.SLOT["x"]+PL.SLOT["w"]:.1f}</td><td class="num">{PL.SLOT["y0"]:.0f} - {PL.SLOT["y1"]:.0f}</td><td>{PL.SLOT["w"]} mm wide, routed</td></tr></tbody></table></div>'
             '<h3>Enclosure: 120 x 80 x 55 mm IP67 transparent ABS box (IDIS SKU 10188)</h3>' + ENCL_HTML + '<h3>Edge plan</h3><ul class="rules"><li><b>Top edge:</b> J2 (ultrasonic), J3 (float), J12 (DHT11), J6 (expansion), antenna end of the ESP32-C3 module.</li><li><b>Left edge:</b> J1 (DC jack) and J5 (USB-C).</li><li><b>Bottom edge:</b> J4 and J8 (probe terminals, cables down).</li><li><b>Right side:</b> J10 (5 V terminal) and J11 (LDR) in the free low-voltage area, then the optional 230 V block with J9 (AC in) on the far right.</li></ul>'
             '<p class="mut">Silkscreen box per block: one dashed rectangle with its title on the Top Silkscreen layer (as in the BorePilot guide). The checker confirmed: no overlaps, no part outside its own box, no box touching a mounting hole or another box, 3.2 mm from low-voltage parts to the mains parts, and nothing above the antenna end.</p></section>')
    o.append('<section class="card" id="plan"><h2>Floor plan<span class="cnt">dashed boxes = silkscreen boxes; dashed part outlines = optional parts; click a part to tick it</span></h2><div class="scroll">' + board_svg() + '</div></section>')
    for b in PL.BLOCKS:
        bx = b[4]
        crop = (max(bx[0] - 3, -2), max(bx[1] - 3, -2), min(bx[2] + 3, BW + 2), min(bx[3] + 3, BH + 2))
        wpx = int(min(900, max(520, (crop[2] - crop[0]) * 14)))
        o.append(f'<section class="card" id="{b[0]}" style="--c:{b[2]}"><h2>{e(b[1])}<span class="cnt"><span class="done">0</span> / {len(b[3])} placed &middot; box x {bx[0]:.1f} to {bx[2]:.1f}, y {bx[1]:.1f} to {bx[3]:.1f} mm</span></h2><ul class="rules">' + "".join(f"<li>{e(t)}</li>" for t in BLOCK_NOTES[b[0]]) + f'</ul><div class="scroll">{board_svg(view=crop, active=b[0], width_px=wpx)}</div>{parts_table(b)}</section>')
    o.append('<section class="card" id="nets"><h2>Nets and trace widths<span class="cnt">1 oz copper, with margin</span></h2><div class="scroll"><table><thead><tr><th>Net</th><th>Width</th><th>Notes</th></tr></thead><tbody>' + "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in NETS) + '</tbody></table></div></section>')
    o.append('<section class="card" id="steps"><h2>Order of work</h2><ol class="steps">' + "".join(f"<li>{e(t)}</li>" for t in STEPS) + "</ol></section>" + links())
    o.append("""<script>
const K='tank-pcb-ticks';let st={};try{st=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
function apply(){const total=document.querySelectorAll('#plan .pt').length;document.querySelectorAll('.pt').forEach(g=>g.classList.toggle('ok',!!st[g.dataset.ref]));
 document.querySelectorAll('tr[data-ref]').forEach(r=>{const on=!!st[r.dataset.ref];r.classList.toggle('ok',on);r.querySelector('.ck').checked=on});
 const n=Object.keys(st).length;document.getElementById('tot').textContent=n;document.getElementById('barfill').style.width=(100*n/total)+'%';
 document.querySelectorAll('section.card[id]').forEach(sec=>{const rows=sec.querySelectorAll('tr[data-ref]');if(!rows.length)return;const d=[...rows].filter(r=>st[r.dataset.ref]).length;const c=sec.querySelector('.done');if(c)c.textContent=d});
 try{localStorage.setItem(K,JSON.stringify(st))}catch(e){}}
function tog(r){if(st[r])delete st[r];else st[r]=1;apply()}
document.querySelectorAll('.pt').forEach(g=>g.addEventListener('click',()=>tog(g.dataset.ref)));document.querySelectorAll('input.ck').forEach(c=>c.addEventListener('change',()=>tog(c.dataset.k)));
document.getElementById('reset').onclick=()=>{st={};apply()};apply();
</script></div></body></html>""")
    return "".join(o)


def standalone_svg():
    inner = board_inner(True).replace("var(--fg)", "#1c2330").replace("var(--board)", "#e8efe4").replace("var(--line)", "#c9d1dc")
    leg = "".join(f'<rect x="{-3 + (i % 5) * 21}" y="{4.6 + (i // 5) * 2.6:.1f}" width="1.6" height="1.6" fill="{b[2]}"/><text x="{-3 + (i % 5) * 21 + 2.2}" y="{5.9 + (i // 5) * 2.6:.1f}" font-size="1.35" fill="#1c2330">{e(b[1])}</text>' for i, b in enumerate(PL.BLOCKS))
    vh = BH + 16
    return (f'<svg viewBox="-3 {-(BH+5)} {BW+6} {vh}" width="1000" height="{1000*vh/(BW+6):.0f}" xmlns="http://www.w3.org/2000/svg" font-family="system-ui,Segoe UI,sans-serif"><rect x="-3" y="{-(BH+5)}" width="{BW+6}" height="{vh}" fill="#ffffff"/>'
            f'<text x="-2" y="{-(BH+2.5)}" font-size="2" font-weight="700" fill="#1c2330">TankPilot PCB floor plan - {PL.BOARD_W:.0f} x {PL.BOARD_H:.0f} mm, 2 layers, one silkscreen box per block (planning estimate)</text>{inner}{leg}</svg>')


def main():
    write_bom()
    for old in ("bom-by-section.html", "wiring-by-section.html", "connection-diagram.html", "schematic-guide.html", "pcb-section-guide.html", "page1-power.html", "page2-esp32-core.html", "page3-sensors.html"):
        f = os.path.join(DOCS, old)
        if os.path.exists(f) and old != "wiring-by-section.html":
            os.remove(f)
    open(os.path.join(DOCS, "bom.html"), "w", encoding="utf-8").write(page_bom())
    open(os.path.join(DOCS, "wiring-by-section.html"), "w", encoding="utf-8").write(page_wiring())
    open(os.path.join(DOCS, "schematic-sections.html"), "w", encoding="utf-8").write(page_schem())
    open(os.path.join(DOCS, "pcb-floorplan.html"), "w", encoding="utf-8").write(page_pcb())
    open(os.path.join(DOCS, "images", "pcb-floorplan.svg"), "w", encoding="utf-8").write(standalone_svg())
    open(os.path.join(ROOT, "hardware", "bom", "bom-table.md"), "w", encoding="utf-8").write(bom_md())
    pr = PL.check()
    print("pages written; layout problems:", len(pr), "; pieces", D.TOTAL_PIECES, "; totals", [round(x, 2) for x in D.totals()])


if __name__ == "__main__":
    main()
