"""Pagina „Despre noi”, part 2: Povestea. Four directions, each modelled on a real website.

usage: python3 .aidesigner/povestea_options.py
writes .aidesigner/canvas/project/Povestea1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Povestea*.html
Copy: docs/continut-site.md, „Despre noi” → „Povestea” (3 paragraphs, cleaned of the Google Docs bold). The two sentences
Alessia bolded as whole sentences stay emphasised. Photos: two real ones from October, one Unsplash placeholder.
"""
import os, re, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, DUO_SQ, STATIC_JS
from despre_noi_options import RINGS

S1 = "Așa am ajuns la lut, fără să știu cât de mult avea să-mi schimbe drumul."
S2 = "Când mâinile sunt ocupate, oamenii încep să vorbească altfel: mai sincer, mai blând, mai aproape unii de alții."
P1 = ("În primul an de facultate am simțit nevoia de o activitate care să mă ajute să mă reconectez cu latura mea creativă și "
      "ludică, pe care am reprimat-o din ce în ce mai mult pe măsură ce creșteam. <strong>" + S1 + "</strong> Lucrând cu el, "
      "simțeam liniște și curiozitate, iar acum este modalitatea care mă ajută să mă apropii mai mult de copilul meu interior.")
P2 = ("Cu timpul, mi-am dat seama că modelajul în lut nu este doar un prilej de conectare cu sinele, ci și cu ceilalți oameni "
      "cu care stai la masă. <strong>" + S2 + "</strong>")
P3 = ("AVA a pornit dintr-o pasiune, însă pe parcurs am descoperit că, în timp ce mâinile lucrează, mintea se liniștește, "
      "oamenii își dau voie să se relaxeze. Așa a devenit AVA un loc de conectare, comunitate și prezență, unde creăm împreună conștient.")
PARAS = [P1, P2, P3]
LUT_PH = "/_blob/27d62de5381eeee8e9ab504567023c22"    # placeholder (Unsplash): hands shaping a bowl
BOL = "/_blob/42c18be93cd80d91d6d1d16793e790c6"       # real, October: two guests passing a clay bowl
ATELIER = "/_blob/988e3a505fd5ae1db56d481b3d1e33b1"   # real, October workshop
IMGS = [(LUT_PH, "Mâini care modelează un bol de lut pe roată"),
        (BOL, "Doi participanți își dau din mână în mână un bol de lut, la un atelier AVA"),
        (ATELIER, "Participanți modelând lut în jurul mesei, la un atelier AVA")]
H2 = '<h2 class="disp" id="pv-h">Povestea</h2>'


def words(t):
    """each word in its own span (--k = its index), so the words can arrive one after another"""
    return " ".join(f'<span class="w" style="--k: {k}">{w}</span>' for k, w in enumerate(t.split()))


