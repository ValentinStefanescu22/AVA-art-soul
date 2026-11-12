"""Pagina „Despre noi”, part 5: Oamenii care vin la masă (text + workshop photos + short testimonials).
Four directions, each from a real product or site, each with real motion.

usage: python3 .aidesigner/oameni_masa_options.py
writes .aidesigner/canvas/project/Masa1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Masa*.html
Copy: docs/continut-site.md („Oamenii care vin la masă” + „Testimoniale primite”, no workshop names).
Photos: two real ones from October, two Unsplash placeholders (finished bowls, painting a bowl) until the photo shoot.
Motion rules as in formari_wallet.py: entrances once in view, interruptible, reduced motion = still, nothing hidden without JS.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS

TEXT = ("Fiecare atelier devine un prilej de a încetini, de a te reconecta cu tine și de a cunoaște oameni noi în jurul aceleiași "
        "mese. Unii oameni vin timizi și pleacă râzând, alții vin singuri și pleacă cu prieteni noi, iar împreună fac din AVA un loc "
        "al apartenenței, care se simte ca „acasă”.")
QUOTES = [("Foarte frumos și cozy, chiar am reușit să reflect asupra mea cât timp lucram cu lutul.", "Costin"),
          ("A fost o experiență foarte plăcută și relaxantă. Pauzele de socializare dintre activități au fost exact ce trebuia.", "Mario"),
          ("O activitate foarte relaxantă într-un cadru intim și frumos. Revin cu siguranță!", "Adina")]
PHOTOS = [("/_blob/42c18be93cd80d91d6d1d16793e790c6", "Doi participanți își dau din mână în mână un bol de lut, la un atelier AVA"),   # real
          ("/_blob/988e3a505fd5ae1db56d481b3d1e33b1", "Participanți modelând lut în jurul mesei, la un atelier AVA"),               # real
          ("/_blob/74f239bfbd557a0a5a661ddd26484b66", "Boluri de lut terminate, așezate unul lângă altul"),                         # placeholder
          ("/_blob/dad600a42f9bdc35b94ba47b4a49fc4a", "Un bol de lut pictat cu pensula")]                                           # placeholder
H2 = '<h2 class="disp" id="ms-h">Oamenii care vin la masă</h2>'
QM = '<svg class="qm" viewBox="0 0 32 24" aria-hidden="true"><path d="M0 24V14C0 6 4.5 1.5 12 0l1.4 3C9 4.6 7 7.4 7 11h6v13zm18 0V14C18 6 22.5 1.5 30 0l1.4 3C27 4.6 25 7.4 25 11h6v13z" style="fill:currentColor"></path></svg>'
SOURCES = {
    "Masa1Amintiri": "Apple Photos: „Amintiri” (fotografiile se apropie încet, efectul Ken Burns)",
    "Masa2Pinterest": "pinterest.com: grila în coloane inegale; coloanele alunecă cu viteze diferite la scroll",
    "Masa3Masa": "Apple Freeform: tabla pe care muți pozele și bilețelele cu degetul",
    "Masa4Banda": "framer.com: componenta Ticker (rânduri care curg fără oprire)",
}


def quote(i, cls="qt"):
    q, n = QUOTES[i]
    return f'<figure class="{cls}">{QM}<blockquote>{q}</blockquote><figcaption>{n}</figcaption></figure>'


CSS = """
.ms{position:relative;overflow:hidden;--spring:cubic-bezier(.3,1.32,.5,1);--soft:cubic-bezier(.22,1,.36,1)}
.ms h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05;text-wrap:balance}
.ms .lead{margin:22px 0 0;max-width:46ch;font-size:19px;line-height:1.7;color:#4A382C;text-wrap:pretty}
.qt{margin:0;padding:26px 26px 24px;border-radius:24px;corner-shape:squircle;background:#FBF7F0;box-shadow:0 1px 0 rgba(58,42,32,.05),0 22px 44px -30px rgba(58,30,15,.45)}
.qt .qm{width:26px;height:20px;color:var(--terra)}
.qt blockquote{margin:14px 0 0;font:italic 400 21px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--ink);text-wrap:pretty}
.qt figcaption{margin-top:14px;font:600 15px/1 var(--text);color:var(--ink2)}
.ms .ctl{display:grid;place-items:center;width:44px;height:44px;padding:0;border:0;border-radius:50%;background:rgba(58,42,32,.08);color:var(--ink);cursor:pointer;transition:background-color .2s ease}
.ms .ctl:hover{background:rgba(58,42,32,.14)}.ms .ctl:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.ms .ctl i{display:flex;gap:4px}.ms .ctl i::before,.ms .ctl i::after{content:"";width:3px;height:13px;border-radius:2px;background:currentColor}
.ms .ctl[aria-pressed="true"] i::before{width:0;height:0;border-radius:0;background:none;border-left:11px solid currentColor;border-top:7px solid transparent;border-bottom:7px solid transparent;margin-left:3px}
.ms .ctl[aria-pressed="true"] i::after{display:none}
@media (max-width:980px){.ms .lead{font-size:18px}.qt blockquote{font-size:19px}}
"""

ENTER = """
    var self = this, s = this.sec; if (!s) return;
    var reduce = this.reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    s.classList.add('js');
    if (reduce || !window.IntersectionObserver) s.classList.add('in');
    else { this.io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { s.classList.add('in'); self.io.disconnect(); } }, { threshold: 0.2 }); this.io.observe(s); }"""


def script(mount="", unmount="", cb=""):
    return f"""class Component extends DCLogic {{
  componentDidMount() {{{ENTER}{mount}
  }}
  componentWillUnmount() {{ if (this.io) this.io.disconnect(); {unmount} }}
  renderVals() {{
    var self = this;
    if (!this.cb) this.cb = {{ secRef: function (el) {{ self.sec = el; }}{cb} }};
    return this.cb;
  }}
}}"""


OPTS = {}

# 1. Amintiri: one big frame plays the workshop like an Apple Photos Memory. Each photo drifts slowly closer (Ken Burns),
#    then dissolves into the next; a testimonial rides on each one. 7s a slide, pause button, tap a bar to jump.
NS = 3
KB = ["from{scale:1.02;translate:-1.5% 1%}to{scale:1.14;translate:1.5% -1%}", "from{scale:1.14;translate:1% 1%}to{scale:1.02;translate:-1% -1%}",
      "from{scale:1.04;translate:0 -1.5%}to{scale:1.15;translate:0 1.5%}"]
SEL1 = "".join(f'.ma[data-i="{i}"] .sl:nth-of-type({i + 1}){{opacity:1;visibility:visible;transition:opacity 1.2s ease,visibility 0s}}'
               f'.ma[data-i="{i}"] .sl:nth-of-type({i + 1}) img{{animation:ma-kb{i} 8s linear both}}'
               f'.ma[data-i="{i}"] .sl:nth-of-type({i + 1}) .qt{{opacity:1;translate:0 0;transition-delay:.5s}}'
               + "".join(f'.ma[data-i="{i}"] .bar:nth-child({k + 1}) i{{scale:1 1}}' for k in range(i))
               + f'.ma[data-i="{i}"] .bar:nth-child({i + 1}) i{{animation:ma-run 7s linear forwards}}' for i in range(NS)) \
     + "".join(f"@keyframes ma-kb{i}{{{KB[i]}}}" for i in range(NS))
OPTS["Masa1Amintiri"] = ("Oamenii la masă 1: amintiri", """
.ma{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 120px}
.ma .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:0 72px;align-items:center}
.ma .frame{position:relative;aspect-ratio:5/4;border-radius:32px;corner-shape:squircle;overflow:hidden;background:#2A140C;box-shadow:0 40px 70px -40px rgba(58,30,15,.6)}
.ma .sl{position:absolute;inset:0;margin:0;opacity:0;visibility:hidden;transition:opacity 1.2s ease,visibility 0s linear 1.2s}
.ma .sl img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.ma .sl::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,14,8,0) 45%,rgba(30,14,8,.55) 100%)}
.ma .qt{position:absolute;left:24px;bottom:24px;z-index:2;max-width:380px;background:rgba(251,247,240,.86);-webkit-backdrop-filter:blur(14px) saturate(150%);backdrop-filter:blur(14px) saturate(150%);
  opacity:0;translate:0 14px;transition:opacity .6s ease,translate .7s var(--soft)}
