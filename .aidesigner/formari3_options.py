"""Pagina „Despre noi”, part 3: Formări, the quiet family (Vali, 11 nov, feedback from Alessia): Formări 3 as the base,
no icons, nothing that pulls the eye. Clean, readable, elegant. Four layouts of the same four lines.

usage: python3 .aidesigner/formari3_options.py
writes .aidesigner/canvas/project/Formari3A..3D*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Formari3*.html
Copy: formari_options.ITEMS (from docs/continut-site.md). Motion: only the site's scroll reveal (opacity + 16px rise,
800ms ease-out, 80ms apart), once; nothing hidden without JS or with reduced motion.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS
from formari_options import ITEMS
from cf_pagina_options import script

H2 = '<h2 class="disp" id="fm-h">Formări</h2>'
SOURCES = {
    "Formari3ADoua": "Formări 3 (airbnb.com, profilul gazdei), fără iconițe: două coloane",
    "Formari3BRand": "aesop.com: detaliile produsului în coloane, fiecare sub o linie fină",
    "Formari3CMargine": "Kinfolk (revista): titlul pe margine, textul în dreapta",
    "Formari3DCentrat": "Cereal (revista): text centrat, cu mult spațiu alb",
}

COMMON = """
.fq{position:relative;background:#F4EDE4;padding:112px 0 120px}
.fq h2{font-size:clamp(40px,4.2vw,60px);line-height:1.05}
.fq ul{margin:0;padding:0;list-style:none}
.fq .t{margin:0;font:400 22px/1.35 var(--display);font-variation-settings:'opsz' 20;color:var(--ink);text-wrap:pretty}
.fq .w{margin:8px 0 0;color:var(--ink2);font-size:16.5px;line-height:1.55}
.fq .yr{font-variant-numeric:tabular-nums;white-space:nowrap}
.fq .w .yr::before{content:"·";margin:0 8px}
@keyframes fq-up{from{opacity:0;translate:0 16px}}
.fq.js:not(.in) :is(h2,li){opacity:0}
.fq.js.in h2{animation:fq-up .8s cubic-bezier(.22,1,.36,1) backwards}
.fq.js.in li{animation:fq-up .8s cubic-bezier(.22,1,.36,1) backwards;animation-delay:calc(80ms + var(--i) * 80ms)}
@media (max-width:980px){.fq{padding:72px 0 80px}.fq .t{font-size:20px}.fq .w{font-size:16px}}
@media (prefers-reduced-motion:reduce){.fq *{animation:none!important}}
"""


def items(sep=True):
    return "".join(f'<li style="--i: {i}"><p class="t">{t}</p><p class="w">{w}<span class="yr">{d}</span></p></li>'
                   for i, (t, w, d, _) in enumerate(ITEMS))


OPTS = {}

# 3A. Formări 3 as it was, minus the icons: two columns, generous gaps, nothing else.
OPTS["Formari3ADoua"] = ("Formări 3A: două coloane, fără iconițe", """
.f3a h2{margin-bottom:48px}
.f3a ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:44px 72px}
@media (max-width:980px){.f3a h2{margin-bottom:32px}.f3a ul{grid-template-columns:1fr;gap:28px}}
""", '<section class="fq f3a" aria-labelledby="fm-h" ref="{{ secRef }}"><div class="wrap">' + H2 + f"<ul>{items()}</ul></div></section>")

# 3B. One row of four columns, each under a fine hairline (Aesop's product details); the year sits on its own line.
OPTS["Formari3BRand"] = ("Formări 3B: un rând, sub linii fine", """
.f3b h2{margin-bottom:48px}
.f3b ul{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 40px}
.f3b li{padding-top:22px;border-top:1px solid rgba(58,42,32,.22)}
.f3b .t{font-size:20px}
.f3b .w .yr{display:block;margin-top:2px}.f3b .w .yr::before{content:none}
@media (max-width:980px){.f3b h2{margin-bottom:28px}.f3b ul{grid-template-columns:1fr;gap:26px}.f3b li{padding-top:18px}}
""", '<section class="fq f3b" aria-labelledby="fm-h" ref="{{ secRef }}"><div class="wrap">' + H2 + f"<ul>{items()}</ul></div></section>")

# 3C. The title in a narrow left column, the four lines in a 2×2 grid on the right (a magazine spread's margin).
OPTS["Formari3CMargine"] = ("Formări 3C: titlul pe margine", """
.f3c .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,8fr);gap:0 64px;align-items:start}
.f3c ul{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:40px 56px;padding-top:10px}
@media (max-width:980px){.f3c .stage{grid-template-columns:1fr;gap:28px}.f3c ul{grid-template-columns:1fr;gap:28px;padding-top:0}}
""", '<section class="fq f3c" aria-labelledby="fm-h" ref="{{ secRef }}"><div class="wrap stage">' + H2 + f"<ul>{items()}</ul></div></section>")

# 3D. Centred, one line under another, a short hairline between them; lots of air (Cereal's quiet pages).
OPTS["Formari3DCentrat"] = ("Formări 3D: centrat", """
.f3d{text-align:center}
.f3d h2{margin-bottom:44px}
.f3d ul{max-width:640px;margin:0 auto}
.f3d li+li{margin-top:28px;padding-top:28px;background:linear-gradient(rgba(58,42,32,.25),rgba(58,42,32,.25)) 50% 0/40px 1px no-repeat}
.f3d .t{text-wrap:balance}
@media (max-width:980px){.f3d h2{margin-bottom:30px}.f3d li+li{margin-top:22px;padding-top:22px}}
""", '<section class="fq f3d" aria-labelledby="fm-h" ref="{{ secRef }}"><div class="wrap">' + H2 + f"<ul>{items()}</ul></div></section>")


def page(name, title, css, html, w, h):
    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
{BASE_CSS}{COMMON}{css}</style>
</helmet>
<div class="pg" data-src="{SOURCES[name]}">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{script()}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"Formari3ADoua": (544, 604), "Formari3BRand": (540, 777), "Formari3CMargine": (528, 600), "Formari3DCentrat": (790, 650)}

if __name__ == "__main__":
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "formari3-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Formari 3 mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1000px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
