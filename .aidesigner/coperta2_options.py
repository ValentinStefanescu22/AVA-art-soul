"""'Cine sunt' / Coperta, round 3: same cover (the huge 'Alessia'), but alive. Vali: 'prea statice'.
Each variant is modelled on a real reference (see SOURCES); the woodsprite light from the hero drives E and F.

usage: python3 .aidesigner/coperta2_options.py
writes .aidesigner/canvas/project/CopertaE..H*.dc.html (+ Mobil twins) and local previews .aidesigner/opt-Coperta*.html
"""
import os, subprocess, sys
from about_options2 import P, HERE, FONTS, BASE_CSS, LIGHT_JS, BG, DUO, ALT, LEAD, BODY, ROLE, LINK, hero_end
from coperta_options import COVER

ATELIER = "/_blob/af69ff19bcdcf8c0410f4609e748d3a2"   # the real October workshop photo (colour crop)
LUT_PH = "/_blob/27d62de5381eeee8e9ab504567023c22"     # placeholder: hands shaping a bowl (Unsplash)
SOURCES = {
    "CopertaE": ("Awwwards: Interactive Text Mask; Mask cursor", "https://www.awwwards.com/inspiration/interactive-text-mask"),
    "CopertaF": ("Awwwards: Rollover name reveal; Bruno Tomé, decorative typography hover", "https://www.awwwards.com/inspiration/rollover-name-reveal"),
    "CopertaG": ("Framer: Scroll Text Fill; Webflow: Text color fills in while scrolling", "https://webflow.com/made-in-webflow/website/text-color-fills-in-while-scrolling"),
    "CopertaH": ("Awwwards: Mask changes shape when hover", "https://www.awwwards.com/inspiration/mask-changes-shape-when-hover"),
}
WARM = """.cv .sprite{background:radial-gradient(circle,#FFFBF2 0 34%,rgba(255,236,206,.95) 52%,rgba(255,214,160,0) 74%);box-shadow:0 0 14px 5px rgba(255,226,186,.95),0 0 46px 18px rgba(214,140,80,.35)}
.cv{isolation:isolate}
"""
OPTS = {}

# E. Lentila: the letters of her name are cut out of the clay; the woodsprite is a lens that shows the real
#    workshop behind them. Desktop: it follows the cursor. Phone: it drifts on its own.
OPTS["CopertaE"] = ("Coperta E: numele ca fereastră spre atelier", """
.e .nm{position:absolute;left:0;right:0;top:30px;height:clamp(120px,22vw,320px);z-index:0}
.e .nm .name{position:absolute;inset:0;top:0;left:0;transform:none;display:flex;align-items:center;justify-content:center;background:url(""" + BG + """) center 60%/cover no-repeat;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.e .lens{position:absolute;inset:0;background:url(""" + ATELIER + """) center 42%/cover no-repeat;-webkit-mask-image:radial-gradient(circle 210px at var(--fx,50%) var(--fy,50%),#000 0%,rgba(0,0,0,.9) 50%,transparent 74%);mask-image:radial-gradient(circle 210px at var(--fx,50%) var(--fy,50%),#000 0%,rgba(0,0,0,.85) 45%,transparent 72%)}
.e .stage{display:flex;flex-direction:column;position:relative;z-index:2}
.e .fig{width:500px;align-self:center;margin-top:150px}
.e .band{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:72px;align-items:end;padding:52px 0 120px;border-top:1px solid rgba(58,42,32,.2)}
.e h2{font-size:clamp(32px,3.6vw,52px);line-height:1.12;max-width:20ch}
.e .role{margin-bottom:12px}
@media (max-width:980px){.e .nm{top:20px;height:28vw}.e .nm .name{font-size:27vw}.e .lens{-webkit-mask-image:radial-gradient(circle 90px at var(--fx,50%) var(--fy,50%),#000 0%,rgba(0,0,0,.85) 45%,transparent 72%);mask-image:radial-gradient(circle 90px at var(--fx,50%) var(--fy,50%),#000 0%,rgba(0,0,0,.9) 50%,transparent 74%)}.e .fig{width:min(100%,420px);margin-top:9vw}.e .band{grid-template-columns:1fr;gap:22px;padding:30px 0 76px}.e h2{font-size:clamp(28px,7.6vw,36px)}}
""", """<div class="nm" aria-hidden="true" ref="{{ anchorRef }}" data-ax=".5" data-ay=".52" data-wr=".32" data-wy=".16"><p class="name">Alessia</p><div class="lens"></div></div>
<div class="wrap stage">
<figure class="fig fade"><img src="%(DUO)s" alt="%(ALT)s"></figure>
<div class="band"><h2 class="disp" id="despre-h">Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus.</h2>
<div><span class="role">%(ROLE)s</span><p class="body">%(BODY)s</p>%(LINK)s</div></div>
</div>""", "light")

