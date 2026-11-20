"""REJECTED by Vali (20 nov 2026): a bar stuck to the bottom doesn't fit the site's elegance. Archived on the canvas
(page „Arhivă: CTA lipit jos pe mobil”); kept for reference, not built.

Sticky mobile CTA (Vali's launch checklist, item 10, 20 nov 2026): four variants, mobile only (on desktop the header
already carries the menu and every page's main button sits in its hero).

Each artboard is a 390×844 phone showing the real Ateliere de grup page (dc-import of the assembled page) scrolled into
„Cum funcționează”, where no other button is on screen, with the bar over it. You can scroll inside it in Play: the bar
appears once the hero button has left the screen and hides again while another main button is visible or at the footer.

Inspired by:
  1. Airbnb (listing page):        full-width bar, date + price on the left, the button on the right
  2. Apple Store (product page):   one floating green pill, nothing else
  3. Aesop (product page):         editorial bar: the service name in Bodoni + the hero's facts
  4. Eventbrite (event page):      a ticket stub, like the tickets in the list, with the seats left

Copy reused from the page: „Mă înscriu”, „Ateliere de grup”, „În fiecare lună”, „de la 200 lei”, the ticket date.
MINE (to approve): „Mai sunt 3 locuri” (would come live from the Worker, E8).

usage: python3 .aidesigner/cta_mobil_options.py
writes canvas/project/CtaMobil{1..4}*.dc.html + local previews .aidesigner/opt-CtaMobil*.html
"""
import os, subprocess
from about_options2 import P, HERE
from acasa_combine import page

W, H = 390, 844
PAGE_H = 7152          # AteliereDeGrup at 390px
START = 3100           # scrollTop of the still: inside „Cum funcționează”, no other button on screen
# Where the page's own main buttons sit at 390px (measured on the assembled page), and where the footer starts.
BUTTONS = [537, 1729, 2153, 2858, 4087]
FOOTER = 5340

BASE = f"""
.cta{{--ink:#3A2A20;--ink2:#6B5444;--paper:#F4EDE4;--acc:#2F5D50;--acc-d:#244A3F;--on:#F8F1E8;--display:'Bodoni Moda',Georgia,serif;--text:'Literata',Georgia,serif;
  position:relative;width:{W}px;height:{H}px;overflow:hidden;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--text);-webkit-font-smoothing:antialiased}}
.cta .scr{{position:absolute;inset:0;overflow-y:auto;overscroll-behavior:contain;scrollbar-width:none}}
.cta .scr::-webkit-scrollbar{{display:none}}
.cta .btn{{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 24px;border-radius:999px;background:var(--acc);color:var(--on);
  font:500 15px/1 var(--text);letter-spacing:.02em;text-decoration:none;white-space:nowrap;transition:background-color .25s ease,scale .15s ease}}
.cta .btn:hover{{background:var(--acc-d)}}.cta .btn:active{{scale:.97}}
.cta .btn:focus-visible{{outline:2px solid #9C472C;outline-offset:3px}}
.cta .bar{{position:absolute;z-index:5;box-sizing:border-box;transition:translate .42s cubic-bezier(.22,1,.36,1),opacity .3s ease}}
.cta .bar:not(.on){{translate:0 calc(100% + 40px);opacity:0;pointer-events:none}}
.cta .num{{font-variant-numeric:tabular-nums}}
/* the iPhone home indicator, so the safe-area padding is visible */
.cta .home{{position:absolute;z-index:6;left:50%;bottom:8px;width:134px;height:5px;margin-left:-67px;border-radius:3px;background:rgba(58,42,32,.85);pointer-events:none}}
@media (prefers-reduced-motion:reduce){{.cta .bar{{transition:opacity .2s ease}}.cta .bar:not(.on){{translate:none}}}}
"""

