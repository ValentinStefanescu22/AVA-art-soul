"""Pagina „Ce oferim”, part 1: the opening (title + every service at a glance). Four directions, each from a real
product, all animated.

usage: python3 .aidesigner/cf_pagina_options.py
writes .aidesigner/canvas/project/CFPagina1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-CFPagina*.html
Copy: docs/continut-site.md. Title „Ce oferim” (menu), lede = the Acasă subtitle from the doc, each service's first
sentence + facts from its page (same data as the Acasă „Ce oferim” block, ce_facem_options.py / ce_facem2_options.py).
Photos are the provisional ones from Acasă (Unsplash + October workshop).
Motion rules as everywhere: .js before hiding, entrances once (.in from IntersectionObserver), `backwards` fill,
lerp/transition so it stays interruptible, prefers-reduced-motion = still.
"""
import os, re, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
from header_options import HX_CSS, V, header_html, VASE
from ce_facem2_options import BYK, COPII

TITLE = "Ce oferim"
LEDE = "Ateliere cu lut, consiliere și retreaturi pentru momentele în care ai nevoie să te auzi din nou. Pentru tine sau pentru echipa ta."
# Vali's canvas comments on Ce oferim 1 (11 nov): button labels, „Evenimente” for companies, schools without „60 min”
G = dict(BYK["grup"], cta="Vezi atelierul din decembrie")
PR = dict(BYK["privat"], cta="Află mai multe")
CO = dict(BYK["consiliere"], cta="Află mai multe")
RE = BYK["retreat"]
CP = dict(BYK["companii"], line="Evenimente de autocunoaștere și conectare pentru echipe, în care lutul este unealta.")
COPII = dict(COPII, meta=["de la 6 ani", "de la 50 lei / copil"])
ORDER = [G, PR, CO, RE, CP, COPII]
FORMATE = ["Atelier de 3 ore modelaj în lut", "Jumătate de zi cu lut și teme de wellbeing", "Program lunar de wellbeing", "Teambuilding la cerere"]

SOURCES = {
    "CFPagina1Comutator": "airbnb.com: filele „Locuințe · Experiențe · Servicii” cu iconițe animate (2025)",
    "CFPagina2Bento": "apple.com: grila „bento” de pe paginile de produs (plăci de mărimi diferite)",
    "CFPagina3Drum": "Duolingo: drumul lecțiilor, cu butoane rotunde care se apasă",
    "CFPagina4CoverFlow": "Apple iTunes (2006): Cover Flow, copertele care se rotesc în 3D, cu reflexie",
}


def h1(cls=""):
    """the title as letters that rise one by one; screen readers get the plain words"""
    k, ws = 0, []
    for w in TITLE.split():
        ls = []
        for ch in w:
            ls.append(f'<span class="l" style="--k: {k}">{ch}</span>'); k += 1
        ws.append('<span class="w" aria-hidden="true">' + "".join(ls) + "</span>")
    return f'<h1 class="disp cph {cls}" id="cp-h" aria-label="{TITLE}">' + " ".join(ws) + "</h1>"


def meta(s):
    return '<span class="m">' + " · ".join(s["meta"]) + "</span>"


def img(s, extra=""):
    return f'<img src="{s["img"]}" alt="{s["alt"]}" style="object-position: {s["pos"]}"{extra}>'


COMMON = """
.cp{position:relative;overflow:clip;--sp:cubic-bezier(.3,1.32,.5,1);--so:cubic-bezier(.22,1,.36,1)}
.cp a{text-decoration:none}
.cph{font-size:clamp(72px,9vw,128px);line-height:.95;letter-spacing:-.025em;font-variation-settings:'opsz' 72}
.cph .w{display:inline-block;white-space:nowrap}.cph .l{display:inline-block}
.cp .lede{margin:0;font:400 clamp(20px,1.7vw,24px)/1.4 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.cp .m{display:block;font-size:14px;line-height:1.5;color:#833A22;font-variant-numeric:tabular-nums}
.cp .n{display:block;font:400 28px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.cp .ln{display:block;margin-top:8px;font-size:15px;line-height:1.55;color:var(--ink2);text-wrap:pretty}
@keyframes cp-l{from{opacity:0;translate:0 .4em;filter:blur(8px)}}
@keyframes cp-up{from{opacity:0;translate:0 16px}}
@media (prefers-reduced-motion:no-preference){
  .cph .l{animation:cp-l 1s var(--so) backwards;animation-delay:calc(.1s + var(--k) * 45ms)}
  .cp .up{animation:cp-up .8s var(--so) .45s backwards}
}
@media (max-width:980px){.cph{font-size:clamp(56px,16vw,84px)}}
@media (prefers-reduced-motion:reduce){.cp *{animation:none!important;transition:none!important}}
"""

ENTER = """
    var self = this, s = this.sec; if (!s) return;
    var reduce = this.reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    s.classList.add('js');
    if (reduce || !window.IntersectionObserver) s.classList.add('in');
    else { this.io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { s.classList.add('in'); self.io.disconnect(); } }, { threshold: 0.1 }); this.io.observe(s); }"""


