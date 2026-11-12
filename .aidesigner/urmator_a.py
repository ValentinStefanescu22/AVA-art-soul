"""'Următorul atelier', the chosen variant A (story + bilet), now SOLD OUT (Vali, 10 nov):
- the story starts from the first frame each time it comes into view, and starts over after the last one;
- on a laptop it has the round arrows of a real Instagram story, outside the card (on a phone: tap, as before).
Sold-out wording comes from the Evenimente FAQ in docs/continut-site.md ('Ce fac dacă nu mai sunt locuri?').
B-D stay in the archive as urmator_options.py made them; this script rewrites only UrmatorulA(+Mobil).

usage: python3 .aidesigner/urmator_a.py
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
from urmator_options import (COMMON, H, TITLE, DATE, WHERE, PRICE, PRICE_NOTE, WHO, FRAMES, IMGS, N, STAMP, LINK_ICON, states)

SOLD = "Sold out"
WAIT = "Intră pe lista de așteptare"
WAIT_NOTE = "Dacă se eliberează un loc, te anunțăm primii."
CHEV = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3.5L10.5 8L6 12.5" fill="none" stroke="currentColor" style="stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"></path></svg>'


def story():
    imgs = "".join(f'<img class="i{k}" src="{s}" alt="{a}" style="object-position:{p}">' for k, (s, a, p) in enumerate(IMGS))
    bars = "".join(f'<span class="bar b{k}"><i></i></span>' for k in range(N))
    frs = []
    for k, (kind, text) in enumerate(FRAMES):
        if kind == "cover":
            frs.append(f'<div class="fr f{k} cover"><span class="so">{SOLD}</span><p class="k">duminică · 15 noiembrie · ora 17:00</p>'
                       f'<p class="t">{TITLE}</p><p class="w">{WHERE}</p></div>')
        elif kind == "end":
            frs.append(f'<div class="fr f{k}"><p class="t">{text}</p><p class="w">{PRICE} · {SOLD}</p>'
                       f'<a class="stk" href="#contact">{LINK_ICON}Lista de așteptare</a></div>')
        else:
            frs.append(f'<div class="fr f{k}"><p class="t">{text}</p></div>')
    return (f'<div class="sw">'
            f'<button class="arw pv" type="button" aria-label="Cadrul anterior" data-d="-1" onClick="{{{{ step }}}}">{CHEV}</button>'
            f'<div class="sy" onPointerDown="{{{{ hold }}}}" onPointerUp="{{{{ release }}}}" onPointerLeave="{{{{ release }}}}" onPointerCancel="{{{{ release }}}}">'
            f'<div class="ph">{imgs}</div><span class="shade" aria-hidden="true"></span>'
            f'<div class="bars" aria-hidden="true">{bars}</div>'
            f'<div class="who" aria-hidden="true"><img src="{STAMP}" alt="">ava.art.soul <span>· 15 nov</span></div>'
            f'<button class="nav p" type="button" aria-label="Cadrul anterior" data-d="-1" onClick="{{{{ step }}}}" tabindex="-1"></button>'
            f'<button class="nav n" type="button" aria-label="Cadrul următor" data-d="1" onClick="{{{{ step }}}}" tabindex="-1"></button>'
            f'{"".join(frs)}</div>'
            f'<button class="arw nx" type="button" aria-label="Cadrul următor" data-d="1" onClick="{{{{ step }}}}">{CHEV}</button></div>')


DL = (f'<dl class="dl"><div><dt>Unde</dt><dd>{WHERE}</dd></div><div><dt>Preț</dt><dd class="num">{PRICE}</dd></div>'
      f'<div><dt>Locuri</dt><dd>Toate cele 8 locuri sunt ocupate</dd></div><div><dt>Facilitează</dt><dd>{WHO}</dd></div></dl>')
CSS = """
.ua{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.ua .grid{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:120px;align-items:center}
.ua .l{display:flex;flex-direction:column;gap:22px}
.ua .l h2{margin-bottom:18px}
.ua .tr{display:flex;align-items:center;flex-wrap:wrap;gap:12px 18px}
.ua .badge{display:inline-flex;align-items:center;min-height:30px;padding:0 14px;border-radius:999px;border:1px solid #9C472C;color:#9C472C;font-size:14px;font-weight:600;letter-spacing:.02em}
.ua .dl{margin-top:10px}
.ua .buy{margin-top:16px}
.ua .wait{display:inline-flex;align-items:center;gap:12px;min-height:52px;padding:0 28px;border-radius:999px;border:1.5px solid #9C472C;background:#9C472C;color:#F4EDE4;font-weight:500;text-decoration:none;transition:background .25s,border-color .25s}
.ua .wait:hover{background:var(--ink);border-color:var(--ink)}  /* Vali (11 nov): filled, so it stands out from the sand */.ua .wait:hover .ar{transform:translateX(4px)}
.ua .wait:focus-visible{outline:2px solid #9C472C;outline-offset:4px}
.ua .wn{margin:0;font-size:15px;color:var(--ink2)}
/* sold-out sticker on the cover frame */
.sy .so{display:inline-block;margin-bottom:16px;padding:8px 14px 7px;border-radius:10px;background:#9C472C;color:#FBF4EA;font:400 italic 22px/1 var(--display);font-variation-settings:'opsz' 20;transform:rotate(-4deg);box-shadow:0 8px 18px -8px rgba(0,0,0,.5)}
/* laptop arrows, as on Instagram on the web: round, outside the card, hidden where they lead nowhere */
.sw{position:relative}
.arw{position:absolute;top:50%;z-index:3;display:grid;place-items:center;width:32px;height:32px;margin-top:-16px;padding:0;border:0;border-radius:50%;background:rgba(255,255,255,.94);color:#262626;cursor:pointer;box-shadow:0 1px 3px rgba(0,0,0,.18),0 4px 12px -4px rgba(0,0,0,.25);transition:transform .2s cubic-bezier(.2,.7,.2,1),opacity .2s}
.arw::before{content:"";position:absolute;inset:-8px}
.arw svg{width:16px;height:16px}
.arw.pv{left:-48px}.arw.pv svg{transform:rotate(180deg)}
.arw.nx{right:-48px}
.arw:hover{transform:scale(1.08)}
.arw:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
.ua[data-a="0"] .arw.pv{opacity:0;pointer-events:none}
@media (max-width:820px){.arw{display:none}.sw{justify-self:center;width:100%;max-width:360px}
.ua .grid{grid-template-columns:1fr;gap:36px}.ua .l{display:contents}.ua .l h2{order:-3;margin:0}.ua .date{order:-2}.ua .sw{order:-1}.ua .tr{display:none}.ua .l>*{margin:0}.ua .wait{justify-content:center}.ua .wn{text-align:center}}
""" + states(".ua")

HTML = f"""<section class="u ua" id="evenimente" aria-labelledby="u-h" data-a="0" ref="{{{{ rootRef }}}}">
<div class="wrap grid">
<div class="l"><h2 class="disp" id="u-h">{H}</h2><div class="tr"><p class="ttl">{TITLE}</p><span class="badge">{SOLD}</span></div><p class="date">{DATE}</p>
{DL}<p class="note">{PRICE}, {PRICE_NOTE}</p>
<div class="buy"><a class="wait" href="#contact">{WAIT} {ARROW}</a><p class="wn">{WAIT_NOTE}</p></div></div>
{story()}
</div>
</section>"""

JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, r = this.root, reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!r) return;
    this.go(0);
    if (reduce) return;
    // (re)start from the first frame whenever the story comes into view; stop when it leaves
    this.start = function () { self.go(0); r.removeAttribute('data-run'); void r.offsetWidth; r.setAttribute('data-run', ''); };
    this.stop = function () { r.removeAttribute('data-run'); };
    if ('IntersectionObserver' in window) {
      this.io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) self.start(); else self.stop(); }, { threshold: 0.5 });
      this.io.observe(r.querySelector('.sy'));
    } else this.start();
    this.onEnd = function (e) {
      if (e.animationName !== 'syfill') return;
      self.go((parseInt(r.getAttribute('data-a'), 10) + 1) % """ + str(N) + """);
    };
    r.addEventListener('animationend', this.onEnd);
  }
  componentWillUnmount() { if (this.io) this.io.disconnect(); if (this.root && this.onEnd) this.root.removeEventListener('animationend', this.onEnd); }
  renderVals() {
    var self = this, n = """ + str(N) + """;
    if (!this.cb) {
      this.go = function (i) { if (self.root) self.root.setAttribute('data-a', String(i)); };
      this.cb = {
        rootRef: function (el) { self.root = el; },
        step: function (e) {
          var a = parseInt(self.root.getAttribute('data-a'), 10) + parseInt(e.currentTarget.getAttribute('data-d'), 10);
          self.go((a + n) % n);
        },
        hold: function () { if (self.root) self.root.setAttribute('data-hold', ''); },
        release: function () { if (self.root) self.root.removeAttribute('data-hold'); }
      };
    }
    return this.cb;
  }
}"""


def page(title, w, h):
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
{BASE_CSS}{COMMON}{CSS}</style>
</helmet>
<div class="pg">
{HTML}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for suffix, w, h in (("", 1440, 960), ("Mobil", 390, 1400)):
        f = os.path.join(P, f"UrmatorulA{suffix}.dc.html")
        open(f, "w", encoding="utf-8").write(page("Următorul atelier: sold out" + (" · mobil" if suffix else ""), w, h))
    subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), os.path.join(P, "UrmatorulA.dc.html"), os.path.join(HERE, "opt-UrmatorulA.html")], check=True)
