"""Formări, round 2: the Wallet family (Vali, 11 nov: „only Formări 4 looks interesting… be creative, smooth animations”).
Four takes on credentials as cards in the brand's colours, each with its own motion and a named source.

usage: python3 .aidesigner/formari_wallet.py
writes .aidesigner/canvas/project/Formari4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Formari4*.html
Motion rules: every entrance runs once, when the section comes into view (IntersectionObserver); every hover/tap
transition is interruptible (CSS transitions or a lerp loop from the current value); prefers-reduced-motion turns all of it off;
without JS nothing is hidden (the hidden start state needs the .js class that the script adds).
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS
from formari_options import ITEMS, CARD, ROT, icon, COMMON as FM_COMMON

H2 = '<h2 class="disp" id="fm-h">Formări</h2>'
N = len(ITEMS)
SOURCES = {
    "Formari4Wallet": "apple.com/wallet: cardurile din Apple Wallet; vecinii se dau la o parte ca în Dock-ul de pe macOS",
    "Formari4BTeanc": "Apple Wallet pe iPhone: teancul de carduri; atingi unul și vine în față",
    "Formari4CEvantai": "Cărțile ținute în mână, ca un evantai; inspirație: apple.com/wallet + Dock-ul macOS",
    "Formari4DHolo": "poke-holo.simey.me (Simon Goellner): cardurile holografice care se înclină după cursor",
}

CSS = FM_COMMON + """
.fm{--spring:cubic-bezier(.3,1.32,.5,1);--soft:cubic-bezier(.22,1,.36,1)}
.fm h2{margin-bottom:56px}
.cd{position:relative;display:flex;flex-direction:column;box-sizing:border-box;width:100%;height:100%;margin:0;padding:24px;border:0;border-radius:26px;corner-shape:squircle;
  background:var(--bg);color:var(--fg);font:inherit;text-align:left;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.16),inset 0 0 0 1px rgba(255,255,255,.06),0 26px 44px -26px rgba(40,20,10,.55),0 6px 14px -8px rgba(40,20,10,.35)}