def script(mount="", unmount=""):
    return ("class Component extends DCLogic {\n  componentDidMount() {" + ENTER + mount + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); " + unmount + " }\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = { secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


def eased_gradient(a, b, c0="#3A2418", c1="#F4EDE4", n=18, head="#2E1C13 0", tail="#EFE4D4 100%"):
    """brown -> cream between a and b px, eased (ease-in-out sine, the "easing gradients" technique) and mixed in OKLab,
    so there is no visible band or muddy orange middle. Plain hex stops, so every browser draws the same thing."""
    import math
    def lin(x): x /= 255; return x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4
    def gam(x): x = max(0, min(1, x)); return round(255 * (12.92 * x if x <= .0031308 else 1.055 * x ** (1 / 2.4) - .055))
    def to_lab(h):
        r, g, bb = (lin(int(h[i:i + 2], 16)) for i in (1, 3, 5))
        l, m, s_ = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * bb, 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * bb, 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * bb)
        l, m, s_ = (v ** (1 / 3) for v in (l, m, s_))
        return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s_, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s_, 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s_)
    def to_hex(L, A, B):
        l, m, s_ = ((L + 0.3963377774 * A + 0.2158037573 * B) ** 3, (L - 0.1055613458 * A - 0.0638541728 * B) ** 3, (L - 0.0894841775 * A - 1.2914855480 * B) ** 3)
        r, g, bb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s_, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s_, -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s_)
        return "#%02X%02X%02X" % (gam(r), gam(g), gam(bb))
    p0, p1 = to_lab(c0), to_lab(c1)
    stops = []
    for i in range(n + 1):
        t = i / n; e = 0.5 - 0.5 * math.cos(math.pi * t)
        stops.append(f"{to_hex(*(x + (y - x) * e for x, y in zip(p0, p1)))} {a + (b - a) * t:.0f}px")
    return "linear-gradient(180deg," + (head + "," if head else "") + ",".join(stops) + ("," + tail if tail else "") + ")"


OPTS = {}

# 1. Comutator (Airbnb, 2025): three tabs with little icons, like Homes · Experiences · Services. The underline slides
#    to the chosen tab on a spring, its icon gives a small hop, and the cards of that path rise in one after another.
#    Without JS all three groups simply stay visible one under the other.
ICONS = {
    "tine": VASE,
    "companii": '<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" style="stroke-width:3.2;stroke-linecap:round"><circle cx="32" cy="20" r="8"></circle><circle cx="15" cy="27" r="6.5"></circle><circle cx="49" cy="27" r="6.5"></circle><path d="M18 54C18 44 24 38 32 38S46 44 46 54M4 52C4 45 8 40 15 40M60 52C60 45 56 40 49 40"></path></g></svg>',
    "scoli": '<svg viewBox="0 0 64 64" aria-hidden="true"><g fill="none" stroke="currentColor" style="stroke-width:3.2;stroke-linecap:round"><circle cx="32" cy="32" r="11"></circle><path d="M32 6V13M32 51V58M6 32H13M51 32H58M13.6 13.6L18.5 18.5M45.5 45.5L50.4 50.4M13.6 50.4L18.5 45.5M45.5 18.5L50.4 13.6"></path></g></svg>',
}
TABS = [("tine", "Pentru tine", [G, PR, CO, RE]), ("companii", "Pentru companii", [CP]), ("scoli", "Pentru școli și copii", [COPII])]


def card1(s, i, wide=False):
    extra = ""
    if s is CP:
        extra = '<ul class="fm">' + "".join(f"<li>{f}</li>" for f in FORMATE) + "</ul>"
    return (f'<a class="cd{" wide" if wide else ""}" href="#{s["k"]}" style="--i: {i}"><span class="ph">{img(s)}</span>'
            f'<span class="tx"><span class="n">{s["name"]}</span><span class="ln">{s["line"]}</span>{extra}{meta(s)}'
            f'<span class="more">{s["cta"]} {ARROW}</span></span></a>')


tabs1 = "".join(f'<button class="tb" role="tab" id="cp-t{j}" aria-controls="cp-p{j}" aria-selected="{"true" if j == 0 else "false"}" data-j="{j}">'
                f'<span class="ic">{ICONS[k]}</span><span class="tl">{lab}</span></button>' for j, (k, lab, _) in enumerate(TABS))
pans1 = "".join(f'<div class="pn" role="tabpanel" id="cp-p{j}" aria-labelledby="cp-t{j}"><div class="grid{" one" if len(ss) == 1 else ""}">'
                + "".join(card1(s, i, len(ss) == 1) for i, s in enumerate(ss)) + "</div></div>" for j, (k, lab, ss) in enumerate(TABS))
