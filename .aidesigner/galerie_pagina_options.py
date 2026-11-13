"""Galerie, the page (Vali, 12 nov). Four variants of the whole page (header + the gallery); the footer comes at assembly.
The doc: three categories, Ateliere (people, hands, atmosphere) · Piese (what people made, Alessia's work) · Retreaturi.
Photos: 4 real (the October workshop) + 7 provisional from Unsplash (their alt text says so). No retreat has happened, so
„Retreaturi” shows a short note instead of a stock cabin passing for one. Every photo opens large (lightbox: arrows, Esc,
swipe on phones); motion stops with prefers-reduced-motion.

usage: python3 .aidesigner/galerie_pagina_options.py
Mine, to approve (MINE): the line under the title, „Toate”, the empty Retreaturi note, the album names, the captions.
"""
import os, subprocess, sys
from about_options2 import P, HERE, ARROW
import grup_hero_options as gh
from galerie_options import IM, IG
from cf_pagina_options import ENTER

TITLE = "Galerie"
LEDE = "Momente de la atelierele noastre: oameni, mâini, lut și ce prinde formă din el."     # MINE
CATS = [("toate", "Toate"), ("ateliere", "Ateliere"), ("piese", "Piese"), ("retreaturi", "Retreaturi")]   # „Toate” MINE
EMPTY = "Pozele de la retreaturi vin după primul retreat."                                   # MINE
IG_LINK = f'<a class="more" href="https://www.instagram.com/ava.art.soul/">{IG} {ARROW}</a>'
HANDS = dict(src=gh.HANDS[0], alt=gh.HANDS[1], pos=gh.HANDS[2], cat="ateliere")
CAP = {"masa": "Atelierul din octombrie", "bol": "Primul bol", "sus": "Masa, văzută de sus", "hands": "Concentrare",
       "pictat": "Pictură pe ceramică", "piese": "După ardere", "maini": "Primele forme", "vas": "Din mână în mână",
       "grup": "Împreună, la lut", "cani": "O pauză de ceai", "copil": "Și cei mici"}    # MINE
ORDER = ["masa", "pictat", "bol", "piese", "hands", "grup", "maini", "sus", "vas", "cani", "copil"]
PH = [dict(IM[k] if k != "hands" else HANDS, k=k, cap=CAP[k]) for k in ORDER]
REAL = {"masa", "bol", "sus", "hands"}


def img(p, i, cls="it", extra=""):
    return (f'<button type="button" class="{cls}" data-c="{p["cat"]}" data-i="{i}" onClick="{{{{ open }}}}" aria-label="Deschide: {p["alt"]}"{extra}>'
            f'<img src="{p["src"]}" alt="{p["alt"]}" style="object-position: {p["pos"]}" loading="lazy"></button>')


def chips():
    return ('<div class="chips" role="group" aria-label="Categorii">' + "".join(
        f'<button type="button" class="chip" data-f="{k}" aria-pressed="{"true" if k == "toate" else "false"}" onClick="{{{{ filt }}}}">{n}</button>' for k, n in CATS) + "</div>")


BOX = ('<div class="lb" role="dialog" aria-modal="true" aria-label="Fotografie" hidden><button type="button" class="x" aria-label="Închide" onClick="{{ close }}">'
       '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8"></path></svg></button>'
       '<button type="button" class="nv pv" aria-label="Fotografia anterioară" onClick="{{ prev }}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3L5 8l5 5"></path></svg></button>'
       '<figure><img alt=""><figcaption></figcaption></figure>'
       '<button type="button" class="nv nx" aria-label="Fotografia următoare" onClick="{{ next }}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3l5 5-5 5"></path></svg></button></div>')

