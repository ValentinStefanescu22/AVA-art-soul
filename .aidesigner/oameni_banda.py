"""'Ce spun oamenii' + galerie. Vali chose B2 (10 nov); B, B3, B4 are archived. Origin: B (bandă) refined: arrows on the testimonials, + 3 more band variants.
B  Bandă + săgeți        two photo rows; the quote in the middle with round arrows on its sides and a 1 / 3 counter.
B2 Bandă + bare           same, but story-like progress bars above the quote (you see that it advances, and when).
B3 Carduri + bandă        the testimonials are cards in a row (the next one peeks out), user-driven only; one photo row under them.
B4 Citat cu poza          one tall photo row; a card overlaps it, each testimonial with a photo from its own workshop.

UX shared by all four:
- arrows are 44px buttons; keys ← → work when focus is in the testimonials; swipe on touch screens;
- auto-advance (B, B2) pauses on hover / focus / when off-screen, and stops for good once the visitor uses the arrows:
  they took control (W3C APG carousel pattern); aria-live is 'off' while rotating, 'polite' after;
- a small 'Oprește mișcarea' button stops the band and the rotation (WCAG 2.2.2: moving content needs a pause);
- prefers-reduced-motion: nothing moves, the band becomes a scrollable row.
This script owns OameniB (+Mobil); galerie_options.py skips it.

usage: python3 .aidesigner/oameni_banda.py
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, ARROW
from galerie_options import COMMON, CHEV, H, LINKS, Q, IM, img, quote, row, ROW1, ROW2

N = len(Q)
DUR = "9s"


def bind(name):
    return "{{ " + name + " }}"


PAUSE = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.5v9M11 3.5v9" style="fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round"></path></svg>'
PLAY = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5 3.2v9.6L12.6 8z" style="fill:currentColor"></path></svg>'
STILL = (f'<button class="still" type="button" onClick="{bind("still")}"><span class="i-p">{PAUSE}</span><span class="i-r">{PLAY}</span>'
         f'<span class="lb">Oprește mișcarea</span></button>')
PV = f'<button class="rd pv" type="button" aria-label="Testimonialul anterior" data-d="-1" onClick="{bind("step")}">{CHEV}</button>'
NX = f'<button class="rd nx" type="button" aria-label="Testimonialul următor" data-d="1" onClick="{bind("step")}">{CHEV}</button>'
CNT = ('<span class="cnt" aria-hidden="true"><span class="cn">' + "".join(f"<i>{i + 1}</i>" for i in range(N))
       + f'</span><span class="of">/ {N}</span></span>')
def stage(cls=""):
    return f'class="stage{" " + cls if cls else ""}" role="region" aria-roledescription="carusel" aria-label="Testimoniale"'


STAGE = stage()


def slides(inner=lambda i: quote(i), tick=True):
    return '<div class="sls" aria-live="off">' + "".join(
        f'<div class="sl s{i}" role="group" aria-roledescription="testimonial" aria-label="{i + 1} din {N}">{inner(i)}'
        + ('<span class="tk" aria-hidden="true"></span>' if tick else "") + "</div>" for i in range(N)) + "</div>"


SHARED = """
.og .mq{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent);mask-image:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.og .mq ul{display:flex;gap:14px;width:max-content;list-style:none;margin:0;padding:0;animation:obl 70s linear infinite}
.og .mq.r2 ul{animation-name:obr;animation-duration:80s}
.og .mq:hover ul,.og[data-still] .mq ul,.og[data-off] .mq ul{animation-play-state:paused}
.og .mq li{height:250px;aspect-ratio:4/5;border-radius:20px;corner-shape:squircle;overflow:hidden;flex:none}
.og .mq li:nth-child(3n+2){aspect-ratio:3/2}
.og .mq img{width:100%;height:100%;object-fit:cover}
@keyframes obl{to{transform:translateX(-50%) translateX(-7px)}}
@keyframes obr{from{transform:translateX(-50%) translateX(-7px)}to{transform:none}}
@keyframes obtick{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.og{padding-bottom:88px}
.og .stage{touch-action:pan-y}
.og .sls{display:grid}
.og .sl{grid-area:1/1;position:relative;opacity:0;visibility:hidden;transform:translateX(calc(var(--d,1) * 22px));transition:opacity .45s,transform .7s cubic-bezier(.2,.7,.2,1),visibility 0s linear .45s}
.og .sl[data-out]{transform:translateX(calc(var(--d,1) * -22px))}
.og[data-dir="-1"]{--d:-1}
.og .tk{position:absolute;left:0;top:0;width:1px;height:1px;transform-origin:left}
.og[data-hold] .tk,.og[data-still] .tk,.og[data-off] .tk{animation-play-state:paused!important}
.og .rd[aria-disabled="true"]{opacity:.3;cursor:default;transform:none}
.og .cnt{display:inline-flex;gap:6px;font-size:15px;font-variant-numeric:tabular-nums;color:var(--ink2);letter-spacing:.04em}
.og .cn i{display:none;font-style:normal;color:var(--ink);font-weight:600}
.og .stillrow{display:flex;justify-content:flex-end;margin-top:18px}
.og .still{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 13px;border:1px solid rgba(58,42,32,.22);border-radius:999px;background:none;font-size:14px;color:var(--ink2);transition:border-color .2s,color .2s}
.og .still:hover{border-color:var(--ink);color:var(--ink)}
.og .still svg{width:13px;height:13px}.og .still span{display:inline-flex}
.og .i-r,.og[data-still] .i-p{display:none!important}.og[data-still] .i-r{display:inline-flex!important}
.og .still:focus-visible{outline:2px solid #9C472C;outline-offset:3px}
@media (max-width:820px){.og{padding-bottom:60px}.og .mq li{height:170px}}
@media (prefers-reduced-motion:reduce){.og .mq ul{animation:none}.og .mq{overflow-x:auto}.og .still{display:none}.og .sl{transition:none}}
"""


def states(root, slide=True, bars=False):
    css = ""
    for i in range(N):
        a = f'{root}[data-a="{i}"]'
        if slide:
            css += f'{a} .s{i}{{opacity:1;visibility:visible;transform:none;transition-delay:0s}}'
        css += f'{a} .cn i:nth-child({i + 1}){{display:inline}}'
        css += f'{root}[data-run][data-a="{i}"] .s{i} .tk{{animation:obtick {DUR} linear}}'
        if bars:
            css += "".join(f'{a} .g{j} .tk{{transform:scaleX(1)}}' for j in range(i + 1))
            css += f'{root}[data-run][data-a="{i}"] .g{i} .tk{{animation:obtick {DUR} linear}}'
    return css


OPTS = {}
BAND2 = f'{row(ROW1, "r1")}' + "{MID}" + f'{row(ROW2, "r2")}<div class="wrap stillrow">{STILL}</div>'

# ---------- B. Bandă + săgeți ----------
OPTS["OameniB"] = ("Ce spun oamenii B: bandă + săgeți", "data-wrap data-auto", """
.ob{background:#EFE4D4}
.ob .head{flex-direction:column;align-items:center;text-align:center;gap:18px;margin-bottom:48px}
.ob .stage{display:grid;grid-template-columns:44px minmax(0,1fr) 44px;grid-template-areas:"pv s nx" ". c .";column-gap:56px;align-items:center;max-width:1000px;margin:56px auto;padding:0 40px;text-align:center}
.ob .sls{grid-area:s}.ob .pv{grid-area:pv}.ob .nx{grid-area:nx}.ob .cnt{grid-area:c;justify-self:center;margin-top:26px}
.ob .q .qm{margin:0 auto 22px;width:38px;height:28px}
.ob .q blockquote{font-size:clamp(26px,2.6vw,36px);line-height:1.25}
.ob .q figcaption{justify-content:center}
@media (max-width:820px){.ob .stage{grid-template-areas:"s s s" "pv c nx";column-gap:12px;row-gap:22px;margin:36px auto;padding:0 20px}.ob .cnt{margin:0}.ob .q blockquote{font-size:22px}}
""" + states(".ob"), BAND2.replace("{MID}", f'<div {STAGE}>{slides()}{PV}{NX}{CNT}</div>'))

# ---------- B2. Bandă + bare de progres ----------
SEGS = '<div class="segs">' + "".join(
    f'<button class="seg g{i}" type="button" data-i="{i}" aria-label="Testimonialul {i + 1}" onClick="{bind("pick")}"><span><i class="tk"></i></span></button>'
    for i in range(N)) + "</div>"
OPTS["OameniB2"] = ("Ce spun oamenii B2: bandă + bare de progres", "data-wrap data-auto", """
.ob2{background:linear-gradient(180deg,#F4EDE4 0%,#EDE0CD 100%)}
.ob2 .stage{display:grid;grid-template-columns:44px minmax(0,1fr) 44px;grid-template-areas:". g ." "pv s nx";column-gap:56px;align-items:center;max-width:1000px;margin:60px auto;padding:0 40px;text-align:center}
.ob2 .sls{grid-area:s}.ob2 .pv{grid-area:pv}.ob2 .nx{grid-area:nx}
.ob2 .segs{grid-area:g;justify-self:center;display:flex;gap:6px;width:min(260px,100%);margin-bottom:30px}
.ob2 .seg{flex:1;height:44px;padding:0;border:0;background:none;display:flex;align-items:center}
.ob2 .seg span{display:block;width:100%;height:3px;border-radius:2px;background:rgba(58,42,32,.22);overflow:hidden}
.ob2 .seg .tk{position:static;display:block;width:100%;height:100%;background:#9C472C;transform:scaleX(0)}
.ob2 .seg:hover span{background:rgba(58,42,32,.28)}
.ob2 .seg:focus-visible{outline:2px solid #9C472C;outline-offset:2px;border-radius:4px}
.ob2 .q .qm{display:none}
.ob2 .q blockquote{font-size:clamp(28px,2.8vw,40px);line-height:1.22}
.ob2 .q blockquote::before{content:"„"}.ob2 .q blockquote::after{content:"”"}
.ob2 .q figcaption{justify-content:center}
@media (max-width:820px){.ob2 .stage{grid-template-areas:"pv g nx" "s s s";column-gap:14px;row-gap:22px;margin:36px auto;padding:0 20px}.ob2 .segs{margin:0;width:100%}.ob2 .q blockquote{font-size:23px}}
""" + states(".ob2", bars=True), BAND2.replace("{MID}", f'<div {STAGE}>{SEGS}{slides(tick=False)}{PV}{NX}</div>'))

# ---------- B3. Carduri + bandă ----------
CARDS = '<div class="trk">' + "".join(
    f'<div class="card c{i}" data-i="{i}" onClick="{bind("pick")}" role="group" aria-roledescription="testimonial" aria-label="{i + 1} din {N}">{quote(i)}</div>'
    for i in range(N)) + "</div>"
OPTS["OameniB3"] = ("Ce spun oamenii B3: carduri + bandă", "", """
.ob3{background:#F4EDE4}
.ob3 .stage{overflow:hidden;padding:6px 0 0}
.ob3 .trk{--w:600px;--g:24px;--a:0;--x:max(40px,calc(50% - 580px));position:relative;left:var(--x);display:flex;gap:var(--g);width:max-content;transform:translateX(calc(-1 * var(--a) * (var(--w) + var(--g))));transition:transform .7s cubic-bezier(.22,.8,.2,1)}
.ob3 .card{flex:none;box-sizing:border-box;width:var(--w);min-height:330px;padding:40px 44px 36px;border-radius:26px;corner-shape:squircle;background:#FBF7F0;box-shadow:0 1px 0 rgba(58,42,32,.06),0 30px 60px -44px rgba(70,35,15,.5);opacity:.55;cursor:pointer;transition:opacity .5s,transform .7s cubic-bezier(.22,.8,.2,1)}
.ob3 .card .q{display:flex;flex-direction:column;height:100%}
.ob3 .card figcaption{margin-top:auto;padding-top:24px}
.ob3 .q blockquote{font-size:27px;line-height:1.28}
.ob3 .c1{background:#9C472C;color:#FBF4EA}.ob3 .c1 .qm{color:#F2C79C}.ob3 .c1 figcaption span{color:#F3DCC8}
.ob3 .c2{background:#3A2A20;color:#F4EDE4}.ob3 .c2 .qm{color:#F2C79C}.ob3 .c2 figcaption span{color:#D9C7B4}
.ob3 .ctl{display:flex;justify-content:flex-start;padding-left:max(40px,calc(50% - 580px));align-items:center;gap:22px;margin-top:30px}
.ob3 .band{margin-top:72px}
@media (max-width:820px){.ob3 .trk{--w:calc(100vw - 64px);--g:12px;--x:20px}.ob3 .card{min-height:300px;padding:28px 24px 26px}.ob3 .ctl{padding-left:20px}.ob3 .q blockquote{font-size:21px}.ob3 .ctl{margin-top:22px}.ob3 .band{margin-top:52px}}
""" + states(".ob3", slide=False) + "".join(
    f'.ob3[data-a="{i}"] .trk{{--a:{i}}}.ob3[data-a="{i}"] .c{i}{{opacity:1;transform:none;cursor:auto}}' for i in range(N)),
    f'<div {STAGE}>{CARDS}<div class="ctl">{PV}{CNT}{NX}</div></div>'
    f'<div class="band">{row(ROW1 + ROW2[:3], "r1")}</div><div class="wrap stillrow">{STILL}</div>')

# ---------- B4. Citat cu poza atelierului ----------
B4_PH = ["bol", "grup", "maini", "cani"]  # one photo from the workshop each testimonial comes from (placeholders for now)
OPTS["OameniB4"] = ("Ce spun oamenii B4: citat cu poza atelierului", "data-wrap", """
.ob4{background:#EFE4D4}
.ob4 .mq li{height:320px}
.ob4 .stillrow{margin-top:28px}
.ob4 .card{position:relative;z-index:2;margin:-104px auto 0;max-width:980px;box-sizing:border-box;padding:28px;border-radius:30px;corner-shape:squircle;background:#FBF7F0;box-shadow:0 1px 0 rgba(58,42,32,.06),0 50px 90px -56px rgba(70,35,15,.6)}
.ob4 .sl{display:grid;grid-template-columns:250px minmax(0,1fr);gap:52px;align-items:center}
.ob4 .ph{height:310px;border-radius:20px;corner-shape:squircle;overflow:hidden}
.ob4 .ph img{width:100%;height:100%;object-fit:cover}
.ob4 .q{padding:8px 24px 68px 0}
.ob4 .q blockquote{font-size:clamp(25px,2.3vw,31px);line-height:1.27}
.ob4 .ctl{position:absolute;right:32px;bottom:28px;display:flex;align-items:center;gap:18px}
@media (max-width:820px){.ob4 .mq li{height:220px}.ob4 .card{margin:-60px 16px 0;padding:16px 16px 20px}.ob4 .sl{grid-template-columns:1fr;gap:22px}.ob4 .ph{height:170px}.ob4 .q{padding:0 6px}.ob4 .q blockquote{font-size:21px}
.ob4 .ctl{position:static;justify-content:space-between;margin:20px 6px 0}}
""" + states(".ob4"),
    f'{row(ROW1 + ROW2[:2], "r1")}<div class="wrap"><div {stage("card")}>'
    + slides(lambda i: f'<div class="ph">{img(B4_PH[i]).replace(" loading=" + chr(34) + "lazy" + chr(34), "")}</div>{quote(i)}')
    + f'<div class="ctl">{PV}{CNT}{NX}</div></div></div><div class="wrap stillrow">{STILL}</div>')

JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this, r = this.root;
    if (!r) return;
    var st = r.querySelector('.stage'), reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.go(0, 1);
    if (!st) return;
    // keyboard: ← → while focus is in the testimonials
    st.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); self.user(e.key === 'ArrowLeft' ? -1 : 1); }
    });
    // swipe on touch screens (the mouse uses the arrows)
    var x0 = null;
    st.addEventListener('pointerdown', function (e) { x0 = e.pointerType === 'mouse' ? null : e.clientX; });
    st.addEventListener('pointerup', function (e) {
      if (x0 === null) return;
      var dx = e.clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) { self.sw = Date.now(); self.user(dx < 0 ? 1 : -1); }
    });
    st.addEventListener('pointercancel', function () { x0 = null; });
    if (r.hasAttribute('data-auto') && !reduce) {
      r.setAttribute('data-run', '');
      var hold = function (on) { if (on) r.setAttribute('data-hold', ''); else r.removeAttribute('data-hold'); };
      st.addEventListener('pointerenter', function (e) { if (e.pointerType === 'mouse') hold(true); });
      st.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') hold(false); });
      st.addEventListener('focusin', function () { hold(true); });
      st.addEventListener('focusout', function (e) { if (!st.contains(e.relatedTarget)) hold(false); });
      this.onEnd = function (e) { if (e.animationName === 'obtick' && r.hasAttribute('data-run')) self.go((self.a() + 1) % self.n(), 1); };
      r.addEventListener('animationend', this.onEnd);
    }
    if ('IntersectionObserver' in window) {
      this.io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) r.removeAttribute('data-off'); else r.setAttribute('data-off', ''); }, { threshold: 0.3 });
      this.io.observe(st);
    }
    this.live();
  }
  componentWillUnmount() { if (this.io) this.io.disconnect(); if (this.root && this.onEnd) this.root.removeEventListener('animationend', this.onEnd); }
  renderVals() {
    var self = this;
    if (!this.cb) {
      this.a = function () { return parseInt(self.root.getAttribute('data-a'), 10) || 0; };
      this.n = function () { return parseInt(self.root.getAttribute('data-n'), 10); };
      this.live = function () { var s = self.root.querySelector('.sls'); if (s) s.setAttribute('aria-live', self.root.hasAttribute('data-run') ? 'off' : 'polite'); };
      this.go = function (i, d) {
        var r = self.root, cur = self.a(), outs = r.querySelectorAll('.sl[data-out]'), k;
        for (k = 0; k < outs.length; k++) outs[k].removeAttribute('data-out');
        var old = r.querySelector('.sl.s' + cur);
        if (old && cur !== i) old.setAttribute('data-out', '');
        r.setAttribute('data-dir', String(d));
        r.setAttribute('data-a', String(i));
        if (!r.hasAttribute('data-wrap')) {  // clamp: the arrow that leads nowhere says so
          var pv = r.querySelectorAll('.pv'), nx = r.querySelectorAll('.nx');
          for (k = 0; k < pv.length; k++) pv[k].setAttribute('aria-disabled', String(i === 0));
          for (k = 0; k < nx.length; k++) nx[k].setAttribute('aria-disabled', String(i === self.n() - 1));
        }
      };
      // the visitor took control: auto-advance stops for good (W3C APG carousel)
      this.user = function (d) {
        var r = self.root, n = self.n(), a = self.a() + d;
        r.removeAttribute('data-run'); self.live();
        a = r.hasAttribute('data-wrap') ? (a + n) % n : Math.max(0, Math.min(n - 1, a));
        if (a !== self.a()) self.go(a, d);
      };
      this.cb = {
        rootRef: function (el) { self.root = el; },
        step: function (e) { self.user(parseInt(e.currentTarget.getAttribute('data-d'), 10)); },
        pick: function (e) {
          if (Date.now() - (self.sw || 0) < 400) return;
          var i = parseInt(e.currentTarget.getAttribute('data-i'), 10), a = self.a();
          self.root.removeAttribute('data-run'); self.live();
          if (i !== a) self.go(i, i > a ? 1 : -1);
        },
        still: function (e) {
          var r = self.root, on = !r.hasAttribute('data-still');
          if (on) r.setAttribute('data-still', ''); else r.removeAttribute('data-still');
          e.currentTarget.querySelector('.lb').textContent = on ? 'Pornește mișcarea' : 'Oprește mișcarea';
        }
      };
    }
    return this.cb;
  }
}"""


def section(name, attrs, html):
    cls = {"OameniB": "ob", "OameniB2": "ob2", "OameniB3": "ob3", "OameniB4": "ob4"}[name]
    return (f'<section class="og {cls}" id="oameni" aria-labelledby="og-h" data-a="0" data-n="{N}" {attrs} ref="{bind("rootRef")}">'
            f'<div class="wrap"><div class="head"><h2 class="disp" id="og-h">{H}</h2>{LINKS}</div></div>\n{html}\n</section>')


def page(title, css, body, w, h):
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
{BASE_CSS}{COMMON}{SHARED}{css}</style>
</helmet>
<div class="pg">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, attrs, css, html) in OPTS.items():
        body = section(name, attrs, html)
        for suffix, w, h in (("", 1440, 1300), ("Mobil", 390, 1300)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), css, body, w, h))
        subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), os.path.join(P, f"{name}.dc.html"), os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "banda.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Banda</title><style>body{margin:0}iframe{width:1440px;height:1250px;border:0;display:block;border-bottom:8px solid #222}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "banda-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Banda mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0;flex:none}iframe{width:390px;height:1300px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