OPTS["CFPagina1Comutator"] = ("Ce oferim 1: comutatorul", "dark", """
.c1{background:""" + eased_gradient(330, 800) + """;padding:184px 0 120px;text-align:center}
.c1 .cph{color:#F4EDE4}
.c1 .lede{max-width:44ch;margin:28px auto 0;color:#EFE3D3}
.c1 .tabs{position:relative;display:flex;justify-content:center;gap:48px;margin:196px auto 0;padding-bottom:14px;border-bottom:1px solid rgba(58,42,32,.14)}
.c1 .tb{display:flex;flex-direction:column;align-items:center;gap:8px;min-width:120px;min-height:44px;padding:4px 6px;border:0;background:none;color:var(--ink);font:400 21px/1.2 var(--display);font-variation-settings:'opsz' 20;cursor:pointer;opacity:.62;transition:opacity .25s ease}
.c1 .tb:hover,.c1 .tb[aria-selected="true"]{opacity:1}
.c1 .tb:focus-visible{outline:2px solid var(--terra-d);outline-offset:4px;border-radius:12px}
.c1 .ic{display:grid;place-items:center;width:52px;height:52px;border-radius:50%;background:#F8F1E7;box-shadow:inset 0 -4px 8px rgba(58,30,15,.08),0 10px 18px -12px rgba(58,30,15,.5);transition:scale .4s var(--sp)}
.c1 .ic svg{width:28px;height:28px;color:var(--ink)}
.c1 .tb:hover .ic{scale:1.08}
.c1 .tb[aria-selected="true"] .ic svg{color:var(--terra-d)}
@keyframes c1-hop{0%{translate:0 0;rotate:0deg}35%{translate:0 -9px;rotate:-8deg}70%{translate:0 0;rotate:5deg}100%{rotate:0deg}}
.c1.js .tb[aria-selected="true"] .ic{animation:c1-hop .6s var(--sp)}
.c1 .bar{position:absolute;left:0;bottom:-1px;height:2px;width:var(--w,0);translate:var(--x,0) 0;background:var(--ink);border-radius:2px;opacity:0;transition:translate .6s var(--sp),width .6s var(--sp)}
.c1.js .bar{opacity:1}
.c1 .pn{margin-top:48px;text-align:left}
.c1.js .pn[hidden]{display:none}
.c1:not(.js) .pn+.pn{margin-top:72px}
.c1 .grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:22px}
.c1 .cd{display:flex;flex-direction:column;color:var(--ink)}
.c1 .ph{display:block;overflow:hidden;aspect-ratio:4/5;border-radius:22px;corner-shape:squircle;background:#E6D5BD}
.c1 .ph img{display:block;width:100%;height:100%;object-fit:cover;transition:scale 1.1s var(--so)}
.c1 .cd:hover .ph img{scale:1.06}
.c1 .tx{display:block;padding:20px 4px 0}
.c1 .tx .m{margin-top:12px}
.c1 .more{margin-top:8px}
.c1 .grid.one{grid-template-columns:1fr}
.c1 .wide{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:56px;align-items:center}
.c1 .wide .ph{aspect-ratio:16/11}
.c1 .wide .n{font-size:44px}
.c1 .wide .ln{font-size:18px;max-width:40ch}
.c1 .fm{margin:18px 0 0;padding:0;list-style:none;columns:2;column-gap:28px}
.c1 .fm li{position:relative;break-inside:avoid;padding:6px 0 6px 18px;font-size:15px;line-height:1.45}
.c1 .fm li::before{content:"";position:absolute;left:0;top:14px;width:7px;height:7px;border-radius:50%;background:var(--clay)}
@keyframes c1-in{from{opacity:0;translate:0 26px;scale:.97}}
.c1.js.in .pn:not([hidden]) .cd{animation:c1-in .8s var(--so) backwards;animation-delay:calc(var(--i) * 80ms + 60ms)}
.c1.js:not(.in) .pn .cd{opacity:0}
@media (max-width:980px){
  .c1{background:""" + eased_gradient(280, 680) + """;padding:128px 0 72px}.c1 .lede{margin-top:20px}
  .c1 .tabs{gap:6px;margin-top:168px;padding-bottom:10px}.c1 .tb{flex:1 1 0;min-width:0;font-size:17px}.c1 .ic{width:44px;height:44px}.c1 .ic svg{width:24px;height:24px}
  .c1 .pn{margin-top:32px}.c1 .grid{grid-template-columns:1fr;gap:36px}.c1 .ph{aspect-ratio:16/11}
  .c1 .wide{grid-template-columns:1fr;gap:0}.c1 .wide .n{font-size:30px}.c1 .wide .ln{font-size:16px}.c1 .fm{columns:1}
}
""", '<section class="cp c1" aria-labelledby="cp-h" ref="{{ secRef }}"><div class="wrap">' + h1() + f'<p class="lede up">{LEDE}</p>'
   + f'<div class="tabs up" role="tablist" aria-label="Pentru cine">{tabs1}<span class="bar" aria-hidden="true"></span></div>{pans1}</div></section>',
   script(mount="""
    var tabs = [].slice.call(s.querySelectorAll('[role=tab]')), pans = [].slice.call(s.querySelectorAll('[role=tabpanel]')), bar = s.querySelector('.bar');
    var place = function () { var t = tabs.filter(function (x) { return x.getAttribute('aria-selected') === 'true'; })[0]; bar.style.setProperty('--x', t.offsetLeft + 'px'); bar.style.setProperty('--w', t.offsetWidth + 'px'); };
    var pick = function (i, focus) {
      tabs.forEach(function (t, j) { t.setAttribute('aria-selected', j === i ? 'true' : 'false'); t.tabIndex = j === i ? 0 : -1; });
      pans.forEach(function (p, j) { p.hidden = j !== i; });
      place(); if (focus) tabs[i].focus();
    };
    pick(0);
    this.click = function (e) { var t = e.target.closest && e.target.closest('[role=tab]'); if (t) pick(+t.getAttribute('data-j')); };
    this.key = function (e) {
      var i = tabs.indexOf(document.activeElement); if (i < 0) return;
      if (e.key === 'ArrowRight') pick((i + 1) % tabs.length, true); else if (e.key === 'ArrowLeft') pick((i + tabs.length - 1) % tabs.length, true); else return;
      e.preventDefault();
    };
    this.resize = place;
    s.addEventListener('click', this.click); s.addEventListener('keydown', this.key); window.addEventListener('resize', this.resize);
    if (document.fonts) document.fonts.ready.then(place);""",
          unmount="if (this.sec && this.click) { this.sec.removeEventListener('click', this.click); this.sec.removeEventListener('keydown', this.key); window.removeEventListener('resize', this.resize); }"))