COMMON = """
.gl{position:relative;background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:150px 0 112px;--so:cubic-bezier(.22,1,.36,1)}
.gl a{text-decoration:none}
.gl .lede{margin:20px 0 0;max-width:40ch;color:#4A382C}
.gl .chips{display:flex;flex-wrap:wrap;gap:8px}
.gl .chip{min-height:44px;padding:0 18px;border:0;border-radius:999px;background:#E9DCCA;font:500 15px/1 var(--text);color:#4A382C;cursor:pointer;transition:background-color .2s,color .2s}
.gl .chip:hover{background:#E0D0BB}
.gl .chip[aria-pressed="true"]{background:#3A2A20;color:#F4EDE4}
.gl .chip:focus-visible,.gl .it:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.gl .it{position:relative;display:block;width:100%;padding:0;border:0;background:#E6D5BD;overflow:hidden;cursor:zoom-in}
.gl .it img{display:block;width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--so)}
@media (hover:hover){.gl .it:hover img{transform:scale(1.04)}}
.gl[data-f="ateliere"] [data-c]:not([data-c="ateliere"]),.gl[data-f="piese"] [data-c]:not([data-c="piese"]),.gl[data-f="retreaturi"] [data-c]{display:none}
.gl .empty{display:none;margin:40px 0 0;padding:48px 24px;border:1px dashed rgba(58,42,32,.25);border-radius:22px;text-align:center;font:400 italic 22px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2)}
.gl[data-f="retreaturi"] .empty{display:block}
.gl .foot{display:flex;justify-content:center;margin-top:48px}
@keyframes gl-up{from{opacity:0;translate:0 16px}}
.gl.js:not(.in) .ri{opacity:0}
.gl.js.in .ri{animation:gl-up .8s var(--so) backwards;animation-delay:calc(var(--i,0) * 60ms)}
/* lightbox */
.gl .lb{position:fixed;inset:0;z-index:50;display:grid;grid-template-columns:72px minmax(0,1fr) 72px;align-items:center;padding:24px;background:rgba(28,16,10,.94)}
.gl .lb[hidden]{display:none}
@keyframes gl-fade{from{opacity:0}}
@media (prefers-reduced-motion:no-preference){.gl .lb:not([hidden]){animation:gl-fade .25s ease}.gl .lb figure img{animation:gl-up .35s var(--so)}}
.gl .lb figure{grid-column:2;margin:0;display:flex;flex-direction:column;align-items:center;gap:14px;height:100%;justify-content:center;min-height:0}
.gl .lb img{display:block;max-width:100%;max-height:calc(100vh - 120px);border-radius:10px;object-fit:contain}
.gl .lb figcaption{color:#EFE3D3;font-size:15px;text-align:center;max-width:60ch}
.gl .lb button{display:grid;place-items:center;width:52px;height:52px;border:0;border-radius:50%;background:rgba(244,237,228,.12);color:#F4EDE4;cursor:pointer}
.gl .lb button:hover{background:rgba(244,237,228,.22)}
.gl .lb button:focus-visible{outline:2px solid #F2C79C;outline-offset:2px}
.gl .lb svg{width:18px;height:18px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.gl .lb .x{position:absolute;right:20px;top:20px}
.gl .lb .pv{grid-column:1}.gl .lb .nx{grid-column:3}
@media (max-width:980px){.gl{padding:112px 0 72px}.gl .lb{grid-template-columns:1fr;padding:64px 12px 84px}.gl .lb figure{grid-column:1}
  .gl .lb .pv,.gl .lb .nx{position:absolute;bottom:20px}.gl .lb .pv{left:calc(50% - 64px)}.gl .lb .nx{right:calc(50% - 64px)}}
@media (prefers-reduced-motion:reduce){.gl *{animation:none!important;transition:none!important}}
"""

OPTS = {}
HEAD = f'<h1 class="disp gh" id="gh-h">{TITLE}</h1><p class="lede up" style="--d: .3s">{LEDE}</p>'