# F. Lumina umple literele: the name is drawn as an outline, like a sketch in wet clay; where the woodsprite
#    passes, the letters fill with terracotta. Asymmetric cover (D), which you liked for the text.
OPTS["CopertaF"] = ("Coperta F: lumina umple literele", """
.f .nm{position:absolute;top:30px;left:max(36px,calc(50% - 584px));z-index:0}
.f .nm .name{position:relative;left:0;top:0;transform:none;display:block}
.f .nm .o{color:transparent;-webkit-text-stroke:1.4px #B4583A}
.f .nm .fl{position:absolute;inset:0;-webkit-mask-image:radial-gradient(circle 280px at var(--fx,40%) var(--fy,50%),#000 38%,rgba(0,0,0,.7) 58%,transparent 80%);mask-image:radial-gradient(circle 280px at var(--fx,40%) var(--fy,50%),#000 38%,rgba(0,0,0,.7) 58%,transparent 80%)}
.f .stage{display:grid;grid-template-columns:minmax(0,1fr) 500px;gap:0 64px;min-height:850px;position:relative;z-index:2}
.f .fig{grid-column:2;grid-row:1;align-self:end}
.f .l{grid-column:1;grid-row:1;align-self:end;padding:0 0 128px}
.f h2{font-size:clamp(32px,3.5vw,50px);line-height:1.12;max-width:19ch}
.f .row{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:40px;align-items:end;margin-top:36px;padding-top:28px;border-top:1px solid rgba(58,42,32,.2)}
@media (max-width:980px){.f .nm{left:16px;top:20px}.f .nm .name{font-size:27vw}.f .nm .fl{-webkit-mask-image:radial-gradient(circle 120px at var(--fx,40%) var(--fy,50%),#000 25%,rgba(0,0,0,.6) 50%,transparent 76%);mask-image:radial-gradient(circle 120px at var(--fx,40%) var(--fy,50%),#000 25%,rgba(0,0,0,.6) 50%,transparent 76%)}.f .stage{grid-template-columns:1fr;min-height:0}.f .fig{grid-column:1;grid-row:1;width:min(88%,400px);margin:12vw 0 0 auto}.f .l{grid-row:2;margin-top:-16px;padding-bottom:76px}.f h2{font-size:clamp(28px,7.6vw,36px)}.f .row{grid-template-columns:1fr;gap:16px}}
""", """<div class="nm" aria-hidden="true" ref="{{ anchorRef }}" data-ax=".5" data-ay=".5" data-wr=".36" data-wy=".14"><p class="name o">Alessia</p><p class="name fl">Alessia</p></div>
<div class="wrap stage">
<figure class="fig fade"><img src="%(DUO)s" alt="%(ALT)s"></figure>
<div class="l"><h2 class="disp" id="despre-h">Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus.</h2>
<div class="row"><p class="body">%(BODY)s</p><div><span class="role">%(ROLE)s</span>%(LINK)s</div></div></div>
</div>""", "light")