# 2. Bento (apple.com): the title and every service as tiles of different sizes in one grid. The tiles open from the
#    centre one after another; a warm light follows the cursor inside the tile you point at, the photo leans in and the
#    arrow chip turns.
RINGS = ('<svg class="orn" viewBox="0 0 120 34" aria-hidden="true">'
         + "".join(f'<path d="M4 {y}C19 {y-6} 34 {y-6} 49 {y}S79 {y+6} 94 {y}S112 {y-4} 116 {y}" style="stroke:{c}"></path>'
                   for y, c in ((9, "#3A2A20"), (17, "#B4583A"), (25, "#3A2A20")))
         + "</svg>")
CHIP = f'<span class="chip" aria-hidden="true">{ARROW}</span>'
AREAS = {"grup": "g", "privat": "p", "consiliere": "c", "retreat": "r", "companii": "o", "copii": "k"}
tiles2 = "".join(f'<a class="tile" href="#{s["k"]}" style="grid-area: {AREAS[s["k"]]}; --i: {i + 1}">{img(s)}<span class="tx">'
                 f'<span class="n">{s["name"]}</span><span class="ln">{s["line"]}</span>{meta(s)}</span>{CHIP}</a>' for i, s in enumerate(ORDER))
OPTS["CFPagina2Bento"] = ("Ce oferim 2: bento", "light", """
.c2{background:linear-gradient(180deg,#F4EDE4 0%,#EDE1CF 100%);padding:150px 0 120px}
.c2 .bento{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));grid-auto-rows:150px;gap:16px;
  grid-template-areas:"i i i g g g" "i i i g g g" "i i i g g g" "p p c c r r" "p p c c r r" "o o o o k k" "o o o o k k"}
.c2 .intro{grid-area:i;display:flex;flex-direction:column;justify-content:flex-end;padding:44px;border-radius:30px;corner-shape:squircle;
  background:radial-gradient(ellipse 80% 70% at 20% 0%,#FBF6EE 0%,rgba(251,246,238,0) 70%),#E9DCC8}
.c2 .orn{display:block;width:96px;height:28px;margin-bottom:auto;fill:none;stroke-width:2.2px;stroke-linecap:round}
.c2 .lede{margin-top:22px;max-width:30ch}
.c2 .tile{position:relative;isolation:isolate;display:flex;flex-direction:column;justify-content:flex-end;overflow:hidden;padding:30px;border-radius:30px;corner-shape:squircle;color:#F4EDE4;background:#5B3A27}
.c2 .tile img{position:absolute;inset:0;z-index:-2;width:100%;height:100%;object-fit:cover;transition:scale 1.2s var(--so)}
.c2 .tile::before{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(26,13,8,0) 30%,rgba(26,13,8,.78) 100%)}
.c2 .tile::after{content:"";position:absolute;inset:0;z-index:-1;opacity:0;transition:opacity .5s ease;pointer-events:none;
  background:radial-gradient(circle 260px at var(--x,50%) var(--y,50%),rgba(255,214,160,.38),rgba(255,214,160,0) 70%);mix-blend-mode:soft-light}
.c2 .tile:hover::after{opacity:1}
.c2 .tile:hover img{scale:1.05}
.c2 .tile .n{font-size:30px}
.c2 .tile .ln{color:#EFE3D3;max-width:44ch}
.c2 .tile .m{margin-top:8px;color:var(--glowc)}
.c2 .chip{position:absolute;top:20px;right:20px;display:grid;place-items:center;width:44px;height:44px;border-radius:50%;background:rgba(244,237,228,.92);color:var(--ink);transition:rotate .5s var(--sp),scale .5s var(--sp)}
.c2 .chip .ar{width:18px;height:18px}
.c2 .tile:hover .chip{rotate:-45deg;scale:1.08}
.c2 .tile:focus-visible{outline:2px solid var(--terra-d);outline-offset:4px}
.c2 [style*="grid-area: g"] .n{font-size:42px}
@keyframes c2-open{from{clip-path:inset(12% 12% 12% 12% round 30px);scale:.94;opacity:0}to{clip-path:inset(0 0 0 0 round 30px)}}
.c2.js:not(.in) .tile{opacity:0}
.c2.js.in .tile{animation:c2-open 1s var(--so) backwards;animation-delay:calc(var(--i) * 90ms + 250ms)}
@media (max-width:980px){
  .c2{padding:118px 0 72px}
  .c2 .bento{grid-template-columns:1fr 1fr;grid-auto-rows:auto;gap:12px;grid-template-areas:"i i" "g g" "p c" "r r" "o o" "k k"}
  .c2 .intro{padding:30px 24px 32px;border-radius:26px}.c2 .orn{margin-bottom:36px}
  .c2 .tile{min-height:300px;padding:22px;border-radius:26px}.c2 .tile .n,.c2 [style*="grid-area: g"] .n{font-size:28px}
  .c2 [style*="grid-area: p"],.c2 [style*="grid-area: c"]{min-height:340px;padding:18px}
  .c2 [style*="grid-area: p"] .n,.c2 [style*="grid-area: c"] .n{font-size:22px}
  .c2 [style*="grid-area: p"] .ln,.c2 [style*="grid-area: c"] .ln{font-size:14px}
  .c2 [style*="grid-area: p"] .chip,.c2 [style*="grid-area: c"] .chip{top:14px;right:14px}
}
""", '<section class="cp c2" aria-labelledby="cp-h" ref="{{ secRef }}"><div class="wrap"><div class="bento">'
   + f'<div class="intro">{RINGS}{h1()}<p class="lede up">{LEDE}</p></div>{tiles2}</div></div></section>',
   script(mount="""
    this.move = function (e) {
      var t = e.target.closest && e.target.closest('.tile'); if (!t || e.pointerType !== 'mouse') return;
      var r = t.getBoundingClientRect(); t.style.setProperty('--x', (e.clientX - r.left) + 'px'); t.style.setProperty('--y', (e.clientY - r.top) + 'px');
    };
    s.addEventListener('pointermove', this.move);""",
          unmount="if (this.sec && this.move) this.sec.removeEventListener('pointermove', this.move);"))