.ma .qt blockquote{font-size:19px}
.ma .bars{position:absolute;top:16px;left:16px;right:16px;z-index:3;display:flex;gap:6px}
.ma .bar{flex:1;height:28px;padding:12px 0;border:0;background:none;cursor:pointer}
.ma .bar span{display:block;height:3px;border-radius:2px;background:rgba(255,248,238,.4);overflow:hidden}
.ma .bar i{display:block;height:100%;background:#FFF8EE;transform-origin:left;scale:0 1}
.ma .bar:focus-visible{outline:2px solid #FFF8EE;outline-offset:2px;border-radius:4px}
@keyframes ma-run{from{scale:0 1}to{scale:1 1}}
.ma:not([data-run="1"]) :is(.bar i,.sl img),.ma[data-p="1"] :is(.bar i,.sl img){animation-play-state:paused!important}
.ma .side .ctl{margin-top:32px}
""" + SEL1 + """
@media (max-width:980px){.ma{padding:72px 0 80px}.ma .stage{grid-template-columns:1fr;gap:28px}.ma .frame{aspect-ratio:4/5;border-radius:26px}.ma .qt{left:14px;right:14px;bottom:14px;padding:18px}.ma .qt blockquote{font-size:17px}.ma .side .ctl{margin-top:20px}}
@media (prefers-reduced-motion:reduce){.ma .sl,.ma .qt{transition:none!important}.ma .sl img,.ma .bar i{animation:none!important}.ma .side .ctl{display:none}}
""", '<section class="ms ma" aria-labelledby="ms-h" data-i="0" ref="{{ secRef }}"><div class="wrap stage">'
   + f'<div class="side">{H2}<p class="lead">{TEXT}</p><button class="ctl" type="button" aria-label="Pauză" aria-pressed="false" onClick="{{{{ pause }}}}"><i></i></button></div>'
   + '<div class="frame"><div class="bars">' + "".join(f'<button class="bar" type="button" aria-label="Amintirea {i + 1} din {NS}" data-i="{i}" onClick="{{{{ jump }}}}"><span><i></i></span></button>' for i in range(NS)) + "</div>"
   + "".join(f'<figure class="sl"><img src="{PHOTOS[i][0]}" alt="{PHOTOS[i][1]}">{quote(i)}</figure>' for i in range(NS))
   + "</div></div></section>",
   script(mount="""
    this.onEnd = function (e) { if (e.animationName === 'ma-run') s.setAttribute('data-i', String((+s.getAttribute('data-i') + 1) % """ + str(NS) + """)); };
    s.addEventListener('animationend', this.onEnd);
    if (window.IntersectionObserver) { this.io2 = new IntersectionObserver(function (es) { s.setAttribute('data-run', es[0].isIntersecting ? '1' : '0'); }, { threshold: 0.3 }); this.io2.observe(s); }
    else s.setAttribute('data-run', '1');""",
          unmount="if (this.io2) this.io2.disconnect(); if (this.sec) this.sec.removeEventListener('animationend', this.onEnd);",
          cb=""",
      jump: function (e) { self.sec.setAttribute('data-i', e.currentTarget.getAttribute('data-i')); },
      pause: function (e) {
        var on = self.sec.getAttribute('data-p') === '1';
        self.sec.setAttribute('data-p', on ? '0' : '1');
        e.currentTarget.setAttribute('aria-pressed', on ? 'false' : 'true');
        e.currentTarget.setAttribute('aria-label', on ? 'Pauză' : 'Continuă');
      }"""))

# 2. Pinterest: photos and testimonials in uneven columns. They pop in one after another (rise + a little turn that
#    straightens), then, as you scroll, the three columns slide at different speeds (parallax, desktop only).
COLS = [[("p", 0), ("q", 0)], [("q", 1), ("p", 1)], [("p", 2), ("q", 2), ("p", 3)]]
TILT = [-2, 1.5, -1, 2, -1.5, 1, 2.5]
_k = iter(range(20))
OPTS["Masa2Pinterest"] = ("Oamenii la masă 2: grila care respiră", """
.mp{background:#F4EDE4;padding:112px 0 120px}
.mp .head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 72px;align-items:end;margin-bottom:56px}
.mp .head .lead{margin:0}
.mp .grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;align-items:start}
.mp .col{display:flex;flex-direction:column;gap:24px;will-change:transform}
.mp .col:nth-child(2){padding-top:96px}.mp .col:nth-child(3){padding-top:40px}
.mp .ph{margin:0;border-radius:24px;corner-shape:squircle;overflow:hidden;box-shadow:0 22px 44px -30px rgba(58,30,15,.45)}
.mp .ph img{display:block;width:100%;aspect-ratio:var(--ar);object-fit:cover;transition:scale .8s var(--soft)}
@media (hover:hover){.mp .ph:hover img{scale:1.05}}
@keyframes mp-pop{from{opacity:0;translate:0 40px;rotate:var(--t)}}
.mp.js:not(.in) .it{opacity:0}
.mp.js.in .it{animation:mp-pop 1s var(--spring) backwards;animation-delay:calc(var(--k) * 110ms)}
@media (max-width:980px){.mp{padding:72px 0 80px}.mp .head{grid-template-columns:1fr;gap:18px;margin-bottom:32px}.mp .grid{grid-template-columns:1fr 1fr;gap:14px}.mp .col{gap:14px;transform:none!important}
  .mp .col:nth-child(2){padding-top:48px}.mp .col:nth-child(3){grid-column:1/-1;padding-top:0;display:grid;grid-template-columns:1fr 1fr;gap:14px}.mp .col:nth-child(3) .qt{grid-column:1/-1}
  .mp .qt{padding:18px}.mp .qt blockquote{font-size:17px}}
@media (prefers-reduced-motion:reduce){.mp .it{animation:none!important}.mp .col{transform:none!important}}
""", '<section class="ms mp" aria-labelledby="ms-h" ref="{{ secRef }}"><div class="wrap">'
   + f'<div class="head">{H2}<p class="lead">{TEXT}</p></div><div class="grid">'
   + "".join('<div class="col">' + "".join(
        (lambda k: f'<figure class="it ph" style="--k: {k}; --t: {TILT[k]}deg; --ar: {["4/5", "1/1", "3/4", "4/3"][i]}"><img src="{PHOTOS[i][0]}" alt="{PHOTOS[i][1]}"></figure>' if t == "p"
         else quote(i, f'qt it" style="--k: {k}; --t: {TILT[k]}deg'))(next(_k)) for t, i in col) + "</div>" for col in COLS)
   + "</div></div></section>",
   script(mount="""
    if (reduce) return;
    var cols = [].slice.call(s.querySelectorAll('.col')), speed = [-0.06, 0.08, -0.03], cur = [0, 0, 0], raf = 0, wide = true;
    var tick = function () {
      raf = 0; var r = s.getBoundingClientRect(), mid = r.top + r.height / 2 - innerHeight / 2, busy = false;
      cols.forEach(function (c, i) {
        var t = wide ? mid * speed[i] : 0; cur[i] += (t - cur[i]) * 0.1;   // eased, so a flick of the wheel still glides
        if (Math.abs(t - cur[i]) > 0.1) busy = true;
        c.style.transform = 'translate3d(0,' + cur[i].toFixed(1) + 'px,0)';
      });
      if (busy) raf = requestAnimationFrame(tick);
    };
    this.onScroll = function () { wide = innerWidth > 980; if (!raf) raf = requestAnimationFrame(tick); };
    addEventListener('scroll', this.onScroll, { passive: true }); addEventListener('resize', this.onScroll); this.onScroll();""",
          unmount="if (this.onScroll) { removeEventListener('scroll', this.onScroll); removeEventListener('resize', this.onScroll); }"))

# 3. Masa: the workshop table seen from above, with polaroids and handwritten-style notes dropped on it. They fall into
#    place when the section arrives; with a mouse you can pick any of them up and toss it: it keeps a little momentum,
#    stays inside the table and settles at a slight angle. (Phones: the same table, no dragging, so the page scrolls.)
ITEMS = [("p", 0, 6, 8, -6), ("q", 0, 34, 4, 3), ("p", 1, 62, 10, 4), ("q", 1, 70, 52, -3), ("p", 2, 38, 46, -2), ("q", 2, 4, 58, 2)]
ITEMS_M = [(6, 2, -5), (19, 18, 3), (8, 33, 4), (18, 51, -3), (4, 66, -2), (17, 81, 2)]   # notes are 76% wide: x <= 20%
OPTS["Masa3Masa"] = ("Oamenii la masă 3: masa de lucru", """
.mt{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 120px}
.mt .head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 72px;align-items:end;margin-bottom:44px}
.mt .head .lead{margin:0}
.mt .table{position:relative;height:640px;border-radius:40px;corner-shape:squircle;
  background:radial-gradient(ellipse 60% 50% at 50% 40%,rgba(255,236,210,.35),rgba(255,236,210,0) 70%),repeating-linear-gradient(92deg,rgba(90,50,25,.05) 0 2px,transparent 2px 22px),linear-gradient(180deg,#C99A72 0%,#B9875F 100%);
  box-shadow:inset 0 2px 0 rgba(255,236,210,.35),inset 0 -20px 40px rgba(70,35,15,.25),0 40px 70px -46px rgba(58,30,15,.7)}
.mt .it{position:absolute;left:var(--x);top:var(--y);margin:0;box-sizing:border-box;touch-action:none;cursor:grab;user-select:none;rotate:var(--r);transition:box-shadow .3s ease}
.mt .it.drag{cursor:grabbing;z-index:20;box-shadow:0 40px 50px -26px rgba(40,20,8,.6)}
.mt .pol{width:240px;padding:12px 12px 44px;background:#FBF7F0;box-shadow:0 22px 30px -18px rgba(40,20,8,.55),0 2px 4px rgba(40,20,8,.2)}
.mt .pol img{display:block;width:100%;aspect-ratio:1;object-fit:cover;pointer-events:none}
.mt .note{width:280px;border-radius:6px;background:#F6EBD3;box-shadow:0 22px 30px -18px rgba(40,20,8,.5),0 2px 4px rgba(40,20,8,.18)}
.mt .note::before{content:"";position:absolute;left:50%;top:-12px;width:84px;height:24px;margin-left:-42px;rotate:-3deg;background:rgba(244,237,228,.7);box-shadow:0 1px 2px rgba(40,20,8,.15)}
.mt .note blockquote{font-size:19px}
@keyframes mt-drop{from{opacity:0;scale:1.25;translate:0 -30px;rotate:calc(var(--r) * -2)}60%{opacity:1}}
.mt.js:not(.in) .it{opacity:0}
.mt.js.in .it{animation:mt-drop .9s var(--spring) backwards;animation-delay:calc(var(--k) * 120ms)}
@media (hover:none),(max-width:980px){.mt .it{cursor:default;touch-action:auto}}
@media (max-width:980px){.mt{padding:72px 0 80px}.mt .head{grid-template-columns:1fr;gap:18px;margin-bottom:28px}.mt .table{height:1180px;border-radius:30px}
  .mt .it{left:var(--xm);top:var(--ym);rotate:var(--rm)}.mt .pol{width:62%;padding:9px 9px 30px}.mt .note{width:76%}.mt .note blockquote{font-size:17px}}
@media (prefers-reduced-motion:reduce){.mt .it{animation:none!important}}
""", '<section class="ms mt" aria-labelledby="ms-h" ref="{{ secRef }}"><div class="wrap">'
   + f'<div class="head">{H2}<p class="lead">{TEXT}</p></div><div class="table">'
   + "".join((f'<figure class="it pol" style="--k: {k}; --x: {x}%; --y: {y}%; --r: {r}deg; --xm: {ITEMS_M[k][0]}%; --ym: {ITEMS_M[k][1]}%; --rm: {ITEMS_M[k][2]}deg"><img src="{PHOTOS[i][0]}" alt="{PHOTOS[i][1]}" draggable="false"></figure>' if t == "p"
              else quote(i, f'it note qt" style="--k: {k}; --x: {x}%; --y: {y}%; --r: {r}deg; --xm: {ITEMS_M[k][0]}%; --ym: {ITEMS_M[k][1]}%; --rm: {ITEMS_M[k][2]}deg'))
             for k, (t, i, x, y, r) in enumerate(ITEMS))
   + "</div></div></section>",
   script(mount="""
    if (reduce) return;
    var table = s.querySelector('.table'), z = 10;
    // each item keeps its own offset (dx, dy) and angle; a drag moves it, release keeps the throw's speed and lets it glide to a stop
    this.down = function (e) {
      if (e.pointerType !== 'mouse' || innerWidth <= 980) return;
      var it = e.target.closest && e.target.closest('.it'); if (!it) return;
      e.preventDefault();
      var q = it._q || (it._q = { dx: 0, dy: 0, vx: 0, vy: 0, a: parseFloat(getComputedStyle(it).rotate) || 0, raf: 0 });
      cancelAnimationFrame(q.raf); it.style.animation = 'none'; it.style.zIndex = ++z; it.classList.add('drag');
      var x0 = e.clientX, y0 = e.clientY, ox = q.dx, oy = q.dy, lx = x0, ly = y0, lt = performance.now();
      var tb = table.getBoundingClientRect(), ib = it.getBoundingClientRect();
      var minX = tb.left - ib.left + ox + 8, maxX = tb.right - ib.right + ox - 8, minY = tb.top - ib.top + oy + 8, maxY = tb.bottom - ib.bottom + oy - 8;
      var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
      var put = function () { it.style.translate = q.dx.toFixed(1) + 'px ' + q.dy.toFixed(1) + 'px'; it.style.rotate = q.a.toFixed(2) + 'deg'; };
      var mv = function (ev) {
        var now = performance.now(), dt = Math.max(1, now - lt);
        q.vx = (ev.clientX - lx) / dt * 16; q.vy = (ev.clientY - ly) / dt * 16; lx = ev.clientX; ly = ev.clientY; lt = now;
        q.dx = clamp(ox + ev.clientX - x0, minX, maxX); q.dy = clamp(oy + ev.clientY - y0, minY, maxY);
        q.a += (q.vx * 0.6 - q.a) * 0.08;   // swings a little in the direction it is dragged
        put();
      };
      var up = function () {
        removeEventListener('pointermove', mv); removeEventListener('pointerup', up); it.classList.remove('drag');
        var rest = (Math.random() * 8 - 4);
        var glide = function () {
          q.vx *= 0.9; q.vy *= 0.9; q.dx = clamp(q.dx + q.vx, minX, maxX); q.dy = clamp(q.dy + q.vy, minY, maxY); q.a += (rest - q.a) * 0.1; put();
          if (Math.abs(q.vx) + Math.abs(q.vy) + Math.abs(rest - q.a) > 0.05) q.raf = requestAnimationFrame(glide);
        };
        q.raf = requestAnimationFrame(glide);
      };
      addEventListener('pointermove', mv); addEventListener('pointerup', up);
    };
    table.addEventListener('pointerdown', this.down);""",
          unmount="if (this.sec && this.down) this.sec.querySelector('.table').removeEventListener('pointerdown', this.down);"))

# 4. Banda: two endless rows: photos drifting left, testimonials drifting right, like Framer's Ticker. Hover (or focus)
#    and the rows ease down to a crawl instead of stopping dead; the pause button stops them; off screen they rest.
ROW_P = "".join(f'<figure class="ph"><img src="{p}" alt="{a}"></figure>' for p, a in PHOTOS)
ROW_Q = "".join(quote(i) for i in range(len(QUOTES)))
ROW_P2 = ROW_P.replace(" alt=", ' alt="" data-a=')   # the looping copy is decoration: no alt text twice
OPTS["Masa4Banda"] = ("Oamenii la masă 4: banda care curge", """
.mk{background:linear-gradient(180deg,#EDE0CD 0%,#F4EDE4 100%);padding:112px 0 120px}
.mk .head{text-align:center}.mk .lead{margin:22px auto 0}
.mk .head .ctl{margin:28px auto 0}
.mk .rows{display:flex;flex-direction:column;gap:24px;margin-top:56px;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.mk .row{overflow:hidden}
.mk .track{display:flex;gap:24px;width:max-content;will-change:transform}
.mk .set{display:flex;gap:24px}
.mk .ph{flex:none;width:360px;aspect-ratio:4/3;margin:0;border-radius:24px;corner-shape:squircle;overflow:hidden}
.mk .ph img{display:block;width:100%;height:100%;object-fit:cover}
.mk .qt{flex:none;width:420px;box-sizing:border-box}
@media (max-width:980px){.mk{padding:72px 0 80px}.mk .head{text-align:left}.mk .lead{margin-left:0}.mk .head .ctl{margin-left:0}.mk .rows{margin-top:36px;gap:14px}.mk .track,.mk .set{gap:14px}.mk .ph{width:250px}.mk .qt{width:290px;padding:18px}.mk .qt blockquote{font-size:17px}}
@media (prefers-reduced-motion:reduce){.mk .row{overflow-x:auto}.mk .set[aria-hidden]{display:none}.mk .head .ctl{display:none}}
""", '<section class="ms mk" aria-labelledby="ms-h" ref="{{ secRef }}"><div class="wrap head">'
   + f'{H2}<p class="lead">{TEXT}</p><button class="ctl" type="button" aria-label="Pauză" aria-pressed="false" onClick="{{{{ pause }}}}"><i></i></button></div>'
   + '<div class="rows">'
   + f'<div class="row" data-d="-1"><div class="track"><div class="set">{ROW_P}</div><div class="set" aria-hidden="true">{ROW_P2}</div></div></div>'
   + f'<div class="row" data-d="1"><div class="track"><div class="set">{ROW_Q}</div><div class="set" aria-hidden="true">{ROW_Q}</div></div></div>'
   + "</div></section>",
   script(mount="""
    if (reduce) return;
    var rows = [].slice.call(s.querySelectorAll('.row')).map(function (r) { return { el: r.querySelector('.track'), set: r.querySelector('.set'), d: +r.getAttribute('data-d'), x: 0 }; });
    var v = 1, target = 1, vis = true, last = performance.now(), raf = 0;
    var tick = function (now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      v += (target - v) * Math.min(1, dt * 4);                     // speed eases toward its target: slows down, never snaps
      rows.forEach(function (r) {
        var w = r.set.getBoundingClientRect().width + parseFloat(getComputedStyle(r.el).columnGap || 0);
        r.x = (r.x + r.d * 38 * v * dt) % w; if (r.x > 0) r.x -= w;   // one set wide, then it wraps without a seam
        r.el.style.transform = 'translate3d(' + r.x.toFixed(2) + 'px,0,0)';
      });
      raf = vis ? requestAnimationFrame(tick) : 0;
    };
    raf = requestAnimationFrame(tick);
    var paused = false;
    this.slow = function () { target = paused ? 0 : 0.15; }; this.fast = function () { target = paused ? 0 : 1; };
    var rw = s.querySelector('.rows'); rw.addEventListener('pointerenter', this.slow); rw.addEventListener('pointerleave', this.fast);
    rw.addEventListener('focusin', this.slow); rw.addEventListener('focusout', this.fast);
    this.setPaused = function (p) { paused = p; target = p ? 0 : 1; };
    if (window.IntersectionObserver) { this.io2 = new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) { last = performance.now(); raf = requestAnimationFrame(tick); } }); this.io2.observe(s); }
    this.stop = function () { cancelAnimationFrame(raf); };""",
          unmount="if (this.stop) this.stop(); if (this.io2) this.io2.disconnect();",
          cb=""",
      pause: function (e) {
        var on = e.currentTarget.getAttribute('aria-pressed') === 'true';
        e.currentTarget.setAttribute('aria-pressed', on ? 'false' : 'true');
        e.currentTarget.setAttribute('aria-label', on ? 'Pauză' : 'Continuă');
        if (self.setPaused) self.setPaused(!on);
      }"""))


def page(name, title, css, html, js, w, h):
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
{js}
</script>
</body>
</html>
"""


# preview heights, measured in the browser (desktop 1440, phone 390)
H = {"Masa1Amintiri": (786, 1002), "Masa2Pinterest": (1519, 1575), "Masa3Masa": (1078, 1677), "Masa4Banda": (1114, 985)}

if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "masa-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Masa mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:2000px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
