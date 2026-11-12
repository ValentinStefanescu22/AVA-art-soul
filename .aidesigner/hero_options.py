"""Generate the header and hero-text option artboards from the shared hero in Acasa.dc.html.

usage: python3 .aidesigner/hero_options.py   (writes .aidesigner/canvas/project/Header*.dc.html, Text*.dc.html)
Each artboard = the real hero (clay photo, engraved stamp, light) + one variant of the header or of the right-hand copy.
"""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "canvas", "project")
src = open(os.path.join(P, "Acasa.dc.html"), encoding="utf-8").read()


def between(a, b, incl_b=False):
    i = src.index(a)
    j = src.index(b, i) + (len(b) if incl_b else 0)
    return src[i:j]


HERO_CSS = between(".glow{", "/* sections */")
NAV_CSS = between("/* nav */", "/* hero: ștampila în lut */")
NAV_CSS += "@media (max-width:1020px){.links{display:none}.menu-btn{display:inline-flex}.nav .btn{display:none}}\n@media (max-width:820px){.nav{padding:14px 16px}.lang{display:none}}\n"
NAV_HTML = between('<header class="nav">', "</header>", True)
NAV_HTML = re.sub(r' onClick="\{\{ openMenu \}\}"', "", NAV_HTML).replace(' aria-expanded="{{ menuOpen }}"', "")
SEAL = between('<div class="seal"', '<div class="copy">')
EDGE = between('<svg class="edge"', "</svg>", True)
MOUNT = between("  componentDidMount() {", "  componentWillUnmount()")
FONTS = re.search(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2\?[^"]*">', src).group(0)

ARROW = '<svg class="ar" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8H13M9 4L13 8L9 12" fill="none" stroke="currentColor" style="stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round"></path></svg>'
VASE = '<svg viewBox="0 0 64 80" aria-hidden="true"><g fill="none" stroke="currentColor" style="stroke-linecap:round;stroke-linejoin:round"><path d="M22 6H42" style="stroke-width:5"></path><path d="M26 7C26 13 27 15 25 18C17 24 12 31 12 43C12 55 19 64 24 72H40C45 64 52 55 52 43C52 31 47 24 39 18C37 15 38 13 38 7" style="stroke-width:3.6"></path><path d="M14.5 35Q32 40 49.5 35M12.6 48Q32 53 51.4 48" style="stroke-width:3.2"></path></g></svg>'
MENU = '<button class="mbtn" type="button" aria-label="Deschide meniul"><svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 7H17M3 13H17" fill="none" stroke="currentColor" style="stroke-width:1.6;stroke-linecap:round"></path></svg></button>'
LOCK = '<p class="rise d1" style="margin: 0" aria-hidden="true"><span class="ava">AVA</span><span class="soul">Art &amp; Soul</span></p>'
H1 = '<h1 class="h1 disp rise d2"><span class="sr">AVA Art &amp; Soul: </span>Autocunoaștere prin creație</h1>'
LEDE = '<p class="lede rise d3">Ateliere cu lut, consiliere și retreaturi pentru momentele în care ai nevoie să te auzi din nou. Pentru tine sau pentru echipa ta.</p>'
CTAS = '<div class="ctas rise d4"><a class="btn btn-cream" href="#pentru-tine">Pentru tine</a><a class="btn btn-line" href="#pentru-companii">Pentru companii</a></div>'
NEXT = '<a class="next rise d4" href="#evenimente"><span class="dot" aria-hidden="true"></span>Următorul atelier:<b class="num">15 noiembrie</b></a>'
BASE_COPY = LOCK + H1 + LEDE + CTAS + NEXT

BASE_CSS = """body{margin:0;background:#F4EDE4}
.pg{--ink:#3A2A20;--paper:#F4EDE4;--cream:#F4EDE4;--cream2:#E3D3BE;--terra-d:#9C472C;--glowc:#F2C79C;--display:'Bodoni Moda',Georgia,serif;--text:'Hanken Grotesk',system-ui,sans-serif;--script:'Pinyon Script',cursive;position:relative;background:var(--paper);color:var(--ink);font:400 17px/1.6 var(--text);-webkit-font-smoothing:antialiased;overflow-x:clip}
.pg a{color:inherit}
.pg a:focus-visible,.pg button:focus-visible{outline:2px solid var(--cream);outline-offset:3px}
.num{font-variant-numeric:tabular-nums lining-nums}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}
.disp{font-family:var(--display);font-weight:400;font-variation-settings:'opsz' 20;letter-spacing:-.01em;text-wrap:balance}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:50px;padding:0 28px;border:0;border-radius:999px;background:var(--ink);color:var(--paper)!important;font:500 15px/1 var(--text);letter-spacing:.02em;text-decoration:none;cursor:pointer;transition:transform .2s cubic-bezier(.2,.7,.2,1),background-color .25s ease,box-shadow .25s ease}
.btn:active{transform:scale(.97)}
.btn-cream{background:var(--cream);color:var(--ink)!important}
.btn-cream:hover{background:#FFF8EE}
.btn-line{background:rgba(244,237,228,.08);color:var(--cream)!important;box-shadow:inset 0 0 0 1px rgba(244,237,228,.5);backdrop-filter:blur(10px)}
.btn-line:hover{background:rgba(244,237,228,.16)}
.ar{width:16px;height:16px;flex:none}
.mbtn{display:none;width:44px;height:44px;border:0;border-radius:999px;background:rgba(244,237,228,.14);color:var(--cream);align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(12px)}
"""
BASE_MQ = """@media (max-width:1020px){.mbtn{display:inline-flex}}
@media (max-width:820px){.hero{min-height:0}.stage{grid-template-columns:1fr;gap:24px;padding:96px 20px 88px}.seal{width:min(64vw,250px)}.hero::after{background:linear-gradient(180deg,rgba(42,20,12,.25) 0%,rgba(42,20,12,.3) 30%,rgba(42,20,12,.55) 42%,rgba(42,20,12,.55) 100%)}.copy{max-width:none}.edge{height:64px}}
@media (prefers-reduced-motion:reduce){.rise{animation:none!important}.sprite{display:none}.pg *{transition:none!important}}
"""

# ---------------------------------------------------------------- headers
HEADERS = {}

HEADERS["Header1Editorial"] = ("Header A: editorial, logo în centru", """
.hn{position:absolute;top:0;left:0;right:0;z-index:20;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;max-width:1280px;margin:0 auto;padding:22px 40px 18px;box-sizing:border-box;color:var(--cream)}
.hn::after{content:"";position:absolute;left:40px;right:40px;bottom:0;height:1px;background:linear-gradient(90deg,rgba(244,237,228,0),rgba(244,237,228,.34) 12%,rgba(244,237,228,.34) 88%,rgba(244,237,228,0))}
.hn ul{display:flex;gap:30px;margin:0;padding:0;list-style:none}
.hn-l{justify-self:start}.hn-r{justify-self:end;display:flex;align-items:center;gap:28px}
.hl{position:relative;display:inline-flex;align-items:center;min-height:44px;font:500 12.5px/1 var(--text);letter-spacing:.18em;text-transform:uppercase;color:rgba(244,237,228,.84);text-decoration:none;transition:color .2s ease}
.hl::after{content:"";position:absolute;left:0;right:0;bottom:11px;height:1px;background:currentColor;transform:scaleX(0);transition:transform .3s cubic-bezier(.2,.7,.2,1)}
.hl:hover{color:var(--cream)}.hl:hover::after{transform:scaleX(1)}
.logo{display:flex;flex-direction:column;align-items:center;gap:6px;text-decoration:none;color:var(--cream)}
.logo svg{width:22px;height:28px}
.logo .w{font:400 26px/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:.34em;margin-right:-.34em}
.logo .s{font:500 9.5px/1 var(--text);letter-spacing:.32em;margin-right:-.32em;color:rgba(244,237,228,.8)}
.lng{display:flex;gap:2px;font:500 12px/1 var(--text);letter-spacing:.14em}
.lng a{display:inline-flex;align-items:center;justify-content:center;min-width:36px;min-height:44px;text-decoration:none;color:rgba(244,237,228,.6)}
.lng a[aria-current]{color:var(--cream)}
.cta{display:inline-flex;align-items:center;gap:10px;min-height:44px;padding:0 0 0 22px;border-left:1px solid rgba(244,237,228,.28);font:500 12.5px/1 var(--text);letter-spacing:.18em;text-transform:uppercase;color:var(--glowc)!important;text-decoration:none}
.cta .ar{transition:transform .3s cubic-bezier(.2,.7,.2,1)}.cta:hover .ar{transform:translateX(4px)}
.stage{padding-top:150px}
@media (max-width:1020px){.hn ul,.hn-r .hl,.lng,.cta{display:none}.hn{grid-template-columns:44px 1fr 44px}.hn-l{display:none}.logo{grid-column:2}.hn-r{grid-column:3}}
""", f"""<header class="hn">
<nav class="hn-l" aria-label="Meniu principal"><ul><li><a class="hl" href="#despre">Despre noi</a></li><li><a class="hl" href="#ce-facem">Ce oferim</a></li><li><a class="hl" href="#evenimente">Evenimente</a></li></ul></nav>
<a class="logo" href="#top" aria-label="AVA Art &amp; Soul, pagina principală">{VASE}<span class="w">AVA</span><span class="s">ART &amp; SOUL</span></a>
<div class="hn-r"><a class="hl" href="#galerie">Galerie</a><a class="hl" href="#contact">Contact</a><div class="lng" role="group" aria-label="Limba site-ului"><a href="#ro" aria-current="true">RO</a><a href="#en" lang="en">EN</a></div><a class="cta" href="#evenimente">Mă înscriu {ARROW}</a>{MENU}</div>
</header>""")

HEADERS["Header2Anunt"] = ("Header B: anunț + bară minimă", """
.hn{position:absolute;top:0;left:0;right:0;z-index:20;color:var(--cream)}
.an{display:flex;justify-content:center;align-items:center;gap:12px;min-height:42px;margin:0;padding:0 16px;background:rgba(24,11,6,.5);backdrop-filter:blur(12px);box-shadow:inset 0 -1px 0 rgba(244,237,228,.12);font:400 13.5px/1.3 var(--text);color:#EFE3D3}
.an i{font-style:normal;color:rgba(244,237,228,.4)}
.an b{font-weight:500;color:var(--cream)}
.an a{display:inline-flex;align-items:center;gap:6px;min-height:42px;margin-left:6px;font-weight:500;color:var(--glowc)!important;text-decoration:none}
.an a .ar{width:14px;height:14px;transition:transform .3s cubic-bezier(.2,.7,.2,1)}.an a:hover .ar{transform:translateX(3px)}
.live{position:relative;width:7px;height:7px;border-radius:50%;background:#A9B88E}
.live::after{content:"";position:absolute;inset:-4px;border-radius:50%;border:1px solid #A9B88E;opacity:0;animation:ping 2.4s cubic-bezier(.2,.7,.2,1) infinite}
@keyframes ping{0%{transform:scale(.6);opacity:.9}100%{transform:scale(1.6);opacity:0}}
.row{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;max-width:1280px;margin:0 auto;padding:16px 40px;box-sizing:border-box}
.logo{display:inline-flex;align-items:center;gap:12px;min-height:44px;text-decoration:none;color:var(--cream);justify-self:start}
.logo svg{width:22px;height:28px}
.logo span{display:flex;flex-direction:column;line-height:1}
.logo .w{font:400 21px/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:.18em}
.logo .s{font:500 9.5px/1 var(--text);letter-spacing:.26em;margin-top:5px}
.row ul{display:flex;gap:6px;margin:0;padding:0;list-style:none}
.row ul a{position:relative;display:inline-flex;align-items:center;min-height:44px;padding:0 14px;font:500 15px/1 var(--text);color:rgba(244,237,228,.78);text-decoration:none;transition:color .2s ease}
.row ul a:hover,.row ul a[aria-current]{color:var(--cream)}
.row ul a[aria-current]::after{content:"";position:absolute;left:50%;bottom:4px;width:4px;height:4px;margin-left:-2px;border-radius:50%;background:var(--glowc)}
.end{justify-self:end;display:flex;align-items:center;gap:12px}
.seg{display:flex;padding:3px;border-radius:999px;background:rgba(244,237,228,.1);box-shadow:inset 0 0 0 1px rgba(244,237,228,.16)}
.seg a{display:inline-flex;align-items:center;justify-content:center;min-width:40px;min-height:38px;border-radius:999px;font:500 12px/1 var(--text);letter-spacing:.1em;color:rgba(244,237,228,.7);text-decoration:none}
.seg a[aria-current]{background:var(--cream);color:var(--ink)}
.end .btn{min-height:44px;padding:0 22px;font-size:14px}
.stage{padding-top:170px}
@media (max-width:1020px){.row ul,.seg,.end .btn{display:none}.an span.hide{display:none}}
@media (max-width:820px){.an{font-size:12.5px;gap:8px}.an .hide{display:none}}
@media (prefers-reduced-motion:reduce){.live::after{animation:none}}
""", f"""<div class="hn">
<p class="an"><span class="live" aria-hidden="true"></span><b>Următorul atelier</b><i aria-hidden="true">·</i><span class="num">duminică, 15 noiembrie, ora 17:00</span><i class="hide" aria-hidden="true">·</i><span class="hide">Cotroceni, sector 5</span><a href="#evenimente">Sold out {ARROW}</a></p>
<header class="row">
<a class="logo" href="#top" aria-label="AVA Art &amp; Soul, pagina principală">{VASE}<span><span class="w">AVA</span><span class="s">ART &amp; SOUL</span></span></a>
<nav aria-label="Meniu principal"><ul><li><a href="#top" aria-current="page">Acasă</a></li><li><a href="#despre">Despre noi</a></li><li><a href="#ce-facem">Ce oferim</a></li><li><a href="#evenimente">Evenimente</a></li><li><a href="#galerie">Galerie</a></li><li><a href="#contact">Contact</a></li></ul></nav>
<div class="end"><div class="seg" role="group" aria-label="Limba site-ului"><a href="#ro" aria-current="true">RO</a><a href="#en" lang="en">EN</a></div><a class="btn btn-cream" href="#evenimente">Mă înscriu</a>{MENU}</div>
</header>
</div>""")

HEADERS["Header3Rama"] = ("Header C: ramă de galerie", """
.frame{position:absolute;top:14px;left:14px;right:14px;bottom:78px;z-index:3;border-radius:26px;box-shadow:inset 0 0 0 1px rgba(244,237,228,.3);pointer-events:none}
.hn{position:absolute;top:14px;left:14px;right:14px;z-index:20;display:flex;align-items:center;justify-content:space-between;gap:24px;padding:26px 44px;color:var(--cream)}
.logo{display:inline-flex;align-items:baseline;gap:12px;min-height:44px;text-decoration:none;color:var(--cream)}
.logo svg{width:20px;height:26px;align-self:center}
.logo .w{font:400 24px/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:.26em}
.logo .s{font:400 26px/1 var(--script);color:var(--glowc)}
.hn ul{display:flex;align-items:center;margin:0;padding:0;list-style:none}
.hn li+li::before{content:"";display:inline-block;width:3px;height:3px;margin:0 16px;border-radius:50%;background:rgba(244,237,228,.4);vertical-align:middle}
.hn ul a{display:inline-flex;align-items:center;min-height:44px;font:500 12.5px/1 var(--text);letter-spacing:.18em;text-transform:uppercase;color:rgba(244,237,228,.8);text-decoration:none;transition:color .2s ease}
.hn ul a:hover,.hn ul a[aria-current]{color:var(--cream)}
.end{display:flex;align-items:center;gap:18px}
.lng{font:500 12px/1 var(--text);letter-spacing:.14em;color:rgba(244,237,228,.6)}
.lng a{display:inline-flex;align-items:center;min-height:44px;padding:0 4px;text-decoration:none}
.lng a[aria-current]{color:var(--cream)}
.ghost{display:inline-flex;align-items:center;min-height:44px;padding:0 22px;border-radius:999px;box-shadow:inset 0 0 0 1px rgba(244,237,228,.55);font:500 12.5px/1 var(--text);letter-spacing:.18em;text-transform:uppercase;color:var(--cream)!important;text-decoration:none;transition:background-color .25s ease,color .25s ease}
.ghost:hover{background:var(--cream);color:var(--ink)!important}
.stage{padding-top:150px}
@media (max-width:1020px){.hn ul,.lng,.ghost{display:none}}
@media (max-width:820px){.hn{padding:16px 22px}.frame{top:8px;left:8px;right:8px;bottom:56px;border-radius:20px}}
""", f"""<div class="frame" aria-hidden="true"></div>
<header class="hn">
<a class="logo" href="#top" aria-label="AVA Art &amp; Soul, pagina principală">{VASE}<span class="w">AVA</span><span class="s">Art &amp; Soul</span></a>
<nav aria-label="Meniu principal"><ul><li><a href="#top" aria-current="page">Acasă</a></li><li><a href="#despre">Despre noi</a></li><li><a href="#ce-facem">Ce oferim</a></li><li><a href="#evenimente">Evenimente</a></li><li><a href="#galerie">Galerie</a></li><li><a href="#contact">Contact</a></li></ul></nav>
<div class="end"><div class="lng" role="group" aria-label="Limba site-ului"><a href="#ro" aria-current="true">RO</a>/<a href="#en" lang="en">EN</a></div><a class="ghost" href="#evenimente">Mă înscriu</a>{MENU}</div>
</header>""")

HEADERS["Header4Sticla"] = ("Header D: bară de sticlă", """
.hn{position:absolute;top:16px;left:16px;right:16px;z-index:20;display:flex;align-items:center;gap:26px;height:66px;padding:0 10px 0 22px;border-radius:20px;corner-shape:squircle;color:var(--cream);background:rgba(28,13,7,.34);backdrop-filter:blur(18px) saturate(130%);-webkit-backdrop-filter:blur(18px) saturate(130%);box-shadow:inset 0 0 0 1px rgba(244,237,228,.14),inset 0 1px 0 rgba(255,240,220,.12),0 18px 40px -20px rgba(0,0,0,.45)}
.logo{display:inline-flex;align-items:center;gap:12px;min-height:44px;padding-right:24px;border-right:1px solid rgba(244,237,228,.16);text-decoration:none;color:var(--cream)}
.logo svg{width:20px;height:26px}
.logo span{display:flex;flex-direction:column;line-height:1}
.logo .w{font:400 20px/1 var(--display);font-variation-settings:'opsz' 20;letter-spacing:.18em}
.logo .s{font:500 9px/1 var(--text);letter-spacing:.26em;margin-top:5px}
.hn ul{display:flex;gap:4px;margin:0;padding:0;list-style:none}
.hn ul a{display:inline-flex;align-items:center;min-height:44px;padding:0 12px;font:500 15px/1 var(--text);color:rgba(244,237,228,.74);text-decoration:none;text-underline-offset:8px;transition:color .2s ease}
.hn ul a:hover{color:var(--cream)}
.hn ul a[aria-current]{color:var(--cream);text-decoration:underline;text-decoration-thickness:1px;text-decoration-color:var(--glowc)}
.end{margin-left:auto;display:flex;align-items:center;gap:14px}
.lng{font:500 12.5px/1 var(--text);letter-spacing:.12em;color:rgba(244,237,228,.55)}
.lng a{display:inline-flex;align-items:center;min-height:44px;padding:0 5px;text-decoration:none}
.lng a[aria-current]{color:var(--cream)}
.pill{display:inline-flex;align-items:center;gap:10px;min-height:46px;padding:0 6px 0 20px;border-radius:14px;corner-shape:squircle;background:var(--cream);color:var(--ink)!important;font:500 14px/1 var(--text);text-decoration:none;transition:background-color .25s ease}
.pill:hover{background:#FFF8EE}
.pill .chip{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;background:var(--ink);color:var(--cream)}
.pill .chip .ar{transition:transform .3s cubic-bezier(.2,.7,.2,1)}.pill:hover .chip .ar{transform:translateX(2px)}
.stage{padding-top:140px}
@media (max-width:1020px){.hn ul,.lng{display:none}}
@media (max-width:820px){.hn{top:10px;left:10px;right:10px;height:60px;padding:0 8px 0 16px}.logo{border:0;padding:0}.pill{display:none}}
""", f"""<header class="hn">
<a class="logo" href="#top" aria-label="AVA Art &amp; Soul, pagina principală">{VASE}<span><span class="w">AVA</span><span class="s">ART &amp; SOUL</span></span></a>
<nav aria-label="Meniu principal"><ul><li><a href="#top" aria-current="page">Acasă</a></li><li><a href="#despre">Despre noi</a></li><li><a href="#ce-facem">Ce oferim</a></li><li><a href="#evenimente">Evenimente</a></li><li><a href="#galerie">Galerie</a></li><li><a href="#contact">Contact</a></li></ul></nav>
<div class="end"><div class="lng" role="group" aria-label="Limba site-ului"><a href="#ro" aria-current="true">RO</a><a href="#en" lang="en">EN</a></div><a class="pill" href="#evenimente">Mă înscriu <span class="chip">{ARROW}</span></a>{MENU}</div>
</header>""")

# ---------------------------------------------------------------- hero texts (with the current capsule header)
TEXTS = {}

TEXTS["Text1Editorial"] = ("Text 1: editorial", """
.eyebrow{display:flex;align-items:center;gap:14px;margin:0;font:500 12px/1 var(--text);letter-spacing:.24em;text-transform:uppercase;color:var(--glowc)}
.eyebrow::before{content:"";width:34px;height:1px;background:currentColor}
.h1{margin-top:22px;font-size:clamp(52px,6vw,92px);line-height:.98}
.lede{margin-top:26px}
.ctas{align-items:center;gap:28px;margin-top:36px}
.go{display:inline-flex;align-items:center;gap:14px;min-height:56px;padding:0 8px 0 28px;border-radius:999px;background:var(--cream);color:var(--ink)!important;font:500 15px/1 var(--text);text-decoration:none;transition:background-color .25s ease}
.go:hover{background:#FFF8EE}
.go .chip{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:50%;background:var(--ink);color:var(--cream);transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.go:hover .chip{transform:rotate(-45deg)}
.tl{display:inline-flex;align-items:center;gap:10px;min-height:44px;font:500 15px/1 var(--text);color:var(--cream)!important;text-decoration:none;background:linear-gradient(currentColor,currentColor) 0 calc(100% - 10px)/100% 1px no-repeat;transition:background-size .3s cubic-bezier(.2,.7,.2,1)}
.tl:hover{background-size:0 1px;background-position:100% calc(100% - 10px)}
.ticket{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:20px;margin-top:40px;padding-top:22px;border-top:1px solid rgba(244,237,228,.22);text-decoration:none;color:var(--ink2)}
.ticket .d{font:400 30px/1 var(--display);font-variation-settings:'opsz' 20;color:var(--cream)}
.ticket .d small{display:block;margin-top:4px;font:500 11px/1 var(--text);letter-spacing:.2em;text-transform:uppercase;color:var(--glowc)}
.ticket .t{font-size:14.5px;line-height:1.45}
.ticket .t b{display:block;font-weight:500;color:var(--cream)}
.ticket .m{display:inline-flex;align-items:center;gap:8px;font:500 14px/1 var(--text);color:var(--glowc)}
.ticket:hover .m .ar{transform:translateX(3px)}.ticket .ar{transition:transform .3s cubic-bezier(.2,.7,.2,1)}
""", f"""<p class="eyebrow rise d1">Conectare · Comunitate · Apartenență</p>{H1}{LEDE}
<div class="ctas rise d4"><a class="go" href="#pentru-tine">Pentru tine <span class="chip">{ARROW}</span></a><a class="tl" href="#pentru-companii">Pentru companii {ARROW}</a></div>
<a class="ticket rise d5" href="#evenimente"><span class="d num">15<small>nov</small></span><span class="t"><b>Atelier de ceramică &amp; socializare</b>duminică, ora <span class="num">17:00</span> · Cotroceni, sector 5 · <span class="num">200</span> lei</span><span class="m">Mă înscriu {ARROW}</span></a>""")

TEXTS["Text2Card"] = ("Text 2: card de eveniment", """
.h1{font-size:clamp(46px,5.2vw,76px)}
.ctas{margin-top:28px}
.card{display:grid;grid-template-columns:auto 1fr;gap:22px;max-width:470px;margin-top:30px;padding:20px 22px;border-radius:22px;corner-shape:squircle;background:rgba(26,12,6,.36);backdrop-filter:blur(16px) saturate(120%);-webkit-backdrop-filter:blur(16px) saturate(120%);box-shadow:inset 0 0 0 1px rgba(244,237,228,.16),inset 0 1px 0 rgba(255,240,220,.1)}
.cal{display:flex;flex-direction:column;align-items:center;justify-content:center;width:76px;padding:10px 0;border-radius:14px;background:var(--cream);color:var(--ink)}
.cal small{font:500 11px/1 var(--text);letter-spacing:.2em;text-transform:uppercase;color:var(--terra-d)}
.cal b{font:400 40px/1 var(--display);font-variation-settings:'opsz' 20;margin:4px 0 2px}
.cal span{font-size:12px;line-height:1}
.info p{margin:0}
.info .k{font:500 11.5px/1 var(--text);letter-spacing:.2em;text-transform:uppercase;color:var(--glowc)}
.info .n{margin-top:8px!important;font:400 22px/1.15 var(--display);font-variation-settings:'opsz' 20;color:var(--cream)}
.info .m{margin-top:6px!important;font-size:14px;color:var(--ink2)}
.row{display:flex;align-items:center;gap:14px;margin-top:14px}
.row .p{font-weight:500;color:var(--cream)}
.row .l{font-size:13.5px;color:var(--glowc)}
.row .btn{margin-left:auto;min-height:44px;padding:0 20px;font-size:14px}
""", f"""{LOCK}{H1}{LEDE}{CTAS}
<div class="card rise d5"><div class="cal" aria-hidden="true"><small>nov</small><b class="num">15</b><span>duminică</span></div>
<div class="info"><p class="k">Următorul atelier</p><p class="n">Atelier de ceramică &amp; socializare</p><p class="m"><span class="num">15 noiembrie 2026</span>, ora <span class="num">17:00</span> (<span class="num">3</span> ore) · Cotroceni, sector 5</p>
<div class="row"><span class="p num">200 lei</span><span class="l">Doar 8 locuri</span><a class="btn btn-cream" href="#evenimente">Mă înscriu</a></div></div></div>""")

TEXTS["Text3Usi"] = ("Text 3: două uși", """
.h1{font-size:clamp(46px,5.4vw,80px)}
.doors{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:34px}
.door{position:relative;display:flex;flex-direction:column;gap:10px;min-height:150px;padding:20px 22px 22px;border-radius:22px;corner-shape:squircle;text-decoration:none;color:var(--cream);background:rgba(244,237,228,.07);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);box-shadow:inset 0 0 0 1px rgba(244,237,228,.22);transition:background-color .3s ease,transform .3s cubic-bezier(.2,.7,.2,1),box-shadow .3s ease}
.door:hover{background:rgba(244,237,228,.13);transform:translateY(-3px);box-shadow:inset 0 0 0 1px rgba(244,237,228,.4),0 20px 40px -24px rgba(0,0,0,.6)}
.pg .door-main{background:var(--cream);color:var(--ink);box-shadow:none}
.door-main:hover{background:#FFF8EE;box-shadow:0 20px 40px -24px rgba(0,0,0,.6)}
.door .k{font:500 11.5px/1 var(--text);letter-spacing:.2em;text-transform:uppercase;opacity:.75}
.door .n{padding-right:44px;font:400 28px/1.05 var(--display);font-variation-settings:'opsz' 20}
.door .t{margin-top:auto;font-size:14px;line-height:1.45;opacity:.85}
.door .chip{position:absolute;top:16px;right:16px;display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:50%;box-shadow:inset 0 0 0 1px currentColor;transition:transform .35s cubic-bezier(.2,.7,.2,1)}
.door:hover .chip{transform:rotate(-45deg)}
@media (max-width:820px){.doors{grid-template-columns:1fr}}
""", f"""{LOCK}{H1}{LEDE}
<div class="doors rise d4"><a class="door door-main" href="#pentru-tine"><span class="n">Pentru tine</span><span class="t">Ateliere de grup · Consiliere 1:1 · Atelier privat 1:1 · Retreaturi</span><span class="chip">{ARROW}</span></a>
<a class="door" href="#pentru-companii"><span class="n">Pentru companii</span><span class="t">Teambuilding și ateliere de wellbeing</span><span class="chip">{ARROW}</span></a></div>
{NEXT}""")

TEXTS["Text4Centrat"] = ("Text 4: centrat, monumental", """
.hero::after{background:radial-gradient(70% 70% at 50% 58%,rgba(42,20,12,.58) 0%,rgba(42,20,12,.42) 55%,rgba(42,20,12,.3) 100%)}
.stage{grid-template-columns:1fr;justify-items:center;gap:8px;padding:112px 40px 150px;text-align:center}
.seal{width:200px}
.copy{max-width:980px;display:flex;flex-direction:column;align-items:center}
.soul{font-size:clamp(40px,3.6vw,54px)}
.h1{margin-top:6px;font-size:clamp(56px,7.6vw,118px);line-height:.96;letter-spacing:-.02em}
.lede{margin:24px auto 0;max-width:46ch}
.ctas{justify-content:center;margin-top:34px}
.ctas .btn{min-width:190px}
.next{margin-top:20px}
""", f"""<span class="soul rise d1" aria-hidden="true">Art &amp; Soul</span>{H1}{LEDE}{CTAS}{NEXT}""")

# ---------------------------------------------------------------- combinations
H1_NOU = '<h1 class="h1 disp rise d2"><span class="sr">AVA Art &amp; Soul: </span><span class="nb">Creație.</span> <span class="nb">Conexiune.</span><br> <span class="nb">Autocunoaștere.</span></h1>'
_t4css = TEXTS["Text4Centrat"][1]
_bcss, _bhtml = HEADERS["Header2Anunt"][1], HEADERS["Header2Anunt"][2]
# combo: no cream "Mă înscriu" in the nav row (the top strip already has it)
_bhtml = _bhtml.replace('<a class="btn btn-cream" href="#evenimente">Mă înscriu</a>', '')
assert 'btn btn-cream' not in _bhtml
COMBOS = {
    "HeroAnuntCentrat": ("Header B + Text 4", _t4css + _bcss + """
.copy{max-width:1140px}
.h1{font-size:clamp(46px,6.3vw,98px);line-height:1;letter-spacing:-.02em}
.lede{max-width:52ch}
.stage{padding-top:150px}
.nb{white-space:nowrap}
@media (max-width:820px){.stage{padding-top:126px}.stage .seal{width:min(46vw,180px)}.h1{font-size:clamp(36px,10.6vw,56px);line-height:1.04}.an{white-space:nowrap}.an b,.an b+i{display:none}.ctas{flex-direction:column;align-items:stretch;width:100%}.ctas .btn{min-width:0}}
""", _bhtml, '<span class="soul rise d1" aria-hidden="true">Art &amp; Soul</span>' + H1_NOU + LEDE + CTAS),
}

# ---------------------------------------------------------------- page
def page(title, extra_css, nav_html, copy_html, nav_css=""):
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
{BASE_CSS}{nav_css}
{HERO_CSS}{extra_css}{BASE_MQ}</style>
</helmet>
<div class="pg" onPointerMove="{{{{ onMove }}}}" onPointerLeave="{{{{ onLeave }}}}">
{nav_html}
<section class="hero" id="top" ref="{{{{ heroRef }}}}">
<div class="glow" aria-hidden="true"></div>
<span class="sprite" aria-hidden="true" ref="{{{{ spriteRef }}}}"></span>
<div class="stage">
{SEAL}<div class="copy">
{copy_html}
</div>
</div>
{EDGE}
</section>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":960}}}}'>
class Component extends DCLogic {{
{MOUNT}  componentWillUnmount() {{ cancelAnimationFrame(this.raf); }}
  renderVals() {{
    var self = this;
    if (!this.cb) {{
      this.T = {{ x: 0, y: 0, on: false }};
      this.cb = {{
        heroRef: function (el) {{ self.hero = el; }},
        stampRef: function (el) {{ self.stamp = el; }},
        spriteRef: function (el) {{ self.sprite = el; }},
        shadeRef: function (el) {{ self.shade = el; }},
        lipRef: function (el) {{ self.lip = el; }},
        wallRef: function (el) {{ self.wall = el; }},
        farRef: function (el) {{ self.far = el; }},
        onMove: function (e) {{
          if (!self.hero) return;
          var h = self.hero.getBoundingClientRect();
          self.T.x = e.clientX - h.left; self.T.y = e.clientY - h.top;
          self.T.on = e.pointerType === 'mouse' && self.T.y < h.height;
        }},
        onLeave: function () {{ self.T.on = false; }}
      }};
    }}
    return this.cb;
  }}
}}
</script>
</body>
</html>
"""

out = []
for name, (title, css, html) in HEADERS.items():
    open(os.path.join(P, name + ".dc.html"), "w", encoding="utf-8").write(page(title, css, html, BASE_COPY))
    out.append(name)
for name, (title, css, html) in TEXTS.items():
    open(os.path.join(P, name + ".dc.html"), "w", encoding="utf-8").write(page(title, css, NAV_HTML, html, NAV_CSS))
    out.append(name)
for name, (title, css, html, copy) in COMBOS.items():
    doc = re.sub(r'<path class="ring"[^>]*></path>\n?', '', page(title, css, html, copy))  # combo: no clay rings at the hero's bottom edge
    open(os.path.join(P, name + ".dc.html"), "w", encoding="utf-8").write(doc)
    out.append(name)
    # phone-width view of the same artboard
    open(os.path.join(P, name + "Mobil.dc.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<title>{title}: mobil</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>body{{margin:0;background:#F4EDE4}}</style>
</helmet>
<div style="width: 390px; background: #F4EDE4">
<dc-import name="{name}" hint-size="390px,900px"></dc-import>
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":390,"height":900}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
""")
    out.append(name + "Mobil")
print("\n".join(out))
