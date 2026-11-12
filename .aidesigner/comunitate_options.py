"""Pagina „Despre noi”, part 4: Comunitatea AVA (the intro + three collaborators). Four directions, each from a real
website, each with real motion (Vali, 11 nov: „don't be afraid to use smooth animations”).

usage: python3 .aidesigner/comunitate_options.py
writes .aidesigner/canvas/project/Comunitate1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Comunitate*.html
Copy: docs/continut-site.md, „Despre noi” → „Comunitatea AVA”. They are collaborators, never „echipa”.
No photos of them yet: every portrait is a visible placeholder [POZĂ …].
Motion rules as in formari_wallet.py: entrances run once when in view, everything interruptible, reduced motion = still,
nothing hidden without JS.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS

INTRO = ("Comunitatea AVA înseamnă oamenii alături de care creez și cei care iau parte la evenimentele noastre. AVA este "
         "proiectul meu, dar îmi place să creez experiențe și alături de alți artiști și antreprenori care cred în aceleași lucruri ca mine.")
PEOPLE = [
    ("Samargiu Casandra", "Casandra", "Social Media &amp; Brand Manager",
     "Ea e motivul pentru care AVA Art &amp; Soul arată așa cum arată. Are grijă ca fiecare culoare, poză și postare să transmită "
     "aceeași căldură pe care o simți la atelierele și evenimentele noastre. Prietene încă din gimnaziu, ne cunoaștem atât de bine "
     "încât știe, de multe ori, cum vreau să arate ceva înainte să îi spun.", "#B4583A"),
    ("Ramona Nichifor", "Ramona", "Colaboratoare · Artă &amp; Povești",
     "De la ea am învățat, înainte de orice, că cel mai frumos mod de a-ți trăi viața este prin AUTENTICITATE, iar arta e un fel "
     "de a spune ce simți. Mama mea este pictoriță, ilustratoare, scriitoare și consilier în dezvoltare personală. În cadrul "
     "colaborărilor noastre, ea aduce culoarea, poveștile și blândețea cu care m-a crescut.", "#6F7B5C"),
    ("Iuliana Petrescu", "Iuliana", "Colaboratoare",
     "Ne-am cunoscut pe băncile facultății de Psihologie și am mers mai departe împreună, la master. Astăzi ne întâlnim și la masa "
     "de lucru: în atelierele la care colaborăm, aduce o privire atentă asupra oamenilor și grija ca fiecare să se simtă bine "
     "primit, de la primul ceai până la ultima poveste spusă la masă.", "#C07A4E"),
]
N = len(PEOPLE)
H2 = '<h2 class="disp" id="cm-h">Comunitatea AVA</h2>'
SOURCES = {
    "Comunitate1Lista": "Awwwards: liste de nume cu imaginea care urmărește cursorul (hover image reveal)",
    "Comunitate2Highlights": "Instagram: cercurile „Highlights” de pe profil",
    "Comunitate3Contributori": "The New Yorker: pagina „Contributors” din fiecare număr",
    "Comunitate4Cursoare": "figma.com: cursoarele cu nume care lucrează împreună pe aceeași pânză",
}


def ph(i, cls="ph"):
    """visible placeholder until we get their photos: initial in Bodoni + the label"""
    full, first, *_ = PEOPLE[i]
    return (f'<span class="{cls}" role="img" aria-label="[POZĂ {first.upper()}]" style="--c: {PEOPLE[i][4]}">'
            f'<b aria-hidden="true">{first[0]}</b><i aria-hidden="true">[POZĂ {first.upper()}]</i></span>')


CSS = """
.cm{position:relative;overflow:hidden;--spring:cubic-bezier(.3,1.32,.5,1);--soft:cubic-bezier(.22,1,.36,1)}
.cm h2{font-size:clamp(40px,4.4vw,64px);line-height:1.05}
.cm .intro{margin:24px 0 0;max-width:46ch;font-size:19px;line-height:1.7;color:#4A382C;text-wrap:pretty}
.cm .role{display:block;font:italic 400 19px/1.3 var(--display);font-variation-settings:'opsz' 20;color:var(--terra-d)}
.cm .desc{margin:0;color:#4A382C;font-size:17px;line-height:1.7;text-wrap:pretty}
.ph{position:relative;display:grid;place-items:center;overflow:hidden;background:radial-gradient(ellipse 70% 60% at 50% 35%,rgba(255,250,242,.55),rgba(255,250,242,0) 70%),
  repeating-linear-gradient(135deg,rgba(58,42,32,.045) 0 2px,transparent 2px 12px),color-mix(in srgb,var(--c) 22%,#EDE0CD)}
.ph b{font:400 clamp(64px,7vw,120px)/1 var(--display);font-variation-settings:'opsz' 60;color:color-mix(in srgb,var(--c) 75%,#3A2A20)}
.ph i{position:absolute;left:0;right:0;bottom:14px;font:500 11.5px/1 var(--text);letter-spacing:.08em;font-style:normal;text-align:center;color:color-mix(in srgb,var(--c) 70%,#3A2A20)}
@media (max-width:980px){.cm .intro{font-size:18px}.cm .desc{font-size:16.5px}}
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

# 1. Lista: their names set huge, one per row. On a desktop, hovering a row brings their portrait out to float beside the
#    cursor (it trails behind with a lerp and leans with the speed); each row is a <details>, so it opens to the full text
#    natively (no JS needed) and the height animates where the browser can (interpolate-size).
OPTS["Comunitate1Lista"] = ("Comunitatea 1: numele mari", """
.cl{background:#F4EDE4;padding:112px 0 120px;interpolate-size:allow-keywords}
.cl .head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 72px;align-items:end;margin-bottom:56px}
.cl .head .intro{margin:0}
.cl details{border-top:1px solid rgba(58,42,32,.18)}
.cl details:last-of-type{border-bottom:1px solid rgba(58,42,32,.18)}
.cl summary{display:flex;align-items:baseline;justify-content:space-between;gap:24px;padding:22px 0;cursor:pointer;list-style:none}
.cl summary::-webkit-details-marker{display:none}
.cl summary:focus-visible{outline:2px solid var(--ink);outline-offset:4px;border-radius:8px}
.cl .nm{font:400 clamp(40px,6.4vw,96px)/1 var(--display);font-variation-settings:'opsz' 60;letter-spacing:-.02em;color:var(--ink);
  transition:translate .5s var(--spring),color .3s ease}
.cl .role{flex:none;text-align:right;transition:opacity .3s ease}
.cl .plus{position:relative;flex:none;width:22px;height:22px;margin-left:8px;align-self:center}
.cl .plus::before,.cl .plus::after{content:"";position:absolute;left:0;right:0;top:50%;height:1.5px;margin-top:-.75px;background:currentColor;transition:rotate .4s var(--spring)}
.cl .plus::after{rotate:90deg}.cl details[open] .plus::after{rotate:0deg}
@media (hover:hover){.cl summary:hover .nm{translate:28px 0;color:var(--terra-d)}}
.cl details[open] .nm{color:var(--terra-d)}
.cl details::details-content{height:0;overflow:clip;transition:height .55s var(--soft),content-visibility .55s allow-discrete}
.cl details[open]::details-content{height:auto}
.cl .body{display:grid;grid-template-columns:200px minmax(0,1fr);gap:0 40px;padding:4px 0 36px;max-width:900px}
.cl .body .ph{width:200px;aspect-ratio:4/5;border-radius:20px;corner-shape:squircle}
.cl .body .ph b{font-size:72px}
.cl .float{position:absolute;left:0;top:0;z-index:5;width:260px;aspect-ratio:4/5;margin:-160px 0 0 -130px;pointer-events:none;opacity:0;scale:.6;
  transition:opacity .35s ease,scale .5s var(--spring)}
.cl .float.on{opacity:1;scale:1}
.cl .float .ph{position:absolute;inset:0;border-radius:24px;corner-shape:squircle;opacity:0;transition:opacity .3s ease;box-shadow:0 30px 50px -24px rgba(58,30,15,.55)}
.cl .float .ph.on{opacity:1}
@media (hover:none){.cl .float{display:none}}
@media (max-width:980px){.cl{padding:72px 0 80px}.cl .head{grid-template-columns:1fr;gap:20px;margin-bottom:36px}.cl summary{flex-wrap:wrap;gap:6px 16px;padding:18px 0}.cl .nm{font-size:clamp(34px,10.5vw,52px)}.cl .role{order:3;flex-basis:100%;text-align:left;font-size:17px}.cl .plus{margin-left:auto}
  .cl .body{grid-template-columns:1fr;gap:18px}.cl .body .ph{width:150px}}
@media (prefers-reduced-motion:reduce){.cl *{transition:none!important}.cl .float{display:none}}
""", '<section class="cm cl" aria-labelledby="cm-h" ref="{{ secRef }}"><div class="wrap">'
   + f'<div class="head">{H2}<p class="intro">{INTRO}</p></div>'
   + "".join(f'<details{" open" if i == 0 else ""} data-i="{i}"><summary><span class="nm">{p[0]}</span><span class="role">{p[2]}</span><span class="plus" aria-hidden="true"></span></summary>'
             f'<div class="body">{ph(i)}<p class="desc">{p[3]}</p></div></details>' for i, p in enumerate(PEOPLE))
   + '</div><div class="float" aria-hidden="true">' + "".join(ph(i) for i in range(N)) + "</div></section>",
   script(mount="""
    if (reduce) return;
    var fl = s.querySelector('.float'), imgs = fl.querySelectorAll('.ph'), P = { x: 0, y: 0, tx: 0, ty: 0, r: 0 }, raf = 0, on = false;
    var step = function () {
      raf = 0;
      var vx = (P.tx - P.x) * 0.14; P.x += vx; P.y += (P.ty - P.y) * 0.14;
      P.r += (Math.max(-12, Math.min(12, vx * 0.6)) - P.r) * 0.12;   // leans into the movement, settles when still
      fl.style.transform = 'translate3d(' + P.x.toFixed(1) + 'px,' + P.y.toFixed(1) + 'px,0) rotate(' + P.r.toFixed(2) + 'deg)';
      if (on || Math.abs(P.tx - P.x) + Math.abs(P.ty - P.y) + Math.abs(P.r) > 0.3) raf = requestAnimationFrame(step);
    };
    this.move = function (e) {
      if (e.pointerType !== 'mouse') return;
      var row = e.target.closest && e.target.closest('summary'), r = s.getBoundingClientRect();
      P.tx = e.clientX - r.left + 240; P.ty = e.clientY - r.top - 30;   // beside the cursor, clear of the name
      if (!on) { P.x = P.tx; P.y = P.ty; }
      on = !!row; fl.classList.toggle('on', on);
      if (row) { var i = +row.parentNode.getAttribute('data-i'); imgs.forEach(function (m, k) { m.classList.toggle('on', k === i); }); }
      if (!raf) raf = requestAnimationFrame(step);
    };
    this.leave = function () { on = false; fl.classList.remove('on'); };
    s.addEventListener('pointermove', this.move); s.addEventListener('pointerleave', this.leave);""",
          unmount="if (this.sec && this.move) { this.sec.removeEventListener('pointermove', this.move); this.sec.removeEventListener('pointerleave', this.leave); }"))

# 2. Highlights: like the round Highlights on an Instagram profile. Each ring turns slowly; tap one and her card opens
#    out of the circle (a clip-path circle that grows from the ring you tapped). Without JS all three cards show.
OPTS["Comunitate2Highlights"] = ("Comunitatea 2: cercurile Highlights", """
@property --ang{syntax:'<angle>';inherits:false;initial-value:0deg}
.ci{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%);padding:112px 0 120px}
.ci .head{text-align:center}.ci .intro{margin:24px auto 0}
.ci .rings{display:flex;justify-content:center;gap:56px;margin:56px 0 0;padding:0;list-style:none}
.ci .hl{display:flex;flex-direction:column;align-items:center;gap:14px;padding:0;border:0;background:none;color:var(--ink);font:500 16px/1 var(--text);cursor:pointer}
.ci .hl:focus-visible{outline:2px solid var(--ink);outline-offset:6px;border-radius:12px}
.ci .ring{position:relative;display:block;width:136px;height:136px;padding:5px;box-sizing:border-box;border-radius:50%;
  background:conic-gradient(from var(--ang),#B4583A,#C07A4E,#F2C79C,#6F7B5C,#B4583A);animation:ci-spin 9s linear infinite;transition:scale .45s var(--spring),filter .3s ease}
.ci .ring::before{content:"";position:absolute;inset:4px;border-radius:50%;background:#F4EDE4}
.ci .ring .ph{position:absolute;inset:9px;border-radius:50%}
.ci .ring .ph b{font-size:52px}.ci .ring .ph i{display:none}
@keyframes ci-spin{to{--ang:360deg}}
@media (hover:hover){.ci .hl:hover .ring{scale:1.06}}
.ci.js .hl[aria-pressed="false"] .ring{filter:saturate(.6) opacity(.8);animation-play-state:paused}
.ci.js .hl[aria-pressed="true"] .ring{scale:1.08;animation-duration:3.5s}
.ci .cards{position:relative;max-width:900px;margin:44px auto 0}
.ci .card{display:grid;grid-template-columns:240px minmax(0,1fr);gap:0 40px;align-items:center;padding:28px;border-radius:32px;corner-shape:squircle;background:#FBF7F0;
  box-shadow:0 1px 0 rgba(58,42,32,.05),0 30px 60px -36px rgba(58,30,15,.45)}
.ci .card+.card{margin-top:20px}
.ci.js .card:not(.on){display:none}
.ci .card .ph{aspect-ratio:4/5;border-radius:22px;corner-shape:squircle}
.ci .card h3{margin:0;font:400 clamp(30px,3vw,42px)/1.1 var(--display);font-variation-settings:'opsz' 40}
.ci .card .role{margin:8px 0 18px}
@media (max-width:980px){.ci{padding:72px 0 80px}.ci .head{text-align:left}.ci .intro{margin-left:0}.ci .rings{gap:18px;margin-top:36px;justify-content:space-between}.ci .ring{width:96px;height:96px;padding:4px}.ci .ring .ph{inset:7px}.ci .ring .ph b{font-size:36px}.ci .hl{font-size:14.5px}
  .ci .card{grid-template-columns:1fr;gap:20px;padding:18px;border-radius:26px}.ci .card .ph{width:150px}}
@media (prefers-reduced-motion:reduce){.ci .ring{animation:none;transition:none}}
""", '<section class="cm ci" aria-labelledby="cm-h" ref="{{ secRef }}" onClick="{{ pick }}"><div class="wrap">'
   + f'<div class="head">{H2}<p class="intro">{INTRO}</p></div>'
   + '<ul class="rings">' + "".join(f'<li><button class="hl" type="button" aria-pressed="{"true" if i == 0 else "false"}" aria-controls="ci-{i}" data-i="{i}"><span class="ring">{ph(i)}</span>{p[1]}</button></li>' for i, p in enumerate(PEOPLE)) + "</ul>"
   + '<div class="cards">' + "".join(f'<article class="card{" on" if i == 0 else ""}" id="ci-{i}">{ph(i)}<div><h3>{p[0]}</h3><span class="role">{p[2]}</span><p class="desc">{p[3]}</p></div></article>' for i, p in enumerate(PEOPLE))
   + "</div></div></section>",
   script(cb=""",
      pick: function (e) {
        var b = e.target.closest && e.target.closest('.hl'), s = self.sec; if (!b || !s) return;
        var i = b.getAttribute('data-i'), card = s.querySelector('#ci-' + i);
        s.querySelectorAll('.hl').forEach(function (h) { h.setAttribute('aria-pressed', h === b ? 'true' : 'false'); });
        s.querySelectorAll('.card').forEach(function (c) { c.classList.toggle('on', c === card); });
        if (self.reduce || !card.animate) return;
        // the card grows out of the ring that was tapped
        var rr = b.querySelector('.ring').getBoundingClientRect(), cr = card.getBoundingClientRect();
        var x = (rr.left + rr.width / 2 - cr.left).toFixed(0) + 'px', y = (rr.top + rr.height / 2 - cr.top).toFixed(0) + 'px';
        card.animate([{ clipPath: 'circle(40px at ' + x + ' ' + y + ')', opacity: .4 }, { clipPath: 'circle(160% at ' + x + ' ' + y + ')', opacity: 1 }],
                     { duration: 750, easing: 'cubic-bezier(.22,1,.36,1)' });
      }"""))

# 3. Contributori: The New Yorker's contributors page, with motion. As the section comes in, each portrait is uncovered
#    from the bottom up (a clip that rises like clay being pulled up on the wheel) while the image settles from 1.15 to 1,
#    and the lines of text follow, 80ms apart. Hover: the portrait breathes in, a terracotta line draws under the name.
OPTS["Comunitate3Contributori"] = ("Comunitatea 3: contributorii", """
.cn{background:#F4EDE4;padding:112px 0 120px}
.cn .stage{display:grid;grid-template-columns:minmax(0,4fr) minmax(0,7fr);gap:0 88px;align-items:start}
.cn .head{position:sticky;top:112px}
.cn ol{margin:0;padding:0;list-style:none}
.cn li{display:grid;grid-template-columns:200px minmax(0,1fr);gap:0 36px;padding:0 0 56px}
.cn li+li{padding-top:56px;border-top:1px solid rgba(58,42,32,.14)}
.cn .pic{overflow:hidden;aspect-ratio:4/5;border-radius:18px;corner-shape:squircle}
.cn .pic .ph{width:100%;height:100%;transition:scale .7s var(--soft)}
.cn h3{display:inline;margin:0;font:400 clamp(28px,2.6vw,36px)/1.15 var(--display);font-variation-settings:'opsz' 40;
  background:linear-gradient(var(--terra),var(--terra)) 0 100%/0 2px no-repeat;padding-bottom:4px;transition:background-size .5s var(--soft)}
.cn .role{margin:12px 0 16px}
@media (hover:hover){.cn li:hover .pic .ph{scale:1.05}.cn li:hover h3{background-size:100% 2px}}
@keyframes cn-rise{from{clip-path:inset(100% 0 0 0 round 18px)}to{clip-path:inset(0 0 0 0 round 18px)}}
@keyframes cn-settle{from{scale:1.18}}
@keyframes cn-up{from{opacity:0;translate:0 18px}}
.cn.js:not(.in) :is(.pic,.tx>*){opacity:0}
.cn.js.in .pic{animation:cn-rise 1.1s var(--soft) backwards;animation-delay:calc(var(--i) * 180ms)}
.cn.js.in .pic .ph{animation:cn-settle 1.6s var(--soft) backwards;animation-delay:calc(var(--i) * 180ms)}
.cn.js.in .tx>*{animation:cn-up .8s var(--soft) backwards;animation-delay:calc(var(--i) * 180ms + 250ms + var(--k) * 80ms)}
@media (max-width:980px){.cn{padding:72px 0 80px}.cn .stage{grid-template-columns:1fr;gap:40px}.cn .head{position:static}.cn li{grid-template-columns:1fr;gap:20px;padding-bottom:40px}.cn li+li{padding-top:40px}.cn .pic{width:170px}}
@media (prefers-reduced-motion:reduce){.cn *{animation:none!important;transition:none!important}}
""", '<section class="cm cn" aria-labelledby="cm-h" ref="{{ secRef }}"><div class="wrap stage">'
   + f'<div class="head">{H2}<p class="intro">{INTRO}</p></div><ol>'
   + "".join(f'<li style="--i: {i}"><div class="pic">{ph(i)}</div><div class="tx"><h3 style="--k: 0">{p[0]}</h3><span class="role" style="--k: 1">{p[2]}</span><p class="desc" style="--k: 2">{p[3]}</p></div></li>' for i, p in enumerate(PEOPLE))
   + "</ol></div></section>", script())

# 4. Cursoare: figma.com's multiplayer cursors. Four named cursors (Alessia and the three collaborators) drift over the
#    section as if they were working on it together. Hover a card and its person's cursor glides over to point at her name.
CUR = '<svg viewBox="0 0 20 22" aria-hidden="true"><path d="M2 1.5L17.5 10.2L10.2 11.8L6.6 19.5Z" style="fill:var(--c);stroke:#FBF7F0;stroke-width:1.6;stroke-linejoin:round"></path></svg>'
CURSORS = [("Alessia", "#3A2A20")] + [(p[1], p[4]) for p in PEOPLE]
OPTS["Comunitate4Cursoare"] = ("Comunitatea 4: cursoare care lucrează împreună", """
.cf{background:radial-gradient(ellipse 60% 70% at 50% 60%,#FAF4EA 0%,rgba(250,244,234,0) 70%),#F4EDE4;padding:112px 0 128px}
.cf .head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 72px;align-items:end;margin-bottom:56px}
.cf .head .intro{margin:0}
.cf ul{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px;margin:0;padding:0;list-style:none}
.cf .card{height:100%;box-sizing:border-box;padding:16px 16px 28px;border-radius:30px;corner-shape:squircle;background:#FBF7F0;
  box-shadow:0 1px 0 rgba(58,42,32,.05),0 24px 48px -32px rgba(58,30,15,.4);transition:translate .45s var(--spring),box-shadow .45s var(--soft)}
@media (hover:hover){.cf .card:hover{translate:0 -8px;box-shadow:0 1px 0 rgba(58,42,32,.05),0 40px 60px -34px rgba(58,30,15,.5)}}
.cf .card .ph{aspect-ratio:5/4;border-radius:22px;corner-shape:squircle}
.cf .card .tx{padding:22px 10px 0}
.cf h3{margin:0;font:400 clamp(26px,2.3vw,32px)/1.15 var(--display);font-variation-settings:'opsz' 40}
.cf .role{margin:8px 0 14px;font-size:17px}
.cf .desc{font-size:16px}
.cf .cur{position:absolute;left:0;top:0;z-index:6;display:flex;align-items:flex-start;pointer-events:none;will-change:transform}
.cf .cur svg{width:20px;height:22px;filter:drop-shadow(0 2px 3px rgba(40,20,10,.3))}
.cf .cur span{margin:16px 0 0 -2px;padding:5px 10px 6px;border-radius:999px 999px 999px 4px;background:var(--c);color:#FBF7F0;font:600 13px/1 var(--text);white-space:nowrap;box-shadow:0 4px 10px -4px rgba(40,20,10,.4)}
.cf.js:not(.in) .cur{opacity:0}
.cf .cur{transition:opacity .6s ease}
@media (max-width:980px){.cf{padding:72px 0 80px}.cf .head{grid-template-columns:1fr;gap:20px;margin-bottom:32px}.cf ul{grid-template-columns:1fr;gap:20px}.cf .cur[data-k="0"]{display:none}}
@media (prefers-reduced-motion:reduce){.cf .card{transition:none}}
""", '<section class="cm cf" aria-labelledby="cm-h" ref="{{ secRef }}"><div class="wrap">'
   + f'<div class="head">{H2}<p class="intro">{INTRO}</p></div><ul>'
   + "".join(f'<li><article class="card" data-i="{i}">{ph(i)}<div class="tx"><h3>{p[0]}</h3><span class="role">{p[2]}</span><p class="desc">{p[3]}</p></div></article></li>' for i, p in enumerate(PEOPLE))
   + "</ul></div>" + "".join(f'<span class="cur" data-k="{k}" aria-hidden="true" style="--c: {c}">{CUR}<span>{n}</span></span>' for k, (n, c) in enumerate(CURSORS))
   + "</section>",
   script(mount="""
    var curs = [].slice.call(s.querySelectorAll('.cur')), cards = [].slice.call(s.querySelectorAll('.card'));
    var st = curs.map(function (c, k) { return { x: 0, y: 0, ph: k * 1.9, set: false }; }), hover = -1, raf = 0, t0 = performance.now(), vis = true;
    // where each cursor hangs out: Alessia roams the middle, each collaborator stays near her card
    var home = function (k, t) {
      var r = s.getBoundingClientRect(), c, a = st[k].ph;
      if (k === 0) { var hd = s.querySelector('.head').getBoundingClientRect(); return { x: hd.left - r.left + hd.width * (0.5 + 0.4 * Math.sin(t * 0.21 + a)), y: hd.bottom - r.top + 18 + 12 * Math.sin(t * 0.5 + a) }; }
      c = cards[k - 1].querySelector('.ph').getBoundingClientRect();   // over her own photo, never over the text
      if (hover === k - 1) { var h = cards[k - 1].querySelector('h3').getBoundingClientRect(); return { x: h.right - r.left + 6, y: h.top - r.top + h.height * 0.6 }; }
      return { x: c.left - r.left + c.width * (0.5 + 0.3 * Math.sin(t * 0.37 + a)), y: c.top - r.top + c.height * (0.42 + 0.26 * Math.sin(t * 0.29 + a * 1.7)) };
    };
    var step = function (now) {
      raf = 0; var t = (now - t0) / 1000;
      curs.forEach(function (el, k) {
        var q = st[k], h = home(k, reduce ? 0 : t);
        if (!q.set || reduce) { q.x = h.x; q.y = h.y; q.set = true; }
        var ease = hover === k - 1 ? 0.12 : 0.05;
        q.x += (h.x - q.x) * ease; q.y += (h.y - q.y) * ease;
        el.style.transform = 'translate3d(' + q.x.toFixed(1) + 'px,' + q.y.toFixed(1) + 'px,0)';
      });
      if (!reduce && vis) raf = requestAnimationFrame(step);
    };
    raf = requestAnimationFrame(step);
    this.over = function (e) { var c = e.target.closest && e.target.closest('.card'); hover = c ? +c.getAttribute('data-i') : -1; };
    this.out = function () { hover = -1; };
    s.addEventListener('pointerover', this.over); s.addEventListener('pointerleave', this.out);
    if (window.IntersectionObserver) {   // only animate while the section is on screen
      this.io2 = new IntersectionObserver(function (es) { vis = es[0].isIntersecting; if (vis && !raf) raf = requestAnimationFrame(step); });
      this.io2.observe(s);
    }
    this.stop = function () { cancelAnimationFrame(raf); };""",
          unmount="if (this.stop) this.stop(); if (this.io2) this.io2.disconnect(); if (this.sec && this.over) { this.sec.removeEventListener('pointerover', this.over); this.sec.removeEventListener('pointerleave', this.out); }"))


# 5. Carduri (Vali, 11 nov, feedback from Alessia): only the intro paragraph, then one small card per collaborator with
#    the name and the subtitle (their long texts are gone). Valentin added; his subtitle is mine, to approve.
#    The example card from another site hasn't arrived yet: this is an AVA-styled proposal, to adjust to the example.
#    Motion: the site's scroll reveal only, plus a 3px lift on hover.
# Vali (11 nov, canvas comments): Iuliana „Colaboratoare · Facilitatoare”, Valentin „Specialist IT”
CARDS = [(p[0], "Colaboratoare · Facilitatoare" if p[0] == "Iuliana Petrescu" else p[2]) for p in PEOPLE] + [("Valentin Stefanescu", "Specialist IT")]
SOURCES["Comunitate5Carduri"] = "un card mic per colaboratoare, după exemplul trimis de Vali (în stilul AVA)"
OPTS["Comunitate5Carduri"] = ("Comunitatea 5: intro + carduri", """
.ck5{background:linear-gradient(180deg,#F4EDE4 0%,#EFE4D4 100%);padding:112px 0 120px}
.ck5 ul{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:48px 0 0;padding:0;list-style:none}
.ck5 li{padding:24px 24px 26px;border-radius:22px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);transition:translate .4s cubic-bezier(.22,1,.36,1),box-shadow .4s ease}
@media (hover:hover){.ck5 li:hover{translate:0 -3px;box-shadow:0 0 0 1px rgba(58,42,32,.08),0 18px 30px -22px rgba(58,30,15,.45)}}
.ck5 .nm{margin:0;font:400 23px/1.2 var(--display);font-variation-settings:'opsz' 20;color:var(--ink)}
.ck5 .role{margin-top:8px;font-size:17px}
@keyframes ck5-up{from{opacity:0;translate:0 16px}}
.ck5.js:not(.in) :is(h2,.intro,li){opacity:0}
.ck5.js.in :is(h2,.intro){animation:ck5-up .8s cubic-bezier(.22,1,.36,1) backwards}
.ck5.js.in .intro{animation-delay:80ms}
.ck5.js.in li{animation:ck5-up .8s cubic-bezier(.22,1,.36,1) backwards;animation-delay:calc(160ms + var(--i) * 80ms)}
@media (max-width:980px){.ck5{padding:72px 0 80px}.ck5 ul{grid-template-columns:1fr;gap:10px;margin-top:32px}.ck5 li{padding:20px 22px}}
@media (prefers-reduced-motion:reduce){.ck5 *{animation:none!important;transition:none!important}}
""", '<section class="cm ck5" aria-labelledby="cm-h" ref="{{ secRef }}"><div class="wrap">' + H2 + f'<p class="intro">{INTRO}</p><ul>'
   + "".join(f'<li style="--i: {i}"><p class="nm">{n}</p><span class="role">{r}</span></li>' for i, (n, r) in enumerate(CARDS))
   + "</ul></div></section>", script())

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
H = {"Comunitate1Lista": (1152, 1223), "Comunitate2Highlights": (1106, 1158), "Comunitate3Contributori": (1319, 2219), "Comunitate4Cursoare": (1091, 2333), "Comunitate5Carduri": (662, 855)}

if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "comunitate-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Comunitate mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:2600px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