# 1. Unsplash / Pinterest: masonry columns, the category chips above, every photo at its own height.
OPTS["Galerie1Zid"] = ("Galerie 1: zid de poze, cu filtre", """
.g1x .top{display:flex;align-items:end;justify-content:space-between;flex-wrap:wrap;gap:24px 40px;margin-bottom:40px}
.g1x .mas{columns:3;column-gap:14px}
.g1x .it{margin:0 0 14px;break-inside:avoid;border-radius:18px;corner-shape:squircle}
.g1x .it:nth-child(3n+1) img{aspect-ratio:4/5}.g1x .it:nth-child(3n+2) img{aspect-ratio:1}.g1x .it:nth-child(3n) img{aspect-ratio:3/4}
.g1x .it:nth-child(4n) img{aspect-ratio:4/3}
@media (max-width:980px){.g1x .top{margin-bottom:24px}.g1x .chips{flex-wrap:nowrap;overflow-x:auto;margin:0 -20px;padding:0 20px;scrollbar-width:none}.g1x .chip{flex:none}.g1x .mas{columns:2;column-gap:8px}.g1x .it{margin-bottom:8px;border-radius:12px}}
""", '<section class="gp gl g1x" data-f="toate" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="top"><div>{HEAD}</div><div class="up" style="--d: .45s">{chips()}</div></div>'
    '<div class="mas">' + "".join(img(p, i, "it ri", f' style="--i: {i}"') for i, p in enumerate(PH)) + f'</div><p class="empty">{EMPTY}</p>'
    f'<div class="foot">{IG_LINK}</div></div>{BOX}</section>')


# 2. Apple Photos, albums: one album per workshop (and one for the pieces); open one to see all its photos.
def stack(ps):
    return "".join(f'<img src="{p["src"]}" alt="" style="object-position: {p["pos"]}">' for p in ps[:3])


ALBUMS = [("toate", "Toate fotografiile", "din toate albumele", PH),   # Vali (13 nov): one more album, first; the grouping comes later
          ("oct", "Atelierul din octombrie", "octombrie 2026", [p for p in PH if p["k"] in REAL]),
          ("piese", "Piese", "ce a prins formă", [p for p in PH if p["cat"] == "piese"]),
          ("altele", "Din alte ateliere", "fotografii provizorii", [p for p in PH if p["cat"] == "ateliere" and p["k"] not in REAL])]   # MINE
OPTS["Galerie2Albume"] = ("Galerie 2: albume", """
.g2x .albs{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:20px;margin-top:48px}
.g2x .alb{display:flex;flex-direction:column;gap:12px;padding:0;border:0;background:none;text-align:left;font:inherit;color:inherit;cursor:pointer}
.g2x .stack{position:relative;aspect-ratio:1;isolation:isolate}
.g2x .stack img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;border-radius:18px;box-shadow:0 18px 30px -22px rgba(58,30,15,.6);transition:rotate .5s var(--so),translate .5s var(--so)}
.g2x .stack img:nth-child(2){z-index:-1;rotate:4deg;translate:6px 2px}.g2x .stack img:nth-child(3){z-index:-2;rotate:-5deg;translate:-6px 4px}
@media (hover:hover){.g2x .alb:hover .stack img:nth-child(2){rotate:8deg;translate:14px 0}.g2x .alb:hover .stack img:nth-child(3){rotate:-9deg;translate:-14px 4px}}
.g2x .alb b{font:400 22px/1.2 var(--display);font-variation-settings:'opsz' 20}
.g2x .alb small{font-size:14px;color:var(--ink2)}
.g2x .alb[aria-pressed="true"] b{color:var(--terra-d)}
.g2x .alb:focus-visible{outline:2px solid #9C472C;outline-offset:6px;border-radius:18px}
.g2x .soon{display:grid;place-items:center;aspect-ratio:1;border:1px dashed rgba(58,42,32,.3);border-radius:18px;padding:20px;text-align:center;font:400 italic 19px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2)}
.g2x .open{margin-top:56px;padding-top:32px;border-top:1px solid rgba(58,42,32,.18)}
.g2x .open h2{font-size:clamp(32px,3vw,44px)}
.g2x .grid{display:none;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin-top:24px}
.g2x .grid.on{display:grid}
.g2x .grid .it{aspect-ratio:1;border-radius:14px}
@media (max-width:980px){.g2x .albs{grid-template-columns:1fr 1fr;gap:20px 14px;margin-top:32px}.g2x .alb b{font-size:19px}.g2x .grid{grid-template-columns:1fr 1fr;gap:8px}.g2x .open{margin-top:40px}}
""", '<section class="gp gl g2x" data-f="toate" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">' + HEAD + '<div class="albs">'
    + "".join(f'<button type="button" class="alb ri" style="--i: {n}" data-a="{k}" aria-pressed="{"true" if n == 0 else "false"}" onClick="{{{{ album }}}}">'
              f'<span class="stack" aria-hidden="true">{stack(ps[3:] if k == "toate" else ps)}</span>'
              f'<b>{t}</b><small>{d} · {len(ps)} fotografii</small></button>' for n, (k, t, d, ps) in enumerate(ALBUMS))
    + f'<div class="alb ri" style="--i: {len(ALBUMS)}"><span class="soon">{EMPTY}</span><b>Retreaturi</b><small>în curând</small></div></div>'
    + '<div class="open">' + "".join(
        f'<div class="grid{" on" if n == 0 else ""}" data-a="{k}"><h2 class="disp" style="grid-column: 1 / -1">{t}</h2>'
        + "".join(img(p, PH.index(p)) for p in ps) + "</div>" for n, (k, t, d, ps) in enumerate(ALBUMS))
    + f'</div><div class="foot">{IG_LINK}</div></div>{BOX}</section>')

