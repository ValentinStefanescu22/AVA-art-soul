"""Biletele de Crăciun (Vali, 12 nov): the December tickets („Atelier cu tematică de Crăciun”) get a Christmas touch,
the ticket itself stays exactly as in Lista 3 (grup_ateliere_options.bilete). Four directions, each from a real site.
Nothing new to read: the decorations are aria-hidden, no new copy. All motion stops with prefers-reduced-motion.

usage: python3 .aidesigner/grup_craciun_options.py
writes .aidesigner/canvas/project/GrupCraciun1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-GrupCraciun*.html
"""
import math, os, random, subprocess, sys
import grup_ateliere_options as ga
from about_options2 import P, HERE

XMAS = lambda e: "Crăciun" in e["title"]
FX = '<span class="fx" aria-hidden="true">{}</span>'

# 1. Google, „let it snow”: snow falls over the page. Here a few line-drawn flakes in clay drift down inside the ticket.
def flake():
    d = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        ex, ey = 9 * math.cos(a), 9 * math.sin(a)
        d.append(f"M0 0L{ex:.1f} {ey:.1f}")
        mx, my = 5.2 * math.cos(a), 5.2 * math.sin(a)
        for s in (-1, 1):
            b = a + s * math.radians(42)
            d.append(f"M{mx:.1f} {my:.1f}L{mx + 3 * math.cos(b):.1f} {my + 3 * math.sin(b):.1f}")
    return f'<svg viewBox="-10 -10 20 20"><path d="{"".join(d)}"></path></svg>'


FLAKE = flake()


def snow(e):
    if not XMAS(e):
        return ""
    r = random.Random(int(e["day"]))
    return FX.format("".join(
        f'<i style="--x: {r.uniform(2, 97):.1f}%; --s: {r.uniform(13, 24):.0f}px; --d: {r.uniform(11, 19):.1f}s; --dl: -{r.uniform(0, 19):.1f}s; '
        f'--dx: {r.uniform(-30, 30):.0f}px; --o: {r.uniform(.4, .7):.2f}; --ry: {r.uniform(4, 150):.0f}px">{FLAKE}</i>' for _ in range(11)))


SNOW_CSS = """
.cx .fx{position:absolute;inset:0;overflow:hidden;border-radius:inherit;pointer-events:none}
.cx .fx i{position:absolute;left:var(--x);top:-24px;width:var(--s);height:var(--s);opacity:var(--o);color:#C07A4E;animation:cx-fall var(--d) linear var(--dl) infinite}
.cx .fx svg{display:block;width:100%;height:100%;fill:none;stroke:currentColor;stroke-width:1.4;stroke-linecap:round}
@keyframes cx-fall{to{transform:translate(var(--dx),460px) rotate(200deg)}}
.cx .xmas .stub b{color:#9C472C}
@media (prefers-reduced-motion:reduce){.cx .fx i{animation:none;transform:translateY(var(--ry))}}
"""

# 2. Regent Street, London: strings of warm lights across the street. A garland hangs along the top of the ticket and twinkles.
BULBS = ["#B4583A", "#E2A65F", "#6F7B5C", "#C07A4E", "#E2A65F"]


def lights(e):
    if not XMAS(e):
        return ""
    n, sag, out = 17, 20, []
    for k in range(n):
        t = (k + .5) / n
        y = 2 * t * (1 - t) * 2 * sag
        out.append(f'<i style="left: {100 * t:.2f}%; top: {y + 1:.1f}px; --c: {BULBS[k % len(BULBS)]}; --dl: {(k * 7 % 11) * .37:.2f}s; rotate: {(t - .5) * -36:.0f}deg"></i>')
    wire = f'<svg viewBox="0 0 100 {2 * sag}" preserveAspectRatio="none"><path d="M0 0Q50 {2 * sag} 100 0"></path></svg>'
    return FX.format(wire + "".join(out))