VARIANTS = [
    dict(name="CtaMobil1Bara", title="CTA mobil 1: bară cu data și prețul (Airbnb)", css="""
.cta .b1{left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:14px;
  padding:12px 16px calc(12px + 34px);background:#FBF7F1;box-shadow:0 -1px 0 rgba(58,42,32,.12),0 -18px 30px -24px rgba(58,30,15,.35)}
.cta .b1 .m{display:flex;flex-direction:column;min-width:0;line-height:1.3}
.cta .b1 .d{font:500 15.5px/1.3 var(--text);color:var(--ink);text-decoration:underline;text-decoration-color:rgba(58,42,32,.3);text-underline-offset:4px}
.cta .b1 .p{font-size:14px;color:var(--ink2)}
""", bar="""<div class="bar b1 on" ref="{{ barRef }}"><div class="m"><span class="d num">duminică, 6 decembrie</span><span class="p num">200 lei · 3 ore</span></div><a class="btn" href="#">Mă înscriu</a></div>"""),
    dict(name="CtaMobil2Pastila", title="CTA mobil 2: pastilă plutitoare (Apple Store)", css="""
.cta .b2{left:16px;right:16px;bottom:calc(14px + 26px);display:flex}
.cta .b2 .btn{flex:1;min-height:54px;font-size:16px;box-shadow:0 0 0 1px rgba(255,255,255,.08) inset,0 14px 30px -12px rgba(36,74,63,.55),0 4px 10px -4px rgba(36,74,63,.35)}
.cta .b2 .btn .p{margin-left:10px;padding-left:10px;border-left:1px solid rgba(248,241,232,.35);font-weight:400;opacity:.9}
""", bar="""<div class="bar b2 on" ref="{{ barRef }}"><a class="btn" href="#">Mă înscriu<span class="p num">de la 200 lei</span></a></div>"""),
    dict(name="CtaMobil3Editorial", title="CTA mobil 3: bară editorială (Aesop)", css="""
.cta .b3{left:0;right:0;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:14px;
  padding:14px 16px calc(14px + 34px);background:rgba(244,237,228,.86);-webkit-backdrop-filter:blur(18px) saturate(1.2);backdrop-filter:blur(18px) saturate(1.2);
  border-top:1px solid rgba(58,42,32,.14)}
.cta .b3 .m{display:flex;flex-direction:column;min-width:0}
.cta .b3 .t{font:400 21px/1.15 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;white-space:nowrap}
.cta .b3 .p{margin-top:3px;font:400 italic 14.5px/1.3 var(--display);font-variation-settings:'opsz' 20;color:#9C472C}
""", bar="""<div class="bar b3 on" ref="{{ barRef }}"><div class="m"><span class="t">Ateliere de grup</span><span class="p num">În fiecare lună · de la 200 lei</span></div><a class="btn" href="#">Mă înscriu</a></div>"""),
    dict(name="CtaMobil4Bilet", title="CTA mobil 4: cotor de bilet (Eventbrite)", css="""
.cta .b4{left:10px;right:10px;bottom:calc(10px + 24px);display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:0 14px;
  padding:10px 10px 10px 18px;border-radius:18px;corner-shape:squircle;background:#FBF7F1;
  box-shadow:0 0 0 1px rgba(58,42,32,.08),0 20px 36px -22px rgba(58,30,15,.55);
  -webkit-mask:radial-gradient(circle 9px at 74px 0,#0000 98%,#000) top/100% 51% no-repeat,radial-gradient(circle 9px at 74px 100%,#0000 98%,#000) bottom/100% 51% no-repeat;
  mask:radial-gradient(circle 9px at 74px 0,#0000 98%,#000) top/100% 51% no-repeat,radial-gradient(circle 9px at 74px 100%,#0000 98%,#000) bottom/100% 51% no-repeat}
.cta .b4 .dt{display:flex;flex-direction:column;align-items:center;width:42px;line-height:1}
.cta .b4 .dt b{font:400 30px/1 var(--display);font-variation-settings:'opsz' 20}
.cta .b4 .dt i{margin-top:3px;font:400 italic 13px/1 var(--display);color:#9C472C}
.cta .b4 .m{display:flex;flex-direction:column;padding-left:14px;border-left:1.5px dashed rgba(58,42,32,.25);line-height:1.3}
.cta .b4 .m span:first-child{font-size:14.5px;font-weight:500}
.cta .b4 .m span+span{font-size:13.5px;color:var(--ink2)}
.cta .b4 .btn{padding:0 20px}
""", bar="""<div class="bar b4 on" ref="{{ barRef }}"><div class="dt"><b class="num">6</b><i>dec</i></div><div class="m"><span>Mai sunt 3 locuri</span><span class="num">200 lei · 3 ore</span></div><a class="btn" href="#">Mă înscriu</a></div>"""),
]

