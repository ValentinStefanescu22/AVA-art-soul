"""Final 2 (carte poștală) variants (Vali, 11 nov: more variants, try something darker; on the phone the contact list is left-aligned).
A  Final2CartePostala   the original: cream postcard on light sand (rebuilt by newsletter_options.py).
B  Final2BFundalInchis  cream postcard on a dark 'lut ars' band.
C  Final2CCardInchis    dark postcard on light sand.
D  Final2DTeracota      terracotta postcard on a dark 'lut ars' band.

usage: python3 .aidesigner/final2_options.py   (after newsletter_options.py)
"""
import os, subprocess, sys
from about_options2 import P, HERE
from newsletter_options import FINALS, page

TITLE, SRC, CSS, HTML = FINALS["Final2CartePostala"]

DARK_CARD = """
.{v} .card{{background:{card};color:{text}}}
.{v} .l{{border-color:{rule}}}
.{v} .five,.{v} .nf .ok{{color:{soft}}}
.{v} .sig,.{v} .seal,.{v} .nf .done{{color:{accent}}}
.{v} .nf .lbl{{color:{text}}}
.{v} .nf.line input[type=email]{{border-bottom-color:{line};color:{text}}}
.{v} .nf.line input[type=email]::placeholder{{color:{ph}}}
.{v} .nf.line input[type=email]:focus-visible{{border-bottom-color:{accent}}}
.{v} .btn{{background:#F4EDE4;color:#3A2A20}}.{v} .btn:hover{{background:#FFF8EE}}
.{v} .nf[data-err] .ok span{{color:{accent}}}
.{v} .btn:focus-visible,.{v} .nf .ok a:focus-visible{{outline-color:{accent}}}
@media (max-width:820px){{.{v} .l{{border-color:{rule}}}}}
"""
DARK_BAND = """
.{v}{{background:linear-gradient(180deg,#3A2A20 0%,#2E2119 100%)}}
.{v} .card{{box-shadow:0 50px 100px -50px rgba(0,0,0,.65)}}
.{v} .ct span{{color:#BFA992}}.{v} .ct a{{color:#F4EDE4}}
.{v} .ct a:focus-visible{{outline-color:#F2C79C}}
"""

V = {
    "Final2BFundalInchis": ("Final 2B: carte poștală pe fundal închis", DARK_BAND.format(v="vb")),
    "Final2CCardInchis": ("Final 2C: carte poștală închisă", DARK_CARD.format(
        v="vc", card="#3A2A20", text="#F4EDE4", rule="rgba(244,237,228,.18)", soft="#D9C7B4",
        accent="#F2C79C", line="rgba(244,237,228,.45)", ph="#A8927E")),
    "Final2DTeracota": ("Final 2D: carte poștală teracotă pe lut ars", DARK_BAND.format(v="vd") + DARK_CARD.format(
        v="vd", card="#9C472C", text="#FBF4EA", rule="rgba(251,244,234,.28)", soft="#FBEBDD",
        accent="#FBF4EA", line="rgba(251,244,234,.6)", ph="#F6E0D0")),
}
CLS = {"Final2BFundalInchis": "vb", "Final2CCardInchis": "vc", "Final2DTeracota": "vd"}

if __name__ == "__main__":
    for name, (title, css) in V.items():
        html = HTML.replace('class="nl n2"', f'class="nl n2 {CLS[name]}"').replace('id="nl-e2"', f'id="nl-{CLS[name]}"').replace('for="nl-e2"', f'for="nl-{CLS[name]}"').replace('id="sr2"', f'id="sr-{CLS[name]}"').replace('href="#sr2"', f'href="#sr-{CLS[name]}"')
        for suffix, w, h in (("", 1440, 820), ("Mobil", 390, 1100)):
            open(os.path.join(P, f"{name}{suffix}.dc.html"), "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), CSS + css, html, w, h))
        subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), os.path.join(P, f"{name}.dc.html"), os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = ["Final2CartePostala"] + list(V)
    open(os.path.join(HERE, "final2.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Final 2</title><style>body{margin:0}iframe{width:1440px;height:820px;border:0;display:block;border-bottom:8px solid #222}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "final2-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Final 2 mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:1100px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