# G. Rândurile se umplu: her two sentences, set large, fill in word by word as you scroll, like clay darkening as it dries.
def words(text, start, em=()):
    out, i = [], start
    for w in text.split(" "):
        cls = ' class="em"' if w.strip(".,:") in em else ""
        out.append(f'<span{cls} style="--w:{i}">{w}</span>')
        i += 1
    return " ".join(out), i


_h, _n = words(LEAD, 0, em=("mâinile", "știu"))
_b, _n = words(BODY, _n)
N_WORDS = _n
OPTS["CopertaG"] = ("Coperta G: rândurile se umplu la scroll", """
.g .stage{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:0 56px;position:relative;z-index:2}
.g .fig{grid-column:2;grid-row:1/3;align-self:start;margin-top:130px;width:100%}
.g .fill{grid-column:1;grid-row:1;padding-top:300px;--n:""" + str(N_WORDS) + """}
.g .fill span{color:color-mix(in srgb,var(--ink) calc(clamp(0, (var(--p,1) * (var(--n) + 6) - var(--w)) / 6, 1) * 100%),#D2BEA4);transition:color .2s linear}
.g .fill .em{font-style:italic;color:color-mix(in srgb,#9C472C calc(clamp(0, (var(--p,1) * (var(--n) + 6) - var(--w)) / 6, 1) * 100%),#D9B9A0)}
.g h2{font-size:clamp(34px,3.6vw,52px);line-height:1.14}
.g .big{margin:18px 0 0;font:400 clamp(26px,2.5vw,36px)/1.28 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:pretty}
.g .meta{grid-column:1;grid-row:2;padding:34px 0 120px;display:flex;gap:40px;align-items:center;border-top:1px solid rgba(58,42,32,.2);margin-top:36px}
@media (max-width:980px){.g .stage{grid-template-columns:1fr}.g .fig{grid-column:1;grid-row:1;width:min(100%,420px);margin:9vw auto 0}.g .fill{grid-row:2;padding-top:20px}.g .meta{grid-row:3;flex-direction:column;align-items:flex-start;gap:6px;padding-bottom:76px}.g h2{font-size:clamp(30px,8vw,38px)}.g .big{font-size:clamp(23px,6.2vw,28px)}}
@media (prefers-reduced-motion:reduce){.g .fill{--p:1!important}}
""", """<div class="wrap stage">
<figure class="fig fade"><img src="%(DUO)s" alt="%(ALT)s"></figure>
<div class="fill" ref="{{ fillRef }}"><h2 class="disp" id="despre-h">""" + _h + """</h2><p class="big">""" + _b + """</p></div>
<div class="meta"><span class="role">%(ROLE)s</span>%(LINK)s</div>
</div>""", "scroll")

# H. Două roluri: under the name, her two crafts as two big words either side of the portrait.
#    Vali (10 nov): keep the same cut-out portrait as Despre 6, no swap on hover; pointing at a role only underlines it.
ROLES = [("Artist ceramist", "Lucrez cu lutul de peste trei ani, cu cursuri de specializare la Brașov.", LUT_PH,
          "Mâini care modelează un bol de lut (fotografie provizorie)"),
         ("Consilier acreditat", "Consilier în dezvoltare personală (Sandonia Institute), cu licență în Psihologie.", DUO, ALT)]
