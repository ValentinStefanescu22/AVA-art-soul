"""'Cine sunt, pe scurt' (About), round 2: four concepts that leave the photo-left / text-right template.

usage: python3 .aidesigner/about_options2.py
writes .aidesigner/canvas/project/Despre5..8*.dc.html (+ *Mobil twins) and local previews .aidesigner/opt-Despre*.html
Small vs large portrait x light vs dark, as Vali asked. Portrait = clay-toned duotone (public/images/alessia*-duo.webp).
Copy: docs/continut-site.md (Pagina Acasă block 2 + Despre noi role line). No eyebrow above the heading.
"""
import math, os, random, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "canvas", "project")
FONTS = re.search(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2\?[^"]*">',
                  open(os.path.join(P, "Acasa.dc.html"), encoding="utf-8").read()).group(0)

BG = "/_blob/a36432dd59596088ec01e9f25409bd5d"       # hero clay photo
DUO = "/_blob/eea66386c5e507e37343fcb18e98611a"      # alessia.webp, colour cut-out, 1200x1600 (Vali: no colour filter)
DUO_SQ = "/_blob/61696ece195f787b8ccb139b396a6450"   # alessia-stamp.webp, square, face centred

ARROW = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8H13M9 4L13 8L9 12" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
LEAD = "Sunt Alessia și cred că mâinile știu uneori lucruri pe care mintea încă nu le-a spus."
LEAD_EM = "Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus."
BODY = "Creez experiențe în care lutul e doar începutul: restul e despre tine, despre ce simți și despre oamenii cu care împarți masa."
ROLE = "Artist ceramist și consilier acreditat în dezvoltare personală"
LINK = f'<a class="more" href="#povestea">Povestea mea {ARROW}</a>'
ALT = "Alessia Văideanu, fondatoarea AVA Art &amp; Soul"

BASE_CSS = """body{margin:0;background:#F4EDE4}
.pg{--ink:#3A2A20;--ink2:#6B5444;--paper:#F4EDE4;--sand:#E6D5BD;--terra:#B4583A;--terra-d:#9C472C;--clay:#C07A4E;--glowc:#F2C79C;--display:'Bodoni Moda',Georgia,serif;--text:'Literata',Georgia,serif;--script:'Pinyon Script',cursive;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--text);-webkit-font-smoothing:antialiased;overflow-x:clip}
.pg ::selection{background:#B4583A;color:#F4EDE4}
.pg a{color:inherit}
.pg a:focus-visible{outline:2px solid currentColor;outline-offset:4px;border-radius:4px}
.disp{font-family:var(--display);font-weight:400;font-variation-settings:'opsz' 20;letter-spacing:-.012em;text-wrap:balance;margin:0}
.disp em{font-style:italic}
.wrap{position:relative;max-width:1240px;margin:0 auto;padding:0 40px;box-sizing:border-box}
.ar{width:16px;height:16px;flex:none;transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.more{display:inline-flex;align-items:center;gap:10px;min-height:44px;margin-top:18px;font-weight:500;text-decoration:none;text-underline-offset:6px;background:linear-gradient(currentColor,currentColor) 0 calc(100% - 9px)/100% 1px no-repeat;transition:background-size .3s cubic-bezier(.2,.7,.2,1)}
.more:hover{background-size:0 1px;background-position:100% calc(100% - 9px)}
.more:hover .ar{transform:translateX(4px)}
.body{margin:0;text-wrap:pretty;max-width:46ch}
.role{display:block;font:500 15px/1.45 var(--text);letter-spacing:.01em;max-width:34ch}
/* the bottom of the chosen hero, for context (light variants keep its cream wave) */
.heroend{position:relative;height:120px;background:#8A4A30 url(""" + BG + """) center 85%/cover no-repeat}
.heroend::before{content:"";position:absolute;inset:0;background:rgba(42,20,12,.45)}
.heroend svg{position:absolute;left:0;right:0;bottom:-1px;width:100%;height:120px}
/* woodsprite + its warm halo, same recipe as the hero */
.glow{position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(circle var(--lr,340px) at var(--lx,70%) var(--ly,40%),rgba(255,206,150,.30) 0%,rgba(255,180,110,.10) 40%,rgba(255,170,100,0) 70%);mix-blend-mode:screen}
.sprite{position:absolute;left:0;top:0;z-index:4;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border-radius:50%;pointer-events:none;background:radial-gradient(circle,#FFFDF6 0 35%,rgba(255,246,228,.9) 52%,rgba(255,236,206,0) 74%);box-shadow:0 0 16px 6px rgba(255,250,238,.85),0 0 60px 26px rgba(255,236,206,.4);will-change:transform}
@media (max-width:820px){.wrap{padding:0 20px}.heroend{height:72px}.heroend svg{height:72px}}
@media (prefers-reduced-motion:reduce){.sprite{display:none}.pg *{transition:none!important}}
"""


def hero_end(fill):
    return ('<div class="heroend" aria-hidden="true"><svg viewBox="0 0 1440 120" preserveAspectRatio="none">'
            f'<path d="M0 86C240 62 480 62 720 86C960 110 1200 110 1440 86L1440 120L0 120Z" style="fill:{fill}"></path></svg></div>')


# ---------- procedural fingerprint (Amprenta) ----------
def fingerprint(seed=11, rings=30, size=800):
    rnd = random.Random(seed)
    cx = cy = size / 2
    ph = [rnd.uniform(0, 2 * math.pi) for _ in range(5)]
    out = []
    for i in range(rings):
        r = 70 + i * 10.4
        k = i / rings                          # distortion grows outward, so rings drift apart like real ridges
        outer = i >= 19                        # outer ridges open into arches at the base
        t0, t1 = (math.pi - .7 + (i - 19) * .04, 2 * math.pi + .7 - (i - 19) * .04) if outer else (0, 2 * math.pi)
        gaps = [rnd.uniform(t0, t1) for _ in range(rnd.choice([0, 1, 1, 2, 3]))]
        seg, segs, n = [], [], 170
        for s in range(n + 1):
            t = t0 + (t1 - t0) * s / n
            if any(abs(t - g) < .045 + .03 * rnd.random() for g in gaps):
                if len(seg) > 2: segs.append(seg)
                seg = []; continue
            w = (1 + (.03 + .07 * k) * math.sin(2 * t + ph[0] + i * .11) + (.02 + .04 * k) * math.sin(3 * t + ph[1] + i * .07)
                 + .015 * math.sin(5 * t + ph[2] + i * .2) + .006 * math.sin(9 * t + ph[3]))
            x = cx + r * w * math.cos(t) + 18 * k * math.sin(t + ph[4])
            y = cy - i * 3.1 + r * 1.24 * w * math.sin(t)
            if outer and math.sin(t) > 0:      # arches flare outward and flatten at the base, like the delta of a print
                x += (x - cx) * .18 * math.sin(t); y -= (y - cy) * .25 * math.sin(t)
            seg.append(f"{x:.1f} {y:.1f}")
        if len(seg) > 2: segs.append(seg)
        d = "".join("M" + "L".join(sg) for sg in segs)
        cls = "rg k" if i % 6 == 3 else "rg"   # every sixth ridge in terracotta, the brand's two-dark-one-terracotta rhythm
        out.append(f'<path class="{cls}" d="{d}"></path>')
    return f'<svg class="fp" viewBox="0 0 {size} {size}" aria-hidden="true">{"".join(out)}</svg>'


OPTS = {}

# 5. Scrisoarea: dark, small portrait. The hero's clay keeps going; the sentence is the hero of the section,
#    signed like a letter with a portrait pressed into the clay like a seal.
OPTS["Despre5Scrisoare"] = ("Despre 5: scrisoarea (închis, portret mic)", True, """
.dk{position:relative;background:#24150E;color:#F4EDE4;overflow:hidden;isolation:isolate}
.dk::before{content:"";position:absolute;inset:0;z-index:-2;background:url(""" + BG + """) center 78%/cover no-repeat}
.dk::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(42,20,12,.45) 0,rgba(36,20,13,.84) 280px,rgba(28,16,10,.93) 100%)}
.dk .spacer{height:120px}
.letter{position:relative;z-index:2;padding-top:72px;padding-bottom:120px}
.big{font-size:clamp(36px,5.3vw,78px);line-height:1.08;max-width:21ch;color:#F4EDE4}
.big em{color:var(--glowc)}
.sign{display:grid;grid-template-columns:auto minmax(0,.9fr) minmax(0,1.1fr);gap:28px 56px;align-items:center;margin-top:84px;padding-top:44px;border-top:1px solid rgba(244,237,228,.16)}
.coin{width:120px;height:120px;margin:0;border-radius:50%;padding:7px;box-sizing:border-box;background:#1C100A;box-shadow:inset 3px 4px 8px rgba(0,0,0,.65),inset -2px -2px 1px rgba(255,214,170,.16),0 1px 0 rgba(255,214,170,.08)}
.coin img{display:block;width:100%;height:100%;border-radius:50%;object-fit:cover;box-shadow:0 0 0 1px rgba(255,214,170,.18)}
.who .n{display:block;font:400 58px/1 var(--script);color:var(--glowc);margin-bottom:10px}
.who .role{color:#D7C3A9;max-width:30ch}
.txt .body{color:#E6D7C4}
.txt .more{color:var(--glowc)}
@media (max-width:820px){.dk .spacer{height:72px}.letter{padding-top:48px;padding-bottom:84px}.big{font-size:clamp(32px,9vw,44px);line-height:1.12}.sign{grid-template-columns:auto 1fr;gap:20px 20px;margin-top:52px;padding-top:32px}.coin{width:92px;height:92px;padding:5px}.who .n{font-size:46px}.txt{grid-column:1/-1}}
""", f"""<div class="dk" ref="{{{{ secRef }}}}" onPointerMove="{{{{ onMove }}}}" onPointerLeave="{{{{ onLeave }}}}">
<div class="glow" aria-hidden="true"></div>
<span class="sprite" aria-hidden="true" ref="{{{{ spriteRef }}}}"></span>
<div class="spacer" aria-hidden="true"></div>
<section class="wrap letter" id="despre" aria-labelledby="despre-h">
<h2 class="disp big" id="despre-h">{LEAD_EM}</h2>
<div class="sign">
<figure class="coin" ref="{{{{ anchorRef }}}}" data-ax=".5" data-ay=".5" data-wr="1.6"><img src="{DUO_SQ}" alt="{ALT}"></figure>
<div class="who"><span class="n" aria-hidden="true">Alessia</span><span class="role">{ROLE}</span></div>
<div class="txt"><p class="body">{BODY}</p>{LINK}</div>
</div>
</section>
</div>""")

# 6. Coperta: light, large portrait. A magazine cover: her name set huge in terracotta, the portrait in front of it.
OPTS["Despre6Coperta"] = ("Despre 6: coperta (deschis, portret mare)", False, """
.cv{position:relative;overflow:hidden;background:radial-gradient(ellipse 55% 60% at 50% 38%,#F6EEE3 0%,rgba(246,238,227,0) 70%),linear-gradient(180deg,#EFE4D4 0%,#E8D9C3 58%,#E2CDB0 100%)}
.cv .name{position:absolute;left:50%;top:34px;z-index:0;transform:translateX(-50%);margin:0;font:400 clamp(112px,23vw,340px)/.82 var(--display);font-variation-settings:'opsz' 96;letter-spacing:-.04em;color:var(--terra);white-space:nowrap;pointer-events:none;user-select:none}
.cv .stage{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,540px) minmax(0,1fr);gap:0 48px;min-height:860px;align-items:end}
.cv .fig{grid-column:2;grid-row:1;margin:0;align-self:end;aspect-ratio:3/4;width:100%;-webkit-mask-image:linear-gradient(180deg,#000 74%,transparent 99%);mask-image:linear-gradient(180deg,#000 74%,transparent 99%)}
.cv .fig img{display:block;width:100%;height:100%;object-fit:contain;object-position:50% 100%}
.cv .l{grid-column:1;grid-row:1;align-self:center;padding-top:200px}
.cv .l h2{font-size:clamp(26px,2.5vw,36px);line-height:1.2;max-width:15ch}
.cv .r{grid-column:3;grid-row:1;align-self:end;padding-bottom:132px}
.cv .r .role{color:#833A22;margin-bottom:14px}
.cv .r .body{color:#5E4838}
.cv .r .more{color:var(--ink)}
@media (max-width:980px){.cv .stage{grid-template-columns:1fr;min-height:0;padding-top:12px}.cv .name{top:20px;font-size:27vw}.cv .fig{grid-column:1;grid-row:1;width:min(100%,420px);justify-self:center;margin-top:9vw;-webkit-mask-image:linear-gradient(180deg,#000 70%,transparent 98%);mask-image:linear-gradient(180deg,#000 70%,transparent 98%)}.cv .l,.cv .r{grid-column:1;padding:0}.cv .l{grid-row:2;margin-top:-56px}.cv .l h2{font-size:clamp(28px,7.6vw,36px);max-width:18ch}.cv .r{grid-row:3;padding:20px 0 72px}}
""", f"""<section class="cv" id="despre" aria-labelledby="despre-h">
<p class="name" aria-hidden="true">Alessia</p>
<div class="wrap stage">
<figure class="fig"><img src="{DUO}" alt="{ALT}"></figure>
<div class="l"><h2 class="disp" id="despre-h">{LEAD}</h2></div>
<div class="r"><span class="role">{ROLE}</span><p class="body">{BODY}</p>{LINK}</div>
</div>
</section>""")

# 7. Amprenta: light, small portrait. Hands know things: a fingerprint drawn in the brand's ridges, Alessia at its core.
OPTS["Despre7Amprenta"] = ("Despre 7: amprenta (deschis, portret mic)", False, """
.am{position:relative;overflow:hidden;background:radial-gradient(ellipse 50% 70% at 70% 50%,#F8F2EA 0%,rgba(248,242,234,0) 70%),var(--paper)}
.am .print{position:absolute;top:50%;left:calc(50% - 20px);width:820px;aspect-ratio:1;transform:translateY(-50%);margin:0}
.am .fp{position:absolute;inset:0;width:100%;height:100%}
.am .rg{fill:none;stroke:var(--clay);opacity:.5;stroke-linecap:round;stroke-width:1.4px;vector-effect:non-scaling-stroke}
.am .rg.k{stroke:var(--terra);opacity:.85;stroke-width:1.7px}
.am .core{position:absolute;left:50%;top:50%;width:168px;height:168px;margin:-84px 0 0 -84px;border-radius:50%;padding:10px;box-sizing:border-box;background:var(--paper);box-shadow:0 0 0 1px rgba(156,71,44,.35),0 24px 40px -24px rgba(58,42,32,.5)}
.am .core img{display:block;width:100%;height:100%;border-radius:50%;object-fit:cover}
.am .txt{position:relative;z-index:1;max-width:540px;padding:150px 0 170px}
.am h2{font-size:clamp(32px,3.7vw,54px);line-height:1.14}
.am h2 em{color:var(--terra-d)}
.am .body{margin-top:28px;color:var(--ink2)}
.am .role{margin-top:30px;color:var(--terra-d)}
@media (max-width:980px){.am{background:var(--paper)}.am .print{position:relative;top:auto;left:50%;width:min(132vw,620px);transform:translateX(-50%);margin:-12vw 0 -14vw}.am .core{width:118px;height:118px;margin:-59px 0 0 -59px;padding:7px}.am .txt{max-width:none;padding:0 0 80px}.am h2{font-size:clamp(30px,8.4vw,40px)}}
""", f"""<section class="am" id="despre" aria-labelledby="despre-h">
<div class="wrap">
<figure class="print">{fingerprint()}<span class="core"><img src="{DUO_SQ}" alt="{ALT}"></span></figure>
<div class="txt"><h2 class="disp" id="despre-h">{LEAD_EM}</h2><p class="body">{BODY}</p><span class="role">{ROLE}</span>{LINK}</div>
</div>
</section>""")

# 8. Lumina: dark, large portrait. Alessia stands in a dim atelier; the woodsprite is the lamp that lights her face.
OPTS["Despre8Lumina"] = ("Despre 8: lumina (închis, portret mare)", True, """
.lm{position:relative;background:#1D100A;color:#F4EDE4;overflow:hidden;isolation:isolate}
.lm::before{content:"";position:absolute;inset:0;z-index:-2;background:url(""" + BG + """) center 78%/cover no-repeat}
.lm::after{content:"";position:absolute;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(42,20,12,.45) 0,rgba(30,16,10,.9) 260px,rgba(26,14,9,.96) 100%)}
.lm .spacer{height:120px}
.lm .stage{position:relative;z-index:2;min-height:820px}
.lm .fig{position:absolute;right:-10px;bottom:0;width:600px;aspect-ratio:3/4;margin:0}
.lm .fig img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:50% 100%}
.lm .fig .base{filter:brightness(.38) saturate(.75);-webkit-mask-image:linear-gradient(180deg,#000 66%,transparent 98%);mask-image:linear-gradient(180deg,#000 66%,transparent 98%)}
.lm .fig .lit{-webkit-mask-image:radial-gradient(circle var(--fr,300px) at var(--fx,60%) var(--fy,34%),#000 0%,rgba(0,0,0,.6) 38%,transparent 72%);mask-image:radial-gradient(circle var(--fr,300px) at var(--fx,60%) var(--fy,34%),#000 0%,rgba(0,0,0,.6) 38%,transparent 72%)}
.lm .txt{position:relative;z-index:3;max-width:620px;padding:96px 0 140px}
.lm h2{font-size:clamp(34px,4.5vw,66px);line-height:1.1}
.lm h2 em{color:var(--glowc)}
.lm .body{margin-top:30px;color:#E6D7C4}
.lm .role{margin-top:30px;color:#D7C3A9}
.lm .more{color:var(--glowc)}
@media (max-width:980px){.lm .spacer{height:72px}.lm .stage{min-height:0}.lm .fig{position:relative;right:auto;width:min(100%,440px);margin:0 auto}.lm .txt{max-width:none;margin-top:-90px;padding:0 0 80px}.lm h2{font-size:clamp(30px,8.6vw,42px)}}
""", f"""<div class="lm" ref="{{{{ secRef }}}}" onPointerMove="{{{{ onMove }}}}" onPointerLeave="{{{{ onLeave }}}}">
<div class="glow" aria-hidden="true"></div>
<span class="sprite" aria-hidden="true" ref="{{{{ spriteRef }}}}"></span>
<div class="spacer" aria-hidden="true"></div>
<section class="wrap stage" id="despre" aria-labelledby="despre-h">
<figure class="fig" ref="{{{{ anchorRef }}}}" data-ax=".58" data-ay=".32" data-wr=".28"><img class="base" src="{DUO}" alt="{ALT}"><img class="lit" src="{DUO}" alt=""></figure>
<div class="txt"><h2 class="disp" id="despre-h">{LEAD_EM}</h2><p class="body">{BODY}</p><span class="role">{ROLE}</span>{LINK}</div>
</section>
</div>""")

# Woodsprite logic for the dark variants: critically damped spring toward the cursor; on touch / idle it drifts
# around an anchor (data-ax/ay = point inside the anchor element, data-wr = drift radius in anchor widths).
LIGHT_JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this;
    var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
    var W = 2 * Math.PI / 0.5, P = { x: 0, y: 0, vx: 0, vy: 0 }, started = false, t0 = performance.now(), last = t0;
    var tick = function (now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      var r = self.sec && self.sec.getBoundingClientRect(), a = self.anchor;
      if (r && a && r.bottom > 0) {
        var f = a.getBoundingClientRect(), T = self.T, s = (now - t0) / 1000;
        var ax = f.left - r.left + f.width * +a.dataset.ax, ay = f.top - r.top + f.height * +a.dataset.ay, wr = f.width * +a.dataset.wr;
        if (!T.on) { T.x = ax + Math.cos(-2.2 + s * 0.23) * wr; T.y = ay + Math.sin(-2.2 + s * 0.31) * (a.dataset.wy ? f.height * +a.dataset.wy : wr * 0.6); }
        if (!started) { P.x = T.x; P.y = T.y; started = true; }
        P.vx += (W * W * (T.x - P.x) - 2 * W * P.vx) * dt; P.x += P.vx * dt;
        P.vy += (W * W * (T.y - P.y) - 2 * W * P.vy) * dt; P.y += P.vy * dt;
        if (self.sprite) self.sprite.style.transform = 'translate3d(' + P.x.toFixed(1) + 'px,' + P.y.toFixed(1) + 'px,0)';
        self.sec.style.setProperty('--lx', P.x.toFixed(1) + 'px'); self.sec.style.setProperty('--ly', P.y.toFixed(1) + 'px');
        a.style.setProperty('--fx', (P.x - (f.left - r.left)).toFixed(1) + 'px'); a.style.setProperty('--fy', (P.y - (f.top - r.top)).toFixed(1) + 'px');
        a.style.setProperty('--fr', Math.max(200, f.width * 0.55).toFixed(0) + 'px');
      }
      if (!reduce) self.raf = requestAnimationFrame(tick);
    };
    this.raf = requestAnimationFrame(tick);
  }
  componentWillUnmount() { cancelAnimationFrame(this.raf); }
  renderVals() {
    var self = this;
    if (!this.cb) {
      this.T = { x: 0, y: 0, on: false };
      this.cb = {
        secRef: function (el) { self.sec = el; },
        spriteRef: function (el) { self.sprite = el; },
        anchorRef: function (el) { self.anchor = el; },
        onMove: function (e) {
          if (!self.sec) return;
          var r = self.sec.getBoundingClientRect();
          self.T.x = e.clientX - r.left; self.T.y = e.clientY - r.top; self.T.on = e.pointerType === 'mouse';
        },
        onLeave: function () { self.T.on = false; }
      };
    }
    return this.cb;
  }
}"""
STATIC_JS = "class Component extends DCLogic {\n  renderVals() { return {}; }\n}"


def page(title, dark, css, html, w, h):
    end = "" if dark else hero_end("#EFE4D4" if "cv" in html[:40] else "#F4EDE4")
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
{BASE_CSS}{css}</style>
</helmet>
<div class="pg">
{end}{html}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{LIGHT_JS if dark else STATIC_JS}
</script>
</body>
</html>
"""


if __name__ == "__main__":
  for name, (title, dark, css, html) in OPTS.items():
      for suffix, w, h in (("", 1440, 960), ("Mobil", 390, 1100)):
          f = os.path.join(P, f"{name}{suffix}.dc.html")
          open(f, "w", encoding="utf-8").write(page(title + (" · mobil" if suffix else ""), dark, css, html, w, h))
          if not suffix:
              subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
