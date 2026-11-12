"""Pagina „Despre noi”, part 6: Ce credem (three values). Four directions, each from a real product or site, with motion.

usage: python3 .aidesigner/credem_options.py
writes .aidesigner/canvas/project/Credem1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Credem*.html
Copy: docs/continut-site.md, „Ce credem”: Prezență, Comunitate, Creativitate, „fiecare cu o frază”. The sentences are not
written yet, so each shows a visible placeholder [FRAZA PENTRU …]. Every value and its sentence is always visible (hover only highlights).
Motion rules as in formari_wallet.py.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS
from header_options import VASE

VALS = [("Prezență", "PREZENȚĂ", "#3A2A20", "#B4583A"), ("Comunitate", "COMUNITATE", "#9C472C", "#C07A4E"), ("Creativitate", "CREATIVITATE", "#4F5A43", "#6F7B5C")]
N = len(VALS)
H2 = '<h2 class="disp" id="cr-h">Ce credem</h2>'
SOURCES = {
    "Credem1Wrapped": "Spotify Wrapped: panouri pline de culoare, cu forme mari care se mișcă",
    "Credem2Inele": "Apple Watch: inelele Activity care se închid",
    "Credem3Forme": "headspace.com: forme organice, rotunde, care respiră",
    "Credem4Stampila": "Awwwards: insigne cu text circular care se rotește",
}


def phrase(i):
    return f"[FRAZA PENTRU {VALS[i][1]}]"


CSS = """
.cr{position:relative;overflow:hidden;--spring:cubic-bezier(.3,1.32,.5,1);--soft:cubic-bezier(.22,1,.36,1)}
.cr h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05}
.cr .ph{color:inherit;opacity:.8;font-size:16px;letter-spacing:.02em}
"""

ENTER = """
    var self = this, s = this.sec; if (!s) return;
    var reduce = this.reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    s.classList.add('js');
    if (reduce || !window.IntersectionObserver) s.classList.add('in');
    else { this.io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { s.classList.add('in'); self.io.disconnect(); } }, { threshold: 0.25 }); this.io.observe(s); }"""


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

# 1. Wrapped: three full panels in the brand's colours, each with a big shape that keeps floating. They rise in one after
#    another, the word slides up out of a mask; hovering a panel widens it (the others make room).
SHAPES = ['<circle cx="100" cy="100" r="78"></circle>',
          '<circle cx="70" cy="110" r="52"></circle><circle cx="130" cy="110" r="52"></circle><circle cx="100" cy="62" r="52"></circle>',
          '<path d="M20 120C45 40 75 40 90 100S140 170 160 90S185 40 190 60" style="fill:none;stroke-width:22;stroke-linecap:round"></path>']
OPTS["Credem1Wrapped"] = ("Ce credem 1: panouri pline", """
.cw{background:#F4EDE4;padding:112px 0 120px}
.cw h2{margin-bottom:44px}
.cw .row{display:flex;gap:16px;height:520px;margin:0;padding:0;list-style:none}
.cw .pn{position:relative;flex:1 1 0;min-width:0;container-type:inline-size;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;padding:34px;border-radius:32px;corner-shape:squircle;background:var(--bg);color:#F7EFE5;
  transition:flex-grow .7s var(--spring)}
@media (hover:hover){.cw .row:hover .pn{flex-grow:.85}.cw .row .pn:hover{flex-grow:1.35}}
.cw .sh{position:absolute;right:-30px;top:-20px;width:300px;height:300px;fill:var(--ac);stroke:var(--ac);opacity:.9;animation:cw-float 9s ease-in-out infinite alternate;animation-delay:calc(var(--i) * -3s);transition:scale .7s var(--spring)}
.cw .pn:hover .sh{scale:1.12}
@keyframes cw-float{from{translate:0 0;rotate:-6deg}to{translate:-24px 22px;rotate:8deg}}
.cw .w{display:block;overflow:hidden}
.cw .w span{display:block;font:400 min(64px,12.5cqi)/1 var(--display);font-variation-settings:'opsz' 60;letter-spacing:-.02em}
.cw .ph{position:relative;margin:14px 0 0}
@keyframes cw-rise{from{clip-path:inset(100% 0 0 0 round 32px)}to{clip-path:inset(0 0 0 0 round 32px)}}
@keyframes cw-word{from{translate:0 105%}}
.cw.js:not(.in) .pn{opacity:0}
.cw.js.in .pn{animation:cw-rise 1s var(--soft) backwards;animation-delay:calc(var(--i) * 140ms)}
.cw.js.in .w span{animation:cw-word .9s var(--soft) backwards;animation-delay:calc(var(--i) * 140ms + 380ms)}
@media (max-width:980px){.cw{padding:72px 0 80px}.cw h2{margin-bottom:28px}.cw .row{flex-direction:column;height:auto;gap:12px}.cw .pn{min-height:230px;padding:26px;border-radius:26px}.cw .sh{width:200px;height:200px}.cw .w span{font-size:min(46px,12.5cqi)}}
@media (prefers-reduced-motion:reduce){.cw *{animation:none!important;transition:none!important}}
""", '<section class="cr cw" aria-labelledby="cr-h" ref="{{ secRef }}"><div class="wrap">' + H2 + '<ul class="row">'
   + "".join(f'<li class="pn" style="--bg: {v[2]}; --ac: {v[3]}; --i: {i}"><svg class="sh" viewBox="0 0 200 200" aria-hidden="true">{SHAPES[i]}</svg>'
             f'<h3 class="w"><span>{v[0]}</span></h3><p class="ph">{phrase(i)}</p></li>' for i, v in enumerate(VALS))
   + "</ul></div></section>", script())

# 2. Inele: three concentric rings like Apple Watch's Activity rings, one per value, in the brand's colours. They close
#    when the section arrives (with a small overshoot, the way the rings do); point at a value and its ring glows thicker
#    while the others step back.
R = [150, 116, 82]
RING = "".join(f'<circle class="tr" cx="180" cy="180" r="{r}"></circle><circle class="rg" cx="180" cy="180" r="{r}" style="--c: {VALS[i][3]}; --len: {2 * 3.14159 * r:.1f}; --i: {i}" data-i="{i}"></circle>' for i, r in enumerate(R))
OPTS["Credem2Inele"] = ("Ce credem 2: inelele", """
.ck{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 120px}
.ck .stage{display:grid;grid-template-columns:400px minmax(0,1fr);gap:0 96px;align-items:center}
.ck .rings{width:100%;aspect-ratio:1;rotate:-90deg}
.ck .tr{fill:none;stroke:rgba(58,42,32,.08);stroke-width:26}
.ck .rg{fill:none;stroke:var(--c);stroke-width:26;stroke-linecap:round;stroke-dasharray:var(--len);stroke-dashoffset:0;transition:stroke-width .45s var(--spring),opacity .35s ease,filter .35s ease}
@keyframes ck-close{0%{stroke-dashoffset:var(--len)}80%{stroke-dashoffset:calc(var(--len) * -.03)}100%{stroke-dashoffset:0}}
.ck.js:not(.in) .rg{stroke-dashoffset:var(--len)}
.ck.js.in .rg{animation:ck-close 1.6s var(--soft) backwards;animation-delay:calc(var(--i) * 220ms + 150ms)}
.ck[data-on] .rg{opacity:.3}
""" + "".join(f'.ck[data-on="{i}"] .rg[data-i="{i}"]{{opacity:1;stroke-width:32;filter:drop-shadow(0 0 10px color-mix(in srgb,var(--c) 55%,transparent))}}.ck[data-on="{i}"] .val:nth-child({i + 1}){{translate:12px 0}}.ck[data-on] .val:not(:nth-child({i + 1})){{}}' for i in range(N)) + """
.ck[data-on] .val{opacity:.45}
""" + "".join(f'.ck[data-on="{i}"] .val:nth-child({i + 1}){{opacity:1}}' for i in range(N)) + """
.ck ul{margin:28px 0 0;padding:0;list-style:none}
.ck .val{display:grid;grid-template-columns:18px minmax(0,1fr);gap:4px 18px;padding:22px 0;border-top:1px solid rgba(58,42,32,.14);cursor:default;transition:opacity .35s ease,translate .45s var(--spring)}
.ck .dot{width:18px;height:18px;margin-top:10px;border-radius:50%;background:var(--c)}
.ck h3{margin:0;font:400 clamp(34px,3.2vw,46px)/1.1 var(--display);font-variation-settings:'opsz' 40}
.ck .ph{grid-column:2;margin:0;color:var(--ink2)}
@media (max-width:980px){.ck{padding:72px 0 80px}.ck .stage{grid-template-columns:1fr;gap:32px}.ck .rings{width:min(100%,300px);justify-self:center}.ck h3{font-size:34px}}
@media (prefers-reduced-motion:reduce){.ck *{animation:none!important;transition:none!important}}
""", '<section class="cr ck" aria-labelledby="cr-h" ref="{{ secRef }}"><div class="wrap stage">'
   + f'<svg class="rings" viewBox="0 0 360 360" aria-hidden="true">{RING}</svg>'
   + f'<div>{H2}<ul>' + "".join(f'<li class="val" data-i="{i}" style="--c: {v[3]}"><span class="dot" aria-hidden="true"></span><h3>{v[0]}</h3><p class="ph">{phrase(i)}</p></li>' for i, v in enumerate(VALS))
   + "</ul></div></div></section>",
   script(mount="""
    this.over = function (e) { var el = e.target.closest && e.target.closest('[data-i]'); if (el) s.setAttribute('data-on', el.getAttribute('data-i')); else s.removeAttribute('data-on'); };
    this.out = function () { s.removeAttribute('data-on'); };
    s.addEventListener('pointerover', this.over); s.addEventListener('pointerleave', this.out);""",
          unmount="if (this.sec && this.over) { this.sec.removeEventListener('pointerover', this.over); this.sec.removeEventListener('pointerleave', this.out); }"))

# 3. Forme: three soft clay shapes that keep breathing (their corners slowly reshape), like Headspace's rounded forms.
#    They pop in one after another; hovering one squishes it a little, like pressing soft clay.
BLOB = ["60% 40% 55% 45% / 50% 60% 40% 50%", "45% 55% 40% 60% / 60% 45% 55% 40%", "55% 45% 60% 40% / 45% 55% 45% 55%"]
BLOB2 = ["40% 60% 45% 55% / 60% 40% 60% 40%", "60% 40% 55% 45% / 40% 55% 45% 60%", "40% 60% 45% 55% / 55% 40% 60% 45%"]
OPTS["Credem3Forme"] = ("Ce credem 3: forme care respiră", """
.cs{background:radial-gradient(ellipse 60% 60% at 50% 60%,#FAF4EA 0%,rgba(250,244,234,0) 70%),#F4EDE4;padding:112px 0 120px}
.cs h2{text-align:center;margin-bottom:56px}
.cs ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px;margin:0;padding:0;list-style:none;text-align:center}
.cs .blob{display:grid;place-items:center;width:min(100%,320px);aspect-ratio:1;margin:0 auto;border-radius:var(--b1);
  background:radial-gradient(circle at 35% 30%,color-mix(in srgb,var(--ac) 60%,#FFF7EC),var(--bg) 72%);color:#F7EFE5;
  box-shadow:inset 0 -18px 30px rgba(30,14,8,.22),0 30px 50px -30px rgba(58,30,15,.55);animation:cs-breathe 9s ease-in-out infinite alternate;animation-delay:calc(var(--i) * -3s);
  transition:scale .6s var(--spring)}
@keyframes cs-breathe{from{border-radius:var(--b1)}to{border-radius:var(--b2)}}
@media (hover:hover){.cs .blob:hover{scale:1.08 .94}}
.cs h3{margin:0;font:400 clamp(32px,3vw,44px)/1 var(--display);font-variation-settings:'opsz' 40}
.cs .ph{margin:22px auto 0;max-width:24ch;color:var(--ink2)}
@keyframes cs-pop{from{scale:.5;opacity:0}60%{opacity:1}}
.cs.js:not(.in) li{opacity:0}
.cs.js.in li{animation:cs-pop .9s var(--spring) backwards;animation-delay:calc(var(--i) * 140ms)}
@media (max-width:980px){.cs{padding:72px 0 80px}.cs h2{text-align:left;margin-bottom:32px}.cs ul{grid-template-columns:1fr;gap:36px}.cs .blob{width:240px}}
@media (prefers-reduced-motion:reduce){.cs *{animation:none!important;transition:none!important}}
""", '<section class="cr cs" aria-labelledby="cr-h" ref="{{ secRef }}"><div class="wrap">' + H2 + "<ul>"
   + "".join(f'<li style="--i: {i}"><div class="blob" style="--bg: {v[2]}; --ac: {v[3]}; --i: {i}; --b1: {BLOB[i]}; --b2: {BLOB2[i]}"><h3>{v[0]}</h3></div><p class="ph">{phrase(i)}</p></li>' for i, v in enumerate(VALS))
   + "</ul></div></section>", script())

# 4. Ștampila: the three values run around a circle, like the brand's stamp (and the rotating text badges on Awwwards),
#    with the clay vase in the middle. It turns slowly; point at a value below and the ring eases round to bring that word
#    to the top, then waits. Ring speed is a lerp, so it never jerks.
WORDS = "".join(f'<text class="wd" data-i="{i}"><textPath href="#cr-circ" startOffset="{(i * 100 / N + 100 / (2 * N)):.2f}%" text-anchor="middle">{v[1]}</textPath></text>' for i, v in enumerate(VALS))
DOTS = "".join(f'<circle cx="{200 + 150 * __import__("math").sin(__import__("math").radians(i * 120)):.1f}" cy="{200 - 150 * __import__("math").cos(__import__("math").radians(i * 120)):.1f}" r="4"></circle>' for i in range(N))
OPTS["Credem4Stampila"] = ("Ce credem 4: ștampila care se rotește", """
.ct{background:linear-gradient(180deg,#EDE0CD 0%,#F4EDE4 100%);padding:112px 0 120px}
.ct .stage{display:grid;grid-template-columns:420px minmax(0,1fr);gap:0 96px;align-items:center}
.ct .seal{position:relative;width:100%;aspect-ratio:1}
.ct .ring{position:absolute;inset:0;width:100%;height:100%;will-change:transform}
.ct .ring text{font:500 27px/1 var(--text);letter-spacing:.32em;fill:var(--ink);transition:fill .35s ease}
.ct .ring .dots circle{fill:var(--terra)}
.ct .disc{position:absolute;inset:23%;display:grid;place-items:center;border-radius:50%;background:radial-gradient(circle at 40% 35%,#F8EFE3,#E6D5BD);box-shadow:inset 0 -10px 22px rgba(58,30,15,.16),0 24px 40px -26px rgba(58,30,15,.5)}
.ct .disc svg{width:34%;color:var(--ink)}
""" + "".join(f'.ct[data-on="{i}"] .wd[data-i="{i}"]{{fill:var(--terra-d)}}.ct[data-on="{i}"] .val[data-i="{i}"] h3{{color:var(--terra-d)}}' for i in range(N)) + """
.ct ul{margin:28px 0 0;padding:0;list-style:none}
.ct .val{padding:22px 0;border-top:1px solid rgba(58,42,32,.14);transition:translate .45s var(--spring)}
.ct[data-on] .val{opacity:.5;transition:opacity .35s ease,translate .45s var(--spring)}
""" + "".join(f'.ct[data-on="{i}"] .val[data-i="{i}"]{{opacity:1;translate:12px 0}}' for i in range(N)) + """
.ct h3{margin:0;font:400 clamp(34px,3.2vw,46px)/1.1 var(--display);font-variation-settings:'opsz' 40;transition:color .35s ease}
.ct .ph{margin:6px 0 0;color:var(--ink2)}
@keyframes ct-in{from{scale:.7;rotate:-40deg;opacity:0}}
.ct.js:not(.in) .seal{opacity:0}
.ct.js.in .seal{animation:ct-in 1.2s var(--spring) backwards}
@media (max-width:980px){.ct{padding:72px 0 80px}.ct .stage{grid-template-columns:1fr;gap:32px}.ct .seal{width:min(100%,320px);justify-self:center}.ct h3{font-size:34px}}
@media (prefers-reduced-motion:reduce){.ct *{animation:none!important;transition:none!important}}
""", '<section class="cr ct" aria-labelledby="cr-h" ref="{{ secRef }}"><div class="wrap stage">'
   + f'<div class="seal" aria-hidden="true"><svg class="ring" viewBox="0 0 400 400"><defs><path id="cr-circ" d="M200 50A150 150 0 1 1 199.99 50"></path></defs><g class="dots">{DOTS}</g>{WORDS}</svg><div class="disc">{VASE}</div></div>'
   + f'<div>{H2}<ul>' + "".join(f'<li class="val" data-i="{i}"><h3>{v[0]}</h3><p class="ph">{phrase(i)}</p></li>' for i, v in enumerate(VALS))
   + "</ul></div></div></section>",
   script(mount="""
    var ring = s.querySelector('.ring'), a = 0, v = 9, target = null, last = performance.now(), raf = 0, vis = true;
    var tick = function (now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (target === null) { v += (9 - v) * Math.min(1, dt * 2); a += v * dt; }            // 9°/s drift
      else { var d = ((target - a) % 360 + 540) % 360 - 180; a += d * Math.min(1, dt * 4); v = 0; }   // ease the chosen word to the top
      ring.style.transform = 'rotate(' + a.toFixed(2) + 'deg)';
      raf = vis ? requestAnimationFrame(tick) : 0;
    };
    if (!reduce) raf = requestAnimationFrame(tick);
    this.over = function (e) {
      var el = e.target.closest && e.target.closest('.val'); if (!el) { s.removeAttribute('data-on'); target = null; return; }
      var i = +el.getAttribute('data-i'); s.setAttribute('data-on', i); target = -i * """ + str(360 // N) + """ - """ + str(180 // N) + """;
    };
    this.out = function () { s.removeAttribute('data-on'); target = null; };
    s.addEventListener('pointerover', this.over); s.addEventListener('pointerleave', this.out);
    if (window.IntersectionObserver && !reduce) { this.io2 = new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) { last = performance.now(); raf = requestAnimationFrame(tick); } }); this.io2.observe(s); }
    this.stop = function () { cancelAnimationFrame(raf); };""",
          unmount="if (this.stop) this.stop(); if (this.io2) this.io2.disconnect(); if (this.sec && this.over) { this.sec.removeEventListener('pointerover', this.over); this.sec.removeEventListener('pointerleave', this.out); }"))


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
H = {"Credem1Wrapped": (863, 1092), "Credem2Inele": (702, 890), "Credem3Forme": (748, 1212), "Credem4Stampila": (708, 916)}

if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "credem-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Credem mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1400px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