OPTS["CopertaH"] = ("Coperta H: două roluri", """
.h .stage{position:relative;z-index:2;display:grid;grid-template-columns:minmax(0,1fr) 500px minmax(0,1fr);gap:0 56px;align-items:center;padding-top:120px}
.h .fig{grid-column:2;grid-row:1;width:100%;margin:0;aspect-ratio:3/4;-webkit-mask-image:linear-gradient(180deg,#000 52%,transparent 92%),linear-gradient(90deg,transparent 0,#000 9%,#000 91%,transparent 100%);-webkit-mask-composite:source-in;mask-image:linear-gradient(180deg,#000 52%,transparent 92%),linear-gradient(90deg,transparent 0,#000 9%,#000 91%,transparent 100%);mask-composite:intersect}
.h .fig img{display:block;width:100%;height:100%;object-fit:contain;object-position:50% 100%}
.h .rb{appearance:none;border:0;background:none;padding:12px 0;cursor:pointer;text-align:inherit;color:#8C705D;font:inherit;display:flex;flex-direction:column;gap:12px;min-height:44px}
.h .rb .w{font:400 italic clamp(34px,3.4vw,50px)/1.05 var(--display);font-variation-settings:'opsz' 20;letter-spacing:-.015em;transition:color .3s}
.h .rb .d{font-size:15.5px;line-height:1.5;color:#7A6152;max-width:30ch;transition:color .3s}
.h .rb.a{grid-column:1;grid-row:1;justify-self:end;text-align:right;align-items:flex-end}
.h .rb.b{grid-column:3;grid-row:1;justify-self:start;text-align:left}
.h[data-r="0"] .rb.a .w,.h[data-r="1"] .rb.b .w{color:#9C472C}
.h[data-r="0"] .rb.a .d,.h[data-r="1"] .rb.b .d{color:#5E4838}
.h .rb .w::after{content:"";display:block;height:1px;margin-top:10px;background:currentColor;transform:scaleX(0);transition:transform .45s cubic-bezier(.2,.7,.2,1)}
.h .rb.a .w::after{transform-origin:right}.h .rb.b .w::after{transform-origin:left}
.h[data-r="0"] .rb.a .w::after,.h[data-r="1"] .rb.b .w::after{transform:none}
.h .rb:focus-visible{outline:2px solid #9C472C;outline-offset:6px;border-radius:6px}
.h .cap{display:flex;flex-direction:column;align-items:center;text-align:center;margin-top:8px;padding:0 0 120px;position:relative;z-index:2}
.h .cap h2{font-size:clamp(30px,3.2vw,46px);line-height:1.14;max-width:24ch}
.h .cap .body{margin-top:22px;max-width:48ch}
@media (max-width:980px){.h .stage{grid-template-columns:1fr 1fr;gap:0 16px;padding-top:9vw}.h .fig{grid-column:1/-1;width:min(100%,400px);justify-self:center}.h .rb.a,.h .rb.b{grid-row:2;align-self:start;justify-self:stretch;text-align:left;align-items:flex-start;padding-top:22px}.h .rb.a{grid-column:1}.h .rb.b{grid-column:2}.h .rb .w{font-size:26px}.h .rb .d{font-size:14px}.h .cap{margin-top:0;padding:36px 0 76px}.h .cap h2{font-size:clamp(26px,7vw,34px)}}
""", """<div class="wrap stage">
<button class="rb a" type="button" data-i="0" aria-pressed="true" onMouseEnter="{{ pick }}" onFocus="{{ pick }}" onClick="{{ pick }}"><span class="w">%(R0)s</span><span class="d">%(D0)s</span></button>
<figure class="fig"><img src="%(DUO)s" alt="%(ALT)s"></figure>
<button class="rb b" type="button" data-i="1" aria-pressed="false" onMouseEnter="{{ pick }}" onFocus="{{ pick }}" onClick="{{ pick }}"><span class="w">%(R1)s</span><span class="d">%(D1)s</span></button>
</div>
<div class="wrap cap"><h2 class="disp" id="despre-h">Sunt Alessia și cred că <em>mâinile știu</em> uneori lucruri pe care mintea încă nu le-a spus.</h2><p class="body">%(BODY)s</p>%(LINK)s</div>""", "roles")