# 3. Kinfolk photo essays: a few photos large, others small, with short captions, an asymmetric rhythm.
SPANS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
OPTS["Galerie3Eseu"] = ("Galerie 3: eseu foto", """
.g3x .top{display:flex;align-items:end;justify-content:space-between;flex-wrap:wrap;gap:24px 40px;margin-bottom:48px}
.g3x .ess{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:20px;align-items:start}
.g3x figure{margin:0}
.g3x figcaption{margin-top:10px;font:400 italic 17px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--ink2)}
.g3x .it{border-radius:6px}
.g3x .a{grid-column:1/8}.g3x .a .it{aspect-ratio:4/3}
.g3x .b{grid-column:9/13;margin-top:120px}.g3x .b .it{aspect-ratio:4/5}
.g3x .c{grid-column:2/6}.g3x .c .it{aspect-ratio:3/4}
.g3x .d{grid-column:7/13;margin-top:80px}.g3x .d .it{aspect-ratio:3/2}
.g3x .e{grid-column:1/5}.g3x .e .it{aspect-ratio:1}
.g3x .f{grid-column:5/13}.g3x .f .it{aspect-ratio:16/9}
.g3x .g{grid-column:3/7;margin-top:40px}.g3x .g .it{aspect-ratio:4/5}
.g3x .h{grid-column:8/12;margin-top:140px}.g3x .h .it{aspect-ratio:1}
.g3x .i{grid-column:1/7}.g3x .i .it{aspect-ratio:3/2}
.g3x .j{grid-column:7/10;margin-top:60px}.g3x .j .it{aspect-ratio:3/4}
.g3x .k{grid-column:10/13;margin-top:160px}.g3x .k .it{aspect-ratio:3/4}
.g3x[data-f="ateliere"] figure:not(:has([data-c="ateliere"])),.g3x[data-f="piese"] figure:not(:has([data-c="piese"])),.g3x[data-f="retreaturi"] figure{display:none}
.g3x[data-f]:not([data-f="toate"]) figure{grid-column:auto/span 4!important;margin-top:0!important}
@media (max-width:980px){.g3x .top{margin-bottom:28px}.g3x .chips{flex-wrap:nowrap;overflow-x:auto;margin:0 -20px;padding:0 20px;scrollbar-width:none}.g3x .chip{flex:none}
  .g3x .ess{grid-template-columns:1fr 1fr;gap:16px 10px}.g3x .ess figure{grid-column:auto!important;margin-top:0!important}
  .g3x .ess figure:nth-child(3n+1){grid-column:1/-1!important}.g3x figcaption{font-size:15px}}
""", '<section class="gp gl g3x" data-f="toate" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="top"><div>{HEAD}</div><div class="up" style="--d: .45s">{chips()}</div></div><div class="ess">'
    + "".join(f'<figure class="{SPANS[i]} ri" style="--i: {i}">{img(p, i)}<figcaption>{p["cap"]}</figcaption></figure>' for i, p in enumerate(PH))
    + f'</div><p class="empty">{EMPTY}</p><div class="foot">{IG_LINK}</div></div>{BOX}</section>')

