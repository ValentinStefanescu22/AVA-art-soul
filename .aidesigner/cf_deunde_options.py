"""Pagina „Ce oferim”, part 2: „De unde încep?”. Four directions, each from a real product, all animated.

usage: python3 .aidesigner/cf_deunde_options.py
writes .aidesigner/canvas/project/DeUnde1..4*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-DeUnde*.html
Copy: docs/continut-site.md, Acasă FAQ „Nu știu ce mi se potrivește. De unde încep?” and its answer (3 sentences), the
services' facts from their pages. Mine (to approve): the three quiz options in 1, „Scrie-mi” (as on the Acasă FAQ card),
the short fact lines in 4 (summaries of the doc). „Înapoi” and „Toate serviciile” were approved on 11 nov.
Motion rules as in cf_pagina_options.py.
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW, DUO_SQ, ALT
from cf_pagina_options import script, img, meta, G, PR, CO

Q = "Nu știu ce mi se potrivește. De unde încep?"
A1 = "Dacă vrei să încerci, un atelier de grup e cel mai simplu început."
A2 = "Dacă vrei ceva doar pentru tine, alege un atelier privat sau o ședință de consiliere."
A3 = "Poți explora opțiunile pe site sau îmi poți scrie și te ajut să alegi."
WRITE, ALLS = "Scrie-mi", "Toate serviciile"
SOURCES = {
    "DeUnde1Typeform": "typeform.com: o singură întrebare pe ecran, variante cu literele A, B, C",
    "DeUnde2Mesaje": "Apple Messages (iMessage): bulele de chat și cele trei puncte „scrie…”",
    "DeUnde3Carte": "„Choose Your Own Adventure” (Bantam Books, 1979): alegi și întorci pagina",
    "DeUnde4Compara": "apple.com/iphone/compare: modelele puse unul lângă altul, pe coloane",
}

COMMON = """
.du{position:relative;overflow:clip;--sp:cubic-bezier(.3,1.32,.5,1);--so:cubic-bezier(.22,1,.36,1)}
.du a{text-decoration:none}
.du h2{font-size:clamp(38px,4vw,58px);line-height:1.06}
.du .m{display:block;font-size:14px;line-height:1.5;color:#833A22;font-variant-numeric:tabular-nums}
.du .n{display:block;font:400 30px/1.1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em}
.du .btn{display:inline-flex;align-items:center;gap:10px;min-height:48px;padding:0 24px;border-radius:999px;background:var(--ink);color:#F4EDE4;font-weight:500;transition:background .25s ease,scale .4s var(--sp)}
.du .btn:hover{background:#2A1D16;scale:1.03}.du .btn:hover .ar{transform:translateX(4px)}
.du .btn.ghost{background:none;color:var(--ink);box-shadow:inset 0 0 0 1px rgba(58,42,32,.35)}
.du .btn.ghost:hover{background:rgba(58,42,32,.06)}
.du :is(button,a):focus-visible{outline:2px solid var(--terra-d);outline-offset:4px}
@media (prefers-reduced-motion:reduce){.du *{animation:none!important;transition:none!important}}
"""


def btn(label, href, ghost=False):
    return f'<a class="btn{" ghost" if ghost else ""}" href="{href}">{label} {ARROW}</a>'


OPTS = {}

# 1. Typeform: one question, three big options keyed A / B / C. Pick one (click or the letter key while the section has
#    focus): it blinks twice like Typeform's confirmation, the others step back, the thin progress line fills and the
#    answer rises in with its links. Without JS every answer is simply listed under the options.
OPTS1 = [("Vreau să încerc", A1, btn(G["name"], "#grup")),
         ("Vreau ceva doar pentru mine", A2, btn(PR["name"], "#privat") + btn(CO["name"], "#consiliere", True)),
         ("Vreau să vorbim întâi", A3, btn(WRITE, "#contact") + btn(ALLS, "#ce-facem", True))]
CHECK = '<svg class="ck" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5L6.5 12L13 4.5" fill="none" stroke="currentColor" style="stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
OPTS["DeUnde1Typeform"] = ("De unde încep 1: întrebarea", """
.d1{background:linear-gradient(180deg,#EFE4D4 0%,#F4EDE4 100%);padding:120px 0 128px}
.d1 .prog{position:absolute;left:0;right:0;top:0;height:4px;background:rgba(58,42,32,.08)}
.d1 .prog span{display:block;height:100%;background:var(--terra);transform-origin:0 50%;scale:0 1;transition:scale .9s var(--sp)}
.d1[data-o] .prog span{scale:1 1}
.d1 .stage{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 96px;align-items:start}
.d1 h2{max-width:13ch}
.d1 .opts{display:flex;flex-direction:column;gap:12px;margin:0;padding:0}
.d1 .op{display:flex;align-items:center;gap:16px;width:100%;min-height:64px;padding:12px 18px 12px 14px;border:0;border-radius:14px;box-shadow:inset 0 0 0 1px rgba(156,71,44,.35);background:rgba(244,237,228,.6);color:var(--ink);font:500 19px/1.3 var(--text);text-align:left;cursor:pointer;
  transition:background .25s ease,box-shadow .25s ease,opacity .4s ease,translate .5s var(--sp)}
.d1 .op:hover{background:rgba(180,88,58,.08);box-shadow:inset 0 0 0 1px rgba(156,71,44,.7)}
.d1 kbd{display:grid;place-items:center;flex:none;width:30px;height:30px;border-radius:7px;box-shadow:inset 0 0 0 1px rgba(156,71,44,.5);background:#FBF7F1;color:var(--terra-d);font:600 14px/1 var(--text)}
.d1 .op .tx{flex:1 1 auto}
.d1 .ck{flex:none;width:20px;height:20px;color:var(--terra-d);opacity:0;scale:.4;transition:opacity .25s ease,scale .45s var(--sp)}
.d1 .op[aria-pressed="true"]{background:rgba(180,88,58,.13);box-shadow:inset 0 0 0 2px var(--terra-d);translate:6px 0}
.d1 .op[aria-pressed="true"] kbd{background:var(--terra-d);color:#F4EDE4;box-shadow:none}
.d1 .op[aria-pressed="true"] .ck{opacity:1;scale:1}
.d1[data-o] .op[aria-pressed="false"]{opacity:.5}
@keyframes d1-blink{0%,50%,100%{background:rgba(180,88,58,.13)}25%,75%{background:rgba(180,88,58,.32)}}
.d1 .op.blink{animation:d1-blink .5s linear}
.d1 .answ{display:grid;margin-top:32px}
.d1 .ans{grid-area:1/1;padding:26px 28px 28px;border-radius:20px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 24px 40px -30px rgba(58,30,15,.5)}
.d1 .ans p{margin:0;font:400 22px/1.4 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.d1 .ans .acts{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.d1.js .ans{opacity:0;visibility:hidden;translate:0 18px;transition:opacity .3s ease,translate .5s var(--so),visibility 0s .3s}
""" + "".join(f'.d1.js[data-o="{i}"] .ans[data-o="{i}"]{{opacity:1;visibility:visible;translate:none;transition:opacity .45s ease .35s,translate .7s var(--sp) .35s,visibility 0s}}' for i in range(3)) + """
.d1:not(.js) .answ{gap:12px}.d1:not(.js) .ans{grid-area:auto}
@keyframes d1-in{from{opacity:0;translate:0 22px}}
.d1.js:not(.in) :is(h2,.op){opacity:0}
.d1.js.in h2{animation:d1-in .8s var(--so) backwards}
.d1.js.in .op{animation:d1-in .7s var(--so) backwards;animation-delay:calc(.25s + var(--i) * 90ms)}
@media (max-width:980px){.d1{padding:76px 0 84px}.d1 .stage{grid-template-columns:1fr;gap:32px}.d1 .op{font-size:17px;min-height:60px}.d1 .answ{margin-top:20px}.d1 .ans{padding:22px 20px 24px}.d1 .ans p{font-size:20px}}
""", '<section class="du d1" aria-labelledby="du-h" ref="{{ secRef }}"><div class="prog" aria-hidden="true"><span></span></div><div class="wrap stage">'
   + f'<h2 class="disp" id="du-h">{Q}</h2><div><div class="opts" role="group" aria-label="Alege ce ți se potrivește">'
   + "".join(f'<button class="op" data-o="{i}" aria-pressed="false" style="--i: {i}"><kbd>{"ABC"[i]}</kbd><span class="tx">{o[0]}</span>{CHECK}</button>' for i, o in enumerate(OPTS1))
   + '</div><div class="answ" aria-live="polite">' + "".join(f'<div class="ans" data-o="{i}"><p>{o[1]}</p><div class="acts">{o[2]}</div></div>' for i, o in enumerate(OPTS1))
   + "</div></div></div></section>",
   script(mount="""
    var ops = [].slice.call(s.querySelectorAll('.op'));
    var pick = function (i) {
      ops.forEach(function (o, j) { o.setAttribute('aria-pressed', j === i ? 'true' : 'false'); o.classList.remove('blink'); });
      void ops[i].offsetWidth; ops[i].classList.add('blink'); s.setAttribute('data-o', i);
    };
    this.click = function (e) { var o = e.target.closest && e.target.closest('.op'); if (o) pick(+o.getAttribute('data-o')); };
    this.key = function (e) { var i = 'abc'.indexOf((e.key || '').toLowerCase()); if (i >= 0 && !e.metaKey && !e.ctrlKey && !e.altKey) { pick(i); ops[i].focus(); } };
    s.addEventListener('click', this.click); s.addEventListener('keydown', this.key);""",
          unmount="if (this.sec && this.click) { this.sec.removeEventListener('click', this.click); this.sec.removeEventListener('keydown', this.key); }"))

# 2. Mesaje (iMessage): the question is the visitor's bubble; Alessia answers in her own words, one bubble at a time, each
#    preceded by the three bouncing dots, then the answers become quick-reply chips. Runs once when the chat arrives.
AV = f'<img class="av" src="{DUO_SQ}" alt="" aria-hidden="true">'
DOTS = '<span class="dots" aria-hidden="true"><i></i><i></i><i></i></span>'
OPTS["DeUnde2Mesaje"] = ("De unde încep 2: mesajele", """
.d2{background:radial-gradient(ellipse 50% 60% at 50% 40%,#FAF4EA 0%,rgba(250,244,234,0) 70%),#EFE4D4;padding:112px 0 120px}
.d2 .win{max-width:680px;margin:0 auto;border-radius:34px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 40px 70px -40px rgba(58,30,15,.55),0 0 0 1px rgba(58,42,32,.06);overflow:hidden}
.d2 .top{display:flex;flex-direction:column;align-items:center;gap:6px;padding:22px 0 16px;border-bottom:1px solid rgba(58,42,32,.08);background:rgba(244,237,228,.7)}
.d2 .top img{width:52px;height:52px;border-radius:50%;object-fit:cover}
.d2 .top span{font-size:14px;font-weight:500}
.d2 .log{display:flex;flex-direction:column;gap:8px;padding:28px 26px 30px}
.d2 .b{max-width:78%;margin:0;padding:12px 18px;border-radius:22px;font:400 17px/1.45 var(--text);text-wrap:pretty}
.d2 h2.b{align-self:flex-end;background:var(--terra-d);color:#FBF3EA;font:400 17px/1.45 var(--text);letter-spacing:0;border-bottom-right-radius:6px;margin-bottom:14px}
.d2 .row{display:flex;align-items:flex-end;gap:10px}
.d2 .av{flex:none;width:30px;height:30px;border-radius:50%;object-fit:cover;opacity:0}
.d2 .row.last .av{opacity:1}
.d2 .her{background:#EADCC8;color:var(--ink);border-bottom-left-radius:6px}
.d2 .dots{display:none;gap:5px;padding:4px 2px}
.d2 .dots i{width:8px;height:8px;border-radius:50%;background:#8C7564;animation:d2-dot 1.2s ease-in-out infinite}
.d2 .dots i:nth-child(2){animation-delay:.15s}.d2 .dots i:nth-child(3){animation-delay:.3s}
@keyframes d2-dot{0%,60%,100%{translate:0 0;opacity:.45}30%{translate:0 -5px;opacity:1}}
@keyframes d2-pop{from{opacity:0;scale:.6;translate:0 12px}}
.d2.js .row:not(.typing):not(.said){display:none}
.d2.js .row.typing .dots{display:flex}.d2.js .row.typing .t{display:none}
.d2.js .row.typing,.d2.js .row.said .t{animation:d2-pop .45s var(--sp) backwards}
.d2.js .row .her{transform-origin:0 100%}
.d2.js h2.b{transform-origin:100% 100%}
.d2.js:not(.in) h2.b{opacity:0}
.d2.js.in h2.b{animation:d2-pop .5s var(--sp) .2s backwards}
.d2 .chips{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:8px;margin-top:16px}
.d2 .chips a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 18px;border-radius:999px;box-shadow:inset 0 0 0 1px rgba(156,71,44,.5);color:var(--terra-d);font-weight:500;font-size:15px;transition:background .25s ease,scale .4s var(--sp)}
.d2 .chips a:hover{background:rgba(180,88,58,.1);scale:1.04}
.d2.js:not(.done) .chips a{opacity:0}
.d2.js.done .chips a{animation:d2-pop .5s var(--sp) backwards;animation-delay:calc(var(--i) * 80ms)}
@media (max-width:980px){.d2{padding:64px 0 72px}.d2 .win{border-radius:26px}.d2 .log{padding:22px 14px 24px}.d2 .b{max-width:84%;font-size:16px}.d2 h2.b{font-size:16px}.d2 .chips{justify-content:flex-start;padding-left:40px}}
""", '<section class="du d2" aria-labelledby="du-h" ref="{{ secRef }}"><div class="wrap"><div class="win">'
   + f'<div class="top"><img src="{DUO_SQ}" alt="{ALT}"><span>Alessia Văideanu</span></div><div class="log">'
   + f'<h2 class="b" id="du-h">{Q}</h2>'
   + "".join(f'<div class="row{" last" if i == 2 else ""}">{AV}<p class="b her">{DOTS}<span class="t">{a}</span></p></div>' for i, a in enumerate((A1, A2, A3)))
   + '<div class="chips">' + "".join(f'<a href="{h}" style="--i: {i}">{l} {ARROW}</a>' for i, (l, h) in enumerate(((G["name"], "#grup"), (PR["name"], "#privat"), (CO["name"], "#consiliere"), (WRITE, "#contact"))))
   + "</div></div></div></div></section>",
   script(mount="""
    var rows = [].slice.call(s.querySelectorAll('.row')), timers = this.timers = [];
    var all = function () { rows.forEach(function (r) { r.classList.remove('typing'); r.classList.add('said'); }); s.classList.add('done'); };
    if (reduce || !window.IntersectionObserver) { all(); return; }
    var at = function (ms, f) { timers.push(setTimeout(f, ms)); };
    this.io2 = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; self.io2.disconnect();
      var t = 900;
      rows.forEach(function (r, i) {
        at(t, function () { r.classList.add('typing'); });
        t += 1100 + i * 250;
        at(t, function () { r.classList.remove('typing'); r.classList.add('said'); });
        t += 450;
      });
      at(t + 150, function () { s.classList.add('done'); });
    }, { threshold: 0.35 });
    this.io2.observe(s);""",
          unmount="if (this.io2) this.io2.disconnect(); (this.timers || []).forEach(clearTimeout);"))

# 3. Carte („Choose Your Own Adventure”): an open book. The left page asks, the right page offers the three „Dacă…”
#    sentences. Point at a choice and the page lifts a little; pick one and the page turns: its back lands on the left
#    with the photo, the next page on the right tells you about that service. „Înapoi” turns it back.
#    Phone: one page that turns over in place, like a card.
TG = [G, PR, CO]
RINGS = ('<svg class="orn" viewBox="0 0 120 34" aria-hidden="true">'
         + "".join(f'<path d="M4 {y}C19 {y-6} 34 {y-6} 49 {y}S79 {y+6} 94 {y}S112 {y-4} 116 {y}" style="stroke:{c}"></path>'
                   for y, c in ((9, "#3A2A20"), (17, "#B4583A"), (25, "#3A2A20")))
         + "</svg>")


def ch(i):
    return f'<a class="ch" href="#{TG[i]["k"]}" data-t="{i}">{TG[i]["name"]} {ARROW}</a>'


BACKBTN = '<button class="back" type="button"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M13 8H3M7 4L3 8L7 12" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>Înapoi</button>'


def dest(s):
    return f'<span class="n">{s["name"]}</span><p class="ln">{s["line"]}</p>{meta(s)}{btn(s["cta"], "#" + s["k"])}{BACKBTN}'


OPTS["DeUnde3Carte"] = ("De unde încep 3: cartea", """
.d3{background:linear-gradient(180deg,#F4EDE4 0%,#E9DCC8 100%);padding:112px 0 128px}
.d3 .book{position:relative;display:grid;grid-template-columns:1fr 1fr;max-width:1060px;height:600px;margin:0 auto;perspective:2200px}
.d3 .book::before{content:"";position:absolute;inset:14px -14px -16px;border-radius:10px;background:#C9B496;box-shadow:0 50px 70px -40px rgba(58,30,15,.6)}
.d3 .pg{position:relative;box-sizing:border-box;height:100%;padding:64px 60px;background:#FBF6EE}
.d3 .left{border-radius:8px 0 0 8px;background:linear-gradient(270deg,rgba(58,30,15,.12),rgba(58,30,15,0) 12%),#FBF6EE;display:flex;flex-direction:column;justify-content:center}
.d3 .orn{display:block;width:96px;height:28px;margin-top:36px;fill:none;stroke-width:2.2px;stroke-linecap:round}
.d3 .under{border-radius:0 8px 8px 0;background:linear-gradient(90deg,rgba(58,30,15,.12),rgba(58,30,15,0) 12%),#FBF6EE}
.d3 .leaf{position:absolute;top:0;right:0;width:50%;height:100%;transform-origin:0 50%;transform-style:preserve-3d;transition:transform 1.15s cubic-bezier(.6,.05,.25,1)}
.d3 .face{position:absolute;inset:0;box-sizing:border-box;backface-visibility:hidden;-webkit-backface-visibility:hidden}
.d3 .front{padding:64px 60px;border-radius:0 8px 8px 0;background:linear-gradient(90deg,rgba(58,30,15,.12),rgba(58,30,15,0) 12%),#FBF6EE;display:flex;flex-direction:column;justify-content:center;gap:26px}
.d3 .front p{margin:0;font:400 21px/1.45 var(--display);font-variation-settings:'opsz' 20;text-wrap:pretty}
.d3 .front .ch{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-right:16px;color:var(--terra-d);font:500 16px/1.2 var(--text);background:linear-gradient(currentColor,currentColor) 0 calc(100% - 10px)/100% 1px no-repeat}
.d3 .front .ch:hover .ar{transform:translateX(4px)}
.d3 .front .lk{display:flex;flex-wrap:wrap;gap:0 4px}
.d3 .rev{transform:rotateY(180deg);border-radius:8px 0 0 8px;overflow:hidden;background:#5B3A27}
.d3 .rev img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 0s .6s}
.d3 .rev::after{content:"";position:absolute;inset:0;background:linear-gradient(270deg,rgba(20,10,5,.35),rgba(20,10,5,0) 14%)}
.d3 .dst{position:absolute;inset:0;box-sizing:border-box;padding:64px 60px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;opacity:0;visibility:hidden;transition:opacity .4s ease,visibility 0s .4s}
.d3 .dst .n{font-size:44px}
.d3 .dst .ln{margin:14px 0 0;font-size:18px;line-height:1.55;color:var(--ink2);max-width:36ch}
.d3 .dst .m{margin:12px 0 26px}
.d3 button.back{display:inline-flex;align-items:center;gap:8px;min-height:44px;margin-top:14px;padding:0;border:0;background:none;color:var(--ink2);font:500 15px/1 var(--text);cursor:pointer}
.d3 button.back svg{width:16px;height:16px}
.d3 button.back:hover{color:var(--ink)}
""" + "".join(f'.d3[data-t="{i}"] .rev img[data-t="{i}"]{{opacity:1;transition:none}}.d3.turned[data-t="{i}"] .dst[data-t="{i}"]{{opacity:1;visibility:visible;transition:opacity .5s ease .7s,visibility 0s}}' for i in range(3)) + """
.d3.turned .leaf{transform:rotateY(-180deg)}
@media (hover:hover){.d3:not(.turned) .book:has(.ch:hover) .leaf{transform:rotateY(-7deg)}}
.d3 .mob{display:none}
@keyframes d3-open{from{transform:rotateY(-100deg)}}
@keyframes d3-up{from{opacity:0;translate:0 30px}}
.d3.js:not(.in) .book{opacity:0}
.d3.js.in .book{animation:d3-up .9s var(--so) backwards}
.d3.js.in:not(.turned) .leaf{animation:d3-open 1.4s cubic-bezier(.3,1.2,.4,1) .35s backwards}
@media (max-width:980px){
  .d3{padding:68px 0 80px}
  .d3 .book{display:block;height:640px;perspective:1600px}
  .d3 .book::before{inset:10px -6px -10px 6px}
  .d3 .left,.d3 .under{display:none}
  .d3 .head{display:block;margin-bottom:32px}
  .d3 .leaf{width:100%;transform-origin:50% 50%}
  .d3.turned .leaf{transform:rotateY(180deg)}
  .d3:not(.turned) .book:has(.ch:hover) .leaf{transform:none}
  .d3 .front{padding:40px 26px;border-radius:8px}.d3 .front p{font-size:19px}
  .d3 .rev{border-radius:8px}
  .d3 .rev img{height:42%}
  .d3 .rev::after{display:none}
  .d3 .mob{display:block;position:absolute;left:0;right:0;bottom:0;top:42%;background:#FBF6EE}
  .d3 .mob .dst{padding:24px 24px 26px;justify-content:flex-start}
  .d3 .mob .dst .n{font-size:30px}.d3 .mob .dst .ln{font-size:16px;margin-top:8px}.d3 .mob .dst .m{margin:8px 0 16px}
  """ + "".join(f'.d3.turned[data-t="{i}"] .mob .dst[data-t="{i}"]{{opacity:1;visibility:visible;transition:opacity .4s ease .6s,visibility 0s}}' for i in range(3)) + """
  .d3.js.in:not(.turned) .leaf{animation:none}
}
@media (min-width:981px){.d3 .head{display:none}}
""", '<section class="du d3" data-t="0" aria-labelledby="du-h" ref="{{ secRef }}"><div class="wrap">'
   + f'<h2 class="disp head" aria-hidden="true">{Q}</h2><div class="book">'
   + f'<div class="pg left"><h2 class="disp" id="du-h">{Q}</h2>{RINGS}</div>'
   + '<div class="pg under">' + "".join(f'<div class="dst" data-t="{i}">{dest(s)}</div>' for i, s in enumerate(TG)) + "</div>"
   + '<div class="leaf"><div class="face front">'
   + f'<p>{A1}</p><div class="lk">{ch(0)}</div><p>{A2}</p><div class="lk">{ch(1)}{ch(2)}</div>'
   + f'<p>{A3}</p><div class="lk"><a class="ch" href="#contact">{WRITE} {ARROW}</a><a class="ch" href="#ce-facem">{ALLS} {ARROW}</a></div></div>'
   + '<div class="face rev">' + "".join(f'<img data-t="{i}" src="{s["img"]}" alt="" style="object-position: {s["pos"]}">' for i, s in enumerate(TG))
   + '<div class="mob">' + "".join(f'<div class="dst" data-t="{i}">{dest(s)}</div>' for i, s in enumerate(TG)) + "</div></div></div>"
   + "</div></div></section>",
   script(mount="""
    var front = s.querySelector('.front'), dsts = [].slice.call(s.querySelectorAll('.dst'));
    var sync = function () {
      var on = s.classList.contains('turned'), t = s.getAttribute('data-t');
      front.inert = on;
      dsts.forEach(function (d) { d.inert = !(on && d.getAttribute('data-t') === t); });
    };
    sync();
    this.click = function (e) {
      var c = e.target.closest && e.target.closest('.ch[data-t]');
      if (c) { e.preventDefault(); s.setAttribute('data-t', c.getAttribute('data-t')); s.classList.add('turned'); sync(); return; }
      if (e.target.closest && e.target.closest('button.back')) { s.classList.remove('turned'); sync(); var f = front.querySelector('.ch[data-t="' + s.getAttribute('data-t') + '"]'); if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 600); }
    };
    s.addEventListener('click', this.click);""",
          unmount="if (this.sec && this.click) this.sec.removeEventListener('click', this.click);"))

# 4. Compară (apple.com/iphone/compare): the three ways in, side by side. On top, the FAQ sentences over their columns
#    (the second spans privat + consiliere, with a drawn bracket). The columns rise one after another and the facts fill
#    in row by row like a wave; point at a column and it lifts while the others step back. Phone: swipe the columns.
I = {
    "who": '<path d="M5.5 7.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM1 14c0-2.5 2-4.5 4.5-4.5S10 11.5 10 14M11 7.5a2 2 0 1 0 0-4M12 9.7c1.8.4 3 2 3 4.3"></path>',
    "time": '<circle cx="8" cy="8" r="6.3"></circle><path d="M8 4.5V8L10.5 9.5"></path>',
    "price": '<path d="M8.6 1.8H14.2V7.4L7.6 14L2 8.4ZM11.4 4.6h.01"></path>',
    "where": '<path d="M8 14.5S3 9.8 3 6.3a5 5 0 0 1 10 0c0 3.5-5 8.2-5 8.2Z"></path><circle cx="8" cy="6.3" r="1.7"></circle>',
    "inc": '<path d="M2.5 8.5L6 12L13.5 4"></path>',
}
FACTS = {
    "grup": [("who", "Grup de maxim 8 persoane"), ("time", "3 ore, o dată pe lună"), ("price", "De la 185 lei / persoană"), ("where", "București"), ("inc", "Materiale, ghidare, o băutură / gustare")],
    "privat": [("who", "Doar tu, sau doi: cuplu, mamă-fiică"), ("time", "60 sau 90 de minute"), ("price", "De la 220 lei"), ("where", "București"), ("inc", "Pentru adult sau copil, materialele incluse")],
    "consiliere": [("who", "Doar tu"), ("time", "60–90 de minute"), ("price", "180 lei / oră"), ("where", "Online sau față în față"), ("inc", "Prima discuție, de 15 minute, gratuită")],
}


def ic(k):
    return f'<svg class="fi" viewBox="0 0 16 16" aria-hidden="true"><g fill="none" stroke="currentColor" style="stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round">{I[k]}</g></svg>'


cells4 = ""
for c, s in enumerate(TG):
    col = c + 1
    cells4 += f'<div class="cbg" data-c="{c}" style="grid-column: {col}; --c: {c}"></div>'
    cells4 += f'<div class="ph" data-c="{c}" style="grid-column: {col}; --c: {c}; --r: 0">{img(s)}</div>'
    cells4 += f'<span class="n" data-c="{c}" style="grid-column: {col}; --c: {c}; --r: 1">{s["name"]}</span>'
    for r, (k, v) in enumerate(FACTS[s["k"]]):
        cells4 += f'<span class="fc" data-c="{c}" style="grid-column: {col}; grid-row: {r + 5}; --c: {c}; --r: {r + 2}">{ic(k)}{v}</span>'
    cells4 += f'<span class="cta" data-c="{c}" style="grid-column: {col}; --c: {c}; --r: 8">{btn(s["cta"], "#" + s["k"], c > 0)}</span>'
OPTS["DeUnde4Compara"] = ("De unde încep 4: comparația", """
.d4{background:#F4EDE4;padding:112px 0 120px}
.d4 h2{max-width:17ch;margin:0 auto;text-align:center}
.d4 .cmp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:auto auto 260px auto repeat(5,auto) auto;column-gap:28px;margin-top:56px}
.d4 .note{grid-row:1;align-self:end;margin:0;padding:0 26px 18px;font:400 italic 21px/1.4 var(--display);font-variation-settings:'opsz' 20;color:var(--ink);text-wrap:balance}
.d4 .br{grid-row:2;position:relative;height:10px;margin:0 22px 26px;border:1.5px solid var(--clay);border-top:0;border-radius:0 0 6px 6px}
.d4 .br.two::after{content:"";position:absolute;left:50%;top:100%;width:1.5px;height:10px;background:var(--clay)}
.d4 .cbg{grid-row:3/-1;border-radius:28px;corner-shape:squircle;background:#FBF7F1;box-shadow:0 0 0 1px rgba(58,42,32,.06);transition:box-shadow .5s var(--so),translate .6s var(--sp),opacity .4s ease}
.d4 .ph{grid-row:3;overflow:hidden;margin:12px 12px 0;border-radius:20px;corner-shape:squircle}
.d4 .ph img{display:block;width:100%;height:100%;object-fit:cover;transition:scale 1s var(--so)}
.d4 .n{grid-row:4;padding:24px 26px 14px;font-size:30px}
.d4 .fc{display:flex;gap:12px;align-items:flex-start;margin:0 26px;padding:13px 0;border-top:1px solid rgba(58,42,32,.1);font-size:15px;line-height:1.45}
.d4 .fi{flex:none;width:18px;height:18px;margin-top:1px;color:var(--terra-d)}
.d4 .cta{grid-row:10;padding:20px 26px 28px}
.d4 .cta .btn{font-size:15px;min-height:46px;padding:0 20px;white-space:nowrap}
.d4 .more3{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px 24px;margin-top:48px;text-align:center}
.d4 .more3 p{margin:0;font:400 21px/1.4 var(--display);font-variation-settings:'opsz' 20;max-width:40ch}
.d4 .more3 .acts{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
""" + "".join(f'.d4[data-hc="{c}"] :is(.cbg,.ph,.n,.fc,.cta):not([data-c="{c}"]){{opacity:.5}}.d4[data-hc="{c}"] .cbg[data-c="{c}"]{{translate:0 -8px;box-shadow:0 40px 60px -36px rgba(58,30,15,.5),0 0 0 1px rgba(156,71,44,.25)}}.d4[data-hc="{c}"] :is(.ph,.n,.fc,.cta)[data-c="{c}"]{{translate:0 -8px}}.d4[data-hc="{c}"] .ph[data-c="{c}"] img{{scale:1.05}}' for c in range(3)) + """
.d4 :is(.ph,.n,.fc,.cta){transition:opacity .4s ease,translate .6s var(--sp)}
@keyframes d4-rise{from{opacity:0;translate:0 40px}}
@keyframes d4-fade{from{opacity:0;translate:0 10px}}
@keyframes d4-draw{from{clip-path:inset(0 100% -12px 0)}to{clip-path:inset(0 0 -12px 0)}}
.d4.js:not(.in) :is(.cbg,.ph,.n,.fc,.cta,.note){opacity:0}
.d4.js:not(.in) .br{clip-path:inset(0 100% -12px 0)}
.d4.js.in .cbg{animation:d4-rise .9s var(--so) backwards;animation-delay:calc(var(--c) * 120ms)}
.d4.js.in :is(.ph,.n,.fc,.cta){animation:d4-fade .6s var(--so) backwards;animation-delay:calc(.25s + var(--c) * 120ms + var(--r) * 70ms)}
.d4.js.in .note{animation:d4-fade .7s var(--so) .1s backwards}
.d4.js.in .br{animation:d4-draw 1.2s cubic-bezier(.45,.05,.3,1) .5s backwards}
@media (max-width:980px){
  .d4{padding:68px 0 76px}.d4 h2{text-align:left;margin:0}
  .d4 .cmp{grid-template-columns:repeat(3,82%);grid-template-rows:auto auto 200px auto repeat(5,auto) auto;column-gap:12px;margin:32px -20px 0;padding:0 20px 8px;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding:0 20px;scrollbar-width:none}
  .d4 .cmp::-webkit-scrollbar{display:none}
  .d4 .cbg{scroll-snap-align:start}
  .d4 .note{padding:0 18px 12px;font-size:18px}
  .d4 .n{padding:20px 20px 12px;font-size:26px}.d4 .fc{margin:0 20px}.d4 .cta{padding:18px 20px 22px}.d4 .cta .btn{font-size:14px;padding:0 16px}
  .d4 .more3{justify-content:flex-start;text-align:left;margin-top:32px}.d4 .more3 .acts{justify-content:flex-start}
}
""", '<section class="du d4" aria-labelledby="du-h" ref="{{ secRef }}"><div class="wrap">' + f'<h2 class="disp" id="du-h">{Q}</h2><div class="cmp">'
   + f'<p class="note" style="grid-column: 1">{A1}</p><p class="note" style="grid-column: 2 / 4">{A2}</p>'
   + '<span class="br" style="grid-column: 1" aria-hidden="true"></span>'
   + '<span class="br two" style="grid-column: 2 / 4" aria-hidden="true"></span>'
   + cells4 + "</div>"
   + f'<div class="more3"><p>{A3}</p><div class="acts">{btn(WRITE, "#contact")}{btn(ALLS, "#ce-facem", True)}</div></div></div></section>',
   script(mount="""
    this.over = function (e) { if (e.pointerType !== 'mouse') return; var el = e.target.closest && e.target.closest('[data-c]'); if (el) s.setAttribute('data-hc', el.getAttribute('data-c')); else s.removeAttribute('data-hc'); };
    this.out = function () { s.removeAttribute('data-hc'); };
    var cmp = s.querySelector('.cmp'); cmp.addEventListener('pointerover', this.over); cmp.addEventListener('pointerleave', this.out); this.cmp = cmp;""",
          unmount="if (this.cmp && this.over) { this.cmp.removeEventListener('pointerover', this.over); this.cmp.removeEventListener('pointerleave', this.out); }"))


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
H = {"DeUnde1Typeform": (680, 793), "DeUnde2Mesaje": (787, 817), "DeUnde3Carte": (840, 941), "DeUnde4Compara": (1362, 1214)}

if __name__ == "__main__":
    for name, (title, css, html, js) in OPTS.items():
        for suffix, w, h in (("", 1440, H[name][0]), ("Mobil", 390, H[name][1])):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, html, js, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True, capture_output=True)
        print("wrote", name)
    names = list(OPTS)
    open(os.path.join(HERE, "deunde-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>De unde mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1500px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