LIGHTS_CSS = """
.cx .fx{position:absolute;left:18px;right:18px;top:0;height:40px;pointer-events:none}
.cx .fx svg{position:absolute;left:0;top:0;width:100%;height:40px;overflow:visible;fill:none;stroke:rgba(58,42,32,.45);stroke-width:1.2;vector-effect:non-scaling-stroke}
.cx .fx svg path{vector-effect:non-scaling-stroke}
.cx .fx i{position:absolute;width:8px;height:12px;margin-left:-4px;transform-origin:50% 0;border-radius:50% 50% 50% 50% / 40% 40% 60% 60%;background:var(--c);
  box-shadow:0 0 0 0 var(--c);animation:cx-glow 3.2s ease-in-out var(--dl) infinite}
.cx .fx i::before{content:"";position:absolute;left:1.5px;top:-3px;width:5px;height:4px;border-radius:1px;background:#5A4535}
@keyframes cx-glow{0%,100%{opacity:.55;box-shadow:0 0 0 0 transparent}50%{opacity:1;box-shadow:0 0 12px 3px var(--c)}}
@media (hover:hover){.cx .xmas .card:hover .fx i{animation-duration:1.1s}}
.cx .xmas .stub,.cx .xmas .bd{padding-top:48px}
@media (max-width:980px){.cx .xmas .stub{padding-top:36px}.cx .xmas .bd{padding-top:18px}}
@media (prefers-reduced-motion:reduce){.cx .fx i{animation:none;opacity:.9}}
"""


# 3. Papier: winter cards with fine botanical line drawings. A fir sprig with clay berries, drawn on the stub as the ticket appears.
def sprig():
    # a curved stem; needles both sides, shorter towards the tip
    P0, C, P1 = (6, 62), (30, 30), (70, 8)
    q = lambda t: tuple((1 - t) ** 2 * a + 2 * (1 - t) * t * b + t ** 2 * c for a, b, c in zip(P0, C, P1))
    d = [f"M{P0[0]} {P0[1]}Q{C[0]} {C[1]} {P1[0]} {P1[1]}"]
    for k in range(1, 19):
        t = k / 19
        (x, y), (x2, y2) = q(t), q(min(t + .01, 1))
        a = math.atan2(y2 - y, x2 - x)
        L = 15 * (1 - t * .5)
        for s in (-1, 1):
            b = a + s * math.radians(52)
            d.append(f"M{x:.1f} {y:.1f}L{x + L * math.cos(b):.1f} {y + L * math.sin(b):.1f}")
    berries = "".join(f'<circle cx="{x}" cy="{y}" r="{r}"></circle>' for x, y, r in [(20, 58, 3.6), (26, 61, 3.1), (21, 66, 2.8)])
    return (f'<svg class="sp" viewBox="0 0 80 80"><path pathLength="1" d="{"".join(d)}"></path>'
            f'<g class="be">{berries}</g></svg>')


SPRIG = sprig()


def bough(e):
    return FX.format(SPRIG + SPRIG.replace('class="sp"', 'class="sp two"')) if XMAS(e) else ""


SPRIG_CSS = """
.cx .fx{position:absolute;inset:0;pointer-events:none}
.cx .sp{position:absolute;left:-10px;top:-14px;width:104px;height:104px;fill:none;stroke:#6F7B5C;stroke-width:1.5;stroke-linecap:round;overflow:visible}
.cx .sp.two{left:auto;top:auto;right:6px;bottom:2px;width:70px;height:70px;rotate:180deg;transform-origin:50% 50%}
.cx .sp .be{fill:#B4583A;stroke:none}
.cx .sp path{stroke-dasharray:1;stroke-dashoffset:0}
.cx.js:not(.in) .sp path{stroke-dashoffset:1}.cx.js:not(.in) .sp .be{opacity:0}
.cx.js.in .sp path{animation:cx-draw 1.6s var(--so) .5s backwards}
.cx.js.in .sp .be{animation:cx-pop .5s cubic-bezier(.3,1.32,.5,1) 1.7s backwards}
.cx.js.in .sp.two path{animation-delay:.9s}.cx.js.in .sp.two .be{animation-delay:2.1s}
@keyframes cx-draw{from{stroke-dashoffset:1}}
@keyframes cx-pop{from{opacity:0;scale:.2}}
.cx .sp .be circle{transform-box:fill-box;transform-origin:center}
.cx .sp{transform-origin:10% 80%;transition:rotate .6s var(--so)}
@media (hover:hover){.cx .xmas .card:hover .sp:not(.two){rotate:-6deg}}
@media (max-width:980px){.cx .sp{width:76px;height:76px;left:-8px;top:-10px}.cx .xmas .stub{padding-left:52px}.cx .sp.two{display:none}}
"""