# 3. Drum (Duolingo's lesson path): the services as round, pressable buttons on a winding stitched path, starting with
#    the group workshop („cel mai simplu început”, from the Acasă FAQ). The path draws itself, each button pops up when
#    the line reaches it, a woodsprite keeps walking the path; pressing a button sinks it like Duolingo's 3D buttons.
#    Desktop: the path runs left to right. Phone: it winds down the page.
DX = [100 + 200 * i for i in range(6)]
DY = [250 if i % 2 == 0 else 400 for i in range(6)]
DPATH = f"M{DX[0]} {DY[0]}" + "".join(f"C{DX[i - 1] + 100} {DY[i - 1]} {DX[i] - 100} {DY[i]} {DX[i]} {DY[i]}" for i in range(1, 6))
MX = [58 if i % 2 == 0 else 292 for i in range(6)]
MY = [130 + 260 * i for i in range(6)]
MPATH = f"M{MX[0]} {MY[0]}" + "".join(f"C{MX[i - 1]} {MY[i - 1] + 140} {MX[i]} {MY[i] - 140} {MX[i]} {MY[i]}" for i in range(1, 6))


def road(cls, vb, d):
    return (f'<svg class="road {cls}" viewBox="{vb}" aria-hidden="true"><defs><mask id="cp-m-{cls}"><path class="draw" d="{d}" pathLength="1"></path></mask></defs>'
            f'<path class="bed" d="{d}"></path><path class="dash" d="{d}" mask="url(#cp-m-{cls})"></path>'
            f'<circle class="spr" r="7"><animateMotion dur="14s" repeatCount="indefinite" path="{d}" begin="2.6s"></animateMotion></circle></svg>')


nodes3 = "".join(
    f'<li class="st{" lo" if i % 2 else " hi"}" style="--i: {i}; --x: {DX[i] / 12:.3f}%; --y: {DY[i] / 6.6:.3f}%">'
    f'<a href="#{s["k"]}"><span class="bt">{img(s)}</span>'
    + ('<span class="start">Cel mai simplu început</span>' if i == 0 else "")
    + f'<span class="lb"><span class="n">{s["name"]}</span><span class="ln">{s["line"]}</span>{meta(s)}</span></a></li>' for i, s in enumerate(ORDER))