RV_JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, s = this.sec; if (!s) return;
    var reduce = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
    s.classList.add('js');
    var els = s.querySelectorAll('.rv, .ws, .qa');
    if (reduce || !window.IntersectionObserver) els.forEach(function (e) { e.classList.add('in'); });
    else {
      this.io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); self.io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
      els.forEach(function (e) { self.io.observe(e); });
    }
    /*EXTRA*/
  }
  componentWillUnmount() { if (this.io) this.io.disconnect(); /*UNEXTRA*/ }
  renderVals() { var self = this; if (!this.cb) this.cb = { secRef: function (el) { self.sec = el; } }; return this.cb; }
}"""
MEDIUM_EXTRA = """
    if (reduce) return;
    // reading progress along the top, and the wide photo drifting inside its frame (parallax, eased)
    var img = s.querySelector('.wide img'), raf = 0, cur = 0;
    var tick = function () {
      raf = 0;
      var r = s.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * 0.6 - r.top) / r.height));
      s.style.setProperty('--p', p.toFixed(4));
      if (img) {
        var fr = img.parentNode.getBoundingClientRect(), t = Math.max(-40, Math.min(40, (fr.top + fr.height / 2 - innerHeight / 2) * -0.08));
        cur += (t - cur) * 0.15; img.style.translate = '0 ' + cur.toFixed(1) + 'px';
        if (Math.abs(t - cur) > 0.2) raf = requestAnimationFrame(tick);
      }
    };
    this.onScroll = function () { if (!raf) raf = requestAnimationFrame(tick); };
    addEventListener('scroll', this.onScroll, { passive: true }); this.onScroll();"""
ARR = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8H13M9 4L13 8L9 12" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'

SOURCES = {
    "Povestea1Medium": "medium.com: coloana de lectură și citatele scoase în evidență",
    "Povestea2SnowFall": "The New York Times, „Snow Fall” (2012): fotografia stă pe loc cât citești capitolul",
    "Povestea3Stories": "Instagram Stories: cadre cu bare de progres, atingi ca să treci mai departe",
    "Povestea4Interviu": "The Paris Review: interviurile întrebare–răspuns",
}

COMMON = """
.pv{position:relative;overflow:clip;--so:cubic-bezier(.22,1,.36,1)}
/* reveals (Vali, 11 nov: more motion): blocks rise in as they reach the screen, words of a quote/question arrive one by one,
   and the sentence Alessia bolded gets a clay-coloured marker stroke drawn under it. Nothing hidden without JS. */