SCROLL_JS = """class Component extends DCLogic {
  componentDidMount() {
    var self = this;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.upd = function () {
      if (!self.fill) return;
      if (reduce) { self.fill.style.setProperty('--p', '1'); return; }
      var r = self.fill.getBoundingClientRect(), vh = window.innerHeight || 800;
      var p = (vh * 0.9 - r.top) / (r.height + vh * 0.45);
      self.fill.style.setProperty('--p', Math.max(0, Math.min(1, p)).toFixed(3));
    };
    this.upd();
    window.addEventListener('scroll', this.upd, { passive: true });
    window.addEventListener('resize', this.upd);
  }
  componentWillUnmount() { window.removeEventListener('scroll', this.upd); window.removeEventListener('resize', this.upd); }
  renderVals() {
    var self = this;
    if (!this.cb) this.cb = { fillRef: function (el) { self.fill = el; } };
    return this.cb;
  }
}"""
ROLES_JS = """class Component extends DCLogic {
  renderVals() {
    var self = this;
    if (!this.cb) this.cb = {
      secRef: function (el) { self.sec = el; },
      pick: function (e) {
        if (!self.sec) return;
        var i = e.currentTarget.getAttribute('data-i');
        self.sec.setAttribute('data-r', i);
        var bs = self.sec.querySelectorAll('.rb');
        for (var k = 0; k < bs.length; k++) bs[k].setAttribute('aria-pressed', bs[k].getAttribute('data-i') === i ? 'true' : 'false');
      }
    };
    return this.cb;
  }
}"""
JS = {"light": LIGHT_JS, "scroll": SCROLL_JS, "roles": ROLES_JS}
FILL = dict(DUO=DUO, ALT=ALT, ROLE=ROLE, BODY=BODY, LINK=LINK, R0=ROLES[0][0], D0=ROLES[0][1], I0=ROLES[0][2], A0=ROLES[0][3],
            R1=ROLES[1][0], D1=ROLES[1][1], I1=ROLES[1][2], A1=ROLES[1][3])


def page(name, title, css, inner, kind, w, h):
    cls = name[-1].lower()
    attrs = {"light": ' ref="{{ secRef }}" onPointerMove="{{ onMove }}" onPointerLeave="{{ onLeave }}"',
             "roles": ' data-r="0" ref="{{ secRef }}"', "scroll": ""}[kind]
    sprite = '<span class="sprite" aria-hidden="true" ref="{{ spriteRef }}"></span>\n' if kind == "light" else ""
    name_p = "" if kind == "light" else '<p class="name" aria-hidden="true">Alessia</p>\n'
    body = (f'<section class="cv {cls}" id="despre" aria-labelledby="despre-h"{attrs}>\n{sprite}{name_p}{inner % FILL}\n</section>')
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
{BASE_CSS}{COVER}{WARM}{css}</style>
</helmet>
<div class="pg">
{hero_end("#EFE4D4")}{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
{JS[kind]}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    for name, (title, css, inner, kind) in OPTS.items():
        for suffix, w, h in (("", 1440, 1100), ("Mobil", 390, 1100)):
            f = os.path.join(P, f"{name}{suffix}.dc.html")
            open(f, "w", encoding="utf-8").write(page(name, title + (" · mobil" if suffix else ""), css, inner, kind, w, h))
            if not suffix:
                subprocess.run([sys.executable, os.path.join(HERE, "dc2html.py"), f, os.path.join(HERE, f"opt-{name}.html")], check=True)
    names = list(OPTS)
    open(os.path.join(HERE, "coperta2.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Coperta 2</title><style>body{margin:0}iframe{width:1440px;height:1500px;border:0;display:block}</style>' + "".join(f'<iframe src="opt-{n}.html"></iframe>' for n in names))
    open(os.path.join(HERE, "coperta2-mobil.html"), "w").write('<!doctype html><meta charset="utf-8"><title>Coperta 2 mobil</title><style>body{margin:0;padding:10px;background:#1b1b1b;display:flex;gap:12px;color:#ddd;font:13px system-ui}figure{margin:0}iframe{width:390px;height:1400px;border:0;display:block}</style>' + "".join(f'<figure><figcaption>{n}</figcaption><iframe src="opt-{n}.html"></iframe></figure>' for n in names))