OPTS["CFPagina3Drum"] = ("Ce oferim 3: drumul", "light", """
.c3{background:radial-gradient(ellipse 50% 50% at 15% 10%,#FAF4EA 0%,rgba(250,244,234,0) 70%),linear-gradient(180deg,#F4EDE4 0%,#ECDFCB 100%);padding:176px 0 96px}
.c3 .head{display:grid;grid-template-columns:auto minmax(0,1fr);gap:0 80px;align-items:end}
.c3 .lede{max-width:38ch;padding-bottom:14px}
.c3 .map{position:relative;margin:40px 0 0;aspect-ratio:1200/660}
.c3 .road{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.c3 .road.mob{display:none}
.c3 .bed{fill:none;stroke:rgba(156,71,44,.10);stroke-width:26;stroke-linecap:round}
.c3 .dash{fill:none;stroke:var(--clay);stroke-width:3.5;stroke-dasharray:3 14;stroke-linecap:round}
.c3 .draw{fill:none;stroke:#fff;stroke-width:40;stroke-dasharray:1;stroke-dashoffset:0}
@keyframes c3-draw{from{stroke-dashoffset:1}}
.c3.js.in .draw{animation:c3-draw 2.6s cubic-bezier(.45,.05,.3,1) .4s backwards}
.c3.js:not(.in) .draw{stroke-dashoffset:1}
.c3 .spr{fill:#FFF6E6;filter:drop-shadow(0 0 6px rgba(255,214,150,.95)) drop-shadow(0 0 16px rgba(255,190,120,.7))}
.c3 ol{margin:0;padding:0;list-style:none}
.c3 .st{position:absolute;left:var(--x);top:var(--y);width:190px;margin-left:-95px}
.c3 .st a{display:flex;flex-direction:column;align-items:center;text-align:center;color:var(--ink)}
.c3 .bt{position:relative;z-index:1;display:block;width:124px;height:124px;margin-top:-62px;border-radius:50%;overflow:hidden;border:5px solid #F8F1E7;
  box-shadow:0 9px 0 #9C472C,0 22px 30px -12px rgba(58,30,15,.55);transition:translate .18s ease-out,box-shadow .18s ease-out}
.c3 .bt img{display:block;width:100%;height:100%;object-fit:cover;transition:scale .8s var(--so)}
.c3 .st a:hover .bt img{scale:1.08}
.c3 .st a:active .bt{translate:0 6px;box-shadow:0 3px 0 #9C472C,0 10px 16px -10px rgba(58,30,15,.5)}
.c3 .st a:focus-visible{outline:none}.c3 .st a:focus-visible .bt{outline:3px solid var(--terra-d);outline-offset:6px}
.c3 .lb{display:block;padding-top:24px;transition:translate .45s var(--sp)}
.c3 .st a:hover .lb{translate:0 -4px}
.c3 .hi .lb{position:absolute;bottom:calc(100% + 76px);padding:0}
.c3 .n{font-size:25px}
.c3 .ln{font-size:14px;margin-top:6px}
.c3 .m{margin-top:6px;font-size:13px}
.c3 .start{position:absolute;left:50%;top:76px;z-index:2;translate:-50% 0;padding:9px 14px;border-radius:14px;background:var(--ink);color:#F4EDE4;font-size:13px;font-weight:500;white-space:nowrap;
  animation:c3-bob 2.4s ease-in-out infinite}
.c3 .start::before{content:"";position:absolute;left:50%;top:-6px;width:12px;height:12px;margin-left:-6px;background:inherit;rotate:45deg;border-radius:2px}
@keyframes c3-bob{50%{translate:-50% 6px}}
@keyframes c3-pop{from{scale:.2;opacity:0}60%{opacity:1}}
@keyframes c3-lb{from{opacity:0;translate:0 12px}}
.c3.js:not(.in) .st{opacity:0}
.c3.js.in .bt{animation:c3-pop .7s var(--sp) backwards;animation-delay:calc(.5s + var(--i) * 400ms)}
.c3.js.in .lb{animation:c3-lb .7s var(--so) backwards;animation-delay:calc(.7s + var(--i) * 400ms)}
.c3.js.in .start{animation:c3-lb .7s var(--so) 1s backwards,c3-bob 2.4s ease-in-out 1.7s infinite}
@media (max-width:980px){
  .c3{padding:128px 0 64px}.c3 .head{grid-template-columns:1fr;gap:20px}.c3 .lede{padding:0}
  .c3 .map{aspect-ratio:auto;margin-top:36px}
  .c3 .road.desk{display:none}.c3 .road.mob{display:block;height:auto;aspect-ratio:350/1560}
  .c3 .st{position:relative;left:auto;top:auto;width:auto;height:260px;margin:0}
  .c3 .st a{flex-direction:row;align-items:center;gap:18px;height:100%;text-align:left}
  .c3 .lo a{flex-direction:row-reverse;text-align:right}
  .c3 .bt{flex:none;width:104px;height:104px;margin:0}
  .c3 .lb,.c3 .hi .lb{position:static;padding:0;flex:1 1 0;min-width:0}
  .c3 .n{font-size:23px}
  .c3 .start{left:52px;top:auto;bottom:calc(50% - 108px);font-size:12px;padding:7px 11px}
}
""", '<section class="cp c3" aria-labelledby="cp-h" ref="{{ secRef }}"><div class="wrap"><div class="head">' + h1()
   + f'<p class="lede up">{LEDE}</p></div><div class="map">{road("desk", "0 0 1200 660", DPATH)}{road("mob", "0 0 350 1560", MPATH)}<ol>{nodes3}</ol></div></div></section>',
   script(mount="""
    if (reduce) [].forEach.call(s.querySelectorAll('svg.road'), function (g) { if (g.pauseAnimations) { g.pauseAnimations(); g.setCurrentTime(0); } g.querySelector('.spr').style.display = 'none'; });"""))

# 4. Cover Flow (iTunes, 2006): the services as photo covers turning in 3D on a dark clay-lit stage, with a reflection
#    on the floor. Drag or swipe and they follow your hand (continuous, lerped); let go and they settle on the nearest.
#    Click a side cover, use the round arrows or ← →. The caption under the stage changes with the cover in front.
covers4 = "".join(f'<button class="cv" data-i="{i}" aria-label="{s["name"]}" style="--i: {i}" tabindex="-1">{img(s, " draggable=\"false\"")}</button>' for i, s in enumerate(ORDER))
caps4 = "".join(f'<div class="cap" data-i="{i}"><span class="n">{s["name"]}</span><span class="ln">{s["line"]}</span>{meta(s)}'
                f'<a class="go" href="#{s["k"]}">{s["cta"]} {ARROW}</a></div>' for i, s in enumerate(ORDER))