SCRIPT = f"""var BUTTONS = {BUTTONS}, FOOTER = {FOOTER}, H = {H};
class Component extends DCLogic {{
  componentDidMount() {{
    var self = this, s = this.scr; if (!s) return;
    // The assembled page arrives a moment after the artboard (dc-import); then jump to the still.
    // A second, 1px nudge wakes the sections' scroll reveals, which ignore the programmatic jump.
    this.ts = [900, 1600, 2600, 4000].map(function (ms, i) {{
      return setTimeout(function () {{ if (i < 2) s.scrollTop = {START} + i; self.sync(); }}, ms); }});
    this.on = function () {{ if (!self.raf) self.raf = requestAnimationFrame(function () {{ self.raf = 0; self.sync(); }}); }};
    s.addEventListener('scroll', this.on, {{ passive: true }});
  }}
  componentWillUnmount() {{ (this.ts || []).forEach(clearTimeout); if (this.scr) this.scr.removeEventListener('scroll', this.on); cancelAnimationFrame(this.raf); }}
  // Shown once the hero button is gone, hidden while another main button is on screen or at the footer.
  sync() {{
    var y = this.scr.scrollTop, b = this.bar; if (!b) return;
    // The page's header and reveals listen to the window, which doesn't scroll here: drive them from the phone.
    var hx = this.scr.querySelector('.hx');
    if (hx) {{ hx.setAttribute('data-sc', y > 40 ? '1' : '0'); hx.setAttribute('data-tone', y > 740 ? 'light' : 'dark'); }}
    this.scr.querySelectorAll('.js:not(.in)').forEach(function (s) {{ s.classList.add('in'); }});
    var pastHero = y > BUTTONS[0] + 40, other = BUTTONS.slice(1).some(function (t) {{ return t > y + 60 && t < y + H - 120; }});
    b.classList.toggle('on', pastHero && !other && y + H < FOOTER + 140);
  }}
  renderVals() {{ var self = this; if (!this.cb) this.cb = {{
    scrRef: function (el) {{ self.scr = el; }}, barRef: function (el) {{ self.bar = el; }} }}; return this.cb; }}
}}"""


def board(v):
    body = (f'<div class="cta" data-src="{v["title"].split("(")[-1].rstrip(")")}">\n'
            f'<div class="scr" ref="{{{{ scrRef }}}}"><div style="width: {W}px"><dc-import name="AteliereDeGrup" hint-size="{W}px,{PAGE_H}px"></dc-import></div></div>\n'
            f'{v["bar"]}\n<span class="home" aria-hidden="true"></span>\n</div>')
    return page(v["title"], body, W, H, SCRIPT, BASE + v["css"])


if __name__ == "__main__":
    for v in VARIANTS:
        out = os.path.join(P, v["name"] + ".dc.html")
        open(out, "w", encoding="utf-8").write(board(v))
        subprocess.run(["python3", os.path.join(HERE, "dc2html.py"), out, os.path.join(HERE, f"opt-{v['name']}.html")], check=True)
        print("wrote", v["name"])