# 4. instagram.com, a profile: the avatar and the handle on top, the category tabs, a tight square grid.
OPTS["Galerie4Profil"] = ("Galerie 4: ca un profil de Instagram", """
.g4x .prof{display:flex;align-items:center;gap:28px;padding-bottom:28px;border-bottom:1px solid rgba(58,42,32,.15)}
.g4x .av{flex:none;width:112px;height:112px;border-radius:50%;padding:4px;background:conic-gradient(#B4583A,#E2A65F,#C07A4E,#B4583A)}
.g4x .av span{display:block;width:100%;height:100%;border-radius:50%;overflow:hidden;box-shadow:0 0 0 3px #F4EDE4;background:#E6D5BD}
.g4x .av img{display:block;width:100%;height:100%;object-fit:cover;object-position:50% 8%}
.g4x .gh{font-size:clamp(48px,5vw,72px)}
.g4x .lede{margin-top:8px;font-size:19px}
.g4x .prof .more{margin-top:6px}
.g4x .tabs{display:flex;justify-content:center;gap:4px;margin:0 0 20px;border-top:1px solid transparent}
.g4x .chip{background:none;border-radius:0;box-shadow:inset 0 2px 0 transparent;min-height:52px;letter-spacing:.06em;text-transform:uppercase;font-size:13px;font-weight:600;color:var(--ink2)}
.g4x .chip:hover{background:none;color:var(--ink)}
.g4x .chip[aria-pressed="true"]{background:none;color:var(--ink);box-shadow:inset 0 2px 0 #3A2A20}
.g4x .sq{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px;max-width:960px;margin:0 auto}
.g4x .it{aspect-ratio:4/5}
.g4x .empty{max-width:960px;margin:0 auto}
@media (max-width:980px){.g4x .prof{gap:16px}.g4x .av{width:76px;height:76px}.g4x .gh{font-size:44px}.g4x .lede{font-size:16px}.g4x .chip{padding:0 10px;font-size:12px}.g4x .sq{gap:2px;margin:0 -20px}}
""", '<section class="gp gl g4x" data-f="toate" aria-labelledby="gh-h" ref="{{ secRef }}"><div class="wrap">'
    f'<div class="prof up" style="--d: .1s"><span class="av"><span><img src="{gh.BOWL[0]}" alt="" style="object-position: 50% 40%"></span></span><div>'
    f'<h1 class="disp gh" id="gh-h">{TITLE}</h1><p class="lede">{LEDE}</p>{IG_LINK}</div></div>'
    + chips().replace('class="chips"', 'class="chips tabs"') + '<div class="sq">' + "".join(img(p, i, "it ri", f' style="--i: {i}"') for i, p in enumerate(PH))
    + f'</div><p class="empty">{EMPTY}</p></div>{BOX}</section>')

SOURCES = {
    "Galerie1Zid": "unsplash.com / pinterest.com: zid de poze pe coloane, fiecare cu înălțimea ei, filtrele deasupra",
    "Galerie2Albume": "Apple Photos, albumele: câte un album pentru fiecare atelier; îl deschizi și vezi toate pozele",
    "Galerie3Eseu": "Kinfolk, eseurile foto: câteva poze mari, altele mici, cu legende scurte, într-un ritm asimetric",
    "Galerie4Profil": "instagram.com, un profil: titlul sus, filele cu categorii, grila strânsă de poze",
}

