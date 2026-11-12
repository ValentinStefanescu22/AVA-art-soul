"""'Ce oferim', round 2: four bolder ways to show the services. Placeholder photos from Unsplash
(public/images/placeholder/SURSE.txt), to be swapped for AVA's own after the photo shoot.

usage: python3 .aidesigner/ce_facem2_options.py
writes .aidesigner/canvas/project/CeFacem5..8*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-CeFacem*.html
References: hover-expanding image accordions and image-reveal service lists (Framer / Divi components), Awwwards
studio sites with scroll and pointer interaction; the vessel shelf is AVA's own (pottery silhouettes as photo frames).
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
from ce_facem_options import S as S1, SCOLI, HEAD_P, COMMON, meta, more

IMG = dict(grup="/_blob/70ad22aacebcba3dbca6580a21b45332", companii="/_blob/18303291bcb407fd0b37b52607ecebba",
           privat="/_blob/27d62de5381eeee8e9ab504567023c22", consiliere="/_blob/f2f68570a5d5b88f15c8b0c9d18a7c34",
           retreat="/_blob/8485d5712a94ed66603aeb86f80c0aac", copii="/_blob/4b9ba5277b8dd3fad28a1395c891c1d1")
ALT = dict(grup="Un grup lucrează la roata olarului într-un atelier de ceramică (fotografie provizorie)",
           companii="Mâini care își dau din mână în mână un vas de lut (fotografie provizorie)",
           privat="O femeie modelează un bol de lut la masă (fotografie provizorie)",
           consiliere="Două persoane stau la masă, cu câte o cană în mâini (fotografie provizorie)",
           retreat="Cabană de lemn într-o pădure de pini (fotografie provizorie)",
           copii="Un copil zâmbește, cu un vas de lut în mâini (fotografie provizorie)")
POS = dict(grup="50% 45%", companii="50% 40%", privat="50% 35%", consiliere="50% 50%", retreat="50% 60%", copii="60% 35%")
S = [dict(s, img=IMG[s["k"]], alt=ALT[s["k"]], pos=POS[s["k"]]) for s in S1]
BYK = {s["k"]: s for s in S}
COPII = dict(k="copii", name=SCOLI[0], line="Modelaj în lut pentru școli și afterschool, în joacă: copiii învață despre argilă și își iau piesa acasă.",
             meta=SCOLI[1], cta="Află mai multe", img=IMG["copii"], alt=ALT["copii"], pos=POS["copii"])
ORDER = [BYK["grup"], BYK["privat"], BYK["consiliere"], BYK["companii"], BYK["retreat"], COPII]
SCOLI_LINK = f'<a class="sc" href="#scoli"><b>{SCOLI[0]}</b><span>{" · ".join(SCOLI[1])}</span>{ARROW}</a>'


def active(sel_root, n, rules):
    """CSS that applies `rules` (a dict of 'child-selector' -> 'declarations') to the nth item when data-a=n."""
    return "".join(f'{sel_root}[data-a="{i}"] {sub.replace("&", f":nth-child({i + 1})")}{{{decl}}}' for i in range(n) for sub, decl in rules.items())


OPTS = {}

# 5. Acordeon: six tall photo panels side by side; the one you point at opens wide and tells its story.
pan5 = "".join(
    f'<a class="p" href="#{s["k"]}" data-i="{i}" onMouseEnter="{{{{ pick }}}}" onFocus="{{{{ pick }}}}" onClick="{{{{ pick }}}}">'
    f'<img src="{s["img"]}" alt="{s["alt"]}" style="object-position:{s["pos"]}"><span class="vl" aria-hidden="true">{s["name"]}</span>'
    f'<span class="tx">{meta(s)}<span class="n">{s["name"]}</span><span class="l">{s["line"]}</span><span class="cta">{s["cta"]}</span></span></a>'
    for i, s in enumerate(ORDER))
OPTS["CeFacem5Acordeon"] = ("Ce oferim 5: acordeon de fotografii", """
.ac .panels{display:flex;gap:12px;height:620px}
.ac .p{position:relative;flex:1 1 0;min-width:0;border-radius:24px;corner-shape:squircle;overflow:hidden;color:#F4EDE4;isolation:isolate;transition:flex-grow .75s cubic-bezier(.22,.8,.2,1)}
.ac .p img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transform:scale(1.08);transition:transform 1.4s cubic-bezier(.2,.7,.2,1),filter .6s;filter:saturate(.85) brightness(.92)}
.ac .p::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(22,12,7,.10) 0%,rgba(22,12,7,.30) 45%,rgba(22,12,7,.86) 100%)}
.ac .vl{position:absolute;left:50%;bottom:30px;transform:translateX(-50%) rotate(180deg);writing-mode:vertical-rl;font:400 25px/1 var(--display);font-variation-settings:'opsz' 20;white-space:nowrap;transition:opacity .3s}
.ac .tx{position:absolute;left:0;bottom:0;width:min(470px,100%);box-sizing:border-box;padding:0 40px 38px;opacity:0;transform:translateY(18px);transition:opacity .3s,transform .5s cubic-bezier(.2,.7,.2,1);pointer-events:none}
.ac .tx .m{color:var(--glowc)}
.ac .tx .n{display:block;margin-top:8px;font:400 46px/1.02 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.015em}
.ac .tx .l{display:block;margin-top:12px;color:#EFE3D3;font-size:17px;line-height:1.55;text-wrap:pretty}
.ac .cta{display:inline-flex;align-items:center;gap:10px;min-height:46px;margin-top:22px;padding:0 22px;border-radius:999px;background:#F4EDE4;color:#2E1D14;font-weight:500}
.ac .p:focus-visible{outline:2px solid var(--terra-d);outline-offset:4px}
""" + active(".ac .panels", 6, {".p&": "flex-grow:4.4", ".p& img": "transform:none;filter:none", ".p& .vl": "opacity:0", ".p& .tx": "opacity:1;transform:none;transition-delay:.22s"}) + """
@media (max-width:820px){.ac .panels{flex-direction:column;height:auto;gap:10px}.ac .p{flex:none;height:84px;transition:height .6s cubic-bezier(.22,.8,.2,1)}.ac .vl{writing-mode:horizontal-tb;transform:none;left:22px;bottom:auto;top:50%;margin-top:-12px;font-size:24px}.ac .tx{width:100%;padding:0 22px 26px}.ac .tx .n{font-size:34px}}
@media (max-width:820px){""" + active(".ac .panels", 6, {".p&": "height:440px"}) + """}
@media (prefers-reduced-motion:reduce){.ac .p,.ac .p img,.ac .tx{transition:none}}
""", f"""<section class="cf ac" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<div class="panels" data-a="0" ref="{{{{ rootRef }}}}">{pan5}</div>
</div>
</section>""", True)

# 6. Fereastra: the whole section is a window onto the chosen service. A big typographic list on the left;
#    the photo behind changes, slowly, like a room you walk into.
bg6 = "".join(f'<img src="{s["img"]}" alt="" style="object-position:{s["pos"]}">' for s in ORDER)
li6 = "".join(
    f'<li><a href="#{s["k"]}" data-i="{i}" onMouseEnter="{{{{ pick }}}}" onFocus="{{{{ pick }}}}" onClick="{{{{ pick }}}}">'
    f'<span class="n">{s["name"]}</span><span class="d"><span class="in"><span class="l">{s["line"]}</span>{meta(s)}{more(s["cta"])}</span></span></a></li>'
    for i, s in enumerate(ORDER))
OPTS["CeFacem6Fereastra"] = ("Ce oferim 6: fereastră", """
.fe{background:#1D100A;color:#F4EDE4;isolation:isolate;min-height:900px;box-sizing:border-box}
.fe .bg{position:absolute;inset:0;z-index:-2}
.fe .bg img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transform:scale(1.1);transition:opacity .9s ease,transform 7s cubic-bezier(.2,.7,.2,1)}
.fe::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(90deg,rgba(24,12,7,.92) 0%,rgba(24,12,7,.78) 38%,rgba(24,12,7,.30) 72%,rgba(24,12,7,.18) 100%),linear-gradient(0deg,rgba(24,12,7,.55),rgba(24,12,7,0) 35%)}
.fe .head h2{color:#F4EDE4}
.fe .head p{color:#E3D3BE}
.fe ul{list-style:none;margin:0;padding:0;max-width:640px;border-top:1px solid rgba(244,237,228,.16)}
.fe li a{display:block;padding:16px 0 14px;border-bottom:1px solid rgba(244,237,228,.16);color:inherit}
.fe .n{display:block;font:400 clamp(34px,3.5vw,52px)/1.06 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.015em;opacity:.45;transition:opacity .35s,transform .5s cubic-bezier(.2,.7,.2,1)}
.fe li a:hover .n{opacity:.8}
.fe .d{display:grid;grid-template-rows:0fr;transition:grid-template-rows .55s cubic-bezier(.2,.7,.2,1)}
.fe .in{overflow:hidden}
.fe .l{display:block;margin-top:12px;max-width:46ch;color:#EFE3D3;font-size:17px;text-wrap:pretty}
.fe .m{margin-top:8px;color:var(--glowc)}
.fe .more{margin-top:6px;color:var(--glowc)}
.fe .sc,.fe .sc b{color:#F4EDE4}
""" + active(".fe", 6, {".bg img&": "opacity:1;transform:none", "li& .n": "opacity:1;transform:translateX(12px)", "li& .d": "grid-template-rows:1fr"}) + """
@media (max-width:820px){.fe{min-height:0}.fe::after{background:linear-gradient(180deg,rgba(24,12,7,.62) 0%,rgba(24,12,7,.86) 55%,rgba(24,12,7,.93) 100%)}.fe .n{font-size:32px}}
@media (prefers-reduced-motion:reduce){.fe .bg img,.fe .d,.fe .n{transition:none}}
""", f"""<section class="cf fe" id="ce-facem" aria-labelledby="cf-h" data-a="0" ref="{{{{ rootRef }}}}">
<div class="bg" aria-hidden="true">{bg6}</div>
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<ul>{li6}</ul>
</div>
</section>""", True)

# 7. Teanc: one big card per service, each in its own brand colour; scrolling stacks them like clay tiles.
COL7 = dict(grup=("#E6D5BD", "#3A2A20", "#833A22"), privat=("#3A2A20", "#F4EDE4", "#F2C79C"), consiliere=("#4F5A43", "#F4EDE4", "#E8D9A8"),
            companii=("#2E1D14", "#F4EDE4", "#F2C79C"), retreat=("#9C472C", "#F4EDE4", "#FBE3CC"))
WHO7 = dict(grup="Pentru tine", privat="Pentru tine", consiliere="Pentru tine", companii="Pentru echipa ta", retreat="Pentru tine, în curând")
cards7 = "".join(
    f'<li class="card" style="--i:{i};--bg:{COL7[s["k"]][0]};--fg:{COL7[s["k"]][1]};--ac:{COL7[s["k"]][2]}"><img src="{s["img"]}" alt="{s["alt"]}" style="object-position:{s["pos"]}">'
    f'<div class="tx"><div><span class="who">{WHO7[s["k"]]}</span><h3 class="n">{s["name"]}</h3></div>'
    f'<div><p class="l">{s["line"]}</p>{meta(s)}<a class="btn" href="#{s["k"]}">{s["cta"]} {ARROW}</a></div></div></li>'
    for i, s in enumerate(ORDER[:5]))
OPTS["CeFacem7Teanc"] = ("Ce oferim 7: teanc de cărți", """
.tc{overflow:visible}
.tc .stack{display:flex;flex-direction:column;gap:32px;margin:0;padding:0;list-style:none}
.tc .card{position:sticky;top:calc(48px + var(--i) * 20px);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);min-height:540px;border-radius:30px;corner-shape:squircle;overflow:hidden;background:var(--bg);color:var(--fg);box-shadow:0 -24px 50px -34px rgba(30,16,10,.55)}
.tc .card:nth-child(even) img{order:2}
.tc .card img{display:block;width:100%;height:100%;min-height:540px;object-fit:cover}
.tc .tx{display:flex;flex-direction:column;justify-content:space-between;gap:40px;padding:56px 60px 52px}
.tc .who{font:400 italic 21px/1.2 var(--display);color:var(--ac)}
.tc .n{margin:12px 0 0;font:400 clamp(44px,4.4vw,66px)/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.02em;text-wrap:balance}
.tc .l{margin:0;max-width:40ch;font-size:18px;line-height:1.55;text-wrap:pretty;opacity:.92}
.tc .m{margin-top:10px;color:var(--ac)}
.tc .btn{display:inline-flex;align-items:center;gap:10px;min-height:48px;margin-top:26px;padding:0 24px;border-radius:999px;background:var(--fg);color:var(--bg);font-weight:500;transition:transform .25s}
.tc .btn:hover{transform:translateY(-2px)}
.tc .foot{margin-top:48px}
@media (max-width:820px){.tc .stack{gap:20px}.tc .card{grid-template-columns:1fr;top:calc(16px + var(--i) * 12px);min-height:0;border-radius:24px}.tc .card:nth-child(even) img{order:0}.tc .card img{min-height:0;height:220px}.tc .tx{padding:26px 24px 28px;gap:18px}.tc .n{font-size:38px}.tc .l{font-size:16.5px}}
""", f"""<section class="cf tc" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<ul class="stack">{cards7}</ul>
<div class="foot">{SCOLI_LINK}</div>
</div>
</section>""", False)

# 8. Raftul cu vase: each service is a photo shaped like a different pot, standing on one shelf.
#    Bowl for the group (many hands around one table), jug, tea cup for counselling, tall bottle, amphora for the journey.
SHAPES = {  # clip paths in 0..1 box units; (path, height px on desktop, width/height)
    "bowl": ("M0 0H1C1 .52 .80 .90 .63 .97L.61 1H.39L.37 .97C.20 .90 0 .52 0 0Z", 165, 1.3),
    "jug": ("M.20 0H.80C.78 .10 .78 .15 .83 .23C.93 .40 .93 .70 .85 .87C.80 .96 .72 1 .60 1H.40C.28 1 .20 .96 .15 .87C.07 .70 .07 .40 .17 .23C.22 .15 .22 .10 .20 0Z", 300, .7),
    "cup": ("M.04 0H.96L.85 .93C.84 .98 .80 1 .75 1H.25C.20 1 .16 .98 .15 .93Z", 250, .82),
    "bottle": ("M.39 0H.61V.17C.61 .25 .79 .29 .88 .43C.97 .58 .95 .80 .85 .92C.79 .98 .71 1 .60 1H.40C.29 1 .21 .98 .15 .92C.05 .80 .03 .58 .12 .43C.21 .29 .39 .25 .39 .17Z", 400, .52),
    "amphora": ("M.40 0H.60V.06C.60 .10 .62 .12 .70 .16C.92 .26 .98 .42 .96 .58C.94 .76 .80 .90 .66 .96L.64 1H.36L.34 .96C.20 .90 .06 .76 .04 .58C.02 .42 .08 .26 .30 .16C.38 .12 .40 .10 .40 .06Z", 360, .58),
}
PAIR8 = [("grup", "bowl"), ("privat", "jug"), ("consiliere", "cup"), ("companii", "bottle"), ("retreat", "amphora")]


def vessel(s, shape, i):
    d, h, ar = SHAPES[shape]
    W, H = 100, round(100 / ar, 1)
    return (f'<svg class="v" viewBox="0 0 {W} {H}" style="--h:{h}px;--ar:{ar}" aria-hidden="true">'
            f'<defs><clipPath id="vc{i}" clipPathUnits="objectBoundingBox"><path d="{d}"></path></clipPath></defs>'
            f'<path class="ol" d="{d}" transform="translate(3.5 4.5) scale({W} {H})"></path>'
            f'<g class="ph"><image href="{s["img"]}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice" style="clip-path:url(#vc{i})"></image></g></svg>')


items8 = "".join(
    f'<li><a href="#{k}"><span class="pot">{vessel(BYK[k], shape, i)}</span><span class="tx"><span class="n">{BYK[k]["name"]}</span>'
    f'<span class="l">{BYK[k]["line"]}</span>{meta(BYK[k])}{more(dict(grup="Vezi atelierele", privat="Rezervă", consiliere="Programează", companii="Cere o ofertă", retreat="Anunță-mă")[k])}</span></a></li>'
    for i, (k, shape) in enumerate(PAIR8))
OPTS["CeFacem8Vase"] = ("Ce oferim 8: raftul cu vase", """
.va{background:radial-gradient(ellipse 60% 55% at 50% 38%,#FAF5EE 0%,rgba(250,245,238,0) 70%),var(--paper)}
.va .shelf{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:0 24px;margin:0;padding:0;list-style:none}
.va li a{display:flex;flex-direction:column;color:var(--ink)}
.va .pot{position:relative;display:flex;align-items:flex-end;justify-content:center;height:420px;border-bottom:1px solid rgba(58,42,32,.35)}
.va .pot::after{content:"";position:absolute;left:12%;right:12%;bottom:-1px;height:18px;border-radius:50%;background:radial-gradient(closest-side,rgba(58,42,32,.28),rgba(58,42,32,0));transform:translateY(50%)}
.va .v{position:relative;z-index:1;display:block;height:var(--h);width:auto;max-width:100%;overflow:visible;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.va .ol{fill:none;stroke:#9C472C;stroke-width:1.2px;vector-effect:non-scaling-stroke;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.va .ph{transition:transform .9s cubic-bezier(.2,.7,.2,1)}
.va li a:hover .v,.va li a:focus-visible .v{transform:translateY(-10px)}
.va .tx{display:flex;flex-direction:column;padding-top:30px}
.va .n{font:400 27px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em}
.va .l{margin-top:10px;color:var(--ink2);font-size:15.5px;line-height:1.55;text-wrap:pretty}
.va .m{margin-top:10px;font-size:13.5px}
.va .more{margin-top:8px;align-self:flex-start}
.va .foot{margin-top:56px;padding-top:22px;border-top:1px solid rgba(58,42,32,.18)}
@media (max-width:820px){.va .shelf{display:flex;gap:22px;overflow-x:auto;scroll-snap-type:x mandatory;margin:0 -20px;padding:0 20px 8px;scrollbar-width:none}.va .shelf::-webkit-scrollbar{display:none}.va .shelf li{flex:0 0 68vw;scroll-snap-align:start}.va .pot{height:300px}.va .v{height:calc(var(--h) * .8)}}
@media (prefers-reduced-motion:reduce){.va .v{transition:none}}
""", f"""<section class="cf va" id="ce-facem" aria-labelledby="cf-h">
<div class="wrap">
<div class="head"><h2 class="disp" id="cf-h">Ce oferim</h2><p>{HEAD_P}</p></div>
<ul class="shelf">{items8}</ul>
<div class="foot">{SCOLI_LINK}</div>
</div>
</section>""", False)

PICK_JS = """class Component extends DCLogic {
  renderVals() {
    var self = this;
    if (!this.cb) this.cb = {
      rootRef: function (el) { self.root = el; },
      pick: function (e) { if (self.root) self.root.setAttribute('data-a', e.currentTarget.getAttribute('data-i')); }
    };
    return this.cb;
  }
}"""
STATIC_JS = "class Component extends DCLogic {\n  renderVals() { return {}; }\n}"


def page(title, css, html, js, w, h):
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
<div class="pg">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{PICK_JS if js else STATIC_JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, 1200), ("Mobil", 390, 1800)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "cefacem2.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce oferim 2</title><style>body{margin:0}iframe{width:1440px;height:3400px;border:0;display:block}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "cefacem2-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce oferim 2 mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:2400px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