.cd::after{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;background:linear-gradient(140deg,rgba(255,255,255,.16) 0%,rgba(255,255,255,0) 38%)}
.cd .top{display:flex;justify-content:space-between;align-items:center;gap:12px}
.cd .ic{flex:none;width:30px;height:30px}
.cd .yr{flex:none;font-size:14.5px;font-weight:500;opacity:.85}
.cd .t{display:block;margin:auto 0 0;font:400 23px/1.25 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.cd .w{display:block;margin:12px 0 0;font-size:14.5px;line-height:1.45;opacity:.85}
.fm button.cd{cursor:pointer}
.fm button.cd:focus-visible{outline:2px solid var(--ink);outline-offset:4px}
"""


def card(i, tag="div", band=False, extra=""):
    t, w, d, k = ITEMS[i]
    bt = f'<span class="bt" aria-hidden="true">{t}</span>' if band else ""
    attrs = f' type="button" aria-expanded="false" data-n="{i}"' if tag == "button" else ""
    return (f'<{tag} class="cd"{attrs}{extra} style="--bg: {CARD[i][0]}; --fg: {CARD[i][1]}">'
            f'<span class="top">{icon(k)}{bt}<span class="yr">{d}</span></span>'
            f'<span class="t">{t}</span><span class="w">{w}</span></{tag}>')


# One script for all four: the entrance (IO adds .in once), plus each variant's own bit (/*EXTRA*/).
JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, s = this.sec; if (!s) return;
    var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    s.classList.add('js');
    if (reduce || !window.IntersectionObserver) s.classList.add('in');
    else {
      this.io = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { s.classList.add('in'); self.io.disconnect(); }
      }, { threshold: 0.25 });
      this.io.observe(s);
    }
    /*EXTRA*/
  }
  componentWillUnmount() { if (this.io) this.io.disconnect(); /*UNEXTRA*/ }
  renderVals() {
    var self = this;
    if (!this.cb) this.cb = { secRef: function (el) { self.sec = el; }/*CB*/ };
    return this.cb;
  }
}"""


def js(extra="", unextra="", cb=""):
    return JS.replace("/*EXTRA*/", extra).replace("/*UNEXTRA*/", unextra).replace("/*CB*/", cb)


# a click on a card opens it (aria-expanded); clicking it again, or another one, moves on
PICK_CB = """,
      pick: function (e) {
        var b = e.target.closest && e.target.closest('.cd'); if (!b || !self.sec) return;
        var n = b.getAttribute('data-n'), open = self.sec.getAttribute('data-open') === n;
        self.sec.setAttribute('data-open', open ? '' : n);
        self.sec.querySelectorAll('.cd').forEach(function (c) { c.setAttribute('aria-expanded', !open && c === b ? 'true' : 'false'); });
      }"""

OPTS = {}

# 4. Wallet, now alive: the cards are dealt from one pile into the row; hovering one lifts and straightens it
#    while its neighbours lean away (CSS :has()). Phone: a sideways swipe, one card at a time.
DX = 302
OPTS["Formari4Wallet"] = ("Formări 4: carduri împărțite", """
.fw{background:#F4EDE4;padding:112px 0 128px}
.fw ul{display:flex;justify-content:center;gap:14px;margin:0;padding:0;list-style:none}
.fw li{position:relative;flex:0 0 288px;aspect-ratio:4/5;rotate:var(--r);
  transition:rotate .45s var(--spring),translate .45s var(--spring),scale .45s var(--spring)}
@keyframes fw-deal{from{translate:var(--dx) 40px;rotate:0deg;opacity:0}60%{opacity:1}}
.fw.js:not(.in) li{opacity:0}
.fw.js.in li{animation:fw-deal 1.1s var(--spring) backwards;animation-delay:calc(var(--i) * 110ms)}
@media (hover:hover){
  .fw li:hover{rotate:0deg;translate:0 -18px;scale:1.04;z-index:2}
  .fw li:has(+ li:hover){translate:-18px 4px;rotate:calc(var(--r) - 2deg)}
  .fw li:hover + li{translate:18px 4px;rotate:calc(var(--r) + 2deg)}
}
@media (max-width:1240px){.fw li{flex-basis:250px}.fw .cd .t{font-size:20px}}
@media (max-width:980px){.fw{padding:72px 0 80px}.fw h2{margin-bottom:28px}.fw ul{justify-content:flex-start;overflow-x:auto;scroll-snap-type:x mandatory;padding:12px 20px 24px;margin:0 -20px;scrollbar-width:none}
  .fw li{flex:0 0 78%;rotate:0deg;scroll-snap-align:center}.fw .cd .t{font-size:21px}
  @keyframes fw-up{from{translate:40px 0;opacity:0}}.fw.js.in li{animation-name:fw-up;animation-duration:.8s}}
@media (prefers-reduced-motion:reduce){.fw li{transition:none;animation:none!important}}
""", '<section class="fm fw" aria-labelledby="fm-h" ref="{{ secRef }}"><div class="wrap">' + H2 + "<ul>"
   + "".join(f'<li style="--r: {ROT[i]}deg; --i: {i}; --dx: {(1.5 - i) * DX:.0f}px">{card(i)}</li>' for i in range(N))
   + "</ul></div></section>", js())

# 4B. Teancul: Apple Wallet's stack. The cards arrive piled, then spread so each shows its top band; tap one and it
#     rises to the front, fully open, while the others tuck into a tight pile beneath it. Tap it again to put it back.
BAND, CH, GAP, PEEK = 84, 272, 22, 14
BAND_M, CH_M = 70, 212
rules = []
for k in range(N):
    others = [j for j in range(N) if j != k]
    for j in range(N):
        y = 0 if j == k else f"calc(var(--ch) + {GAP}px + {others.index(j)} * {PEEK}px)"
        sc = 1 if j == k else f"{1 - .03 * (len(others) - others.index(j)):.2f}"
        rules.append(f'.wb[data-open="{k}"] li:nth-child({j + 1}){{translate:0 {y};scale:{sc};z-index:{9 if j == k else 1 + others.index(j)}}}')
    rules.append(f'.wb[data-open="{k}"] li:nth-child({k + 1}) .cd :is(.t,.w){{opacity:1;transition-delay:.15s}}')
OPTS["Formari4BTeanc"] = ("Formări 4B: teancul din Wallet", """
.wb{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 120px;--band:""" + str(BAND) + """px;--ch:""" + str(CH) + """px}
.wb .stage{display:grid;grid-template-columns:minmax(0,1fr) 460px;gap:0 96px;align-items:start}
.wb .stk{position:relative;height:calc(var(--ch) + """ + str(GAP + (N - 2) * PEEK) + """px + var(--ch));margin:0;padding:0;list-style:none}
.wb li{position:absolute;left:0;right:0;top:0;height:var(--ch);translate:0 calc(var(--i) * var(--band));transform-origin:50% 0;
  transition:translate .65s var(--spring),scale .65s var(--spring),top .3s var(--soft)}
.wb .bt{flex:1;min-width:0;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;font:600 15px/1.2 var(--text);opacity:.92}
.wb .cd .t,.wb .cd .w{opacity:0;transition:opacity .35s ease}
.wb:not([data-open]) li:last-child .cd :is(.t,.w),.wb[data-open=""] li:last-child .cd :is(.t,.w){opacity:1;transition-delay:.15s}
@media (hover:hover){.wb:not([data-open]) li:not(:last-child):hover,.wb[data-open=""] li:not(:last-child):hover{top:-10px}}
@keyframes wb-in{from{translate:0 0;opacity:0}30%{opacity:1}}
.wb.js:not(.in) li{opacity:0}
.wb.js.in li{animation:wb-in 1s var(--spring) backwards;animation-delay:calc(150ms + var(--i) * 120ms)}
""" + "".join(rules) + """
@media (max-width:980px){.wb{padding:72px 0 80px;--band:""" + str(BAND_M) + """px;--ch:""" + str(CH_M) + """px}.wb .stage{grid-template-columns:1fr}.wb h2{margin-bottom:28px}.wb .cd{padding:20px}.wb .cd .t{font-size:18px}}
@media (prefers-reduced-motion:reduce){.wb li{transition:none;animation:none!important}}
""", '<section class="fm wb" aria-labelledby="fm-h" ref="{{ secRef }}" onClick="{{ pick }}"><div class="wrap stage">' + H2
   + '<ul class="stk">' + "".join(f'<li style="--i: {i}">{card(i, "button", band=True)}</li>' for i in range(N)) + "</ul></div></section>",
   js(cb=PICK_CB))

# 4C. Evantaiul: the cards are held like a hand of playing cards, fanned around a pivot below them. They open out
#     from one pile; hovering one pulls it up out of the hand and the others lean away; a click lifts it to the front.
ANG = 13
OPTS["Formari4CEvantai"] = ("Formări 4C: evantaiul de cărți", """
.fe{background:radial-gradient(ellipse 50% 60% at 50% 70%,#F8F1E7 0%,rgba(248,241,231,0) 70%),linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 96px}
.fe h2{text-align:center;margin-bottom:64px}
.fe .cd .top{justify-content:flex-start}.fe .cd .t{font-size:21px}
.fe .hand{position:relative;height:500px;max-width:1000px;margin:0 auto;padding:0;list-style:none}
.fe li{position:absolute;left:50%;bottom:24px;width:270px;height:340px;margin-left:-135px;transform-origin:50% 230%;rotate:var(--a);
  transition:rotate .5s var(--spring),translate .5s var(--spring),scale .5s var(--spring),filter .4s ease}
@keyframes fe-open{from{rotate:0deg;translate:0 50px;opacity:0}35%{opacity:1}}
.fe.js:not(.in) li{opacity:0}
.fe.js.in li{animation:fe-open 1.2s var(--spring) backwards;animation-delay:calc(200ms + var(--i) * 90ms)}
@media (hover:hover){
  .fe li:hover{translate:0 -44px;z-index:5}
  .fe li:has(+ li:hover){rotate:calc(var(--a) - 4deg)}
  .fe li:has(+ li + li:hover){rotate:calc(var(--a) - 2deg)}
  .fe li:hover + li{rotate:calc(var(--a) + 4deg)}
  .fe li:hover + li + li{rotate:calc(var(--a) + 2deg)}
}
.fe[data-open]:not([data-open=""]) li{filter:saturate(.8) brightness(.94)}
""" + "".join(f'.fe[data-open="{k}"] li:nth-child({k + 1}){{rotate:0deg;translate:0 -64px;scale:1.08;z-index:9;filter:none}}' for k in range(N)) + """
@media (max-width:980px){.fe{padding:72px 0 80px}.fe h2{text-align:left;margin-bottom:28px}
  .fe .hand{display:flex;gap:14px;height:auto;overflow-x:auto;scroll-snap-type:x mandatory;padding:12px 20px 24px;margin:0 -20px;scrollbar-width:none}
  .fe li,.fe[data-open] li{position:relative;left:auto;bottom:auto;flex:0 0 78%;width:auto;height:auto;aspect-ratio:4/5;margin:0;rotate:0deg!important;translate:none!important;scale:1!important;filter:none!important;scroll-snap-align:center}
  @keyframes fe-up{from{translate:40px 0;opacity:0}}.fe.js.in li{animation-name:fe-up;animation-duration:.8s}}
@media (prefers-reduced-motion:reduce){.fe li{transition:none;animation:none!important}}
""", '<section class="fm fe" aria-labelledby="fm-h" ref="{{ secRef }}" onClick="{{ pick }}"><div class="wrap">' + H2
   + '<ul class="hand">' + "".join(f'<li style="--a: {(i - (N - 1) / 2) * ANG:.1f}deg; --i: {i}">{card(i, "button")}</li>' for i in range(N))
   + "</ul></div></section>", js(cb=PICK_CB))

# 4D. Holo: the cards turn over into place one by one, then tilt in 3D under the cursor with a warm glare and a faint
#     holographic sheen where the light hits (poke-holo). A lerp loop eases every card from where it is, so nothing snaps.
HOLO_JS = js(extra="""
    if (reduce) return;
    var cards = [].slice.call(s.querySelectorAll('.cd')), st = cards.map(function () { return { x: 0, y: 0, o: 0, tx: 0, ty: 0, to: 0 }; }), raf = 0;
    var step = function () {
      raf = 0; var busy = false;
      cards.forEach(function (c, i) {
        var q = st[i];
        q.x += (q.tx - q.x) * 0.12; q.y += (q.ty - q.y) * 0.12; q.o += (q.to - q.o) * 0.12;
        if (Math.abs(q.tx - q.x) + Math.abs(q.ty - q.y) + Math.abs(q.to - q.o) > 0.002) busy = true;
        c.style.setProperty('--rx', (-q.y * 9).toFixed(2) + 'deg'); c.style.setProperty('--ry', (q.x * 11).toFixed(2) + 'deg');
        c.style.setProperty('--mx', (50 + q.x * 50).toFixed(1) + '%'); c.style.setProperty('--my', (50 + q.y * 50).toFixed(1) + '%');
        c.style.setProperty('--o', q.o.toFixed(3));
      });
      if (busy) raf = requestAnimationFrame(step);
    };
    var kick = function () { if (!raf) raf = requestAnimationFrame(step); };
    this.move = function (e) {
      if (e.pointerType !== 'mouse') return;
      var hit = e.target.closest && e.target.closest('.cd');
      cards.forEach(function (c, i) {
        var q = st[i];
        if (c === hit) { var r = c.getBoundingClientRect(); q.tx = ((e.clientX - r.left) / r.width - 0.5) * 2; q.ty = ((e.clientY - r.top) / r.height - 0.5) * 2; q.to = 1; }
        else { q.tx = 0; q.ty = 0; q.to = 0; }
      });
      kick();
    };
    this.leave = function () { st.forEach(function (q) { q.tx = 0; q.ty = 0; q.to = 0; }); kick(); };
    s.addEventListener('pointermove', this.move); s.addEventListener('pointerleave', this.leave);""",
    unextra="if (this.sec && this.move) { this.sec.removeEventListener('pointermove', this.move); this.sec.removeEventListener('pointerleave', this.leave); }")
OPTS["Formari4DHolo"] = ("Formări 4D: carduri holografice", """
.fh{background:radial-gradient(ellipse 60% 70% at 50% 60%,#FAF4EA 0%,rgba(250,244,234,0) 70%),#F4EDE4;padding:112px 0 128px}
.fh ul{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;margin:0;padding:0;list-style:none;perspective:1100px}
.fh li{aspect-ratio:4/5}
.fh .cd{transform:rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg));transform-style:preserve-3d;will-change:transform}
.fh .cd::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;opacity:calc(var(--o,0) * .9);mix-blend-mode:soft-light;
  background:linear-gradient(115deg,transparent 18%,rgba(242,199,156,.9) 36%,rgba(255,250,240,.85) 48%,rgba(192,122,78,.8) 60%,rgba(111,123,92,.7) 72%,transparent 86%) var(--mx,50%) var(--my,50%)/260% 260% no-repeat}
.fh .cd::after{background:radial-gradient(circle at var(--mx,30%) var(--my,20%),rgba(255,244,226,calc(.08 + var(--o,0) * .32)) 0%,rgba(255,244,226,0) 55%),linear-gradient(140deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,0) 38%)}
@keyframes fh-flip{from{transform:rotateY(-110deg) translateZ(-40px);opacity:0}45%{opacity:1}}
.fh.js:not(.in) li{opacity:0}
.fh.js.in li{animation:fh-flip 1.1s var(--spring) backwards;animation-delay:calc(var(--i) * 120ms);transform-origin:0 50%}
@media (hover:none){@keyframes fh-sheen{from{--mx:10%}to{--mx:90%}}}
@media (max-width:1240px){.fh .cd .t{font-size:20px}}
@media (max-width:980px){.fh{padding:72px 0 80px}.fh h2{margin-bottom:28px}.fh ul{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;padding:12px 20px 24px;margin:0 -20px;scrollbar-width:none}.fh li{flex:0 0 78%;scroll-snap-align:center}.fh .cd .t{font-size:21px}}
@media (prefers-reduced-motion:reduce){.fh li{animation:none!important}.fh .cd{transform:none}}
""", '<section class="fm fh" aria-labelledby="fm-h" ref="{{ secRef }}"><div class="wrap">' + H2 + "<ul>"
   + "".join(f'<li style="--i: {i}">{card(i)}</li>' for i in range(N)) + "</ul></div></section>", HOLO_JS)


def page(name, title, css, html, script, w, h):
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
{BASE_CSS}{CSS}{css}</style>
</helmet>
<div class="pg" data-src="{SOURCES[name]}">
{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{script}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"Formari4Wallet": (720, 600), "Formari4BTeanc": (826, 696), "Formari4CEvantai": (835, 600), "Formari4DHolo": (700, 600)}

if __name__ == "__main__":
    for name, (title, css, html, script) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, script, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "wallet-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Wallet mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1000px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