NAVB = ('<button class="nb prev" aria-label="Serviciul anterior"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8L10 13" fill="none" stroke="currentColor" style="stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"></path></svg></button>'
        '<button class="nb next" aria-label="Serviciul următor"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3L11 8L6 13" fill="none" stroke="currentColor" style="stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round"></path></svg></button>')
OPTS["CFPagina4CoverFlow"] = ("Ce oferim 4: cover flow", "dark", """
.c4{background:radial-gradient(ellipse 46% 40% at 50% 62%,rgba(255,190,130,.16) 0%,rgba(255,190,130,0) 70%),linear-gradient(180deg,#3A2418 0%,#24150E 100%);color:#F4EDE4;padding:176px 0 96px;text-align:center}
.c4 .cph{color:#F4EDE4}
.c4 .lede{max-width:44ch;margin:26px auto 0;color:#EFE3D3}
.c4 .stage{position:relative;height:430px;margin-top:44px;perspective:1300px;touch-action:pan-y;cursor:grab;user-select:none}
.c4 .stage.drag{cursor:grabbing}
.c4 .cv{position:absolute;left:50%;top:20px;width:320px;height:320px;margin-left:-160px;padding:0;border:0;border-radius:10px;background:#5B3A27;cursor:pointer;
  transform-style:preserve-3d;transition:transform .75s var(--so),filter .75s var(--so);-webkit-box-reflect:below 4px linear-gradient(transparent 58%,rgba(255,255,255,.2))}
.c4 .stage.drag .cv{transition:none}
.c4 .cv img{display:block;width:100%;height:100%;object-fit:cover;border-radius:10px;pointer-events:none}
.c4 .cv:focus-visible{outline:2px solid var(--glowc);outline-offset:6px}
@keyframes c4-in{from{opacity:0;scale:.6;translate:0 60px}}
.c4.js:not(.in) .cv{opacity:0}
.c4.js.in .cv{animation:c4-in 1s var(--sp) backwards;animation-delay:calc(.35s + var(--i) * 90ms)}
.c4 .ctl{display:flex;align-items:flex-start;justify-content:center;gap:28px;margin-top:6px}
.c4 .nb{flex:none;display:grid;place-items:center;width:48px;height:48px;margin-top:4px;border:1px solid rgba(244,237,228,.3);border-radius:50%;background:rgba(244,237,228,.06);color:#F4EDE4;cursor:pointer;transition:background .25s ease,scale .4s var(--sp)}
.c4 .nb:hover{background:rgba(244,237,228,.16);scale:1.06}
.c4 .nb svg{width:18px;height:18px}
.c4 .caps{position:relative;width:min(560px,100%);min-height:220px}
.c4 .cap{position:absolute;inset:0 0 auto;opacity:0;visibility:hidden;translate:0 10px;transition:opacity .35s ease,translate .5s var(--so),visibility 0s .35s}
.c4 .cap .n{font-size:40px}
.c4 .cap .ln{color:#EFE3D3;font-size:16px;margin:10px auto 0;max-width:46ch}
.c4 .cap .m{margin-top:10px;color:var(--glowc)}
.c4 .go{display:inline-flex;align-items:center;gap:10px;min-height:46px;margin-top:18px;padding:0 22px;border-radius:999px;background:#F4EDE4;color:#2E1D14;font-weight:500}
.c4 .go:hover .ar{transform:translateX(4px)}
""" + "".join(f'.c4[data-a="{i}"] .cap[data-i="{i}"]{{opacity:1;visibility:visible;translate:none;transition:opacity .45s ease .12s,translate .6s var(--so) .12s,visibility 0s}}' for i in range(6)) + """
@media (max-width:980px){
  .c4{padding:128px 0 64px}.c4 .lede{margin-top:18px}
  .c4 .stage{height:300px;margin-top:28px}.c4 .cv{width:210px;height:210px;margin-left:-105px;top:16px}
  .c4 .ctl{flex-wrap:wrap;gap:12px}.c4 .nb{width:44px;height:44px;margin-top:0}.c4 .caps{order:-1;flex-basis:100%;min-height:236px}.c4 .go{white-space:nowrap}.c4 .cap .n{font-size:30px}.c4 .cap .ln{font-size:15px}
}
""", '<section class="cp c4" data-a="0" aria-labelledby="cp-h" aria-roledescription="carusel" ref="{{ secRef }}"><div class="wrap">' + h1()
   + f'<p class="lede up">{LEDE}</p><div class="stage">{covers4}</div>'
   + f'<div class="ctl">{NAVB.split("</button>")[0]}</button><div class="caps" aria-live="polite">{caps4}</div>{NAVB.split("</button>")[1]}</button></div></div></section>',
   script(mount="""
    var st = s.querySelector('.stage'), cv = [].slice.call(s.querySelectorAll('.cv')), n = cv.length, a = 0, pos = 0, drag = null;
    var small = function () { return st.offsetWidth < 700; };
    var lay = function (p) {
      var k = small() ? [118, 58, 90] : [190, 105, 130];
      cv.forEach(function (c, i) {
        var d = i - p, ad = Math.abs(d), sg = d < 0 ? -1 : 1, near = Math.min(ad, 1);
        var x = sg * (k[0] * near + Math.max(ad - 1, 0) * k[1]), z = k[2] * (1 - near) - 60 * near, ry = -sg * 58 * near;
        c.style.transform = 'translateX(' + x.toFixed(1) + 'px) translateZ(' + z.toFixed(1) + 'px) rotateY(' + ry.toFixed(1) + 'deg)';
        c.style.zIndex = String(100 - Math.round(ad * 10));
        c.style.filter = 'brightness(' + (1 - Math.min(ad, 3) * .14).toFixed(2) + ')';
        c.style.opacity = ad > 3.4 ? '0' : '';
      });
    };
    var go = function (i) { a = Math.max(0, Math.min(n - 1, i)); pos = a; s.setAttribute('data-a', a); lay(a); };
    go(0);
    this.click = function (e) {
      if (e.target.closest('.prev')) return go(a - 1);
      if (e.target.closest('.next')) return go(a + 1);
      var c = e.target.closest('.cv'); if (c && !st.moved) go(+c.getAttribute('data-i'));
    };
    this.key = function (e) { if (e.key === 'ArrowRight') { go(a + 1); e.preventDefault(); } else if (e.key === 'ArrowLeft') { go(a - 1); e.preventDefault(); } };
    this.down = function (e) { drag = { x: e.clientX, p: a }; st.moved = false; };
    this.mv = function (e) {
      if (!drag) return; var dx = e.clientX - drag.x;
      if (!st.moved && Math.abs(dx) < 6) return;
      if (!st.moved) { st.moved = true; st.classList.add('drag'); try { st.setPointerCapture(e.pointerId); } catch (_) {} }
      pos = Math.max(-0.4, Math.min(n - 0.6, drag.p - dx / (small() ? 120 : 190))); lay(pos);
    };
    this.up = function () { if (!drag) return; drag = null; st.classList.remove('drag'); if (st.moved) go(Math.round(pos)); setTimeout(function () { st.moved = false; }, 0); };
    this.resize = function () { lay(a); };
    s.addEventListener('click', this.click); s.addEventListener('keydown', this.key);
    st.addEventListener('pointerdown', this.down); st.addEventListener('pointermove', this.mv); st.addEventListener('pointerup', this.up); st.addEventListener('pointercancel', this.up);
    window.addEventListener('resize', this.resize);
    cv.forEach(function (c) { c.tabIndex = 0; });""",
          unmount="if (this.sec && this.click) { this.sec.removeEventListener('click', this.click); this.sec.removeEventListener('keydown', this.key); window.removeEventListener('resize', this.resize); }"))