DATA = "var GL = " + __import__("json").dumps([{"src": p["src"], "alt": p["alt"], "c": p["cat"]} for p in PH], ensure_ascii=False) + ";\n"
HANDLERS = """
    open: function (e) { self.show(+e.currentTarget.getAttribute('data-i'), e.currentTarget); },
    close: function () { self.hide(); },
    prev: function () { self.step(-1); }, next: function () { self.step(1); },
    filt: function (e) { var b = e.currentTarget, s = self.sec;
      s.querySelectorAll('.chip').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.setAttribute('data-f', b.getAttribute('data-f')); },
    album: function (e) { var b = e.currentTarget, s = self.sec, a = b.getAttribute('data-a');
      s.querySelectorAll('.alb[data-a]').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      s.querySelectorAll('.grid').forEach(function (g) { g.classList.toggle('on', g.getAttribute('data-a') === a); }); },"""
METHODS = """
  visible() { var s = this.sec; return Array.prototype.filter.call(s.querySelectorAll('.it[data-i]'), function (b) { return b.offsetParent !== null; })
      .map(function (b) { return +b.getAttribute('data-i'); }).filter(function (v, i, a) { return a.indexOf(v) === i; }); }
  show(i, from) { var s = this.sec, lb = s.querySelector('.lb'); this.i = i; this.from = from || this.from; this.list = this.visible();
    if (this.list.indexOf(i) < 0) this.list = [i];
    lb.querySelector('img').src = GL[i].src; lb.querySelector('img').alt = GL[i].alt; lb.querySelector('figcaption').textContent = GL[i].alt;
    lb.hidden = false; lb.querySelector('.x').focus({ preventScroll: true }); }
  hide() { var lb = this.sec.querySelector('.lb'); lb.hidden = true; if (this.from) this.from.focus({ preventScroll: true }); }
  step(d) { var l = this.list || [this.i], k = (l.indexOf(this.i) + d + l.length) % l.length; this.show(l[k]); }"""
KEYS = """
    var me = this; this.key = function (e) { var lb = s.querySelector('.lb'); if (!lb || lb.hidden) return;
      if (e.key === 'Escape') me.hide(); else if (e.key === 'ArrowLeft') me.step(-1); else if (e.key === 'ArrowRight') me.step(1); };
    document.addEventListener('keydown', this.key);
    var lb = s.querySelector('.lb'), x0 = null;
    lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) { if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) me.step(dx < 0 ? 1 : -1); x0 = null; });"""


def script():
    return (DATA + "class Component extends DCLogic {\n  componentDidMount() {" + ENTER + KEYS + "\n  }\n"
            "  componentWillUnmount() { if (this.io) this.io.disconnect(); if (this.key) document.removeEventListener('keydown', this.key); }\n" + METHODS + "\n"
            "  renderVals() { var self = this; if (!this.cb) this.cb = {" + HANDLERS + " secRef: function (el) { self.sec = el; } }; return this.cb; }\n}")


H = {"Galerie1Zid": (2284, 1725), "Galerie2Albume": (1991, 2526), "Galerie3Eseu": (3411, 3090), "Galerie4Profil": (2147, 1106)}

if __name__ == "__main__":
    gh.SOURCES.update(SOURCES)
    gh.script = lambda *a, **k: script()   # the page() helper takes the script from the module
    for name, (title, css, html) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            doc = gh.page(name, title + (" · mobil" if suffix else ""), "light", COMMON + css, html, w, h)
            doc = doc.replace('<a href="#ce-facem" aria-haspopup="true" aria-current="page">', '<a href="#ce-facem" aria-haspopup="true">')
            doc = doc.replace('<a href="#galerie">', '<a href="#galerie" aria-current="page">')
            open(f, "w", encoding="utf-8").write(doc)
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