# 4. Anthropologie: hand-painted ceramic baubles. A clay bauble with the brand's three wavy rings hangs from the ticket's top and sways.
BAUBLE = ('<span class="orn"><span class="th"></span><span class="cap"></span>'
          '<svg class="ball" viewBox="0 0 40 40"><defs><radialGradient id="cx-g" cx="35%" cy="30%" r="75%">'
          '<stop offset="0" stop-color="#E7B28A"></stop><stop offset=".45" stop-color="#C07A4E"></stop><stop offset="1" stop-color="#8E4A2E"></stop></radialGradient>'
          '<clipPath id="cx-c"><circle cx="20" cy="20" r="19"></circle></clipPath></defs>'
          '<circle cx="20" cy="20" r="19" fill="url(#cx-g)"></circle><g clip-path="url(#cx-c)" fill="none" stroke-width="1.6" stroke-linecap="round">'
          '<path d="M-2 15q5.5-4 11 0t11 0 11 0 11 0" stroke="#3A2A20" opacity=".7"></path>'
          '<path d="M-2 20q5.5-4 11 0t11 0 11 0 11 0" stroke="#F4EDE4"></path>'
          '<path d="M-2 25q5.5-4 11 0t11 0 11 0 11 0" stroke="#3A2A20" opacity=".7"></path></g>'
          '<ellipse cx="13" cy="11" rx="4" ry="2.4" fill="#FFF3E4" opacity=".55" transform="rotate(-30 13 11)"></ellipse></svg></span>')


def bauble(e):
    return FX.format(BAUBLE + BAUBLE.replace('class="orn"', 'class="orn o2"')) if XMAS(e) else ""


BAUBLE_CSS = """
.cx .fx{position:absolute;inset:0;pointer-events:none}
.cx .orn{position:absolute;right:78px;top:0;--th:24px;display:flex;flex-direction:column;align-items:center;transform-origin:50% 0;animation:cx-sway 4.2s ease-in-out infinite alternate}
.cx .orn.o2{right:134px;--th:44px;animation-delay:-2.1s;animation-duration:3.6s}.cx .orn.o2 .ball{width:30px;height:30px}
.cx .orn .th{width:1px;height:var(--th);background:rgba(58,42,32,.5)}
.cx .orn .cap{width:9px;height:6px;margin-bottom:-2px;border-radius:2px 2px 1px 1px;background:linear-gradient(90deg,#8C7A62,#D9C7A8,#8C7A62)}
.cx .orn .ball{display:block;width:38px;height:38px;filter:drop-shadow(0 6px 6px rgba(58,30,15,.25))}
@keyframes cx-sway{from{rotate:-5deg}to{rotate:5deg}}
@media (hover:hover){.cx .xmas .card:hover .orn{animation-duration:1.4s}}
@media (max-width:980px){.cx .orn{top:var(--seam,94px);right:22px;--th:30px}.cx .orn.o2{right:66px;--th:12px}}
@media (prefers-reduced-motion:reduce){.cx .orn{animation:none}}
"""

SOURCES = {
    "GrupCraciun1Ninsoare": "Google, căutarea „let it snow”: fulgi care cad peste pagină; aici fulgi desenați cu linie de lut, doar pe biletele din decembrie",
    "GrupCraciun2Beculete": "luminițele de Crăciun de pe Regent Street, Londra: o ghirlandă de beculețe calde atârnă pe marginea de sus a biletului",
    "GrupCraciun3Crengute": "felicitările de iarnă Papier: ilustrații botanice cu linie fină; o crenguță de brad cu boabe de lut se desenează pe bilet",
    "GrupCraciun4Glob": "globurile de ceramică pictate de mână de la Anthropologie: un glob de lut cu inelele AVA atârnă de bilet și se leagănă",
}
OPTS = {
    "GrupCraciun1Ninsoare": ("Biletele de Crăciun 1: ninsoare", SNOW_CSS, snow),
    "GrupCraciun2Beculete": ("Biletele de Crăciun 2: beculețe", LIGHTS_CSS, lights),
    "GrupCraciun3Crengute": ("Biletele de Crăciun 3: crenguțe de brad", SPRIG_CSS, bough),
    "GrupCraciun4Glob": ("Biletele de Crăciun 4: glob de lut", BAUBLE_CSS, bauble),
}
H = {k: ga.H["GrupAteliere3Bilete"] for k in OPTS}
H["GrupCraciun2Beculete"] = (1059, 1561)   # the garland adds room at the top

if __name__ == "__main__":
    ga.SOURCES.update(SOURCES)
    base_css = ga.OPTS["GrupAteliere3Bilete"][1]
    for name, (title, css, deco) in OPTS.items():
        html = ga.bilete(deco, "a3 cx")
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(ga.page(name, title + (" · mobil" if suffix else ""), base_css + css, html, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