# „De ce să alegi AVA Art & Soul?” (Vali, 11 nov): the section right under the hero. The text comes from Vali later;
# until then a visible placeholder. Motion: the site's scroll reveal only.
SOURCES["CFDeCe"] = "secțiune nouă cerută de Vali; textul vine de la Vali"
OPTS["CFDeCe"] = ("Ce oferim: De ce să alegi AVA Art & Soul?", None, """
.cw{background:linear-gradient(180deg,#EFE4D4 0%,#F4EDE4 100%);padding:112px 0 120px}
.cw h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05;max-width:18ch}
.cw .todo{margin:28px 0 0;max-width:52ch;font-size:17px;line-height:1.6;color:var(--terra-d);font-weight:500;letter-spacing:.02em}
@keyframes cw-up{from{opacity:0;translate:0 16px}}
.cw.js:not(.in) :is(h2,.todo){opacity:0}
.cw.js.in :is(h2,.todo){animation:cw-up .8s cubic-bezier(.22,1,.36,1) backwards}
.cw.js.in .todo{animation-delay:80ms}
@media (max-width:980px){.cw{padding:72px 0 80px}.cw .todo{margin-top:20px}}
""", '<section class="cp cw" aria-labelledby="cw-h" ref="{{ secRef }}"><div class="wrap"><h2 class="disp" id="cw-h">De ce să alegi AVA Art &amp; Soul?</h2>'
   '<p class="todo">[TEXTUL PENTRU „DE CE SĂ ALEGI AVA ART &amp; SOUL?”: VINE DE LA VALI]</p></div></section>', script())

def header(tone):
    """Header 1 at the top of the page, static, with „Ce oferim” as the current page"""
    h = header_html("1").replace('data-tone="dark"', f'data-tone="{tone}"').replace('ref="{{ hxRef }}"', 'style="--y: 42px"')
    h = re.sub(r'\s(?:on[A-Z]\w+|ref)="\{\{[^}]*\}\}"', "", h)
    h = h.replace(' aria-current="page"', "").replace('<a href="#ce-facem" aria-haspopup="true">', '<a href="#ce-facem" aria-haspopup="true" aria-current="page">', 1)
    assert 'aria-current="page">Ce oferim' in h
    return h


def page(name, title, tone, css, html, js, w, h):
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
{BASE_CSS}{HX_CSS}{V["1Pastila"]["css"]}{COMMON}{css}</style>
</helmet>
<div class="pg hxv v1" data-src="{SOURCES[name]}">
{header(tone) if tone else ''}
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{js}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"CFPagina1Comutator": (1462, 2535), "CFPagina2Bento": (1416, 2322), "CFPagina3Drum": (1072, 1980), "CFPagina4CoverFlow": (1221, 1008), "CFDeCe": (448, 311)}

if __name__ == "__main__":
    for name, (title, tone, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), tone, css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "cfpagina-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Ce oferim mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:2700px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