.js .rv:not(.in),.js .ws:not(.in) .w,.js .qa:not(.in) .a{opacity:0}
.ws .w{display:inline-block}
@media (prefers-reduced-motion:no-preference){
  .js .rv.in{animation:pv-up .9s var(--so) backwards}
  .js .ws.in .w{animation:pv-w .8s var(--so) backwards;animation-delay:calc(var(--k) * 45ms)}
  .js .qa.in .a{animation:pv-up .9s var(--so) .5s backwards}
}
@keyframes pv-up{from{opacity:0;translate:0 26px}}
@keyframes pv-w{from{opacity:0;translate:0 .5em;filter:blur(6px)}}
.pv strong{background:linear-gradient(transparent 60%,rgba(192,122,78,.3) 60%) 0 0/0% 100% no-repeat;transition:background-size 1.3s var(--so) .35s}
.pv:not(.js) strong,.js .in strong{background-size:100% 100%}
.pv h2{font-size:clamp(44px,4.8vw,68px);line-height:1.04}
.pv strong{font-weight:600;color:var(--ink)}
.orn{display:block;width:84px;height:24px;fill:none;stroke-width:2.2px;stroke-linecap:round}
"""
OPTS = {}

# 1. Medium: one calm reading column; the two sentences she bolded come back as pull quotes that break out of it.
OPTS["Povestea1Medium"] = ("Povestea 1: coloana de lectură", """
.pm{background:#F4EDE4;padding:120px 0 128px}
.pm .col{max-width:680px;margin:0 auto}
.pm h2{margin-bottom:44px}
.pm .t{margin:0 0 1.5em;font-size:19px;line-height:1.75;color:#4A382C;text-wrap:pretty}
.pm .pq{margin:64px -110px 64px;text-align:center}
.pm .pq .orn{margin:0 auto 22px}
.pm .pq p{margin:0;font:italic 400 clamp(28px,2.9vw,40px)/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d);text-wrap:balance}
.pm .wide{margin:72px -180px;border-radius:24px;corner-shape:squircle;overflow:hidden;aspect-ratio:16/9}
.pm .wide img{display:block;width:100%;height:100%;object-fit:cover;scale:1.14;will-change:translate}
.pm .prog{position:sticky;top:0;z-index:5;height:3px;background:var(--terra);transform-origin:0 50%;scale:var(--p,0) 1}
.pm .pq .orn path{stroke-dasharray:130;stroke-dashoffset:0;transition:stroke-dashoffset 1.4s var(--so) .1s}
.js .pm .pq:not(.in) .orn path{stroke-dashoffset:130}
@media (max-width:980px){.pm{padding:72px 0 80px}.pm .t{font-size:18px}.pm .pq{margin:44px 0}.pm .pq p{font-size:clamp(25px,7vw,30px)}.pm .wide{margin:44px 0;border-radius:18px;aspect-ratio:4/3}}
""", f"""<section class="pv pm" id="povestea" aria-labelledby="pv-h" ref="{{{{ secRef }}}}"><div class="prog" aria-hidden="true"></div><div class="wrap col">
{H2}
<p class="t rv">{P1}</p>
<blockquote class="pq rv" aria-hidden="true">{RINGS}<p class="ws">{words(S1)}</p></blockquote>
<p class="t rv">{P2}</p>
<figure class="wide rv"><img src="{IMGS[1][0]}" alt="{IMGS[1][1]}"></figure>
<blockquote class="pq rv" aria-hidden="true">{RINGS}<p class="ws">{words(S2)}</p></blockquote>
<p class="t rv">{P3}</p>
</div></section>""", RV_JS.replace("/*EXTRA*/", MEDIUM_EXTRA).replace("/*UNEXTRA*/", "if (this.onScroll) removeEventListener('scroll', this.onScroll);"))

# 2. Snow Fall: three chapters; each photo sticks in place while its paragraph scrolls past (CSS sticky, no JS),
#    then the next chapter's photo takes over. Phone: photo above its paragraph.
OPTS["Povestea2SnowFall"] = ("Povestea 2: capitole cu fotografie fixă", """
.ps{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:120px 0 64px}
.ps h2{margin-bottom:24px}
.ps .ch{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,.9fr);gap:0 88px;min-height:760px}
.ps .ch:nth-of-type(even){grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr)}
.ps .ch:nth-of-type(even) .fig{order:2}
.ps .fig{position:sticky;top:96px;align-self:start;height:min(78vh,620px);margin:40px 0;border-radius:26px;corner-shape:squircle;overflow:hidden;background:#E6D5BD}
.ps .fig img{display:block;width:100%;height:100%;object-fit:cover}
@media (prefers-reduced-motion:no-preference){.ps .fig img{animation:ps-kb 16s ease-in-out infinite alternate}.js .ps .fig.rv.in{animation:ps-open 1.2s var(--so) backwards}}
@keyframes ps-kb{to{scale:1.09}}
@keyframes ps-open{from{clip-path:inset(18% 10% 18% 10% round 26px);opacity:0}}
.ps .t{align-self:center;margin:0;padding:96px 0;font-size:20px;line-height:1.75;color:#4A382C;max-width:30em;text-wrap:pretty}
@media (max-width:980px){.ps{padding:72px 0 40px}.ps .ch,.ps .ch:nth-of-type(even){grid-template-columns:1fr;min-height:0}.ps .ch:nth-of-type(even) .fig{order:0}.ps .fig{position:relative;top:auto;height:auto;aspect-ratio:4/3;margin:24px 0 0;border-radius:20px}.ps .t{padding:24px 0 32px;font-size:18px}}
""", f"""<section class="pv ps" id="povestea" aria-labelledby="pv-h" ref="{{{{ secRef }}}}"><div class="wrap">
{H2}
""" + "\n".join(f'<div class="ch"><figure class="fig rv"><img src="{IMGS[i][0]}" alt="{IMGS[i][1]}"></figure><p class="t rv">{PARAS[i]}</p></div>' for i in range(3))
  + "\n</div></section>", RV_JS)

# 3. Stories: the story as three Instagram-style frames (most visitors arrive from Instagram). Each frame runs 9s,
#    pauses on hover / focus / the pause button, and stops on the last one. Tap the left third to go back.
BARS = "".join("<span class=\"bar\"><i></i></span>" for _ in range(3))
SEL = "".join(f'.pi[data-i="{i}"] .sl:nth-of-type({i + 1}){{opacity:1;visibility:visible;transition:opacity .45s ease,visibility 0s}}'
              + "".join(f'.pi[data-i="{i}"] .bar:nth-child({k + 1}) i{{scale:1 1}}' for k in range(i))
              + f'.pi[data-i="{i}"] .bar:nth-child({i + 1}) i{{animation:pi-run 9s linear forwards}}'
              + f'.pi[data-i="{i}"] .sl:nth-of-type({i + 1}) img{{animation:pi-kb 9s linear both}}'
              + f'.pi[data-i="{i}"] .sl:nth-of-type({i + 1}) p{{animation:pi-p .8s cubic-bezier(.22,1,.36,1) .2s backwards}}' for i in range(3))
SEL += "@keyframes pi-kb{from{scale:1.02}to{scale:1.13}}@keyframes pi-p{from{opacity:0;translate:0 18px}}"
OPTS["Povestea3Stories"] = ("Povestea 3: poveste în cadre", """
.pi{background:linear-gradient(180deg,#EDE0CD 0%,#E6D5BD 100%);padding:112px 0 120px}
.pi .stage{display:grid;grid-template-columns:minmax(0,1fr) 404px minmax(0,1fr);gap:0 64px;align-items:center}
.pi h2{justify-self:end;align-self:start;margin-top:40px}
.pi .card{position:relative;aspect-ratio:9/16;border-radius:30px;corner-shape:squircle;overflow:hidden;background:#2A140C;box-shadow:0 40px 70px -34px rgba(58,30,15,.6),0 10px 22px -12px rgba(58,30,15,.35)}
.pi .sl{position:absolute;inset:0;margin:0;opacity:0;visibility:hidden;transition:opacity .45s ease,visibility 0s linear .45s}
.pi .sl img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pi .sl::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(30,14,8,.42) 0,rgba(30,14,8,0) 18%,rgba(30,14,8,0) 34%,rgba(30,14,8,.72) 62%,rgba(30,14,8,.92) 100%)}
.pi .sl p{position:absolute;left:24px;right:24px;bottom:30px;z-index:1;margin:0;color:#F7EFE5;font-size:16.5px;line-height:1.62;text-wrap:pretty}
.pi .sl strong{color:var(--glowc);font-weight:600}
.pi .bars{position:absolute;top:12px;left:12px;right:12px;z-index:3;display:flex;gap:4px}
.pi .bar{flex:1;height:2.5px;border-radius:2px;background:rgba(255,248,238,.38);overflow:hidden}
.pi .bar i{display:block;height:100%;background:#FFF8EE;transform-origin:left;scale:0 1}
@keyframes pi-run{from{scale:0 1}to{scale:1 1}}
.pi:not([data-run="1"]) :is(.bar i,.sl img),.pi[data-p="1"] :is(.bar i,.sl img),.pi .card:is(:hover,:focus-within) :is(.bar i,.sl img){animation-play-state:paused!important}
.pi .card{transform:perspective(1100px) rotateX(var(--rx,0deg)) rotateY(var(--ry,0deg))}
.pi .who{position:absolute;top:26px;left:14px;z-index:3;display:flex;align-items:center;gap:9px;color:#FFF8EE;font:600 13.5px/1 var(--text)}
.pi .who img{width:32px;height:32px;border-radius:50%;object-fit:cover;box-shadow:0 0 0 1.5px rgba(255,248,238,.8)}
.pi .tap{position:absolute;top:0;bottom:0;z-index:2;padding:0;border:0;background:none;cursor:pointer}
.pi .tap.b{left:0;width:34%}.pi .tap.f{right:0;width:66%}
.pi .ctl{display:flex;gap:10px;align-self:end;margin-bottom:24px}
.pi .ctl button{display:grid;place-items:center;width:52px;height:52px;padding:0;border:0;border-radius:50%;background:rgba(58,42,32,.08);color:var(--ink);cursor:pointer;transition:background-color .2s ease,scale .2s ease}
.pi .ctl button:hover{background:rgba(58,42,32,.14)}.pi .ctl button:active{scale:.94}
.pi .ctl button:focus-visible{outline:2px solid var(--ink);outline-offset:3px}
.pi .ctl svg{width:18px;height:18px}.pi .ctl .bk svg{rotate:180deg}
.pi .ctl .ps i{display:flex;gap:4px}.pi .ctl .ps i::before,.pi .ctl .ps i::after{content:"";width:3px;height:14px;border-radius:2px;background:currentColor}
.pi .ctl .ps[aria-pressed="true"] i::before{width:0;height:0;border-radius:0;background:none;border-left:12px solid currentColor;border-top:7px solid transparent;border-bottom:7px solid transparent;margin-left:3px}
.pi .ctl .ps[aria-pressed="true"] i::after{display:none}
@media (prefers-reduced-motion:reduce){.pi .bar i,.pi .sl :is(img,p){animation:none!important}.pi .ctl .ps{display:none}}
@media (max-width:980px){.pi{padding:72px 0 80px}.pi .stage{grid-template-columns:1fr;justify-items:center}.pi h2{justify-self:start;margin:0 0 28px}.pi .card{width:min(100%,360px)}.pi .sl p{font-size:15.5px;left:20px;right:20px;bottom:24px}.pi .ctl{align-self:center;margin:20px 0 0}}
""" + SEL, f"""<section class="pv pi" id="povestea" aria-labelledby="pv-h" data-i="0" ref="{{{{ secRef }}}}">
<div class="wrap stage">
{H2}
<div class="card" aria-roledescription="carusel" aria-label="Povestea, în trei cadre">
<div class="bars" aria-hidden="true">{BARS}</div>
<div class="who" aria-hidden="true"><img src="{DUO_SQ}" alt="">ava.art.soul</div>
""" + "".join(f'<figure class="sl" aria-roledescription="cadru" aria-label="{i + 1} din 3"><img src="{IMGS[i][0]}" alt="{IMGS[i][1]}"><p>{PARAS[i]}</p></figure>' for i in range(3)) + """
<button class="tap b" type="button" tabindex="-1" aria-hidden="true" onClick="{{ prev }}"></button><button class="tap f" type="button" tabindex="-1" aria-hidden="true" onClick="{{ next }}"></button>
</div>
<div class="ctl"><button class="bk" type="button" aria-label="Înapoi" onClick="{{ prev }}">""" + ARR + """</button><button class="ps" type="button" aria-label="Pauză" aria-pressed="false" onClick="{{ pause }}"><i></i></button><button class="fw" type="button" aria-label="Înainte" onClick="{{ next }}">""" + ARR + """</button></div>
</div></section>""", """class Component extends DCLogic {
  componentDidMount() {
    var self = this, sec = this.sec; if (!sec) return;
    // each frame's bar is a 9s CSS animation; when it ends, go to the next frame (stop on the last)
    this.onEnd = function (e) { if (e.animationName === 'pi-run') { var i = +sec.getAttribute('data-i'); if (i < 2) self.go(i + 1); } };
    sec.addEventListener('animationend', this.onEnd);
    // run only while the story is on screen
    if (window.IntersectionObserver) {
      this.io = new IntersectionObserver(function (es) { sec.setAttribute('data-run', es[0].isIntersecting ? '1' : '0'); }, { threshold: 0.4 });
      this.io.observe(sec);
    } else sec.setAttribute('data-run', '1');
    // the card leans toward the cursor (lerped, so it glides back when the pointer leaves)
    if (!matchMedia('(prefers-reduced-motion: reduce)').matches) {
      var card = sec.querySelector('.card'), q = { x: 0, y: 0, tx: 0, ty: 0 }, raf = 0;
      var step = function () {
        raf = 0; q.x += (q.tx - q.x) * 0.1; q.y += (q.ty - q.y) * 0.1;
        card.style.setProperty('--rx', (-q.y * 6).toFixed(2) + 'deg'); card.style.setProperty('--ry', (q.x * 8).toFixed(2) + 'deg');
        if (Math.abs(q.tx - q.x) + Math.abs(q.ty - q.y) > 0.002) raf = requestAnimationFrame(step);
      };
      card.addEventListener('pointermove', function (e) { if (e.pointerType !== 'mouse') return; var r = card.getBoundingClientRect(); q.tx = (e.clientX - r.left) / r.width * 2 - 1; q.ty = (e.clientY - r.top) / r.height * 2 - 1; if (!raf) raf = requestAnimationFrame(step); });
      card.addEventListener('pointerleave', function () { q.tx = 0; q.ty = 0; if (!raf) raf = requestAnimationFrame(step); });
    }
  }
  componentWillUnmount() { if (this.sec) this.sec.removeEventListener('animationend', this.onEnd); if (this.io) this.io.disconnect(); }
  renderVals() {
    var self = this;
    if (!this.cb) {
      this.go = function (i) { if (self.sec) self.sec.setAttribute('data-i', String(Math.max(0, Math.min(2, i)))); };
      this.cb = {
        secRef: function (el) { self.sec = el; },
        prev: function () { self.go(+self.sec.getAttribute('data-i') - 1); },
        next: function () { self.go(+self.sec.getAttribute('data-i') + 1); },
        pause: function (e) {
          var on = self.sec.getAttribute('data-p') === '1';
          self.sec.setAttribute('data-p', on ? '0' : '1');
          e.currentTarget.setAttribute('aria-pressed', on ? 'false' : 'true');
          e.currentTarget.setAttribute('aria-label', on ? 'Pauză' : 'Continuă');
        }
      };
    }
    return this.cb;
  }
}""")

# 4. Interviu: the questions from the content brief, set like The Paris Review's Q&A: the question large on the left,
#    her answer on the right. Question 3 has no written answer yet, so it keeps a visible placeholder.
QA = [("Cum ai ajuns la lut și ce simțeai când lucrai cu el?", f"<p>{P1}</p>"),
      ("Când ți-ai dat seama că nu e doar despre ceramică, ci despre oameni?", f"<p>{P2}</p>"),
      ("De ce ai creat AVA Art &amp; Soul?", f'<p>{P3}</p>')]
OPTS["Povestea4Interviu"] = ("Povestea 4: interviu", """
.pr{background:#F4EDE4;padding:120px 0 120px}
.pr h2{margin-bottom:56px}
.pr .qa{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:0 80px;padding:52px 0;border-top:1px solid rgba(58,42,32,.18)}
.pr .qa:last-child{border-bottom:1px solid rgba(58,42,32,.18)}
.pr h3{margin:0;font:italic 400 clamp(26px,2.5vw,36px)/1.25 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d);text-wrap:balance}
.pr .a p{margin:0;font-size:19px;line-height:1.75;color:#4A382C;text-wrap:pretty}
.pr .a p+p{margin-top:1em}
.pr .todo{padding:14px 16px;border:1px dashed rgba(156,71,44,.55);border-radius:12px;font-size:15px!important;letter-spacing:.02em;color:var(--terra-d)!important}
@media (max-width:980px){.pr{padding:72px 0 80px}.pr h2{margin-bottom:32px}.pr .qa{grid-template-columns:1fr;gap:16px;padding:32px 0}.pr h3{font-size:clamp(24px,6.6vw,28px)}.pr .a p{font-size:18px}}
""", f"""<section class="pv pr" id="povestea" aria-labelledby="pv-h" ref="{{{{ secRef }}}}"><div class="wrap">
{H2}
""" + "\n".join(f'<div class="qa"><h3 class="ws">{words(q)}</h3><div class="a">{a}</div></div>' for q, a in QA) + "\n</div></section>", RV_JS)


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
{BASE_CSS}{COMMON}{css}</style>
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
H = {"Povestea1Medium": (2085, 1817), "Povestea2SnowFall": (2559, 1934), "Povestea3Stories": (950, 920), "Povestea4Interviu": (1151, 1392)}

if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "povestea-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Povestea mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:2600px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
